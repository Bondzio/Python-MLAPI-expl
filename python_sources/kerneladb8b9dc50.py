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


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


health_data=pd.read_csv('../input/heart.csv')


# In[ ]:


health_data


# In[ ]:


#Extracting only the independent variables
X=health_data.iloc[:,[2,3,4,5,6,7,8,9,10,11,12]].values

#Extracting only the dependent variables
Y=health_data.iloc[:,13].values


# In[ ]:


sns.heatmap(health_data.corr())


# In[ ]:


#Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split( X, Y, test_size=0.25, random_state=0)


# In[ ]:


#Features scaling
from sklearn.preprocessing import StandardScaler
sc_X=StandardScaler()
X_train=sc_X.fit_transform(X_train)
X_test=sc_X.fit_transform(X_test)


# In[ ]:


#Fitting Logistic Regression to training set
from sklearn.linear_model import LogisticRegression
classifier=LogisticRegression(random_state=0)
classifier.fit(X_train,Y_train)


# In[ ]:


#Predicting the test set results
Y_pred=classifier.predict(X_test)


# In[ ]:


Y_pred


# In[ ]:


#Confusion metrics Evaluation
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(Y_test,Y_pred)
cm


# In[ ]:


#Total observation/data used for testing
25+8+4+39


# In[ ]:


#Total observation predicted correctly
25+39


# In[ ]:


#Accuracy of the prediction
64/76

