#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import pandas as pd
from sklearn.metrics import accuracy_score


# In[ ]:


## Load dummy data & solution
df_dummy = pd.read_csv("/kaggle/input/scl-dummy/Dummy data.csv")
df_solution = pd.read_csv("/kaggle/input/scl-dummy/Solution.csv")


# In[ ]:


df_dummy.head()


# In[ ]:


df_solution.head()


# In[ ]:


## Generate new_number value
df_res = df_dummy.copy()
df_res['new_number'] = df_res['id'] + 2


# In[ ]:


df_res.head()


# In[ ]:


## Drop number column
df_res = df_res.drop("number", axis=1)


# In[ ]:


df_res.head()


# In[ ]:


## Check accuracy
accuracy_score(df_res['new_number'], df_solution['new_number'])


# In[ ]:


## Export solution
df_res.to_csv("solution_bahy.csv", index=False)


# In[ ]:


## Test open solution before submit
pd.read_csv("/kaggle/working/solution_bahy.csv")

