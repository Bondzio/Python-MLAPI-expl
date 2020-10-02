#!/usr/bin/env python
# coding: utf-8

# **Exploring data as India's perspective ** . Upvote if found useful

# In[1]:


import numpy as np # linear algebra
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
import cufflinks as cf
cf.set_config_file(offline=True, world_readable=True, theme='ggplot')

from subprocess import check_output
print(check_output(["ls", "../input/"]).decode("utf8"))


# In[2]:


file = '../input/globalterrorismdb_0617dist.csv'
data = pd.read_csv(file,encoding = "ISO-8859-1",low_memory=False)
data.info()


# In[3]:


data.columns[0:50]


# In[4]:


data.columns[50:100]


# In[5]:


data.columns[100:137]


# In[6]:


data[200:205]


# **Top countries faced terrorist attacks**

# In[7]:


data['country_txt'].value_counts()[:40][::-1].iplot(kind="barh",bargap=.4, title="Top 40 countries faced terrorist attacks")


# **Year wise terrorist attacks in world.**

# In[8]:


w = data.groupby('iyear').size()
w.iplot(kind="bar")
#plt.xlabel("Year",color='g',fontsize=20)
#plt.ylabel("Frequency",color='b',fontsize=20)
#plt.title("Year-wise attacks on world",color='b',fontsize=30)


# In[9]:


india = data.loc[data['country_txt'] == 'India']
india[15:20]


# In[10]:


pak = data.loc[data['country_txt'] == 'Pakistan']
america = data.loc[data['country_txt'] == 'United States']
amr= america.groupby('iyear')
pak = pak.groupby('iyear')


# In[11]:


#plt.xlabel("Year",color='green',fontsize=20)
#plt.ylabel("Frequency",color='b',fontsize=20)
#plt.title("Year wise Attacks on India",color='darkorange',fontsize=40)
ind = india.groupby('iyear')
ind.size().iplot(kind="bar",color='orange')


# In[12]:


plt.figure(figsize=(12,6))
i = ind.size()
a = amr.size()
p = pak.size()

plt.plot(i.index,i.values/i.values[0],color='orange')
plt.plot(p.index,p.values/p.values[0],color='green')
plt.plot(a.index,a.values/a.values[0],color='navy')
plt.xticks(a.index,rotation=75)
plt.legend(['India','Pakistan','United States'], loc='upper left',fontsize=15)
plt.xlabel("Year",fontsize=20)
plt.ylabel("Frequency",color='b',fontsize=20)
plt.title("Year-wise terrorist attacks comparison",color='r',fontsize=30)


# In[13]:


df = pd.DataFrame({'America':a.values},index=a.index)
dfi = pd.DataFrame({'India':i.values},index=i.index)
dfp = pd.DataFrame({'Pakistan':p.values},index=p.index)

result = pd.concat([df,dfi,dfp], axis=1, join_axes=[df.index]).fillna(0)
result.iplot(kind='scatter', filename='cufflinks/cf-simple-line')


# In[14]:


i = ind.sum()['nkill']
a = amr.sum()['nkill']
p = pak.sum()['nkill']
df = pd.DataFrame({'America':a.values},index=a.index)
dfi = pd.DataFrame({'India':i.values},index=i.index)
dfp = pd.DataFrame({'Pakistan':p.values},index=p.index)

result = pd.concat([df,dfi,dfp], axis=1, join_axes=[df.index]).fillna(0)
result.iplot(kind='scatter')


# In[15]:


data_part =data[['provstate', 'city','specificity', 'vicinity','location', 'summary']]
d = data_part['city'].value_counts()[1:31].iplot(kind="bar",fontsize=15)
#d.set_title("Top 30 cities faced attacks(Excluded Unknown)",color='r',fontsize=30)
#d.set_xlabel("City",color='m',fontsize=20)
#d.set_ylabel("Frequency",color='m',fontsize=20)


# Baghdad faced most attacks. Srinagar from India is also in top 30.

# In[16]:


d = data_part['location'].value_counts()[0:20].iplot(kind="barh",fontsize=9,color='green')
#d.set_title("Top 20 locations faced attacks",color='r',fontsize=30)
#d.set_ylabel("Location",fontsize=20)
#d.set_xlabel("Frequency",fontsize=20)


# In[17]:


data_part =data[['crit1', 'crit2', 'crit3', 'doubtterr','country_txt']]
data_part.describe()


# In[18]:


data_part =data[['nkill', 'nkillus', 'nkillter', 'nwound', 'nwoundus', 'nwoundte','country_txt','location']]
data_part.describe()


# In[19]:


d = data_part.groupby('country_txt').sum()
nkill = d.reindex().sort_values(by='nkill',ascending=False)['nkill']
s=nkill[0:20].iplot(kind="bar")
#s.set_title("Top 20 countries had highest casualities",color='r',fontsize=30)
#s.set_xlabel("Country",color='m',fontsize=20)
#s.set_ylabel("No. of wounded person",color='m',fontsize=20)


# In[20]:


nwound = d.reindex().sort_values(by='nwound',ascending=False)['nwound']
s=nwound[0:20].iplot(kind="bar")
#s.set_title("Top 20 countries had highest injuries",color='r',fontsize=30)
#s.set_xlabel("Country",color='m',fontsize=20)
#s.set_ylabel("No. of wounded person",color='m',fontsize=20)


# In[21]:


attackkill_ratio =  data_part.groupby('country_txt')['nkill'].sum()/data.groupby('country_txt').size()
attackkill_ratio1= attackkill_ratio.reindex().sort_values(ascending=False)
s=attackkill_ratio1[0:30].iplot(kind="bar")
#s.set_title("Top 30 countries highest casualities per attacks",color='r',fontsize=30)
#s.set_xlabel("Country",color='m',fontsize=20)
#s.set_ylabel("Casualities per attacks",color='m',fontsize=20)


# Ironically most of top thirty countries shown in above graph were not in top 30 attacked countries e.g. Afghanistan, India, Pakistan are not in above graph.

# In[22]:


attacknwound_ratio =  data_part.groupby('country_txt')['nwound'].sum()/data.groupby('country_txt').size()
attacknwound_ratio1= attacknwound_ratio.reindex().sort_values(ascending=False)
s=attacknwound_ratio1[0:30].iplot(kind="bar")
#s.set_title("Top 30 countries highest injuries per attacks",color='r',fontsize=30)
#s.set_xlabel("Country",color='m',fontsize=20)
#s.set_ylabel("Casualities per attacks",color='m',fontsize=20)


# Ironically, countries shown in above graph were not in top 30 countries which faced most attacks e.g. Afghanistan, India, Pakistan are not in above graph. In all graphs **Sri Lanka** is always present.

# In[23]:


cols = ['weaptype1', 'weaptype1_txt', 'weapsubtype1', 'weapsubtype1_txt',
       'weaptype2', 'weaptype2_txt', 'weapsubtype2', 'weapsubtype2_txt',
       'weaptype3', 'weaptype3_txt', 'weapsubtype3', 'weapsubtype3_txt',
       'weaptype4', 'weaptype4_txt', 'weapsubtype4', 'weapsubtype4_txt',
       'weapdetail', 'nkill', 'nkillus']
w = data[cols]
w.head()


# In[24]:


w['weapdetail'].value_counts()[:40].iplot(kind="bar",color='blue')

