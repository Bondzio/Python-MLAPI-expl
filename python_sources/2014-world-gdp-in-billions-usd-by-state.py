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


import plotly as py
import plotly.graph_objs as go
import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode,plot,iplot
init_notebook_mode(connected=True) # here we initialize notebook mode


# In[ ]:


df2=pd.read_csv("../input/world_gdp.csv")
df2.head()


# In[ ]:


# here we create another geographical plot for world data
data= dict(type = 'choropleth',
            locations = df2["CODE"],
            colorscale= 'Earth', # I use earth colorscale
            text= df2["COUNTRY"],
            z=df2["GDP (BILLIONS)"],
            colorbar = {'title':'GDP in Billions USD'})


# In[ ]:


layout=dict(title = '2014 World GDP in Billions USD by State',
              geo = dict(scope='world',
                         showlakes = True,
                         lakecolor = 'rgb(85,173,240)')
             )


# In[ ]:


go.Figure(data,layout)

