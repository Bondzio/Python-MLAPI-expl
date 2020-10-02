#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


wine = pd.read_csv('/kaggle/input/wine-reviews/winemag-data-130k-v2.csv')
wine = wine.drop('Unnamed: 0', axis=1)


# In[ ]:


wine.head()


# In[ ]:


wine.describe()


# In[ ]:


wine['province'].value_counts().head(10).plot.bar()


# In[ ]:


(wine['province'].value_counts().head(10) / len(wine)).plot.bar()


# In[ ]:


wine['points'].value_counts().sort_index().plot.bar()


# In[ ]:


wine['points'].value_counts().sort_index().plot.line()


# <h1>Performance nas provas </h1>

# In[ ]:


students = pd.read_csv('/kaggle/input/students-performance-in-exams/StudentsPerformance.csv')
import seaborn as sns

