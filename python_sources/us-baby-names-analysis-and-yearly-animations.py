#!/usr/bin/env python
# coding: utf-8

# #US Baby Names Data Analysis

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings("ignore", message="axes.color_cycle is deprecated")
import numpy as np
import pandas as pd
import scipy as sp
import seaborn as sns
import sqlite3


# In[ ]:


#%%sh
get_ipython().system('pwd')
get_ipython().system('ls -ls /kaggle/input/*/')


# In[ ]:


get_ipython().system('ls ../input/')
con = sqlite3.connect('../input/us-baby-names/database.sqlite')
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())


# In[ ]:


# helper method to load the data
def load(what='NationalNames'):
    assert what in ('NationalNames', 'StateNames')
    cols = ['Name', 'Year', 'Gender', 'Count']
    if what == 'StateNames':
        cols.append('State')
    df = pd.read_sql_query("SELECT {} from {}".format(','.join(cols), what), con)
    return df


# In[ ]:


#National data
national = load(what='NationalNames')
national.head(5)


# In[ ]:


top_names = national.groupby(['Name','Gender'])['Count'].sum().reset_index().sort_values(by='Count',ascending=False)
top_names.head()


# ## Top Male and Female Names

# In[ ]:


top_names_male = top_names[top_names['Gender']=='M'].head(50)
top_names_female = top_names[top_names['Gender']=='F'].head(50)
#print(top_names_male.head())
#print(top_names_female.head())


# In[ ]:


import matplotlib.pyplot as plt
fig,ax=plt.subplots(1,2,figsize=(20,12))
sns.barplot(data=top_names_female,y='Name',x='Count',ax=ax[0], color='Red')
sns.barplot(data=top_names_male,y='Name',x='Count',ax=ax[1], color='Blue')


# In[ ]:





# In[ ]:





# In[ ]:


national['Decade'] = national['Year'].apply(lambda x: 10*(x//10))


# In[ ]:


import plotly.express as px

gender='M'

top_names_by_year = national[national['Gender']==gender].groupby(['Name','Decade'])['Count'].sum().reset_index().sort_values(by=['Decade','Count'],ascending=[True,False])
top_names_by_year.head()

fig = px.bar(top_names_by_year, x="Name", y="Count",
  animation_frame="Decade", color='Count') #range_y=[0,4000000000]
fig.show()


# In[ ]:


# Is number of males increased over the year, compared to same of female?
tmp = national.groupby(['Year','Gender']).sum()

male = tmp.query("Gender=='M'").reset_index('Year').sort_index()
female = tmp.query("Gender=='F'").reset_index('Year').sort_index()
#print(male.head())
#print(female.head())
final = pd.merge(male, female, on = ['Year'], how = 'outer', suffixes = ['_m', '_f'])
final['male_extra'] = final['Count_m'] - final['Count_f'] 
final = final.set_index('Year').sort_index()


# In[ ]:


print(final.head())
final.plot()


# In[ ]:


name_year = national.groupby(['Name','Year']).sum().reset_index(['Name','Year'])


# In[ ]:


dr = name_year[name_year['Name']=='Michel']
dr['lag'] = (dr['Count'] - dr['Count'].shift(5))#/dr['Count']
print(dr['lag'].sum())
dr[['Year', 'Count', 'lag']].plot('Year')


# In[ ]:


name_year[name_year['Name']=='George'].plot('Year')


# In[ ]:




