#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df = pd.read_csv('../input/train.csv')
df.head(5)
test = pd.read_csv('../input/test.csv')


# In[ ]:


sns.barplot(x="Pclass", y="Survived", data=df);


# In[ ]:


sns.barplot(x="Sex", y="Survived", data=df);


# In[ ]:


sns.barplot(x="Embarked", y="Survived", data=df);


# In[ ]:


sns.barplot(x="Pclass", y="Survived", data=df);


# In[ ]:


import re
df['Title'] = df.Name.apply(lambda x: re.search(' ([A-Z][a-z]+)\.', x).group(1))
sns.countplot(x='Title', data=df);
plt.xticks(rotation=45);


# In[ ]:


df['Title'] = df['Title'].replace({'Mlle':'Miss', 'Mme':'Mrs', 'Ms':'Miss'})
df['Title'] = df['Title'].replace(['Don', 'Dona', 'Rev', 'Dr',
                                            'Major', 'Lady', 'Sir', 'Col', 'Capt', 'Countess', 'Jonkheer'],'Other')

sns.countplot(x='Title', data=df);
plt.xticks(rotation=45);


# In[ ]:


df.drop('Name',axis=1, inplace=True)

df.head(5)


# In[ ]:


df['Has_Cabin'] = ~df.Cabin.isnull()
df.drop('Cabin',axis=1, inplace=True)
df.head(5)


# In[ ]:


df.drop('Ticket',axis=1, inplace=True)

df.head(5)


# In[ ]:


df = pd.get_dummies(df)

df.head()


# In[ ]:


x = df.iloc[1:].values
y = df.iloc[0].values
print(x.shape)
print(y.shape)


# In[ ]:


df.head(5)


# In[ ]:


df['Age'] = df.Age.fillna(df.Age.median())


# In[ ]:


df['CatAge'] = pd.qcut(df.Age, q=4, labels=False )
df['CatFare']= pd.qcut(df.Fare, q=4, labels=False)
df.head()


# In[ ]:


df = df.drop(['Age', 'Fare'], axis=1)

print(x.shape)
print(y.shape)


# In[ ]:


df.info()


# In[ ]:


df.head(5)


# In[ ]:


y = df['Survived'].values 
X = df.drop('Survived',axis=1).values
print(X.shape)
print(y.shape)


# In[ ]:


import xgboost as xgb
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

xgb_model = xgb.XGBClassifier(objective="binary:logistic", random_state=42)
xgb_model.fit(X, y)

y_pred = xgb_model.predict(X)

print(confusion_matrix(y, y_pred))
print(precision_recall_fscore_support(y, y_pred, average='macro'))


# In[ ]:


from sklearn.model_selection import cross_val_score
result = cross_val_score(xgb_model, X, y_pred, cv=10) # r2 scores
print(result.mean())


# In[ ]:


test.head(5)


# In[ ]:


Y_pred = xgb_model.predict(test)
df['Survived'] = Y_pred
df[['PassengerId', 'Survived']].to_csv('data/predictions/my_sub.csv', index=False)

