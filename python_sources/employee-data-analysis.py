#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

data=pd.read_csv("../input/HR_comma_sep.csv")

# Any results you write to the current directory are saved as output.


# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier


# In[ ]:


data.head()


# In[ ]:


data.dtypes


# In[ ]:


obcol = ['salary','sales']


# In[ ]:


le = LabelEncoder()
for df in obcol:
    data[df]=le.fit_transform(data[df].astype('str'))


# In[ ]:


np.random.seed(42)
data['ran'] = np.random.choice(range(0,14998),data.shape[0])
data.head()


# In[ ]:


train=data[data['ran']<12000]
test=data[data['ran']>=12000]


# In[ ]:


print(test.shape)
print(train.shape)


# In[ ]:


train.columns


# In[ ]:


train=train.drop(['ran',],axis=1)
test=test.drop(['ran'],axis=1)


# In[ ]:


corr=train.corr()
corr['left']


# In[ ]:


plt.figure(figsize=(12,12))
x=sns.heatmap(corr, vmax=1, square=True)


# In[ ]:


X_train=train.drop(['left'],axis=1)
X_test=test.drop(['left'],axis=1)
Y_train=train['left']
Y_test=test['left']


# Random Forest

# In[ ]:


rf = RandomForestRegressor(n_estimators=100,oob_score=True,random_state=42,max_features=.3)
rf.fit(X_train,Y_train)
score=rf.score(X_train,Y_train)
print(round(score*100,2))
y = rf.oob_prediction_
roc_auc_score(Y_train,y)


# SVC

# In[ ]:


svc=SVC(max_iter=10)
print(svc.fit(X_train,Y_train))
score=rf.score(X_train,Y_train)
print(round(score*100,2))


# 99.0
# 0.99047021065466334

# array([[2271,    5],
#        [  25,  654]])

# In[ ]:


Y_pred=rf.predict(X_test)
confusion_matrix(Y_test,Y_pred.round(0))

