#!/usr/bin/env python
# coding: utf-8

# Introductory analysis to Zika virus dataset

# In[ ]:


import numpy as np # linear algebra



import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)



import matplotlib.pyplot as plt



import seaborn as sbn



get_ipython().run_line_magic('matplotlib', 'inline')







from subprocess import check_output



print(check_output(["ls", "../input"]).decode("utf8"))


# In[ ]:


df = pd.read_csv("../input/cdc_zika.csv",parse_dates=['report_date'],



                 infer_datetime_format=True,



                 index_col=0)



df.head(3)


# In[ ]:


df.location.value_counts()[:30].plot(kind='bar', figsize=(12, 7))

plt.title("Number of locations reported - Top 30")


# In[ ]:


df[df.data_field == "confirmed_male"].value.plot()

df[df.data_field == "confirmed_female"].value.plot().legend(("Male","Female"),loc="best")

plt.title("Confirmed Male vs Female cases")


# In[ ]:


age_groups = ('confirmed_age_under_1', 'confirmed_age_1-4',
       'confirmed_age_5-9', 'confirmed_age_10-14', 'confirmed_age_15-19',
       'confirmed_age_20-24', 'confirmed_age_25-34', 'confirmed_age_35-49',
       'confirmed_age_50-59', 'confirmed_age_60-64',
       'confirmed_age_60_plus')

for i,age_group in enumerate(age_groups):
    print (age_group)
    print (df[df.data_field==age_group].value)
    print ("")


# Looking at the confirmed cases based on age group doesn't show us anything useful other than the fact the categorical report of cases based on age group does not contain enough data and the report was done at single place on a single date :/
# 
# Though looking closely in the reported data we see the number of confirmed cases is more in the working age group (20 - 60) with peak in 35-49 ages

# In[ ]:


symptoms = ['confirmed_fever',
       'confirmed_acute_fever', 'confirmed_arthralgia',
       'confirmed_arthritis', 'confirmed_rash', 'confirmed_conjunctivitis',
       'confirmed_eyepain', 'confirmed_headache', 'confirmed_malaise']
fig = plt.figure(figsize=(13,13))
for symptom in symptoms:
    df[df.data_field == symptom].value.plot()
plt.legend(symptoms, loc='best')
plt.title('Understanding symptoms of zika virus')

