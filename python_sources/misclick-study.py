#!/usr/bin/env python
# coding: utf-8

# ## Inspired by:
# https://www.kaggle.com/zgzjnbzl/visualizing-distraction-and-misclicking

# In[ ]:


import numpy as np
import pandas as pd
import math
import json
from tqdm import tqdm_notebook as tqdm
import matplotlib.pyplot as plt


# In[ ]:


train_labels_df = pd.read_csv('/kaggle/input/data-science-bowl-2019/train_labels.csv')
#print(train_labels_df.shape)
#train_labels_df.head()


# In[ ]:


train_df = pd.read_csv('/kaggle/input/data-science-bowl-2019/train.csv')
print(train_df.shape)
# get rid of useless ids
real_ids = train_labels_df.installation_id.unique()
train_df = train_df[train_df.installation_id.isin(real_ids)]
print(train_df.shape)
# Next gametime at current line
train_df['next_gt'] = train_df['game_time'].shift(-1)
train_df.head()
#train_df.head()


# In[ ]:


# Clean data for 4070 events
event4070 = train_df[train_df.event_code == 4070]
# Additional cleaning
del event4070['event_id']
del event4070['timestamp']
del event4070['world']


# In[ ]:


event4070.loc[:, 'dist_norm'] = 0
event4070.loc[:, 'event_count_diff'] = 0
event4070.loc[:, 'time_diff'] = 0
event4070.loc[:, 'time_diff_forward'] = 0

prev_x = 0
prev_y = 0
prev_event_count = 0
prev_game_time = 0

for (i, row) in tqdm(event4070.iterrows(), total=event4070.shape[0]):
    event_data_str = row['event_data']
    event_count = row['event_count']
    game_time = row['game_time']
    next_game_time = row['next_gt']
    
    event_diff = event_count - prev_event_count
    if event_diff > 0:
        event4070.at[i, 'event_count_diff'] = event_diff
    else:
        if event_diff == 0: 
            event4070.at[i, 'event_count_diff'] = event_count
        if event_diff < 0:
            event4070.at[i, 'event_count_diff'] = -1
    
    coordinates = json.loads(event_data_str)['coordinates']
    x_norm = int(coordinates['x'] / coordinates['stage_width'] * 100)
    y_norm = int(coordinates['y'] / coordinates['stage_height'] * 100)
    event4070.at[i, 'dist_x'] = x_norm - prev_x
    event4070.at[i, 'dist_y'] = y_norm - prev_y
    event4070.at[i, 'dist_norm'] = math.sqrt((x_norm - prev_x) ** 2 + (y_norm - prev_y) ** 2)
    
    if game_time >= prev_game_time:
        time_diff = game_time - prev_game_time
    else:
        time_diff = 0
    event4070.at[i, 'time_diff'] = time_diff
    
    if  next_game_time > game_time:
        time_diff_forward = next_game_time - game_time
    else:
        time_diff_forward = -1
    event4070.at[i, 'time_diff_forward'] = time_diff_forward
    
    prev_x = x_norm
    prev_y = y_norm
    prev_event_count = event_count
    prev_game_time = game_time


# ## Number of events between 4070 events
# 
# Minus -1 if first misclick of game session.

# In[ ]:


event4070['event_count_diff'].max()


# In[ ]:


event4070['event_count_diff'].plot.hist(bins=1000, xlim=(-5,20))


# ### Time spent with singular 4070 events
# 
# If we have a singular 4070 event (not followed by another misclick) then the only interesting feature is the time spent until the next action. This feature might correlate to thinking speed / game concept understanding.

# In[ ]:


event4070_nonrepeat = event4070[event4070.event_count_diff != 1]


# In[ ]:


# Filter outliers
event4070_nonrepeat_filtered_out = event4070_nonrepeat[event4070_nonrepeat.time_diff_forward > 60000]
event4070_nonrepeat = event4070_nonrepeat[event4070_nonrepeat.time_diff_forward <= 60000]


# In[ ]:


event4070_nonrepeat['time_diff_forward'].plot.hist(bins=4000, xlim=(-100,2500))


# ## Time and position diff between multiple 4070 events
# 
# If we have a multiple 4070 event after each other then we have multiple interesting feature.
# 
# 1) The time spent between two misclick. (0 time difference might be touchpad related)
# 
# 2) The distance between two misclick. (similar coords might be touchpad related issue, larger distance is another incorrect guess)
# 
# These features might correlate to reaction speed / thinking speed / game concept understanding.

# In[ ]:


event4070_repeat = event4070[event4070.event_count_diff == 1]


# In[ ]:


# Filter outliers
event4070_filtered_out = event4070_repeat[event4070_repeat.time_diff > 10000] # 30 s
print(event4070_filtered_out.shape)
event4070_repeat = event4070_repeat[event4070_repeat.time_diff <= 10000]


# In[ ]:


event4070_repeat['time_diff'].plot.hist(bins=200, xlim=(-100,3000), ylim=(0,120000))


# In[ ]:


event4070_repeat['dist_x'].plot.hist(bins=50)


# In[ ]:


event4070_repeat['dist_x'].plot.hist(bins=50)


# In[ ]:


event4070_repeat['dist_x'].plot.hist(bins=100, xlim=(-10,10))


# In[ ]:


x = event4070_repeat['time_diff']
y = event4070_repeat['dist_x']
H, xedges, yedges = np.histogram2d(x, y, bins=[100,100])
H = H.T

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, title='2D histogram (square bins)')
plt.imshow(np.log1p(H), interpolation='nearest', origin='low')


# In[ ]:


event4070_repeat['dist_y'].hist(bins=50)


# In[ ]:


x = event4070_repeat['time_diff']
y = event4070_repeat['dist_y']
H, xedges, yedges = np.histogram2d(x, y, bins=[100,100])
H = H.T

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, title='2D histogram (square bins)')
plt.imshow(np.log1p(H), interpolation='nearest', origin='low')


# In[ ]:


event4070_repeat['dist_norm'].hist(bins=141)


# #### Three interesting mini peak at bottom right corner!

# In[ ]:


x = event4070_repeat['dist_x']
y = event4070_repeat['dist_y']
H, xedges, yedges = np.histogram2d(x, y, bins=[50,50])
H = H.T

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, title='2D histogram (square bins)')
plt.imshow(np.log1p(H), interpolation='nearest', origin='low')


# In[ ]:


x = event4070_repeat['time_diff']
y = event4070_repeat['dist_norm']
H, xedges, yedges = np.histogram2d(x, y, bins=[100,141])
H = H.T

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, title='2D histogram (square bins)')
plt.imshow(np.log1p(H), interpolation='nearest', origin='low')


# In[ ]:


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, title='2D histogram (square bins)')
plt.imshow(np.log1p(H[:20,:20]), interpolation='nearest', origin='low')

