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


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# In[ ]:


df = pd.read_csv("../input/headbrain/headbrain.csv")


# In[ ]:


df


# In[ ]:


df.keys()


# In[ ]:


x=df.iloc[:,0:1]
y =df.iloc[:,-1]


# In[ ]:


x


# In[ ]:


y


# In[ ]:


HeadBraintrain = LinearRegression()


# In[ ]:


HeadBraintrain.fit(x,y)


# In[ ]:


m =HeadBraintrain.coef_


# In[ ]:


c =HeadBraintrain.intercept_


# In[ ]:


y_predict = m*x +c


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


y_predict =HeadBraintrain.predict(x)


# In[ ]:


h1=3597
h2=4523


# In[ ]:


w = HeadBraintrain.predict([[h1],[h2]])


# In[ ]:


plt.scatter(x,y)
plt.scatter([h1,h2],w,color=["red","black"])
plt.plot(x ,y_predict,c="blue")
plt.show()

