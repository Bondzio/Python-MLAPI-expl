#!/usr/bin/env python
# coding: utf-8

# # Diamonds Dataset - Toy Kaggle: find carat peaks

# ### Imports

# In[ ]:


#Number manipulation
import numpy as np

#Data Manipulation
import pandas as pd

#Plotting Libraries
from matplotlib import pyplot as plt
import seaborn as sns


# In[ ]:


#Some configuration settings
get_ipython().run_line_magic('matplotlib', 'inline')
pd.set_option("display.max_columns", 100)


# ### Getting the data

# In[ ]:


df = pd.read_csv("../input/diamonds.csv", index_col=0)


# In[ ]:


sns.distplot(df['carat'])


# In[ ]:


import scipy.stats as stats
from PyAstronomy import pyaC

x = np.linspace(0, 3, 1000)

# compute density function
nparam_density = stats.kde.gaussian_kde(df.carat.ravel())
nparam_density = nparam_density(x)

# compute gradient (derivative 1)
grad = np.gradient(nparam_density)

# Get coordinates and indices of zero crossings
xcross, grad_cross_idx = pyaC.zerocross1d(x, grad, getIndices=True)

fig, ax = plt.subplots(figsize=(10, 6))

# plot density histogram
ax.hist(df.carat, bins=50, normed=True, alpha=0.5)

# plot density functions
ax.plot(x, nparam_density, 'r-', label='density')
ax.plot(x, grad, 'b-', label='density derivative')

# Add vertical line where the zero line is crossed
peaks = []
for idx, pos in enumerate(grad_cross_idx):
    # only show peaks, ignore valleys
    if grad[pos] > 0:
        peaks.append(xcross[idx])
        ax.axvline(x=xcross[idx], color='g', alpha=0.5, label='peak')


# In[ ]:


print(np.round(peaks, 1))


# ### Now we want to detect the "hidden data"

# In[ ]:


sns.distplot(df['price'])


# In[ ]:


sns.scatterplot(x="carat", y="price", hue="clarity", data=df.sample(10000))


# In[ ]:


sns.distplot(df[df.price > 10000].price)


# In[ ]:


import scipy.stats as stats
from PyAstronomy import pyaC

values = df[df.price > 10000].price.ravel() 

x = np.linspace(np.min(values) - 1000, np.max(values) + 1000, 2000)

# compute density function
nparam_density = stats.kde.gaussian_kde(values)
nparam_density = nparam_density(x)

# compute gradient (derivative 1)
grad = np.gradient(nparam_density)

# Get coordinates and indices of zero crossings
xcross, grad_cross_idx = pyaC.zerocross1d(x, grad, getIndices=True)

fig, ax = plt.subplots(figsize=(10, 6))

# plot density histogram
ax.hist(values, bins=50, normed=True, alpha=0.5)

# plot density functions
ax.plot(x, nparam_density, 'r-', label='density')
ax2 = ax.twinx()
ax2.plot(x, grad, 'b-', label='density derivative')


# In[ ]:




