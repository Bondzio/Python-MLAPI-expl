#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# **INTRODUCTION**

# *Coronaviruses (CoV) are a large family of viruses that cause illness ranging from the common cold to more severe diseases such as Middle East Respiratory Syndrome (MERS-CoV) and Severe Acute Respiratory Syndrome (SARS-CoV). A novel coronavirus (nCoV) is a new strain that has not been previously identified in humans. * 
# *Coronaviruses are zoonotic, meaning they are transmitted between animals and people.  Detailed investigations found that SARS-CoV was transmitted from civet cats to humans and MERS-CoV from dromedary camels to humans. Several known coronaviruses are circulating in animals that have not yet infected humans. * - From WHO Website - [coronavirus](https://www.who.int/health-topics/coronavirus)
# 
# Prayers for all those who are suffering the agony of this calamity!!

# In[ ]:


# Dataset
cov_data = pd.read_csv("../input/novel-corona-virus-2019-dataset/2019_nCoV_data.csv")


# In[ ]:


cov_data.head(20)


# In[ ]:


# Impacted Countries from the dataset
set(cov_data['Country'])


# In[ ]:


# Get the top 5 countries where the incidents were recovered
cov_data.groupby(['Country'])['Recovered'].sum().sort_values(ascending = False)[:5]


# In[ ]:


# Get the top 10 countries where most incidents were confirmed
cov_data.groupby(['Country'])['Confirmed'].sum().sort_values(ascending = False)[:10]


# **From the data, it is clear that China is the most impacted country from this virus. Let's go ahead and analyze data for China**

# In[ ]:


# Prepare dataset with only data from Mainland China
china_cov_data = cov_data[cov_data['Country'] == "Mainland China"]
china_cov_data.head()


# In[ ]:


# A simple time series for the confirmed cases in the country over last few days
confirmed_ts=china_cov_data.groupby(["Last Update"])["Confirmed"].sum()
confirmed_ts.astype('float')
plt.figure(figsize=(20,8))
plt.title('Trend of confirmed cases in Mainland China')
plt.xlabel('Timeline')
plt.ylabel('Confirmed Cases')
plt.plot(confirmed_ts);


# **Let's now see the most impacted State in China because of this virus**

# In[ ]:


# Group the confirmed cases in each state
state_level_china_data = china_cov_data.groupby(["Province/State"])["Confirmed"].sum().sort_values(ascending = False)[:10].to_frame()


# In[ ]:


# States in Mainland China with the most number of confirmed cases

plt.rcParams['figure.figsize'] = (20, 9)
plt.style.use('seaborn')

color = plt.cm.ocean(np.linspace(0, 1, 15))
state_level_china_data.plot.bar(color = color, figsize = (25, 10))

plt.title('Top regions in Mainland China with the confirmed cases',fontsize = 20)

plt.xticks(rotation = 90)
plt.show()


# Hubei, the MOST impacted city because of Corona Virus!

# In[ ]:


# PIE chart showing the significant increase in deaths with time due to this virus.
each_day_china_data = china_cov_data.groupby(["Last Update"])["Deaths"].sum().to_frame()
plt.style.use('seaborn')
each_day_china_data.plot.pie(figsize = (15, 15),subplots=True)

plt.title('Day wise deaths cases in Mainland China',fontsize = 20)
plt.xticks(rotation = 90)
plt.show()


# Thank you for reading this Kernel. A lot can be done with the dataset. Will try adding more visualizations in the coming days!
