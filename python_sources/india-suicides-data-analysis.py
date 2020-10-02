#!/usr/bin/env python
# coding: utf-8

# 

# **Ending ones  own life is a very daring act,  but people who commit  suicide are cowards.  **

# ![](http://www.supportisp.org/images/pic01.jpg)

# In[ ]:



# Import necessary libraries and tools for analysis
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import os
print("The file name for the analysis is ", os.listdir("../input"))


# In[ ]:


# Read the data into dataframe
df = pd.read_csv('../input/Suicides in India 2001-2012.csv')


# In[ ]:


df.head()


# Assuming the column Total indicates number of suicides ,  the zero (0) valued rows do not offer any sense in the data set. Hence decided to truncate the data set by removing these rows

# In[ ]:


df = df[df['Total'] != 0]


# Also decided to remove age group 0-100+ as this not clear for my understanding

# In[ ]:


df = df[df['Age_group'] != '0-100+']


# In[ ]:


print ( "Number of rows are", df.shape[0])
print ( "Number of columns are", df.shape[1])


# In[ ]:


print ( " Indian states where the data is collected from ", df['State'].unique())


# In[ ]:


# column Total is number of suicides . 
# Yearwise sucides. 
yearwise= df[['Year', 'Total']].groupby('Year').sum()
yearwise.reset_index(inplace = True)
#yearwise
plt.rcParams.update({'font.size': 18})
plt.figure(figsize= (20,10)) # Make a plot size
trace = sns.barplot(x = yearwise['Year'], y = yearwise['Total'], data = yearwise)
# Adding values on the top of the bars
for index, row in yearwise.iterrows():
    trace.text(x = row.name, y = row.Total, s = str(row.Total),color='black', ha="center")
plt.title('Year wise Suicide count')    
plt.show()


# In[ ]:


round((yearwise['Total'].max() - yearwise['Total'].min())/yearwise['Total'].min()*100, 2)


# <p> <span style="color:blue">Year 2011 recorded highest suicides ( 405989)  <em> </span>.</p>
# <p> <span style="color:blue">From Year 2001 to 2011 sucides rate is increased by 24.76% <em> </span>.</p>

#  **Yearly Males , Females suicide rates**

# In[ ]:


gender_wise = df[['Year', 'Gender','Total']].groupby(['Year', 'Gender']).sum()
gender_wise.reset_index(inplace = True)
plt.rcParams.update({'font.size': 18})
plt.figure(figsize= (20,10)) # Make a plot size
plt.title('Yearly Males & Females Sucides rate')
ax = sns.barplot(x = 'Year', y = 'Total', hue = 'Gender', data = gender_wise)
plt.show()


# ** Males appear to be more vulnerable for suicide -- Reasons to be analyzed**

# Considering the data where cause of death is specified as separate set for analysis. 
# 

# In[ ]:


reasons_set = df[df['Type_code'] == 'Causes']
reasons_set['Type'].value_counts()


# 1. Some reasons seem to be repetitive need to unify the reasons to one cause 

# In[ ]:


# Category correction 
pd.options.mode.chained_assignment = None
reasons_set.loc[reasons_set['Type']=='Bankruptcy or Sudden change in Economic Status', 'Type'] = 'Bankruptcy'
reasons_set.loc[reasons_set['Type']=='Bankruptcy or Sudden change in Economic', 'Type'] = 'Bankruptcy'
reasons_set.loc[reasons_set['Type']=='Causes Not known', 'Type'] = 'Unknown'
reasons_set.loc[reasons_set['Type']=='Other Causes (Please Specity)', 'Type'] = 'Unknown'
reasons_set.loc[reasons_set['Type']=='Not having Children(Barrenness/Impotency', 'Type'] = 'Infertility'
reasons_set.loc[reasons_set['Type']=='Not having Children (Barrenness/Impotency', 'Type'] = 'Infertility'


# In[ ]:


reasons_set['Type'].value_counts()


# **Reasons and Suicides**

# In[ ]:


#df.sort_values(['job','count'],ascending=False).groupby('job').head(3)
set1 = reasons_set[['Type','Total']]
set1 = set1.groupby('Type').sum()
set1.reset_index(inplace = True)
set1 = set1.sort_values('Total', ascending = False)
set1 = set1.reset_index(drop=True)
plt.rcParams.update({'font.size': 15})
plt.figure(figsize= (20,15)) # Make a plot size
trace = sns.barplot(x = set1['Type'], y = set1['Total'], data = set1, orient = 'v')
# Adding values on the top of the bars
for index, row in set1.iterrows():
    trace.text(x = row.name, y = row.Total+ 10000, s = str(row.Total),color='black', ha="center")
plt.title('Reasons for Suicides')    
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()


# Observations :  Family Problems, Illness, Love afairs are in the top reasons list.  

# **Suicide Reasons and Gender**

# In[ ]:


# Reasons for Males suicides
gender_set = reasons_set[['Type', 'Gender', 'Total']]
male_set = gender_set[gender_set['Gender'] == 'Male']
male_set = male_set.groupby('Type').sum().reset_index()
male_set = male_set.sort_values('Total', ascending = False)
male_set = male_set.reset_index(drop=True)
plt.figure(figsize = (20,10))
male_set.plot(kind = 'bar', x = 'Type', figsize = (20,10), color = (0.3,0.1,0.4,0.6))
plt.xticks(rotation = 90)
plt.title("Males and Reasons for Suicide")
plt.show()


# In[ ]:


# Reasons for Males suicides
female_set = gender_set[gender_set['Gender'] == 'Female']
female_set = female_set.groupby('Type').sum().reset_index()
female_set = female_set.sort_values('Total', ascending = False)
female_set = female_set.reset_index(drop=True)
plt.figure(figsize = (20,10))
female_set.plot(kind = 'bar', x = 'Type', figsize = (20,10), color = (0.3,0.5,0.4,0.6))
plt.xticks(rotation = 90)
plt.title("Females and Reasons for Suicide")
plt.show()


# In[ ]:


plt.rcParams.update({'font.size': 18})
gender_set = gender_set.sort_values('Total', ascending = False)
gender_set = gender_set.reset_index(drop = True)
plt.figure(figsize= (20,10)) # Make a plot size
plt.title('India "Suicide Reasons" and "Gender" from Year 2001 to 2012')
ax = sns.barplot(x = 'Type',y = 'Total', hue = 'Gender', data = gender_set)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:





# 1. Men seem  to be more vulnerable to commit suicide. 
# 2. "Family problems" is the  major reason for all the  suicides irrespective of the  gender
# 3. Dowry Dispute is second highest reason for women to commit suicide.
# 4. Dowry Dispute , Infertility , Physical abuse are the reasons where Women suicide rate is more than men.
# 5. Love affairs  is the reason where  suicide rate is alomost same in  Men and Women.
# 
# 

# **Age Group and Reasons for Suicide**

# In[ ]:


age_set = reasons_set[['Type','Age_group','Total']]
age_grp = reasons_set['Age_group'].value_counts().index
age_grp = list(age_grp)
for x in age_grp:
    group_set = age_set[age_set['Age_group'] == x ]
    group_set =group_set.groupby('Type').sum().sort_values('Total', ascending = False)
    group_set = group_set.head(10)
    group_set.plot(kind = 'bar', figsize = (15,5), title = 'Age Group '+x+ ' Suicide Reasons')
    plt.show()


# From top 10 Reasons of each age group  the following observation were drawn
# 1. Age group 0-14, 15-29 Love affairs is one of the top ten reasons
# 2. Age group 0-14 --Failure in  Examination is the second  Strong reason -- Sad to note this.
# 3. Family Problems is the strongest reason in all the age groups --  Are we still proud of our family sytems?. 
# 4. Prolonged illness is the  strongest reason for age group Age 60+ -- This is some what anticipated
# 5. Ingeneral  illness is appearing as the strongest reason irrespective of age group and gender 
# 6. Unknown reasons are highest --  Data collection is not effective enough.  
# 

# Yearwise  Reasons count - How it is changing? 

# In[ ]:


# Year wise, how the reasons are changing 
year_reasons = reasons_set[['Year', 'Type', 'Total']]
year_reasons = year_reasons.groupby(['Type', 'Year']).sum().reset_index()
reasons = year_reasons['Type']
reasons = reasons.value_counts()
years = year_reasons['Year'].values
years  = list(years)
count = 1
reasons = list(reasons.index)
for var in reasons:
    plt.rcParams.update({'font.size': 10})
    fig = plt.figure(figsize = (10,5))
    trace1 =  year_reasons[year_reasons['Type'] == var]
    plt.plot( 'Year', 'Total', data=trace1, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=2)
    plt.title(var + '--Reason Trend')
    plt.tight_layout()
    plt.show()


# Observations :  
# 1. Drug Abuse/Addiction trend is is linearly increasing  -- More than doubled
# 2. Family problems also shows upward trend
# 3 .Unemployment trend is showing decline - Employment opportunites are growing 
# 4. Love affairs show increased trend.
# 

# **States and Suicide reasons**

# In[ ]:


states_set = reasons_set[['Type','State','Total']]
states = reasons_set['State'].value_counts().index
states = list(states)
for x in states:
    grp_set = states_set[states_set['State'] == x ]
    grp_set =grp_set.groupby('Type').sum().sort_values('Total', ascending = False)
    grp_set = grp_set.head(10)
    grp_set.plot(kind = 'bar', figsize = (15,5), title = x+ ' Suicide Reasons')
    plt.show()


# **States and overall suicides count**

# In[ ]:


state_count = df[['State','Total']]
state_count = state_count.groupby('State').sum()
state_count = state_count.sort_values('Total', ascending = False)
state_count = state_count.reset_index()
plt.figure(figsize = (20,15))
state_count.plot(kind = 'bar',x = 'State', figsize = (15,5), title = 'States and Suicide count')
plt.show()


# In[ ]:


print('Top 5 States that recorded highest number of suicides')
print(state_count.head(5))


# In[ ]:




