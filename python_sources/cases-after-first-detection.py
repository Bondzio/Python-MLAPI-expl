#!/usr/bin/env python
# coding: utf-8

# ## This notebook is intended to study the low rate of case detection for the past days in Nicaragua. Opposing it to the first stages for the countries with most cases confirmed

# ## Import libraries, list files and dependencies

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ## Import Processed data file, preprocessed from the covid_19_data.csv. File was processed to normalize time periods after first detection and aggregate for these time periods. See table summary

# In[ ]:


df=pd.read_csv('/kaggle/input/weeklyinfectionsv2/Weekly Infections_v2.csv')
tablex = pd.pivot_table(df, values='Confirmed',index=["Country/Region"],columns=["Week"],fill_value=0)
tablex


# ## Plot for visuals. Thousands of cases per week after first detection. This indicates it's normal to see slow detection at first. It will take around 5-7 weeks for the spike of cases to show and increase exponentially.

# In[ ]:


figu = plt.figure(figsize=(20,6))
#  subplot #1
figu.add_subplot(121)
plt.title('1,000s of Confirmed Cases-Cumulative per Week', fontsize=14)
df["Confirmed"]=df["Confirmed"]/1000
sns.set_style("dark")
sns.axes_style("darkgrid")
sns.lineplot(x="Week",y="Confirmed",hue="Country/Region", data=df)
#  subplot #2
figu.add_subplot(122)
plt.subplot(122).set_yticklabels(tablex.index)
plt.title('1,000s of Confirmed Cases-Cumulative per Week-Heatmap', fontsize=14)
plt.pcolor(tablex,cmap='Reds')
plt.colorbar()

plt.show()


# In[ ]:




