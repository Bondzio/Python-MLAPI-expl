#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


apps = pd.read_csv("../input/googleplaystore.csv")


# In[ ]:


print(apps['Price'].value_counts(dropna=False))


# Price of an app is "Everyone" as it is seen above. Probably, there has been a mistake on entrying data. Below we will analyze other properties of this app having price value "Everyone". 

# In[ ]:


apps[apps['Price'] == 'Everyone']


# In[ ]:


apps[10470:10475]


# **Category** of this app (Life Made WI-Fi Touchscreen Photo Frame) is not included and the places of other data shifted to the left. Below is the correction of this mistake.

# In[ ]:


import warnings                     #to close warnings
warnings.filterwarnings("ignore")

apps['Android Ver'][10472]=apps['Current Ver'][10472]
apps['Current Ver'][10472]=apps['Last Updated'][10472]
apps['Last Updated'][10472]=apps['Genres'][10472]
apps['Genres'][10472]=apps['Content Rating'][10472]
apps['Content Rating'][10472]=apps['Price'][10472]
apps['Price'][10472]=apps['Type'][10472]
apps['Type'][10472]=apps['Installs'][10472]
apps['Installs'][10472]=apps['Size'][10472]
apps['Size'][10472]=apps['Reviews'][10472]
apps['Reviews'][10472]=apps['Rating'][10472]
apps['Rating'][10472]=apps['Category'][10472]
apps['Category'][10472]="Unknown"

apps[10472:10473]


# > **DATAFRAME FROM DICTIONARY**

# In[ ]:


category = apps.Category
price = apps.Price
installs = apps.Installs
reviews = apps.Reviews

labels = ["Category","Price","Installs","Reviews"]
columns = [category,price,installs,reviews]

zipped = list(zip(labels,columns))
df = pd.DataFrame(dict(zipped))
df[4775:4800]      #as an example


# Now I want to plot Reviews and Installs but types of values are 'str' so I need to convert them into 'int'. I will use first 2000 rows to show.

# In[ ]:


i = 0
while (i<2000):
    df.Installs[i] = df.Installs[i][:-1]               #remove the last character in string which is "+"
    df.Installs[i] = df.Installs[i].replace(",", "")   #remove all ","s in a string
    i = i+1
    
df.Installs[0:2000] = df.Installs[0:2000].astype(int)
df.Reviews[0:2000] = df.Reviews[0:2000].astype(int)

df[0:2000]


# **VISUAL EXPLORATORY DATA ANALYSIS**

# In[ ]:


df1 = df[0:2000].loc[:,["Reviews","Installs"]]
df1.plot(figsize=(15,10))
plt.show()


# Since the range of installs and reviews are very different, the graph is not a good representation. Below there is a more convenient way to analyze these two properties together.

# In[ ]:


df1.plot(subplots=True,figsize=(10,10))
plt.show()


# In[ ]:


df1.plot(kind = "hist",y = "Reviews",bins =50,range= (0,1000),normed = True)    #analyze number of reviews
plt.show()


# In[ ]:


fig, axes = plt.subplots(nrows=2,ncols=1,figsize=(10,10))
df1.plot(kind = "hist",y = "Reviews",bins =50,range= (0,1000),normed = True, ax=axes[0])
df1.plot(kind = "hist",y = "Reviews",bins =50,range= (0,1000),normed = True, ax=axes[1], cumulative=True)
plt.savefig('graph.png')
plt


# **INDEXING PANDAS TIME SERIES**

# In[ ]:


df2 = apps[0:2000]
m=[]                #an empty month list
y=[]                #an empty year list
d=[]                #an empty day list
date_update = []    #join year, month and day into this list
i = 0
while (i<len(df2["Last Updated"])):
    if (df2["Last Updated"][i][0:3]=="Jan"):
        m.append("01")
    elif (df2["Last Updated"][i][0:3]=="Feb"):
        m.append("02")
    elif (df2["Last Updated"][i][0:3]=="Mar"):
        m.append("03")
    elif (df2["Last Updated"][i][0:3]=="Apr"):
        m.append("04")
    elif (df2["Last Updated"][i][0:3]=="May"):
        m.append("05")
    elif (df2["Last Updated"][i][0:3]=="Jun"):
        m.append("06")
    elif (df2["Last Updated"][i][0:3]=="Jul"):
        m.append("07")
    elif (df2["Last Updated"][i][0:3]=="Aug"):
        m.append("08")
    elif (df2["Last Updated"][i][0:3]=="Sep"):
        m.append("09")
    elif (df2["Last Updated"][i][0:3]=="Oct"):
        m.append("10")
    elif (df2["Last Updated"][i][0:3]=="Nov"):
        m.append("11")
    else:
        m.append("12")
    y.append(df2["Last Updated"][i][-4:])            #check last 4 characters in string df2["Last Updated"][i]
    if (df2["Last Updated"][i][-8]==" "):            #if eight character from last in string df2["Last Updated"][i] is not a number, then day has one digit (which is in -7)
        d.append("0"+df2["Last Updated"][i][-7])     
    else:
        d.append(df2["Last Updated"][i][-8:-6])      #if eight character from last in string df2["Last Updated"][i] is a number, then day is (-8:-6)
    date_update.append(y[i]+"-"+m[i]+"-"+d[i])       #fill date_update list with dates in format yyyy:mm:dd
    i = i + 1  
    
date_update[0:10]     


# I will analyze means of installs and reviews in each month and year so I need to convert these properties from "object" to "int". 

# In[ ]:


df2["Installs"] = df1["Installs"].astype(int)    
df2["Reviews"] = df1["Reviews"].astype(int)


# In[ ]:


date_time_object = pd.to_datetime(date_update)    #create a DatetimeIndex by converting date_update
df2["Last Updated"] = date_time_object            
df2 = df2.set_index("Last Updated")               #index of df2 = "Last Updated"
df2[0:10]


# In[ ]:


print(df2.loc["2018-08-01":"2018-10-01"])     #show items which have index from 2018-08-01 to 2018-10-01


# In[ ]:


df2.resample("A").mean()    #show means of "Rating", "Reviews" and "Installs" for each year


# In[ ]:


df2.resample("M").mean()    #show means of "Rating", "Reviews" and "Installs" for each month
                            #NaN values mean that there are no data on that months


# In[ ]:


df2.resample("M").mean().interpolate("linear")     #fill NaN values by interpolation


# **MANIPULATING DATAFRAMES**
# 
# I will analyze approximately how much money was spent on each app.

# In[ ]:


notfree = apps[apps.Price != "0"]    #notfree includes app which are not free

def remove(x):
    """remove "$" in Price so that we can convert Price into type float"""
    x = x[1:]
    return x    
notfree.Price = notfree.Price.apply(remove)   #apply remove function for all elements in notfree.Price
notfree.Price = notfree.Price.astype(float)


# Before Visual Exploratory Data Analysis, I had manipulated "Installs" column in apps dataframe to use installs as numbers. Now, I need it again and I created a function for this purpose. It does the same thing with:

# In[ ]:


#i = 0
#while (i<2000):
#    df.Installs[i] = df.Installs[i][:-1]                    #remove the last character in string which is "+"
#    df.Installs[i] = df.Installs[i].replace(",", "")   #remove all ","s in a string
#    i = i+1


# We see that using functions can be helpful in case we want to do same operations afterwards.

# In[ ]:


def installs(x):
    x = x[:-1]
    x = x.replace(",","")
    return x

notfree.Installs = notfree.Installs.apply(installs)  #convert "Installs" to an approximate number
notfree.Installs = notfree.Installs.astype(float) 

notfree["Money_Spent"] = notfree.Installs * notfree.Price  #calculate total money spent for each app


# In[ ]:


df3 = notfree.set_index(["Category","Genres"])
df3[750:800]


# In[ ]:


df4 = notfree[25:30]
df4.pivot(index="Genres",columns="Price",values="App")


# In[ ]:


notfree.groupby("Category").mean()     #mean values in each category


# In[ ]:


notfree.groupby("Category")[["Rating","Money_Spent"]].max()   #max values of Rating and Money_Spent in each category

