#!/usr/bin/env python
# coding: utf-8

# **Simple Data Exploration of Top 500 Indian Cities**
# ----------------------------------------------------

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

from subprocess import check_output

cities = pd.read_csv('../input/cities_r2.csv')


# ----------
# **States according to literacy rate**
# -------------------------------------
# 
# 
# ----------
# 
# 
# >  - Literacy rate in eastern states is higher as compared to rest of the India
# >  - 5 out of 7 states in eastern India are in top 10
# >  - Most of the northern states have low literacy rate

# In[ ]:


# States according to literacy rate
lit_by_states  = cities.groupby('state_name').agg({'literates_total': np.sum})
pop_by_states  = cities.groupby('state_name').agg({'population_total': np.sum})
literate_rate = lit_by_states.literates_total * 100 / pop_by_states.population_total
literate_rate = literate_rate.sort_values(ascending=False)

plt.subplots(figsize=(6, 6))
ax = sns.barplot(x=literate_rate, y=literate_rate.index)
ax.set_title('States according to literacy rate', size=20, alpha=0.5, color='green')
ax.set_xlabel('Literacy Rate(as % of population)', size=15, alpha=0.5, color='red')
ax.set_ylabel('States', size=25, alpha=0.5, color='red')


# ----------
# 
# 
# **States by female literacy rate**
# ----------------------------------
# 
# 
# ----------

# In[ ]:


def proportion(group, col1, col2):
    col = group[col1].sum()
    tot_pop = group[col2].sum()
    return (col * 100 / tot_pop)

prop_female_lit = cities.groupby('state_name').apply(proportion, 'literates_female', 'population_female')
prop_male_lit = cities.groupby('state_name').apply(proportion, 'literates_male', 'population_male')

summary = pd.DataFrame({'literates_female': prop_female_lit, 'literates_male':prop_male_lit})
fem_summary = summary.sort_values([('literates_female')], ascending=False)

plt.subplots(figsize=(6, 6))
ax = sns.barplot(x='literates_female', y=fem_summary.index, data=fem_summary)
ax.set_title('States by female literacy rate', size=20, alpha=0.5, color='green')
ax.set_xlabel('Female literacy Rate', size=20, alpha=0.5, color='red')
ax.set_ylabel('States', size=20, alpha=0.5, color='red')


# ----------
# 
# 
# **States by male literacy rate**
# ----------------------------------
# 
# 
# ----------

# In[ ]:


male_summary = summary.sort_values([('literates_male')], ascending=False)

plt.subplots(figsize=(6, 6))
ax = sns.barplot(x='literates_male', y=male_summary.index, data=male_summary)
ax.set_title('States by male literacy rate', size=20, alpha=0.5, color='green')
ax.set_xlabel('Male literacy Rate', size=15, alpha=0.5, color='red')
ax.set_ylabel('States', size=20, alpha=0.5, color='red')


# ----------
# **Is there any relation between sex ratio and female literacy?**
# ----------------------------------------------------------------
# ----------
# 
# 

# In[ ]:


prop_female_lit = cities.groupby('state_name').apply(proportion, 'literates_female', 'population_female')
prop_female_lit = prop_female_lit * 10
sex_ratio_by_state = cities.groupby('state_name').agg({'sex_ratio':np.mean})

prop_female_lit = pd.DataFrame({'female_lit':prop_female_lit})
df = pd.concat([prop_female_lit, sex_ratio_by_state], axis='columns')

plt.subplots(figsize=(8, 6))
ax = sns.regplot(x='sex_ratio', y='female_lit', data=df, order=3, ci=50, 
                 scatter_kws={'alpha':0.5, 'color':'red'})
ax.set_title('Female literacy vs sex ratio', size=20, alpha=0.5, color='green')
ax.set_xlabel('Sex Ratio', size=20, alpha=0.5, color='red')
ax.set_ylabel('Female literacy(per thousand)', size=20, alpha=0.5, color='red')


# ----------
# 
# 
# **Top 5 states with most literates by number**
# ----------------------------------------------
# 
# 
# ----------

# In[ ]:


# Top 5 most literate state by population
lit_by_states  = cities.groupby('state_name').agg({'literates_total': np.sum}).sort_values(
    [('literates_total')], ascending=False)[:5]
lit_by_states = lit_by_states / 1000000
plt.subplots(figsize=(8, 5))
ax = sns.barplot(data=lit_by_states, x=lit_by_states.index, y='literates_total')

ax.set_title('Top 5 states with most literates', size=25, alpha=0.5, color='green')
ax.set_xlabel('States', size=20, alpha=0.5, color='red')
ax.set_ylabel('Number of literates (millions)', size=20, alpha=0.5, color='red')


# ----------
# **States with most 500 cities**
# ----------
# -------------------------------
# 
#  - Bigger states have more cities in top 500

# In[ ]:


# states which has most top 500 cities
most_cities_in_states = cities.state_name.value_counts().sort_values(ascending=False)
plt.subplots(figsize=(5, 6))
ax = sns.barplot(x=most_cities_in_states, y=most_cities_in_states.index)

ax.set_title('States with most top 500 cities', size=20, alpha=0.5, color='green')
ax.set_xlabel('Number of cities in state', size=25, alpha=0.5, color='red')
ax.set_ylabel('States', size=25, alpha=0.5, color='red')

