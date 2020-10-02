#!/usr/bin/env python
# coding: utf-8

# ## Importing the libraries

# In[ ]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# ## Reading the datasets

# In[ ]:


train_df = pd.read_csv('../input/astro-analytics-techsoc-iitm/train_techsoc.csv')
test_df = pd.read_csv('../input/astro-analytics-techsoc-iitm/test_techsoc.csv')
sub_df = pd.read_csv('../input/astro-analytics-techsoc-iitm/sample_submission_techsoc.csv')


# ## EDA

# In[ ]:


train_df.head()


# In[ ]:


test_df.head()


# In[ ]:


sub_df.head()


# ### Visualizing the correlation between real and simulated values

# In[ ]:


fig, ax = plt.subplots(ncols=3,nrows=2)
fig.set_size_inches(14.7, 8.27)
sns.scatterplot(data=train_df,x='x_sim',y='x',ax=ax[0][0])
sns.scatterplot(data=train_df,x='y_sim',y='y',ax=ax[0][1])
sns.scatterplot(data=train_df,x='z_sim',y='z',ax=ax[0][2])
sns.scatterplot(data=train_df,x='Vx_sim',y='Vx',ax=ax[1][0])
sns.scatterplot(data=train_df,x='Vy_sim',y='Vy',ax=ax[1][1])
sns.scatterplot(data=train_df,x='Vz_sim',y='Vz',ax=ax[1][2])


# ### Visualizing the path traversed by a satellite

# In[ ]:


sat_df = train_df[train_df['sat_id']==0]
fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection='3d')
xs = sat_df.x
ys = sat_df.y
zs = sat_df.z
ax.plot3D(xs, ys, zs, 'gray')
ax.view_init(30,30)


# It is evident that the path is elliptical. This can be used in the model for better predictions (Not done in this notebook).

# ## Linear Model

# ### Check whether a linear relationship exists

# In[ ]:


X = train_df['x_sim']
y = train_df['x']
X2 = sm.add_constant(X)
est = sm.OLS(y,X2)
est2 = est.fit()
print(est2.summary())


# R-squared score suggests that there is a strong linear relationship between real and simulated satellite coordinates

# In[ ]:


X = train_df['Vx_sim']
y = train_df['Vx']
X2 = sm.add_constant(X)
est = sm.OLS(y,X2)
est2 = est.fit()
print(est2.summary())


# The linear relationship is not very strong. Still for the base model predictions it can be assumed to be linear

# ### Fitting the Linear Model

# In[ ]:


params1 = ['x','y','z','Vx','Vy','Vz']
params2 = ['x_sim','y_sim','z_sim','Vx_sim','Vy_sim','Vz_sim']


# In[ ]:


reg = LinearRegression()
for i in range(6):
    X = train_df.loc[:,params2[i]].values.reshape(-1,1)
    y = train_df.loc[:,params1[i]].values.reshape(-1,1)
    X_test = test_df.loc[:,params2[i]].values.reshape(-1,1)
    reg.fit(X,y)
    sub_df[params1[i]] = reg.predict(X_test)


# In[ ]:


sub_df.set_index('id',inplace=True)


# In[ ]:


sub_df.head()


# In[ ]:


sub_df.to_csv('basic_submission.csv')

