#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
print ("ready")


# In[ ]:


from google.cloud import bigquery
from bq_helper import BigQueryHelper
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


# # How to get data

# In[ ]:



# Create a "Client" object
client = bigquery.Client()

# Construct a reference to the "openaq" dataset
dataset_ref = client.dataset("openaq", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# List all the tables in the "openaq" dataset
tables = list(client.list_tables(dataset))

# Print names of all tables in the dataset (there's only one!)
for table in tables:  
    print(table.table_id)


# In[ ]:


# Construct a reference to the "global_air_quality" table
table_ref = dataset_ref.table("global_air_quality")

# API request - fetch the table
table = client.get_table(table_ref)

# Preview the first five lines of the "global_air_quality" table
client.list_rows(table, max_results=5).to_dataframe()


# * https://openaq.org/
# * Country is given with ISO code (i.g. Algery == DZ , Italy == IT)

# In[ ]:


query = """
        SELECT city
        FROM `bigquery-public-data.openaq.global_air_quality`
        WHERE country = 'IT'
        """
client = bigquery.Client()
# Set up the query
query_job = client.query(query)
# API request - run the query, and return a pandas DataFrame
cities = query_job.to_dataframe()
# What five cities have the most measurements?
cities.city.value_counts().head()


# # Analysis
# 
# * only so2
# 
# Inhaling sulfur dioxide causes irritation to the nose, eyes, throat, and lungs. Typical symptoms include sore throat, runny nose, burning eyes, and cough. Inhaling high levels can cause swollen lungs and difficulty breathing. Skin contact with sulfur dioxide vapor can cause irritation or burns.

# In[ ]:


query = """
        SELECT *
        FROM `bigquery-public-data.openaq.global_air_quality` 
        WHERE 
            timestamp > "1990-01-01" 
            AND country = "US"
        
        
        """


# In[ ]:


# AND country = "US"
# AND pollutant = "so2" 
# ORDER BY value DESC
# LIMIT 10000
# `bigquery-public-data.openaq.global_air_quality`


# * The quick way to execute this query is to use the bq_helper library: https://github.com/SohierDane/BigQuery_Helper

# In[ ]:


bq_assistant = BigQueryHelper('bigquery-public-data', 'openaq')

df = bq_assistant.query_to_pandas(query)
df.head()


# In[ ]:


plt.figure(figsize=(15,8))
sns.scatterplot(x = df["longitude"],y = df["latitude"], size = df["value"] , hue = df["value"], sizes=(40, 400))


# In[ ]:


df["pollutant"].unique()


# ## Time series

# In[ ]:


df = df.sort_values("timestamp")
df = df.set_index("timestamp")
df["value"].plot(figsize = (20,10))


# In[ ]:





# In[ ]:





# In[ ]:




