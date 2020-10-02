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


import matplotlib.pylab as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.linear_model import LinearRegression
from sklearn import datasets


# In[ ]:


diabetes = datasets.load_diabetes()


# In[ ]:


diabetes.data.shape #feature matrix shape


# In[ ]:


diabetes.target.shape #target shape


# In[ ]:


diabetes.feature_names #column_names


# In[ ]:


#split train, test data

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(diabetes.data, diabetes.target, test_size=0.2,random_state=0)


# In[ ]:


#1)set up model

model = LinearRegression()

#2)use fit

model.fit(X_train,y_train)

#3) check the score

model.score(X_test,y_test)


# In[ ]:


#getting coeffiients-> m

model.coef_


# In[ ]:


#getting intercept -> c

model.intercept_


# In[ ]:


#predict the unknown data

model.predict(X_test)


# In[ ]:


#plot prediction and actual data

y_pred = model.predict(X_test)
plt.plot(y_test,y_pred,'.')
# plot a line, a perfit predict would all fall on this line
x = np.linspace(0, 330, 100)
y = x
plt.plot(x, y)
plt.show()


# In[ ]:




