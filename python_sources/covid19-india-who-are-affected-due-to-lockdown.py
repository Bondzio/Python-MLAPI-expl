#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
data= pd.read_csv('../input/covid19india/data.csv')
data.head()


# In[ ]:


with sns.axes_style('white'):
    g = sns.factorplot(y ="detected_state", data=data, aspect=1.5,
                       kind="count", color='red', height=8, hue='gender')
    g.set_xticklabels(step=1)
plt.figure(figsize=(16,6))


# In[ ]:


from datetime import date
data['diagnosed_date'] = pd.to_datetime(data['diagnosed_date']).dt.strftime("%Y%m%d")
data['status_change_date'] = pd.to_datetime(data['status_change_date']).dt.strftime("%Y%m%d")
x = (data['diagnosed_date'])
x
y = (data['status_change_date'])
#data['Difference'] = x.sub(y, axis=0)


# In[ ]:


age = data.loc[(data.age >= 91.0) & (data.age<=100.0), ['id']]
age.count()


# **0 - 10  14 cases**
# 
# **11 - 20 44 cases** 
# 
# **21 - 30 129 cases**
# 
# **31 - 40 94 cases**
# 
# **41 - 50 66 cases**
# 
# **51 - 60 74 cases**
# 
# **61 - 70 58 cases**
# 
# **71 - 80 9 cases**
# 
# **81 - 90 4 cases**
# 
# **90 - 100 1 cases**

# In[ ]:


df = pd.DataFrame([14,44,129,94,66,74,58,9,4,1], index=['0-10', '11-20', '21-30', '31-40', '41-50'
, '51-60', '61-70', '71-80', '81-90', '91-100'], columns=['x'])
 
# make the plot
df.plot(kind='pie', subplots=True, figsize=(8, 8))


# In[ ]:


x = data.groupby('current_status').count()
first =data.loc[data.current_status=='Deceased',['id']]
y = first.count()
y


# In[ ]:


Male = (data['current_status'] == 'Deceased') & (data['gender'] == 'Female')
Male = len(data.loc[Male])
Male


df = pd.DataFrame([18,31,975], index=['Deceased', 'Recovered', 'Hospitalized'], columns=['x'])
 
# make the plot
df.plot(kind='pie', subplots=True, figsize=(8, 8))


# 
# Deceased - 18 Male - 14 Female - 4
# 
# Recovered - 31. Male - 17 Female - 7
# 
# Hospitalized - 975 Male - 308 Female - 165

# In[ ]:


School = (data['diagnosed_date'] > '2020-01-30') & (data['diagnosed_date'] <= '2020-03-08') 
School = len(data.loc[School])
Public = (data['diagnosed_date'] > '2020-01-30') & (data['diagnosed_date'] <= '2020-03-12')
Public = len(data.loc[Public])
WFH = (data['diagnosed_date'] > '2020-01-30') & (data['diagnosed_date'] <= '2020-03-15')
WFH = len(data.loc[WFH])
Lockdown = (data['diagnosed_date'] > '2020-01-30') & (data['diagnosed_date'] <= '2020-03-28') 
Lockdown = len(data.loc[Lockdown])


# In[ ]:


CaseCount = [School,Public,WFH,Lockdown]
labels = ['schools shutdown','public places shutdown',
            'work from home started','country under lockdown']
dates = ['2020-03-09','2020-03-13','2020-03-15','2020-03-28']


# In[ ]:


plot = pd.DataFrame({'dates':dates,'Labels': labels, 'CaseCount': CaseCount})
plot


# In[ ]:


with sns.axes_style('white'):
    g = sns.factorplot(y ="dates", x = CaseCount, data=plot, aspect=1, color='blue', height=5, hue='Labels')
    g.set_xticklabels(step=1)


# In[ ]:


data['diagnosed_date'] = pd.to_datetime(data['diagnosed_date'])
data['status_change_date'] = pd.to_datetime(data['status_change_date'])
data['days'] = data['diagnosed_date'] - data['status_change_date']
Male = (data['current_status'] == 'Recovered')
first = (data.loc[Male])


# # **Average number of days to recover is 13 days**

# 
