#!/usr/bin/env python
# coding: utf-8

# ### Please UPVOTE if you like my work!!!

# # Project Domain - Bank

# ## Task- Predict Defaulters

# ### HIGHLIGHTS 

# > **DownSampling**<br>
# > **EDA**<br>
# > **ML algorithms(XGB, Logistic Regression, RandomForest)**<br>
# > **CrossValidation**

# #### Importing Libraries

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.under_sampling import NearMiss
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
import xgboost
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_curve

pd.options.display.max_rows = 20


# #### Reading Data

# In[ ]:


get_ipython().run_line_magic('time', "data = pd.read_table('../input/XYZCorp_LendingData.txt',parse_dates=['issue_d'],low_memory=False)")


# # Exploratory Data Analysis

# In[ ]:


data.head() # Top 5 rows


# In[ ]:


data.shape #(rows,columns)


# ### Dependent Variable Analysis

# In[ ]:


data['default_ind'].value_counts()


# In[ ]:


sns.countplot('default_ind',data=data)


# **Thus, we can conclude it is an Imbalanced Data**

# #### NULL Values

# In[ ]:


data.isnull().sum()


# #### Delete columns having more 8M records as NULL 

# In[ ]:


lis=data.isnull().sum()
for i in range(len(lis)):
    if lis[i]>800000:
        del data['{}'.format(lis.index[i])]


# #### Correlation of O/P variable with all others

# In[ ]:


lis=data[data.columns].corr()['default_ind'][:]
data[data.columns].corr()['default_ind'][:]


# #### Removing columns with very low Correlation

# In[ ]:


lis2=[]
for i in range(len(lis)):
    if lis[i]<0.02 and lis[i]>(-0.02):
        lis2.append(lis.index[i])


# In[ ]:


for i in range(len(lis2)):
    del data['{}'.format(lis2[i])]


# In[ ]:


data[data.columns].corr()['default_ind'][:]


# #### Total columns left- 43

# In[ ]:


data.info()


# ## Text Data(Object Type)

# #### APPLICATION_TYPE

# In[ ]:


data['application_type'].value_counts()


# In[ ]:


sns.countplot('application_type',data=data)


# #### Grouping based on O/P variable

# In[ ]:


df=data.groupby('application_type')
df['default_ind'].value_counts()


# In[ ]:


data['application_type'] = np.where(data['application_type']=='INDIVIDUAL', 0, data['application_type'])
data['application_type'] = np.where(data['application_type']=='JOINT', 1, data['application_type'])


# In[ ]:


data['application_type'].value_counts()


# In[ ]:


data['application_type']=data['application_type'].astype(float)
# Object to Float type


# ### Verification_Status

# In[ ]:


#data['verification_status'].value_counts()
df=data.groupby('verification_status')
df['default_ind'].value_counts()


# In[ ]:


sns.countplot('verification_status',data=data,hue='default_ind')


# In[ ]:


df=pd.get_dummies(data['verification_status'],drop_first=True)
data=pd.concat([df,data],axis=1)
del data['verification_status']
# Dummy Variables


# ### Initial_list_status

# In[ ]:


data['initial_list_status'].value_counts()


# In[ ]:


sns.countplot('initial_list_status',data=data,hue='default_ind')


# In[ ]:


data['initial_list_status'] = np.where(data['initial_list_status']=='f', 0, data['initial_list_status'])
data['initial_list_status'] = np.where(data['initial_list_status']=='w', 1, data['initial_list_status'])


# In[ ]:


data['initial_list_status'].value_counts()


# In[ ]:


data['initial_list_status']=data['initial_list_status'].astype(float)


# ### Term

# In[ ]:


data['term'].value_counts()


# In[ ]:


sns.countplot('term',data=data,hue='default_ind')


# In[ ]:


data['term'] = np.where(data['term']==' 36 months', 0, data['term'])
data['term'] = np.where(data['term']==' 60 months', 1, data['term'])


# In[ ]:


data['term'].value_counts()


# In[ ]:


data['term']=data['term'].astype(float)


# ### Grade

# In[ ]:


data['grade'].value_counts()


# In[ ]:


sns.countplot('grade',data=data,hue='default_ind',color='red',saturation=0.5)


# In[ ]:


data['grade'] = np.where(data['grade']=='A', 0, data['grade'])
data['grade'] = np.where(data['grade']=='B', 0, data['grade'])
data['grade'] = np.where(data['grade']=='C', 0, data['grade'])
data['grade'] = np.where(data['grade']=='D', 1, data['grade'])
data['grade'] = np.where(data['grade']=='E', 1, data['grade'])
data['grade'] = np.where(data['grade']=='F', 1, data['grade'])
data['grade'] = np.where(data['grade']=='G', 1, data['grade'])


# In[ ]:


data['grade'].value_counts()


# In[ ]:


data['grade']=data['grade'].astype(float)


# ### Home_Ownership

# In[ ]:


data['home_ownership'].value_counts()


# In[ ]:


df=data.groupby('home_ownership')
df['default_ind'].value_counts()


# In[ ]:


sns.countplot('home_ownership',data=data,hue='default_ind')


# In[ ]:


data['home_ownership'] = np.where(data['home_ownership']=='RENT', 1, data['home_ownership'])
data['home_ownership'] = np.where(data['home_ownership']=='OWN', 1, data['home_ownership'])
data['home_ownership'] = np.where(data['home_ownership']=='MORTGAGE', 1, data['home_ownership'])
data['home_ownership'] = np.where(data['home_ownership']=='NONE', 2, data['home_ownership'])
data['home_ownership'] = np.where(data['home_ownership']=='OTHER', 2, data['home_ownership'])
data['home_ownership'] = np.where(data['home_ownership']=='ANY', 0, data['home_ownership'])


# In[ ]:


data['home_ownership'].value_counts()


# In[ ]:


df=pd.get_dummies(data['home_ownership'],drop_first=True)
data=pd.concat([df,data],axis=1)
del data['home_ownership']
# Dummy Variables


# ### Pymnt_Plan

# In[ ]:


data['pymnt_plan'].value_counts()


# In[ ]:


del data['pymnt_plan']


# In[ ]:


data.info()


# ### Last_credit_pull_d

# In[ ]:


data['last_credit_pull_d'] = pd.to_datetime(data['last_credit_pull_d'])
data['Month'] = data['last_credit_pull_d'].apply(lambda x: x.month)
data['Year'] = data['last_credit_pull_d'].apply(lambda x: x.year)
data = data.drop(['last_credit_pull_d'], axis = 1)


# #### Removing all object type Features

# In[ ]:


lis3=[]
for i in range(len(data.dtypes)):
    if data.dtypes[i]!='object':
        lis3.append(data.dtypes.index[i])


# In[ ]:


data=data[lis3]


# In[ ]:


data.isnull().sum()


# #### Deleting unnecessary columns

# In[ ]:


del data['mths_since_last_record']
del data['id']
del data['member_id']
del data['tot_cur_bal']
del data['total_rev_hi_lim']
del data['policy_code']


# #### HEATMAP

# In[ ]:


plt.figure(figsize=(20,20))
sns.heatmap(data.corr(),annot=False,cmap='magma')


# #### Filling Null values

# In[ ]:


data['revol_util'].fillna(data['revol_util'].mean(),inplace=True)
data['Month'].fillna(data.mode()['Month'][0],inplace=True)
data['Year'].fillna(data.mode()['Year'][0],inplace=True)


# ### Final Shape

# In[ ]:


data.shape


# #### Making Output Variable last column

# In[ ]:


data['last']=data['default_ind']
del data['default_ind']
data['default_ind']=data['last']
del data['last']


# # Continuous Variable

# In[ ]:


data.info()


# #### Int_rate

# In[ ]:


sns.boxplot('grade','int_rate',data=data)


# In[ ]:


sns.violinplot('default_ind','int_rate',data=data,bw='scott',inner='quartile')


# #### annual_inc

# In[ ]:


sns.stripplot('default_ind','annual_inc',data=data,jitter=True)


# #### inq_last_6mths

# In[ ]:


sns.boxplot('default_ind','inq_last_6mths',data=data)


# #### out_prncp

# In[ ]:


sns.boxplot('default_ind','out_prncp',data=data)


# #### total_pymnt

# In[ ]:


sns.boxplot('default_ind','total_pymnt',data=data)


# #### total_rec_prncp

# In[ ]:


sns.stripplot('default_ind','total_rec_prncp',data=data,jitter=True)


# #### total_rec_int

# In[ ]:


sns.violinplot('default_ind','total_rec_int',data=data,inner='quartile')


# #### Recoveries

# In[ ]:


sns.boxplot('default_ind','recoveries',data=data)


# In[ ]:


sns.stripplot('default_ind','recoveries',data=data,jitter=True)


# #### collection_recovery_fee

# In[ ]:


sns.stripplot('default_ind','collection_recovery_fee',data=data,jitter=True)


# #### Last_pymnt_amt

# In[ ]:


sns.stripplot('default_ind','last_pymnt_amnt',data=data,jitter=True)


# In[ ]:


data.info()


# In[ ]:


data.head()


# ### Machine Learning/Modelling

# In[ ]:


'''train = data[data['issue_d'] < '2015-6-01']
test = data[data['issue_d'] >= '2015-6-01']'''


# ### Deleting date column

# In[ ]:


del data['issue_d']


# In[ ]:


'''X_train=train.iloc[:,:-1].values
y_train=train.iloc[:,-1].values
X_test=test.iloc[:,:-1].values
y_test=test.iloc[:,-1].values'''


# #### Independent & Dependent Varibles

# In[ ]:


X=data.iloc[:,:-1].values
y=data.iloc[:,-1].values


# #### Downsampling

# In[ ]:


os=NearMiss(random_state=42)
X_res,y_res=os.fit_sample(X,y)


# #### Splitting data

# In[ ]:


X_train,X_test,y_train,y_test=train_test_split(X_res,y_res,test_size=0.25,random_state=0)


# In[ ]:


'''
class_weights = class_weight.compute_class_weight('balanced',
                                                 np.unique(y_train),
                                                 y_train)
#model.fit(X_train, y_train, class_weight=class_weights)'''


# In[ ]:


'''class_weights'''


# In[ ]:


'''
xgb= XGBClassifier()
xgb.fit(X_train,y_train)
y_pred=xgb.predict(X_test)'''


# In[ ]:


'''
lr=LogisticRegression(class_weight="balanced")
lr.fit(X_train,y_train)
y_pred=lr.predict(X_test)'''


# #### Modelling

# In[ ]:


lr=RandomForestClassifier(n_estimators=10, criterion='entropy')
lr.fit(X_train,y_train)
y_pred=lr.predict(X_test)
y_pred_prob=lr.predict_proba(X_test)


# #### Evaluation Metrics

# In[ ]:


print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))


# #### Cross-Validation

# In[ ]:


acc=cross_val_score(estimator=lr,X=X_train,y=y_train,cv=10)
acc.mean()


# ### ROC Curve

# In[ ]:


y_pred_prob_1=y_pred_prob[:,1]


# In[ ]:


fpr,tpr,thresholds=roc_curve(y_test,y_pred_prob_1)
plt.plot(fpr,tpr)
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.0])
plt.title('ROC Curve')
plt.xlabel('FalsePositiveRate')
plt.ylabel('TruePositiveRate')
plt.grid(True)

