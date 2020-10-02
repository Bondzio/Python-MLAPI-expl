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


# # THIS CODE GIVES GRAPHICAL REPRESENTATION OF ANY DATA (X,Y)

# In[ ]:


import pandas as pd
df=pd.read_csv("../input/random-linear-regression/test.csv")
df


# In[ ]:


df.keys()
from sklearn.linear_model import LinearRegression
machinebrain=LinearRegression()
x=df.iloc[:,0:1].values #converts x into 2D format
y=df.iloc[:,1].values #converts y into 1D format
machinebrain.fit(x,y)
m=machinebrain.coef_
c=machinebrain.intercept_
y_predict=m*x+c  #This is the straight line equation which plots the slope & intercept values.
import matplotlib.pyplot as plt
plt.scatter(x,y)
plt.plot(x,y_predict,c="red")
plt.show()


# # IF WE GIVE ANY INPUT IT WILL GIVE PREDICTED VALUE USING (X,Y) DATA REPRESENTED IN GRAPH

# In[ ]:


h = 10
w = machinebrain.predict([[h]])
plt.scatter(x,y)
plt.plot(x,y_predict, c="yellow")
plt.scatter([h],w,c="orange")
plt.xlabel("x")
plt.ylabel("y")
plt.show()


# # The Point which is of Orange color on the plot,is the new added/predicted value to the present data
