#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import package with helper functions 
import bq_helper

# create a helper object for this dataset
open_aq = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="openaq")

# print all the tables in this dataset (there's only one!)
open_aq.list_tables()


# # Scavenger hunt
# ___
# 
# * Which countries use a unit other than ppm to measure any type of pollution? (Hint: to get rows where the value *isn't* something, use "!=")
# * Which pollutants have a value of exactly 0?

# In[ ]:


query1 = """
SELECT DISTINCT(country) AS Countries
FROM `bigquery-public-data.openaq.global_air_quality`
WHERE unit !='ppm'
"""

query2 = """
SELECT DISTINCT(pollutant) AS Nonexisting_pollutants
FROM `bigquery-public-data.openaq.global_air_quality`
WHERE value = 0
"""

distinct_countries = open_aq.query_to_pandas_safe(query1)
Nonexisting_pollutants = open_aq.query_to_pandas_safe(query2)

print("Countries",distinct_countries['Countries'].tolist())
print("pollutants with zero value",Nonexisting_pollutants['Nonexisting_pollutants'].tolist())





