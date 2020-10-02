#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
sns.set(style="whitegrid")
from collections import Counter
get_ipython().run_line_magic('matplotlib', 'inline')

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
import warnings
warnings.filterwarnings('ignore')

dat = pd.read_csv('../input/beaver-body-temperature/beaver.csv')


# In[ ]:


dat.head


# In[ ]:


dat.info()


# In[ ]:


dat['activ'].value_counts()


# In[ ]:


f, ax = plt.subplots(figsize=(8,6))
x = dat['temp']
ax = sns.distplot(x, bins=10)
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8,6))
x = dat['temp']
x = pd.Series(x, name="Temp variable")
ax = sns.distplot(x, bins=10)
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8,6))
x = dat['temp']
ax = sns.distplot(x, bins=10, vertical = True)
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8,6))
x = dat['temp']
x = pd.Series(x, name="Temp variable")
ax = sns.kdeplot(x)
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8,6))
x = dat['temp']
x = pd.Series(x, name="Age variable")
ax = sns.kdeplot(x, shade=True, color='r')
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8,6))
x = dat['temp']
ax = sns.distplot(x, kde=False, rug=True, bins=10)
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8,6))
x = dat['temp']
ax = sns.distplot(x, hist=False, rug=True, bins=10)
plt.show()


# In[ ]:


dat['temp'].nunique()


# In[ ]:


dat['temp'].value_counts()


# In[ ]:


f, ax = plt.subplots(figsize=(8, 6))
sns.countplot(x="temp", data=dat, color="c")
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8, 6))
sns.countplot(x="temp", hue="activ", data=dat)
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8, 6))
sns.countplot(y="temp", data=dat, color="c")
plt.show()


# In[ ]:


g = sns.catplot(x="activ", kind="count", palette="ch:.25", data=dat)


# In[ ]:


f, ax = plt.subplots(figsize=(8, 6))
sns.stripplot(x="temp", y="activ", data=dat)
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8, 6))
sns.stripplot(x="temp", y="activ", hue="activ", 
                   data=dat, palette="Set2", size=20, marker="D",
                   edgecolor="gray", alpha=.25)
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(x=dat["temp"])
plt.show()


# In[ ]:


f, ax = plt.subplots(figsize=(8, 6))
ax = sns.lineplot(x="temp", y="activ", data=dat)
plt.show()


# In[ ]:


datt =dat[['temp', 'activ']]
g = sns.PairGrid(datt)
g = g.map(plt.scatter)


# In[ ]:


g = sns.PairGrid(datt)
g = g.map_diag(plt.hist)
g = g.map_offdiag(plt.scatter)


# In[ ]:


g = sns.PairGrid(datt, hue="activ")
g = g.map_diag(plt.hist)
g = g.map_offdiag(plt.scatter)
g = g.add_legend()


# In[ ]:


g = sns.PairGrid(datt, hue="activ")
g = g.map_diag(plt.hist, histtype="step", linewidth=3)
g = g.map_offdiag(plt.scatter)
g = g.add_legend()


# In[ ]:


g = sns.PairGrid(datt, vars=['temp', 'activ'])
g = g.map(plt.scatter)


# In[ ]:


g = sns.PairGrid(datt)
g = g.map_upper(plt.scatter)
g = g.map_lower(sns.kdeplot, cmap="Blues_d")
g = g.map_diag(sns.kdeplot, lw=3, legend=False)


# In[ ]:


g = sns.JointGrid(x="temp", y="activ", data=dat)
g = g.plot(sns.regplot, sns.distplot)

