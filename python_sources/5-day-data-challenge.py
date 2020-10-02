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

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df=pd.read_csv("../input/camera_dataset.csv")


# In[ ]:


print(df.head())


# In[ ]:


x=df.drop("Price",1)


# In[ ]:


y=df["Price"]


# In[ ]:


print(y)


# In[ ]:


import matplotlib.pyplot as plt
plt.hist(y)
plt.show()


# In[ ]:


co=x.corr(method='pearson')
print(co.head())


# In[ ]:


print(x)


# In[ ]:



for i in x.columns:
    b=x[i].corr(y)
    if b>0.6:
        print(b)


# In[ ]:




