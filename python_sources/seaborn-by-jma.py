#!/usr/bin/env python
# coding: utf-8

# Codes from Johar M.Ashfaque. Thanks Johar for sharing. (user:ukveteran)

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


nRowsRead = 1000 # specify 'None' if want to read whole file
df = pd.read_csv('../input/cusersmarildownloadsearningcsv/earning.csv', delimiter=';', nrows = nRowsRead)
df.dataframeName = 'earning.csv'
nRow, nCol = df.shape
print(f'There are {nRow} rows and {nCol} columns')


# In[ ]:


df.tail(5)


# In[ ]:


categorical_cols = [cname for cname in df.columns if
                    df[cname].nunique() < 10 and 
                    df[cname].dtype == "object"]


# Select numerical columns
numerical_cols = [cname for cname in df.columns if 
                df[cname].dtype in ['int64', 'float64']]


# In[ ]:


print(categorical_cols)


# In[ ]:


print(numerical_cols)


# In[ ]:


from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import os 


# In[ ]:


p = df.hist(figsize = (20,20))


# In[ ]:


sns.regplot(x=df['femaleprofessionals'], y=df['femalesmanagers']) 


# In[ ]:


sns.regplot(x=df['maleprofessionals'], y=df['malemanagers']) 


# In[ ]:


sns.lmplot(x="femaleprofessionals", y="femalesmanagers", hue="year", data=df)


# In[ ]:


f, ax = plt.subplots(figsize=(6, 6))
sns.kdeplot(df.femaleprofessionals, df.maleprofessionals, ax=ax)
sns.rugplot(df.femaleprofessionals, color="g", ax=ax)
sns.rugplot(df.maleprofessionals, vertical=True, ax=ax);


# In[ ]:


f, ax = plt.subplots(figsize=(6, 6))
cmap = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)
sns.kdeplot(df.femaleprofessionals, df.femalesmanagers, cmap=cmap, n_levels=60, shade=True);


# In[ ]:


g = sns.jointplot(x="femalesmanagers", y="femaleprofessionals", data=df, kind="kde", color="m")
g.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
g.ax_joint.collections[0].set_alpha(0)
g.set_axis_labels("$femalesmanagers$", "$femaleprofessionals$");


# Thanks Johar M. Ashfaque (JMA), at least I have smth different from my same boring scripts.
