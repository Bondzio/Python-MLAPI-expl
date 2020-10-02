#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


data=pd.read_csv('../input/winequality-red.csv')


# In[ ]:


data.head


# In[ ]:


data.info()


# In[ ]:


data.describe()


# In[ ]:


data[data.isnull()=='True'].count()


# In[ ]:


features = ['fixed acidity','volatile acidity','citric acid','residual sugar','chlorides',
            'free sulfur dioxide','total sulfur dioxide','density','pH','sulphates','alcohol']
target = ['quality']


# # Linear Regression Analysis of Wine Quality vs Age

# In[ ]:


X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

model = linear_model.LinearRegression()
model = model.fit(y_train, X_train)
predicted_data = model.predict(y_test)
predicted_data = np.round_(predicted_data)

print (mean_squared_error(X_test,predicted_data))


print (predicted_data)


# # Polynomial Regression
# 
# 

# In[ ]:



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = PolynomialFeatures(degree= 4)
y_ = model.fit_transform(y)
y_test_ = model.fit_transform(y_test)


lg = LinearRegression()
lg.fit(y_,X)
predicted_data = lg.predict(y_test_)
predicted_data = np.round_(predicted_data)

print (mean_squared_error(X_test,predicted_data))

print (predicted_data)


# 
# 
# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




