#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime
import plotly.plotly as py
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
init_notebook_mode(connected=True)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
#print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.
proc_data = pd.read_csv(r'../input/procurement-notices.csv')
proc_data.head(10)


# In[ ]:


# datetiming deadline date
proc_data['Deadline Date'] = pd.to_datetime(proc_data['Deadline Date'])
proc_data.head(10)


# In[ ]:


# number of calls currently out
# cell with N/A deadline are currently out
proc_data[(proc_data['Deadline Date'] > pd.Timestamp.today()) |         (proc_data['Deadline Date'].isnull())].count().ID


# In[ ]:


# distribution by country
current_calls = proc_data[(proc_data['Deadline Date'] > pd.Timestamp.today())]
calls_by_country = current_calls.groupby('Country Name').size()

iplot([go.Choropleth(
    locationmode='country names',
    locations=calls_by_country.index.values,
    text=calls_by_country.index,
    z=calls_by_country.values
)])


# In[ ]:


# distribution of due dates
ax = current_calls.groupby('Deadline Date').size().plot.line(figsize = (12,6))
ax.set_title('Deadline Dates Distribution')

