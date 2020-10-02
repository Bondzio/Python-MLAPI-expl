#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import re
import seaborn as sns
from matplotlib import rcParams
import matplotlib.pyplot as plt


# In[ ]:


country_death = pd.read_csv("/kaggle/input/hiv-aids-dataset/no_of_deaths_by_country_clean.csv")
country_death.head()


# In[ ]:


country_death.shape


# In[ ]:


country_death.isna().sum()


# In[ ]:


country_death = country_death.fillna(method='ffill')


# In[ ]:


country_death.isna().sum()


# In[ ]:


# country_death = country_death.dropna(how="any")


# In[ ]:


country_death


# In[ ]:


country_death.isna().sum()


# In[ ]:


def new_count(count_string):
    pattern = r'\d[0-9]*'
    final_temp = re.findall(pattern=pattern,string=count_string)
    if len(final_temp) ==0:
        temp = 0
    else:
        temp = final_temp[0]
    return temp


# In[ ]:


country_death["Count"]


# In[ ]:


# country_death["Count"] = country_death["Count"].replace("na"," ")


# In[ ]:


country_death.shape


# In[ ]:


country_death["Count"].value_counts()


# In[ ]:


country_death["value_count"] = country_death["Count"].apply(new_count)


# In[ ]:


country_death.head()


# In[ ]:


country_death["Count_median"] = country_death["Count_median"].astype(int)


# In[ ]:


set(country_death["Count_median"])


# In[ ]:


rcParams["figure.figsize"] = 60,30
sns.barplot(x=country_death["Country"],y=country_death["Count_median"])


# In[ ]:


country_sort = country_death.sort_values(by="Count_median",ascending=False)


# In[ ]:


country_sort.head()


# In[ ]:


rcParams["figure.figsize"] = 15,10
sns.barplot(x="Year",y="Count_median",data=country_sort[:50])


# In[ ]:


rcParams["figure.figsize"] = 15,10
sns.lineplot(x="Year",y="Count_median",data=country_sort[:50])


# ## Year 2000 has more death for HIV cases and later it is reduced in the coming year

# In[ ]:


sns.barplot(x="Country",y="Count_median",data=country_sort[:50])


# In[ ]:


import plotly.express as px


# In[ ]:


def plot_map(df, col, pal):
    df = df[df[col]>0]
    fig = px.choropleth(df, locations="Country", locationmode='country names', 
                  color=col, hover_name="Country", 
                  title=col, color_continuous_scale=pal,width=1500)
#     fig.update_layout(coloraxis_showscale=False)
    fig.show()


# In[ ]:


plot_map(country_death, 'Count_median', 'matter')


# In[ ]:


people_with_hiv = pd.read_csv("/kaggle/input/hiv-aids-dataset/no_of_people_living_with_hiv_by_country_clean.csv")
people_with_hiv.head()


# In[ ]:


people_with_hiv.info()


# In[ ]:


people_with_hiv.shape


# In[ ]:


people_with_hiv.isna().sum()


# In[ ]:


people_with_hiv = people_with_hiv.fillna(method='ffill')


# In[ ]:


people_with_hiv.isna().sum()


# In[ ]:


people_with_hiv.head()


# In[ ]:


people_with_hiv_sort = people_with_hiv.sort_values(by="Count_median",ascending=False)


# In[ ]:


rcParams["figure.figsize"] = 15,10
sns.barplot(x="Year",y="Count_median",data=people_with_hiv_sort[:50])


# In[ ]:


rcParams["figure.figsize"] = 15,10
sns.lineplot(x="Year",y="Count_median",data=people_with_hiv_sort[:50])


# In[ ]:


sns.barplot(x="Country",y="Count_median",data=people_with_hiv_sort[:50])


# In[ ]:


plot_map(people_with_hiv, 'Count_median', 'matter')


# In[ ]:


age_15_19 = pd.read_csv("/kaggle/input/hiv-aids-dataset/no_of_cases_adults_15_to_49_by_country_clean.csv")
age_15_19.head()


# In[ ]:


age_15_19 = age_15_19.fillna(method='ffill')


# In[ ]:


age_15_19.head()


# In[ ]:


rcParams["figure.figsize"]=15,10
sns.barplot(x=age_15_19["Year"],y=age_15_19["Count_median"])


# In[ ]:


age_15_19_sort = age_15_19.sort_values(by="Count_median",ascending=False)


# In[ ]:


rcParams["figure.figsize"]=15,10
sns.barplot(x="Country",y="Count_median",data=age_15_19_sort[:50])


# In[ ]:


sns.lineplot(x="Year",y="Count_median",data=age_15_19_sort[:50])


# In[ ]:


plot_map(age_15_19, 'Count_median', 'matter')


# In[ ]:




