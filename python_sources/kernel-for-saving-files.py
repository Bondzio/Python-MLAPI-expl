#!/usr/bin/env python
# coding: utf-8

# # Kernel for saving files 

# In[ ]:



import os
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import json
import time
import warnings

#from pycountry_convert import ( map_countries, country_name_to_country_alpha3,)
import pytz as pytz
import datetime

#Plotting
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')

#Sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold

#lgm and graph viz
import graphviz 
import lightgbm as lgb

warnings.filterwarnings('ignore')


# In[ ]:


os.listdir('../input')


# In[ ]:


def load_df(csv_path='../input/train.csv', nrows=None):
    JSON_COLUMNS = ['device', 'geoNetwork', 'totals', 'trafficSource']
      
    df = pd.read_csv(csv_path, 
                     converters={column: json.loads for column in JSON_COLUMNS}, 
                     dtype={'fullVisitorId': 'str', 'visitId':'str', 'visitStartTime':'str', 'date':'str'}, 
                     nrows=nrows)

    #Normalize JSON colunmns and drop
    for column in JSON_COLUMNS:
        column_as_df = json_normalize(df[column])
        column_as_df.columns = [f"{column}.{subcolumn}" for subcolumn in column_as_df.columns]
        df = df.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)
    return df


def drop_constant_cols(df):
    ## Drop constant columns
    const_cols = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
    df.drop(const_cols, axis=1, inplace=True)
    
    #this columnm is only in train data
    try:
        df.drop('trafficSource.campaignCode', axis=1, inplace=True)   
    except:
        None   
    


# In[ ]:


get_ipython().run_cell_magic('time', '', "#Load\ntrain_df = load_df(csv_path='../input/ga-customer-revenue-prediction/train.csv', nrows = None)\ndrop_constant_cols(train_df)\n\ntest_df = load_df(csv_path='../input/ga-customer-revenue-prediction/test.csv', nrows = None)\ndrop_constant_cols(test_df)")


# In[ ]:


# Extract target values and Ids
cat_cols = ['channelGrouping','device.browser',
       'device.deviceCategory', 'device.isMobile', 'device.operatingSystem',
       'geoNetwork.city', 'geoNetwork.continent', 'geoNetwork.country',
       'geoNetwork.metro', 'geoNetwork.networkDomain', 'geoNetwork.region',
       'geoNetwork.subContinent','trafficSource.adContent',
       'trafficSource.adwordsClickInfo.adNetworkType',
       'trafficSource.adwordsClickInfo.gclId',
       'trafficSource.adwordsClickInfo.isVideoAd',
       'trafficSource.adwordsClickInfo.page',
       'trafficSource.adwordsClickInfo.slot', 'trafficSource.campaign',
       'trafficSource.isTrueDirect', 'trafficSource.keyword',
       'trafficSource.medium', 'trafficSource.referralPath',
       'trafficSource.source'  ]


num_cols = ['visitNumber', 'totals.bounces', 'totals.hits',
            'totals.newVisits', 'totals.pageviews', 
            '_local_hourofday'  ]

interaction_cols = ['totals.hits / totals.pageviews', 'totals.hits * totals.pageviews',
       'totals.hits - totals.pageviews']

visitStartTime = ['visitStartTime']

time_cols = ['_dayofweek', '_monthofyear', '_dayofyear']

ID_cols = ['date', 'fullVisitorId', 'sessionId', 'visitId']

target_col = ['totals.transactionRevenue']


# In[ ]:


#Load
geocode_df= pd.read_csv('../input/geocoded-data/geocodes_timezones.csv')

def time_zone_converter(x):
    
    try:
        return pytz.country_timezones(x)[0]
    except AttributeError:
        return np.nan
   

def time_localizer(s):
    #format of series [time,zone]
    try:
        tz =pytz.timezone(s[1])
        return pytz.utc.localize(s[0], is_dst=None).astimezone(tz)
    except:
        return np.nan
    
def remove_missing_vals(x):
    remove_list = ['(not set)', 'not available in demo dataset','unknown.unknown']
    if x in remove_list:
        return ''
    else:
        return x 
    
def map_timezone(x):   
    try:
        return timezone_dict[x]
    except KeyError:
        return 'UTC'


# In[ ]:


get_ipython().run_cell_magic('time', '', "train_df['visitStartTime'] = pd.to_datetime(train_df['visitStartTime'], unit = 's')\ntest_df['visitStartTime'] = pd.to_datetime(test_df['visitStartTime'], unit = 's')\n\n#Generate foreign key '_search_term' by concatenating city, region, country\ntrain_df['_search_term'] = train_df['geoNetwork.city'].map(remove_missing_vals) + ' ' + train_df['geoNetwork.region'].map(remove_missing_vals) + ' ' + train_df['geoNetwork.country'].map(remove_missing_vals)\ntest_df['_search_term'] = test_df['geoNetwork.city'].map(remove_missing_vals) + ' ' + test_df['geoNetwork.region'].map(remove_missing_vals) + ' ' + test_df['geoNetwork.country'].map(remove_missing_vals)\n\n#Set global variable, needed for map_timezone function\nglobal timezone_dict\ntimezone_dict = dict(zip(geocode_df['search_term'], geocode_df['timeZoneId']))\n\n#Map timezones\ntrain_df['_timeZoneId'] = train_df['_search_term'].map(map_timezone)\ntest_df['_timeZoneId'] = test_df['_search_term'].map(map_timezone)\n  \n#Create time zone aware column\ntrain_df['_local_time'] = train_df[['visitStartTime', '_timeZoneId']].apply(time_localizer, axis = 1).astype(str)\ntest_df['_local_time'] = test_df[['visitStartTime', '_timeZoneId']].apply(time_localizer, axis = 1).astype(str)  \n\n#Localize hour time\ntrain_df['_local_hourofday'] = train_df['_local_time'].str[11:13]\ntest_df['_local_hourofday'] = test_df['_local_time'].str[11:13]\n")


# ## Time since last visit 

# In[ ]:


get_ipython().run_cell_magic('time', '', "train_df['_time_since_last_visit'] = train_df[['fullVisitorId','visitStartTime']].groupby('fullVisitorId')['visitStartTime'].diff()\ntest_df['_time_since_last_visit'] = test_df[['fullVisitorId','visitStartTime']].groupby('fullVisitorId')['visitStartTime'].diff()\n\n#Replace 0 with very large number, as we are interested in small / medium values\ntrain_df['_time_since_last_visit'] = train_df['_time_since_last_visit'].fillna(999999999)\ntest_df['_time_since_last_visit'] = test_df['_time_since_last_visit'].fillna(999999999)\n\n#Convert to numeric\ntrain_df['_time_since_last_visit'] = pd.to_numeric(train_df['_time_since_last_visit'])\ntest_df['_time_since_last_visit'] = pd.to_numeric(test_df['_time_since_last_visit'])")


# In[ ]:





# ## Label encoding 

# In[ ]:


get_ipython().run_cell_magic('time', '', "#Categorical encoding\nfor c in cat_cols:\n    #Convert NAs to unknown\n    train_df[c] = train_df[c].fillna('unknown')\n    test_df[c] = test_df[c].fillna('unknown')\n    \n    #Encode\n    lbl = LabelEncoder()\n    lbl.fit( list(train_df[c].values.astype('str')) + list(test_df[c].values.astype('str')))\n    train_df[c] = lbl.transform(list(train_df[c].values.astype('str')))\n    test_df[c] = lbl.transform(list(test_df[c].values.astype('str')))\n")


# In[ ]:


train_df.to_pickle('train_flat_local_cat_enc.pkl')
test_df.to_pickle('test_flat_local_cat_enc.pkl')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




