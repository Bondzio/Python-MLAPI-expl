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


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


dataset = pd.read_csv('diabetes')
dataset.head()


# In[ ]:


dataset = pd.read_csv('diabetes.csv')
dataset.head()


# In[ ]:





# In[ ]:


import pandas as pd
diabetes_csv = pd.read_csv("../input/diabetes.csv.csv")


# In[ ]:


diabetes_csv.head


# In[ ]:


diabetes_csv.shape

