#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_notebook, show 


# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


info = "../input/vietnam-covid19-patient-dataset/Vietnam_province_info.csv"
data = pd.read_csv(info)


# In[ ]:


data.head()


# In[ ]:


data.columns


# In[ ]:


data.describe


# In[ ]:


data.isnull().sum()


# In[ ]:


data.ndim


# In[ ]:


data.tail()


# In[ ]:


data['Lat'].hist(bins=20)


# In[ ]:


data['Long'].hist(bins=40)


# In[ ]:


data.boxplot(column='Long', by = 'Lat')


# In[ ]:


plt.scatter(x=data['Lat'], y=data['Long'], label='stars' ,color= 'r' , marker='*', s=30)
plt.show()


# In[ ]:


plt.scatter(x=data['Long'], y=data['Lat'], label='stars' ,color= 'm' , marker='*', s=50)
plt.show()


# In[ ]:


data = pd.DataFrame(data, columns = ['Province/State', 'Region code', 'Country/Region', 'Lat', 'Long'])
data.hist()
plt.show()


# In[ ]:


data.plot.bar() 

# plot between 2 attributes 
plt.bar(data['Lat'], data['Long']) 
plt.xlabel("Lat") 
plt.ylabel("Long") 
plt.show() 


# In[ ]:


data.plot.box() 
# individual attribute box plot 
plt.boxplot(data['Lat']) 
plt.show() 


# In[ ]:


data.plot.box() 

# individual attribute box plot 
plt.boxplot(data['Long']) 
plt.show() 


# In[ ]:


plt.pie(data['Lat'],autopct ='% 1.1f %%', shadow = True)  
plt.show()  


# In[ ]:


plt.pie(data['Long'],autopct ='% 1.1f %%', shadow = True) 
plt.show() 


# In[ ]:


p = figure(plot_width = 10, plot_height = 10) 
p.circle(x=data['Lat'], y=data['Long'],size = 10, color = "navy", alpha = 0.5) 
show(p) 

