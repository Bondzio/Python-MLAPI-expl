#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from time import time
import gc
gc.enable()

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


train_data = pd.read_csv('../input/train_V2.csv')
test_data = pd.read_csv('../input/test_V2.csv')


# In[ ]:


train_data.drop(['Id', 'groupId', 'matchId'], axis=1, inplace=True)
train_data.head()


# In[ ]:


train_data.columns


# The **kills** feature seems pretty important, practically, for prediction **winPlacePerc** 

# In[ ]:


train_data[train_data['kills'] > 0].plot.scatter(x='winPlacePerc', y='kills', figsize=(12, 6))


# As you can see in the above figure, there is a very moderate increase in the slope, which suggests that **kills** has an alright amount of correlation with **winPlacePerc** but also cannot have a high variance.
# 
# Let's have a look at the **Heatmap** for more correlation analysis.

# In[ ]:


l = ['winPlacePerc', 'boosts', 'damageDealt', 'heals', 'kills', 'rideDistance', 'roadKills', 'walkDistance', 'weaponsAcquired']
figure, ax = plt.subplots(figsize=(12,8))
f = train_data.loc[:, l].corr()
g = sns.heatmap(f, annot=True, ax=ax)
g.set_yticklabels(labels=l[::-1], rotation=0)
g.set_xticklabels(labels=l[:], rotation=90)


# Seemingly, **walkDistance**, **boosts** and **weaponsAcquired** have the most correlation with **winPlacePerc**. 

# In[ ]:


fig, axarr = plt.subplots(2, 2, figsize=(12, 8))
train_data[train_data['walkDistance'] > 0].plot.scatter(x='winPlacePerc', y='walkDistance', ax=axarr[0][0])
train_data[train_data['boosts'] > 0].plot.scatter(x='winPlacePerc', y='boosts', ax=axarr[0][1])
train_data[train_data['weaponsAcquired'] > 0].plot.scatter(x='winPlacePerc', y='weaponsAcquired', ax=axarr[1][0])
train_data[train_data['damageDealt'] > 0].plot.scatter(x='winPlacePerc', y='damageDealt', ax=axarr[1][1])
plt.subplots_adjust(hspace=.3)
sns.despine()


# # Data preprocessing
# 
# Removing unnecessary features and filling in missing values

# In[ ]:


train_data.columns


# Kaggler ['averagemn'](https://www.kaggle.com/donkeys) pointed out that there is one NaN value in **winPlacePerc**.

# In[ ]:


train_data[train_data['winPlacePerc'].isnull()]


# In[ ]:


train_data.drop(2744604, inplace=True)


# **swimDistance** doesn't make much sense, to me, for predicting **winPlacePerc** as swimming distance would generally be much much less than ride distance or walking distance.
# 
# But as seen from the figure below, it is pretty useful or maybe that's where everyone's hiding!

# In[ ]:


figure1, axarr1 = plt.subplots(1, 3, figsize=(14, 6))
train_data['swimDistance'].value_counts().sort_index()[1:20].plot.hist(ax=axarr1[0])
train_data['rideDistance'].value_counts().sort_index()[1:20].plot.hist(ax=axarr1[1])
train_data['walkDistance'].value_counts().sort_index()[1:20].plot.hist(ax=axarr1[2])
axarr1[0].set_title('Swim dist')
axarr1[1].set_title('Ride dist')
axarr1[2].set_title('Walk dist')
plt.subplots_adjust(hspace=.3)
sns.despine()


# In[ ]:


train_data['totalDistance'] = train_data['swimDistance'] + train_data['rideDistance'] + train_data['walkDistance']
train_data.drop(['swimDistance', 'rideDistance', 'walkDistance'], axis=1, inplace=True)


# In[ ]:


train_data['matchType'].value_counts().index


# In[ ]:


# Creating cat codes of match type

train_data['matchType'] = train_data['matchType'].astype('category')
train_data['matchType'] = train_data['matchType'].cat.codes


# In[ ]:


# Combining boosts and heals as health

train_data['health'] = train_data['boosts'] + train_data['heals']
train_data.drop(['boosts', 'heals'], axis=1, inplace=True)


# In[ ]:


train_data.head()


# As seen below, most of the kill types are not that varied on their own. So we'll just add those to **kills**

# In[ ]:


figure2, axarr2 = plt.subplots(1, 3, figsize=(14, 6))
train_data['headshotKills'].value_counts().sort_index().head(10)[1:].plot.bar(ax=axarr2[0])
train_data['roadKills'].value_counts().sort_index().head(10)[1:].plot.bar(ax=axarr2[1])
train_data['teamKills'].value_counts().sort_index().head(10)[1:].plot.bar(ax=axarr2[2])
axarr2[0].set_title('Headshot kills')
axarr2[1].set_title('Road kills')
axarr2[2].set_title('Team kills')
plt.subplots_adjust(hspace=.3)
sns.despine()


# In[ ]:


train_data['kills'] += train_data['headshotKills'] + train_data['roadKills'] + train_data['teamKills']
train_data.drop(['headshotKills', 'roadKills', 'teamKills'], axis=1, inplace=True)


# In[ ]:


train_data.head()


# # Preprocessing train data

# In[ ]:


test_data.drop(['Id', 'groupId', 'matchId'], axis=1, inplace=True)


# In[ ]:


test_data['totalDistance'] = test_data['swimDistance'] + test_data['rideDistance'] + test_data['walkDistance']
test_data.drop(['swimDistance', 'rideDistance', 'walkDistance'], axis=1, inplace=True)


# In[ ]:


test_data['matchType'] = test_data['matchType'].astype('category')
test_data['matchType'] = test_data['matchType'].cat.codes


# In[ ]:


test_data['health'] = test_data['boosts'] + test_data['heals']
test_data.drop(['boosts', 'heals'], axis=1, inplace=True)


# In[ ]:


test_data['kills'] += test_data['headshotKills'] + test_data['roadKills'] + test_data['teamKills']
test_data.drop(['headshotKills', 'roadKills', 'teamKills'], axis=1, inplace=True)


# In[ ]:


train_data.columns


# # Preparing data for ML model

# In[ ]:


# Mean

fill_NaN = Imputer(missing_values=np.nan, strategy='mean', axis=1)
train_data_mu = pd.DataFrame(fill_NaN.fit_transform(train_data))
train_data_mu.columns = train_data.columns
train_data_mu.index = train_data.index
train_data_mu.head()


# In[ ]:


y = train_data_mu['winPlacePerc']
X = train_data_mu.drop(['winPlacePerc'], axis=1)
train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.2, random_state=1511)


# In[ ]:


gc.collect()


# In[ ]:


clf = RandomForestRegressor(n_estimators=60, min_samples_leaf=2, min_samples_split=3, max_features=0.5 ,n_jobs=-1)
t0 = time()
clf.fit(train_X, train_y)
print('Training time', round(time() - t0, 3), 's')
pred = clf.predict(val_X)
print('MAE validation', mean_absolute_error(val_y, pred))


# In[ ]:


# Mean

fill_NaN_test = Imputer(missing_values=np.nan, strategy='mean', axis=1)
test_data_mu = pd.DataFrame(fill_NaN_test.fit_transform(test_data))
test_data_mu.columns = test_data.columns
test_data_mu.index = test_data.index
test_data_mu.head()


# In[ ]:


test_data = pd.read_csv('../input/test_V2.csv')
pred1 = clf.predict(test_data_mu)
test_data['winPlacePerc'] = pred1
submission = test_data[['Id', 'winPlacePerc']]
submission.to_csv('output.csv', index=False)

