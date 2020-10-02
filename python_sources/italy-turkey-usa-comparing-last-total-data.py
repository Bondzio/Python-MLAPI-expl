#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


data=pd.read_csv("/kaggle/input/covid-19-italy-updated-regularly/national_data.csv")


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


turkeydata=pd.read_csv("../input/covid19-in-turkey/covid_19_data_tr.csv")


# In[ ]:


turkeydata


# In[ ]:


data.head()


# In[ ]:


datausa=pd.read_csv("../input/covid19-in-usa/us_covid19_daily.csv")


# In[ ]:


datausa1=datausa.copy()


# In[ ]:


datausa1.positive.sort_index(ascending=False,inplace=True)
datausa1.death.sort_index(ascending=False,inplace=True)


# In[ ]:


datausa1.head(10)


# In[ ]:


plt.figure(figsize=(13,7))
sns.regplot(x=data.index,y="total_positive_cases",data=data);
sns.regplot(x=turkeydata.index,y="Confirmed",data=turkeydata);
sns.regplot(x=datausa1.index,y="positive",data=datausa1);


# In[ ]:


plt.figure(figsize=(13,7))
sns.regplot(x=data.index,y="death",data=data);
sns.regplot(x=turkeydata.index,y="Deaths",data=turkeydata);
sns.regplot(x=datausa1.index,y="death",data=datausa1);


# In[ ]:


sns.regplot(x=data.index,y="total_positive_cases",data=data);
sns.regplot(x=data.index,y="death",data=data);


# In[ ]:





# In[ ]:


sns.regplot(x=turkeydata.index,y="Deaths",data=turkeydata);
sns.regplot(x=turkeydata.index,y="Confirmed",data=turkeydata);

