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
from numpy.random import randn
from pandas import Series, DataFrame

import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sb

california_cities = pd.read_csv("../input/california-cities/california_cities.csv")
california_cities


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
rcParams['figure.figsize'] = 5, 4
sb.set_style('whitegrid')


# In[ ]:


cols = california_cities.columns.tolist()
cols


# In[ ]:


areas = california_cities["Area"]
areas


# In[ ]:


areas = areas.str.strip('sq. mile')
# areas = areas.str.strip('sq')
# areas = areas.str.strip('mi')
areas = [float(i) for i in areas]
areas


# In[ ]:


california_cities["Area"] = areas
california_cities


# In[ ]:


california_cities["Altitude"] = california_cities["Altitude"].str.strip("'")
california_cities


# In[ ]:


california_cities["Attraction"] = california_cities["Attraction"].str.replace(' and', ',')
california_cities


# In[ ]:





# In[ ]:


california_cities.rename(columns={"Area":"Area (sq. miles)", "Altitude":"Altitude (ft)"}, inplace = True)


# In[ ]:


california_cities.sort_values(by=['Area (sq. miles)'])


# In[ ]:


california_cities


# In[ ]:




