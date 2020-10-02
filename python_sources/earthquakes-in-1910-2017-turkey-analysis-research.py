#!/usr/bin/env python
# coding: utf-8

# ![Earhtmap](https://seismo.berkeley.edu/gifs/blog_20200126_Figure2.png)

# # The reality of earthquake becomes important every day in our country. We need analysis and research to learn this truth to the most important points. For this reason, I share my analysis between 1910 and 2017 with you.
# # I wish you healt. :)

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import time
import datetime
from datetime import datetime
import collections

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# **First we will convert the csv file to Panda Data Frame**

# In[ ]:


data = pd.read_csv('../input/earthquake.csv')


# <font color = "Blue"> 
# 1. id:           id of the earthquake
# 1. date:         date
# 1. time:         time
# 1. lat:          latitude (enlem)
# 1. long:         longitude (boylam)
# 1. country:      country
# 1. city:         city
# 1. area:         area
# 1. direction:    direction
# 1. dist:         distance of eq
# 1. depth:        depth of eq
# 1. xm:           Biggest magnitude out of MD, ML, Mw, Ms and Mb
# 1. md:           Duration Magnitude
# 1. richter:      Richter magnitude or local magnitude (ML)
# 1. mw:           moment magnitude
# 1. ms:           surface-wave magnitude
# 1. mb:           body-wave magnitude

# **As we can see here we have some null areas in given data like in: "city" "area" "direction" columns**

# In[ ]:


data.columns


# In[ ]:


data.info()


# In[ ]:


data.describe()


# In[ ]:


data.corr()


# In[ ]:


data.head(5)


# In[ ]:


data.tail(5)


# In[ ]:


data["city"].unique()


# In[ ]:


data["city"].value_counts()


# **First we need to combine both date and time that we can use it as one parameter for each eq**

# In[ ]:


print(data.iloc[:5,1])


# In[ ]:


a=data.loc[:,"date"]                            
b=data.loc[:,"time"]
print (a[0], b[0])
type(a)                                        

temp = a+"_"+b                               # this is the combined form we would like to achieve
timeformat="%Y.%m.%d_%H:%M:%S %p"

new=[datetime.strptime(x, timeformat) for x in temp]

#for i in temp:
#    i=datetime.strptime(i,timeformat)
#why not this way??

print("temp =",type(temp),"\n""new =",type(new),"\n""data.time =",type(data.date))

data.time=new

data.rename(columns={'time': 'newtime'}, inplace=True) 
del data["date"]                            # we dont need it anymore as all stored in date.time


# In[ ]:


data["year"]=[int(datetime.strftime(x,"%Y")) for x in data.newtime]
data["month"]=[int(datetime.strftime(x,"%m"))+int(datetime.strftime(x,"%Y"))*12 for x in data.newtime]


# In[ ]:


tur=data.country == "turkey"
real=data.richter > 1

cit=data[tur & real].city
cits=cit.unique()

print("Total Cities =",cit.size)

a=0
for i in cits:
    a=a+1
    if a==len(cits):
        print("Unique Cities = {}".format(a))

f=Counter(cit)
newf=f.most_common()

print(type(f))
print(type(newf))


# In[ ]:


maks=max(f, key=f.get) 
most=f.most_common(5)[0]
most2=f.most_common(5)[1]
print("Max number of eq occured in {} with {} eq and second is {} with {}" .format(maks.upper(),most[1],most2[0].upper(),most2[1]))


# In[ ]:


yearfilter = data.year > 1997
data[yearfilter][["year","country","city","area","depth"]].groupby(["year"], as_index = False).count().sort_values(by = "year", ascending = False)


# In[ ]:


yearfilter = data.year > 1997
data[yearfilter][["year","richter","xm","md","mw","ms","mb"]].groupby(["year"], as_index = False).count().sort_values(by = "richter", ascending = False)


# In[ ]:


yearfilter = data.year > 1997
data[yearfilter][["year","richter","long"]].groupby(["year"], as_index = False).mean().sort_values(by = "richter", ascending = False)


# In[ ]:


data.columns[data.isnull().any()]  


# In[ ]:


data.isnull().sum()


# In[ ]:


data.year.plot(kind = "hist" , color = "red" , edgecolor="black", bins = 100 , figsize = (12,12) , label = "Earthquakes frequency")
plt.legend(loc = "upper right")
plt.show()


# In[ ]:


def dist(baslik):
    
    
    tur = data.country=="turkey"                # There arent many records before 2000 roughly, so lets filter after 1998, also just take magnitudes over 2 
    richter = data.richter > 2
    yearfilter = data.year > 1998
    md = data.md > 2
    
    datatr= data[tur & richter & yearfilter & md]
    
    plt.figure(figsize=(10,5))
    plt.hist(datatr[baslik], bins=30, color="blue")
    plt.ylabel("Frequency")
    plt.title(baslik)

ozet=["richter", "year", "md", "xm","lat","long"]
    
for each in ozet:
    dist(each)
    


# **We have some null values however these are irrevelant headers for our analysis so we can ignore**

# In[ ]:


plt.scatter(data.year,data.country, color="red", alpha=0.5)


# In[ ]:


data.country.value_counts().plot(kind = "bar" , color = "blue" , figsize = (30,10),fontsize = 20)
plt.xlabel("country",fontsize=18,color="blue")
plt.ylabel("Frequency",fontsize=18,color="blue")
plt.show()


# In[ ]:


a=data.country.value_counts()[0:6]
sizes=a.values
labels=a.index
explode=[0,0,0,0,0,0]
colors=["orange","red","blue","green","yellow","violet"]
plt.figure(figsize=(7,7))
plt.pie(sizes,explode=[0.1]*6,labels=labels,colors=colors,autopct='%1.1f%%')
plt.title('Country',color = 'blue',fontsize = 15)


# In[ ]:


data.city.value_counts().plot(kind = "bar" , color = "blue" , figsize = (30,10),fontsize = 20)
plt.xlabel("City",fontsize=18,color="blue")
plt.ylabel("Frequency",fontsize=18,color="blue")
plt.show()


# In[ ]:


a=data.city.value_counts()[0:6]
sizes=a.values
labels=a.index
explode=[0,0,0,0,0,0]
colors=["orange","red","blue","green","yellow","violet"]
plt.figure(figsize=(7,7))
plt.pie(sizes,explode=[0.1]*6,labels=labels,colors=colors,autopct='%1.1f%%')
plt.title('City',color = 'blue',fontsize = 15)


# In[ ]:


a=data.area.value_counts()[0:6]
sizes=a.values
labels=a.index
explode=[0,0,0,0,0,0]
colors=["orange","red","blue","green","yellow","violet"]
plt.figure(figsize=(7,7))
plt.pie(sizes,explode=[0.1]*6,labels=labels,colors=colors,autopct='%1.1f%%')
plt.title('Area',color = 'blue',fontsize = 15)


# In[ ]:


data.plot(kind = "scatter",x="richter",y = "xm")
plt.show()


# In[ ]:


#plt.scatter(d.long, d.lat, grid=True, label= "latitude - duration", color="red")
data.plot(kind= "scatter", x= "long", y= "lat", grid=True, label= "long - lat", color="red")
plt.legend()
plt.xlabel("duration")
plt.ylabel("latitude")
plt.title("long - lat")


# In[ ]:


plt.scatter(data.depth, data.mb)
plt.legend()
plt.xlabel("Depth")
plt.ylabel("Magnitude body")
plt.show()


# In[ ]:


data.plot(kind= "scatter", x= "xm", y= "dist",color= "brown", grid= True)
plt.xlabel= "Latitude"
plt.ylabel= "md"
plt.legend()


# In[ ]:


plt.scatter(data.depth, data.xm, color= "green")
plt.legend()
plt.xlabel = "Depth"
plt.ylabel = "xm"
plt.show()


# In[ ]:


data.plot(kind= "scatter", x= "depth", y= "dist",color= "purple", grid= True)
plt.xlabel= "Latitude"
plt.ylabel= "md"
plt.legend()


# In[ ]:


istanbul = data[data.city== "istanbul"]
print(istanbul)


# In[ ]:


print(len(istanbul), "times in izmir except the districts")


# In[ ]:


ankara = data[data.city== "ankara"]
print(ankara)


# In[ ]:


print(len(ankara), "times in izmir except the districts")


# In[ ]:


izmir = data[data.city== "izmir"]
print(izmir)


# In[ ]:


print(len(izmir), "times in izmir except the districts")


# In[ ]:


corum = data[data.city== "corum"]
print(corum)


# In[ ]:


corum = data[data.city== "corum"]
print(corum)


# # YARARLANDIGIM MAKALELER
# 
# https://www.kaggle.com/tuttypie/earthquakes-turkey
# https://www.kaggle.com/berkesun/earthquakes-in-turkey-1910-2017-basic-eda
# 

# In[ ]:




