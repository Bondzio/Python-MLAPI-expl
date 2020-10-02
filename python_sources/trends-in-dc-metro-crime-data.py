#!/usr/bin/env python
# coding: utf-8

# # Plotting Basic Trends

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# Load and examine the dataset
df = pd.read_csv('../input/crime_homicide_subset.csv', encoding='latin1', sep=',')
df.head(5)


# In[ ]:


# Examine available columns
df.columns.tolist()


# In this notebook, we'll have a look at broad trends in the data by examining the reported crimes as a function of year, month, time of day, and offense. Running Version 3 contains only a subset of the data so not all types of offenses are present.

# In[ ]:


g = sns.factorplot(x='year', data=df, kind='count', size=6)
g.set_axis_labels('Year', 'Number of Crimes')


# In[ ]:


g = sns.factorplot(x='mont', data=df, kind='count', size=6)
g.set_axis_labels('Month', 'Number of Crimes')


# In[ ]:


g = sns.factorplot(x='OFFENSE', data=df, kind='count', size=6)
g.set_axis_labels('Offense', 'Number of Crimes')
g.set_xticklabels(rotation=90)


# In[ ]:


g = sns.factorplot(x="year", hue="OFFENSE", data=df, size=6, kind="count")
g.set_axis_labels('Year', 'Number of Crimes')


# In[ ]:


g = sns.factorplot(x='year', hue="SHIFT", data=df, kind='count', size=6)
g.set_axis_labels('Year', 'Number of Crimes')

