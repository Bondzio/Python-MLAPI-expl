#!/usr/bin/env python
# coding: utf-8

# In[48]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[49]:


dataset = pd.read_csv('../input/50_Startups.csv')


# In[50]:


dataset.columns


# In[51]:


X = dataset.iloc[:,:-1].values
y = dataset.iloc[:,-1].values


# In[52]:


X


# In[53]:


from sklearn.preprocessing import LabelEncoder, OneHotEncoder

labelencoder_x = LabelEncoder()
X[:,3] = labelencoder_x.fit_transform(X[:,3])

onehotencoder = OneHotEncoder(categorical_features=[3])
X = onehotencoder.fit_transform(X).toarray()


# In[55]:


type(X)


# In[ ]:





# In[ ]:




