#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
get_ipython().run_line_magic('matplotlib', 'inline')
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


median_house_hold_in_come=pd.read_csv('../input/fatal-police-shootings-in-the-us/MedianHouseholdIncome2015.csv', encoding="windows-1252")
percentage_people_below_poverty_level=pd.read_csv('../input/fatal-police-shootings-in-the-us/PercentagePeopleBelowPovertyLevel.csv', encoding="windows-1252")
percent_over_25_completed_highSchool=pd.read_csv('../input/fatal-police-shootings-in-the-us/PercentOver25CompletedHighSchool.csv', encoding="windows-1252")
kill =pd.read_csv('../input/fatal-police-shootings-in-the-us/PoliceKillingsUS.csv', encoding="windows-1252")
share_race_city=pd.read_csv('../input/fatal-police-shootings-in-the-us/ShareRaceByCity.csv', encoding="windows-1252")


# In[ ]:


percentage_people_below_poverty_level.info()


# In[ ]:


percentage_people_below_poverty_level.poverty_rate.value_counts()


# In[ ]:


percentage_people_below_poverty_level.City.value_counts()


# In[ ]:


percentage_people_below_poverty_level['Geographic Area'].unique()


# In[ ]:


percentage_people_below_poverty_level.poverty_rate.replace(['-'],0.0,inplace = True)
percentage_people_below_poverty_level.poverty_rate = percentage_people_below_poverty_level.poverty_rate.astype(float)
area_list = list(percentage_people_below_poverty_level['Geographic Area'].unique())
area_poverty_ratio = []
for i in area_list:
    x = percentage_people_below_poverty_level[percentage_people_below_poverty_level['Geographic Area']==i]
    area_poverty_rate = sum(x.poverty_rate)/len(x)
    area_poverty_ratio.append(area_poverty_rate)
data = pd.DataFrame({'area_list': area_list,'area_poverty_ratio':area_poverty_ratio})
new_index = (data['area_poverty_ratio'].sort_values(ascending=False)).index.values
sorted_data = data.reindex(new_index)


# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x=sorted_data['area_list'], y=sorted_data['area_poverty_ratio'])
plt.xticks(rotation= 45)
plt.xlabel('States')
plt.ylabel('Poverty Rate')
plt.title('Poverty Rate Given States')


# In[ ]:


kill.head(7)


# In[ ]:


kill.name.value_counts()


# In[ ]:


separate = kill.name[kill.name != 'TK TK'].str.split() 
a,b = zip(*separate)                    
name_list = a+b                         
name_count = Counter(name_list)         
most_common_names = name_count.most_common(15)  
x,y = zip(*most_common_names)
x,y = list(x),list(y)


# In[ ]:


plt.figure(figsize=(15,10))
ax= sns.barplot(x=x, y=y,palette = sns.cubehelix_palette(len(x)))
plt.xlabel('Name or Surname of killed people')
plt.ylabel('Frequency')
plt.title('Most common 15 Name or Surname of killed people')
plt.show()


# In[ ]:


percent_over_25_completed_highSchool.columns


# In[ ]:


percent_over_25_completed_highSchool.percent_completed_hs.value_counts()


# In[ ]:


percent_over_25_completed_highSchool.percent_completed_hs.replace(["-"],0.0,inplace=True)
percent_over_25_completed_highSchool.percent_completed_hs=percent_over_25_completed_highSchool.percent_completed_hs.astype(float)
area_list=list(percent_over_25_completed_highSchool["Geographic Area"].unique())
area_highschool = []
for i in area_list:
    x=percent_over_25_completed_highSchool[percent_over_25_completed_highSchool["Geographic Area"]==i]
    area_highschool_rate=sum(x.percent_completed_hs)/len(x)
    area_highschool.append(area_highschool_rate)
    
data=pd.DataFrame({"area_list":area_list,"area_highschool_ratio":area_highschool})
new_index=(data["area_highschool_ratio"].sort_values(ascending=True)).index.values
sorted_data2=data.reindex(new_index)

plt.figure(figsize=(15,10))
sns.barplot(x=sorted_data2["area_list"],y=sorted_data2["area_highschool_ratio"])
plt.xticks(rotation=45)
plt.xlabel("States")
plt.ylabel("High School Graduate Rate")
plt.title("Percentage of Given State's Population Above 25 that Has Graduated High School")
plt.show()


# In[ ]:


share_race_city.head()


# In[ ]:


share_race_city.info()


# In[ ]:


#'(X)'
share_race_city.replace(['-'],0.0,inplace = True)
share_race_city.replace(['(X)'],0.0,inplace = True)
share_race_city.loc[:,['share_white','share_black','share_native_american','share_asian','share_hispanic']] = share_race_city.loc[:,['share_white','share_black','share_native_american','share_asian','share_hispanic']].astype(float)
area_list = list(share_race_city['Geographic area'].unique())
share_white=[]
share_black=[]
share_native_american=[]
share_asian=[]
share_hispanic=[]
for i in area_list:
    x = share_race_city[share_race_city['Geographic area']==i]
    share_white.append(sum(x.share_white)/len(x))
    share_black.append(sum(x.share_black) / len(x))
    share_native_american.append(sum(x.share_native_american) / len(x))
    share_asian.append(sum(x.share_asian) / len(x))
    share_hispanic.append(sum(x.share_hispanic) / len(x))
f,ax = plt.subplots(figsize = (9,15))
sns.barplot(x=share_white,y=area_list,color='green',alpha = 0.5,label='White' )
sns.barplot(x=share_black,y=area_list,color='blue',alpha = 0.7,label='African American')
sns.barplot(x=share_native_american,y=area_list,color='cyan',alpha = 0.6,label='Native American')
sns.barplot(x=share_asian,y=area_list,color='yellow',alpha = 0.6,label='Asian')
sns.barplot(x=share_hispanic,y=area_list,color='red',alpha = 0.6,label='Hispanic')

ax.legend(loc='lower right',frameon = True)     # legendlarin gorunurlugu
ax.set(xlabel='Percentage of Races', ylabel='States',title = "Percentage of State's Population According to Races ")


# In[ ]:


data.head()


# In[ ]:


sorted_data['area_poverty_ratio'] = sorted_data['area_poverty_ratio']/max( sorted_data['area_poverty_ratio'])
sorted_data2['area_highschool_ratio'] = sorted_data2['area_highschool_ratio']/max( sorted_data2['area_highschool_ratio'])
data = pd.concat([sorted_data,sorted_data2['area_highschool_ratio']],axis=1)
data.sort_values('area_poverty_ratio',inplace=True)
f,ax1 = plt.subplots(figsize =(20,10))
sns.pointplot(x='area_list',y='area_poverty_ratio',data=data,color='green')
sns.pointplot(x='area_list',y='area_highschool_ratio',data=data,color='red')
plt.text(40,0.6,'high school graduate ratio',color='red',fontsize = 17)
plt.text(40,0.55,'poverty ratio',color='green',fontsize = 18)
plt.xlabel('States',fontsize = 15)
plt.ylabel('Values',fontsize = 15)
plt.title('High School Graduate  VS  Poverty Rate',fontsize = 20)
plt.grid()


# In[ ]:


g = sns.jointplot(data.area_poverty_ratio, data.area_highschool_ratio, kind="kde", height=7)
plt.savefig('graph.png')
plt.show()


# In[ ]:


g = sns.jointplot("area_poverty_ratio", "area_highschool_ratio", data=data,size=5, ratio=3, color="r")


# In[ ]:


kill.race.head(11)


# In[ ]:


kill.race.value_counts()


# In[ ]:


kill.race.dropna(inplace=True)
labels=kill.race.value_counts().index
colors=["grey","blue","red","yellow","green","brown"]
explode=[0,0,0,0,0,0]
sizes=kill.race.value_counts().values
plt.figure(figsize=(7,7))
plt.pie(sizes,explode=explode,labels=labels,colors=colors,autopct='%1.1f%%')
plt.title("Killed People According to Races")
plt.show()


# In[ ]:


sns.lmplot(x="area_poverty_ratio", y="area_highschool_ratio", data=data)
plt.show()


# In[ ]:


sns.kdeplot(data.area_poverty_ratio, data.area_highschool_ratio, shade=True, cut=3)
plt.show()


# In[ ]:


pal = sns.cubehelix_palette(2, rot=-.5, dark=.3)
sns.violinplot(data=data, palette=pal, inner="points")
plt.show()


# In[ ]:


data.corr()


# In[ ]:


f,ax = plt.subplots(figsize=(5, 5))
sns.heatmap(data.corr(), annot=True,  fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


f,ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x="gender",y="age",hue="manner_of_death",data=kill,ax=ax)
plt.show()


# In[ ]:


plt.subplots(figsize=(10, 10))
sns.swarmplot(x="gender",y="age",hue="manner_of_death",data=kill)
plt.show()


# In[ ]:


sns.pairplot(data)
plt.show()


# In[ ]:


kill.gender.value_counts()


# In[ ]:


sns.countplot(kill.gender)
plt.title("Gender")
plt.show()


# In[ ]:


kill.manner_of_death.value_counts()


# In[ ]:


sns.countplot(kill.manner_of_death)
plt.title("Manner of Death")
plt.show


# In[ ]:


armed.head(7)


# In[ ]:


armed=kill.armed.value_counts()
plt.figure(figsize=(10,7))
sns.barplot(x=armed[:7].index,y=armed[:7].values)
plt.ylabel('Number of Weapon')
plt.xlabel('Weapon Types')
plt.title('Kill weapon')
plt.show()


# In[ ]:


sns.countplot(data=kill, x='race')
plt.title('Race of killed people')
plt.show()


# In[ ]:


city = kill.city.value_counts()
plt.figure(figsize=(10,7))
sns.barplot(x=city[:12].index,y=city[:12].values)
plt.xticks(rotation=45)
plt.title('Most dangerous cities')
plt.show()

