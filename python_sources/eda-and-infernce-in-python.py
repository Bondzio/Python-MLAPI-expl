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


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import plotly


# In[ ]:


df=pd.read_csv('../input/StudentsPerformance.csv')


# In[ ]:


df.head()


# In[ ]:


df.shape


# In[ ]:


df.describe()


# Lets visualize the marks of all the 3 subjects

# In[ ]:


fig,ax=plt.subplots(figsize=(15,10))
g=sns.countplot(ax=ax,x='math score',data=df)
plt.xticks(rotation=-45)


# Divide the marks in two category, pass and fail by setting the pass marks 40.

# In[ ]:


df['maths_pass']=np.where(df['math score']<40,'Fail','Pass')
df['reading_pass']=np.where(df['reading score']<40,'Fail','Pass')
df['writing_pass']=np.where(df['writing score']<40,'Fail','Pass')


# In[ ]:


df.head()


# Check out the total amount of student pass and fail in each subject.

# In[ ]:


fig ,ax=plt.subplots(1,3,figsize=(12,8))
sns.countplot(df['maths_pass'],hue=df['gender'],ax=ax[0])
sns.countplot(df['reading_pass'],hue=df['gender'],ax=ax[1])
sns.countplot(df['writing_pass'],hue=df['gender'],ax=ax[2])
print(df['writing_pass'].value_counts())


# In[ ]:


df['gender'].value_counts()[0]


# Based on gender it seems that female dominate the passing marks in all the three  subjects and are better than male in these subjects.

# Making the plot appear more interactive.

# In[ ]:


plotly.tools.set_credentials_file(username='abkhandelwal1998', api_key='Wad5KcBBF3eqzprJQZfO')
trace1=go.Bar(x=['Pass','Fail'],y=[df['maths_pass'].value_counts()[0],df['maths_pass'].value_counts()[1]],name='Maths Result')
trace2=go.Bar(x=['Pass','Fail'],y=[df['reading_pass'].value_counts()[0],df['reading_pass'].value_counts()[1]],name='Reading Result')
trace3=go.Bar(x=['Pass','Fail'],y=[df['writing_pass'].value_counts()[0],df['writing_pass'].value_counts()[1]],name='Writing Result')
data=[trace1,trace2,trace3]
Layout=go.Layout(barmode='group')
fig=go.Figure(data=data,layout=Layout)
py.iplot(fig)


# Let's check out the effect of parents education level on the students marks.

# In[ ]:


x_data=list(df['parental level of education'].unique())
trace1=go.Bar(x=x_data,y=df['parental level of education'].value_counts(),name='Parents Education')
layout=go.Layout(barmode='group')
fig=go.Figure(data=[trace1],layout=layout)
py.iplot(fig)


# Plot a bivariate plot to show the effect of parents education in the mathematics marks of students

# In[ ]:



df.groupby(['parental level of education','maths_pass']).size()


# In[ ]:


data_fail=[3,4,14,0,6,13]
data_pass=[219,114,182,59,220,166]


# In[ ]:


trace1=go.Bar(x=df['parental level of education'].unique(),y=data_pass,name='Pass data of Mathematics marks')
trace2=go.Bar(x=df['parental level of education'].unique(),y=data_fail,name='Fail data mathematics marks')
data=[trace1,trace2]
fig=go.Figure(data=data)
py.iplot(fig)


# In[ ]:


df.groupby(['parental level of education','reading_pass']).size()


# In[ ]:


data_fail=[2,0,7,0,7,10]
data_pass=[220,118,189,59,219,169]


# In[ ]:


trace1=go.Bar(x=df['parental level of education'].unique(),y=data_pass,name='Pass data of Reading marks')
trace2=go.Bar(x=df['parental level of education'].unique(),y=data_fail,name='Fail data Reading marks')
data=[trace1,trace2]
layout=go.Layout(barmode='group')
fig=go.Figure(data=data,layout=layout)
py.iplot(fig)


# In[ ]:


df.groupby(['parental level of education','writing_pass']).size()


# In[ ]:


data_fail=[3,2,9,0,9,9]
data_pass=[219,116,189,59,217,170]


# In[ ]:


trace1=go.Bar(x=df['parental level of education'].unique(),y=data_pass,name='Pass data of Writing marks')
trace2=go.Bar(x=df['parental level of education'].unique(),y=data_fail,name='Fail data Writing marks')
data=[trace1,trace2]
layout=go.Layout(barmode='group')
fig=go.Figure(data=data,layout=layout)
py.iplot(fig)


# From the visualizaton it is clear that the students whose parents holds the associate degree never fails in the exam.
# 

# In[ ]:





# In[ ]:





# In[ ]:




