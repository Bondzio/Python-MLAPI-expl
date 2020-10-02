#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.feature_extraction import FeatureHasher


# In[ ]:


aggregated_data = pd.read_csv("../input/raw_aggregated_filter.csv")


# In[ ]:


aggregated_data.head(5)


# In[ ]:


aggregated_data.isnull().sum()


# Replacing nulls with median for coutinous variables 

# In[ ]:


aggregated_data['tolls'].fillna((aggregated_data['tolls'].median()), inplace=True)
aggregated_data['fare'].fillna((aggregated_data['fare'].median()), inplace=True)
aggregated_data['tips'].fillna((aggregated_data['tips'].median()), inplace=True)
aggregated_data['extras'].fillna((aggregated_data['extras'].median()), inplace=True)
aggregated_data['trip_total'].fillna((aggregated_data['trip_total'].median()), inplace=True)


# One hot encoding for categorical variables except for pick_up (and drop_off) census and community

# In[ ]:


dummy = pd.get_dummies(aggregated_data.month_of_year, prefix='Month_flag')
aggregated_data = pd.concat([aggregated_data,dummy], axis = 1)

dummy = pd.get_dummies(aggregated_data.day_of_week, prefix='Day_week_flag')
aggregated_data = pd.concat([aggregated_data,dummy], axis = 1)

dummy = pd.get_dummies(aggregated_data.payment_type, prefix='Card_Type_flag')
aggregated_data = pd.concat([aggregated_data,dummy], axis = 1)


# Hashing company column as number of distinct values is high in it

# In[ ]:


fh = FeatureHasher(n_features=5, input_type='string')
hashed_features = fh.fit_transform(aggregated_data['company'])
hashed_features = hashed_features.toarray()
aggregated_data=pd.concat([aggregated_data, pd.DataFrame(hashed_features,columns=['hasha', 'hashb', 'hashc','hashd','hashe'])], axis=1)


# In[ ]:


import os
os.chdir("/kaggle/working/")
aggregated_data.to_csv('feature_engineered_data.csv',index=False)


# Univariate Analysis

# Checking the distribution of taxi usage though the week

# In[ ]:


# Day_of_week has Sunday as 1, Monday as 2 ... and Saturday as 7
sns.countplot(aggregated_data.day_of_week)
plt.show()


# The usage of taxi is the highest during the weekends and least on Monday with subsequent increase as the week progress.
# This behaviour shows that people go out more over the weekends and take lesser taxis to go to their respective work place.

# Checking the taxi usage through different months

# In[ ]:


sns.countplot(aggregated_data.month_of_year)
plt.show()


# The taxi usage is highest in the month of June and not during the holiday season (December and January)

# Trip distance

# In[ ]:


plt.figure(figsize = (20,5))
sns.boxplot(aggregated_data.trip_miles)
plt.show()


# As we can see from the above plot there as trips that go beyond 700 miles, but since we have already applied the speed filters these trips may be outstation trips

# Fare distribution

# In[ ]:


plt.figure(figsize = (20,5))
sns.boxplot(aggregated_data.fare)
plt.show()


# In[ ]:


aggregated_data.fare.groupby(pd.cut(aggregated_data.fare, np.arange(1,max(aggregated_data.fare),100))).count()


# We are observing very high fare in range of over 9000 dollars.
# To get more insights checking trip distance and related fields to these fares.

# In[ ]:


aggregated_data.loc[(aggregated_data.fare > 1000) & (aggregated_data.company !="Unspecified"), ['fare','trip_miles','trip_seconds']].head(5)


# Removing all the records which has fare over 500 dollars as they are outliers and chicago is one of the cheapest place to travel in taxi with around 12 dollars fare for 5 Miles with 5 Minutes waiting time.
# Also, the fare for max miles rode is 314 dollars.
# Refrence: https://www.world-airport-codes.com/united-states/chicago/chicago-ohare-international/taxis.html

# In[ ]:


aggregated_data = aggregated_data[aggregated_data.fare <= 500]


# Analyzing trip_seconds

# In[ ]:


aggregated_data.trip_seconds.describe()


# In[ ]:


plt.figure(figsize = (20,5))
sns.boxplot(aggregated_data.trip_seconds)
plt.show()


# Some trip durations are over 80000 seconds which is close to 24 hours and can point towards a weekend out of town trip.

# In[ ]:


aggregated_data.trip_seconds.groupby(pd.cut(aggregated_data.trip_seconds, np.arange(1,max(aggregated_data.trip_seconds),3600))).count()


# The distribution depicts that the distrbution of response variable is right skewed

# In[ ]:


aggregated_data.trip_seconds.groupby(pd.cut(aggregated_data.trip_seconds, np.arange(1,7200,600))).count().plot(kind='barh')
plt.xlabel('Trip Counts')
plt.ylabel('Trip Duration (seconds)')
plt.show()


# Most of the trips took 0 - 30 mins to complete i.e. approx 1800 secs

# Bi-Variate Analysis

# Trip Seconds per hour

# In[ ]:


group1 = aggregated_data.groupby('peak_hours_flag').trip_seconds.mean().plot(kind='barh')
plt.ylabel('Trip Duration (seconds)')
plt.xlabel('Pickup Hour')
plt.show()


# This clearly depicts that average trip duration is higher for peak hours than non-peak hours.

# Trip Seconds per weekday

# In[ ]:


group2 = aggregated_data.groupby('day_of_week').trip_seconds.mean()
sns.pointplot(group2.index, group2.values)
plt.ylabel('Trip Duration (seconds)')
plt.xlabel('Weekday')
plt.show()


# We can clearly see that the trip duration is varying between weekdays and weekends.

# Trip Seconds per Month

# In[ ]:


group2 = aggregated_data.groupby('month_of_year').trip_seconds.mean()
sns.pointplot(group2.index, group2.values)
plt.ylabel('Trip Duration (seconds)')
plt.xlabel('Month')
plt.show()


# Trip Seconds per payment type

# In[ ]:


group2 = aggregated_data.groupby('payment_type').trip_seconds.mean()
sns.pointplot(group2.index, group2.values)
plt.ylabel('Trip Duration (seconds)')
plt.xlabel('payment_type')
plt.show()


# The average duration within different payment methods only vary within a range of 350 seconds.

# Feature Selecion

# In[ ]:


#First chech the index of the features and label
#list(zip( range(0,len(aggregated_data.columns)),aggregated_data.columns))


# In[ ]:


#index=['peak_hours_flag','day_hours_flag','night_hours_flag','pickup_census_tract','dropoff_census_tract','pickup_community_area','dropoff_community_area',
      #'tolls','fare','tips','extras','trip_total','trip_miles','Month_flag_1','Month_flag_2','Month_flag_3','Month_flag_4','Month_flag_5','Month_flag_6','Month_flag_7','Month_flag_8','Month_flag_9','Month_flag_10',
       #'Month_flag_11','Month_flag_12','Day_week_flag_1','Day_week_flag_2','Day_week_flag_3','Day_week_flag_4','Day_week_flag_5','Day_week_flag_6','Day_week_flag_7','Card_Type_flag_Cash','Card_Type_flag_Credit Card',
       #'Card_Type_flag_Dispute','Card_Type_flag_Mobile','Card_Type_flag_No Charge','Card_Type_flag_Pcard','Card_Type_flag_Prcard','Card_Type_flag_Prepaid','Card_Type_flag_Split','Card_Type_flag_Unknown',
       #'Card_Type_flag_Way2ride','hasha', 'hashb', 'hashc','hashd','hashe']
#X = aggregated_data[index].values
#Y = aggregated_data.iloc[:,17].values

