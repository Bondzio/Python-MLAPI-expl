#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:


def load_ts_data(status):
    df = pd.read_csv('/kaggle/input/coronavirus-covid19-cases-jhu-data/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-{}.csv'.format(status))
    return df

def create_agg_ts(status):
    df = load_ts_data(status)
    df = df.drop(['Lat','Long','Province/State','Country/Region'], axis=1)
    df = df.sum().astype(int)
    return df

def create_country_ts(status):
    df = load_ts_data(status)
    df = df.drop(['Lat','Long','Province/State'], axis=1)
    df = df.groupby('Country/Region').sum().astype(int)
    df = df.transpose()
    df.index.name = 'Date'
    df.index  = pd.to_datetime(df.index)
    return df

def create_region_ts(status):
    df = load_ts_data(status)
    df = df.drop(['Lat','Long','Country/Region'], axis=1)
    df = df.groupby('Province/State').sum().astype(int)
    df = df.transpose()
    df.index.name = 'Date'
    df.index  = pd.to_datetime(df.index)
    return df


# # Global
# Looking at confirmed cases, recoveries and deaths. 

# In[ ]:


df_total = pd.DataFrame(columns=['Confirmed','Deaths','Recovered'])
df_total['Confirmed'] = create_agg_ts('Confirmed')
df_total['Deaths'] = create_agg_ts('Deaths')
df_total['Recovered'] = create_agg_ts('Recovered')


# In[ ]:


df_total.plot()


# In[ ]:


df_total['Deaths'].plot()


# # By Country
# Plotting confirmed cases and deaths focusing on top 10 regions.

# In[ ]:


df_country_confirmed = create_country_ts('Confirmed')
df_country_deaths = create_country_ts('Deaths')


# In[ ]:


top_10_countries_confirmed = df_country_confirmed.drop(['Others'],axis=1).max().sort_values(ascending=False).index[:10].tolist()
top_10_countries_deaths = df_country_deaths.drop(['Others'],axis=1).max().sort_values(ascending=False).index[:10].tolist()


# In[ ]:


df_country_confirmed.loc[:,top_10_countries_confirmed].plot()


# In[ ]:


df_country_confirmed.loc[:,top_10_countries_confirmed[1:]].plot()


# In[ ]:


df_country_deaths.loc[:,top_10_countries_deaths].plot()


# In[ ]:


df_country_deaths.loc[:,top_10_countries_deaths[1:]].plot()


# # By Region
# Plotting confirmed cases and deaths focusing on top 10 regions.

# In[ ]:


df_region_confirmed = create_region_ts('Confirmed')
df_region_deaths = create_region_ts('Deaths')


# In[ ]:


top_10_regions_confirmed = df_region_confirmed.max().sort_values(ascending=False).index[:10].tolist()
top_10_regions_deaths = df_region_deaths.max().sort_values(ascending=False).index[:10].tolist()


# In[ ]:


df_region_confirmed.loc[:,top_10_regions_confirmed].plot()


# In[ ]:


df_region_confirmed.loc[:,top_10_regions_confirmed[1:]].plot()


# In[ ]:


df_region_deaths.loc[:,top_10_regions_deaths].plot()


# In[ ]:


df_region_deaths.loc[:,top_10_regions_deaths[1:]].plot()


# In[ ]:




