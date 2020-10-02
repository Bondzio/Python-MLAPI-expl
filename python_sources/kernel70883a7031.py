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


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import pickle as pkl
from sklearn.preprocessing import StandardScaler, MinMaxScaler


# In[ ]:


df = pd.read_csv("/kaggle/input/iris/Iris.csv")
df.drop(columns=['Id'],inplace=True)


# In[ ]:


df.columns = ['sepal_length','sepal_width','petal_length','petal_width','target']
df.head()


# In[ ]:


df['target'].value_counts()


# In[ ]:


df['target'] = df['target'].apply(lambda x : 1 if x=='Iris-virginica' else 2 if x=='Iris-versicolor' else 3)
corr = df.corr()
corr


# In[ ]:


df.drop(columns=['petal_width'],inplace=True)


# In[ ]:


y = df.target
X = df.drop(columns=['target'])


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.30,random_state=0)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier()


# In[ ]:


rfc.fit(X_train,y_train)


# In[ ]:


y_pred = rfc.predict(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix
confusion_matrix(y_test,y_pred)


# In[ ]:


rfc.score(X_test,y_test)

