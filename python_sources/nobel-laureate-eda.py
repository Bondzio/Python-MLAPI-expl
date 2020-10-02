#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pandas import Series
import matplotlib.pyplot as plt # For visualization
import seaborn as sns # For data Visualization
import seaborn as seabornInstance 
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


df = pd.read_csv('../input/nobel-laureates/archive.csv')


# In[ ]:


df.head()


# In[ ]:


# Let's check the columns
df.keys()


# In[ ]:


# Let's check the data types
df.info()


# In[ ]:


# Let's use value_counts() to determine the frequency of the values present in one particular column
bc = df['Birth Country'].value_counts()


# In[ ]:


bc.head(15)


# So It shows US tops the list with 276 winners followed by UK and Germany

# In[ ]:


# Let's plot it 
sns.countplot(bc)


# In[ ]:


# Let's see how winners year wise disctributed
df["Year"].plot.hist(bins = 100)


# Note: As we know due to World war II there was no winners in 40's

# In[ ]:


# Let's check the birth Cities
bb = df['Birth City'].value_counts()


# In[ ]:


# Top 15 cities with max nobel laureate
bb.head(15)


# Again New York tops the list with 48 winners followed by Paris and London
# Some surprise names in top 10 list Hamburg and Milwaukee

# In[ ]:


# Let's plot it and than see
sns.countplot(bb)


# In[ ]:


# with normalize=True, the object returned contains the relative 
# frequencies of unique values (* 100 to get %ge)
round(df['Birth Country'].value_counts(normalize=True) * 100,2)


# The result shows 29% winners from US followed by UK, Germany and France

# In[ ]:


# extract a subset of the data from a DataFrame to display multiple columns, rows
df_cat = df[['Prize','Category','Sex','Birth Country']]


# In[ ]:


df_cat.head()


# In[ ]:


# Let's use value_counts() to determine the frequency of the values present in Sex column
df_cat['Sex'].value_counts()


# In[ ]:


sns.countplot(df_cat['Sex'])


# In[ ]:


# Let's check the percentage
# with normalize=True, the object returned contains the relative 
# frequencies of unique values (* 100 to get %ge)
round(df_cat['Sex'].value_counts(normalize=True) * 100,2)


# In[ ]:


# crosstab() computes a simple cross-tabulation of two (or more) factors let's check for Sex
pd.crosstab(df_cat.Sex, df_cat.Category)


# In[ ]:


# using isnull(), sum(), sort_values(), count() to get the total missing values and % missing for the features
# I am using sort_values() and head() on the output because we don't need to see all features, many have no missing values
total_missing = df.isnull().sum().sort_values(ascending=False)
col_pct_missing = round(df.isnull().sum()/df.isnull().count()*100, 1).sort_values(ascending=False)
missing_data = pd.concat([total_missing, col_pct_missing], axis=1, keys=['Total Missing', '% Missing'])
missing_data.head(7)


# In[ ]:


# Let's check the Prize share
c = sns.FacetGrid(df, col='Prize Share')
c.map(plt.hist, 'Category', bins=20)


# In[ ]:


# Let's see the Category by Sex
g = sns.FacetGrid(df_cat, col='Sex')
g.map(plt.hist, 'Category', bins=12)


# In[ ]:


# Let's check the winners by County of birth by Category
l = sns.FacetGrid(df_cat, col='Category')
l.map(plt.hist, 'Birth Country', bins=10)


# In[ ]:


# Category by Birth Date
m = sns.FacetGrid(df, col='Category')
m.map(plt.hist, 'Birth Date', bins=10)


# In[ ]:


#plot distributions of winners by Death Country
a = sns.FacetGrid( df, hue = 'Death Country', aspect=4 )
a.map(sns.kdeplot, 'Year', shade= True )
a.set(xlim=(0 , df['Year'].max()))
a.add_legend()


# In[ ]:


# Let's check the winners over the years
df['Year'].plot(legend=True,figsize=(15,5))


# In[ ]:


# How about winners by Category
sns.countplot(df['Category'])


# In[ ]:


# Another way to see it
df["Category"].value_counts(sort = False).plot.bar()


# In[ ]:


# Winners by Prize
sns.countplot(df['Prize'])


# In[ ]:


#Let's check the comparison of sex, Category, and Year with the help of histogram
h = sns.FacetGrid(df, row = 'Sex', col = 'Category', hue = 'Sex')
h.map(plt.hist, 'Year', alpha = .75)
h.add_legend()


# In[ ]:


# Let's check by Laureate Type
sns.countplot(df['Laureate Type'])


# In[ ]:


# Another way
df["Laureate Type"].value_counts(sort = False).plot.bar()


# In[ ]:


# Let's check by Organization 
on = df['Organization Name'].value_counts()
on.head()


# Graph shows the top 5 Organizations (all Universities) with maximum number of winners

# In[ ]:


sns.countplot(on)


# In[ ]:


# Let's see Prize share distribution
df["Prize Share"].value_counts(sort = False).plot.bar()


# In[ ]:


# Let's see winners by Birth City and Category
df.groupby(["Birth City", "Category"]).size()


# In[ ]:


That's all I tried whatever learnt from Kaggle data Visualization so far. 
Love to hear feedback on the same to improve it further. 

