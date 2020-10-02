#!/usr/bin/env python
# coding: utf-8

# # Titanic Disaster - Predicting Survivability Using Classification Techniques

# In this Analysis, I think, tried to cover as much Machine Learning Concepts as applicable so there is enough Hands On. 
# Please feel free to comment (and upvote if you like) , as this keeps me motivated :) 

# Following is the flow of Analysis :  
# - Stage 1 - Apply standard Data Cleaning techniques, Treat Outliers , Derive Features as applicable
# - Stage 2 - EDA - Data Visualisation and Inferences
# - Stage 3 - Data Preparation for Modelling - Apply Dimensionality Reduction (PCA) and Balance the classes as appropriate
# - Stage 4 - Train ML models and derive the associated metrics
# - Stage 5 - Derive the prominent features 
# - Stage 6 - Metric and Model Selection 
# - Stage 7 - Predict Labels for Test Data

# Please Note that - I have detailed some inferences/notes with in Markdown cells. Code level comments are with in the code cells.

# In[ ]:


# Import the required Libraries 

# Data Handling
import pandas as pd
import numpy as np
import warnings

# Visualization
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

# Data pre-processing - Scaling
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Feature Dimension Engineering
from sklearn.decomposition import PCA
from sklearn.decomposition import IncrementalPCA
from sklearn.feature_selection import RFE
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
import statsmodels.api as sm
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier

# Model Tuning 
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV

# Calculate Metrics
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score
from sklearn.metrics import roc_auc_score,roc_curve,scorer,precision_recall_curve 
from sklearn import metrics
from scipy.stats import norm

# Set the session options
get_ipython().run_line_magic('matplotlib', 'inline')
pd.options.display.max_columns = None
pd.options.display.max_rows = None
warnings.filterwarnings("ignore")
pd.options.display.float_format = '{:,.2f}'.format


# In[ ]:


# Read train data into Dataframe
train_data=pd.read_csv('../input/train.csv')
# Read test data into Dataframe
test_data=pd.read_csv('../input/test.csv')
# Check the dimensions
print('Train Size: ',train_data.shape)
print('Test Size: ',test_data.shape)


# In[ ]:


# Get the feel of train data
train_data.head()


# In[ ]:


# Get the feel of test data
test_data.head()


# # Stage - 1
# The idea is to merge the training and test data after  - 
# - Ensuring that the two data frames can be stacked (are same size). 
# - Can be easily seperable based on a flag, when we needed.
# 
# Then investigate each of the feature and apply the clean techniques as applicable.

# In[ ]:


# Add a feature called 'flag' to train and test data. This feature is used to distinguish train from test data.
# Also, add 'Survived' feature to test and initialise that to a dummy variable ..say '9' in this case.
test_data['flag']='test'
train_data['flag']='train'
test_data['Survived']='9'

# Vertically stack the train and test data and check shape
data=train_data.append(test_data)
print('Stacked data size: ',data.shape)

# Get the feel of the merged data
data.head()


# Clearly the data is not clean - there are NaNs, categorical variables etc.. which needs to be treated. 
# The following lines details the idea of data cleaning methodology at high level - 
# - For numeric features, I will take the mean or median as the value to impute.
# - For the features that have too many NaNs or very less unique ness will be excluded from the analysis.
# - Apply one hot encoding for the categorical variables

# In[ ]:


# Age - Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.Age.dtype)
print('Number of Unique values: ',data.Age.nunique())
print('Number of NaNs : ', data.Age.isnull().sum(axis=0))


# In[ ]:


# Age - Calculate the mean and median for various Segments. 
#How the mean / median varies with in train, test data and with in Survived and Not survived data points. 

print(data[data['flag']=='train'].groupby(['Survived'])['Age'].mean())
print(data[data['flag']=='train'].groupby(['Survived'])['Age'].median())

print('Mean Age of full data  ', data.Age.mean())
print('Median Age of full data  ', data.Age.median())

print('Mean Age of full test data  ', data[data['flag']=='test'].Age.mean())
print('Median Age of full test data  ', data[data['flag']=='test'].Age.median())

print('Mean Age of full train data  ', data[data['flag']=='train'].Age.mean())
print('Median Age of full train data  ', data[data['flag']=='train'].Age.median())


# So, from the above statistics, it is evident that the test data is slightly skewed than the train data. But, if we consider the 'Full data'( train + test), the mean and median are almost close. So, I have decided to impute the NaNs of Age feature with the median of Full data. Mean values have some bearing of outliers and therefore, it is always a good practive to choose median to impute NaNs.

# In[ ]:


# Impute the NaNs with median 
data.Age=data.Age.fillna(data.Age.median())

print('Mean Age of full data  ', data.Age.mean())
print('Median Age of full data  ', data.Age.median())

# Print the dist plots to see how the feature is distributed
plt.subplot(1,2,1)
plt.title('Train')
sns.distplot(data[data['flag']=='train']['Age'])
plt.subplot(1,2,2)
plt.title('Test')
sns.distplot(data[data['flag']=='test']['Age'])
plt.show()


# In[ ]:


# Cabin - Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.Cabin.dtype)
print('Number of Unique values: ',data.Cabin.nunique())
print('Number of NaNs : ', data.Cabin.isnull().sum(axis=0))


# In[ ]:


print('Unique values: ',list(data.Cabin.unique()))


# So, 'Cabin' has high degree of variation, and also, the number of NaNs are 1014 - which is ~77% of total data. I choose to ignore this feature in my analysis.Please note that, before arriving to this conclusion, I tried extracting the first charecter of the Cabin and then encoded that to a numeric value( one -hot encoding). I have used a seperate Cabin 'XOC' to fill the vlaues. But, this methodology has introuduced lot of bais in my models. So, I have removed the feature. 

# I left all that code in comments, just to show how I handled this variable - if some one can give any better idea , that really helps :) 

# In[ ]:


#data['Cabin']=data['Cabin'].fillna('XOC')
#data['Cabin_code']=data['Cabin'].apply(lambda x: str(x[0]))
#print('Number of Unique values: ',data.Cabin_code.nunique())
#print('Unique values: ',data.Cabin_code.unique())
#print('Number of NaNs : ', data.Cabin_code.isnull().sum(axis=0))

# Convert cabin_code to dummies
#CC_dummies = pd.get_dummies(data['Cabin_code'], drop_first=True)
#data=pd.concat([CC_dummies,data],axis=1)


# In[ ]:


# Embarked - Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.Embarked.dtype)
print('Number of Unique values: ',data.Embarked.nunique())
print('Number of NaNs : ', data.Embarked.isnull().sum(axis=0))
print('Number of Train NaNs : ', data[data['flag']=='train']['Embarked'].isnull().sum(axis=0))
print('Number of Test NaNs : ', data[data['flag']=='test']['Embarked'].isnull().sum(axis=0))


# In[ ]:


# See what are those Unique Values
print('Unique values: ',data.Embarked.unique())


# In[ ]:


#Check how the 'Embarked' code is distributed across the data 
data.groupby(['Embarked','flag'])['Survived'].count()


# In[ ]:


# Check how Embarked is distributed across the other features 
data[data['flag']=='train'].groupby(['Embarked','Survived','Sex'])['PassengerId'].count()


# In[ ]:


# Check the data that has 'Embarked' code as NaN
data[data['Embarked'].isnull()]


# Quite a few findings here , that gave me a clue on how to impute the missing values :  
# - The most common 'Embarked' code in test and train data is 'S'
# - There are no NaNs in test data, but there are 2 NaNs in Train data.
# - The 'Sex' of the two passengers who have missing Embarked Code is 'female' anf they both survived.
# - From the 'groupby' statistic above,we can see, there is higher chance, that a passenger has Embarked code 'S', if the sex is 'female' and they have 'survived'.

# So, I will impute 'S' for the missing 'Embarked' codes.

# In[ ]:


# Impute 'S' for NaNs in Embarked code
data['Embarked']=data['Embarked'].fillna('S')
print('Number of NaNs : ', data.Embarked.isnull().sum(axis=0))

# Convert Embarked to dummies
EM_dummies = pd.get_dummies(data['Embarked'], drop_first=True)
data=pd.concat([EM_dummies,data],axis=1)


# In[ ]:


# Fare - Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.Fare.dtype)
print('Number of Unique values: ',data.Fare.nunique())
print('Number of NaNs : ', data.Fare.isnull().sum(axis=0))


# In[ ]:


data[data['Fare'].isnull()]


# In[ ]:


print(data[data['flag']=='train'].groupby(['Survived'])['Fare'].mean())
print(data[data['flag']=='train'].groupby(['Survived'])['Fare'].median())
print(data[data['flag']=='train'].groupby(['Survived'])['PassengerId'].count())
print(data[data['flag']=='train'].groupby(['Survived'])['PassengerId'].count())
print('Mean Fare of full data  ', data.Fare.mean())
print('Median Fare of full data  ', data.Fare.median())
print('Mean Fare of full test data  ', data[data['flag']=='test'].Fare.mean())
print('Mean Fare of full train data  ', data[data['flag']=='train'].Fare.mean())
print('Median Fare of full test data  ', data[data['flag']=='test'].Fare.median())
print('Median Fare of full train data  ', data[data['flag']=='train'].Fare.median())


# The investigation is much similar to what i have done for Age. I have decided to impute the ,missing Fare with the median value of Full data.

# In[ ]:


# Impute the median value 
data['Fare']=data['Fare'].fillna(data['Fare'].median())


# In[ ]:


# Print the dist plots to see how the feature is distributed
plt.subplot(1,2,1)
plt.title('Train')
sns.distplot(data[data['flag']=='train']['Fare'])
plt.subplot(1,2,2)
plt.title('Test')
sns.distplot(data[data['flag']=='test']['Fare'])
plt.show()


# In[ ]:


# Name - Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.Name.dtype)
print('Number of Unique values: ',data.Name.nunique())
print('Number of NaNs : ', data.Name.isnull().sum(axis=0))


# Too many unique values. I will choose to ignore this cloumn. We might be loosing some potential information by ignoring this column. Instead of ignoring the column, we can derive some features for example - from the titles - Mr., Miss, Mrs etc... but for now, I will go with ignoring the column. 

# In[ ]:


#Parch Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.Parch.dtype)
print('Number of Unique values: ',data.Parch.nunique())
print('Number of NaNs : ', data.Parch.isnull().sum(axis=0))


# In[ ]:


# See what are those Unique Values
print('Unique values: ',data.Parch.unique())


# In[ ]:


# PassengerId - Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.PassengerId.dtype)
print('Number of Unique values: ',data.PassengerId.nunique())
print('Number of NaNs : ', data.PassengerId.isnull().sum(axis=0))


# In[ ]:


# Pclass - Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.Pclass.dtype)
print('Number of Unique values: ',data.Pclass.nunique())
print('Number of NaNs : ', data.Pclass.isnull().sum(axis=0))


# In[ ]:


# See what are those Unique Values
print('Unique values: ',data.Pclass.unique())


# In[ ]:


# Sex Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.Sex.dtype)
print('Number of Unique values: ',data.Sex.nunique())
print('Number of NaNs : ', data.Sex.isnull().sum(axis=0))


# In[ ]:


# See what are those Unique Values
print('Unique values: ',data.Sex.unique())


# In[ ]:


# Convert Embarked to dummies
Sex_dummies = pd.get_dummies(data['Sex'], drop_first=True)
data=pd.concat([Sex_dummies,data],axis=1)


# In[ ]:


#SibSp Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.SibSp.dtype)
print('Number of Unique values: ',data.SibSp.nunique())
print('Number of NaNs : ', data.SibSp.isnull().sum(axis=0))


# In[ ]:


# See what are those Unique Values
print('Unique values: ',data.SibSp.unique())


# In[ ]:


#Ticket  Find the data type, Unique values and Number of NaNs
print('Dtype: ',data.Ticket.dtype)
print('Number of Unique values: ',data.Ticket.nunique())
print('Number of NaNs : ', data.Ticket.isnull().sum(axis=0))


# In[ ]:


# Derive a new feature which is the sum of siling count and parent count 
#data['Mem_size']=data['SibSp']+data['Parch']


# In[ ]:


#Delete unnecessary cols
data_cleaned=data.drop(columns=['Cabin','Embarked','Name','PassengerId','Sex','Ticket'])


# In[ ]:


print(data_cleaned.shape)
data_cleaned.head()


# # Stage 2: Visualisation to understand Data statistically

# In[ ]:


# Write a function to display subplots of box plot for given variables.
def box_plot(k,fx=16,fy=8):
    fig=plt.figure(figsize=(fx, fy), dpi=70, facecolor='w', edgecolor='k')
    sns.set(style="darkgrid")
    i=1
    for col in k:
        plt.subplot(2,3,i)
        sns.boxplot(y=col,
                    x='Survived',
                palette='pastel',
                data=data_cleaned[data_cleaned['flag']=='train'])
        i=i+1

plt.show()

# Write a function to display subplots of bar plot for given variables.
def count_plot(k,fx=14,fy=10,df=data_cleaned):
    fig=plt.figure(figsize=(fx, fy), dpi=90, facecolor='w', edgecolor='k')
    sns.set(style="darkgrid")
    i=1
    for col in k:
        plt.subplot(4,2,i)
        plt.xticks(rotation='horizontal')
        ax=sns.countplot(x=col,
            data=df[df['flag']=='train'],
            palette='pastel',
            hue='Survived',
            order=data_cleaned[col].value_counts().index)  
        i=i+1
    
    
plt.show()


# In[ ]:


box_plot(['Age','Fare'])


# From the box plots, what I can infer is:
#  - Most of the passengers with lower and higer end of Age have not survived.
#  - The is however remarkably higher aged passenger survived. - This can be counted as an outlier.
#  - Fare is skewed. We can apply a logrithmic transformation to even the feature.
#  - Again, a higher Fare - an outlier can be seen. 

# In[ ]:


# See the percentiles of the Age
data_cleaned.Age.describe(percentiles=[0.25,0.5,0.75,0.95,0.99])


# In[ ]:


# Cap the Age at 99 percentile - this meant any Age more than 99 percentile will be capped 
a=np.percentile(data_cleaned.Age,99.00)
data_cleaned.Age=data_cleaned['Age'].apply(lambda x: a if x > a else x)


# In[ ]:


box_plot(['Age'])


# In[ ]:


# Apply logrithmic transformation on Fare
data_cleaned['Fare_log']=data_cleaned['Fare'].apply(lambda x: np.log(x))


# In[ ]:


# Check the Fare_log distribution
box_plot(['Fare_log'])


# So, it appears, that higher is the fare, higher is the chance of survival.

# In[ ]:


count_plot(['Pclass','male','Q','S'])


# What I can infer from above count plots :
# 
# - Chance of Survival is higher in class 1 and 2 compared to class 3. However, this can be offset by the reason, that there are large number of travellers in class 3.
# - The chance of Survival is higher for femal passenger than a male passenger.

# In[ ]:


count_plot(['SibSp','Parch'])


# In[ ]:


fig=plt.figure(figsize=(18, 16), dpi=50, facecolor='w', edgecolor='k')
sns.set(style="ticks", palette="pastel")
ax = sns.heatmap(data_cleaned.corr(),annot=True)


# There are some cases of string correlation , for example :
#  - Pclass and Logrithmic transformation of Fare
#  - Q and S ('Embarked') are correlated

# # Stage 3: Data preparation for modelling

# In[ ]:


# Remove logrithmic transformations as we will do standardisation
data_cleaned.drop(columns=['Fare_log'],axis=1,inplace=True)
data_cleaned.head()


# In[ ]:


# prepare the x and y variables
x_train = data_cleaned[data_cleaned['flag']=='train'].drop(columns=['Survived','flag'],axis=1)
y_train = data_cleaned[data_cleaned['flag']=='train']['Survived']
x_test = data_cleaned[data_cleaned['flag']=='test'].drop(columns=['Survived','flag'],axis=1)

print('shape of x - Full train data: ', x_train.shape)
print('shape of y - Full train data: ', y_train.shape)
print('shape of x - Full test data: ', x_test.shape)

# Split the training set into training and validation set (80:20)
x_train_set, x_val_set, y_train_set, y_val_set = train_test_split(x_train,y_train, train_size=0.8,test_size=0.2,random_state=100)
print(y_train.mean())
print(y_train.value_counts())

print('shape of x - Model train data: ', x_train_set.shape)
print('shape of x - Model Validate data: ', x_val_set.shape)
print('shape of y - Model train data: ', y_train_set.shape)
print('shape of y - Model Validate data: ', y_val_set.shape)


# Average value of y_train is 38.38% percent which meant, 38% of the data has Survival cases. So the data is fairly balanced and we don't have to apply imbalance techniques

# In[ ]:


# Define a function for Standardizing the values
def scaler_f(a):
    cols=list(a)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(a)
    scaled_frame=pd.DataFrame(scaled, columns=cols)
    return scaler,scaled_frame


# Define a function for PCA
def pca_show(a):
    pca = PCA(svd_solver='randomized', random_state=42)
    pca_frame=pca.fit(a)
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance')
    plt.show()
    
# Incremental PCA
def pca_incr(a,n):
    pca_mo = IncrementalPCA(n_components=n)
    pca_frame = pca_mo.fit_transform(a)
    return pca_mo,pca_frame 


# In[ ]:


# Call the scaler function for the training set. Then, transform the validation set.
scale,x_train_scaled=scaler_f(x_train_set)
x_val_scaled=pd.DataFrame(data=scale.transform(x_val_set),columns=list(x_train_set))


# In[ ]:


# Perform PCA using the scaled set
pca_show(x_train_scaled)


# Ok, we can run the modelling with just 7 components to explain maximum varience. 

# In[ ]:


# Apply PCA to extract 7 components and transform the validation set
pca_final,x_train_pca=pca_incr(x_train_scaled,7)
x_val_pca=pca_final.transform(x_val_scaled)


# In[ ]:


# Check the shapes
y_train=y_train.astype('int')
y_train_set=y_train_set.astype('int')
y_val_set=y_val_set.astype('int')
print(x_train_set.shape)
print(x_val_set.shape)
print(x_train_pca.shape)
print(x_val_pca.shape)


# # Stage 4 : Build Different Classification Models

# In[ ]:


# Create a frame and empty lists to store the predictor and actual values that help easy model visualisation
score_frame=pd.DataFrame()
algorithm_name=[]
recall_scores=[]
f1_scores=[]
accuracy_scores_test=[]
accuracy_scores_train=[]
plot_vars=[]

# Define function to predict the test data set usinf given algorithm
def run_algorithm(algo,tr_fe,tr_lb,ts_fe,ts_lb,algo_name,roc_req):
    # algo - model object
    # tr_fe - Independent variables from test set
    # tr_lb - Predictor variable from training set 
    # ts_fe - Independent variables from test set 
    # ts_lb - Predictor variable from test set
    # algo_name - Algorithm Name 
    # roc_req - Calculations of roc, acu and coefficeints
    
    algo_model = algo.fit(tr_fe,tr_lb)

    # predict values and probabilities
    y_pred_test=algo_model.predict(ts_fe)
    y_prob_test=algo_model.predict_proba(ts_fe)[:,1]
    y_pred_train=algo_model.predict(tr_fe)
    model_roc_auc = roc_auc_score(ts_lb,y_pred_test) 
        
    # Set Values for Display 
    algorithm_name.append(algo_name)
    recall_scores.append(metrics.recall_score(ts_lb,y_pred_test))
    f1_scores.append(metrics.f1_score(ts_lb,y_pred_test))
    accuracy_scores_test.append(accuracy_score(ts_lb,y_pred_test))
    accuracy_scores_train.append(accuracy_score(tr_lb,y_pred_train))
    
    # Print Values
    print (algo_name +' : ')
    print('-------------------------')
    print("Accuracy   Score on Test: ",accuracy_score(ts_lb,y_pred_test))
    print("Accuracy  Score on Train: ",accuracy_score(tr_lb,y_pred_train))
    print ("Area under curve : ",model_roc_auc,"\n")
    #print("Classification report : ","\n", classification_report(y_test_set,y_pred_test))
    #print("Confusion Matrix: ","\n",metrics.confusion_matrix(y_test_set,y_prob_test.round()))
    #print("Recall Score on train Set: ",metrics.recall_score(y_train_set,y_pred_train))
    #print("Recall Score on test Set: ",metrics.recall_score(y_test,y_pred))
    
    # Set up frames for model scores for later use
    score_frame[algo_name+'_Test']=ts_lb
    score_frame[algo_name+'_Prob']=y_prob_test
    plot_vars.append((algo_name+'_Test',algo_name+'_Prob',algo_name))
       
    # Plot the ROC curve 
    if roc_req == 'y':
        fpr,tpr,threshold = roc_curve(ts_lb,y_prob_test)
        plt.figure(figsize=(5, 5))
        plt.plot( fpr, tpr, label='ROC curve (area = %0.2f)' % model_roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate or [1 - True Negative Rate]')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic example')
        plt.legend(loc="lower right")
        plt.show()
    
    
def model_engine(x_tr,y_tr,x_ts,y_ts,roc_curve='n'):
    # Logistic Regression tunes using Grid Serch
    logreg = LogisticRegression(random_state=42)
    param = {'C':[0.001,0.003,0.005,0.01,0.03,0.05,0.1,0.3,0.5,1,2,3,3,4,5,10,20,22,25,27,30]}
    clf = GridSearchCV(logreg,param,scoring='accuracy',refit=True,cv=10)
    clf.fit(x_tr,y_tr)
    print('Best Accuracy: {:.4}, with best C: {}'.format(clf.best_score_, clf.best_params_)+'\n')
    logreg_cv = LogisticRegression(random_state=42, C=clf.best_params_['C'])
    run_algorithm(logreg_cv,x_tr,y_tr,x_ts,y_ts,'Logistic_Reg_P','n')
    
    # AdaBoost Classifier
    adbc = AdaBoostClassifier(n_estimators=500,learning_rate=1,random_state=42)
    run_algorithm(adbc,x_tr,y_tr,x_ts,y_ts,'Adaboost_Classifier',roc_curve) 
    
    # XGB Classifier
    xgb=XGBClassifier(random_state=42)
    run_algorithm(xgb,x_tr,y_tr,x_ts,y_ts,'XGB_Classifier',roc_curve)
    
    # Basic random forest model
    rf = RandomForestClassifier(random_state=42)
    run_algorithm(rf,x_tr,y_tr,x_ts,y_ts,'Random_Forest_Classifier',roc_curve)
    depth=[estimator.tree_.max_depth for estimator in rf.estimators_]
    
    # Tuned Random Forest Classifier using GridSearchCV to find optimal maximum depth and min_samples_leaf
    n_folds = 4
    parameters = {'max_depth': range(5,max(depth)+6, 3),
              'min_samples_leaf': [3,4,5,6] }
    rf = RandomForestClassifier(random_state=42)
    rf_gs = GridSearchCV(rf, param_grid=parameters,
                      cv=n_folds, 
                     scoring="accuracy")
    rf_gs.fit(x_tr, y_tr)
    print('Best parameters: ',rf_gs.best_params_,'\n')
    # model with the best hyperparameters
    rf_tuned = RandomForestClassifier(bootstrap=True,
                             max_depth=rf_gs.best_params_['max_depth'],
                             min_samples_leaf=rf_gs.best_params_['min_samples_leaf'],
                             n_estimators=1500,
                             random_state=42)
    run_algorithm(rf_tuned,x_tr,y_tr,x_ts,y_ts,'Random_Forest_Classifier_GS',roc_curve)
    print('Importance of Features : '+'\n')
    for i,j in zip(list(x_train_scaled),rf_tuned.feature_importances_):
        print(i," : ",j)

    print('\n')
    # gaussian Naive Bayes Classifier
    gnb=GaussianNB()
    run_algorithm(gnb,x_tr,y_tr,x_ts,y_ts,'Gaussian_NB',roc_curve)
    
    # SVM Classifier
    folds = KFold(n_splits = 8, shuffle = True, random_state = 4)
    params = [ {'gamma': [0.001,0.01,0.1,1,2,3],
                     'C': [1,2,2.1,2.2,2,3,5]}]
    model = SVC(kernel="rbf")
    model_cv = GridSearchCV(estimator = model, param_grid = params, 
                        scoring= 'accuracy', 
                        cv = folds, 
                        verbose = 1,
                       return_train_score=True)
    model_cv.fit(x_tr, y_tr) 
    cv_results = pd.DataFrame(model_cv.cv_results_)
    cv_results.param_C=cv_results.param_C.astype(float)
    cv_results.param_gamma=cv_results.param_gamma.astype(float)
    print(' Best Parameters are : ',model_cv.best_params_,'\n')

    svm_gs = SVC(kernel='rbf',gamma=model_cv.best_params_['gamma'],C=model_cv.best_params_['C'],probability=True)
    run_algorithm(svm_gs,x_tr,y_tr,x_ts,y_ts,'SVM_Classifier_RBF_Tuned',roc_curve)
    
    # Emsemble Classifier
    voting_clf=VotingClassifier(estimators=[('lr',logreg_cv),('rf',rf_tuned),('svc',svm_gs),('adb',adbc)],
                            voting='soft')
    run_algorithm(voting_clf,x_tr,y_tr,x_ts,y_ts,'Voting_Classifier',roc_curve)
    
    return [logreg_cv,adbc,xgb,rf_tuned,gnb,svm_gs,voting_clf]

def model_select():
# Use the score_frame to draw consolidated ROC curve and Score matris to select the appropriate model
    score_mat=pd.DataFrame(data={'Algorithm':algorithm_name,
      'Recall':recall_scores,
      'F1':f1_scores,
      'Test Accuracy':accuracy_scores_test,
      'Train Accuracy':accuracy_scores_train})
    print(score_mat)

    plt.figure(figsize=(8, 8))

    for i in plot_vars:
        fpr,tpr,threshold = roc_curve(score_frame[i[0]],score_frame[i[1]])
        plt.plot( fpr, tpr, label=i[2])


    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate or [1 - True Negative Rate]')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristics')
    plt.legend(loc="lower right")

    plt.show()

    plt.figure(figsize=(8, 8))
    for i in plot_vars:
        precision, recall, threshold = precision_recall_curve(score_frame[i[0]],score_frame[i[1]])
        plt.plot( precision, recall, label=i[2])

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Recall vs Precision Charecteric')
    plt.legend(loc="top left")
    plt.show()


# In[ ]:


clfs=model_engine(x_train_pca,y_train_set,x_val_pca,y_val_set)


# # Stage 5 - Derive Prominent Features

# Define a function to execute RFE (Recursive Feature Elimination) and identify the supporting columns. Run a Logistic Regression on the RFE supported features and look at the summary statistics.<br>
# Note that we will run the RFE on the scaled tranining set , rather than the PCA data.

# In[ ]:


# Define function for a logistic classifier and apply RFE to derive the prominent features. Check multi colienarity.

def logrec_rfe(x, y):
    # x = Feature variable 
    # y =  response variable  
   
    # Run RFE on logistic Regression
    logreg_rfe = LogisticRegression(random_state=42)
    y=list(y.astype('int'))
    rfe = RFE(logreg_rfe,len(list(x)))             # running RFE with ALL variables as output
    rfe = rfe.fit(x, y)

    # Select the columns that are supported by RFE
    col = x.columns[rfe.support_]

    x_train_sm = sm.add_constant(x[col])
    logm2 = sm.GLM(y,x_train_sm, family = sm.families.Binomial())
    res = logm2.fit()
    
    # Check Multi colinearity using VIF
    vif = pd.DataFrame()
    vif['features'] = x[col].columns
    vif['VIF'] = [variance_inflation_factor(x[col].values, i) for i in range(x[col].shape[1])]
    vif['VIF'] = round(vif['VIF'], 2)
    vif = vif.sort_values(by = "VIF", ascending = False)
    
    # Print stat summary and VIF table
    print(res.summary())
    print(vif)
    
    return list(vif['features'])


# In[ ]:


prom_f = logrec_rfe(x_train_set,y_train_set)


# In[ ]:


# Remove the variable with High VIF value  -'Pclass'
prom_f=logrec_rfe((x_train_set.drop(columns=['Pclass'],axis=1)),y_train_set)


# In[ ]:


# Remove the variable with High P value  -'Parch'
prom_f=logrec_rfe((x_train_set.drop(columns=['Pclass','Parch'],axis=1)),y_train_set)


# So, the most prominent features are - 'Age', 'Embarked','Fare','SibSp' and 'Sex'. Based on this, the varience in the data can be explained and to some degree the output label can be predicted. However, we have simply removed some features and this results in loss of accurancy.
# If we compare these prominent features with the important features that Random Forest Algorithm has identified, we can see some similarities - 
# - male  :  0.17055916349260553
# - Q  :  0.10184557188402982
# - S  :  0.17221016502344105
# - Age  :  0.26675961592763947
# - Fare  :  0.1184624028916517
# - Parch  :  0.09209078733810572
# - Pclass  :  0.0780722934425268

# # Stage 6 - Model Selection

# In[ ]:


model_select()


# Based on the above accuracies, Tuned Random Forest Classifier can be selected. It has given 84% accuracy on the train data.

# # Stage 7 - Predict labels for Test data

# The approach I follow is, run the full train data aganist the selected model and then, use the model for predictions.

# In[ ]:


# x_train is the full train data and x_test is the full test data.
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)


# In[ ]:


# Call the scaler function for the training set. Then, transform the validation set.
scale,x_train_sc=scaler_f(x_train)
x_test_sc=pd.DataFrame(data=scale.transform(x_test),columns=list(x_train))


# In[ ]:


# Apply PCA to extract 7 components and transform the validation set
pca_final,x_train_pc=pca_incr(x_train_sc,7)
x_test_pc=pca_final.transform(x_test_sc)


# In[ ]:


print(clfs[3])


# In[ ]:


# Run the selected model
rf_tuned=clfs[3]  # Tuned Random Forest Model
rf_tuned_model = rf_tuned.fit(x_train_sc,y_train)

# predict values 
pred_test=rf_tuned_model.predict(x_test_sc)
pred_train=rf_tuned_model.predict(x_train_sc)
print('Training Accuracy: ', accuracy_score(y_train,pred_train))


# In[ ]:


# Write Submission File
d={'PassengerId': test_data['PassengerId'],'Survived':pred_test}
submission_df=pd.DataFrame(d)
submission_df.to_csv('Titanic_Submission.csv',index=False)

