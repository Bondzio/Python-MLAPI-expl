#!/usr/bin/env python
# coding: utf-8

# In[321]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[322]:


data=pd.read_csv('../input/train.csv')
test=pd.read_csv('../input/test.csv')
data.head()


# In[323]:


data.info()


# In[324]:


data.Age.fillna(data.Age.median(),inplace=True)
test.Age.fillna(data.Age.median(),inplace=True)
test.Fare.fillna(data['Fare'][data['Pclass']==3].median(),inplace=True)
data.Embarked.fillna('S',inplace=True)
data.drop(['Cabin','PassengerId','Ticket','Name'],axis=1,inplace=True)
test.drop(['Cabin','PassengerId','Ticket','Name'],axis=1,inplace=True)
data.info()
test.info()


# In[325]:


dummies=pd.get_dummies(data['Sex'])
data=pd.concat([data,dummies],axis=1)
data.drop('Sex',axis=1,inplace=True)
data.info()
dummies=pd.get_dummies(test['Sex'])
test=pd.concat([test,dummies],axis=1)
test.drop('Sex',axis=1,inplace=True)
test.info()


# In[326]:


dummies=pd.get_dummies(data['Embarked'])
data=pd.concat([data,dummies],axis=1)
data.drop('Embarked',axis=1,inplace=True)
data.info()
dummies=pd.get_dummies(test['Embarked'])
test=pd.concat([test,dummies],axis=1)
test.drop('Embarked',axis=1,inplace=True)
test.info()


# In[327]:


data.Age=data.Age.astype(int)


# In[328]:


import xgboost as xgb
model=xgb.XGBClassifier(learning_rate=0.001,n_estimators=1000)
model.fit(data.drop('Survived',axis=1),data.Survived)
print(model.score(data.drop('Survived',axis=1),data.Survived))


# In[329]:


ans=model.predict(test)
x=pd.read_csv('../input/gender_submission.csv')
a=pd.DataFrame({'PassengerId':x['PassengerId'],'Survived':ans})
a.to_csv('submit.csv',index=False)

