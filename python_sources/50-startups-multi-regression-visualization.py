#!/usr/bin/env python
# coding: utf-8

# ## Like & Follow Us:
# Is this helpful?
# <br/>
# Like us on facebook: https://www.facebook.com/codemakerz

# ## Imports

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

import os
print(os.listdir("../input"))


# ## Load & View Dataset

# In[ ]:


# load dataset
df = pd.read_csv("../input/50_Startups.csv")


# In[ ]:


df.head()


# ## Check for Null/Missing Values

# In[ ]:


df.isnull().sum() # So no null values


# ## Change Categorical Feature into Dummy Variables

# In[ ]:


# handlign Dummy Variables
dummy = pd.get_dummies(df["State"])


# In[ ]:


df = pd.concat([dummy, df], axis=1)


# In[ ]:


df.head()


# In[ ]:


# After adding dummy variable remove Gender Column
df.drop(["State"], inplace=True, axis=1)


# In[ ]:


df.head()


# ## Split Dataset into Dependent & Independent Features

# In[ ]:


# lets split our data into dependent and independent dataset
X = df.iloc[:, 0:6].values


# In[ ]:


X


# In[ ]:


y = df.iloc[:, -1:].values


# ## Splitting Dataset into Training & Test Set

# In[ ]:


# split into train and test
from sklearn.model_selection import train_test_split


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=0)


# ## Correlation Table

# In[ ]:


# Lets check the correlation between variables
df.corr()
# from below table we can see R&D Spend and Marketing Spend both have good affect in Profit.


# ## Visualization

# In[ ]:


# Lets plot all the three features together
f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(15, 10))

ax1.scatter(df["R&D Spend"], df.Profit)
ax1.set_title('R&D Spend Vs Profit')

ax2.scatter(df["Administration"], df.Profit)
ax2.set_title('Administration Spend Vs Profit')

ax3.scatter(df["Marketing Spend"], df.Profit)
ax3.set_title('Marketing Spend Vs Profit')

plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
plt.show()


# ## Regression Object

# In[ ]:


# So we can both R&D & Marketing fetures are related to Profit linearly. So we can generate a multi regression
# model using these two
from sklearn.linear_model import LinearRegression


# In[ ]:


regressor = LinearRegression() # Regression object created


# ## Training Model

# In[ ]:


regressor.fit(X_train, y_train) # Training model


# ## Predict Data

# In[ ]:


y_pred = regressor.predict(X_test) # predicting 


# ## Printing Real & Predicted Values

# In[ ]:


print("="*40)
print("Real Values -------> Predicted Values")
print("="*40)
print("\n")
for item in range(len(y_test)):
    print(str(y_test[item]) + " -------> " +str(y_pred[item]))


# In[ ]:


x_test_new = [[0.0000000e+00, 0.0000000e+00, 1.0000000e+00, 200000,
        300000, 150000]]


# In[ ]:


regressor.predict(x_test_new)


# In[ ]:




