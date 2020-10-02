#!/usr/bin/env python
# coding: utf-8

# Hi All!
# Thanks for checking this out :) 
# 
# This is my first stab on the data. According to what I have observed:
# 
#  - The most common call type is "Medical Incidents".
#  - The top three neighborhoods in terms of SFFD calls are "Tenderloin", "South of Market" and "Mission".
#  - As the elevation increases the call number declines
#  - Calls from higher elevations are responded in a comparably shorter time
#  - At noon there is a dramatic drop in the number of calls
#  - Surprisingly before 2008 calls were coming from relavently higher elevations

# # Import the Dependencies

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import mpl_toolkits
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')


# ## Lets read the data and take a look at the fields

# In[ ]:


fdc_data_before_2009 = pd.read_csv("../input/SF_FDplusElev_data_before_2009.csv")
fdc_data_after_2009 = pd.read_csv("../input/SF_FDplusElev_data_before_2009.csv")
fdc_data = pd.concat([fdc_data_before_2009, fdc_data_after_2009])
fdc_data.head()


# # How does the SFFD call numbers vary according to the elevation?
# 
# It seems like as the elevation increases the call number declines

# In[ ]:


ranges = list(np.arange(-10,260,10))
incidences_per_elevation = pd.DataFrame(fdc_data.groupby(pd.cut(fdc_data.elevation, ranges)).count()["elevation"])
incidences_per_elevation.columns = ["count"]
ax = incidences_per_elevation.plot.bar(figsize=(8,6), fontsize = 12, legend = False, color = "palegreen")#counts per elevation
ax.set_xlabel("Elevation Bins", fontsize = 16)
ax.set_ylabel("Count of Fire Department Calls", fontsize = 16)
ax.set_title("Count of Fire Department Calls per Elevation Bin", fontsize = 20)


# In[ ]:


def delta_time(col1,col2):
    timediff = []
    for i in range(0, len(col1)):
        t1 = datetime.strptime(col1[i], '%m/%d/%Y %H:%M:%S %p') 
        t2 = datetime.strptime(col2[i], '%m/%d/%Y %H:%M:%S %p')
        timediff.append((t2-t1).total_seconds())
    return timediff


# # Response time has a declining trend as the elevation increases except the peak at elevations between 140 and 150

# In[ ]:


time_diff_fdc_data = fdc_data[['Received DtTm','Response DtTm', "elevation"]]
time_diff_fdc_data.dropna(inplace = True)
time_diff_column = delta_time(time_diff_fdc_data['Received DtTm'].tolist(),time_diff_fdc_data['Response DtTm'].tolist())
time_diff_fdc_data["Response Time"] = time_diff_column
ranges = list(np.arange(-10,260,10))
response_time_per_elevation = pd.DataFrame(time_diff_fdc_data.groupby(pd.cut(time_diff_fdc_data.elevation, ranges)).mean()["Response Time"])


# In[ ]:


response_time_per_elevation["elevation"] = response_time_per_elevation.index
plt.figure(figsize=(8,5))
ax1 = sns.set_style("whitegrid")
ax1 = sns.set(font_scale=1.3)
ax1 = sns.stripplot(x ="elevation", y = "Response Time", data = response_time_per_elevation, size = 8)
ax1 = plt.xticks(rotation=90)


# In[ ]:


def get_day_time(col, days, hours, months, years):
    for token in col:
        day = int(token.split()[0].split("/")[1])
        month = int(token.split()[0].split("/")[0])
        year = int(token.split()[0].split("/")[2])
        hour = int(token.split()[1].split(":")[0])
        am_pm = token.split()[2]
        if am_pm == "PM":
            hour += 12
        days.append(day)
        hours.append(hour)
        months.append(month)
        years.append(year)
        
hours = []
days = []
months = []
years = []
get_day_time(fdc_data["Received DtTm"].tolist(), days, hours,months, years)
fdc_data["received_hour"] = hours
fdc_data["received_day"] = days
fdc_data["received_month"] = months
fdc_data["received_year"] = years


# # What time of the day the fire department receives less calls?
# They seem to recieve less calls after 12 am, especially between 2 and 7
# At noon there is a dramatic drop in the number of calls. It may be due to lunch break
# 
# 31st day of the month doesnt have as much calls as the other days. However, this is due to the fact that some months have less than 31 days.

# In[ ]:


plt.figure(figsize=(8,6))
incidence_count_matrix_long = pd.DataFrame({'count' : fdc_data.groupby( [ "received_hour","received_day"] ).size()}).reset_index()
incidence_count_matrix_pivot = incidence_count_matrix_long.pivot("received_hour","received_day","count") 
ax = sns.heatmap(incidence_count_matrix_pivot, annot=False, fmt="d", linewidths=1, square = False, cmap="YlGnBu")
ax = plt.xticks(fontsize = 12,color="steelblue", alpha=0.8)
ax = plt.yticks(fontsize = 12,color="steelblue", alpha=0.8)
ax = plt.xlabel("Day", fontsize = 24, color="steelblue")
ax = plt.ylabel("Hour", fontsize = 24, color="steelblue")
ax = plt.title("Count of FD Calls (Day X Hour)", fontsize = 24, color="steelblue")


# Number of calls increases as the years go by, this is most probably due to the population increase. May 2000 seems to have more calls compared to the rest, however this seems like an outlier.

# In[ ]:


plt.figure(figsize=(8,6))
incidence_count_matrix_long = pd.DataFrame({'count' : fdc_data.groupby( [ "received_month","received_year"] ).size()}).reset_index()
incidence_count_matrix_pivot = incidence_count_matrix_long.pivot("received_month","received_year","count") 
ax = sns.heatmap(incidence_count_matrix_pivot, annot=False, fmt="d", linewidths=1, square = False,cmap="YlGnBu")
ax = plt.xticks(rotation=90, fontsize = 12,color="steelblue", alpha=0.8)
ax = plt.yticks(fontsize = 12,color="steelblue", alpha=0.8)
ax = plt.xlabel("Year", fontsize = 24, color="steelblue")
ax = plt.ylabel("Month", fontsize = 24, color="steelblue")
ax = plt.title("Count of FD Calls (Month X Year)", fontsize = 24, color="steelblue")


# In[ ]:


plt.figure(figsize=(8,6))
incidence_count_matrix_long = pd.DataFrame({'count' : fdc_data.groupby( [ "received_month","received_year"])["elevation"].mean()}).reset_index()
incidence_count_matrix_pivot = incidence_count_matrix_long.pivot("received_month","received_year","count") 
ax = sns.heatmap(incidence_count_matrix_pivot, annot=False, fmt="d", linewidths=1, square = False,cmap="YlGnBu")
ax = plt.xticks(rotation=90, fontsize = 12,color="steelblue", alpha=0.8)
ax = plt.yticks(fontsize = 12,color="steelblue", alpha=0.8)
ax = plt.xlabel("Year", fontsize = 24, color="steelblue")
ax = plt.ylabel("Month", fontsize = 24, color="steelblue")
ax = plt.title("Average Elevation of Incidences\n(Month X Year)", fontsize = 24, color="steelblue")


# Surprisingly before 2008 calls were coming from higher elevations

# # What type of calls do SFFD recieve?
# * The most common call type is "Medical Incidents".
# * The top three neighborhoods in terms of SFFD calls are Tenderloin, South of Market and Mission.

# In[ ]:


incidence_count_matrix_long_CT = pd.DataFrame({'count' : fdc_data.groupby( ["Call Type"] ).size()}).reset_index()
plt.figure(figsize=(12,5))
ax = sns.barplot(x = "Call Type", y = "count" , data = incidence_count_matrix_long_CT, palette = "YlGnBu")
ax = plt.xticks(fontsize = 12,color="steelblue", alpha=0.8, rotation = 90)
ax = plt.yticks(fontsize = 12,color="steelblue", alpha=0.8)
ax = plt.xlabel("Call Type", fontsize = 24, color="steelblue")
ax = plt.ylabel("Count", fontsize = 24, color="steelblue")
ax = plt.title("Count of FD Calls", fontsize = 24, color="steelblue")


# In[ ]:


incidence_count_matrix_long_UT = pd.DataFrame({'count' : fdc_data.groupby( ["Unit Type"] ).size()}).reset_index()
ax = sns.barplot(x = "Unit Type", y = "count" , data = incidence_count_matrix_long_UT, palette = "YlGnBu")
ax = plt.xticks(fontsize = 12,color="steelblue", alpha=0.8, rotation = 90)
ax = plt.yticks(fontsize = 12,color="steelblue", alpha=0.8)
ax = plt.xlabel("Unit Type", fontsize = 24, color="steelblue")
ax = plt.ylabel("Count", fontsize = 24, color="steelblue")
ax = plt.title("Count of FD Calls", fontsize = 24, color="steelblue")


# In[ ]:


plt.figure(figsize=(12,5))
incidence_count_matrix_long_ND = pd.DataFrame({'count' : fdc_data.groupby( ["Neighborhood  District"] ).size()}).reset_index()
ax = sns.barplot(x = "Neighborhood  District", y = "count" , data = incidence_count_matrix_long_ND, palette = "YlGnBu")
ax = plt.xticks(fontsize = 12,color="steelblue", alpha=0.8, rotation = 90)
ax = plt.yticks(fontsize = 12,color="steelblue", alpha=0.8)
ax = plt.xlabel("Neighborhood  District", fontsize = 24, color="steelblue")
ax = plt.ylabel("Count", fontsize = 24, color="steelblue")
ax = plt.title("Count of FD Calls", fontsize = 24, color="steelblue")

