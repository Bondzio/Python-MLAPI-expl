#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# Here we are reading in the dataframe of hate crime that has occurred in the US since 1995 up until 2018

# In[ ]:


hate_crime_df = pd.read_csv("/kaggle/input/hate-crime-in-the-us/hate_crime.csv")
hate_crime_df


# Here are the categories by which the hate crime is distinguished:

# In[ ]:


hate_crime_df.columns


# In[ ]:


from collections import Counter

by_year= hate_crime_df.groupby(['DATA_YEAR']).TOTAL_INDIVIDUAL_VICTIMS.count()
by_year


# In[ ]:


data = {'Year':[1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
            'Victims':[4589, 6667, 7608, 5954, 7950, 8790, 8107, 7902, 7943, 8219, 9730, 7485, 7545, 7685, 7411, 7716, 7625, 8039, 6613, 6630, 6299, 6594, 6044, 5599, 5879, 6264, 6421, 6489]}
totals_df = pd.DataFrame(data, columns = ['Year', 'Victims'])
totals_df


# In[ ]:


plt.scatter(totals_df.Year, totals_df.Victims)


# In[ ]:


plt.bar([1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], [4589, 6667, 7608, 5954, 7950, 8790, 8107, 7902, 7943, 8219, 9730, 7485, 7545, 7685, 7411, 7716, 7625, 8039, 6613, 6630, 6299, 6594, 6044, 5599, 5879, 6264, 6421, 6489] )


# Here we can see the classification of hate crime based on bias against a certain race, religion, ancestry, sexual orientation, etc.

# In[ ]:


hate_crime_df.BIAS_DESC.unique()


# Here we can count the number of victims per crime involving biased motivation:

# In[ ]:


bias_df = hate_crime_df.groupby(['BIAS_DESC']).TOTAL_INDIVIDUAL_VICTIMS.count()
bias_df


# In[ ]:


fatal_encounters_df = pd.read_csv('/kaggle/input/fatal-encounters-between-police-and-civilians/FATAL ENCOUNTERS DOT ORG SPREADSHEET (See Read me tab) - Form Responses.csv')
fatal_encounters_df.columns = fatal_encounters_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
fatal_encounters_df.cause_of_death.unique()

