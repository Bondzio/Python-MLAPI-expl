#!/usr/bin/env python
# coding: utf-8

# **How to Query the London Crime Data (BigQuery Dataset)**

# In[ ]:


import bq_helper
from bq_helper import BigQueryHelper
# https://www.kaggle.com/sohier/introduction-to-the-bq-helper-package
london = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="london_crime")


# In[ ]:


bq_assistant = BigQueryHelper("bigquery-public-data", "london_crime")
bq_assistant.list_tables()


# In[ ]:


bq_assistant.head("crime_by_lsoa", num_rows=20)


# In[ ]:


bq_assistant.table_schema("crime_by_lsoa")


# What is the change in the number of crime incidents from 2011 to 2016?
# 
# 
# 

# In[ ]:


query1 = """
SELECT
  borough,
  no_crimes_2011,
  no_crimes_2016,
  no_crimes_2016 - no_crimes_2011 AS change,
  ROUND(((no_crimes_2016 - no_crimes_2011) / no_crimes_2016) * 100, 2) AS perc_change
FROM (
  SELECT
    borough,
    SUM(IF(year=2011, value, NULL)) no_crimes_2011,
    SUM(IF(year=2016, value, NULL)) no_crimes_2016
  FROM
    `bigquery-public-data.london_crime.crime_by_lsoa`
  GROUP BY
    borough )
ORDER BY
  perc_change ASC
;
        """
response1 = london.query_to_pandas_safe(query1)
response1.head(30)


# What were the top 3 crimes per borough in 2016?
# 
# 

# In[ ]:


query2 = """
SELECT
  borough,
  major_category,
  rank_per_borough,
  no_of_incidents
FROM (
  SELECT
    borough,
    major_category,
    RANK() OVER(PARTITION BY borough ORDER BY SUM(value) DESC) AS rank_per_borough,
    SUM(value) AS no_of_incidents
  FROM
    `bigquery-public-data.london_crime.crime_by_lsoa`
  GROUP BY
    borough,
    major_category )
WHERE
  rank_per_borough <= 3
ORDER BY
  borough,
  rank_per_borough;
        """
response2 = london.query_to_pandas_safe(query2)
response2.head(30)


# Credit: Many functions are adapted from https://console.cloud.google.com/marketplace/details/greater-london-authority/london-crime?filter=category:public-safety
