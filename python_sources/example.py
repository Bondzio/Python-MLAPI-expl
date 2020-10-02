#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


df = pd.read_csv('../input/untappd-checkins/main_data_checkins.csv')


# In[ ]:


top_breweries = df['brewery_name'].value_counts()[:10].index.tolist()
top_breweries_df = df[df['brewery_name'].isin(top_breweries)]


# In[ ]:


plt.figure(figsize=(25,6))
figure = sns.countplot(x='brewery_name', data=top_breweries_df, order=top_breweries)
plt.xlabel('Brewery', fontsize=20) 
plt.ylabel('Number of checkins', fontsize=20)
plt.suptitle('Most popular breweries', fontsize=26)
plt.show()


# In[ ]:


df['beer_name'].value_counts()[:10]


# In[ ]:


df['venue_name'].value_counts()[:10]


# In[ ]:




