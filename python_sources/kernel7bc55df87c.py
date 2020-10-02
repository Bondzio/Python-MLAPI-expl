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


train_data=pd.read_csv('/kaggle/input/titanic/train.csv')


# In[ ]:


train_data.head()


# In[ ]:


test_data=pd.read_csv('/kaggle/input/titanic/test.csv')


# In[ ]:


test_data.head(10)


# In[ ]:


women=train_data.loc[train_data.Sex=='female']['Survived']
rate_women=sum(women)/len(women)
print(rate_women)


# 

# In[ ]:


men=train_data.loc[train_data.Sex=='male']['Survived']
rate_men=sum(men)/len(men)
print(rate_men)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
y=train_data['Survived']
features=['Pclass','Sex','SibSp','Parch']
X=pd.get_dummies(train_data[features])
X_test=pd.get_dummies(test_data[features])


# In[ ]:


model=RandomForestClassifier(n_estimators=100,max_depth=5,random_state=1)
model.fit(X,y)


# In[ ]:


predictions=model.predict(X_test)


# In[ ]:


output=pd.DataFrame({'PassengerId':test_data.PassengerId,'Survived':predictions})
output.to_csv('my_sumission.csv',index=False)
print("Your submission has been successfully saved")


# In[ ]:




