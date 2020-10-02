#!/usr/bin/env python
# coding: utf-8

# <font size = 12><u> This is an Introduction Kernel for this Dataset</u> </font>
# 
# **If you find this kernel useful, please upvote the kernel. It will be much appriciated.**

# In[ ]:


#import Common libraries

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 12, 8


# In[ ]:


#importing our datasets

train = pd.read_csv('../input/food-demand-forecasting/train.csv')
test_data = pd.read_csv('../input/food-demand-forecasting/test.csv')
centers = pd.read_csv('../input/food-demand-forecasting/fulfilment_center_info.csv')
meal = pd.read_csv('../input/food-demand-forecasting/meal_info.csv')
sample_submission = ('../input/food-demand-forecasting/sample_submission.csv')


# In[ ]:


#train file

train.head(5)


# In[ ]:


#informations on train dataset

train.info()


# In[ ]:


#Centers data file

centers.head(5)


# In[ ]:


#meal informations

meal.info()


# <u> Heat Map on Correlation </u>
# 
# Correlation or dependence is any statistical relationship, whether causal or not, between two random variables or bivariate data In the broadest sense correlation is any statistical association, though it commonly refers to the degree to which a pair of variables are linearly related

# In[ ]:


plt.figure(figsize=(20,10))
c=train.corr()
sns.heatmap(c,cmap="BrBG",annot=True)


# In[ ]:


#Training and Testing Data

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_log_error

# Create target object and call it y
y = train.num_orders


# In[ ]:


# Create target object and call it y
y = train.num_orders

# Create X
features = ['id','week','center_id','meal_id','checkout_price','base_price','emailer_for_promotion','homepage_featured']
X = train[features]


# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)


# In[ ]:


# Specify Model
client_model = DecisionTreeRegressor(random_state=1)
# Fit Model
client_model.fit(train_X, train_y)


# In[ ]:


#Do training on the full data set
rf_model_on_full_data = RandomForestRegressor(random_state=1)

# fit rf_model_on_full_data on all data from the 
rf_model_on_full_data.fit(train_X, train_y)


# In[ ]:


features = ['id','week','center_id','meal_id','checkout_price','base_price','emailer_for_promotion','homepage_featured']

test_X = test_data[features]

# make predictions which we will submit. 

test_preds = rf_model_on_full_data.predict(test_X)
print(mean_squared_log_error(test_data.id, test_preds))


# In[ ]:


#Exporting the submission file

output = pd.DataFrame({'id': test_data.id,
                       'num_orders': test_preds})

output.to_csv('submission.csv', index=False)

