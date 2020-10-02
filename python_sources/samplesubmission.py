#!/usr/bin/env python
# coding: utf-8

# # NYC taxi fare
# 
# This is a sample notebook with steps to solve the NYC taxi fare.
# 
# 1. Data <br>
#     1.1 Load Data <br>
#     1.2 Data preparation (EDA, feature engineering)  <br>
# 2. Model <br>
#     2.1 First model <br>
#     2.2 Regularization <br>
#     2.3 Boost <br>
# 3. Evaluate <br>
#     3.1 Error <br>
# 4. Submission <br>
#     4.1 Load test dataset <br>
#     4.2 Predictions<br>
#     4.3 Generate submission file

# In[ ]:


import numpy as np 
import pandas as pd

# Visualizations
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import seaborn as sns
palette = sns.color_palette('Paired', 10)

# Set random seed 
RSEED = 100


# ## 1. Data
# ### 1.1 Load Data

# In[ ]:


train = pd.read_csv('../input/train_MV.csv')
train.head()


# In[ ]:


train.shape


# ### 1.2 Data Preparation
# 
# EDA
# I will follow some of the performed steps from: https://www.kaggle.com/willkoehrsen/a-walkthrough-and-a-challenge/notebook

# Let's drop the key column, since it is an id and will not aggregate any information.
# Also, lets make pickup_datetime a datetime column.

# In[ ]:


train.drop('key', axis=1, inplace=True)
train['pickup_datetime'] = pd.to_datetime(train['pickup_datetime'])
train.dtypes


# In[ ]:


# Remove na
train = train.dropna()
train.shape


# In[ ]:


train.describe()


# By the min and max values we can see that there are some clear outliers.
# First, let's understand the fare distribution.

# In[ ]:


sns.distplot(train['fare_amount']);
plt.title('Distribution of Fare');


# In[ ]:


print(f"There are {len(train[train['fare_amount'] < 0])} negative fares.")
print(f"There are {len(train[train['fare_amount'] == 0])} $0 fares.")
print(f"There are {len(train[train['fare_amount'] > 100])} fares greater than $100.")


# In[ ]:


#remove outliers
#keep only fares between 2.5 and 100
train = train[train['fare_amount'].between(left = 2.5, right = 100)]


# In[ ]:


#number of passengers
train['passenger_count'].value_counts().plot.bar(color = 'b', edgecolor = 'k');
plt.title('Passenger Counts'); plt.xlabel('Number of Passengers'); plt.ylabel('Count');
#should we remove the outliers based on number of passengers?


# In[ ]:


# Remove latitude and longtiude outliers
train = train.loc[train['pickup_latitude'].between(40, 42)]
train = train.loc[train['pickup_longitude'].between(-75, -72)]
train = train.loc[train['dropoff_latitude'].between(40, 42)]
train = train.loc[train['dropoff_longitude'].between(-75, -72)]

print(f'New number of observations: {train.shape[0]}')


# Should we explore the location?
# What is the difference if the pickup location is in Manhatan?
# Is there a direction where the fares will be more expensive than others?
# How about the pickup time?

# In[ ]:


train = train.loc[train['passenger_count'].between(0, 6)]


# ### Feature Engineering
# 
# The distance between pickup and dropoff is probably one important feature.
# Let's start by calculating the latitude and longitude differences.

# In[ ]:


# Absolute difference in latitude and longitude
train['abs_lat_diff'] = (train['dropoff_latitude'] - train['pickup_latitude']).abs()
train['abs_lon_diff'] = (train['dropoff_longitude'] - train['pickup_longitude']).abs()


sns.lmplot('abs_lat_diff', 'abs_lon_diff', fit_reg = False,
           data = train.sample(10000, random_state=RSEED));
plt.title('Absolute latitude difference vs Absolute longitude difference');


# In[ ]:


no_diff = train[(train['abs_lat_diff'] == 0) & (train['abs_lon_diff'] == 0)]
no_diff.shape


# A lot of rides have same latitude and longitude. That is odd...
# We will also obtain the euclidean and manhatan distances

# In[ ]:


def minkowski_distance(x1, x2, y1, y2, p):
    return ((abs(x2 - x1) ** p) + (abs(y2 - y1)) ** p) ** (1 / p)


# In[ ]:


train['manhattan'] = minkowski_distance(train['pickup_longitude'], train['dropoff_longitude'],
                                       train['pickup_latitude'], train['dropoff_latitude'], 1)

train['euclidean'] = minkowski_distance(train['pickup_longitude'], train['dropoff_longitude'],
                                       train['pickup_latitude'], train['dropoff_latitude'], 2)


# ## 2. Model
# 
# 

# In[ ]:


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

lr = LinearRegression()


# In[ ]:


# Split data
X_train, X_valid, y_train, y_valid = train_test_split(train, np.array(train['fare_amount']),
                                                      random_state = RSEED, test_size = 300_000)


# In[ ]:


lr.fit(X_train[['abs_lat_diff', 'abs_lon_diff', 'passenger_count']], y_train)

print('Intercept', round(lr.intercept_, 4))
print('abs_lat_diff coef: ', round(lr.coef_[0], 4), 
      '\tabs_lon_diff coef:', round(lr.coef_[1], 4),
      '\tpassenger_count coef:', round(lr.coef_[2], 4))


# ## 3. Evaluation

# In[ ]:


from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore', category = RuntimeWarning)


# In[ ]:


def metrics(train_pred, valid_pred, y_train, y_valid):
    """Calculate metrics:
       Root mean squared error and mean absolute percentage error"""
    
    # Root mean squared error
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    valid_rmse = np.sqrt(mean_squared_error(y_valid, valid_pred))
    
    # Calculate absolute percentage error
    train_ape = abs((y_train - train_pred) / y_train)
    valid_ape = abs((y_valid - valid_pred) / y_valid)
    
    # Account for y values of 0
    train_ape[train_ape == np.inf] = 0
    train_ape[train_ape == -np.inf] = 0
    valid_ape[valid_ape == np.inf] = 0
    valid_ape[valid_ape == -np.inf] = 0
    
    train_mape = 100 * np.mean(train_ape)
    valid_mape = 100 * np.mean(valid_ape)
    
    return train_rmse, valid_rmse, train_mape, valid_mape


# In[ ]:


def evaluate(model, features, X_train, X_valid, y_train, y_valid):
    """Mean absolute percentage error"""
    
    # Make predictions
    train_pred = model.predict(X_train[features])
    valid_pred = model.predict(X_valid[features])
    
    # Get metrics
    train_rmse, valid_rmse, train_mape, valid_mape = metrics(train_pred, valid_pred,
                                                             y_train, y_valid)
    
    print(f'Training:   rmse = {round(train_rmse, 2)} \t mape = {round(train_mape, 2)}')
    print(f'Validation: rmse = {round(valid_rmse, 2)} \t mape = {round(valid_mape, 2)}')


# In[ ]:


evaluate(lr, ['abs_lat_diff', 'abs_lon_diff', 'passenger_count'], 
        X_train, X_valid, y_train, y_valid)


# ## 4. Submission

# In[ ]:


test = pd.read_csv('../input/test_MV.csv')


# In[ ]:


#calculate the features for the test set
# Absolute difference in latitude and longitude
test['abs_lat_diff'] = (test['dropoff_latitude'] - test['pickup_latitude']).abs()
test['abs_lon_diff'] = (test['dropoff_longitude'] - test['pickup_longitude']).abs()

test['manhattan'] = minkowski_distance(test['pickup_longitude'], test['dropoff_longitude'],
                                       test['pickup_latitude'], test['dropoff_latitude'], 1)

test['euclidean'] = minkowski_distance(test['pickup_longitude'], test['dropoff_longitude'],
                                       test['pickup_latitude'], test['dropoff_latitude'], 2)


# In[ ]:


preds = lr.predict(test[['abs_lat_diff', 'abs_lon_diff', 'passenger_count']])


# In[ ]:


sub = pd.DataFrame({'key': test.key, 'fare_amount': preds})
sub.to_csv('sub_lr_simple.csv', index = False)


# This sample solution got a public score of: 4.68897

# In[ ]:




