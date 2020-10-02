#!/usr/bin/env python
# coding: utf-8

# ## Introduction ##
# 
# This notebook will be taking a look on the Cheltenham Crime Data Notebook.  Does the time or day matter when it comes to crime.  Do certain types of crime happen at certain hours?  Let's drill down into some of the other data and how it relates to overall crime. 

# In[ ]:


# This portion of code is boilerplate from the Cheltenham Crime Data Notebook
# This is a simple dataset.  
# When reading in the data, the only area that may requires 
# special attention is the date format.  You may want to use %m/%d/%Y %I:%M:00 %p format.
import pandas as pd
import numpy as np
import scipy as sci
import datetime


import warnings
warnings.filterwarnings("ignore")
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="white", color_codes=True)


dateparse = lambda x: datetime.datetime.strptime(x,'%m/%d/%Y %I:%M:00 %p')

# Read data 
d=pd.read_csv("../input/crime.csv",parse_dates=['incident_datetime'],date_parser=dateparse)
d
# Display data that we retrieve from the CSV file


# Does day of the week matter when it comes to crime?

# In[ ]:





# In[ ]:


days_of_the_week=pd.value_counts(d['day_of_week'])
days_of_the_week.plot(kind="bar")
_=plt.xlabel('Day of the Week')
_=plt.ylabel('How many crimes?')
plt.show()


# Criminals are TGIFing all over the place!

# Does the time of day matter when it comes to crime?

# In[ ]:


time_of_day=pd.value_counts(d['hour_of_day'], sort=False)
time_of_day.sort_index(inplace=True)
time_of_day.plot(kind='bar')
_=plt.xlabel('Hour of the day')
_=plt.ylabel('How many crimes?')
plt.show()


# Crime doesn't stay up late?

# Since traffic crime is the most prevalent, lets remove that from the dataset and see if the days of the week charts and time of day charts look any different

# In[ ]:


no_traffic=d.loc[d['parent_incident_type']!='Traffic']
days_of_the_week_2=pd.value_counts(no_traffic['day_of_week'])
_=days_of_the_week_2.plot(kind="bar", color='red', alpha=.35)
_=days_of_the_week.plot(kind='bar', color='blue', alpha=.25)
_=plt.xlabel('Day of the Week')
_=plt.ylabel('Number of Crimes')
_=plt.legend(['No Traffic', 'All Crimes'])
plt.show()


# In[ ]:


time_of_day_2=pd.value_counts(no_traffic['hour_of_day'], sort=False)
time_of_day_2.sort_index(inplace=True)
_=time_of_day_2.plot(kind='bar', color='red', alpha=.35)
_=time_of_day.plot(kind='bar', color='blue', alpha=.25)
_=plt.xlabel('Hour of the day')
_=plt.ylabel('Number of Crimes')
_=plt.legend(['No Traffic', 'All Crime'])
plt.show()


# Interestingly, the shape of the time of day chart looks almost the same!
# 
# Let's start breaking down the crime by the time of day.  Do we notice any immediate patterns?

# In[ ]:


crime_list=d['parent_incident_type'].unique()
for i in range(len(crime_list)):
    temp_crime=d.loc[d['parent_incident_type']==crime_list[i]]
    time_crime=pd.value_counts(temp_crime['hour_of_day'])
    time_crime.sort_index(inplace=True)
    time_crime.plot(kind='bar', color='blue', alpha=.6)
    plt.xlabel(crime_list[i] + ' During Hour')
    plt.ylabel('Number of occurances')
    plt.show()
    plt.figure()
    


# Early afternoon until midnight seems like a busy time for the police

# What are the bad parts of town, how much do they contribute to the overall crime level?

# In[ ]:


addresses=pd.value_counts(d['address_1'], sort=True)
top_20_add=addresses[0:20]
top_20_add.plot(kind='bar')
_=plt.xlabel('The top 20 addresses account for ' + str(int(100*np.sum(top_20_add)/len(d))) + '% of all crime')
_=plt.ylabel('Number of incidences')
plt.show()


# How much of the chart above is just traffic?
# 

# In[ ]:


addresses=pd.value_counts(d['address_1'], sort=True)
top_20_add=addresses[0:20]
address_traffic=d.loc[d['parent_incident_type']=='Traffic']
address_traffic_count=pd.value_counts(address_traffic['address_1'], sort=True)
top_20_add_traffic=address_traffic_count[0:20]
top_20_add_traffic.plot(kind='bar', color='red', alpha=.9)
top_20_add.plot(kind='bar', color='blue', alpha=.50)
_=plt.xlabel('The top 20 addresses account for ' + str(int(100*np.sum(top_20_add)/len(d))) + '% of all crime')
_=plt.ylabel('Number of incidences')
_=plt.legend(['Traffic only', 'All Crime'])
plt.show()


# Looks like the majority of crime at those top 20 addresses are not Traffic related

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




