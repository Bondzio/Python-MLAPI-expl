#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# <p><h1>Finding survivors of the titanic tragedy</h1></p>
# <h4>Countering data contamination and attempt at a clean code</h4>

# <p>In this notebook:<ul>
#     <li>We will not be doing a detailed EDA since there are many EDA based notebooks out there on this particular problem (titanic survivors)</li>
#     <li>We will enlist and explain the originally existing features , the features that are extracted , and the features that are removed</li>  
#     <li>We will build an xgboost classifier and a logistic regression classifier using pipelines</li>
#     <li>We will evaluate our models using cross validation</li>
#     <li>We will build a voting ensemble classifier using the above models</li>
#     </ul>

# We will mainly emphasize on the optimal usage of pipelines to reduce risks of data leakage . 

# <h1>DATA PREPROCESSING</h1>

# let us first import out libraries

# In[ ]:


import numpy as np
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_selection import SelectKBest,chi2
from category_encoders.leave_one_out import LeaveOneOutEncoder
from category_encoders.cat_boost import CatBoostEncoder
from scipy.stats import boxcox
from xgboost.sklearn import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold,cross_val_score,GridSearchCV
from matplotlib.ticker import MaxNLocator
import math
import sklearn.pipeline as pip
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import quantile_transform
from sklearn.ensemble import VotingClassifier

import warnings
warnings.filterwarnings("ignore")


# <h3>Let us now look at our features</h3>
# 

# <h3>Originally existing features : (description for these features can be found in the data tab of the titanic competition)</h3>

# In[ ]:


train = pd.read_csv('/kaggle/input/titanic/train.csv')
train.info()


# <p><h3>Features that are extracted : </h3></p>
# <ul><li>'Deck' :    The alphabet (prefix) from the 'Cabin' feature is extracted  as deck .</li>
#     <li>'Title' :    The Title alone is extracted from the 'Name' feature and is binned into the major categories .</li>
#     <li>'Family_Size :    = 'SibSp' + 'Parch' .</li>
#     <li>'Fare_Bin' :    'Fare_Bin' is a feature where the 'Fare' column is binned into different categories (the number and boundaries of these categories were decided while analaysing the data)</li>
#     <li>'Age_grp' :    This is the binned form of the 'Age' column and binnning is done using clustering analysis. The optimal no of clusters (k) of age was found using the sillhouette method (find the maxima on the sillhouette curve) . These k clusters of age were then analyzed and their boundaries were extracted . these boundaries were used to map and bin the 'Age' column into different k different categories . </li>
#     <li>'Fare_per_person' :    = 'Fare' / ('Family_Size'+1)</li>
#     <li>'Age*Class' : = 'Age' x 'Class' </li>
#     <li>'Family_Survival' : This feature is extracted based on the assumption that a family either has the same 'Last_name'(extracted from the 'Name' feature) or the same 'Ticket' . This feature states : if any one person from a family survives , the 'Family_Survival' for all the passengers in the family will be = 1 . Subsequently , if any one person from a family dies , the 'Family_Survival' for the whole family will = 0 . All passengers start out with a basic 'Family_Survival' of 0.5 . </li>
#     <li>'is_alone' : If 'Family_Size' == 0 , then 'is_alone' = 1</li>
#     <li>'has_cabin' : If 'Deck'!='Unknown' , then 'has_cabin' = 1</li>
#     <li>'is_3rdclass' : If 'Pclass' == 3 , then 'is_3rdclass' = 1</li>

# <p><h3>features that will be removed : </h3></p>
# <ul>
# <li>'PassengerId'</li>
# <li>'Name'</li>
# <li>'Ticket'</li>
# <li>'Cabin'</li>
# <li>'Last_Name'</li>
# </ul>
# <p>These features are almost unique for each passenger and advanced processing must be done to make use of these features . Therefore , for simplicity we drop these features . </p>

# <p><h3>Over the course of data preprocessing many functions are used that will help in extracting features</h3></p> 
# <p><h3>All the functions that are used for processing the data and extracting the features are given below  : </h3></p> 

# In[ ]:


"""----------------------DATA PREPROCESSING-----------------------"""
"""method used to extract 'Title' """
def substrings_in_string(big_string, substrings):
    for substring in substrings:
        if big_string.find(substring) != -1:
            return substring
    print (big_string)
    return np.nan

"""PHASE 1 : Extracting 'Deck' , 'Title' , 'Family_Size'"""
def phase1clean(df):
    
    #setting silly values to nan
    df.Fare = df.Fare.map(lambda x: np.nan if x==0 else x)
    
    #Special case for cabins as 'nan' may be signal
    df.Cabin = df.Cabin.fillna('Unknown')    
    cabin_list = ['A', 'B', 'C', 'D', 'E', 'F', 'T', 'G', 'Unknown']
    df['Deck']=df['Cabin'].map(lambda x: substrings_in_string(x, cabin_list))
        
    
    #creating a title column from name
    title_list=['Mrs', 'Mr', 'Master', 'Miss', 'Major', 'Rev',
                'Dr', 'Ms', 'Mlle','Col', 'Capt', 'Mme', 'Countess',
                'Don', 'Jonkheer']
    
    df['Title']=df['Name'].map(lambda x: substrings_in_string(x, title_list))
    
    #replacing all titles with mr, mrs, miss, master
    def replace_titles(x):
        title=x['Title']
        if title in ['Countess','Don', 'Major', 'Capt', 'Jonkheer', 'Rev', 'Col']:
            return 'Rare'
        elif title in ['Countess', 'Mme']:
            return 'Mrs'
        elif title in ['Mlle', 'Ms']:
            return 'Miss'
        elif title =='Dr':
            if x['Sex']=='Male':
                return 'Mr'
            else:
                return 'Mrs'
        else:
            return title
    
    df['Title']=df.apply(replace_titles, axis=1)
    
    #Creating new family_size column
    df['Family_Size']=df['SibSp']+df['Parch']
    
    return df

#---------------------------------------------------------------------------------------

"""Creating 'Fare_Bin' : Binning fare using manually set boundaries"""
def fare_grouping(x):
    # Ranging and grouping Fare using historical data
    bins = [-1, 7.91, 14.454, 31, 99, 250, np.inf]
    names = ['a', 'b','c', 'd', 'e', 'f']
    names = [1, 2, 3, 4, 5, 6]
    x['Fare_Bin'] = pd.cut(x['Fare'], bins ,labels=names).astype('int')
    dict_age={1 : 'a' , 2 : 'b' , 3 : 'c' , 4 : 'd' , 5: 'e' , 6 : 'f'}
    x['Fare_Bin']=x['Fare_Bin'].map(dict_age)
    """visualizing fares"""
    # sns.factorplot(x="Fare_Bin", data=x , kind="count",size=6, aspect=.7)
    # plt.show()
    # sns.scatterplot(x="PassengerId",y="fare_gauss",hue="Fare_Bin",data=x,palette='RdYlGn' , legend='full')
    # plt.show()
    # sns.distplot(x['Age'],axlabel='training set');
    # plt.show()
    return x

#----------------------------------------------------------------------------------------

"""Removing all missing values"""
def fill_nan(x):
    """filling age nan's"""
    null_ind=x.loc[x['Age'].isnull(),:].index
    null_count=x.loc[x['Age'].isnull(),]['PassengerId'].count()
    num_ages=x.groupby('Title')['Age'].mean().to_dict()
    x.loc[x['Age'].isnull(),'Age']=x.loc[x['Age'].isnull(),'Title'].map(num_ages)

    
    """filling fare and binning fare"""
    null_ind=x.loc[x['Fare'].isnull(),:].index
    null_count=x.loc[x['Fare'].isnull(),]['PassengerId'].count()
    num_fare=x.groupby('Pclass')['Fare'].mean().to_dict()
    x.loc[x['Fare'].isnull(),'Fare']=x.loc[x['Fare'].isnull(),'Pclass'].map(num_fare)
    fare_grouping(x)
    
    """removing embarked nan's"""
    f_index=x[x['Embarked'].isnull()].index
    x=x.drop(f_index,axis=0)
    
    return x

#----------------------------------------------------------------------------------------

"""Creating 'Age_Grp' : Binning age using silhouette method and clustering """
def age_grouping(x):
    """visualizing age feature"""
    # sns.distplot(x['Age'],axlabel='training set');
    # plt.show()
    # sns.factorplot(x="Age_Grp", data=x , kind="count",size=6, aspect=.7)
    # plt.show()
    # sns.factorplot(x="Age_Grp",col="Survived", data=x , kind="count",size=6, aspect=.7)
    # plt.show()
    k_data=pd.concat([x['Age'],x['Survived']],axis=1)
    k_data.rename( columns={ 0 :'Age' , 1 :'Survived'}, inplace=True )
    """finding optimal no of clusters using silhouette method"""
    model = KMeans()
    sil = []
    # dissimilarity would not be defined for a single cluster, thus, minimum number of clusters should be 2
    for k in range(2, 9):
      kmeans = KMeans(n_clusters = k).fit(k_data)
      labels = kmeans.labels_
      sil.append(silhouette_score(k_data, labels, metric = 'euclidean'))
    plt_data=pd.concat([pd.Series(range(2,9)),pd.Series(sil)],axis=1)
    plt_data.rename( columns={ 0 :'clusters' , 1 :'silhouette scores'}, inplace=True )
    """visualizing the silhouette score plot"""
    # ax = sns.lineplot(x="clusters", y="silhouette scores",
    #                   estimator=None, lw=1,
    #                   err_style="bars", ci=68, 
    #                   data=plt_data)
    kmeans = KMeans(n_clusters=4, random_state=0).fit(k_data)
    labels_=kmeans.labels_
    k_data['age_grp']=labels_+1
    k_data['Passenger_Id']=x['PassengerId']
    """visualizing the distribution of passengers of each cluster"""
    # sns.scatterplot(x="Passenger_Id",y="Age",data=k_data,hue="age_grp",palette='viridis' , legend='full')
    # plt.show()
    # age_grp_survcount=x.loc[x['Survived']==1,:].groupby('Age_Grp')['Survived'].count()
    
    """finding boundaries of the clusters"""
    #age_grp_max=k_data.groupby('Age_Grp').Age.max()
    #age_grp_min=k_data.groupby('Age_Grp').Age.min()
    """making the boundary map for the different clusters """
    agelist=[] 
    for i in range(0, 15):
        agelist.append('a')
    for i in range(15, 29):
        agelist.append('b')
    for i in range(29, 45): 
        agelist.append('c')
    for i in range(45, 90):
        agelist.append('d')
    age_dict={v: k for v, k in enumerate(agelist)}
    x['Age_Grp']=x['Age'].astype(int).map(age_dict)

    return x,age_dict

#---------------------------------------------------------------------------------------------

"""Creating 'Family_Survived' feature"""
def survived_fams(df):
    # A function working on family survival rate using last names and ticket features
    df['Last_Name'] = df['Name'].apply(
        lambda df: str.split(df, ",")[0])
    
    # Adding new feature: 'Survived'
    default_survival_rate = 0.5
    df['Family_Survival'] = default_survival_rate
    
    for grp, grp_df in df[['Survived', 'Name', 'Last_Name', 'Fare', 'Ticket', 'PassengerId','SibSp', 'Parch', 'Age', 'Cabin']].groupby(['Last_Name', 'Fare']):
    
        if (len(grp_df) != 1):
            # A Family group is found.
            for ind, row in grp_df.iterrows():
                smax = grp_df.drop(ind)['Survived'].max()
                smin = grp_df.drop(ind)['Survived'].min()
                passID = row['PassengerId']
                if (smax == 1.0):
                    df.loc[df['PassengerId'] ==
                                  passID, 'Family_Survival'] = 1
                elif (smin == 0.0):
                    df.loc[df['PassengerId'] ==
                                  passID, 'Family_Survival'] = 0
    
    for _, grp_df in df.groupby('Ticket'):
        if (len(grp_df) != 1):
            for ind, row in grp_df.iterrows():
                if (row['Family_Survival'] == 0) | (
                        row['Family_Survival'] == 0.5):
                    smax = grp_df.drop(ind)['Survived'].max()
                    smin = grp_df.drop(ind)['Survived'].min()
                    passID = row['PassengerId']
                    if (smax == 1.0):
                        df.loc[df['PassengerId'] ==
                                      passID, 'Family_Survival'] = 1
                    elif (smin == 0.0):
                        df.loc[df['PassengerId'] ==
                                      passID, 'Family_Survival'] = 0
    
    
    return df

#---------------------------------------------------------------------------------------------

"""Creating 'is_alone' feature"""
def is_alone(x):
    fam_list={False : 0 , True : 1}
    x['is_alone'] = (x['Family_Size']==0).map(fam_list)
    """visualization"""
    # sns.factorplot(x="is_alone", data=clean_train_reg , kind="count",size=6, aspect=.7)
    # f_1=clean_train_reg[clean_train_reg['Survived']==1].groupby('is_alone')['Survived'].count()
    # f_0=clean_train_reg[clean_train_reg['Survived']==0].groupby('is_alone')['Survived'].count()
    # f_s=f_1/f_1+f_0
    return x

#---------------------------------------------------------------------------------------------

"""Creating 'has_cabin' feature"""
def has_cabin(x):
    fam_list={False : 0 , True : 1}
    x['has_cabin'] = (x['Deck']!='Unknown').map(fam_list)
    """visualization"""
    return x
    
#---------------------------------------------------------------------------------------------

"""Creating 'is_3rdclass' feature"""    
def is_3stclass(x):
    class_list={False : 0 , True : 1}
    x['is_3rdclass'] = (x['Pclass']== 3 ).map(class_list)
    """visualization"""
    return x

#---------------------------------------------------------------------------------------------

"""Coverting Pclass.type from 'int' to 'object' """ 
def class_categorizer(x):
    dict_class={1 : 'a' , 2 : 'b' , 3 : 'c' }
    x['Pclass']=x['Pclass'].map(dict_class)
    return x

#---------------------------------------------------------------------------------------------


"""PHASE 2 : Extracting 'Age_Grp' , 'Fare_Per_Person' , 'Age*Class' , 'Family_Survival' , 'is_alone' , 'has_cabin' , 'is_3rdclass' """
def phase2clean(train, test):
            #data type dictionary
    # data_type_dict={'Pclass':'ordinal', 'Sex':'nominal', 
    #                 'Age':'numeric', 
    #                 'Fare':'numeric', 'Embarked':'nominal', 'Title':'nominal',
    #                 'Deck':'nominal', 'Family_Size':'ordinal'}      
    
    
    #imputing nan values
    train=fill_nan(train)
    train,age_dict=age_grouping(train)
    test=fill_nan(test)
    test['Age_Grp']=test['Age'].astype(int).map(age_dict)
    
    
    #Fare per person
    for df in [train, test]:
        df['Fare_Per_Person']=df['Fare']/(df['Family_Size']+1)
    
    #Age times class
    for df in [train, test]:
        df['Age*Class']=df['Age']*df['Pclass']


    combined=pd.concat([train,test])
    combined=survived_fams(combined)
    combined=is_alone(combined)
    combined=has_cabin(combined)
    combined=is_3stclass(combined)
    train=combined.iloc[:len(train),:]
    test=combined.iloc[len(train):,:]
    test=test.drop(['Survived'],axis=1)
    
    return [train,test]

#---------------------------------------------------------------------------------------------

"""Container function for all the data preprocessing methods"""
"""It also handles the removal of the unwanted features ,it also returns the original training and test datasets """
def get_data():
    train_data = pd.read_csv('/kaggle/input/titanic/train.csv')
    submit_x =pd.read_csv('/kaggle/input/titanic/test.csv')
    original_train = pd.read_csv('/kaggle/input/titanic/train.csv')
    original_test = pd.read_csv('/kaggle/input/titanic/test.csv')
    x=phase1clean(train_data)
    pred_set=phase1clean(submit_x)
    x,pred_set=phase2clean(x, pred_set)
    x=x.drop(['PassengerId','Name','Ticket','Cabin','Last_Name'],axis=1)
    pred_set=pred_set.drop(['PassengerId','Name','Ticket','Cabin','Last_Name'],axis=1)
    y = x.Survived
    x = x.loc[:,x.columns!='Survived'] 
    return x,y,pred_set,original_train,original_test

#---------------------------------------------------------------------------------------------





# <h4>We will now implement the data preprocessing and have a look at out processed data</h4>  

# In[ ]:


x,y,pred_set,original_train,pred_set_original=get_data()
x.info()
x.head()


# <h1>MODELLING</h1>

# <p><h3>pipeline_xgb :</h3><ul>
#     <li></li>
#     </ul>
# 
# 
# <p><h3>Pipelines : </h3><ul>
#     <li>Pipelines act as a reusable container of different transformers that need to be used in a particular order , repeatedly . </li>
#     <li>Pipelines make the code look cleaner , make the workflow easier , and makes your work reproducible.</li>
#     <li>Pipelines use a systematic stepwise approach , this approach avoids train-test data contamination .</li>
#     </ul></p>
# <p><h4>We will be using 2 different pipelines in this notebook :</h4> <ol>
#     <li>pipeline_xgb : Pipeline contains XGBClassifier() and  xgboost specific data preprocessing </li>
#     <li>pipeline_log : Pipeline contains LogisticRegression() and  logistic regression specific data preprocessing </li>
#     </ol></p>
# <p><h3>pipeline_xgb : Elements</h3><ol>
#     <li>Changing 'Pclass' to type : 'object' . </li>
#     <li>Applying CatBoostEncoder() to all the categorical features .</li>
#     <li>selecting optimum k features based on chi2 .</li>
#     <li>containing the classifier .</li>
#     </ol>
# <p><h3>pipeline_log : Elements</h3><ol>
#     <li>Changing 'Pclass' to type : 'object' . </li>
#     <li>Applying CatBoostEncoder() to all the categorical features .</li>
#     <li>Applying Quantile transformer to all the numerical features to make them normally distributed . </li>
#     <li>selecting optimum k features based on chi2 .</li>
#     <li>containing the classifier .</li>
#     </ol>
# 
# <p><h3>pipeline_xgb implemention is given below :</h3><ul>

# In[ ]:


"""converting functions to transformers"""
from sklearn.preprocessing import FunctionTransformer
class_cat=FunctionTransformer(class_categorizer)
quantile_transformer = FunctionTransformer(quantile_transform)


"""xgboost pipe_line"""
cat_features=['Title', 'Deck' ,'Pclass' , 'Sex' , 'Embarked' , 'Age_Grp' , 'Fare_Bin']
num_features = list(x.select_dtypes(include=['int64','float64']).columns)
categorical_transformer = pip.Pipeline(steps=[('class_cat',class_cat),
                                              ('enc', CatBoostEncoder())
                                              ])
numerical_transformer = pip.Pipeline([('just','passthrough')])
preprocessor = ColumnTransformer(transformers=[('cat', categorical_transformer , cat_features),
                                               ('num' , numerical_transformer , num_features)
                                               ])
pipeline_xgb =pip.Pipeline(steps=[('preprocessor', preprocessor),
                                  ('feature_select', SelectKBest(chi2 , k = 15)),
                                  ('classifier',XGBClassifier(learning_rate=0.01 ,
                                                              n_estimators=860,
                                                              max_depth=3,
                                                              subsample=1,
                                                              colsample_bytree=1,
                                                              gamma=6,
                                                              reg_alpha = 14,
                                                              reg_lambda = 3))
                                  ])

#---------------------------------------------------------------------------------------------

"""model evaluation"""
cv = StratifiedKFold(5, shuffle=True, random_state=42)
accuracies = cross_val_score(pipeline_xgb, x , y , cv = cv)
print("5 fold cross validation accuracies {}".format(accuracies))


#  <h4> <p>Parameters of the transformers were already tuned using gridsearchCV .</p><p>Given below is the template used to optimize the hyperparameters of the transformers.</p> </h4>

# In[ ]:


"""Template used for hyperparameter tuning"""
params=[{
    # 'classifier__n_estimators' : [i for i in range(700,910,10)]
    # 'classifier__subsample' : [i/100 for i in range(80,101)]
    'feature_select' : [SelectKBest(chi2)],
    'feature_select__k' : [i for i in range(5,19)]
    }]

cv = StratifiedKFold(5, shuffle=True, random_state=42)

search=GridSearchCV(estimator=pipeline_xgb,
                    param_grid=params,
                    n_jobs=-1,
                    cv=cv)

search.fit(x, y)
print("best score : {}  , best params : {}  ".format(search.best_score_ , search.best_params_))
#search.cv_results_


# <p><h3>pipeline_log implemention is given below :</h3><ul>

# In[ ]:


"""logistic regression pipeline"""
cat_features=['Title', 'Deck' ,'Pclass' , 'Sex' , 'Embarked' , 'Age_Grp' , 'Fare_Bin']
num_features = list(x.select_dtypes(include=['int64','float64']).columns)
categorical_transformer = pip.Pipeline(steps=[('class_cat',class_cat),
                                              ('enc', CatBoostEncoder())
                                              ])
numerical_transformer = pip.Pipeline([('normal_trans',quantile_transformer)])
preprocessor = ColumnTransformer(transformers=[('cat', categorical_transformer , cat_features),
                                               ('num' , numerical_transformer , num_features)])
pipeline_log =pip.Pipeline(steps=[('preprocessor', preprocessor),
                                  ('feature_select',SelectKBest(chi2, k = 17 )),
                                  ('classifier',LogisticRegression(penalty = 'l2',
                                                                   solver = 'liblinear',
                                                                   C = 0.25))
                                  ])

#---------------------------------------------------------------------------------------------

"""model evaluation"""
cv = StratifiedKFold(5, shuffle=True, random_state=42)
accuracies = cross_val_score(pipeline_log, x , y , cv = cv)
print("5 fold cross validation accuracies {}".format(accuracies))


# <p><h1>ENSEMBLE : Weighted Voting classifier</h1></p>
# <h4><ul>
#     <li>Voting classifier considers the majority prediction among the predictions of the various classifiers</li>
#     <li>Classifiers included in ensemble models must be diverse by function and by the features they are trained on for maximum benefit.</li>
#     </ul></h4>
# <p><h4>We will use sklearn implementation of weighter voting classifier ( class sklearn.ensemble.VotingClassifier() ) which will contain pipeline_xgb and pipeline_log as its estimators .</h4></p>

# In[ ]:


classifier = VotingClassifier(estimators=[('XGB', pipeline_xgb), ('LOG', pipeline_log)])

"""model evaluation"""
cv = StratifiedKFold(5, shuffle=True, random_state=42)
accuracies = cross_val_score(classifier, x , y , cv = cv)
print("5 fold cross validation accuracies {}".format(accuracies))


# <p><h4>We see that the weighted voting classifier is more stable than its estimators when they are seperate .</h4></p>
# <p><h4>We will now proceed to making our submition using our ensemble model .</h4></p>

# In[ ]:


classifier.fit(x,y)
y_submit=pd.Series((classifier.predict(pred_set)))
y_submit=y_submit.astype(int)
y_1=pred_set_original.PassengerId
y_submit_f=pd.concat([y_1,y_submit],axis=1)
y_submit_f.rename( columns={ 0 :'Survived'}, inplace=True )
y_submit_f.to_csv('submission.csv',index=False)        


# <h3> hope this helps all the readers  .  if u like this notebook , give an upvote to keep me motivated  . critical comments are appreciated  , cheers :) 
