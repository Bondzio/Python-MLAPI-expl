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

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.

#importing additional and useful libreries

import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


# A quick view of the jobs data.

jobs_path = "../input/AIJobsIndustry.csv"
jobs_data = pd.read_csv(jobs_path)

jobs_data.head()


# If we look the company column closely. The values have a little typo at the beginning. So let's remove it.

# In[ ]:


jobs_data['Company'] = jobs_data['Company'].map(lambda x: str(x)[5:])
jobs_data.head()


# In[ ]:


# Finding total number of unique job title in the dataset

total_unique_jobs = jobs_data["JobTitle"].nunique()
print("Total number of jobs titles in all companies:", total_unique_jobs)

# Most offered jobs across all companies
most_common_jobs = jobs_data.groupby(["JobTitle"]).Company.count()
most_common_jobs = most_common_jobs.reset_index(name="Company")
most_common_jobs = most_common_jobs.sort_values(["Company"], ascending=False)
print("\nTop 10 most wanted data science related jobs: ")
most_common_jobs = most_common_jobs.head(20)
most_common_jobs.head(10)


# In[ ]:


# Plotting graph of data science roles

fig, bars=plt.subplots(figsize=(14,7))
bars = sns.barplot(data=most_common_jobs, x="JobTitle", y="Company")
bars.set_xticklabels(most_common_jobs["JobTitle"], rotation=90)
bars.set_xlabel("Job titles", fontsize=25, color="red")
bars.set_ylabel("Number of jobs", fontsize=25, color="red")


# In[ ]:


# Finding companies looking for data science talent.

total_companies = jobs_data["Company"].nunique()
print("Total number of companies offering data science jobs:", total_companies)

# Finding number of jobs per company
companies_with_more_jobs = jobs_data.groupby(["Company"])["JobTitle"].count()
companies_with_more_jobs = companies_with_more_jobs.reset_index(name="JobTitle")
companies_with_more_jobs = companies_with_more_jobs.sort_values(["JobTitle"], ascending=False)
pareto_df = companies_with_more_jobs
companies_with_more_jobs = companies_with_more_jobs.head(20)
print("\nTop 10 companies with more open roles:")
companies_with_more_jobs = companies_with_more_jobs[1:]
companies_with_more_jobs.head(10)


# In[ ]:


fig, bars=plt.subplots(figsize=(14,7))
bars = sns.barplot(data=companies_with_more_jobs, x="Company", y="JobTitle")
bars.set_xticklabels(companies_with_more_jobs["Company"], rotation=90)
bars.set_xlabel("Companies", fontsize=25, color="red")
bars.set_ylabel("Number of jobs", fontsize=25, color="red")


# In[ ]:


# Cities with data science roles

number_of_cities = jobs_data["Location"].nunique()
print("Total number of cities is:", number_of_cities)

cities_with_more_jobs = jobs_data.groupby(["Location"])["JobTitle"].count()
cities_with_more_jobs = cities_with_more_jobs.reset_index(name="JobTitle")
cities_with_more_jobs = cities_with_more_jobs.sort_values(["JobTitle"], ascending=False)
cities_with_more_jobs = cities_with_more_jobs.head(20)
print("\nTop 10 locations with more jobs:")
cities_with_more_jobs.head(10)


# In[ ]:


fig, bars=plt.subplots(figsize=(14,7))
bars = sns.barplot(data=cities_with_more_jobs, x="Location", y="JobTitle")
bars.set_xticklabels(cities_with_more_jobs["Location"], rotation=90)
bars.set_xlabel("Locations", fontsize=25, color="red")
bars.set_ylabel("Number of jobs", fontsize=25, color="red")


# # Conclusions
# 
# We explored the data trying to get insights about the data science job market on earth. And according with the dataset we used, These are some of the conclusions:
# 
# * Data scientist is clearly the most wanted rol by companies. To me, this is because the term "Data scientist" is broadly use to reffered to some that work with data and what that means for a company do not necessary means for the others.
# 
# * Tech giants like Google and Amazon are the ones who have more open roles. Follow by other traditional well known companies.
# 
# * London appears as the city with more available jobs, however data shows us that there are plenty of opportunities accross the globe.
# 
# #### So, there are many and diverse jobs available, great companies are looking for talent and there are opportunities in many locations. My biggest conclusion is that:
# ### It is an exciting time to work in the data science industry!!!
