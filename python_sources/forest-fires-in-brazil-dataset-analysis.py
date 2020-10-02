#!/usr/bin/env python
# coding: utf-8

# ### Context
# Forest fires are a serious problem for the preservation of the Tropical Forests. Understanding the frequency of forest fires in a time series can help to take action to prevent them. Brazil has the largest rainforest on the planet that is the Amazon rainforest.

# In[ ]:


from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import csv


# In[ ]:


dataset = pd.read_csv("../input/forest-fires-in-brazil/amazon.csv",encoding="ISO-8859-1")


# In[ ]:


dataset.info()


# In[ ]:


dataset.head(15)


# In[ ]:


dataset["month"].unique()


# In[ ]:


dataset["state"].unique()


# In[ ]:


years = dataset["year"].unique()
years


# In[ ]:


year_info = dataset[dataset["year"] == years[0]]
year_info.head(10)


# In[ ]:


states = year_info['state'].unique()
states


# In[ ]:


single_year_state = []

for state in states:
  state_name = state
  count_fire = year_info[year_info['state'] == state].number.sum()
  obj = {"state":state_name, "count_fire":count_fire}
  single_year_state.append(obj)
single_year_state


# In[ ]:


year_state_df = pd.DataFrame(single_year_state)
year_state_df


# In[ ]:


plt.figure(figsize=(10,7))
sns.set(style="whitegrid")
ax = sns.barplot(x="state",y="count_fire",data=year_state_df)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
plt.xlabel("States")
plt.ylabel("Count of fire in 1998")
plt.title("Fire Frequency Graph of 1998")
plt.show()


# ## Lets see year wise count of fire in different states. Observe in which year which state has maximum fire count

# In[ ]:


for year in years:
  year_info = dataset[dataset["year"] == year]
  states = year_info['state'].unique()

  single_year_state = []

  for state in states:
    state_name = state
    count_fire = year_info[year_info['state'] == state].number.sum()
    obj = {"state":state_name, "count_fire":count_fire}
    single_year_state.append(obj)

  year_state_df = pd.DataFrame(single_year_state)

  plt.figure(figsize=(10,7))
  sns.set(style="whitegrid")
  ax = sns.barplot(x="state",y="count_fire",data=year_state_df)
  ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
  plt.xlabel("States")
  plt.ylabel("Count of fire in {0}".format(year))
  plt.title("Fire Frequency Graph of {0}".format(year))
  plt.show()


# In[ ]:


years = dataset['year'].unique()
single_state_data = []

for year in years:
  single_year_data_df = dataset[dataset['year'] == year]
  states = single_year_data_df['state'].unique()
  for state in states:
    max_count = single_year_data_df[single_year_data_df['state'] == state].number.max()
    month = single_year_data_df[(single_year_data_df['state'] == state) & (single_year_data_df['number'] == max_count)].month.values[0]
    obj = {
        "month" : month,
        "max_count" : max_count,
        "state" : state,
        "year" : year
    }
    single_state_data.append(obj)


# In[ ]:


max_count_month_df = pd.DataFrame(single_state_data)
max_count_month_df[max_count_month_df["year"] == 1998].head()


# In[ ]:


years = dataset['year'].unique()
for year in years:
  year_wise_df = max_count_month_df[max_count_month_df["year"] == year]
  plt.figure(figsize=(10,7))
  sns.set(style="whitegrid")
  ax = sns.barplot(x="state",y="max_count",data=year_wise_df)
  ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
  plt.xlabel("States")
  plt.ylabel("Max count in {0}".format(year))
  plt.title("Fire max count frequency Graph of {0}".format(year))
  plt.show()


# In[ ]:




