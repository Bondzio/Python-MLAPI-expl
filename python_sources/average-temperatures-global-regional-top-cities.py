#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Imports, yay!
import numpy as np 
import pandas as pd # 
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


# Read and preview data. Toss data before the year 1900 as there are some inaccurate datapoints from years near 200.
df = pd.read_csv("../input/daily-temperature-of-major-cities/city_temperature.csv")
df = df[df["Year"] > 1900]
df.head()


# # Global Temperature Increase Over Time

# In[ ]:


# Years array from 1995 to 2019
years = np.linspace(1995,2019, endpoint=True, num=25)

# Toss average of 2020 due to being partial year at time of making. df2 will be used for annual average analysis
df2 = df[df["Year"] < 2020]
# Toss temperatures below 10 and above 125
df2 = df2[df2["AvgTemperature"] > 10]
df2 = df2[df2["AvgTemperature"] < 125]

# Group data by year and find mean
means = df2.groupby("Year")["AvgTemperature"].mean()
a = means

# Plot data with average line
plt.figure(figsize=(16,8))
plt.plot(a)
plt.xlabel("Year")
plt.ylabel("Average Global Temperature, Fahrenheit")
plt.title("Average Global Temperatures by Year")
arr = pd.Series(a).array
m, b = np.polyfit(years, arr, 1)
plt.plot(years, m*years + b)
plt.legend(['Average Temperature by Year', 'Average over Time'])


# There is a clear increase in temperature from 1995 to 2019.
# 
# # Now, we will look at monthy averages by month

# In[ ]:


## Combine Year and Month into 1 to get monthly average instead of annual
df2['Date'] = pd.to_datetime(df2[['Year', 'Month']].assign(DAY=1))

# Group data by month and find mean
means = df2.groupby("Date")["AvgTemperature"].mean()
b = means

# Plot data
plt.figure(figsize=(16,8))
plt.plot(b)
plt.xlabel("Year")
plt.ylabel("Average Global Temperature, Fahrenheit")
plt.title("Average Global Temperatures by Month")


# The data is global, so seasons should not be a factor and the monthly average should be smoother. Since the monthly averages was cyclic, I hypothesize much of the data is focused in 1 hemisphere, likely the Northern hemisphere.

# In[ ]:


# Plot data counts by region
df['Region'].value_counts().plot(kind='bar')
plt.title('Regional Distribution of Data')
plt.ylabel('Amount of Entries')


# From this Histogram, we can see that the dataset is focused heavily in North America, which matches our hypothesis. For our average temperature, it makes more sense to view the annual average temperatures instead of monthly averages as seasons in the Northern and Southern hemisphere does not allow a global temperature by month to be reliable. This is also why in the average by year graph, we tossed 2020 as the year was not complete and did not accurately represent the full year's average.

# # Regional Temperature Increase Over Time

# In[ ]:


# Create new dataframe to work with

regions = ['North America', 'Europe', 'Asia', 'Africa', 'South/Central America & Carribean', 'Middle East', 'Australia/South Pacific']

# Loop through each region and plot average temperature
plt.figure(figsize=(15,7.5))
for region in regions:
    temp = df2[df2['Region']== region]
    temp = temp.groupby("Year")["AvgTemperature"].mean()
    a = temp
    plt.plot(a)
    
plt.legend(regions, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.title('Average Annual Temperature by Region')
plt.xlabel('Year')
plt.ylabel('Average Temperature, Fahrenheit')


# It is difficult to see large growth be region, but is can be seen that each region ended higher than it started, by some degree. 

# # Rapid Growth by City
# 
# For consistency, we will mostly analyze annual averages.

# In[ ]:


# Store all cities in array
cities = df2['City'].astype('category').cat.categories.tolist()

# Top n Cities in temperature increase, we will use n=10
n=10
# Placeholder arrays for top cities information
topCities = ['']*n
topDiff = np.zeros(n)

# Loop through for each city
for city in cities:
    # Select only by given city
    temp = df2[df2['City']== city]
    
    # Find mean of given city by year
    temp = temp.groupby("Year")["AvgTemperature"].mean()
    
    # Find difference in temp from starting year to ending year. If the data is incomplete (not from 1995-2019) we will handle it differently. 
    # See comment below how it was handeled differently.
    if temp.size != 25:
        twoDiff = [temp.iloc[-2] - temp.iloc[1], temp.iloc[-1] - temp.iloc[0], temp.iloc[-2] - temp.iloc[0], temp.iloc[-1] - temp.iloc[2]]
        diff = np.amin(twoDiff)
    else:
        diff = temp.iloc[-1] - temp.iloc[0]
    
    # Check if difference is in top n and if change is positive (increase in temp)
    if diff > np.amin(topDiff) and  diff > 0:
        
        # Find index of minimum
        minIndex = np.argmin(topDiff)
        
        # Replace minimum difference with this difference and city name with new top n city
        topDiff[minIndex] = diff
        topCities[minIndex] = city
    


# *Addressing Incomplete Data*
# 
# We will use the minimum of start to end, second year to end, start to second to last year, and second year to second to least year as the incomplete data often time has spikes. Using the minimum of the 4 edge combinations, it reduces our chance of having an incorrect top 10, even if these countries differences are slightly off.

# In[ ]:


plt.figure(figsize=(16,8))
plt.bar(topCities, topDiff)
plt.xlabel('City')
plt.ylabel('Change in Temperature, Fahrenheit')
plt.grid(axis='y')
plt.title('Top 10 Temperature Increase by City')


# In[ ]:


plt.figure(figsize=(16,8))
for top in topCities:
    temp = df2[df2['City'] == top]
    temp = temp.groupby("Year")["AvgTemperature"].mean()
    a=temp
    plt.plot(a)
    
plt.legend(topCities, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.title('Average Annual Temperature by Top 10 Cities: Increasing')
plt.xlabel('Year')
plt.ylabel('Average Temperature, Fahrenheit')


# Here we can see the top 10 increase in temperature in cities. The increase is by about 5 degrees.
# 
# From the graph, Dunsanbe is does not have a large increase in temperature but still made our top 10. We attemped to make a fail-safe to prevent spiked data to make out top 10 (see above), but since it was spiked for multiple years before becoming reliable, it snuck through. A possible solution in the future is to require each year to have a certain number of data-points to average in order to be counted. It is possible that Dunsanbe had few data-points around 1995-2000 that causes the average to not be reliable.

# # Top 10 Decreasing Temperatures in Cities

# In[ ]:


# Top n Cities in temperature increase, we will use n=10
n=10
# Placeholder arrays for top cities information
topCities = ['']*n
topDiff = np.zeros(n)

# Loop through for each city
for city in cities:
    # Select only by given city
    temp = df2[df2['City']== city]

    # Find mean of given city by year
    temp = temp.groupby("Year")["AvgTemperature"].mean()
    
    # Find difference in temp from starting year to ending year. If the data is incomplete (not from 1995-2019) we will handle it differently. 
    # See comment below how it was handeled differently.
    if temp.size != 25:
        twoDiff = [temp.iloc[-2] - temp.iloc[1], temp.iloc[-1] - temp.iloc[0], temp.iloc[-2] - temp.iloc[0], temp.iloc[-1] - temp.iloc[2]]
        diff = np.amax(twoDiff)
    else:
        diff = temp.iloc[-1] - temp.iloc[0]
    
    # Check if difference is in top n and if change is *negative* (decrease in temp)
    if diff < np.amax(topDiff) and  diff < 0:
        
        # Find index of minimum
        maxIndex = np.argmax(topDiff)
        
        # Replace minimum difference with this difference and city name with new top n city
        topDiff[maxIndex] = diff
        topCities[maxIndex] = city
    


# In[ ]:


plt.figure(figsize=(16,8))
plt.bar(topCities, topDiff)
plt.xlabel('City')
plt.ylabel('Change in Temperature, Fahrenheit')
plt.grid(axis='y')
plt.title('Top 10 Temperature Decrease by City')


# In[ ]:


plt.figure(figsize=(16,8))
for top in topCities:
    temp = df2[df2['City'] == top]
    temp = temp.groupby("Year")["AvgTemperature"].mean()
    a=temp
    plt.plot(a)

plt.legend(topCities, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.title('Average Annual Temperature by Top 10 Cities: Decreasing')
plt.xlabel('Year')
plt.ylabel('Average Temperature, Fahrenheit')


# Similar to our top 10 increase, we can see that Bujumbura slipped into our top 10 list along with Islamabad due to inconsistent data. Checking amount of data-points for these years and cities would likely resolve these concerns.

# # Thank you!!
# 
# **This is my first ever notebook on Kaggle!!**
# * If you have any tips, please comment below 
# * If you got any value out of this, please consider upvoting, it would mean a lot 
# 
# Thanks for your time!
