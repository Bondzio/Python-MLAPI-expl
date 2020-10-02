#!/usr/bin/env python
# coding: utf-8

# ![](data:image/png;base64,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)

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
from matplotlib import pyplot as plt,cm
from warnings import filterwarnings as fw
fw('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


train = pd.read_csv('../input/train.csv')
train.head()


# ### So we have the task of predicting the revenue of the movies and the numerical features given are the cost in making of the movie and popularity of the movie. We will make a model based on these features.

# In[ ]:


train.corr()


# In[ ]:


sns.heatmap(train.corr(), cmap='YlGnBu', annot=True, linewidths = 0.2);


# In[ ]:


print('Descriptive Stats for the revenue are:\n ', train.revenue.describe())
sns.distplot(train.revenue);


# In[ ]:


sns.jointplot(train.budget, train.revenue);
sns.jointplot(train.popularity, train.revenue);
sns.jointplot(train.runtime, train.revenue);
plt.show()


# In[ ]:


# taking care of missing values
train['runtime'] = train['runtime'].fillna(method='ffill')


# In[ ]:


# Pairplot
cmap = cm.get_cmap('gnuplot')
scatter = pd.scatter_matrix(train[['runtime', 'budget', 'popularity']], c=train.revenue, cmap=cmap, figsize=(12,12), marker='o', s=40,
                           hist_kwds = {'bins' : 15})


# In[ ]:


from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(15,15))
ax = plt.subplot(111,projection = '3d')
ax.scatter(train['budget'],train['runtime'],train['popularity'], c = train['revenue'], marker = 'o', s = 100)
ax.set_xlabel('Budget of the Movie',fontsize=15)
ax.set_ylabel('Runtime of the Movie',fontsize=15)
ax.set_zlabel('Popularity of the Movie',fontsize=15)
plt.show()


# In[ ]:


train.status = pd.get_dummies(train.status)
train.status.head()


# ## Model Building

# In[ ]:


X = train[['runtime', 'budget','popularity','status']]
y = train.revenue
#splitting the data into training and validation to check validity of the model

from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.1, random_state=1)


# In[ ]:


#Linear Model
from sklearn.linear_model import LinearRegression, Ridge, Lasso
def rmsle(y,y0): return np.sqrt(np.mean(np.square(np.log1p(y)-np.log1p(y0)))) 
reg = LinearRegression()
lin_model = reg.fit(X_train, y_train)
y_pred = reg.predict(X_val)
print('RMSLE score for linear model is {}'.format(rmsle(y_val, y_pred)))

#Applyting the model on test data and submission
test = pd.read_csv('../input/test.csv')
test['runtime'] = test.runtime.fillna(method='ffill')
test.status = pd.get_dummies(test.status)
X_test = test[['runtime','popularity','budget','status']]
pred1 = reg.predict(X_test)

#Submission
sub1 = pd.read_csv('../input/sample_submission.csv')
sub1['revenue'] = pred1
sub1.to_csv('lin_model_sub.csv',index=False)


# In[ ]:


from sklearn.neighbors import KNeighborsRegressor
knn = KNeighborsRegressor(n_neighbors = 5)
knn_model = knn.fit(X_train, y_train)
knn_y_pred = knn.predict(X_val)
print('RMSLE score for k-NN model is {}'.format(rmsle(y_val, knn_y_pred)))
pred2 = knn.predict(X_test)

#Submission
sub2 = pd.read_csv('../input/sample_submission.csv')
sub2['revenue'] = pred2
sub2.to_csv('knn_model_sub.csv',index=False)


# In[ ]:


from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
rf_model = rf.fit(X_train, y_train)
rf_y_pred = rf.predict(X_val)
print('RMSLE score for Random Forest model is {}'.format(rmsle(y_val, rf_y_pred)))
pred3 = rf.predict(X_test)

#Submission
sub3 = pd.read_csv('../input/sample_submission.csv')
sub3['revenue'] = pred3
sub3.to_csv('rf_model_sub.csv',index=False)


# In[ ]:




