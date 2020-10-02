#!/usr/bin/env python
# coding: utf-8

# In[23]:


# libraries we'll need
import pandas as pd # dataframes
from io import StringIO # string to data frame
import seaborn as sns # plotting


# In[42]:


# read in our data & convert to a data frame
data_tsv = StringIO("""city    province    position
0   Massena     NY  jr
1   Maysville   KY  pm
2   Massena     NY  m
3   Athens      OH  jr
4   Hamilton    OH  sr
5   Englewood   OH  jr
6   Saluda      SC  sr
7   Batesburg   SC  pm
8   Paragould   AR  m""")

my_data_frame = pd.read_csv(data_tsv, delimiter=r"\s+")


# In[43]:


# double check it looks correct
my_data_frame


# In[50]:


# conver to co-occurance matrix
co_mat = pd.crosstab(my_data_frame.province, my_data_frame.position)
co_mat


# In[51]:


# plot heat map of co-occuance matrix
sns.heatmap(co_mat)

