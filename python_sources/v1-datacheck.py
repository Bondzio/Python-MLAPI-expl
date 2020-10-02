#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

fields = ['site_name', 'posa_continent' ]
train = pd.read_csv("../input/train.csv", 
                   #usecols = fields,
                  nrows= 5)


# In[ ]:


train.columns


# In[ ]:


train = pd.read_csv("../input/train.csv", 
                   usecols = fields,
                  #nrows= 5,
                   )


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt
# preferred continent destinations
sns.countplot(x='site_name', data=train)


# In[ ]:


train.site_name.value_counts()


# In[ ]:


sns.countplot(x='posa_continent', data=train)


# In[ ]:


train.posa_continent.value_counts()


# In[ ]:


fields = [ 'posa_continent', 'hotel_continent', 'is_mobile']
train = pd.read_csv('../input/train.csv', usecols = fields)


# In[ ]:


sns.countplot(x= 'hotel_continent', data = train)


# In[ ]:


sns.countplot(x='posa_continent', hue ='is_mobile', data=train)


# In[ ]:


sns.countplot(x='hotel_continent', hue ='is_mobile', data=train)


# In[ ]:


# Observign plots 14-17, makes sense, since most of the users are from continent 3
# They are also the one who most search for hotels in continent in 2
# 2 must be a very loved continent 

sns.countplot(x='posa_continent', hue ='hotel_continent', data=train)


# In[ ]:


fields = ['hotel_country' , 'user_location_country']
train = pd.read_csv('../input/train.csv', usecols= fields)
sns.distplot(train.hotel_country, label = "Hotel Coutry")
sns.distplot(train.user_location_country, label = "User Country")
plt.legend()


# In[ ]:


import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

fields = ['hotel_continent' , 'posa_continent', 'srch_co', 'srch_ci']
train = pd.read_csv('../input/train.csv', usecols= fields, parse_dates=['srch_ci', 'srch_co'], nrows =100000)

train['hotel_nights'] = ((train.srch_co - train.srch_ci) / np.timedelta64( 1, 'D')).astype(float)
plt.figure(figsize=(11, 9))
ax = sns.boxplot(x='hotel_continent', y='hotel_nights', data=train)
lim = ax.set(ylim=(0, 15))


# In[ ]:




