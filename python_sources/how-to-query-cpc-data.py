#!/usr/bin/env python
# coding: utf-8

# # How to Query Cooperative Patent Classification Data (BigQuery)
# [Click here](https://www.kaggle.com/mrisdal/safely-analyzing-github-projects-popular-licenses) for a detailed notebook demonstrating how to use the bq_helper module and best practises for interacting with BigQuery datasets.

# In[ ]:


# Start by importing the bq_helper module and calling on the specific active_project and dataset_name for the BigQuery dataset.
import bq_helper
from bq_helper import BigQueryHelper
# https://www.kaggle.com/sohier/introduction-to-the-bq-helper-package

cpc = bq_helper.BigQueryHelper(active_project="patents-public-data",
                                   dataset_name="cpc")


# In[ ]:


# View table names under the cpc data table
bq_assistant = BigQueryHelper("patents-public-data", "cpc")
bq_assistant.list_tables()


# In[ ]:


# View the first three rows of the definitions data table
bq_assistant.head("definitions", num_rows=3)


# In[ ]:


# View information on all columns in the definitions data table
bq_assistant.table_schema("definitions")


# ## Example SQL Query
# What kinds of levels are there for describing patent classifications? What is the range?

# In[ ]:


query1 = """
SELECT DISTINCT
  level
FROM
  `patents-public-data.cpc.definitions`
LIMIT
  20;
        """
response1 = cpc.query_to_pandas_safe(query1)
response1.head(20)


# ## Importance of Knowing Your Query Sizes
# 
# It is important to understand how much data is being scanned in each query due to the free 5TB per month quota. For example, if a query is formed that scans all of the data in a particular column, given how large BigQuery datasets are it wouldn't be too surprising if it burns through a large chunk of that monthly quota!
# 
# Fortunately, the bq_helper module gives us tools to very easily estimate the size of our queries before running a query. Start by drafting up a query using BigQuery's Standard SQL syntax. Next, call the estimate_query_size function which will return the size of the query in GB. That way you can get a sense of how much data is being scanned before actually running your query.

# In[ ]:


bq_assistant.estimate_query_size(query1) 


# Interpretting this number, this means my query scanned about ~0.0019 GB (or 1.9 MB) of data in order to return a table of 20 unique levels in the dataset.
