#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import seaborn as sns
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:


for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


nRowsRead = 1000 # specify 'None' if want to read whole file
# free1.csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df1 = pd.read_csv('../input/biopsy-data-on-breast-cancer-patients/biopsy.csv', delimiter=',', nrows = nRowsRead)
df1.dataframeName = 'biopsy.csv'
nRow, nCol = df1.shape
print(f'There are {nRow} rows and {nCol} columns')


# In[ ]:


df1.head(5)


# In[ ]:


sns.pairplot(df1);


# In[ ]:


ax = sns.scatterplot(x="V1", y="V2", hue="class", data=df1)

