#!/usr/bin/env python
# coding: utf-8

# ##### Titanic Solution and approach
# There are several excellent notebooks to study data science competition entries. However many will skip some of the explanation on how the solution is developed as these notebooks are developed by experts for experts. The objective of this notebook is to follow a step-by-step workflow, explaining each step and rationale for every decision we take during solution development.
# 
# Step By Step Processing of data :-
# 
# 1) Understanding the Problem
# 
# 2) Acquire training and testing dataI
# 3) Data preparation 
# 4) Identify the patterne and explore the data
# 5) Model, predict and solve the problem.
# 6) Visualize, report, and present the problem solving steps and final solution
# 7) Supply or submit the results.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ****Read the data through csv file :- 
# 
# The Python Pandas packages helps us work with our datasets. We start by acquiring the training and testing datasets into Pandas DataFrames. We also combine these datasets to run certain operations on both datasets together.

# In[ ]:


sub_file = pd.read_csv("/kaggle/input/titanic/gender_submission.csv")
sub_file.head()


# In[ ]:


train = pd.read_csv("/kaggle/input/titanic/train.csv")
train.head()


# In[ ]:


val = pd.read_csv("/kaggle/input/titanic/test.csv")
val.head()


# In[ ]:


train.columns


# In[ ]:


val.columns


# **** Step By Step Data Preparation 
# 1) Find if any null coloumns are present in the data 

# In[ ]:


train.isnull().mean()


# In[ ]:


val.isnull().mean()


# In[ ]:


train.shape


# 

# In[ ]:


train.describe()


# In[ ]:


val.describe()


# **Which features are numerical?**
# 
# Which features are numerical? These values change from sample to sample. Within numerical features are the values discrete, continuous, or timeseries based? Among other things this helps us select the appropriate plots for visualization.
# 
# 1. Continous: Age, Fare. Discrete: SibSp, Parch.

# **** As we get Null value columns in the data 
#  Folllow the procedure step by step 
# 1.  1) For continous variable , calculate the mean and median for inittial step of data preparation

# In[ ]:


def impute_na_numeric(train,val,var):
    mean = train[var].mean()
    median = train[var].median()
    
    train[var+"_mean"] = train[var].fillna(mean)
    train[var+"_median"] = train[var].fillna(median)
    
    var_original = train[var].std()**2
    var_mean = train[var+"_mean"].std()**2
    var_median = train[var+"_median"].std()**2
    
    print("Original Variance: ",var_original)
    print("Mean Variance: ",var_mean)
    print("Median Variance: ",var_median)
    
    if((var_mean < var_original) | (var_median < var_original)):
        if(var_mean < var_median):
            train[var] = train[var+"_mean"]
            val[var] = val[var].fillna(mean)
        else:
            train[var] = train[var+"_median"]
            val[var] = val[var].fillna(median)
    else:
        val[var] = val[var].fillna(median)
    train.drop([var+"_mean",var+"_median"], axis=1, inplace=True)


# In[ ]:


impute_na_numeric(train,val,"Age")


# In[ ]:


impute_na_numeric(train,val,"Fare")


# **Which features are categorical?**
# 
# * These values classify the samples into sets of similar samples. Within categorical features are the values nominal, ordinal, ratio, or interval based? Among other things this helps us select the appropriate plots for visualization.
# 
# * Categorical: Survived, Sex, and Embarked. Ordinal: Pclass.

# In[ ]:


train["Embarked"].mode().values[0]


# In[ ]:


def impute_na_non_numeric(train,val,var):
    mode = train[var].mode().values[0]
    train[var] = train[var].fillna(mode)
    val[var] = val[var].fillna(mode)


# In[ ]:


impute_na_non_numeric(train,val,"Embarked")


# **Which features are mixed data types?**
# 
# * Numerical, alphanumeric data within same feature. These are candidates for correcting goal.
# 
# * Ticket is a mix of numeric and alphanumeric data types. Cabin is alphanumeric.
# * **Which features may contain errors or typos?**
# 
# * This is harder to review for a large dataset, however reviewing a few samples from a smaller dataset may just tell us outright, which features may require correcting.
# 
# > Name feature may contain errors or typos as there are several ways used to describe a name including titles, round brackets, and quotes used for alternative or short names.

# In[ ]:


def impute_na_max_missing(train,val,var,prefix):
    train[prefix+"_"+var] = np.where(train[var].isna(),0,1)
    train.drop([var],axis=1,inplace=True)
    val[prefix+"_"+var] = np.where(val[var].isna(),0,1)
    val.drop([var],axis=1,inplace=True)


# In[ ]:


impute_na_max_missing(train,val,"Cabin","had")


# ** Missing Values imputed **

# In[ ]:


train.head()


# **Combination of Two coloumns**

# In[ ]:


train["Family_Size"] = train["SibSp"] + train["Parch"]
val["Family_Size"] = val["SibSp"] + val["Parch"]


# **Explore the Feature Engineering **
# 1. We can create one new coloumn with name "Salutation" from "Name" coloumn. Where all the names in "Name" column are unique but still we can apply feature engineering steps for this. Observe the coloumn and we can see that some of them are Mr. , Mrs. , Dr. With feature engineering we can extract these and make the prediction of survival on the basis of this.

# In[ ]:


train["Salutation"] = train["Name"].map(lambda x: x.split(',')[1].split()[0])


# In[ ]:


train["Salutation"].unique()


# In[ ]:


val["Salutation"] = val["Name"].map(lambda x: x.split(',')[1].split()[0])


# In[ ]:


val["Salutation"].unique()


# In[ ]:


val[val["Salutation"] == "Dona."]


# **Analyze by pivoting features**
# * To confirm some of our observations and assumptions, we can quickly analyze our feature correlations by pivoting features against each other. We can only do so at this stage for features which do not have any empty values. It also makes sense doing so only for features which are categorical (Sex), ordinal (Pclass) or discrete (SibSp, Parch) type.
# * Pclass We observe significant correlation (>0.5) among Pclass=1 and Survived (classifying #3). We decide to include this feature in our model.
# * Sex We confirm the observation during problem definition that Sex=female had very high survival rate at 74% (classifying #1).
# * SibSp and Parch These features have zero correlation for certain values. It may be best to derive a feature or a set of features from these individual features (creating #1).

# In[ ]:


def transform_with_target_probs(train,val,var,target):
    var_dict = train.groupby([var])[target].mean().to_dict()
    train[var] = train[var].map(var_dict)
    val[var] = val[var].map(var_dict)


# In[ ]:


transform_with_target_probs(train,val,"Pclass","Survived")


# In[ ]:


transform_with_target_probs(train,val,"Sex","Survived")


# In[ ]:


transform_with_target_probs(train,val,"Embarked","Survived")


# In[ ]:


train["Salutation"] = train["Salutation"].apply(lambda x: x.split('.')[0])
val["Salutation"] = val["Salutation"].apply(lambda x: x.split('.')[0])


# In[ ]:


def get_salutation_map(df,var,rare):
    sal_dict = {}
    for sal, count in df[var].value_counts().to_dict().items():
        count = int(count)
        if count < 10:
            sal_dict[sal] = rare
        else:
            sal_dict[sal] = sal
    return sal_dict


# In[ ]:


transform_with_target_probs(train,val,"Salutation","Survived")


# **Analyze by visualizing data**
# * Now we can continue confirming some of our assumptions using visualizations for analyzing the data.
# * 
# * Correlating numerical features
# * Let us start by understanding correlations between numerical features and our solution goal (Survived).
# * 
# * A histogram chart is useful for analyzing continous numerical variables like Age where banding or ranges will help identify useful patterns. The histogram can indicate distribution of samples using automatically defined bins or equally ranged bands. This helps us answer questions relating to specific bands (Did infants have better survival rate?)
# * 
# * Note that x-axis in historgram visualizations represents the count of samples or passengers.
# * 
# **Observations.**
# 
# * Infants (Age <=4) had high survival rate.
# * Oldest passengers (Age = 80) survived.
# * Large number of 15-25 year olds did not survive.
# * Most passengers are in 15-35 age range.
# * Decisions.
# 
# **This simple analysis confirms our assumptions as decisions for subsequent workflow stages.**
# 
# * We should consider Age (our assumption classifying #2) in our model training.
# * Complete the Age feature for null values (completing #1).
# * We should band age groups (creating #3).

# ### Explore Numeric Data

# In[ ]:


# Explore Age distibution 
g = sns.kdeplot(train["Age"][(train["Survived"] == 0)], color="Red", shade = True)
g = sns.kdeplot(train["Age"][(train["Survived"] == 1)], ax =g, color="Blue", shade= True)
g.set_xlabel("Age")
g.set_ylabel("Frequency")
g = g.legend(["Not Survived","Survived"])


# In[ ]:


# Explore Age distribution 
g = sns.distplot(train["Age"], color="m", label="Skewness : %.2f"%(train["Age"].skew()))
g = g.legend(loc="best")


# In[ ]:


train["Fare"].describe()


# In[ ]:


# Explore Fare distribution 
g = sns.distplot(train["Fare"], color="m", label="Skewness : %.2f"%(train["Fare"].skew()))
g = g.legend(loc="best")


# #### Outlier Removal

# In[ ]:


import warnings
warnings.filterwarnings('ignore')


# In[ ]:


# Apply log to Fare to reduce skewness distribution
train["Fare"] = train["Fare"].map(lambda i: np.log(i) if i > 0 else 0)


# In[ ]:


g = sns.factorplot(x="Survived", y = "Age", hue = "had_Cabin", data = train, kind="violin")


# In[ ]:


train = pd.get_dummies(train, columns=["had_Cabin"], drop_first=True)
val = pd.get_dummies(val, columns=["had_Cabin"], drop_first=True)


# In[ ]:


drop_cols = ['PassengerId', 'Name', 'SibSp','Parch', 'Ticket']


# In[ ]:


train.drop(drop_cols,axis=1).drop(["Survived"],axis=1).values


# In[ ]:


train.drop(drop_cols,axis=1).drop(["Survived"],axis=1).columns


# In[ ]:


X = train.drop(drop_cols,axis=1).drop(["Survived"],axis=1).values
y = train["Survived"].values


# In[ ]:


val["Salutation"] = val["Salutation"].fillna(val["Salutation"].mode().values[0])
val_test = val.drop(drop_cols,axis=1).values


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=101)


# ### Feature Scaling

# #### MinMaxScaling

# In[ ]:


# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
mms = MinMaxScaler()


# In[ ]:


mms.fit(X_train)


# In[ ]:


X_train_mms = mms.transform(X_train)


# #### Standard Scaling

# In[ ]:


# Feature Scaling
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()


# In[ ]:


ss.fit(X_train)


# In[ ]:


X_train_ss = ss.transform(X_train)


# #### Check Distribution after Scaling

# In[ ]:


# For Age

sns.jointplot(X_train[:,2], X_train_mms[:,2], kind='kde')


# In[ ]:


# For Age

sns.jointplot(X_train[:,2], X_train_ss[:,2], kind='kde')


# In[ ]:


# For Fare

sns.jointplot(X_train[:,3], X_train_mms[:,3], kind='kde')


# In[ ]:


# For Fare

sns.jointplot(X_train[:,3], X_train_ss[:,3], kind='kde')


# In[ ]:


X_test_ss = ss.transform(X_test)


# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,VotingClassifier


# In[ ]:


from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score


# In[ ]:


classification_models = ['LogisticRegression',
                         'SVC',
                         'DecisionTreeClassifier',
                         'RandomForestClassifier',
                         'AdaBoostClassifier']


# In[ ]:


cm = []
acc = []
prec = []
rec = []
f1 = []
models = []
estimators = []


# In[ ]:


for classfication_model in classification_models:
    
    model = eval(classfication_model)()
    
    model.fit(X_train_ss,y_train)
    y_pred = model.predict(X_test_ss)
    
    models.append(type(model).__name__)
    estimators.append((type(model).__name__,model))
    cm.append(confusion_matrix(y_test,y_pred))
    acc.append(accuracy_score(y_test,y_pred))
    prec.append(precision_score(y_test,y_pred))
    rec.append(recall_score(y_test,y_pred))
    f1.append(f1_score(y_test,y_pred))


# ### Stacking Ensemble

# In[ ]:


vc = VotingClassifier(estimators)
vc.fit(X_train_ss,y_train)


# In[ ]:


y_pred = vc.predict(X_test_ss)
    
models.append(type(vc).__name__)

cm.append(confusion_matrix(y_test,y_pred))
acc.append(accuracy_score(y_test,y_pred))
prec.append(precision_score(y_test,y_pred))
rec.append(recall_score(y_test,y_pred))
f1.append(f1_score(y_test,y_pred))


# In[ ]:


model_dict = {"Models":models,
             "CM":cm,
             "Accuracy":acc,
             "Precision":prec,
             "Recall":rec,
             "f1_score":f1}


# In[ ]:


model_df = pd.DataFrame(model_dict)
model_df


# In[ ]:


model_df.sort_values(by=['Accuracy','f1_score','Recall','Precision'],ascending=False,inplace=True)
model_df


# ### Scale Test file data

# In[ ]:


val_test = ss.transform(val_test)


# In[ ]:


y_pred_sub = vc.predict(val_test)


# In[ ]:


sub_df = pd.concat([val['PassengerId'],
                    pd.DataFrame(y_pred_sub,columns=["Survived"])],
                   axis=1)
sub_df.head()


# In[ ]:


sub_df.to_csv("Stacked_Ensemble_Baseline_Submission.csv", index=False)


# ##### Achieved Kaggle Score = 0.72248

# ### Hyper parameter Tuning

# In[ ]:


model_param_grid = {}


# In[ ]:


model_param_grid['LogisticRegression'] = {'penalty' : ['l1', 'l2'],
                                          'C' : np.logspace(0, 4, 10)}


# In[ ]:


model_param_grid['SVC'] = [{'kernel': ['rbf'], 
                            'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                            'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                           {'kernel': ['sigmoid'],
                            'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                            'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                           {'kernel': ['linear'], 
                            'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                           {'kernel': ['poly'], 
                            'degree' : [0, 1, 2, 3, 4, 5, 6]}
                          ]


# In[ ]:


model_param_grid['DecisionTreeClassifier'] = {'criterion' : ["gini","entropy"],
                                              'max_features': ['auto', 'sqrt', 'log2'],
                                              'min_samples_split': [2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                                              'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10,11]}


# In[ ]:


model_param_grid['RandomForestClassifier'] = {'n_estimators' : [25,50,75,100],
                                              'criterion' : ["gini","entropy"],
                                              'max_features': ['auto', 'sqrt', 'log2'],
                                              'class_weight' : ["balanced", "balanced_subsample"]}


# In[ ]:


model_param_grid['AdaBoostClassifier'] = {'n_estimators' : [25,50,75,100],
                                          'learning_rate' : [0.001,0.01,0.05,0.1,1,10],
                                          'algorithm' : ['SAMME', 'SAMME.R']}


# #### Function to perform Grid Search with Cross Validation

# In[ ]:


from sklearn.model_selection import GridSearchCV
def tune_parameters(model_name,model,params,cv,scorer,X,y):
    best_model = GridSearchCV(estimator = model,
                              param_grid = params,
                              scoring = scorer,
                              cv = cv,
                              n_jobs = -1).fit(X, y)
    print("Tuning Results for ", model_name)
    print("Best Score Achieved: ",best_model.best_score_)
    print("Best Parameters Used: ",best_model.best_params_)
    return best_model


# #### Define custom Scorer function

# In[ ]:


from sklearn.metrics import make_scorer

# Define scorer
def f1_metric(y_test, y_pred):
    score = f1_score(y_test, y_pred)
    return score


# In[ ]:


# Scorer function would try to maximize calculated metric
f1_scorer = make_scorer(f1_metric,greater_is_better=True)


# #### Run iterations for all the trained baseline models

# In[ ]:


best_estimators = []


# In[ ]:


for m_name, m_obj in estimators:
    best_estimators.append((m_name,tune_parameters(m_name,
                                                   m_obj,
                                                   model_param_grid[m_name],
                                                   10,
                                                   f1_scorer,
                                                   X_train_ss,
                                                   y_train)))


# In[ ]:


tuned_estimators = []


# In[ ]:


tuned_lr = LogisticRegression(C=2.7825594022071245, 
                              penalty = 'l1')
tuned_lr.fit(X_train_ss,y_train)
tuned_estimators.append(("LogisticRegression",tuned_lr))


# In[ ]:


tuned_svc = SVC(C = 10, gamma = 0.01, kernel = 'rbf', probability=True)
tuned_svc.fit(X_train_ss,y_train)
tuned_estimators.append(("SVC",tuned_svc))


# In[ ]:


tuned_dt = DecisionTreeClassifier(criterion = 'entropy', 
                                  max_features = 'log2', 
                                  min_samples_leaf = 5, 
                                  min_samples_split = 11)
tuned_dt.fit(X_train_ss,y_train)
tuned_estimators.append(("DecisionTreeClassifier",tuned_dt))


# In[ ]:


tuned_rf = RandomForestClassifier(class_weight = 'balanced_subsample', 
                                  criterion = 'gini', 
                                  max_features = 'sqrt', 
                                  n_estimators = 100)
tuned_rf.fit(X_train_ss,y_train)
tuned_estimators.append(("RandomForestClassifier",tuned_rf))


# In[ ]:


tuned_adb = AdaBoostClassifier(algorithm = 'SAMME', 
                                  learning_rate = 0.1, 
                                  n_estimators = 75)
tuned_adb.fit(X_train_ss,y_train)
tuned_estimators.append(("AdaBoostClassifier",tuned_adb))


# In[ ]:


tuned_vc = VotingClassifier(tuned_estimators)
tuned_vc.fit(X_train_ss,y_train)


# In[ ]:


y_pred_tuned_sub = tuned_vc.predict(val_test)
tuned_sub_df = pd.concat([val['PassengerId'],
                          pd.DataFrame(y_pred_tuned_sub,columns=["Survived"])],
                         axis=1)
tuned_sub_df.head()


# In[ ]:


tuned_sub_df.to_csv("Stacked_Ensemble_Tuned_Submission.csv", index=False)

