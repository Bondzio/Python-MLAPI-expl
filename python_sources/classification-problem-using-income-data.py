#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Importing required packages

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns


""" - NOT REQ
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.
"""


# In[ ]:


## Read the data file
df = pd.read_csv('../input/income-classification/income_evaluation.csv')
df.head()


# Let's explore the data ## I love this

# In[ ]:


df.shape


# In[ ]:


## Check data for missing values
df.isnull().sum()


# As of now we can see there is no missing values in our current data

# In[ ]:


## Let's check the variable type of each variables

df.info()


# In[ ]:


## columns name seems like with extra space - Let's check that

df.columns


# In[ ]:


## Change the column names
df.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
       'marital-status', 'occupation', 'relationship', 'race', 'sex',
       'capital-gain', 'capital-loss', 'hours-per-week', 'native-country',
       'income']


# In[ ]:


## Check basic summary of numeric and non-numeric data type - Rounding decimalplace to two
round(df.describe(),2)


# In[ ]:


## Check summary of categorical variables / Non-numeric variabls - O is object
## this will give basic idea about the unique categories in the data, frequency and 
## most frequent category(Top) - Check this out
df.describe(include = "O")


# In[ ]:


## Let's take the freq of all non numeric columns
df['education'].value_counts()


# In[ ]:


## Let's do some classical crosstab workout within the categorical variables 
## - Might get more insight about data
## this is intresting and you can do n-number of cross-tab
## for more refrence on cross tab check out this link "https://pbpython.com/pandas-crosstab.html"


pd.crosstab(df.workclass, [df.education, df.sex], margins=True, margins_name="Total")


# WIP....
