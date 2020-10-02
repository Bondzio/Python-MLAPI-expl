#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Offical google cloud library
from google.cloud import bigquery
import pandas as pd
import base64
from IPython.display import HTML
from IPython.display import FileLinks


# In[ ]:


# Initiate bigquery client
bq = bigquery.Client()


# In[ ]:


# Get the first table
query = """
SELECT
    *
FROM
    `bigquery-public-data.google_analytics_sample.ga_sessions_20160801`
"""


# In[ ]:


# Create the query and convert to dataframe
result = bq.query(query).to_dataframe()


# In[ ]:


# View result
result


# In[ ]:


# Converting the first 100 rows to csv
# FileLinks allow downloading of heavy files
result.head(100).to_csv ('export_dataframe.csv', index = None, header=True)
FileLinks('.')

