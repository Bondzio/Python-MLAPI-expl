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


#import the  necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


#read the file

cancer  = pd.read_csv('/kaggle/input/breast-cancer-wisconsin-data/data.csv')
cancer.head()


# In[ ]:


print('The shape of the dataset ', cancer.shape)


# The first column is the ID.
# The second column is the target variable. It contains 2 values either Benign(no tumor) or Malignant cancer.
# Rest of the columns specifies the parameters of the cell nuclei which determines whether the tumor is benign or malignant.
# 

# In[ ]:


#create the X and y variable

X = cancer.iloc[:,2:-1].values
y = cancer.iloc[:,1].values


# In[ ]:


#use label encoder to tranform the class labels from original string representation to integers

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
y = le.fit_transform(y)
y


# In[ ]:


le.classes_, le.transform(['M','B'])


# In[ ]:


#train-test split

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                   test_size=0.2,
                                                   stratify=y,
                                                   random_state=1)


# In[ ]:


X_train.shape, X_test.shape, y_test.shape, y_train.shape


# In[ ]:


#use a pipeline of standardScaler, PCA and logistic Regression

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

pipe_lr = make_pipeline(StandardScaler(),
                       PCA(n_components=2),
                       LogisticRegression(random_state=1))
pipe_lr.fit(X_train, y_train)


# In[ ]:


y_pred = pipe_lr.predict(X_test)
y_pred


# In[ ]:


print('Test accuracy: %.3f' % pipe_lr.score(X_test, y_test))


# In[ ]:




