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


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import warnings
warnings.filterwarnings('ignore')


# In[ ]:


df_raw = pd.read_csv("/kaggle/input/paysim1/PS_20174392719_1491204439457_log.csv") #, nrows=int(1e6))


# In[ ]:


df = df_raw.copy(deep=True)
#df.info()


# In[ ]:


#Dataset's shape
df.shape


# In[ ]:


df = df.rename(columns={'oldbalanceOrg':'oldBalanceOrig', 'newbalanceOrig':'newBalanceOrig',                         'oldbalanceDest':'oldBalanceDest', 'newbalanceDest':'newBalanceDest'})


# In[ ]:


list(df.columns.values)


# In[ ]:


df.head(3)


# In[ ]:


df.tail(3)


# In[ ]:


df.info()


# In[ ]:


df.describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.99]).round(2).T


# In[ ]:


#Check null values
df.isnull().values.any()  #df.isnull().sum()


# In[ ]:


# 'isFlaggedFraud' column analysis
df_temp_Frag_verification = df[df['isFraud']==1]
print("Total Fraud:",df_temp_Frag_verification.shape[0])
print("\n\n'isFraud'x'isFlaggedFraud' Analysis: \n\n",(df_temp_Frag_verification.groupby(['isFraud','isFlaggedFraud'])['step'].size()))
print("\n'isFlaggedFraud' accuracity:", (df[df['isFlaggedFraud']==1].shape[0]/df_temp_Frag_verification.shape[0]))


# In[ ]:


del df_temp_Frag_verification


# In[ ]:


#Conclusion: The 'isFlaggedFraud' accuracity is almost irrelevant, we will drop it from our dataset soon.


# In[ ]:


corrmat = df.corr()
sns.set(font_scale=1.15)
f, ax = plt.subplots(figsize=(8, 6))
hm = sns.heatmap(corrmat, 
                 cbar=True, 
                 annot=True, 
                 square=True, 
                 fmt='.2f', 
                 annot_kws={'size': 10}, 
                 yticklabels=corrmat.columns, 
                 xticklabels=corrmat.columns)


# If you see in the correlation values in heatmap, we observe that these features are highly correlated:
#             newBalanceDest and oldBalanceDest
#             newBalanceOrig and oldBalanceOrig
# Hence we can remove one of the two features for each one. Let's remove oldBalanceDest and oldBalanceOrig too in the future.

# In[ ]:


sns.heatmap(df[['amount','isFraud']].corr(),annot = True)


# In[ ]:


df['step_day'] = df['step'].map(lambda x: x//24)


# In[ ]:


df['hour'] = df['step_day'].map(lambda x: x%24)


# In[ ]:


df['step_week'] = df['step_day'].map(lambda x: x//7)


# In[ ]:


df['step_day'].value_counts().sort_index(ascending=True).plot('bar')
plt.xlabel("Days of the month")
plt.ylabel("# of transactions")
plt.title("# of transactions by days of the month")


# In[ ]:


df['hour'].value_counts().sort_index(ascending=True).plot('bar')
plt.xlabel("Hours of the day")
plt.ylabel("# of transactions")
plt.title("# of transactions by hours of the day")


# In[ ]:


df['step_week'].value_counts().sort_index(ascending=True).plot('bar')
plt.xlabel("Weeks of the month")
plt.ylabel("# of transactions")
plt.title("# of transactions by weeks of the month")


# In[ ]:


df[(df.isFraud == 0)]['hour'].plot.hist(bins=24,color='blue',label='Valid')
plt.xlabel("Hours of the day")
plt.ylabel("# of transactions")
plt.title("# of Valid transactions by hours of the day")
plt.legend()
plt.show()


# In[ ]:


df[(df.isFraud == 1)]['hour'].plot.hist(bins=24,color='orange',label='Fraud')
plt.xlabel("Hours of the day")
plt.ylabel("# of transactions")
plt.title("# of Fraud transactions by hours of the day")
plt.legend()
plt.show()


# In[ ]:


df[(df.isFraud == 0)]['step_day'].plot.hist(bins=7,color='blue',label='Valid')
plt.xlabel("Days of the month")
plt.ylabel("# of transactions")
plt.title("# of Valid transactions by days of the month")
plt.legend()
plt.show()


# In[ ]:


fig, ax = plt.subplots() #1,2, figsize=(7,9)
df[(df.isFraud == 1)]['step_day'].plot.hist(bins=7,color='orange',label='Fraud')
plt.xlabel("Days of the month")
plt.ylabel("# of transactions")
plt.title("# of Fraud transactions by days of the month")
plt.legend()
plt.show()


# In[ ]:


df[(df.isFraud == 0)]['step_week'].plot.hist(bins=4,color='blue',label='Valid')
plt.xlabel("Weeks of the month")
plt.ylabel("# of transactions")
plt.title("# of Valid transactions by weeks of the month")
plt.legend()
plt.show()


# In[ ]:


df[(df.isFraud == 1)]['step_week'].plot.hist(bins=4,color='orange',label='Fraud')
plt.xlabel("Weeks of the month")
plt.ylabel("# of transactions")
plt.title("# of Fraud transactions by weeks of the month")
plt.legend()
plt.show()


# In[ ]:


df['ID_NO'] = df.nameOrig.map(lambda x: x[:1])
df['ID_NO'].value_counts()


# In[ ]:


df['ID_ND'] = df.nameDest.map(lambda x: x[:1])
df['ID_ND'].value_counts(1)


# In[ ]:


df['ID']=df['ID_NO']+df['ID_ND']
df['ID'].value_counts(1).round(2)


# In[ ]:


df.groupby(['type','isFraud'])['type'].count()   #,'amount_O','amount_D'


# In[ ]:


df['wrong_orig_bal'] = np.where((df["oldBalanceOrig"] - df["amount"] - df["newBalanceOrig"]>0.01)|(df["oldBalanceOrig"] - df["amount"] - df["newBalanceOrig"]<-0.01),1,0)
df['wrong_dest_bal'] = np.where((df["newBalanceDest"] + df["amount"] - df["newBalanceDest"]>0.01)|(df["newBalanceDest"] + df["amount"] - df["newBalanceDest"]>0.01),1,0)


# In[ ]:


df.groupby(['wrong_orig_bal','isFraud']).size()#/len(df)).round(4)*100


# In[ ]:


(df.groupby(['wrong_orig_bal','isFraud']).size()/len(df)).round(4)*100


# In[ ]:


df.groupby(['wrong_dest_bal','isFraud']).size()#/len(df)).round(4)*100


# In[ ]:


(df.groupby(['wrong_dest_bal','isFraud']).size()/len(df)).round(4)*100


# In[ ]:


df.head(5).T


# In[ ]:


df['nameOrig'].value_counts().sort_values(ascending=False).head(10)


# In[ ]:


round(len(df['nameOrig'].value_counts())/len(df),3)*100


# In[ ]:


df['nameDest'].value_counts().sort_values(ascending=False).head(10)


# In[ ]:


round(len(df['nameDest'].value_counts())/len(df),3)*100


# In[ ]:


De_Para_type={'type':['PAYMENT','TRANSFER','CASH_OUT','DEBIT','CASH_IN'],'type_num':[0,1,2,3,4]}
De_Para_ID={'ID':['CC','CM','MC','MM'],'ID_num':[0,1,10,11]}
df_Dp_type = pd.DataFrame(De_Para_type, columns = ['type', 'type_num'])
df_Dp_ID = pd.DataFrame(De_Para_ID, columns = ['ID', 'ID_num'])
print(df_Dp_ID)
print()
print(df_Dp_type)


# In[ ]:


df_temp = pd.merge(df, df_Dp_type, left_on='type', right_on='type')
df = pd.merge(df_temp, df_Dp_ID, left_on='ID', right_on='ID')
df.head()


# In[ ]:


df.type.unique()


# In[ ]:


#Get dummies for the type feature
df_get_type = pd.get_dummies(df['type'], drop_first=True)


# In[ ]:


df = pd.concat([df,df_get_type],axis=1)


# In[ ]:


#del df_Dp_ID, df_Dp_type, df_get_type


# In[ ]:


df.head(3).T


# In[ ]:


#Dropping features as previously mentioned
df_clean = df.drop(columns=['type','nameOrig','oldBalanceOrig','nameDest','oldBalanceDest','isFlaggedFraud'], axis=1) #inplace=True


# In[ ]:


df_clean = df_clean.drop(columns=['ID_NO','ID_ND','ID'], axis=1)
#df_clean = df_clean.drop(columns=['type'], axis=1)


# In[ ]:


df_clean.head(3)


# In[ ]:


df.shape


# In[ ]:


df_clean.shape


# In[ ]:


df_clean.groupby(['isFraud']).size()


# In[ ]:


df_clean_Fraud = df_clean[df['isFraud']==1]
df_clean_Valid = df_clean[df['isFraud']==0]
print("Before Sample:\n",df_clean_Fraud.shape[0], df_clean_Valid.shape[0])
#df_clean_Valid.head()
#df_clean_Fraud.shape[0]
df_clean_Valid = df_clean_Valid.sample(df_clean_Fraud.shape[0])
print("After Sample:\n",df_clean_Fraud.shape[0],df_clean_Valid.shape[0])


# In[ ]:


df_new = pd.concat([df_clean_Valid, df_clean_Fraud])
df_new.shape[0]


# In[ ]:


df_new.head()


# In[ ]:


df_final=df_new


# In[ ]:


#Now separate the independent varaibles as X and dependent variable i.e. isFraud as y_target
y_target = df_final['isFraud']
X=df_final.drop('isFraud', axis=1)
X.shape,y_target.shape[0]


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y_target, test_size = 0.3, random_state = 26, stratify=y_target)


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

classifiers = [
    KNeighborsClassifier(3),
    GaussianNB(),
    LogisticRegression(),
    SVC(),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    GradientBoostingClassifier()]


for clf in classifiers:
    
    clf.fit(X_train, y_train)
    
    name = clf.__class__.__name__
    
    print("="*30)
    print(name)
    
    print('****Results****')
    
    y_pred = clf.predict(X_train)
    
    print("Accuracy:     ", round(metrics.accuracy_score(y_train, y_pred),4)*100)
    print("Precision:    ", round(metrics.precision_score(y_train, y_pred),4)*100)
    print("Recall:       ", round(metrics.recall_score(y_train, y_pred),4)*100)


# In[ ]:



for clf in classifiers:
    
    clf.fit(X_test, y_test)
    
    name = clf.__class__.__name__
    
    print("="*30)
    print(name)
    
    print('****Results****')
    
    y_pred = clf.predict(X_test)
    
    print("Accuracy:     ", round(metrics.accuracy_score(y_test, y_pred),4)*100)
    print("Precision:    ", round(metrics.precision_score(y_test, y_pred),4)*100)
    print("Recall:       ", round(metrics.recall_score(y_test, y_pred),4)*100)

