#!/usr/bin/env python
# coding: utf-8

# Import useful libraries and load the dataset.

# In[1]:


import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import folium


# In[2]:


fao = pd.read_csv("../input/FAO.csv", encoding="latin1")

fao.columns = ['_'.join(c.lower().split(' ')) for c in fao.columns]


# # Did we produce more feed than food?

# According to the table, there are two types of elements, which are feed and food. In this section, we visualize the amount of food provided in each year in comparison with the amount of feed. 

# In[3]:


years = ['y' + str(year) for year in range(1961, 2014)]


# In[4]:


total_element_by_year = fao.groupby(by="element")[years].sum()
total_element_by_year.columns = [y[1:] for y in total_element_by_year.columns]


# In[5]:


plt.figure(figsize=(16, 8))
plt.plot(total_element_by_year.loc['Feed'] / 1000, label='feed', c='r')
plt.plot(total_element_by_year.loc['Food'] / 1000, label='food', c='g')
plt.xticks(rotation='vertical')
plt.xlabel("Years", fontsize=14)
plt.ylabel("Food (in millions of tonnes)", fontsize=14)
plt.legend(loc='upper left')
plt.fill_between(total_element_by_year.columns, 
                 total_element_by_year.loc['Feed'].values / 1000,
                 total_element_by_year.loc['Food'].values / 1000, 
                 color='yellow', alpha=0.5)
plt.show()


# As can be seen from the graph, the amount of food is much more than the amount of feed provided. How can we find the difference per year? 

# In[6]:


food_feed_differences = (total_element_by_year.loc["Food"] - total_element_by_year.loc["Feed"]) / 1000 
# food_feed_differences 


# # Visualize distribution of food and feed provided by continent

# In[7]:


import pycountry_convert


# In[8]:


def country_convert(name):
    """
    Given the country name, which continent is it located in?
    """
    try:
        alpha2_name = pycountry_convert.country_name_to_country_alpha2(name, cn_name_format="default")
        continent_code = pycountry_convert.country_alpha2_to_continent_code(alpha2_name)
        return pycountry_convert.convert_continent_code_to_continent_name(continent_code)
    except:
        pass


# In[9]:


keep_cols = ["area"] + years

grouped_by_area = (fao
                   .groupby(by="area")
                   [keep_cols]
                   .sum()
                   .reset_index())


# We will create a continent column which represents the continent in which the area is located in. 

# In[10]:


grouped_by_area["continent"] = grouped_by_area["area"].apply(lambda a: country_convert(a))


# In[11]:


# Checking whether all areas has its continent cell filled?
grouped_by_area[grouped_by_area['continent'].isnull()]


# In[12]:


# Filling in the remaining empty continent cells

grouped_by_area.loc[18, 'continent'] = pycountry_convert.convert_continent_code_to_continent_name('SA')

for i in [32, 33, 34, 35]:
    grouped_by_area.loc[i, 'continent'] = country_convert('China')

grouped_by_area.loc[75, 'continent'] = pycountry_convert.convert_continent_code_to_continent_name('AS')
    
grouped_by_area.loc[126, 'continent'] = pycountry_convert.convert_continent_code_to_continent_name('AS')

grouped_by_area.loc[153, 'continent'] = pycountry_convert.convert_continent_code_to_continent_name('EU')

grouped_by_area.loc[154, 'continent'] = pycountry_convert.convert_continent_code_to_continent_name('AS')

grouped_by_area.loc[169, 'continent'] = pycountry_convert.convert_continent_code_to_continent_name('SA')


# In[13]:


# Create the provision by continent table

provision_by_continent = (grouped_by_area
                          .groupby(by="continent")
                          .sum())

provision_by_continent.columns = [y[1:] for y in provision_by_continent.columns]


# In[14]:


plt.figure(figsize=(16, 8))

colors = ['red', 'green', 'blue', 'purple', 'grey', 'yellow']

for i, continent in enumerate(provision_by_continent.index):
    plt.plot(provision_by_continent.loc[continent] / 1000, 
             c=colors[i], 
             label=str(continent))

plt.title('Distribution of total food and feed provision by continent', fontsize=18)
plt.xlabel('Years', fontsize=14)
plt.ylabel('Millions of tonnes', fontsize=14)
plt.xticks(rotation='vertical')
plt.legend(loc='upper left')
plt.show()


# In[15]:


plt.figure(figsize=(16, 8))

prev_bar_heights = np.array([0] * 53)
index = provision_by_continent.columns
for i, continent in enumerate(provision_by_continent.index):
    plt.bar(index, 
            provision_by_continent.loc[continent].values / 1000, 
            bottom=prev_bar_heights,
            color=colors[i], 
            label=str(continent))
    prev_bar_heights = prev_bar_heights + provision_by_continent.loc[continent].values / 1000

plt.title('Distribution of total food and feed provision by continent', fontsize=18)
plt.xlabel('Years', fontsize=14)
plt.ylabel('Millions of tonnes', fontsize=14)
plt.xticks(rotation='vertical')
plt.legend(loc='upper left')
plt.show()


# # Find out which item is the provided with the largest amount

# In[16]:


item_code_to_item = (fao[['item_code', 'item']]
                     .drop_duplicates()
                     .set_index('item_code'))


# In[17]:


keep_cols = ['item_code'] + years

provision_by_item = (fao[keep_cols].groupby(by="item_code").sum())

provision_by_item.columns = [c[1:] for c in provision_by_item.columns]


# In[18]:


provision_by_item = (provision_by_item.merge(item_code_to_item, how='inner', left_index=True, right_index=True)
                     .reset_index(drop=True)
                     .set_index('item'))


# In[19]:


# Which item is provided with the largest amount from 1961 to 2013?
# According to the data, it is always 'Cereals'
provision_by_item.idxmax().drop_duplicates()


# # Which is the most popular product by continent?

# The most popular product is the product provided by the largest number of areas.

# In[20]:


area_to_continent = grouped_by_area[['area', 'continent']]

fao_with_continent = fao.merge(area_to_continent, left_on='area', right_on='area', how='inner')

keep_cols = ['item', 'continent', 'area']
fao_with_continent = fao_with_continent[keep_cols]

tmp = fao_with_continent.groupby(by=['continent', 'item']).count()


# In[21]:


continent_to_most_popular_product = {}

for continent in tmp.index.levels[0]:
    continent_to_most_popular_product[str(continent)] = tmp.loc[continent].idxmax().values[0]

continent_to_most_popular_product


# In[ ]:





# In[ ]:




