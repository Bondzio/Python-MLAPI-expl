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

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_excel("../input/csv_files/data_e28.csv", header=0)


# In[ ]:


data.head(3)


# In[ ]:


data.groupby("[dem] gender")["[dem] age"].mean()


# In[ ]:


data["[dem] country_code"].value_counts()


# In[ ]:


data["[dem] country_code"].value_counts(normalize=True, dropna=False)


# In[ ]:


list(data)


# In[ ]:


data.rename(columns=lambda c: c[c.find("]")+2:], inplace=True)


# In[ ]:


list(data)


# In[ ]:


data.lgbtq.value_counts(dropna=False)


# In[ ]:


pd.crosstab(data.lgbtq, data.government_controlled_by_elite).apply(lambda r: r/len(data), axis=1)


# In[ ]:




