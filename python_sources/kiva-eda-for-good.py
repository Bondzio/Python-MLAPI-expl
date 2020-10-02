#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import seaborn as sns
import cufflinks as cf

import plotly.offline as py
py.init_notebook_mode(connected=True)
cf.go_offline()
import plotly.graph_objs as go
import plotly.tools as tls
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))
df_loans = pd.read_csv("../input/kiva_loans.csv")
df_locations = pd.read_csv("../input/kiva_mpi_region_locations.csv")
df_loan_theme_id = pd.read_csv("../input/loan_theme_ids.csv")
df_loan_theme_region = pd.read_csv("../input/loan_themes_by_region.csv")
# Any results you write to the current directory are saved as output.


# ## Exploring kiva loans data

# In[2]:


df_loans.describe()


# In[3]:


#lets explore the na values
df_loans.isnull().sum(axis=0)


# In[4]:


df_loans.head()


# In[5]:


df_loans.info()


# In[6]:


#finding correlation between funded amount, loan amount and lender count
sns.heatmap(df_loans[['funded_amount','loan_amount','lender_count']].corr())


# In[7]:


df_loans['activity'].value_counts()[:10]


# In[8]:


df_loans['sector'].value_counts()


# In[9]:


plt.figure(figsize=(16,6))
sns.countplot(x='sector',data=df_loans)


# In[10]:


#df_loans.pivot_table('pivot between sector and activity')


# In[11]:


df_loans['country'].value_counts()[:10]


# In[12]:


df_loans['use'].value_counts().reset_index().values[:3]


# In[13]:


#This will require us to find similar use and club them together.
'''
medical_referrer_index = data['referrer'].str.contains('medical')
medical_referrals = data[medical_referrer_index]
medical_referrals
'''


# In[14]:


df_loans[['posted_time','funded_time','disbursed_time']].isnull().sum()


# In[15]:


df_loans['posted_time']=pd.to_datetime(df_loans['posted_time'])
df_loans['funded_time']=pd.to_datetime(df_loans['funded_time'])
df_loans['disbursed_time']=pd.to_datetime(df_loans['disbursed_time'])


# In[16]:


df_loans['disbursedDayOfWeek'] = df_loans['disbursed_time'].apply(lambda x: x.dayofweek)


# In[17]:


df_loans['disbursedDayOfWeek'].tail()


# In[18]:


dayMap = {0.0:'Mon',1.0:'Tue',2.0:'Wed',3.0:'Thu',4.0:'Fri',5.0:'Sat',6.0:'Sun'}


# In[19]:


df_loans['disbursedDayOfWeek'] = df_loans['disbursedDayOfWeek'].map(dayMap)


# In[20]:


dC = df_loans[['disbursed_time','disbursedDayOfWeek']].groupby('disbursedDayOfWeek').count()


# In[21]:


dC.sort_values('disbursed_time').iplot(kind='bar')


# In[22]:


#df_loans['borrower_genders'].value_counts()
def getGender(data):
    try:
        nd = sorted(data.replace(' ','').replace('\n','').replace('\t','').split(','))
    except Exception as e:
        nd = 'NULL'
    return nd


# In[23]:


#list(map(lambda x: x.strip(),df_loans['borrower_genders'][10].split(',')))
getGender(df_loans['borrower_genders'][1])


# In[24]:


#df_loans['borrower_male'] = map(df['borrower_genders'])
from itertools import groupby
[(x,len(list(y))) for x,y in groupby(map(lambda x: x.strip(),df_loans['borrower_genders'][1].split(',')))]


# In[25]:


df_loans['borrower_count'] = list(map(lambda x : [(ix,len(list(y))) for ix,y in groupby(getGender(x))], df_loans['borrower_genders']))


# In[26]:


#df_loans['borrower_genders'][1]
#df_loans['borrower_count'].head()
df_loans['borrower_count'] = df_loans['borrower_count'].apply(dict)


# In[27]:


df_loans['borrower_male_count'] = list(map(lambda x : x['male'] if 'male' in x.keys() else 0, df_loans['borrower_count']))
df_loans['borrower_female_count'] = list(map(lambda x : x['female'] if 'female' in x.keys() else 0, df_loans['borrower_count']))


# In[28]:


df_loans['borrower_male_count'].sum()


# In[29]:


df_loans['borrower_female_count'].sum()


# In[30]:


df_loans.loc[df_loans['funded_amount'] != df_loans['loan_amount']].head()


# ### Observations till now
# 
# * above data tells us that only 5 records are there which have higher loan amount than funded amount
# * highest amount of loans where disbursed on Friday
# * Philippines has the highest number of loans
# * Agriculture was the sector where highest number of loans was given followed by food
# * There were 274,904 male borrower
# * There were 1,071,308 female borrower

# In[31]:


df_loans.groupby(by = ['sector'])['loan_amount'].sum().sort_values(ascending=False)
#pd.DataFrame({'total_amount':df_loans.groupby(by = ['sector'])['loan_amount'].sum()})


# In[32]:


df_loans.columns


# In[33]:


# Finding correlation between lender count and borrower count


# In[34]:


df_loans['borrower_count'] = list(map(lambda x : sum(x.values()),df_loans['borrower_count']))


# In[35]:


print("Borrower Count: ",df_loans['borrower_count'].sum())
print("Lender Count: ",df_loans['lender_count'].sum())


# In[36]:


print(df_loans[['borrower_count','lender_count']].corr())
sns.heatmap(df_loans[['borrower_count','lender_count']].corr())


# In[37]:


df_loans[['term_in_months', 'id']].groupby(['term_in_months']).count().iplot(kind='line')


# In[38]:


sns.heatmap(df_loans.corr())


# In[39]:


df_loans.hist(bins=50, figsize=(12,8))


# In[40]:


#df_loans.groupby(by = ['sector'])['loan_amount'].sum().sort_values(ascending=False)
df_cca = pd.DataFrame({'amount':df_loans.groupby(by=['country'])['loan_amount'].sum(),'count':df_loans['country'].value_counts()}).reset_index()


# In[41]:


df_cca.head()


# In[42]:


df_cca.columns = ['country','amount','count']


# In[43]:


#pd.DataFrame(df_loans.head()['country'].agg(sum)).reset_index()


# In[44]:


data = [ dict(
        type = 'choropleth',
        locations = df_cca['country'],
        locationmode = 'country names',
        z = df_cca['amount'],
        text = df_cca['country'],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = 'Amount of Loans'),
      ) ]

layout = dict(
    title = 'Amount of loans by Country',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='loans-world-map')


# In[45]:


data = [ dict(
        type = 'choropleth',
        locations = df_cca['country'],
        locationmode = 'country names',
        z = df_cca['count'],
        text = df_cca['country'],
        colorscale = [[0,"rgb(5, 10, 172)"],[0.85,"rgb(40, 60, 190)"],[0.9,"rgb(70, 100, 245)"],\
           [0.94,"rgb(90, 120, 245)"],[0.97,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = 'Number of Loans'),
      ) ]

layout = dict(
    title = 'Number of loans by Country',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='loans-world-map')


# In[ ]:




