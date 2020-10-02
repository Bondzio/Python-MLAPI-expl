#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
np.random.seed(7)

import matplotlib.pyplot as plt

from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense, Activation
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error
from sklearn.ensemble import RandomForestRegressor


# In[ ]:


df_train = pd.read_csv( '../input/train_V2.csv')
df_train = df_train[df_train['maxPlace'] > 1]

df_test = pd.read_csv( '../input/test_V2.csv')


# In[ ]:


# remove Id related and categorical columns
target = 'winPlacePerc'
features = list(df_train.columns)
features.remove("Id")
features.remove("matchId")
features.remove("groupId")
features.remove("matchType")

y_train = np.array(df_train[target])
features.remove(target)
x_train = df_train[features]
x_test = df_test[features]


# In[ ]:


# split the train and the validation set for the fitting
random_seed=1
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size = 0.1, random_state=random_seed)


# In[ ]:


m3 = RandomForestRegressor(n_estimators=66, min_samples_leaf=3, max_features=0.5, n_jobs=-1)


# In[ ]:


get_ipython().run_cell_magic('time', '', 'm3.fit(x_train, y_train)')


# In[ ]:


print('mae train: ', mean_absolute_error(m3.predict(x_train), y_train))
print('mae val: ', mean_absolute_error(m3.predict(x_val), y_val))


# In[ ]:


get_ipython().run_cell_magic('time', '', "pred = m3.predict(x_test)\ndf_test['winPlacePerc'] = pred\nsubmission = df_test[['Id', 'winPlacePerc']]\nsubmission.to_csv('submission.csv', index=False)")


# In[ ]:


plt.hist(pred)
plt.hist(y_train)

