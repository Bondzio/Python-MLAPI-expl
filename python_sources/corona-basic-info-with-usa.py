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


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


data = pd.read_csv("../input/novel-corona-virus-2019-dataset/2019_nCoV_data.csv")


# In[ ]:


data.head()


# In[ ]:


data.describe()


# In[ ]:


data["Confirmed"].sum()


# In[ ]:


data.Deaths.sum()


# In[ ]:


data.Country.unique()


# In[ ]:


len(data.Country.unique())


# In[ ]:


newdata=data[(data.Country!="China")& (data.Country!="Mainland China")]


# In[ ]:


newdata[newdata.Deaths>0.0]


# In[ ]:


#usa information


# In[ ]:


datausa=newdata[newdata.iloc[:,3]=="US"]


# In[ ]:


datausa.head()


# In[ ]:


datausa[datausa.iloc[:,5]==datausa.iloc[:,5].max()]


# In[ ]:


datausa.describe()


# In[ ]:




