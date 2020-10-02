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
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC


# In[ ]:


dataset=pd.read_csv(r"../input/iris-dataset/iris.csv")


# In[ ]:


dataset


# In[ ]:


dataset.info()


# In[ ]:


dataset.head()


# In[ ]:


dataset.tail()


# In[ ]:


dataset.describe()


# In[ ]:


print(dataset.groupby('Species').size())


# In[ ]:


dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
plt.show()


# In[ ]:


dataset.hist()
plt.show()


# In[ ]:


data=dataset.values
x=data[:,0:4]
y=data[:,4]


# In[ ]:


#spliting data
X_train,X_validation,Y_train,Y_validation=train_test_split(x,y,test_size=0.3,random_state=0)


# In[ ]:


#algorithm1
result= SVC()
result.fit(X_train,Y_train)
predictions=result.predict(X_validation)


# In[ ]:


#predictions1
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))


# In[ ]:


#algorithm2
result2= DecisionTreeClassifier()
result2.fit(X_train,Y_train)
predictions2=result2.predict(X_validation)


# In[ ]:


#predictions2
print(accuracy_score(Y_validation, predictions2))
print(confusion_matrix(Y_validation, predictions2))
print(classification_report(Y_validation, predictions2))


# In[ ]:


#algorithm3
result=LogisticRegression()
result.fit(X_train,Y_train)
predictions=result.predict(X_validation)


# In[ ]:


#predictions3
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))


# In[ ]:




