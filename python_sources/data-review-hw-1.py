#!/usr/bin/env python
# coding: utf-8

# # DATA REVIEW

# ** Overview**
#   
# Firstly english is not my mother tongue so some sentences have some grammer mistakes.I'm sorry for that.And this my first homework.I try to learn AI and data review second step on this path.I am grateful to DATAI for all information.We will try to do something on iris flower datas.
# We will both learn and practice with python .

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns  # visualization tool

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv('../input/Iris.csv') #We implement data package on kernel.


# In[ ]:


data.info()  #We take some basic information about datas.


# In[ ]:


data.corr() #It gives correlation.


# In[ ]:


f,ax = plt.subplots(figsize=(10, 10))
sns.heatmap(data.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


data.head()  #head() take  first 5 datas in the dataset. 


# In[ ]:


data.columns #We saw above figure these columns on table.


# # 1. INTRODUCTION TO PYTHON

# ### MATPLOTLIB
# Matplot is a python library that help us to plot data. The easiest and basic plots are line, scatter and histogram plots.
# * Line plot is better when x axis is time.
# * Scatter is better when there is correlation between two variables
# * Histogram is better when we need to see distribution of numerical data.
# * Customization: Colors,labels,thickness of line, title, opacity, grid, figsize, ticks of axis and linestyle  
# If you want to look official site is <a id="https://matplotlib.org/">matplotlib.org</a>

# In[ ]:


# Line Plot
# color = color, label = label, linewidth = width of line, alpha = opacity, grid = grid, linestyle = sytle of line

data.SepalLengthCm.plot(kind = 'line', color = 'g',label = 'SepalLengthCm',linewidth=1,alpha = 0.5,grid = True,linestyle = ':')
data.PetalLengthCm.plot(color = 'r',label = 'PetalLengthCm',linewidth=1, alpha = 0.5,grid = True,linestyle = '-.')
plt.legend(["SepalLengthCm","PetalLengthCm"])
plt.title('Line Plot')
plt.xlabel('x axis')            
plt.ylabel('y axis')
plt.subplots(1,0)

data.SepalWidthCm.plot(kind = 'line', color = 'b',label = 'SepalWidthCm',linewidth=1,alpha = 0.5,grid = True,linestyle = '--')
data.PetalWidthCm.plot(color = 'g',label = 'PetalWidthCm',linewidth=1, alpha = 0.5,grid = True,linestyle = '-')
plt.legend(["SepalWidthCm","PetalWidthCm"])
plt.title('Line Plot')
plt.xlabel('x axis')           
plt.ylabel('y axis')
plt.subplots(2,0)
plt.show()


# In[ ]:


# Scatter Plot 
# x = SepalLengthCm, y = SepalWidthCm
data.plot(kind='scatter', x='SepalLengthCm', y='PetalLengthCm',alpha = 0.5,color = 'red')
plt.xlabel('SepalLengthCm')           
plt.ylabel('PetalLengthCm')
plt.title('Length-Length Scatter Plot') 
plt.subplots(0,0)
data.plot(kind='scatter', x='SepalWidthCm', y='PetalWidthCm',alpha = 0.5,color = 'green')
plt.xlabel('SepalWidthCm')           
plt.ylabel('PetalWidthCm')
plt.title('Width-Width Scatter Plot') 
plt.subplots(0,1)
data.plot(kind='scatter', x='SepalWidthCm', y='PetalLengthCm',alpha = 0.5,color = 'yellow')
plt.xlabel('SepalWidthCm')           
plt.ylabel('PetalLengthCm')
plt.title('Length-Width Scatter Plot') 
plt.subplots(1,0)
data.plot(kind='scatter', x='SepalLengthCm', y='PetalWidthCm',alpha = 0.5,color = 'blue')
plt.xlabel('SepalLengthCm')           
plt.ylabel('PetalWidthCm')
plt.title('Width-Length Scatter Plot') 
plt.subplots(1,0)
plt.show()


# In[ ]:


# Histogram
# bins = number of bar in figure
data.SepalLengthCm.plot(kind = 'hist',bins = 50,alpha = 0.6,figsize = (20,8),color='green')
data.SepalWidthCm.plot(kind = 'hist',bins = 50,alpha = 0.6,figsize = (20,8),color='yellow')
data.PetalLengthCm.plot(kind = 'hist',bins = 50,alpha = 0.5,figsize = (20,8),color='blue')
data.PetalWidthCm.plot(kind = 'hist',bins = 50,alpha = 0.7,figsize = (20,8),color='red')
plt.legend(["SepalLengthCm","SepalWidthCm","PetalLengthCm","PetalWidthCm"])

plt.show()

