#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import bq_helper # It has functions for putting BigQuery results in Pandas DataFrames

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


# create a helper object for our bigquery dataset
hacker_news = bq_helper.BigQueryHelper(active_project= "bigquery-public-data", 
                                       dataset_name = "hacker_news")


# In[ ]:


# print a list of all the tables in the hacker_news dataset
hacker_news.list_tables()


# In[ ]:


# print information on all the columns in the "full" table
# in the hacker_news dataset
hacker_news.table_schema("full")


# In[ ]:


hacker_news.head('full')


# In[ ]:


# preview the first ten entries in the by column of the full table
hacker_news.head("full", selected_columns="by", num_rows=10)


# In[ ]:


# preview the first ten entries in the by column of the full table
hacker_news.head("full", selected_columns=['by', 'text'], num_rows=10)


# **What's a query?** 
# 
# A query is small piece of SQL code that specifies what data would you like to scan from a databases, and how much of that data you would like returned

# Check the size of your query before you run it

# In[ ]:


# this query looks in the full table in the hacker_news
# dataset, then gets the score column from every row where 
# the type column has "job" in it.
query = """SELECT score
            FROM `bigquery-public-data.hacker_news.full`
            WHERE type = "job" """

# check how big this query will be
hacker_news.estimate_query_size(query)


# Run the Query
# 
# Now that we know how to check the size of the query (and make sure we're not scanning several terabytes of data!) we're ready to run our first query. You have two methods available to help you do this:
# 
# * BigQueryHelper.query_to_pandas(query): This method takes a query and returns a Pandas dataframe.
# * BigQueryHelper.query_to_pandas_safe(query, max_gb_scanned=1): This method takes a query and returns a Pandas dataframe only if the size of the query is less than the upperSizeLimit (1 gigabyte by default).
# Here's an example of a query that is larger than the specified upper limit.

# In[ ]:


hacker_news.query_to_pandas_safe(query, max_gb_scanned=0.1) # convert 0.1 into 1 for example  


# In[ ]:


# check out the scores of job postings (if the 
# query is smaller than 1 gig)
job_post_scores = hacker_news.query_to_pandas_safe(query)


# In[ ]:


job_post_scores.score.mean()

