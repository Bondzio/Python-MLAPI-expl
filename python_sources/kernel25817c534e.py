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


from sklearn import datasets, linear_model
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, BaggingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

dfsample = pd.read_csv("/kaggle/input/digit-recognizer/sample_submission.csv")
dftest = pd.read_csv("/kaggle/input/digit-recognizer/test.csv")
dftrain = pd.read_csv("/kaggle/input/digit-recognizer/train.csv")


# In[ ]:


dfy=dftrain["label"]
dfy.shape


# In[ ]:


dfx=dftrain.drop("label", axis=1)
print(dfx.shape)
print(dftest.shape)


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(dfx, dfy, test_size=0.33, random_state=42)
tree = DecisionTreeClassifier()
grad = GradientBoostingRegressor()
bag =  BaggingRegressor()
logistic_reg = LogisticRegression()
rndforestes = RandomForestClassifier()
mlp = MLPClassifier()
svc = LinearSVC()
gauss = GaussianNB()


# In[ ]:


tree.fit(X_train,y_train)


# In[ ]:


grad.fit(X_train,y_train)


# In[ ]:


bag.fit(X_train,y_train)


# In[ ]:


logistic_reg.fit(X_train,y_train)


# In[ ]:


rndforestes.fit(X_train,y_train)


# In[ ]:


mlp.fit(X_train,y_train)


# In[ ]:


svc.fit(X_train,y_train)


# In[ ]:


gauss.fit(X_train,y_train)


# In[ ]:


print(tree.score(X_test,y_test))
print(grad.score(X_test,y_test))
print(bag.score(X_test,y_test))
print(logistic_reg.score(X_test,y_test))
print(rndforestes.score(X_test,y_test))
print(mlp.score(X_test,y_test))
print(svc.score(X_test,y_test))
print(gauss.score(X_test,y_test))


# In[ ]:


models = pd.DataFrame({
    'Model': ['DecisionTreeClassifier', 'GradientBoostingRegressor', 'BaggingRegressor' , 'LogisticRegression' ,'RandomForestClassifier', 'MLPClassifier', 
              'LinearSVC', 'GaussianNB'],
    'Score': [tree.score(X_test,y_test)*100, grad.score(X_test,y_test)*100, bag.score(X_test,y_test)*100, logistic_reg.score(X_test,y_test)*100, rndforestes.score(X_test,y_test)*100,
              mlp.score(X_test,y_test)*100, svc.score(X_test,y_test)*100, gauss.score(X_test,y_test)*100]})
models.sort_values(by='Score', ascending=False)


# In[ ]:


result = mlp.predict(dftest)
result


# In[ ]:


dfresult = dfsample
dfresult["Label"] = result


# In[ ]:


dfsample.info()


# In[ ]:


dfresult.head()

