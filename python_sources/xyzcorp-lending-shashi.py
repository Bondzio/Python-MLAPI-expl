#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Importing important Libraries
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


##Reading the text file
data=pd.read_table("/kaggle/input/xyzcorp-lendingdata/XYZCorp_LendingData.txt",parse_dates=['issue_d'])


# In[ ]:


len(data)


# In[ ]:


data.head()


# In[ ]:


data.columns


# In[ ]:


##Informatin of data
data.info()


# In[ ]:


#Total rows and columns
data.shape


# In[ ]:


##Total number of unique values for each column
data.nunique()


# In[ ]:


#Description of data
data.describe()


# In[ ]:


#Finding, is there any null values?
data.isnull().values.any()


# In[ ]:


##Total number of null values for each column
null=data.isnull().sum()
null


# In[ ]:


fig0=plt.figure(figsize=(20,4))
null.plot(kind='bar')
plt.title('List of columns and there NA values count')


# In[ ]:


#Dependent Variable 
data['default_ind'].value_counts()


# In[ ]:


#Exploratory Data Analysis
##Dependent Variable
fig1=plt.figure()
sns.countplot(data['default_ind'])


# In[ ]:


#Removing unwanted features
dataframe=data.drop(['id', 'member_id'],axis=1)


# In[ ]:


dataframe.shape


# In[ ]:


#Removing features having more than 700000 missing values 
lis=data.isnull().sum()
for i in range(len(lis)):
    if lis[i]>700000:
        del dataframe[(lis.index[i])]


# In[ ]:


dataframe.shape


# In[ ]:


null1=dataframe.isnull().sum()
null1


# In[ ]:


fig=plt.figure(figsize=(20,4))
null1.plot(kind='bar')
plt.title('List of columns after removing columns above 700000 NAs')


# In[ ]:


dataframe.iloc[:,0:10].head()


# In[ ]:


## Exploratory Data Analysis for Independent variables
f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.distplot(dataframe['loan_amnt'],kde=True,ax=ax1)
sns.boxplot(y='default_ind',x='loan_amnt',data=dataframe,orient='h',ax=ax2)


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.distplot(dataframe['funded_amnt_inv'],kde=True,ax=ax1)
sns.boxplot(y='default_ind',x='funded_amnt_inv',data=dataframe,orient='h',ax=ax2)


# In[ ]:


dataframe.term.value_counts()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.countplot(dataframe['term'],ax=ax1)
sns.countplot('term',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


dataframe.groupby('term')['default_ind'].value_counts(normalize=False) ##relative frequencies when normalize=True


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.distplot(dataframe['int_rate'],kde=True,ax=ax1)
sns.boxplot(y='default_ind',x='int_rate',data=dataframe,orient='h',ax=ax2)


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.distplot(dataframe['installment'],kde=True,ax=ax1)
sns.boxplot(y='default_ind',x='installment',data=dataframe,orient='h',ax=ax2)


# In[ ]:


dataframe.grade.value_counts(dropna=False)


# In[ ]:


dataframe.groupby('grade')['default_ind'].value_counts(normalize=False)


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.countplot(dataframe['grade'],ax=ax1)
sns.countplot('grade',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


dataframe.sub_grade.value_counts(dropna=False)


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.countplot(dataframe['sub_grade'],ax=ax1)
sns.countplot('sub_grade',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


dataframe['emp_title'].nunique() #removing
del dataframe['emp_title']


# In[ ]:


dataframe.emp_length.value_counts(dropna=False)


# In[ ]:


## Imputing missing values with most repeated value
dataframe['emp_length'].fillna(value=dataframe['emp_length'].value_counts().index[0],axis=0,inplace=True)


# In[ ]:


dataframe.emp_length.value_counts()


# In[ ]:


dataframe.groupby('emp_length')['default_ind'].value_counts()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.countplot(dataframe['emp_length'],ax=ax1)
sns.countplot('emp_length',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


dataframe.iloc[:,10:20].head()


# In[ ]:


dataframe.home_ownership.value_counts(dropna=False)


# In[ ]:


dataframe.groupby('home_ownership')['default_ind'].value_counts()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.countplot(dataframe['home_ownership'],ax=ax1)
sns.countplot('home_ownership',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


##correlation between annual_inc and default_ind
dataframe[['annual_inc','default_ind']].corr()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.distplot(dataframe['annual_inc'],kde=True,ax=ax1)
sns.boxplot(y='default_ind',x='annual_inc',data=dataframe,orient='h',ax=ax2)


# In[ ]:


dataframe.verification_status.value_counts()


# In[ ]:


dataframe.groupby('verification_status')['default_ind'].value_counts()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.countplot(dataframe['verification_status'],ax=ax1)
sns.countplot('verification_status',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


dataframe.corr()['default_ind']


# In[ ]:


## Correlation matrix
fig13=plt.figure(figsize=(20,20))
sns.heatmap(dataframe.corr(),annot=True,cmap='magma')


# In[ ]:


##Number of unique values of issue_d
dataframe.issue_d.nunique()


# In[ ]:


dataframe.groupby('pymnt_plan')['default_ind'].value_counts()


# In[ ]:


del dataframe['pymnt_plan']


# In[ ]:


#Unique values of purpose
dataframe.purpose.value_counts()


# In[ ]:


dataframe.groupby('purpose')['default_ind'].value_counts()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=2,ncols=1,figsize=(12,12),dpi=90)
sns.countplot(dataframe['purpose'],ax=ax1)
sns.countplot('purpose',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


dataframe.title.nunique()


# In[ ]:


##Removing unwanted features
del dataframe['title']
del dataframe['zip_code']
del dataframe['policy_code']


# In[ ]:


dataframe.addr_state.nunique()


# In[ ]:


del dataframe['addr_state']


# In[ ]:


dataframe.shape


# In[ ]:


dataframe[['dti','delinq_2yrs','default_ind']].corr()


# In[ ]:


##Due to low correlation with dependent variable,removing these features
del dataframe['dti']
del dataframe['delinq_2yrs']


# In[ ]:


dataframe.inq_last_6mths.value_counts()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.countplot(dataframe['inq_last_6mths'],ax=ax1)
sns.countplot('inq_last_6mths',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


dataframe.iloc[:,10:20].head(3)


# In[ ]:


dataframe.mths_since_last_delinq.nunique()


# In[ ]:


del dataframe['mths_since_last_delinq']


# In[ ]:


dataframe.open_acc.unique()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.distplot(dataframe['open_acc'],kde=True,ax=ax1)
sns.boxplot(x='open_acc',y='default_ind',data=dataframe,orient='h',ax=ax2)


# In[ ]:


dataframe.earliest_cr_line.nunique()


# In[ ]:


del dataframe['earliest_cr_line']


# In[ ]:


dataframe.pub_rec.value_counts()


# In[ ]:


dataframe.revol_bal.value_counts()


# In[ ]:


dataframe.revol_util.value_counts()


# In[ ]:


##Imputing missing values with mean
dataframe['revol_util'].fillna(value=dataframe['revol_util'].mean(),inplace=True)


# In[ ]:


##finding correlation 
dataframe[['revol_bal','revol_util','total_acc','default_ind']].corr()


# In[ ]:


dataframe.iloc[:,17:30].head(3)


# In[ ]:


dataframe.total_acc.unique()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.distplot(dataframe['total_acc'],kde=True,ax=ax1)
sns.boxplot(x='total_acc',y='default_ind',data=dataframe,orient='h',ax=ax2)


# In[ ]:


dataframe.initial_list_status.value_counts()


# In[ ]:


dataframe.groupby('initial_list_status')['default_ind'].value_counts()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.countplot(dataframe['initial_list_status'],ax=ax1)
sns.countplot('initial_list_status',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


dataframe.out_prncp.nunique()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.distplot(dataframe['total_pymnt'],kde=True,ax=ax1)
sns.boxplot(x='total_pymnt',y='default_ind',data=dataframe,orient='h',ax=ax2)


# In[ ]:


dataframe.total_rec_late_fee.nunique()


# In[ ]:


dataframe.recoveries.nunique()


# In[ ]:


dataframe.iloc[:,28:35].head(3)


# In[ ]:


dataframe.collection_recovery_fee.nunique()


# In[ ]:


dataframe['last_pymnt_d'].nunique()


# In[ ]:


del dataframe['last_pymnt_d']


# In[ ]:


dataframe.last_pymnt_amnt.nunique()


# In[ ]:


dataframe.next_pymnt_d.value_counts(dropna=False)


# In[ ]:


##imputing missing values with most frequently occured values
dataframe['next_pymnt_d'].fillna(value=dataframe['next_pymnt_d'].value_counts().index[0],inplace=True,axis=0)


# In[ ]:


dataframe.next_pymnt_d.value_counts()


# In[ ]:


dataframe.groupby('next_pymnt_d')['default_ind'].value_counts()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.countplot(dataframe['next_pymnt_d'],ax=ax1)
sns.countplot('next_pymnt_d',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


dataframe.last_credit_pull_d.nunique()


# In[ ]:


del dataframe['last_credit_pull_d']


# In[ ]:


dataframe.collections_12_mths_ex_med.value_counts(dropna=False)


# In[ ]:


del dataframe['collections_12_mths_ex_med']


# In[ ]:


dataframe.mths_since_last_major_derog.nunique()


# In[ ]:


del dataframe['mths_since_last_major_derog']


# In[ ]:


dataframe.application_type.value_counts(dropna=False)


# In[ ]:


dataframe.groupby('application_type')['default_ind'].value_counts()


# In[ ]:


f,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(12,3),dpi=90)
sns.countplot(dataframe['application_type'],ax=ax1)
sns.countplot('application_type',hue='default_ind',data=dataframe,ax=ax2)


# In[ ]:


dataframe.iloc[:,30:37].head(3)


# In[ ]:


##Finding correlation
dataframe[['acc_now_delinq','tot_coll_amt','tot_cur_bal','total_rev_hi_lim','default_ind']].corr()


# In[ ]:


##due to low correlation with dependent variable,removing these features
del dataframe['acc_now_delinq']
del dataframe['tot_coll_amt']


# In[ ]:


dataframe.tot_cur_bal.nunique()


# In[ ]:


#mean imputation
dataframe['tot_cur_bal'].fillna(value=dataframe['tot_cur_bal'].mean(),axis=0,inplace=True)


# In[ ]:


#mean imputaion
dataframe['total_rev_hi_lim'].fillna(value=dataframe['total_rev_hi_lim'].mean(),axis=0,inplace=True)


# In[ ]:


#Checking for count of null values for each column
null2=dataframe.isnull().sum()
null2


# In[ ]:


#Checking for number of unique values so that we can create dummy variables for object type features
dataframe.nunique()


# In[ ]:


dataframe.shape


# In[ ]:


#Dropping unwanted features
dataframe.drop(['sub_grade','funded_amnt','funded_amnt_inv'],inplace=True,axis=1)


# In[ ]:


##Creating dummy variables for object type variables
Term=pd.get_dummies(dataframe['term'],drop_first=True)
Grade=pd.get_dummies(dataframe['grade'],drop_first=True)
Emp_length=pd.get_dummies(dataframe['emp_length'],drop_first=True)
Home_ownership=pd.get_dummies(dataframe['home_ownership'],drop_first=True)
Verification=pd.get_dummies(dataframe['verification_status'],drop_first=True)
Purpose=pd.get_dummies(dataframe['purpose'],drop_first=True)
Inq_last_6mths=pd.get_dummies(dataframe['inq_last_6mths'],drop_first=True)
Initial_list=pd.get_dummies(dataframe['initial_list_status'],drop_first=True)
Next_pymnt_d=pd.get_dummies(dataframe['next_pymnt_d'],drop_first=True)
Application=pd.get_dummies(dataframe['application_type'],drop_first=True)


# In[ ]:


##Dropping old object type columns
dataframe.drop(['term','grade','emp_length','home_ownership','verification_status','purpose',
                'inq_last_6mths','initial_list_status','next_pymnt_d','application_type'],
               inplace=True,axis=1)


# In[ ]:


##joining dataframe with newly created dummy variables using concatenation function
dataframe=pd.concat([dataframe,Term,Grade,Emp_length,Home_ownership,Verification,Purpose,Inq_last_6mths,
                     Initial_list,Next_pymnt_d,Application],axis=1)


# In[ ]:


#checking for new shape of dataframe
dataframe.shape


# In[ ]:


dataframe.head()


# In[ ]:


#Replacing our dependent variable 'default_ind' with 'loan_status'
dataframe['loan_status']=dataframe['default_ind']


# In[ ]:


dataframe.head()


# In[ ]:


#deleting old column
del dataframe['default_ind']


# In[ ]:


dataframe.head()


# In[ ]:


##Splitting our dataframe into train and test on the basis of 
##train set is spplitted from june 2007 to may 2015
##test set is splitted from june 2015 to december 2015
train = dataframe[dataframe['issue_d'] < '2015-6-01']
test = dataframe[dataframe['issue_d'] >= '2015-6-01']


# In[ ]:


train.shape,test.shape


# In[ ]:


print(train.loan_status.value_counts())
print(test.loan_status.value_counts())


# In[ ]:


##Deleting issue_d
del train['issue_d']
del test['issue_d']


# In[ ]:


train.shape,test.shape


# In[ ]:


train.iloc[:,0:70].head()


# In[ ]:


##Splitting train set into X_train and y_train
X_train=train.iloc[:,0:70]
y_train=train['loan_status']


# In[ ]:


#Splitting test set into X_test and y_test
X_test=test.iloc[:,0:70]
y_test=test['loan_status']


# In[ ]:


#Importing LogisticRegression model
from sklearn.linear_model import LogisticRegression
logmodel=LogisticRegression(solver='liblinear')


# In[ ]:


#Fitting model to train set
logmodel.fit(X_train,y_train)


# In[ ]:


#Predicting the test set
predictions=logmodel.predict(X_test)


# In[ ]:


##Classification Report
from sklearn.metrics import classification_report
print(classification_report(y_test,predictions))


# In[ ]:


from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


# In[ ]:


##Confusion Matrix
print(confusion_matrix(y_test,predictions))


# In[ ]:


##Calculating important metrics Precision score,Recall score,F1_Score
print("precision score is",precision_score(y_test,predictions))
print("recall is",recall_score(y_test,predictions))
print("F1_score is",f1_score(y_test,predictions))


# In[ ]:


##Accuracy test
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test,predictions))


# In[ ]:


#Receiver Operating Characteristics Area Under Curve(AUC) score 
from sklearn.metrics import roc_auc_score
print(roc_auc_score(y_test,predictions))


# In[ ]:


from sklearn.metrics import roc_curve
fpr,tpr,thresholds=roc_curve(y_test,predictions)


# In[ ]:


plt.plot(fpr,tpr,color='blue',label='ROC')
plt.plot([0,1],[0,1],color='green',linestyle='--')


# In[ ]:


##Cross validating the training set using logmodel
from sklearn.model_selection import cross_val_score
print(cross_val_score(logmodel,X=X_train,y=y_train,cv=5,scoring='accuracy'))


# In[ ]:


#Importing RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
rf=RandomForestClassifier(n_estimators=120,criterion='gini',
                          min_samples_leaf=3,oob_score=False,
                          max_features=2,
                          random_state=101)


# In[ ]:


#Fitting the model to train set
rf.fit(X_train,y_train)


# In[ ]:


##Prediction on test set
pred=rf.predict(X_test)


# In[ ]:


##Classification Report
from sklearn.metrics import classification_report
print(classification_report(y_test,pred))


# In[ ]:


##Confusion Matrix
print(confusion_matrix(y_test,pred))


# In[ ]:


##Calculating important metrics Precision score,Recall score,F1_Score    
print("Precision score is",precision_score(y_test,pred))
print("Recall is",recall_score(y_test,pred))
print("F1_score is",f1_score(y_test,pred))


# In[ ]:


##Accuracy test
print(accuracy_score(y_test,pred))


# In[ ]:


##Cross Validating with training set 
print(cross_val_score(rf,X=X_train,y=y_train,cv=5))


# In[ ]:




