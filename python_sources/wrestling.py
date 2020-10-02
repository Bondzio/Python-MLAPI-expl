#!/usr/bin/env python
# coding: utf-8

# My first notebook

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
#print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.

df = pd.read_csv('../input/database.csv')
#print(df.columns)


# In[ ]:



df.set_index = ['SCHOOL_ID','ACADEMIC_YEAR','SPORT_CODE']
#print(df.head())

#print(df.SPORT_NAME.unique())
schools= df.SCHOOL_NAME.unique()


# In[ ]:


s = 'Men\'s Wrestling'
print(s)
pd.set_option('display.max_columns', 57)
print(df.loc[(df.SPORT_NAME == s) & (df.SCHOOL_NAME == 'Princeton University'),:])

