#!/usr/bin/env python
# coding: utf-8

# ## Some credit here due to https://www.kaggle.com/apapiu/regularized-linear-models/notebook
# 
# ## **Import and quick view of the data**

# In[ ]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import os
from copy import deepcopy

print(os.listdir("../input"))

from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error


# In[ ]:


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')

# test doesn't have 'SalePrice'
# Note that the 'Id' for train range 1-1460 and test range 1461-2919
print('Train Shape: {}, Train ID Range {} to {}'.format(train.shape,train.Id.min(), train.Id.max()))
print('Test Shape: {}, Test ID Range {} to {}'.format(test.shape,test.Id.min(), test.Id.max()))


# In[ ]:


train.head(3)


# ## **Combining train and test for all preprocessing to be done on one dataframe**

# In[ ]:


all_data = train.append(test,sort = False)
print(all_data.shape)
all_data.head(3)


# ### **Data type counts**

# In[ ]:


all_data.dtypes.groupby(all_data.dtypes).count()


# ### **Checking out numeric data types**

# In[ ]:


numerics = all_data.dtypes[all_data.dtypes != object].index.tolist()
print(numerics)
print(len(numerics))


# ## Looking for skewed data to log transform
# ### Will log-transform those with skew > .75

# In[ ]:


skew_calcs = all_data[numerics].skew().sort_values()
# Note that the skew filter below removes Id from the skewed feature list - we wouldn't have wanted to log-transform Id
skew_calcs = skew_calcs[skew_calcs > .75]
print(skew_calcs)
skew_feats = skew_calcs.index
# Also note that SalePrice will be log_transformed


# ### **Quick Visual of Distribution of skewed features before and after log transformation**

# In[ ]:


all_data[skew_feats].hist()
np.log1p(all_data[skew_feats]).hist()
plt.show()
#plt.tight_layout()


# ## **Log Transforming Skewed features**

# In[ ]:


all_data[skew_feats] = np.log1p(all_data[skew_feats])


# ### Checking object data types

# In[ ]:


#creating list of objects and View the unique strings in columns with object datatype
objects = train.dtypes[train.dtypes == object].index.tolist()
print(objects)
train[objects].apply(lambda x: set(x))


# ### It looks like we can create dummy variables for all of the objects, since there aren't too many to handle...

# In[ ]:


# Create Dummy Variables
all_data = pd.concat([all_data,pd.get_dummies(all_data[objects])],axis = 1)
print(all_data.shape)


# In[ ]:


# Remove original features now that dummies have been created
all_data = all_data.drop(objects,axis = 1)
print(all_data.shape)


# In[ ]:


all_data = all_data.fillna(all_data.mean())
# could also create dummy variable for nulls
all_data.head(3)


# ### **Create Train and Test**

# In[ ]:


train_data = all_data[:1460]
# drop SalePrice from test_data, was created during .fillna(all_data.mean())
test_data = all_data[1460:].drop('SalePrice',axis = 1)


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X = train_data.drop(['SalePrice'],axis = 1)
print(X.shape)
y = train_data['SalePrice']
print(y.shape)


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)


# In[ ]:


def get_mse(model,alpha):
    run_model = model(alpha = alpha)
    run_model.fit(X_train,y_train)
    return mean_squared_error(y_pred=run_model.predict(X_test),y_true=y_test)


# In[ ]:


alphas = [.01,.05,0.1,0.5,1,2,3,5,10,20,40]
ridge_mses = [get_mse(Ridge,x) for x in alphas]
plt.plot(alphas,ridge_mses)


# In[ ]:


lasso_mses = [get_mse(Lasso,x) for x in alphas]
plt.plot(alphas,lasso_mses)


# In[ ]:


# alpha = 5 looks best
pd.DataFrame({'alpha':alphas, 'MSE':ridge_mses}).sort_values('MSE',ascending = True)


# In[ ]:


ridge_model = Ridge(alpha = 5)
ridge_model.fit(X,y)
coefs = ridge_model.coef_


# In[ ]:


labels_and_weights = pd.DataFrame({'field':X.columns,'weight':coefs})


# In[ ]:


top_weight = labels_and_weights['weight'].quantile(.97)
bot_weight = labels_and_weights['weight'].quantile(.03)
heavy_weights = labels_and_weights[(labels_and_weights['weight']>top_weight) | (labels_and_weights['weight']<bot_weight)].sort_values('weight')
plt.barh(heavy_weights['field'],heavy_weights['weight'])


# In[ ]:


predictions = ridge_model.predict(test_data)


# In[ ]:


print(predictions.mean())
# inverse log-transform
preds = np.expm1(predictions)
print(preds.mean())


# In[ ]:


sub = pd.DataFrame()
sub['Id'] = test_data['Id']
sub['SalePrice'] = preds


# In[ ]:


sub.head()


# In[ ]:


sub.to_csv('submission.csv',index=False)

