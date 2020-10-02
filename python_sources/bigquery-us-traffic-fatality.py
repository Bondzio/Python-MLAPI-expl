#!/usr/bin/env python
# coding: utf-8

# ## Environment Setup and Overview

# In[ ]:


# import package with helper functions 
import bq_helper

# create a helper object for this dataset
accidents = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="nhtsa_traffic_fatalities")


# In[ ]:


# preview data set
accidents.head("accident_2015")


# **Which day of the week do most fatal traffic accidents happen on?**

# In[ ]:


query = """
        SELECT COUNT(consecutive_number) as AccCount, EXTRACT(DAYOFWEEK FROM timestamp_of_crash) as DOW
        FROM `bigquery-public-data.nhtsa_traffic_fatalities.accident_2015`
        GROUP BY DOW
        ORDER BY AccCount DESC
        """
accidents_by_day = accidents.query_to_pandas_safe(query)
accidents_by_day


# In[ ]:


# library for plotting
import matplotlib.pyplot as plt

# make a plot to show that our data is, actually, sorted:
plt.plot(accidents_by_day.AccCount)
plt.title("Number of Accidents per Day \n (Ranked most to least dangerous)")


# ## SQL Scavenger Hunt: Day 3 Task

# **1. At which hours of the day do most accidents occur?**

# In[ ]:


query = """
        SELECT EXTRACT(HOUR FROM timestamp_of_crash) as HOD,
            COUNT(consecutive_number) as AccCount
        FROM `bigquery-public-data.nhtsa_traffic_fatalities.accident_2015`
        GROUP BY HOD
        ORDER BY AccCount DESC        
        """
accidents_by_hour = accidents.query_to_pandas_safe(query)
accidents_by_hour


# In[ ]:


# make a plot to show that our data is, actually, sorted:
plt.plot(accidents_by_hour.AccCount)
plt.title("Number of Accidents per Hour \n (Ranked most to least dangerous)")


# **2. Which state has the most hit and runs?**

# In[ ]:


# explore the vehicles table
accidents.head("vehicle_2015")


# In[ ]:


query = """
        SELECT registration_state_name as State, hit_and_run as HnR, count(hit_and_run) as HnR_count
        FROM `bigquery-public-data.nhtsa_traffic_fatalities.vehicle_2015`
        GROUP BY State, HnR
        HAVING HnR = 'Yes'
        ORDER BY HnR_count DESC
        """
hit_and_run_count = accidents.query_to_pandas_safe(query)
hit_and_run_count


# Based on the table above, California state had the highest hit-and-run accidents during the year 2015.
