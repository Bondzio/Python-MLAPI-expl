#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


data = pd.read_csv("/kaggle/input/covid19-in-india/covid_19_india.csv")
indiv = pd.read_csv("/kaggle/input/covid19-in-india/IndividualDetails.csv")
age_grp = pd.read_csv("/kaggle/input/covid19-in-india/AgeGroupDetails.csv")
statewise = pd.read_csv("/kaggle/input/covid19-in-india/StatewiseTestingDetails.csv")
icmr = pd.read_csv("/kaggle/input/covid19-in-india/ICMRTestingLabs.csv")
hospital = pd.read_csv("/kaggle/input/covid19-in-india/HospitalBedsIndia.csv")
data.head()


# # DATA CLEANING

# There are no missing or null values but there are hyphens in ConfirmedIndianNational and ConfirmedForeignNational ... so we need to replace them with 0.

# In[ ]:


data['ConfirmedForeignNational'].replace("-","0")
data['ConfirmedIndianNational'].replace("-","0")


# In[ ]:


import re
data=data.replace(to_replace='\#',value='', regex=True)
data['State/UnionTerritory'].value_counts()


# In[ ]:


data.tail(40)


# **here we can see that in last 36 columns data is addition of previous data...**

# # Calculating total cases confirmed,cured,deaths 

# In[ ]:


Confirmed = data.iloc[-36:-1]['Confirmed'].sum()
Cured = data.iloc[-36:-1]['Cured'].sum()
Deaths = data.iloc[-36:-1]['Deaths'].sum()
print("CONFIRMED CASES = " , Confirmed)
print("PATIENTS CURED = " , Cured)
print("TOTAL DEATHS = " , Deaths)


# **DEATH RATE AND CURE RATE**

# In[ ]:


death_rate = (Deaths/Confirmed)*100
cure_rate = (Cured/Confirmed)*100
print("DEATH RATE = ",death_rate)
print("CURE RATE = ",cure_rate)


# **STATEWISE classification of confirmed cases ,cured , deaths**

# In[ ]:


state_Confirm = data.groupby('State/UnionTerritory').max()[['Confirmed']]
state_Confirm = state_Confirm.sort_values('Confirmed',ascending=False)
state_Confirm.head()


# In[ ]:


state_Cure = data.groupby('State/UnionTerritory').max()[['Cured']]
state_Cure = state_Cure.sort_values('Cured',ascending=False)
state_Cure.head()


# In[ ]:


state_Deaths = data.groupby('State/UnionTerritory').max()[['Deaths']]
state_Deaths = state_Deaths.sort_values('Deaths',ascending=False)
state_Deaths.head()


# *MAHARASHTRA IS THE MOST EFFECTED AS WE CAN SEE FROM THE ABOVE TABLES*
# 

# In[ ]:


icmr = pd.read_csv("/kaggle/input/covid19-in-india/ICMRTestingLabs.csv")
hospital = pd.read_csv("/kaggle/input/covid19-in-india/HospitalBedsIndia.csv")
indiv = pd.read_csv("/kaggle/input/covid19-in-india/IndividualDetails.csv")
statewise = pd.read_csv("/kaggle/input/covid19-in-india/StatewiseTestingDetails.csv")


# **GENDERWISE ANALYSIS**

# In[ ]:


indiv['gender'].value_counts()


# # INSIGHTS

# **AGE GROUP WISE ANALYSIS**

# In[ ]:


age_grp = pd.read_csv("/kaggle/input/covid19-in-india/AgeGroupDetails.csv")
plt.figure(figsize=(14,8))
x = age_grp['AgeGroup']
y = age_grp['TotalCases']
plt.bar(x,y,color='blue')
plt.title("AGE GROUP ANALYSIS",  fontsize = 20)


# *Here, we can conclude that age span of 20-29 are mostly infected in INDIA*

# **RATE OF INCREASE IN CONFIRMED CASES , CURED CASES AND DEATHS**

# In[ ]:


# convert date string to dataframe pandas
data['Date'] = pd.to_datetime(data['Date'],dayfirst=True)
data1=data.groupby('Date').sum()
data1.reset_index(inplace=True)


# In[ ]:


plt.figure(figsize= (10,6))
plt.xticks(rotation = 90 ,fontsize = 10)
plt.yticks(fontsize = 10)
p1 = plt.plot_date(data=data1,y= 'Confirmed',x= 'Date' ,linestyle ='-',color = 'm')
p2 = plt.plot_date(data=data1,y= 'Cured',x= 'Date' ,linestyle ='-',color = 'r')
p3 = plt.plot_date(data=data1,y= 'Deaths',x= 'Date' ,linestyle ='-',color = 'k')
plt.title("TOTAL ANALYSIS",  fontsize = 20)
plt.legend()


# **STATEWISE CONFIRMED CASES **

# In[ ]:


data_dict=data['State/UnionTerritory'].value_counts().to_dict()
data_dict


# **WE NEED TO SUM ALL THE VALUES AS DATA IS CUMULATIVE**

# In[ ]:


dict={}
for i in data_dict:
    data_loc=data[data['State/UnionTerritory'].str.contains(i)]
    #li.append(data_loc["Confirmed"].max())
    dict.update({i:data_loc["Confirmed"].max()})
    
dict


# **WE WILL NEED SEPERATE LISTS IN ORDER TO PLOT A PIE CHART**

# In[ ]:


dict_keys=dict.keys()
print(dict_keys,'\n')

dict_values=dict.values()
print(dict_values)


# In[ ]:


plt.figure(figsize= (25,12))
label = dict_keys
vals = dict_values
plt.pie(vals,labels=label)
plt.show()


# In[ ]:


plt.figure(figsize=(15,8))
plt.bar(dict_keys , dict_values , color = 'green')
plt.xticks(rotation = 90)
plt.show()


# **ANALYSIS OF CASES CURED AND DEATHS**

# In[ ]:


State = list(set(data['State/UnionTerritory'].values.tolist()))
State.sort()
print(State)


# In[ ]:


#we will use state_Cure table we made to analyse total cured cases statewise
print(state_Cure.head())
fig = plt.figure(figsize=(20,10))
plt.bar(x=np.arange(1,38),height=state_Cure['Cured'],color='blue')
plt.xticks(np.arange(1,38),State, rotation=90)
plt.title('CURED CASES' , fontsize = 20)


# In[ ]:


#we will use state_Death table we made to analyse total deaths statewise
print(state_Cure.head())
fig = plt.figure(figsize=(20,10))
plt.bar(x=np.arange(1,38),height=state_Deaths['Deaths'],color='Red')
plt.xticks(np.arange(1,38),State, rotation=90)
plt.title('DEATHS' , fontsize = 20)


# # *PLEASE GIVE A UPVOTE IF THIS IS SOMEHOW HELPFUL*

# In[ ]:




