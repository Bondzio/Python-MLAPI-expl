#!/usr/bin/env python
# coding: utf-8

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


data = pd.read_csv('../input/creditcard.csv')


# In[ ]:


data.info()


# In[ ]:


data.corr()


# In[ ]:


data.head()


# In[ ]:


data.tail()


# In[ ]:


data.V1


# In[ ]:


f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(data.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


data.columns


# In[ ]:


#MatPlotLib
data.V1.plot(kind = 'line', color = 'blue',label = 'V2',linewidth=1,alpha = 0.5,grid = True,linestyle = ':')
data.V2.plot(color = 'gray',label = 'V2',linewidth=1, alpha = 0.5,grid = True,linestyle = '-.')
plt.legend(loc='upper right')     # legend = puts label into plot
plt.xlabel('x axis')              # label = name of label
plt.ylabel('y axis')
plt.title('Line Plot')            # title = title of plot
plt.show()


# In[ ]:


#ScatterPlot
data.plot(kind = 'scatter',x='V1',y='V2', color = 'red',alpha = 0.5,)
plt.xlabel('V1')
plt.ylabel('V2')
plt.title('Comparing V1 and V2')


# In[ ]:


#Histogram
#bins = number of bar in figure
data.V9.plot(kind ='hist',bins=30,figsize=(12,12))
plt.show()

#Burj Khalifa is shown below


# In[ ]:


data.Amount.plot(kind='hist',bins=5)
plt.clf()


# In[ ]:


dictionary = {'Turkey': 'Ankara', 'USA': 'Washington', 'Italy' : 'Rome'}
print(dictionary.keys())
print(dictionary.values())


# In[ ]:


dictionary['Turkey'] = 'Istanbul'
print(dictionary)


# In[ ]:


dictionary['france'] = 'Paris'
print(dictionary)


# In[ ]:


del dictionary['USA']


# In[ ]:


print('france' in dictionary)
dictionary.clear()
print(dictionary)


# In[ ]:


print(dictionary)


# In[ ]:


#PANDAS
data = pd.read_csv('../input/creditcard.csv')
series = data['V1']
print(type(series))
data_frame = data[['V1']]
print(type(data_frame))








# In[ ]:


print(3>2)
print(3!=2)
#Boolean Operators
print(True and False)
print(True or False)


# In[ ]:


x = data['V1']>1.5
data[x]


# In[ ]:


def tuple_ex():
    t = (1,2,3)
    return t
a,b,c = tuple_ex()
print(a,b,c)


# In[ ]:


#Scope

x=2
def f():
    x=3
    return x
print(x)
print(f())





# In[ ]:


import builtins
dir(builtins)


# In[ ]:


def square():
    def add():
        x=2
        y=5
        z=x+y
        return z
    return add()**2
print(square())


# In[ ]:


#Default Arguments
def f(a,b=1,c=2):
    y =a+b+c
    return y 
print(f(5))
print(f(5,4,3))


# In[ ]:


#Flexible Arguments
def f(*args):
    for i in args:
        print(i)
f(1)
    


# In[ ]:


def f(**kwargs):
    for key, value in kwargs.items():
        print(key, " ", value)
        f(country = 'Spain', capital = 'Madrid', Popoulation = 1234567)
        print(key, " ", value)


# In[ ]:




