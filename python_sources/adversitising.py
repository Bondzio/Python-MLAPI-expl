#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# Read in the advertising.csv file

# In[ ]:


df = pd.read_csv('/kaggle/input/advertising/advertising.csv')


# Import necessary libraries

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns


# Check the head of data

# In[ ]:


df.head()


# Check info and describe to check if there are any missing values and max/min values

# In[ ]:


df.info()


# In[ ]:


df.describe()


# Checking the Age column

# In[ ]:


sns.distplot(df['Age'],kde=False)


# 

# In[ ]:


sns.set(style="whitegrid")
sns.jointplot('Age', 'Area Income', df)


# In[ ]:


sns.jointplot('Age', 'Daily Time Spent on Site', df, kind='kde')


# In[ ]:


sns.jointplot('Daily Time Spent on Site', 'Daily Internet Usage', df)


# In[ ]:


sns.pairplot(df, hue='Clicked on Ad')


# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


# In[ ]:


X = df[['Daily Time Spent on Site', 'Age', 'Area Income',
       'Daily Internet Usage', 'Male']]
y = df['Clicked on Ad']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)


# In[ ]:


lgmodel = LogisticRegression()
lgmodel.fit(X_train, y_train)


# In[ ]:


pre = lgmodel.predict(X_test)


# In[ ]:


from sklearn.metrics import classification_report
print(classification_report(y_test, pre))

