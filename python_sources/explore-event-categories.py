#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


dat = pd.read_csv('../input/D2014-18.csv', header=None)


# In[ ]:


dat.head()


# In[ ]:


dat.loc[:, 0] = pd.to_datetime(dat.loc[:, 0])


# In[ ]:


dat.head()


# In[ ]:


(dat.iloc[:, 2].str.strip() == 'United Kingdom').head()


# In[ ]:


dat.iloc[:, 2].head()


# In[ ]:


dat.loc[dat.loc[:, 3].str.contains('High'), 0].dt.weekday.value_counts()


# In[ ]:


dat.iloc[:, 2].value_counts()


# In[ ]:


dat.loc[dat.iloc[:, 2].str.strip() == 'United Kingdom'].iloc[:, 1].value_counts()


# In[ ]:


dat.groupby(3)[2].value_counts(normalize=True)


# In[ ]:


dat.groupby(2)[3].value_counts(normalize=True)


# In[ ]:


dat.loc[:, 4].value_counts()


# In[ ]:


dat.loc[:, 4].str.contains('CPI').sum()


# In[ ]:


dat.loc[:, 4].str.lower().str.contains(r'\bcpi\b').sum()


# In[ ]:


dat.loc[dat.loc[:, 4].str.contains('CPI') & (~dat.loc[:, 4].str.lower().str.contains(r'\bcpi\b')), 4]


# In[ ]:


dat.loc[dat.loc[:, 4].str.lower().str.contains(r'\bcpi\b'), 3].value_counts()


# In[ ]:


dat.loc[:, 4].str.lower().str.contains('consumer price index').sum()


# In[ ]:


dat.loc[:, 4].str.contains('PMI').sum()


# In[ ]:


dat.loc[:, 4].str.lower().str.contains(r'\bpmi\b').sum()


# In[ ]:


dat.loc[:, 4].str.lower().str.contains('purchasing manager\'s index').sum()


# In[ ]:


dat.loc[dat.loc[:, 4].str.lower().str.contains(r'\bpmi\b'), 3].value_counts()


# In[ ]:


dat.loc[dat.loc[:, 4].str.lower().str.contains(r'\bretail sales\b'), 3].value_counts()


# In[ ]:


dat.loc[dat.loc[:, 4].str.lower().str.contains(r'\btrade balance\b'), 3].value_counts()


# In[ ]:


dat.loc[dat.loc[:, 4].str.lower().str.contains(r'\bindustrial production\b'), 3].value_counts()


# In[ ]:


dat.groupby(3)[4].value_counts()


# In[ ]:




