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


# In[ ]:


import pandas as pd
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv("/kaggle/input/hr-analytics/HR_comma_sep.csv")


# In[ ]:


df.head()


# In[ ]:


left = df[df.left==1]
left.shape


# In[ ]:


retained = df[df.left==0]
retained.shape


# In[ ]:


df.groupby('left').mean()


# In[ ]:


pd.crosstab(df.salary,df.left).plot(kind='bar')


# In[ ]:


pd.crosstab(df.Department,df.left).plot(kind='bar')


# In[ ]:


subdf = df[['satisfaction_level','average_montly_hours','promotion_last_5years','salary']]
subdf.head()


# In[ ]:


salary_dummies = pd.get_dummies(subdf.salary, prefix="salary")


# In[ ]:


df_with_dummies = pd.concat([subdf,salary_dummies],axis='columns')


# In[ ]:


df_with_dummies.head()


# In[ ]:


df_with_dummies.drop('salary',axis='columns',inplace=True)
df_with_dummies.head()


# In[ ]:


X = df_with_dummies
X.head()


# In[ ]:


y = df.left


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=0.3)


# In[ ]:


from sklearn.linear_model import LogisticRegression
model = LogisticRegression()


# In[ ]:


model.fit(X_train, y_train)


# In[ ]:


model.predict(X_test)


# In[ ]:


model.score(X_test, y_test)


# In[ ]:




