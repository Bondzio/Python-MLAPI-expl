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


from sklearn.linear_model import LinearRegression


# In[ ]:


get_ipython().system('pwd')


# In[ ]:


test = pd.read_csv('/kaggle/input/finec-1941-hw1/techparams_test.csv')
train = pd.read_csv('/kaggle/input/finec-1941-hw1/techparams_train.csv')


# In[ ]:


y_train = train['target']
y_train_idx = train['index']
x_train = train.drop(['target', 'index'], axis=1)
x_test = test.drop(['index'], axis=1)


# In[ ]:


model = LinearRegression()
model.fit(x_train, y_train)


# In[ ]:


test_pred =  model.predict(x_test)


# In[ ]:


submit = test[['index']]
submit['target']=test_pred


# In[ ]:


submit.head()


# In[ ]:


submit.to_csv('submit.csv', index=False)


# In[ ]:




