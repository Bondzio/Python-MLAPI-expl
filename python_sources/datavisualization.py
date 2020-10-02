#!/usr/bin/env python
# coding: utf-8

# # Data visualization
# 
# ### Contents
# * [1. Registering data](#1)
# * [2. Bar plot](#2)
# * [3. Point plot](#3)
# * [4. Joint plot](#4)
# * [5. Kde plot](#5)
# * [6. Violin plot](#6)
# * [7. Heatmap](#7)
# * [8. Pair plot](#8)
# * [9. Pie chart](#9)
# * [10. Lm plot](#10)
# * [11. Box plot](#11)
# * [12. Swarm plot](#12)
# * [13. Count plot](#13)

# <a id="1"></a> 
# # 1. Registering data 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


# Read datatables
highschool = pd.read_csv("/kaggle/input/fatal-police-shootings-in-the-us/PercentOver25CompletedHighSchool.csv", encoding="windows-1252")
poverty = pd.read_csv("/kaggle/input/fatal-police-shootings-in-the-us/PercentagePeopleBelowPovertyLevel.csv", encoding="windows-1252")
income = pd.read_csv("/kaggle/input/fatal-police-shootings-in-the-us/MedianHouseholdIncome2015.csv", encoding="windows-1252")
race = pd.read_csv("/kaggle/input/fatal-police-shootings-in-the-us/ShareRaceByCity.csv", encoding="windows-1252")
kills = pd.read_csv("/kaggle/input/fatal-police-shootings-in-the-us/PoliceKillingsUS.csv", encoding="windows-1252")


# ### Check dataframes

# In[ ]:


highschool.head()


# In[ ]:


poverty.head()


# In[ ]:


income.head()


# In[ ]:


city.head()


# In[ ]:


kills.head()


# ### Get geographic areas

# In[ ]:


geolist = list(poverty["Geographic Area"].unique())    #Create a geographic area list


# ### Prepare dataframes for data visualisation

# In[ ]:


poverty.head()


# In[ ]:


poverty.info()


# In[ ]:


poverty.poverty_rate.value_counts()


# In[ ]:


poverty.poverty_rate.replace(["-"], 0.0, inplace=True)    # Replace undefined values.
poverty.poverty_rate = poverty.poverty_rate.astype(float) # Change value type to float for analysis
poverty.info()


# <a id="2"></a> 
# # 2. Bar plot
# 

# ### poverty_ratio data

# In[ ]:


geo_poverty_ratio = []      # Create an empty list
for i in geolist:
    x = poverty[poverty["Geographic Area"] == i]
    y = sum(x.poverty_rate)/len(x)
    geo_poverty_ratio.append(y)
povertydata = pd.DataFrame({'geolist': geolist,'geo_poverty_ratio':geo_poverty_ratio})
new_index = (povertydata['geo_poverty_ratio'].sort_values(ascending=False)).index.values
sorted_poverty = povertydata.reindex(new_index)
sorted_poverty.head()


# In[ ]:


# Visualization
plt.figure(figsize=(15,10))
sns.barplot(x=sorted_poverty['geolist'], y=sorted_poverty['geo_poverty_ratio'])
plt.xticks(rotation= 45)
plt.xlabel('States')
plt.ylabel('Poverty Rate')
plt.title('Poverty Rate Given States')
plt.show()


# ### Kills data

# In[ ]:


# Explore data
kills.head()


# In[ ]:


# Prepera data for analysis
seperate = kills.name[kills.name != "TK TK"].str.split()    # seperate name and surname
a,b = zip(*seperate)                                        # a: name, b:surname
name_list = a+b                                             # Combine names and surnames
from collections import Counter                             # Import counter to use Counter
name_count = Counter(name_list)                             # Count names in a list
most_common_names = name_count.most_common(15)              # Take most common names from list
x,y = zip(*most_common_names)                               # Seperate list to tuple. x: names y:count
x,y = list(x),list(y)                                       # Convert tuple to list    


# In[ ]:


# Create a blank graph 
plt.figure(figsize=(15,10))

# Visualization
sns.barplot(x=x, y=y) # palette = sns.cubehelix_palette(len(x))

# Customize graph
plt.xlabel('Name or Surname of killed people')
plt.ylabel('Frequency')
plt.title('Most common 15 Name or Surname of killed people')
plt.show()


# ### Highschool data

# In[ ]:


# Explore data
highschool.head()


# In[ ]:


# Explore data information
highschool.info()


# In[ ]:


# Replace undefined values for "percent_completed_hs" before converting to float

highschool.percent_completed_hs.replace(["-"], 0.0, inplace=True)
#highschool.percent_completed_hs.value_counts()


# In[ ]:


# Convert "percent_completed_hs" type to float
highschool.percent_completed_hs = highschool.percent_completed_hs.astype(float)


# In[ ]:


# Take an area_list for highschool data
area_list = list(highschool["Geographic Area"].unique())


# In[ ]:


# Create a rate_list for high school
rate_list = []                                             # Define an empty rate_list
for i in area_list:                                        # Return a for loop for every area
    x = highschool[highschool["Geographic Area"] == i]     # Take dataframe for that area
    rate = sum(x.percent_completed_hs) / len(x)            # Sum of records / num of records
    rate_list.append(rate)                                 # Append result to rate_list                                


# In[ ]:


# Create a new dataframe with only unique areas and rates
highschooldata = pd.DataFrame({"area": area_list, "rate": rate_list})
highschooldata.head()


# In[ ]:


# Sorting data ascending for better visualization
#highschooldata.rate.sort_values(ascending=True)                         # create a sorted data with index.
nindex = (highschooldata.rate.sort_values(ascending=True)).index.values  # Create a sorted index array
highschooldata_sorted = highschooldata.reindex(nindex)                   # Change index to sorted index
#highschooldata_sorted          # Value sorted data
#highschooldata                 # Raw unique data
#highschool                     # Raw data


# In[ ]:


# Create a blank graph area
plt.figure(figsize=(15,10))

# Visualization
sns.barplot(x = highschooldata_sorted.area, y = highschooldata_sorted.rate)

# Customize graph 
plt.xticks(rotation=90)
plt.xlabel("States")
plt.ylabel("High school rate")
plt.title("High school graduation graph")
plt.show()


# ### Race data

# In[ ]:


# Explore data
race.head()


# In[ ]:


# Data information
race.info()


# In[ ]:


# Define unknown values and convert them to float
race.replace(["-"], 0.0, inplace=True)
race.replace(["(X)"], 0.0, inplace=True)
race.loc[:,["share_white", "share_black", "share_native_american", "share_asian", "share_hispanic"]] = race.loc[:,["share_white", "share_black", "share_native_american", "share_asian", "share_hispanic"]].astype(float)
race.info()


# In[ ]:


# Area list for race data
area_race = race["Geographic area"].unique()
area_race


# In[ ]:


# Calculate race by area
race_white = []
race_black = []
race_native = []
race_asian = []
race_hispanic = []

for i in area_race:
    x = race[race["Geographic area"] == i]
    race_white.append(sum(x.share_white) / len(x.share_white))
    race_black.append(sum(x.share_black) / len(x.share_black))
    race_native.append(sum(x.share_native_american) / len(x.share_native_american))
    race_asian.append(sum(x.share_asian) / len(x.share_asian))
    race_hispanic.append(sum(x.share_hispanic) / len(x.share_hispanic))
    


# In[ ]:


# Create empty graph
f,ax = plt.subplots(figsize = (9,15))

# Draw bar plots
sns.barplot(x= race_white, y= area_race, color="green", alpha=.5, label= "gray")
sns.barplot(x= race_black, y= area_race, color="blue", alpha=.5, label= "black")
sns.barplot(x= race_native, y= area_race, color="cyan", alpha=.5, label= "native")
sns.barplot(x= race_asian, y= area_race, color="yellow", alpha=.5, label= "asian")
sns.barplot(x= race_hispanic, y= area_race, color="red", alpha=.5, label= "hispanic")

# Customize legend
ax.legend(loc= "upper right", frameon=True)

# Customize titles
ax.set(xlabel="Races", ylabel="Area", title="Race distrubution")

# Close info string
plt.show()


# <a id="3"></a> 
# # 3. Point plot
# 
# Compare poverty and high school data

# In[ ]:


# Poverty data
sorted_poverty.head()


# In[ ]:


# High school data
highschooldata_sorted.head()


# In[ ]:


# Normalize data
sorted_poverty["geo_poverty_ratio"] = sorted_poverty["geo_poverty_ratio"] / max(sorted_poverty["geo_poverty_ratio"])
highschooldata_sorted["rate"] = highschooldata_sorted["rate"] / max(highschooldata_sorted["rate"])


# In[ ]:


# Create a new dataframe
highschool_poverty = pd.concat([sorted_poverty, highschooldata_sorted], axis=1)

# Sort data
highschool_poverty.sort_values("geo_poverty_ratio", inplace=True)


# In[ ]:


# Create a blank graph
f, ax = plt.subplots(figsize= (20,10))

# Visualization
sns.pointplot(x="area", y="geo_poverty_ratio", data=highschool_poverty, color="blue", alpha=0.1)
sns.pointplot(x="area", y="rate", data=highschool_poverty, color="red", alpha=0.5)

# Show text on graph
plt.text(10,0.7,"High school graduation VS poverty", fontsize=19, style="italic")

# Customize
#ax.set(xlabel="states", ylabel="values", title="High school - poverty ratio")
plt.xlabel("States", color="red", fontsize=15)
plt.ylabel("Values", color="green", fontsize=15)
plt.title("High school - poverty ratio", color="blue", fontsize=15)

# Add grids to graph
plt.grid()

# Clear info
plt.show()


# <a id="4"></a> 
# # 4. Joint plot

# In[ ]:


# Use highschool_poverty data 

# Joint plot
sns.jointplot(data=highschool_poverty, x="geo_poverty_ratio", y="rate")

# FOR KAGGLE
plt.savefig('graph.png')

# Clear
plt.show()


# In[ ]:


# Joint plot with KDE
sns.jointplot(data=highschool_poverty, x="geo_poverty_ratio", y="rate", kind="kde")

# FOR KAGGLE
plt.savefig('graph.png')

# Clear
plt.show()


# <a id="5"></a> 
# # 5. KDE plot

# In[ ]:


###### Same as JointPlot type=kde
sns.kdeplot(highschool_poverty["geo_poverty_ratio"], highschool_poverty["rate"], shade=True, cut=3)

# FOR KAGGLE
plt.savefig('graph.png')

# Clear
plt.show()


# <a id="6"></a> 
# # 6. Lm plot

# In[ ]:


# Visualization
sns.lmplot(data=highschool_poverty, x="geo_poverty_ratio", y="rate")

# Clear
plt.show()


# <a id="7"></a> 
# # 7. Violin plot

# In[ ]:


# Visualization
pal = sns.cubehelix_palette(2, rot=-.5, dark=.3)         # SNS PALETTE
sns.violinplot(data=highschool_poverty, inner="points")

# FOR KAGGLE
plt.savefig('graph.png')

# Clear
plt.show()


# <a id="8"></a> 
# # 8. Heatmap

# In[ ]:


# Correlation of data
highschool_poverty.corr()


# In[ ]:


# Visualization of correlation
sns.heatmap(highschool_poverty.corr(), annot=True, linecolor="gray", linewidth=.1, fmt=".1f")

# Clear
plt.show()


# <a id="9"></a>
# # 9. Pair plot 

# In[ ]:


# Visualization of correlation
sns.pairplot(highschool_poverty)

# Clear
plt.show()


# <a id="10"></a>
# # 10. Pie plot 

# In[ ]:


# Explore data
kills.race.value_counts()


# In[ ]:


# Prepare data
labels = kills.race.value_counts().index
sizes = kills.race.value_counts().values
colors = ["red", "green", "cyan", "blue", "yellow", "grey"]
explode = [0,0,0,0,0,0]


# In[ ]:


# Visualization
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%')

# Customization
plt.title('Killed People According to Races',color = 'blue',fontsize = 15)

# Clear
plt.show()


# <a id="11"></a> 
# # 11. Box plot

# In[ ]:


# Explore data
kills.head()


# In[ ]:


# Visualization
sns.boxplot(x="gender", y="age", hue="signs_of_mental_illness", data=kills,  palette="PRGn")

# Clear
plt.show()


# <a id="12"></a> 
# # 12. Swarm plot

# In[ ]:


# Visualization
sns.swarmplot(x="gender", y="age", hue="signs_of_mental_illness", data=kills)

# Clear
plt.show()


# <a id="13"></a>
# # 13. Count plot 

# In[ ]:


# Explore data
kills.head()


# In[ ]:


# Visualization
sns.countplot(kills.gender)

# Clear
plt.show()


# In[ ]:


# Visualization
sns.countplot(kills.race)

# Clear
plt.show()


# In[ ]:


# Prepare data
df25 =['above25' if i >= 25 else 'below25' for i in kills.age]
df = pd.DataFrame({'age':df25})

# Visualization
sns.countplot(df.age)

# Clear
plt.show()


# # CONCLUSION
# **I will be happy to hear your comments!!!**
# Thanks
