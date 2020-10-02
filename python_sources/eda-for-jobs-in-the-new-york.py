#!/usr/bin/env python
# coding: utf-8

# Hi everyone! In this kernel, we apply EDA(Exploring Data Analysis) to Jobs in the New York City. 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# To start the analysis of the data, firstly we have to read data from csv file.

# In[ ]:


data = pd.read_csv("../input/nyc-jobs.csv")


# Let's look at the data.

# In[ ]:


data.head()


# We can see the some values of the data, are nan. It means data is not clean.
# we must clean the data to use this data in algorithms such as machine learning algorithms. The cleaning data can be challenging. Let's look at the data information to find, how many value is missed.

# In[ ]:


data.info()


# We can easily see the how many number of data is empty. For example, Recruitment Contact column has 0 non-null object. It means this column is completely empty. We can't use this column. Let's start to clean data.

# In[ ]:


data.drop(columns="Recruitment Contact",axis=1,inplace=True)
data.info()


# Now, we can look at the other missing values for our data set.

# In[ ]:


empty_values = {}
columns = data.columns
for col in columns:
    empty_values[col] = 0
    for val in data[col].values:
        val = str(val)
        if val == "nan":
            empty_values[col] += 1


# We found the all missing values for each columns of our data set. We may increase the understandability with using visualization. You know "a picture is worths lots of words".

# In[ ]:


columns = [*empty_values.keys()]
number_of_missing_Values = [*empty_values.values()]

df = pd.DataFrame({"Columns of Data Set":columns,"# of Missing Values":number_of_missing_Values})
newIndex = (df["# of Missing Values"].sort_values(ascending = False)).index.values
sortedData = df.reindex(newIndex)

plt.figure(figsize = (15,10))
ax = sns.barplot(x = sortedData["Columns of Data Set"],y = sortedData["# of Missing Values"])
plt.xticks(rotation = 90)
plt.xlabel("Columns of Data Set")
plt.ylabel("# of Missing Value")
plt.title("Number of Missing Values for Each Column of Our Data Set")


# The upper bar graph shows us our data is almost clean. But there is problems in some columns in our data set. Let's look at this bar graph again without columns which has 0 missing values.

# In[ ]:


new_columns = []
new_values = []

for col,val in zip(columns,number_of_missing_Values):
    if val != 0:
        new_columns.append(col)
        new_values.append(val)

df = pd.DataFrame({"Columns of Data Set":new_columns ,"# of Missing Values":new_values})
newIndex = (df["# of Missing Values"].sort_values(ascending = False)).index.values
sortedData = df.reindex(newIndex)

plt.figure(figsize = (15,10))
ax = sns.barplot(x = sortedData["Columns of Data Set"],y = sortedData["# of Missing Values"])
plt.xticks(rotation = 90)
plt.xlabel("Columns of Data Set")
plt.ylabel("# of Missing Value")
plt.title("Number of Missing Values for Each Column of Our Data Set")


# Now, We should concentrate those columns to clean the data.

# In[ ]:


for each in sortedData["Columns of Data Set"]:
    print(each+"---->")
    print("--------------------------")
    print(data[each].head())
    print("--------------------------")
    print()


# Let's look at # Of Positions feature closer.

# In[ ]:


plt.figure(figsize = (20,10))
plt.plot(data["# Of Positions"])
plt.show()


# We can replace the nan values with median of the data for # of Positions feature.
# 

# In[ ]:


data["# Of Positions"].fillna(data["# Of Positions"].median(),inplace = True)
cnt_x = 0
cnt_y = 0
for each in data["# Of Positions"]:
    if str(each) == "nan":
        cnt_x += 1
    else:
        cnt_y += 1

plt.figure(figsize = (10,5))
plt.bar(x = "Empty",height = cnt_x,color ="red")
plt.bar(x = "Non Empty",height = cnt_y,color ="blue")
plt.show()


# There is no empty values in # of Positions feature anymore. Okay let's start to explore the data.
# Firsly, let's look at the relationship with Business Title and # Of Positions.

# In[ ]:


number_of_position = {}
for title,np in zip(data["Business Title"],data["# Of Positions"]):
    if title in number_of_position.keys():
        number_of_position[title] += np
    else:
        number_of_position[title] = np
        
columns = [*number_of_position.keys()]
positions = [*number_of_position.values()]

df = pd.DataFrame({"Business Title":columns,"# of positions":positions})
newIndex = (df["# of positions"].sort_values(ascending = False)).index.values
sortedData = df.reindex(newIndex)

plt.figure(figsize = (15,10))
ax = sns.barplot(x = sortedData["Business Title"][0:20],y = sortedData["# of positions"])
plt.xticks(rotation = 90)
plt.xlabel("Business Title")
plt.ylabel("# of Positions")
plt.title("Relationship between Business Title and Number of Positions")        
plt.show()


# After that, we'll look at frequency of each agency in our data set. Then we'll visualize that.

# In[ ]:


agencies = data["Agency"].unique()
freq_Of_agencies = []
for agency in agencies:
    count = len(data[data["Agency"] == agency])
    freq_Of_agencies.append(count)

df = pd.DataFrame({"agency":agencies,"freq":freq_Of_agencies})
newIndex = (df["freq"].sort_values(ascending = False)).index.values
sortedData = df.reindex(newIndex)

plt.figure(figsize = (15,10))
ax = sns.barplot(x = sortedData["agency"],y = sortedData["freq"])
plt.xticks(rotation = 90)
plt.xlabel("agencies")
plt.ylabel("frequencies")
plt.title("Number of Agency in New York")
plt.show()


# Finally ,we can search the relationship with salary range and # of positions. 

# In[ ]:


plt.figure(figsize=(15,10))
sns.jointplot(data["Salary Range To"],data["# Of Positions"],size=10,color="r")
plt.xlabel("Salary Range To")
plt.ylabel("Number Of Positions")
plt.show()


# If you've read my kernel, thank you very much,
# If you write a comment, I'll be appreciate to you...
