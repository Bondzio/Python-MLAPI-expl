#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D


# In[ ]:


import os
print(os.listdir("../input"))


# In[ ]:


df = pd.read_csv('../input/recorded-crime-data-at-police-force-area-level/rec-crime-pfa.csv' )


# ### Data Overview

# In[ ]:


df.sample(10)


# In[ ]:


df.tail(5)


# In[ ]:


df.info()


# In[ ]:


df.isnull().any().any()


# Dataset has 46469 rows and with no null values.

# In[ ]:


df.nunique()


# In[ ]:


df['12 months ending'] = pd.to_datetime(df['12 months ending'])
df['Year'] = df['12 months ending'].dt.year
df['Month'] = df['12 months ending'].dt.month
df['Day'] = df['12 months ending'].dt.year
df['Day of week'] = df['12 months ending'].dt.dayofweek
df['Week of year'] = df['12 months ending'].dt.weekofyear


# In[ ]:


df.sample(5)


# In[ ]:


df = df.rename(columns={'Rolling year total number of offences':'Total crimes'})


# Column has been successfully split into different datetime categories.

# In[ ]:


for col in ['PFA','Region','Offence']:
    print('Unique values for {0}:'.format(col))
    print(df[col].unique())
    


# In[ ]:


for elem in df['Offence'].unique():
    print(elem)


# It is resonable to gruop some offences into common categories.

# In[ ]:


df.loc[df['Offence'].isin(['Domestic burglary','Non-residential burglary','Residential burglary','Non-domestic burglary']), 'Offence'] = 'Burglary'
df.loc[df['Offence'].isin(['All other theft offences','Bicycle theft','Shoplifting','Theft from the person']), 'Offence'] = 'Thieviery'
df.loc[df['Offence'].isin(['Violence with injury','Violence without injury']), 'Offence'] = 'Violence'


# In[ ]:


del df['12 months ending']


# ### Visualizations

# In[ ]:


plt.figure(figsize=(15,6))
ax = sns.barplot(x='Year', y='Total crimes', data=df)
plt.xticks(rotation=45,fontsize=10)
plt.show()


# In[ ]:


plt.figure(figsize=(15,6))
ax = sns.barplot(x='Region', y='Total crimes', data=df)
plt.xticks(rotation=45,fontsize=10)
plt.show()


# Now without Fraud 'regions'

# In[ ]:


df_temp = df[-df['Region'].isin(['Fraud: Action Fraud','Fraud: CIFAS','Fraud: UK Finance'])]


# In[ ]:


plt.figure(figsize=(15,6))
ax = sns.barplot(x='Region', y='Total crimes', data=df_temp)
plt.xticks(rotation=45,fontsize=13)
plt.show()


# Let's explore London region

# In[ ]:


df_london = df[df['Region'] == 'London']


# In[ ]:


plt.figure(figsize=(15,6))
ax = sns.barplot(x='Offence', y='Total crimes', data=df_london)
plt.xticks(rotation=80,fontsize=8)
plt.show()


# In[ ]:


offence_list = list(df_london['Offence'].unique())


# In[ ]:


g = sns.FacetGrid(df_london, col = "Offence", height=5,col_wrap=5)
g.map(plt.bar, "Year",'Total crimes', color = 'red')


# In[ ]:




