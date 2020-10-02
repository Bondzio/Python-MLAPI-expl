#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt


# In[ ]:


df_victim_of_rape = pd.read_csv("../input/20_Victims_of_rape.csv")


# In[ ]:


df_victim_of_rape.shape


# In[ ]:


df_victim_of_rape.dtypes


# In[ ]:


df_victim_of_rape.head(100)


# In[ ]:


df_victim_of_rape.Area_Name.value_counts()


# In[ ]:


df_victim_of_rape.groupby(['Year','Subgroup']).Rape_Cases_Reported.value_counts().mean()


# In[ ]:


df_victim_of_rape.Rape_Cases_Reported.plot(kind='hist',bins=20);


# In[ ]:


Del_total_rape=df_victim_of_rape.loc[df_victim_of_rape['Area_Name']=='Delhi']


# In[ ]:


Del_total_rape.head(30)


# In[ ]:


Del_victim_2010_total = Del_total_rape [(Del_total_rape['Year']==2010) & (Del_total_rape['Subgroup']=='Total Rape Victims')]
Del_victim_2010_total_incest_rape = Del_total_rape [(Del_total_rape['Year']==2010) & (Del_total_rape['Subgroup']=='Victims of Incest Rape')]


# In[ ]:


Del_victim_2010_total.head()


# In[ ]:


Del_victim_2010_total_incest_rape.head()


# In[ ]:


ax=Del_victim_2010_total[['Victims_Above_50_Yrs','Victims_Between_10-14_Yrs','Victims_Between_14-18_Yrs','Victims_Between_18-30_Yrs','Victims_Between_30-50_Yrs'
                         ]].plot(kind='bar',legend=True,title='age of rape victim Delhi')
ax.set_ylabel("No of Victims")


# In[ ]:


victims_rape_2010_total = df_victim_of_rape[(df_victim_of_rape['Year']==2010) & (df_victim_of_rape['Subgroup']== 'Total Rape Victims')]
ax1 = victims_rape_2010_total['Victims_of_Rape_Total'].plot(kind='barh',figsize=(20, 15))
ax1.set_xlabel("Number of rape victims (2010)", fontsize=25)
ax1.set_yticklabels(victims_rape_2010_total['Area_Name']);

