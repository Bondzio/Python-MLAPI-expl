#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
import os 
import pandas as pd

dat = pd.read_csv('../input/data-on-infantmortality/Leinhardt.csv')
dat.head()


# In[ ]:


sns.set(rc={'figure.figsize':(19.7,8.27)})
sns.heatmap(dat.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


sns.distplot(dat["income"])


# In[ ]:


sns.scatterplot(x='income',y='infant',data=dat)


# In[ ]:


sns.countplot(dat["region"])


# In[ ]:


sns.countplot(dat["oil"])


# In[ ]:


import plotly.offline as pyo
import plotly.graph_objs as go
lowerdf = dat.groupby('income').size()/dat['income'].count()*100
labels = lowerdf.index
values = lowerdf.values

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])
fig.show()


# In[ ]:


plt.figure(figsize=(10,6))
sns.catplot(x="income", y="infant", data=dat);
plt.ioff()

