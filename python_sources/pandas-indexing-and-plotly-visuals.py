#!/usr/bin/env python
# coding: utf-8

# ## Pandas Indexing Overview <a id='toc' >
# 
# Proper use of pandas indexing makes life much easier and more importantly much faster, however this is often a misunderstood capability. Wes McKinney spent a good deal of time and effort optimizing pandas through the use of indexing. In this tutorial, we will review the following:
# 
# * [Data prep](#prep)
# * [Initial data exploration](#explore)
# * [Basic pandas indexing](#basic)
# * [Multi indexing](#multi)
# * [Review how much faster indexing is](#fast)
# * [Operating on groups using indexing](#groups)

# In[3]:


import pandas as pd
import requests
import zipfile
import io


# In[4]:


# lets load and examine the dataset

df = pd.read_csv('../input/CAERS_ASCII_2004_2017Q2.csv')


# In[5]:


df.head()


# In[6]:


print("""Dataset shape: {}
        \nDatasets type: {}""".format(df.shape,
                                     df.dtypes))


# ### Data prep <a id='prep' >
# Initial preparation of the data
# 
# * renaming columns
# * converting dtypes
# * normalizing age
# 
# [return to table of contents](#toc)

# In[7]:


# lets prep the data just a bit

# convert CI_Age at Adverse Event to number 
# convert AEC_Event Start Date to datetime and rename to EventDate
# convert RA_CAERS Created Date to datetime and rename to ReportDate
# normalize CI_Age based on units

df.rename(columns={'RA_CAERS Created Date': 'ReportDate',
                  'AEC_Event Start Date': 'EventDate',
                  'AEC_One Row Outcomes': 'Outcome',
                  'SYM_One Row Coded Symptoms': 'Symptoms',
                  'CI_Age at Adverse Event': 'Age',
                  'CI_Gender': 'Gender',
                  'PRI_Reported Brand/Product Name': 'ProductBrandName',
                  'PRI_FDA Industry Name': 'Industry'}, 
         inplace=True)

# convert age to numeric
df['Age'] = pd.to_numeric(df['Age'], errors='coerce') # convert to numeric and convert missing
df['ReportDate'] = pd.to_datetime(df['ReportDate'],
                                 format='%m/%d/%Y')
df['EventDate'] = pd.to_datetime(df['EventDate'],
                                format='%m/%d/%Y')


# In[8]:


# now we need to norm the age - lets inspect what age units we have
df['CI_Age Unit'].unique().tolist()


# In[9]:


# lets create a utility func to help with the conversions

def convert_age(row):
    """
    normalize the age value based on the units. 
    i.e. if units in months, convert to years by dividing by 12
    
    :param row: pd.DataFrame row
    :return float - normalized age
    :rtype: float
    """
    age = row['Age']
    units = row['CI_Age Unit']
    
    # create lookup map
    lookup = {'Year(s)': 1.0,
             'Month(s)': 12.0,
             'Week(s)': 52.0,
             'Day(s)': 365.0,
             'Decade(s)': .1}
    
    if units != 'Not Available':
        # return the age as years
        return float(age)/lookup[units]
    
df['AgeNormed'] = df.apply(lambda row: convert_age(row), axis=1)


# In[10]:


print("""Average victim age: {}
        \nYoungest victim age: {} years,
        \nOldest victim age: {} years""".format(df['AgeNormed'].mean(),
                                               df['AgeNormed'].min(),
                                               df['AgeNormed'].max()))


# In[11]:


# there might be some data quality issues here - lets examine rows with an age 
# greater than 100 years
df[df['AgeNormed'] > 100][['Age', 'CI_Age Unit', 'AgeNormed']]


# In[12]:


# lets drop rows where AgeNormed is greater than 105 - I have never heard of someone
# surviving 76 decades - if thats true, I need to get on their diet ASAP
df = df.drop(df[df['AgeNormed'] > 105].index)

print("""Average victim age: {}
        \nYoungest victim age: {} years,
        \nOldest victim age: {} years""".format(df['AgeNormed'].mean(),
                                               df['AgeNormed'].min(),
                                               df['AgeNormed'].max()))


# In[37]:


df[df['AgeNormed'] < 0.01].head() # as for the other end of hte spectrum, it does look like when 
# an age is at 0, it's due to premature babies according to the symptoms - lets leave these


# In[14]:


# and finally, lets create some age bins
def agebins(age):
    
    if age < 2:
        return 'baby'
    
    if age >=2 and age < 13:
        return 'child'
    
    if age >= 13 and age < 20:
        return 'teenager'
    
    if age >= 20 and age < 35:
        return 'youngAdult'
    
    if age >=35 and age < 60:
        return 'adult'
    
    if age >= 60:
        return 'senior'

df['AgeBins'] = df['Age'].apply(lambda x: agebins(x))


# ### Initial data exploration <a id='explore' >
# Let's get a better sense for what this data is about, and how we might use this to inform proper indexing levels
# 
# [return to table of contents](#toc)

# In[15]:


import plotly
from plotly.offline import init_notebook_mode, plot, iplot
import cufflinks
import plotly.graph_objs as go

# initialize jupyter notebook mode
init_notebook_mode(connected=True)

plotly.__version__ # make sure we have the right version of plotly


# In[16]:


# lets examine the top 10 industries with the most issues
bar_data = (df.groupby('Industry')['Age'].count()
             .reset_index()
             .rename(columns={'Age': 'NumRecords'})
             .sort_values('NumRecords', ascending=False)
             .nlargest(10, 'NumRecords'))

data = [go.Bar(
            x=bar_data['Industry'].values.tolist(),
            y=bar_data['NumRecords'].values.tolist())]

layout = go.Layout(
            title='Events by Industry',
            xaxis=dict(title='Industry', titlefont=dict(family='Courier New, monospace',
                                                       size=18)),
            yaxis=dict(title='# of Records', titlefont=dict(family='Courier New, monospace',
                                                       size=18))
)

figure = go.Figure(data=data, layout=layout)
iplot(figure)


# In[17]:


# lets check out events by age

bar_data = (df.groupby('AgeBins')['Age'].count()
             .reset_index()
             .rename(columns={'Age': 'NumRecords',
                             'AgeBins': 'Age'})
             .sort_values('NumRecords', ascending=False)
             .nlargest(10, 'NumRecords'))

data = [go.Bar(
            x=bar_data['Age'].values.tolist(),
            y=bar_data['NumRecords'].values.tolist())]

layout = go.Layout(
            title='Events by Age',
            xaxis=dict(title='Age', titlefont=dict(family='Courier New, monospace',
                                                       size=18)),
            yaxis=dict(title='# of Records', titlefont=dict(family='Courier New, monospace',
                                                       size=18))
)

figure = go.Figure(data=data, layout=layout)
iplot(figure)


# In[18]:


# lets also examine events by year

# remove null event date rows
years = df[df['EventDate'].notnull()].copy(deep=True)

# extract year and convert to integer
years['EventYear'] = pd.DatetimeIndex(years['EventDate']).year.astype(int).values.tolist()

yeardata = (years.groupby('EventYear')['Age']
           .count()
           .reset_index()
           .rename(columns={'EventYear': 'Year',
                                'Age': 'NumRecords'}))

# filter to last 20 years - drop 2017 due to incomplete collection
yeardata = yeardata[(yeardata['Year'] >= 2000) & (yeardata['Year'] < 2017)]

data = [go.Scatter(
            x=yeardata['Year'].values.tolist(),
            y=yeardata['NumRecords'].values.tolist()
)]

layout = go.Layout(
            title='Events by Year',
            xaxis=dict(title='Year', titlefont=dict(family='Courier New, monospace',
                                                       size=18)),
            yaxis=dict(title='# of Records', titlefont=dict(family='Courier New, monospace',
                                                       size=18))
)

figure = go.Figure(data=data, layout=layout)
iplot(figure)


# ### Basic pandas indexing <a id='basic' >
# * How to set an index
# * How to retrieve via index
# 
# [return to table of contents](#toc)

# In[20]:


# setting an index in pandas is quite easy - lets use AgeBins to start

hdf = df.set_index('AgeBins')

# lets select all rows that are related to children
hdf.loc['child', :].head()


# In[21]:


# you can create a boolean mask to pass from analysis to analysis as well
cmask = hdf.index=='child'
# select age for all children
hdf.loc[cmask, 'Age'].head()


# ### Multi indexing <a id='multi' >
# pandas supports creating multiple levels within your indexing. You can construct the 
# indices in several different ways
# 
# [return to table of contents](#toc)

# In[22]:


hdf = df.set_index(['AgeBins', 'Industry'])
hdf.head()


# In[23]:


# lets create multiple indices - agebins and industry
hdf = df.set_index(['AgeBins', 'Industry'])

# we can select all adults that had an event related to cosmetics with the 
# following:
hdf.loc[('adult', 'Cosmetics'), :].head()


# In[24]:


# however, you may notice that the indices are not sorted
hdf.head()


# In[25]:


# to sort our indices lexicographically (alphabetically) (which pandas will look for in more complex queries)
# we can use:

hdf.sort_index(inplace=True,
              level=[0, 1])

# check that both levels were sorted
hdf.index.lexsort_depth # both levels are sorted against


# In[26]:


# now we can select ranges of items - lets get all records from adult to child 
# without explicitly defining each level (adult, baby, child) - remember its alphabetically
# sorted

hdf.loc[slice('adult', 'child'), :].head()


# In[27]:


# and to select ranges for both levels - in this case all 
# rows that are adult through child, and in industry alcoholic beverage through
# choc/cocoa products

hdf.loc[(slice('adult', 'child'), slice('Alcoholic Beverage', 'Choc/Cocoa Prod')), :].head()


# In[28]:


# however the slice object isn't ideal - we can use pandas IndexSlice to perform 
# in a more compact way
idx = pd.IndexSlice

# lets perform the same query as above with our new slicer
hdf.loc[idx[['adult', 'child'], ['Alcoholic Beverage', 'Choc/Cocoa Prod']], :].head()


# ### How much faster is indexing than traditional conditional lookups? <a id='fast' >
# 
# Lets run a quick simulation to get a sense for how much faster pandas indexing really is
# 
# [return to table of contents](#toc)

# In[29]:


import timeit

# lets set up a scenario to select all adult, baby and child rows
start = timeit.default_timer()

for i in range(1000):
    z = hdf.loc[idx[['adult', 'child'], :], :]
    
elapsed = timeit.default_timer() - start
print(elapsed)


# In[30]:


start = timeit.default_timer()

# and for traditional conditional lookups
for i in range(1000):
    z = df.loc[(df['AgeBins'] == 'adult') & (df['AgeBins'] == 'baby') & (df['AgeBins'] == 'child'), :]
    
elapsed2 = timeit.default_timer() - start
print(elapsed2)


# In[31]:


print("""Total time for 1000 iterations: 
        \nUsing traditional conditional selection: {}
        \nUsing pandas indexing: {}""".format(elapsed2, elapsed))


# ### Operating on groups and getting summary statistics <a id='groups' >
# Lets see how we can get summary stats for varying levels of an index
# 
# [return to table of contents](#toc)

# In[32]:


# lets get the average age of each agebin
hdf['Age'].mean(level=0) # simple as that


# In[33]:


# and if we want it for both levels - average age of 
# reported event victim per bin by industry
hdf['Age'].mean(level=[0, 1]).head()


# In[34]:


# and just the average age for industry
(hdf['Age'].mean(level=1)
 .reset_index()
 .rename(columns={'Age': 'AvgAge'})
 .sort_values('AvgAge', ascending=False)
 .nsmallest(10, 'AvgAge'))


# In[35]:


# get the diff between max and min age by agebin in the index
hdf['Age'].groupby(level=0).apply(lambda x: x.max() - x.min())


# In[36]:


# and finally, to simply return to your normal, unindexed dataframe
# you can use reset_index()

hdf.reset_index().tail()


# In[ ]:




