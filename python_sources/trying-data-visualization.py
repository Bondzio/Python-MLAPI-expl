#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import math
get_ipython().run_line_magic('matplotlib', 'inline')
dataset = pd.read_csv("../input/2015.csv")


# In[ ]:


dataset.head()


# In[ ]:


#Let's rename Economy (blabla) to Economy
dataset = dataset.rename(columns={'Economy (GDP per Capita)': 'Economy'})


# In[ ]:


#correlation matrix
corrmat = dataset.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True);


# In[ ]:


#scatterplot
sns.set()
sns.pairplot(dataset, size = 2.5)
plt.show();


# 

# In[ ]:


sns.swarmplot(x="Region", y="Happiness Score",  data=dataset)
plt.xticks(rotation=30)


# 

# In[ ]:





# 

# In[ ]:


w_europe = dataset[dataset.Region=='Western Europe']
ec_europe = dataset[dataset.Region=='Central and Eastern Europe']
europe = pd.concat([w_europe,ec_europe],axis=0)
europe.head()


# 

# In[ ]:


sns.lmplot(data=europe,x='Economy',y='Happiness Score',hue="Region")


# 

# In[ ]:


selectCols=  ['Happiness Score','Economy','Family','Health (Life Expectancy)','Freedom','Trust (Government Corruption)','Region']
sns.pairplot(europe[selectCols], hue='Region',size=2.5)


# 

# 

# In[ ]:


f, axes = plt.subplots(3, 2, figsize=(16, 16))
axes = axes.flatten()
compareCols = ['Happiness Score','Economy','Family','Health (Life Expectancy)','Freedom','Trust (Government Corruption)']
for i in range(len(compareCols)):
    col = compareCols[i]
    axi = axes[i]
    sns.distplot(w_europe[col],color='blue' , label='West', ax=axi)
    sns.distplot(ec_europe[col],color='green', label='Central/East',ax=axi)
    axi.legend()


# 

# In[ ]:


def plot_compare(dataset,regions,compareCols):
    n = len(compareCols)
    f, axes = plt.subplots(math.ceil(n/2), 2, figsize=(16, 6*math.ceil(n/2)))
    axes = axes.flatten()
    #compareCols = ['Happiness Score','Economy','Family','Health (Life Expectancy)','Freedom','Trust (Government Corruption)']
    for i in range(len(compareCols)):
        col = compareCols[i]
        axi = axes[i]
        for region in regions:
            this_region = dataset[dataset['Region']==region]
            sns.distplot(this_region[col], label=region, ax=axi)
        axi.legend()


# In[ ]:





# In[ ]:


plot_compare(dataset,['Western Europe', 'North America', 'Australia and New Zealand',
       'Middle East and Northern Africa', 'Latin America and Caribbean',
       'Southeastern Asia', 'Central and Eastern Europe', 'Eastern Asia',
       'Sub-Saharan Africa', 'Southern Asia'],['Happiness Score','Economy','Family','Health (Life Expectancy)','Freedom','Trust (Government Corruption)'])


# 

# In[ ]:


regions = [
       'Middle East and Northern Africa', 'Latin America and Caribbean',
       'Southeastern Asia']
selectCol = ['Happiness Score','Economy','Family','Health (Life Expectancy)','Freedom','Trust (Government Corruption)']
plot_compare(dataset,regions,selectCol)


# 

# In[ ]:


regions = ['Western Europe', 'Middle East and Northern Africa',
       'Sub-Saharan Africa', 'Southern Asia']
selectCol = ['Happiness Score','Economy','Family','Health (Life Expectancy)','Freedom','Trust (Government Corruption)']
plot_compare(dataset,regions,selectCol)


# 

# <h3>Next time, we will be looking at how overall happiness change from 2015 to 2016 and what cause them.</h3>
