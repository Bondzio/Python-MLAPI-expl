#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


casual_df=pd.read_csv('../input/Casualties0514.csv')
accident_df=pd.read_csv('../input/Accidents0514.csv')
vehicle_df=pd.read_csv('../input/Vehicles0514.csv')


# In[ ]:


casual_df.head()


# In[ ]:


accident_df.head()


# In[ ]:


vehicle_df.head()


# In[ ]:


accident_df.info()


# In[ ]:


vehicle_df.info()


# In[ ]:


casual_df.info()


# In[ ]:


first_df=pd.merge(casual_df,accident_df,on='Accident_Index')


# In[ ]:


df=pd.merge(first_df,vehicle_df,on='Accident_Index')


# In[ ]:


df.info()


# In[ ]:


df.head()


# In[ ]:


df.isnull().sum()


# In[ ]:


df.drop('LSOA_of_Accident_Location',axis=1,inplace=True)


# In[ ]:


df.dropna(subset=['Location_Easting_OSGR','Location_Northing_OSGR', 'Longitude', 'Latitude'],axis=0,inplace=True)


# In[ ]:


df.dropna(subset=['Time'],axis=0,inplace=True)


# In[ ]:


df.isnull().values.any()


# > > > > ****The dataset is now clean and combined. Let's begin creating subframes as required to answer questions.****

# ****q1: What is the relation between hour, day, week, month with number of fatal accident?****

# In[ ]:


df.head()


# In[ ]:


#creating function to add month column
def month(string):
    return int(string[3:5])
df['Month']=df['Date'].apply(lambda x: month(x))


# In[ ]:


#creating function to add hour column
def hour(string):
    s=string[0:2]
    return int(s)
df['Hour']=df['Time'].apply(lambda x: hour(x))


# In[ ]:


#getting a dataframe as per q1
q1_df=pd.DataFrame(data=df,columns=['Hour','Day_of_Week','Month','Accident_Severity'])


# In[ ]:


q1_df.head()


# In[ ]:


#getting q1_df as per q1 i.e. getting cases of 'Fatal Accidents' only.
q1_df=q1_df[q1_df.Accident_Severity ==1]


# In[ ]:


q1_df.head()


# In[ ]:


sns.heatmap(q1_df.corr())


# **q2: Does driver age has an effect on the number of accident?**

# In[ ]:


q2_df=  pd.DataFrame(data=df, columns=['Journey_Purpose_of_Driver', 'Sex_of_Driver', 'Age_of_Driver','Age_Band_of_Driver','Driver_Home_Area_Type'])


# In[ ]:


q2_df=q2_df[q2_df.Sex_of_Driver !=-1]
q2_df.head()


# In[ ]:


map_df={1:'Journey as part of work',2:'Commuting to/from work',3:'Taking pupil to/from school',4:'Pupil riding to/from school',5:'Other',6:'Not known',15:'Not known/Other'}
map_df_age={1:'0 - 5',2:'6 - 10',3:'11 - 15',4:'16 - 20',5:'21 - 25',6:'26 - 35',7:'36 - 45',8:'46 - 55',9:'56 - 65',10:'66 - 75',11:'Over 75'}
map_df_area={1:'Urban Area',2:'Small Town',3:'Rural'}
q2_df.Age_Band_of_Driver=q2_df.Age_Band_of_Driver.map(map_df_age)
q2_df.Journey_Purpose_of_Driver=q2_df.Journey_Purpose_of_Driver.map(map_df)
q2_df.Driver_Home_Area_Type=q2_df.Driver_Home_Area_Type.map(map_df_area)
q2_df.head()


# In[ ]:


sns.heatmap(q2_df.corr())


# In[ ]:


plt.figure(figsize=(17,4))
sns.barplot('Journey_Purpose_of_Driver','Age_of_Driver',hue='Sex_of_Driver',data=q2_df,ci=None, palette='Set2')
plt.legend(bbox_to_anchor=(1,1))
plt.title('Journey Purpose of Driver vs Age_of_Driver')


# **It is seen that the Drivers who met with an accident were in the age range of 30-40 years.**
# * Usually, drivers who meet with an accident are males.

# In[ ]:


plt.figure(figsize=(12,4))
sns.boxplot('Driver_Home_Area_Type','Age_of_Driver',data=q2_df)


# **q3: How the weather impact the number or severity of an accident?**

# In[ ]:


df.head()


# In[ ]:


q3_df=pd.DataFrame(data=df,columns=['Accident_Severity','Light_Conditions','Weather_Conditions','Hour'])


# In[ ]:


q3_df.head()


# In[ ]:


#creating function to identify time of day: morning, afternoon, evening, night, etc.
def time_of_day(n):
    if n in range(4,8):
        return 'Early Morning'
    elif n in range(8,12):
        return 'Morning'
    elif n in range(12,17):
        return 'Afternoon'
    elif n in range(17,20):
        return 'Evening'
    elif n in range(20,25) or n==0:
        return 'Night'
    elif n in range(1,4):
        return 'Late Night'


# In[ ]:


q3_df['Time_of_Day']=q3_df['Hour'].apply(lambda x: time_of_day(x))


# In[ ]:


q3_df.head()


# In[ ]:


q3_df=q3_df[q3_df.Weather_Conditions!=-1]


# In[ ]:


sns.heatmap(q3_df.corr())


# In[ ]:


plt.figure(figsize=(12,6))
sns.barplot('Weather_Conditions','Hour',data=q3_df, hue='Accident_Severity',ci=None, palette='rainbow')
plt.legend(bbox_to_anchor=(1,1))
plt.title('Weather vs Hour_of_Accident')


# * 1: Fatal
# * 2: Serious
# * 3: Slight

# **Weather Conditions**
# * 1: Fine no high winds
# * 2: Raining no high winds
# * 3: Snowing no high winds
# * 4: Fine + high winds
# * 5: Raining + high winds
# * 6: Snowing + high winds
# * 7: Fog or mist
# * 8: Other
# * 9: Unknown

# In[ ]:


plt.figure(figsize=(12,4))
sns.countplot(x='Accident_Severity',data=q3_df,hue='Weather_Conditions',palette='rainbow')


# In[ ]:


df.Accident_Severity.value_counts()


# * Accidents usually take place in the afternoon: refer fig: Weather vs Hour_of_Accident
# * Accidents with Slight severity occured the most
# * **Accidents ususally took place when the Weather conditions were fine and also there were'nt any high winds** : meaning which the weather conditions didn't effectively contribute to occurences of accidents.

# **q4: Are certain car models safer than others?**

# In[ ]:


q4_df=pd.DataFrame(data=df,columns=['Vehicle_Type','Age_of_Vehicle','Was_Vehicle_Left_Hand_Drive?'
                                    ,'Propulsion_Code','Engine_Capacity_(CC)'])


# In[ ]:


q4_df=q4_df[q4_df.Vehicle_Type!=-1]
q4_df.head()


# In[ ]:


q4_df=q4_df[q4_df.Age_of_Vehicle!=-1]


# In[ ]:


q4_df=q4_df[q4_df.Propulsion_Code!=-1]


# In[ ]:


q4_df=q4_df[q4_df['Engine_Capacity_(CC)']!=-1]


# In[ ]:


map_vehicle_type={1:'Pedal cycle',
2:'Motorcycle 50cc and under',
3:'Motorcycle 125cc and under',
4:'Motorcycle over 125cc and up to 500cc',
5:'Motorcycle over 500cc',
8:'Taxi/Private hire car',
9:'Car',
10:'Minibus (8 - 16 passenger seats)',
11:'Bus or coach (17 or more pass seats)',
16:'Ridden horse',
17:'Agricultural vehicle',
18:'Tram',
19:'Van / Goods 3.5 tonnes mgw or under',
20:'Goods over 3.5t. and under 7.5t',
21:'Goods 7.5 tonnes mgw and over',
22:'Mobility scooter',
23:'Electric motorcycle',
90:'Other vehicle',
97:'Motorcycle - unknown cc',
98:'Goods vehicle - unknown weight'
}
q4_df['Vehicle_Type']=q4_df.Vehicle_Type.map(map_vehicle_type)


# In[ ]:


map_prop={1:'Petrol',
2:'Heavy oil',
3:'Electric',
4:'Steam',
5:'Gas',
6:'Petrol/Gas (LPG)',
7:'Gas/Bi-fuel',
8:'Hybrid electric',
9:'Gas Diesel',
10:'New fuel technology',
11:'Fuel cells',
12:'Electric diesel'
}
q4_df['Propulsion_Code']=q4_df.Propulsion_Code.map(map_prop)


# In[ ]:


q4_df=q4_df[q4_df['Was_Vehicle_Left_Hand_Drive?']!=-1]
q4_df.head()


# In[ ]:


plt.figure(figsize=(12,4))
sns.countplot('Vehicle_Type',data=q4_df, palette='rainbow')
plt.xticks(rotation=90)


# **Number of accidents taking place with other vehciles are almost negligible as comapred to those with Cars.**

# In[ ]:


plt.figure(figsize=(12,4))
sns.countplot('Vehicle_Type',data=q4_df, hue='Was_Vehicle_Left_Hand_Drive?', palette='Set2')
plt.xticks(rotation=90)


# **The vehicles which met with an accident were Left-Hand-Drive type of vehicles.**

# In[ ]:


plt.figure(figsize=(12,4))
sns.barplot('Vehicle_Type','Engine_Capacity_(CC)',data=q4_df, hue='Propulsion_Code', palette='Set2',ci=None)
plt.xticks(rotation=90)
plt.legend(bbox_to_anchor=(1,1))


# **Cars had low Engine Capacity with all types of fuel, which could be a possible reason for accidents.**

# >> > > > > > > > > **Let's begin with Forecasting. We have following lines to work on:**
# * Can you forecast the future daily/weekly/monthly accidents?
# * What about fatal accidents can you predict them?

# First let's begin with prediction of fatal accidents

# In[ ]:


fatal_df=pd.DataFrame(data=df,columns=['Sex_of_Driver','Age_of_Driver','Vehicle_Type','Month','Accident_Severity'])


# In[ ]:


fatal_df=fatal_df[(fatal_df.Sex_of_Driver!=-1) & (fatal_df.Vehicle_Type!=-1) & (fatal_df.Sex_of_Driver!=-1) & (fatal_df.Sex_of_Driver!=3)]
fatal_df.head()


# In[ ]:


acc=pd.get_dummies(data=fatal_df,columns=['Accident_Severity'])
sex=pd.get_dummies(data=fatal_df,columns=['Sex_of_Driver'])


# In[ ]:


sex.head()


# In[ ]:


fatal_df=pd.concat([fatal_df,acc['Accident_Severity_1'],sex['Sex_of_Driver_1']],axis=1)
fatal_df.head()


# In[ ]:


fatal_df.drop(['Accident_Severity','Sex_of_Driver'],axis=1,inplace=True)
fatal_df.head()


# **Note: Accident_Severity_1 corresponds to fatal accident and Sex_of_Driver_1 corresponds to male driver**
# 

# In[ ]:


X=fatal_df.drop('Accident_Severity_1',axis=1)
y=fatal_df['Accident_Severity_1']


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train, X_test, y_train, y_test= train_test_split(X,y)


# **Using Decision Tree**

# In[ ]:


from sklearn.tree import DecisionTreeClassifier


# In[ ]:


dtree= DecisionTreeClassifier()


# In[ ]:


dtree.fit(X_train,y_train)


# In[ ]:


predictions= dtree.predict(X_test)


# In[ ]:


from sklearn.metrics import classification_report, confusion_matrix


# In[ ]:


print(classification_report(y_test,predictions))


# **It seems like the model didn't do well**
# * Though the precision is good, it is noticed that the model had better predictions for only case:0
# * Also, checking the recall, it is noticed that case:1 is neglected.

# In[ ]:


print(confusion_matrix(y_test,predictions))


# **Hence, better data engineering is required to obtain predictions**
# 

# In[ ]:




