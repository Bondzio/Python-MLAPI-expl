#!/usr/bin/env python
# coding: utf-8

# In[2]:


import math
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)


from wordcloud import WordCloud, STOPWORDS

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np # linear algebra
import matplotlib 
import matplotlib.pyplot as plt
import sklearn
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt 
plt.rcParams["figure.figsize"] = [16, 12]
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory


# In[3]:


#BigQuery Tablebigquery-public-data.world_bank_health_population.country_summary

# import package with helper functions 
import bq_helper

# create a helper object for this dataset
world_bank_health_population = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="world_bank_health_population")

# print all the tables in this dataset (there's only one!)
world_bank_health_population.list_tables()


# In[4]:


world_bank_health_population.table_schema('country_summary')


# In[5]:


query = """SELECT currency_unit, count(country_code) as count 
            FROM `bigquery-public-data.world_bank_health_population.country_summary` 
            GROUP BY currency_unit
            ORDER BY count DESC
            
            """  

res = world_bank_health_population.query_to_pandas_safe(query)


# In[6]:


res


# In[9]:


query = """SELECT country_code, short_name, long_name, table_name  
            FROM `bigquery-public-data.world_bank_health_population.country_summary` 
            WHERE currency_unit = 'Danish krone'
            """  

res = world_bank_health_population.query_to_pandas_safe(query)


# In[10]:


res


# In[11]:


query = """SELECT country_code, short_name, long_name, table_name  
            FROM `bigquery-public-data.world_bank_health_population.country_summary` 
            WHERE currency_unit = 'Australian dollar'
            """  

res = world_bank_health_population.query_to_pandas_safe(query)


# In[12]:


res


# In[15]:


query = """SELECT * 
            FROM `bigquery-public-data.world_bank_health_population.country_summary` 
            WHERE country_code = 'GRL'
            """  

res = world_bank_health_population.query_to_pandas_safe(query)


# In[16]:


res


# In[ ]:




