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
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


## Loading the dataset
wine=pd.read_csv('../input/red-wine-quality-cortez-et-al-2009/winequality-red.csv', sep=',')


# In[ ]:


wine.head()


# In[ ]:


wine.info()


# In[ ]:


wine.isnull().sum()


# In[ ]:


### processing the Data
bins=(2,6.5,8)
group_names=['bad', 'good']
wine['quality']=pd.cut(wine['quality'], bins=bins, labels=group_names)
wine['quality'].unique()
                


# In[ ]:


label_quality=LabelEncoder()
wine['quality']=label_quality.fit_transform(wine['quality'])


# In[ ]:


wine.head()


# In[ ]:


wine['quality'].value_counts()


# In[ ]:


## plotting the data
sns.countplot(wine['quality'])


# In[ ]:


## we will separate the dataset as response variable and feature variable
X=wine.drop('quality',axis=1)
y=wine['quality']


# In[ ]:


## We will now Split data into Train and test data 
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)


# In[ ]:


## Applying standard scaling to get optimized result
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.transform(X_test)


# In[ ]:


X_train[:10]


# In[ ]:


### building model with Random Forest Classifier
rfc=RandomForestClassifier(n_estimators=200)
rfc.fit(X_train,y_train)
pred_rfc=rfc.predict(X_test)


# In[ ]:


pred_rfc[ :20]


# In[ ]:


## Lets check the model performance
print(classification_report(y_test,pred_rfc))
print(confusion_matrix(y_test,pred_rfc))


# In[ ]:


## lets build another model with SVM 
clf=svm.SVC()
clf.fit(X_train,y_train)
pred_clf=clf.predict(X_test)


# In[ ]:


## lets check the model performance
print(classification_report(y_test,pred_clf))
print(confusion_matrix(y_test,pred_clf))


# In[ ]:


## we ll bulid third model with neural Network
mlpc=MLPClassifier(hidden_layer_sizes=(11,11,11), max_iter=500)
mlpc.fit(X_train,y_train)
pred_mlpc=mlpc.predict(X_test)


# In[ ]:


## Check the model performance
print(classification_report(y_test,pred_mlpc))
print(confusion_matrix(y_test, pred_mlpc))


# In[ ]:


from sklearn.metrics import accuracy_score
cm=accuracy_score(y_test, pred_rfc)
cm


# In[ ]:




