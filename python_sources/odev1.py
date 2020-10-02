#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


data2=pd.read_csv('../input/novel-corona-virus-2019-dataset/covid_19_data.csv')
data2.head()


# In[ ]:


data2['Active_case']=data2['Confirmed']-data2['Deaths']-data2['Recovered']
data2.drop(['Country/Region'], axis=1)
data2


# In[ ]:


data2[['Confirmed','Recovered','Deaths']]=data2[['Confirmed','Recovered','Deaths']].astype(int)
data2.head()


# In[ ]:





# In[ ]:


Data=data2[data2['ObservationDate']==max(data2['ObservationDate'])].reset_index()
Data.head()


# In[ ]:


data3=Data[(Data['Country/Region']=='Azerbaijan')].reset_index(drop=True)
data3


# In[ ]:


data3.set_index('Country/Region')[['Confirmed','Deaths','Recovered']].plot.bar()
plt.show()


# In[ ]:


data2.Confirmed.plot(kind="line", color='r',label='Confirmed', linewidth=1, alpha=0.5, grid=True, linestyle='--',figsize=(20,20))

plt.legend(loc='upper right')
plt.xlabel('time')
plt.ylabel('per capita')
plt.show()


# In[ ]:


data2.corr()


# In[ ]:


f,ax=plt.subplots(figsize=(10,10))
sns.heatmap(data2.corr(),annot=True,linewidths=.5,fmt='.1f',ax=ax)
plt.show()


# In[ ]:


data2.plot(kind='scatter', x='Confirmed', y='Deaths', alpha=0.5, color='r',figsize=(15,15))
plt.xlabel('Confirmed')
plt.ylabel('Deaths')
plt.title('Confirmed Deaths scatter plot')
plt.show()


# In[ ]:


data2.Confirmed.plot(kind='line', color='r', alpha=0.5, linewidth=1, label='Confirmed', grid=True, linestyle='--',
                figsize=(15,15))
data2.Deaths.plot(color='g', alpha=0.5, label='Deaths', grid=True, linestyle=':', linewidth=1)
plt.legend(loc='upper right')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.show()


# In[ ]:


data2.Deaths.plot(kind='hist', bins=50, figsize=(15,15))
plt.show()


# In[ ]:


Data=data2[data2['ObservationDate']==max(data2['ObservationDate'])].reset_index()
Data.head()


# In[ ]:


data_frame1=data2[['Confirmed','Deaths','Recovered']]
data_frame1


# In[ ]:


data_frame=data2[['Confirmed']]
data_frame


# In[ ]:


series=data2['Confirmed']
series


# In[ ]:


turk=data2[data2['Country/Region']=='Turkey']
turk


# In[ ]:


turk.Confirmed.plot(kind='line', color='r', alpha=0.5, linewidth=2, label='Confirmed', grid=True, 
                    linestyle='--',figsize=(15,15))
turk.Deaths.plot(color='g', alpha=0.5, label='Deaths', grid=True, linestyle=':', linewidth=2)
turk.Recovered.plot(color='b', alpha=0.5, label='Deaths', grid=True, linestyle=':', linewidth=2)
plt.legend(loc='upper right')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.show()


# In[ ]:


azer=data2[data2['Country/Region']=='Azerbaijan']
azer


# In[ ]:





# In[ ]:


azer.Confirmed.plot(kind='line', color='r', alpha=0.5, linewidth=2, label='Confirmed', grid=True, 
                    linestyle='--',figsize=(15,15))
azer.Deaths.plot(color='g', alpha=0.5, label='Deaths', grid=True, linestyle=':', linewidth=2)
azer.Recovered.plot(color='b', alpha=0.5, label='Deaths', grid=True, linestyle=':', linewidth=2)
plt.legend(loc='upper right')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.show()


# In[ ]:


x=data2[['Deaths']]>2000
[x]


# In[ ]:


data2[np.logical_and(data2['Deaths']>200,data2['Recovered']>100)]


# In[ ]:


data2


# In[ ]:


data2[['Province/State','Country/Region']]


# In[ ]:


data2=pd.read_csv('../input/novel-corona-virus-2019-dataset/covid_19_data.csv')
data2.head()


# In[ ]:


azer=data2[data2['Country/Region']=='Azerbaijan']
azer


# In[ ]:


ukr=data2[data2['Country/Region']=='Ukraine']
ukr


# In[ ]:


turk=data2[data2['Country/Region']=='Turkey']
turk


# In[ ]:


rus=data2[data2['Country/Region']=='Russia']
rus


# In[ ]:


ulkeler=pd.concat([azer,turk,ukr,rus],axis=0, ignore_index=True)
ulkeler


# In[ ]:


ulkeler['Province/State'].value_counts(dropna=False)


# In[ ]:





# In[ ]:


data1=ulkeler
data1['Province/State'].dropna(inplace=True)


# In[ ]:


assert ulkeler['Province/State'].notnull().all()


# In[ ]:


ulkeler['Province/State'].fillna('empty', inplace=True)


# In[ ]:


assert ulkeler['Province/State'].notnull().all()


# In[ ]:


ulkeler


# In[ ]:


ulkeler.Confirmed.plot(kind='line', color='r', alpha=0.5, linewidth=2, label='Confirmed', grid=True, 
                    linestyle='--',figsize=(15,15))
ulkeler.Deaths.plot(color='g', alpha=0.5, label='Deaths', grid=True, linestyle=':', linewidth=2)
ulkeler.Recovered.plot(color='b', alpha=0.5, label='Deaths', grid=True, linestyle=':', linewidth=2)
plt.legend(loc='upper right')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.show()


# In[ ]:



ulkeler['Aktive case']=ulkeler['Confirmed']-ulkeler['Deaths']-ulkeler['Recovered']
ulkeler.drop('Province/State', axis=1)


# In[ ]:


azer=data2[data2['Country/Region']=='Azerbaijan']
azer


# In[ ]:



azer=data2[data2['Country/Region']=='Azerbaijan'].drop(['Province/State','SNo'], axis=1)
azer


# In[ ]:



azer['Aktive case']=azer['Confirmed']-azer['Deaths']-azer['Recovered']
azer.index=range(1,123)
azer


# In[ ]:


ulkeler.Confirmed.plot(kind='line', color='r', alpha=0.5, linewidth=2, label='Confirmed', grid=True, 
                    linestyle='--',figsize=(15,15))
ulkeler.Deaths.plot(color='g', alpha=0.5, label='Deaths', grid=True, linestyle=':', linewidth=2)
ulkeler.Recovered.plot(color='b', alpha=0.5, label='Deaths', grid=True, linestyle=':', linewidth=2)
plt.legend(loc='upper right')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.show()

