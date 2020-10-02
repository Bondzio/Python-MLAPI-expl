#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('pylab', 'inline')
pylab.rcParams['figure.figsize'] = (10, 6) 
color = sns.color_palette()

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

# import TPOT and sklearn stuff
from tpot import TPOTClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import sklearn.metrics


# In[ ]:


# to customize the displayed area of the dataframe 
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# In[ ]:


df=pd.read_csv('/kaggle/input/Train_v2.csv')


# In[ ]:


df.head()


# In[ ]:


df.shape


# In[ ]:


df.info()


# In[ ]:


for i in df.columns:
    print(i,df[i].unique())
    print("%%%%%%%%")


# In[ ]:


def bank_account_num(x):
    if x=="Yes":
        return 1
    else:
        return 0

def gender_num(x):
    if x=="Male":
        return 1
    else:
        return 0
    
def location_num(x):
    if x=="Urban":
        return 1
    else:
        return 0
    
def phone_num(x):
    if x=="Yes":
        return 1
    else:
        return 0
    
def phone_num(x):
    if x=="Yes":
        return 1
    else:
        return 0
    


# In[ ]:


df['bank_account']=df['bank_account'].apply(lambda x:bank_account_num(x))
df['gender_of_respondent']=df['gender_of_respondent'].apply(lambda x:gender_num(x))
df['location_type']=df['location_type'].apply(lambda x:location_num(x))
df['cellphone_access']=df['cellphone_access'].apply(lambda x:phone_num(x))


# In[ ]:


maxi=max(df['age_of_respondent'])
df['age_of_respondent']=df['age_of_respondent'].apply(lambda x:x/maxi)
maxi=max(df['household_size'])
df['household_size']=df['household_size'].apply(lambda x:x/maxi)


# In[ ]:


df.head()


# In[ ]:


df = pd.get_dummies(df, columns=['relationship_with_head'], prefix = ['R.W.H'])
df = pd.get_dummies(df, columns=['year'], prefix = ['Y'])
df = pd.get_dummies(df, columns=['marital_status'], prefix = ['MS'])
df = pd.get_dummies(df, columns=['education_level'], prefix = ['EL'])
df = pd.get_dummies(df, columns=['job_type'], prefix = ['JT'])
df = pd.get_dummies(df, columns=['country'], prefix = ['C'])


# In[ ]:


df.head()


# In[ ]:


X=df.drop(['uniqueid', 'bank_account'], axis=1)


# In[ ]:


Y=df['bank_account']


# In[ ]:


X_train, X_test, y_train,y_test=train_test_split(X,Y,train_size=0.75,random_state=123)


# In[ ]:


# tpot=TPOTClassifier(generations=5,population_size=100, cv=5,subsample=0.3,verbosity=2,n_jobs=-1)
# tpot.fit(X_train,y_train)


# In[ ]:


# print(tpot.score(X_train,y_train))


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
clf =  RandomForestClassifier(bootstrap=False, criterion="entropy", max_features=0.55, min_samples_leaf=8, min_samples_split=12, n_estimators=100)
clf.fit(X_train, y_train)


# In[ ]:


y_pred=clf.predict(X_test)

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
print("Accuracy: %.2f%%" % (accuracy_score(y_test, y_pred)*100))
print("F1: %.2f%%" % (f1_score(y_test, y_pred)*100))


# In[ ]:


import xgboost as xgb

model1 = xgb.XGBClassifier()
model2 = xgb.XGBClassifier(n_estimators=100, max_depth=8, learning_rate=0.1, subsample=0.5)

model1.fit(X_train, y_train)
y_pred=model1.predict(X_test)
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
print("Accuracy: %.2f%%" % (accuracy_score(y_test, y_pred)*100))
print("F1: %.2f%%" % (f1_score(y_test, y_pred)*100))


# In[ ]:


model2.fit(X_train, y_train)
y_pred=model2.predict(X_test)

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
print("Accuracy: %.2f%%" % (accuracy_score(y_test, y_pred)*100))
print("F1: %.2f%%" % (f1_score(y_test, y_pred)*100))


# In[ ]:


from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
print("Accuracy: %.2f%%" % (accuracy_score(y_test, y_pred)*100))
print("F1: %.2f%%" % (f1_score(y_test, y_pred)*100))


# In[ ]:


# from sklearn.linear_model import LogisticRegression
# clf2 =  LogisticRegression().fit(X_train, y_train)
# y_pred2=clf2.predict(X_test)


# In[ ]:


# from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
# print("Accuracy: %.2f%%" % (accuracy_score(y_test, y_pred2)*100))
# print("F1: %.2f%%" % (f1_score(y_test, y_pred2)*100))


# In[ ]:


df5=pd.read_csv('/kaggle/input/SubmissionFile.csv')


# In[ ]:


df5.head()


# In[ ]:


df3=pd.read_csv('/kaggle/input/Test_v2.csv')


# In[ ]:


df3.head()


# In[ ]:


df3['gender_of_respondent']=df3['gender_of_respondent'].apply(lambda x:gender_num(x))
df3['location_type']=df3['location_type'].apply(lambda x:location_num(x))
df3['cellphone_access']=df3['cellphone_access'].apply(lambda x:phone_num(x))


# In[ ]:


maxi=max(df3['age_of_respondent'])
df3['age_of_respondent']=df3['age_of_respondent'].apply(lambda x:x/maxi)
maxi=max(df3['household_size'])
df3['household_size']=df3['household_size'].apply(lambda x:x/maxi)


# In[ ]:


df3 = pd.get_dummies(df3, columns=['relationship_with_head'], prefix = ['R.W.H'])
df3 = pd.get_dummies(df3, columns=['year'], prefix = ['Y'])
df3 = pd.get_dummies(df3, columns=['marital_status'], prefix = ['MS'])
df3 = pd.get_dummies(df3, columns=['education_level'], prefix = ['EL'])
df3 = pd.get_dummies(df3, columns=['job_type'], prefix = ['JT'])
dfy=df3
df3 = pd.get_dummies(df3, columns=['country'], prefix = ['C'])


# In[ ]:


df3.head()


# In[ ]:


dfy.head()


# In[ ]:


X1=df3.drop(['uniqueid'], axis=1)


# In[ ]:


X1.head()


# In[ ]:


Y1=model2.predict(X1)


# In[ ]:


Y1


# In[ ]:


L=list(dfy['country'])
M=list(dfy['uniqueid'])


# In[ ]:


LM=[]
for i in range(len(L)):
    LM.append(M[i]+" x "+L[i])


# In[ ]:


LM


# In[ ]:


d = {"unique_id":LM,'bank_account': Y1}


# In[ ]:


dfx=pd.DataFrame(data=d)


# In[ ]:


dfx.head()


# In[ ]:


dfx.to_csv('financial inclusion.csv',index=False)

