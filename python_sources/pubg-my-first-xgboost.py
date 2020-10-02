#!/usr/bin/env python
# coding: utf-8

# **Introduction**
# 
# Hi, I will trying to implement a XGBoost model in this kernel. This is my very first time implementing this. 
# The data is from the PUBG competition.
# 
# The purpose of this kernel is sharing my learning and also a little demonstration by a beginner for beginner.

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


#read the data
data = pd.read_csv('../input/train_V2.csv')


# In[ ]:


data.shape


# In[ ]:


from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# For this first trial, I will only be using 10% of the data provided.

# In[ ]:


data_sample = data.sample(frac=0.1)
data_sample.head()


# I have decided to group a few of the matchType into others.
# 'normal-squad-fpp', 'crashfpp', 'crashtpp', 'normal-duo-fpp', 'flarefpp', 'normal-solo-fpp', 'flaretpp', 'normal-duo', 'normal-squad', 'normal-solo' are converted into others.

# In[ ]:


data_sample.matchType.unique()


# In[ ]:


def merge_matchType(x):
    if x in {'normal-squad-fpp', 'crashfpp', 'crashtpp', 'normal-duo-fpp',
       'flarefpp', 'normal-solo-fpp', 'flaretpp', 'normal-duo',
       'normal-squad', 'normal-solo'}:
        return 'others'
    else:
        return x


# In[ ]:


data_sample['matchType'] = data_sample.matchType.apply(merge_matchType)

data_sample.matchType.unique()


# In order to use the XGBoost algorithm, the categorical variables need to be converted into numerical. I have thus generated dummy variables for the matchType variable. matchType_others was dropped from the dataframe.

# In[ ]:


data_sample_dumm = pd.get_dummies(data_sample, columns=['matchType'])
data_sample_dumm.head()


# In[ ]:


data_sample_dumm = data_sample_dumm.drop('matchType_others', axis=1)


# In[ ]:


data_sample_dumm.columns


# In[ ]:


data_sample = data_sample_dumm.loc[:,['Id', 'groupId', 'matchId', 'assists', 'boosts', 'damageDealt', 'DBNOs',
       'headshotKills', 'heals', 'killPlace', 'killPoints', 'kills',
       'killStreaks', 'longestKill', 'matchDuration', 'maxPlace', 'numGroups',
       'rankPoints', 'revives', 'rideDistance', 'roadKills', 'swimDistance',
       'teamKills', 'vehicleDestroys', 'walkDistance', 'weaponsAcquired',
       'winPoints', 'matchType_duo', 'matchType_duo-fpp',
       'matchType_solo', 'matchType_solo-fpp', 'matchType_squad',
       'matchType_squad-fpp', 'winPlacePerc']]


# In[ ]:


print(data_sample.shape)
data_sample.head()


# In[ ]:


# split data into X and y
X = data_sample.iloc[:,3:33]
Y = data_sample.iloc[:,33]
X.head()


# The data was split into 67% train, 33% test set.

# In[ ]:


# split data into train and test sets
seed = 7
test_size = 0.33
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)


# For this demonstration, I am going with the XGBRegressor as the output is numeric. The evaluation metric is Mean Absolute Error.

# In[ ]:


model = XGBRegressor()
model.fit(X_train, y_train, eval_metric='mae')


# In[ ]:


# make predictions for test data
y_pred = model.predict(X_test)


# In[ ]:


y_pred


# In[ ]:


# evaluate predictions
from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y_test, y_pred)
print("MAE: {}".format(mae))


# I have also plot the feature importance. killPlace is the most important feature, followed by walkDistance and kills

# In[ ]:


from xgboost import plot_importance

plot_importance(model)


# Below is an example tree from the XGBoost model.

# In[ ]:


from xgboost import to_graphviz

to_graphviz(model, num_trees=1)


# I have also plot the histogram of my prediction and the actual winPlacePerc. Both of them looks pretty different.

# In[ ]:


pd.Series(y_pred).plot(kind='hist',bins=10)


# In[ ]:


pd.Series(y_test).plot(kind='hist', bins=10)


# **Conclusion**
# 
# Hope you have learnt something from this implementation of the XGBoost model. The Mean Absolute Error from my model is pretty high as compared to the other submissions in the competition.
