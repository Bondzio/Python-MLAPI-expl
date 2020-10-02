#!/usr/bin/env python
# coding: utf-8

# **Understanding the patterns of terror strikes in India.**
# 
# *Importing data, selecting relevant columns and giving them more intuitive names.*

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.figsize'] = 8, 5
plt.rcParams['image.cmap'] = 'viridis'
import warnings
warnings.filterwarnings('ignore')

terror_data = pd.read_csv('../input/globalterrorismdb_0718dist.csv', encoding='ISO-8859-1',
                          usecols=[0, 1, 2, 3, 8, 11, 13, 14, 35, 84, 100, 103])
terror_data = terror_data.rename(
    columns={'eventid':'id', 'iyear':'year', 'imonth':'month', 'iday':'day',
             'country_txt':'country', 'provstate':'state', 'targtype1_txt':'target',
             'weapsubtype1_txt':'weapon', 'nkillter':'fatalities', 'nwoundte':'injuries'})


# Filter the data for India and doing a quick summary

# In[ ]:


terror_data.shape
terror_data.head().T
India = terror_data[terror_data.country=='India']
India.describe(include='all').T


# Doing basic Feature Engineering 
# 1. Creating a column for day of the week
# 2. Renaming the names of the states which had different spellings
# 3. Replacing na with 0 in fatalities and injuries columns

# In[ ]:


sns.set_style("white")
plot = India.drop(['id','latitude','longitude','country'],axis=1)
plot['day'] = plot['day'].replace(0,1)
plot['weekday'] = pd.to_datetime(plot[['year','month','day']],errors='coerce').dt.weekday_name

t = {'Andhra pradesh':'Andhra Pradesh','Orissa':'Odisha'}
plot.state.replace(t,inplace=True)

plot['fatalities'] = plot.fatalities.fillna(0)
plot['injuries'] = plot.injuries.fillna(0)


# Ploting histograms for numeric variables

# In[ ]:


t = plot.select_dtypes(include=np.number)
for c in t.columns:
    sns.distplot(t[c],color='red')
    plt.xlim(t[c].min(),t[c].max())
    plt.show()


# Plotting distributions of Non Numeric Columns

# In[ ]:


# sns.set(rc={'figure.figsize':(16,5)})
t = plot.select_dtypes(exclude=np.number)
for columns in t.columns:
    sns.countplot(data=t,x=columns,order = plot[columns].value_counts().sort_values(ascending=False).index)
    plt.xticks(rotation=85)
    plt.show()


# Heatmaps of Non Numerics variables

# In[ ]:


t = pd.crosstab(plot.state, plot.target)
sns.set(rc={'figure.figsize':(16,8)})
sns.heatmap(t,linewidths=.1,linecolor='gray',annot=True,fmt='d',annot_kws={"size": 8})


# In[ ]:


t = pd.crosstab(plot.state, plot.weapon)
sns.set(rc={'figure.figsize':(16,9)})
sns.heatmap(t,linewidths=.1,linecolor='gray',annot=True,fmt='d',annot_kws={"size": 8})


# In[ ]:


sns.set(rc={'figure.figsize':(16,9)})
t = pd.crosstab(plot['state'],plot['year'])
sns.heatmap(t)


# The number of terror strikes has gone up since 2009 and has gone up even further since 2014.

# In[ ]:




