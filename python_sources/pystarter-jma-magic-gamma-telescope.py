#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math as mt
import itertools
import scipy

from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore")


# In[ ]:


for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


nRowsRead = 1000 # specify 'None' if want to read whole file
# free1.csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df1 = pd.read_csv('../input/magic-gamma-telescope-data/MAGIC Gamma Telescope Data.csv', delimiter=',', nrows = nRowsRead)
df1.dataframeName = 'MAGIC Gamma Telescope Data.csv'
nRow, nCol = df1.shape
print(f'There are {nRow} rows and {nCol} columns')


# In[ ]:


df1.head(5)


# In[ ]:


sns.pairplot(df1);


# In[ ]:


ax = sns.scatterplot(x="Flength", y="Fwidth", hue="Class", data=df1)


# In[ ]:


columns=df1.columns[:8]
plt.subplots(figsize=(18,15))
length=len(columns)
for i,j in itertools.zip_longest(columns,range(length)):
    plt.subplot((length/2),3,j+1)
    plt.subplots_adjust(wspace=0.2,hspace=0.5)
    df1[i].hist(bins=20,edgecolor='black')
    plt.title(i)
plt.show()


# In[ ]:


sns.heatmap(df1[df1.columns[:]].corr(),annot=True,cmap='RdYlGn')
fig=plt.gcf()
fig.set_size_inches(10,8)
plt.show()


# In[ ]:


sns.pairplot(data=df1,hue='Class',diag_kind='kde')
plt.show()

