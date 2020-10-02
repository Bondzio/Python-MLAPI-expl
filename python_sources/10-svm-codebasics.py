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


import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_digits


# In[ ]:


digits = load_digits()
dir(digits)


# In[ ]:


df = pd.DataFrame(digits.data, digits.target)
df


# In[ ]:


df['target'] = digits.target


# In[ ]:


df


# In[ ]:


y = df.target


# In[ ]:


from sklearn.model_selection import train_test_split
X = df.drop(['target'], axis = 'columns')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.8)


# In[ ]:


from sklearn.svm import SVC
model = SVC()
model.fit(X_train, y_train)
model.score(X_test, y_test)


# In[ ]:


rbf_model = SVC(kernel = 'rbf')
rbf_model.fit(X_train, y_train)
rbf_model.score(X_test, y_test)


# In[ ]:


linear_model = SVC(kernel = 'linear')
linear_model.fit(X_train, y_train)
linear_model.score(X_test, y_test)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




