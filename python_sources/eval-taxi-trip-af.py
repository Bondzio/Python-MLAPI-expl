#!/usr/bin/env python
# coding: utf-8

# Import Librairies

# In[50]:


import pandas as pd
import seaborn as sns
import pathlib as Path
import matplotlib.pyplot as plt
import sklearn

import numpy as np
from sklearn.model_selection import ShuffleSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score


import os
print(os.listdir("../input"))


# ## Exploration DataTrain

# In[51]:


df_train = pd.read_csv('../input/train.csv')
df_train.head()


# In[52]:


df_train = df_train[df_train['passenger_count'] >= 1] 
df_train = df_train[df_train['trip_duration'] <= 5000]


# In[53]:


plt.figure(figsize=(20, 5))
sns.set(style="darkgrid")
sns.countplot(x="trip_duration", data=df_train);


# In[54]:


df_train['pickup_datetime'] = pd.to_datetime(df_train['pickup_datetime'])
df_train['year'] = df_train['pickup_datetime'].dt.year
df_train['month'] = df_train['pickup_datetime'].dt.month
df_train['day'] = df_train['pickup_datetime'].dt.day
df_train['hour'] = df_train['pickup_datetime'].dt.hour
df_train['minute'] = df_train['pickup_datetime'].dt.minute
df_train['second'] = df_train['pickup_datetime'].dt.second


# In[55]:


df_train.describe()


# ## Usefull Columns

# In[56]:


selected_columns = ['passenger_count', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude',
                  'dropoff_latitude','year','month','day','hour','minute',
                  'second']


# In[57]:


X_train = df_train[selected_columns]
y_train = df_train['trip_duration']


# In[58]:


rf = RandomForestRegressor()
random_split = ShuffleSplit(n_splits=3, test_size=0.05, train_size=0.1, random_state=0)
looses = -cross_val_score(rf, X_train, y_train, cv=random_split, scoring='neg_mean_squared_log_error')
looses = [np.sqrt(l) for l in looses]
np.mean(looses)


# In[59]:


rf.fit(X_train, y_train)


# In[60]:


df_test = pd.read_csv('../input/test.csv')
df_test['pickup_datetime'] = pd.to_datetime(df_test['pickup_datetime'])
df_test.head()


# In[61]:


df_test['pickup_datetime'] = pd.to_datetime(df_test['pickup_datetime'])
df_test['year'] = df_test['pickup_datetime'].dt.year
df_test['month'] = df_test['pickup_datetime'].dt.month
df_test['day'] = df_test['pickup_datetime'].dt.day
df_test['hour'] = df_test['pickup_datetime'].dt.hour
df_test['minute'] = df_test['pickup_datetime'].dt.minute
df_test['second'] = df_test['pickup_datetime'].dt.second


# In[62]:


X_test = df_test[selected_columns]


# In[63]:


y_pred = rf.predict(X_test)
y_pred.mean()


# In[64]:


submission = pd.read_csv('../input/sample_submission.csv')
submission['trip_duration'] = y_pred
submission.to_csv('submission.csv', index=False)


# In[ ]:




