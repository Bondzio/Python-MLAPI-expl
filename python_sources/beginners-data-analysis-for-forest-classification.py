#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_profiling as pp
import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.express as px


# ### Exploratory Data Analysis

# In[ ]:


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


df_train = pd.read_csv("/kaggle/input/learn-together/train.csv", index_col='Id')
df_test = pd.read_csv("/kaggle/input/learn-together/test.csv", index_col='Id')
print(df_train.head())


# In[ ]:


df_sub = pd.read_csv("/kaggle/input/learn-together/sample_submission.csv")
print(df_sub.head())


# In[ ]:


print("Train dataset shape: "+ str(df_train.shape))
print("Test dataset shape:  "+ str(df_test.shape))


# In[ ]:


print(df_train.info())


# In[ ]:


df_train.describe().T


# In[ ]:


print(df_train.iloc[:,10:-1].columns)


# In[ ]:


pd.unique(df_train.iloc[:,10:-1].values.ravel())


# In[ ]:


df_train.iloc[:,10:-1] = df_train.iloc[:,10:-1].astype("category")
df_test.iloc[:,10:-1] = df_test.iloc[:,10:-1]. astype("category")


# In[ ]:


f, ax = plt.subplots(figsize=(8,6))
sns.heatmap(df_train.corr(), annot=True, linewidths=.5, fmt='.1f', ax=ax)
plt.show()


# It seems the most important correlations are between "Horizontal Distance To Hydrology" and "Vertical Distance To Hydrology" with 70%; between "Aspect" and "Hillshade 3pm" with 60%; between "Hillshade Noon" and "Hillshade 3pm" with %60; between "Elevation" and "Horizontal Distance To Roadways" with %60. Let's see how they are looking.

# ### Data Visualization

# In[ ]:


df_train.plot(kind='scatter', x='Vertical_Distance_To_Hydrology', y='Horizontal_Distance_To_Hydrology', alpha=0.5, color='darkblue', figsize=(12,9))
plt.title('Vertical And Horizontal Distance To Hydrology')
plt.xlabel("Vertical Distance")
plt.ylabel("Horizontal Distance")
plt.show()


# In[ ]:


df_train.plot(kind='scatter', x='Aspect', y='Hillshade_3pm', alpha=0.5, color='maroon', figsize=(12,9))
plt.title('Aspect and Hillshade 3pm Relation')
plt.xlabel("Aspect")
plt.ylabel("Hillshade 3pm")
plt.show()


# In[ ]:


df_train.plot(kind='scatter', x='Hillshade_Noon', y='Hillshade_3pm', alpha=0.5, color='purple', figsize = (12,9))
plt.title('Hillshade Noon and Hillshade 3pm Relation')
plt.xlabel("Hillshade_Noon")
plt.ylabel("Hillshade 3pm")
plt.show()


# Boxplot can use to see outliers. For a better visualization i will use plotly this time.

# In[ ]:


trace1 = go.Box(
    y = df_train["Vertical_Distance_To_Hydrology"],
    name = 'Vertical Distance',
    marker = dict(color = 'rgb(0,145,119)')
)

trace2 = go.Box(
    y=df_train["Horizontal_Distance_To_Hydrology"],
    name = 'Horizontal Distance',
    marker = dict(color = 'rgb(5, 79, 174)')
)

data = [trace1, trace2]

layout = dict(autosize=False, width=700, height=500, title='Distance To Hydrology', paper_bgcolor='rgb(243, 243, 243)',
             plot_bgcolor='rgb(243, 243, 243)', margin=dict(l=40,r=30,b=80,t=100,))

fig = dict(data=data, layout=layout)
iplot(fig)


# In[ ]:


trace1 = go.Box(
    y=df_train["Hillshade_Noon"],
    name = 'Hillshade Noon',
    marker = dict(color = 'rgb(255,111,145)')
)
trace2 = go.Box(
    y=df_train["Hillshade_3pm"],
    name = 'Hillshade 3pm',
    marker = dict(color = 'rgb(132,94,194)')
)

data = [trace1, trace2]
layout = dict(autosize=False, width=700,height=500, title='Hillshade 3pm and Noon', paper_bgcolor='rgb(243, 243, 243)', 
              plot_bgcolor='rgb(243, 243, 243)', margin=dict(l=40,r=30,b=80,t=100,))
fig = dict(data=data, layout=layout)
iplot(fig)


# This time i'll compare vertical and horizontal distance to hydrology with histogram.

# In[ ]:


f,ax=plt.subplots(1,2,figsize=(15,7))
df_train.Vertical_Distance_To_Hydrology.plot.hist(ax=ax[0],bins=30,edgecolor='black',color='crimson')
ax[0].set_title('Vertical Distance To Hydrology')
x1=list(range(-150,350,50))
ax[0].set_xticks(x1)
df_train.Horizontal_Distance_To_Hydrology.plot.hist(ax=ax[1],bins=30,edgecolor='black',color='darkmagenta')
ax[1].set_title('Horizontal Distance To Hydrology')
x2=list(range(0,1000,100))
ax[1].set_xticks(x2)


# I will take a look our categorical categorical variables soil types and wilderness areas.

# I took help from Fatih Bilgin's kernel. Thanks a lot to show us new ways for data analysis.

# To be continued...
