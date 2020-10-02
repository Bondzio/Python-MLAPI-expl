#!/usr/bin/env python
# coding: utf-8

# # Countries' gps/mobile behavior.   
# Below, you will see the spike in cases and deaths along with the decrease of mobility     
# in Spain, Brazil, UK, and USA.      
# While they seem the same, the graph provide clues as to onset of pandemic, public behavior,    
# and difference among countries during lockdowns due to COVID-19.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

##Apple's dataset on device mobility during the COVID19 pandemic.

apple= pd.read_csv("../input/apples-mobility-report/Copy of applemobilitytrends-2020-04-14.csv")
apple=apple.drop(['geo_type'], axis = 1) 
apple.head(2)


# In[ ]:


#Dataset from the World Health Organization on COVID19 cases and deaths

World = pd.read_csv("../input/httpsourworldindataorgcoronavirussourcedata/updated apr 16.csv")
World.head(2)


# **Countries of focus**:    
# 'Brazil', 'Spain', 'UK', and the 'United States'   

# In[ ]:


USA1=World.loc[World['location']== 'United States']
Spain1=World.loc[World['location']== 'Spain']
Brzl1=World.loc[World['location']== 'Brazil']
UK1=World.loc[World['location']== 'United Kingdom']


# **SPAIN**

# In[ ]:


##COVID-cases and deaths reported

Spain1.date=pd.to_datetime(Spain1.date)
Spain1


# In[ ]:


x=Spain1['date']
a=Spain1['total_cases']
b=Spain1['total_deaths']

fig = plt.figure(figsize=(18,7))
plt.plot(x, a)
plt.plot(x, b)

plt.title('Cases and Deaths from COVID-19 in SPAIN') # Title
plt.xticks(Spain1.date.unique(), rotation=90) # All values in the x axis rotate 90 degrees
plt.show()


# In[ ]:


Spa=apple.loc[apple['region']== 'Spain']
Spa=Spa.drop(['region'], axis = 1) 

###transposed dataset

Spain=Spa.T
Spain.head(3)


# In[ ]:


#rename and fix dataframe columns

Spn = Spain.rename(columns={123: 'driving', 124: 'transit', 125:'walking'})
Spn = Spn.drop(['transportation_type'])
Spn.head(2)


# In[ ]:


##change dates on indexes (rows) to date object
Spn.index = pd.to_datetime(Spn.index)
Spn.head(2)


# In[ ]:


Spn.plot.line()
plt.title('Device movement in SPAIN') # Title
plt.show()


# **BRAZIL**

# In[ ]:


##COVID-cases and deaths reported
#first, I fixed the date format

Brzl1.date=pd.to_datetime(Brzl1.date)
Brzl1.head(2)


# In[ ]:


x=Brzl1['date']
a=Brzl1['total_cases']
b=Brzl1['total_deaths']

fig = plt.figure(figsize=(18,7))
plt.plot(x, a)
plt.plot(x, b)

plt.title('Cases and Deaths from COVID-19 in BRAZIL') # Title
plt.xticks(Brzl1.date.unique(), rotation=90) # All values in the x axis rotate 90 degrees
plt.show()


# In[ ]:


Bra=apple.loc[apple['region']== 'Brazil']
Bra


# In[ ]:


Bra=Bra.drop(['region'], axis = 1) 

###transposed dataset

Brazil=Bra.T
Brazil.head(3)


# In[ ]:


#rename and fix dataframe columns

Bzl = Brazil.rename(columns={12: 'driving', 13: 'transit', 14:'walking'})
Bzl = Bzl.drop(['transportation_type'])

##change dates on indexes (rows) to date object

Bzl.index = pd.to_datetime(Bzl.index)
Bzl.head(2)


# In[ ]:


Bzl.plot.line()
plt.title('Device movement in BRAZIL') # Title
plt.show()


# **United States**

# In[ ]:


USA1.date=pd.to_datetime(USA1.date)
USA1.head(2)


# In[ ]:


x=USA1['date']
a=USA1['total_cases']
b=USA1['total_deaths']

fig = plt.figure(figsize=(18,7))
plt.plot(x, a)
plt.plot(x, b)

plt.title('Cases and Deaths from COVID-19 in the USA') 
plt.xticks(USA1.date.unique(), rotation=90) 
plt.show()


# In[ ]:


USA=apple.loc[apple['region']== 'United States']
USA


# In[ ]:


USA=USA.drop(['region'], axis = 1) 

###transposed dataset

UnitedStates=USA.T
UnitedStates.head(3)


# In[ ]:


#rename and fix dataframe columns

USofA = UnitedStates.rename(columns={142: 'driving', 143: 'transit', 144:'walking'})
USofA = USofA.drop(['transportation_type'])

##change dates on indexes (rows) to date object

USofA.index = pd.to_datetime(USofA.index)
USofA.head(2)


# In[ ]:


USofA.plot.line()
plt.title('Device movement in the USA') 
plt.show()


# **UNITED KINGDOM**

# In[ ]:


UK1.date=pd.to_datetime(UK1.date)
UK1.head(2)


# In[ ]:


x=UK1['date']
a=UK1['total_cases']
b=UK1['total_deaths']

fig = plt.figure(figsize=(18,7))
plt.plot(x, a)
plt.plot(x, b)

plt.title('Cases and Deaths from COVID-19 in the UK') 
plt.xticks(UK1.date.unique(), rotation=90) 
plt.show()


# In[ ]:


UK=apple.loc[apple['region']== 'UK']
UK


# In[ ]:


UK=UK.drop(['region'], axis = 1) 

###transposed dataset

UnitedKingdom=UK.T
UnitedKingdom.head(3)


# In[ ]:


#rename and fix dataframe columns

UK2 = UnitedKingdom.rename(columns={139: 'driving', 140: 'transit', 141:'walking'})
UK2 = UK2.drop(['transportation_type'])

##change dates on indexes (rows) to date object

UK2.index = pd.to_datetime(UK2.index)
UK2.head(2)


# In[ ]:


UK2.plot.line()
plt.title('Device movement in the UK') 
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




