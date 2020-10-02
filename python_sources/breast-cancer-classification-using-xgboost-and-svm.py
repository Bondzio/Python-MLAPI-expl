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


ds=pd.read_csv("/kaggle/input/breast-cancer-wisconsin-data/data.csv")


# In[ ]:


ds.head()


# In[ ]:


#checking the number of rows in the dataset
len(ds)


# In[ ]:


#checking the null values in each column
ds.isna().sum()


# In[ ]:


#giving the inputs and outputs
x=ds.iloc[:,2:-1].values
y=ds.iloc[:,1:2].values
y


# In[ ]:


#data preprocessing 
from sklearn.preprocessing import LabelEncoder
l=LabelEncoder()
y=l.fit_transform(y)
y


# In[ ]:


#splitting the data into training and split
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.3)


# In[ ]:


#algorithm approach
from catboost import CatBoostClassifier

d = CatBoostClassifier(iterations=1000,
                          learning_rate=0.05,
                          depth=4)
d.fit(xtrain,ytrain)


# In[ ]:


ypred=d.predict(xtest)
ypred


# In[ ]:


#confusion matrix for accuracy
from sklearn.metrics import confusion_matrix
a=confusion_matrix(ytest,ypred)
a


# In[ ]:


accuracy=(a[0][0]+a[1][1])/(len(xtest))
accuracy=accuracy*100
accuracy


# In[ ]:



from sklearn import svm
r=svm.SVC(kernel='linear')
r.fit(xtrain,ytrain)


# In[ ]:


rpred=r.predict(xtest)
rpred


# In[ ]:


#confusion matrix for accuracy
from sklearn.metrics import confusion_matrix
a1=confusion_matrix(ytest,rpred)
a1


# In[ ]:


accuracys=(a1[0][0]+a1[1][1])/(len(xtest))
accuracysvm1=accuracys*100
accuracysvm1


# In[ ]:




