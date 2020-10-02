#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[ ]:


import os as s
import pandas as pd


# In[ ]:


data=pd.read_csv("../input/train.csv")


# In[ ]:


target=pd.read_csv("../input/trainLabels.csv")


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test =train_test_split(data,target,train_size=0.7,random_state=42)


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
clf=DecisionTreeClassifier(criterion='entropy')
clf.fit(X_train,y_train)


# In[ ]:


clf.score(X_test,y_test)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier 
model=RandomForestClassifier(n_estimators=1000,criterion="entropy",n_jobs=-1,random_state=22,verbose=1)


# In[ ]:


model.fit(X_train,y_train)


# In[ ]:


model.score(X_test,y_test)


# In[ ]:


from sklearn.svm import SVC
svm=SVC()
svm.fit(X_train,y_train)

print(svm.score(X_test,y_test))


# In[ ]:


print(svm.score(X_test,y_test))


# In[ ]:




