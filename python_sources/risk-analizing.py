#!/usr/bin/env python
# coding: utf-8

#  <h1>1 [Data preprocessing](#dp)<h1>
#  <h1>2 [Correlation map](#mcm)<h1>

# <a id="dp"><h2>Data preprocessing<h2></a>

# <h3>Importing libraries <h3>

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import seaborn as sns
from matplotlib import pyplot
from matplotlib import rcParams
import seaborn as sns
import matplotlib.pyplot as pl


# <h3>Reading and cleaning data<h3>

# In[ ]:


df=pd.read_csv("../input/restaurant-and-market-health-inspections.csv")
total = df.isnull().sum().sort_values(ascending=False)
percent = (df.isnull().sum()*100/df.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(20)


# In[ ]:


df.columns.values


# 
# 
# <h3>Choosing column to  work with. If there are to many different values (more than 700) than it will be impossible to get dummy variables<h3>
# 
# 

# In[ ]:


print('serial_number ',df.serial_number.unique().shape)
print('activity_date ',df.activity_date.unique().shape)
print('facility_name ',df.facility_name.unique().shape)#to remove
print('score ',df.score.unique().shape)
print('grade ',df.grade.unique().shape)
print('service_code ',df.service_code.unique().shape)
print('service_description ',df.service_description.unique().shape)
print('employee_id ',df.employee_id.unique().shape)
print('facility_address ',df.facility_address.unique().shape)#to remove
print('facility_id',df.facility_id.unique().shape)#to remove
print('facility_state',df.facility_state.unique().shape)#to remove
print('facility_zip',df.facility_zip.unique().shape)
print('owner_id ',df.owner_id.unique().shape)#to remove
print('owner_name',df.owner_name.unique().shape)#to remove
print('pe_description',df.pe_description.unique().shape)#VIP
print('program_element_pe',df.program_element_pe.unique().shape)#VIP
print('program_name',df.program_name.unique().shape)
print('program_status',df.program_status.unique().shape)
print('record_id',df.record_id.unique().shape)


# In[ ]:


df=df.sort_values(by=['facility_name'])
fe_v=df.loc[:,'facility_name'].values
print(fe_v[0:20])


# 
# <h3>There are 11681 unique restaurants which were noticed 4-7 times and while noting they changed parameters, like adress.<h3>
# 

# In[ ]:


fd=df.sort_values(by=['owner_id'])
fd.head(20)


# <h3>We have to drop repeting values<h3>

# In[ ]:


df_nd=df.drop_duplicates('owner_id',keep='first')
df_nd=df_nd.drop_duplicates('owner_name',keep='first')
df_nd.head()


# In[ ]:


print('serial_number ',df_nd.serial_number.unique().shape)
print('activity_date ',df_nd.activity_date.unique().shape)
print('facility_name ',df_nd.facility_name.unique().shape)#to remove
print('score ',df_nd.score.unique().shape)
print('grade ',df_nd.grade.unique().shape)
print('service_code ',df_nd.service_code.unique().shape)
print('service_description ',df_nd.service_description.unique().shape)
print('employee_id ',df_nd.employee_id.unique().shape)
print('facility_address ',df_nd.facility_address.unique().shape)#to remove
print('facility_id',df_nd.facility_id.unique().shape)#to remove
print('facility_state',df_nd.facility_state.unique().shape)#to remove
print('facility_zip',df_nd.facility_zip.unique().shape)
print('owner_id ',df_nd.owner_id.unique().shape)#to remove
print('owner_name',df_nd.owner_name.unique().shape)#to remove
print('pe_description',df_nd.pe_description.unique().shape)#VIP
print('program_element_pe',df_nd.program_element_pe.unique().shape)#VIP
print('program_name',df_nd.program_name.unique().shape)
print('program_status',df_nd.program_status.unique().shape)
print('record_id',df_nd.record_id.unique().shape)


# <h3> It looks like facility_id, owner_ide and owner name it is the same value except some "bad values"<h3>
# <h3> Also program_name and facility_name are the same<h3>

# In[ ]:


df2=df_nd[['score','grade','service_code','service_description','employee_id',
        'pe_description','program_element_pe','program_status','facility_zip','owner_id','facility_address']].copy()


# In[ ]:


df2['facility_zip'] = df2['facility_zip'].str.extract('(\d+)', expand=False)
df2['facility_zip']=pd.to_numeric(df2['facility_zip'])  
df2['owner_id'].astype(str) 
df2['owner_id'] = df2['owner_id'].str.extract('(\d+)', expand=False)
df2['owner_id']=pd.to_numeric(df2['owner_id'])  
df2['employee_id'].astype(str) 
df2['employee_id'] = df2['employee_id'].str.extract('(\d+)', expand=False)
df2['employee_id']=pd.to_numeric(df2['employee_id'])     


# In[ ]:


df2.head()


# **It is not clear if in service code there is only few values >1 and it is bad data or real data**

# In[ ]:


df_sc=df[df.service_code>1]
df_sc.loc[:,'service_code'].values.shape


# In[ ]:


df2.info()


# In[ ]:


df2 = pd.get_dummies(df2, prefix='grade_', columns=['grade'])
df2 = pd.get_dummies(df2, prefix='pe_description_', columns=['pe_description'])
df2 = pd.get_dummies(df2, prefix='program_status_', columns=['program_status'])


# <a id="mcm"><h2>Making correlation martix<h2></a>

# In[ ]:




f, ax = pl.subplots(figsize=(10, 8))
corr = df2.corr()
sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax)


# 1. Score is vell corelated with grade A and pe_description_low risk in three categories
# 1. Grade A is not corelated with risk- it is not good parameter to distinguish risk
# 1. Program_element_pe is much often korelate with hi risk

# Getting back to original df data- let us look how score is changing in time

# In[ ]:


df_1=df.sort_values(by=['owner_id'])
df_1['year']=df_1.activity_date.str[0:4]
df_1['year']=pd.to_numeric(df_1['year'])  
df_1['month']=df_1.activity_date.str[5:7]
df_1['month']=pd.to_numeric(df_1['month'])  
df_1['date']=df_1['year']+df_1['month']/12


# In[ ]:


df_1.head()


# In[ ]:


ax = sns.boxplot(x="year", y="score",data=df_1, palette="Set3")


# In[ ]:


ax1 = sns.boxplot(x="date", y="score",data=df_1, palette="Set3")


# It looka like in 2018 both average score was slightly higher than before 
