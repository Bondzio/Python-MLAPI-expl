#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import warnings
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
warnings.filterwarnings("ignore")

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno


# In[ ]:


train = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/train.csv')
print(train.shape)


# In[ ]:


train.head()


# ### df.describe shows that 38 Columns are Numeric, hence the others are categorical according to algo, we need to check again though

# In[ ]:


train.describe()


# In[ ]:


plt.style.use('fivethirtyeight')
sns.distplot(train.SalePrice)


# ### let's Transform this Sales price - We can use BoxCox Transformation to convert to normal distribtion

# In[ ]:


from fitter import Fitter
f = Fitter(train.SalePrice)
f.fit()
# may take some time since by default, all distributions are tried
# but you call manually provide a smaller set of distributions
# Fitting a lot of Distribution Function to find the best one.


# In[ ]:


f.summary()


# *JohnsonSu is the best fitting distribution to the Target Variable. Will be Helpful later*

# In[ ]:


# This Graph is to compare your graph against a Normal Distribution
from scipy import stats
fig = plt.figure()
ax1 = fig.add_subplot(211)
prob = stats.probplot(train.SalePrice, dist=stats.norm, plot=ax1)
ax1.set_xlabel('')
ax1.set_title('Probplot against normal distribution')


# In[ ]:


fig = plt.figure()
ax2 = fig.add_subplot(212)
Yt, gamma = stats.boxcox(train.SalePrice)
prob = stats.probplot(Yt, dist=stats.norm, plot=ax2)
ax1.set_xlabel('')
ax1.set_title('Probplot against normal distribution')


# In[ ]:


## This shows that SalePrice is now Close to normal and can be used better- WE'll be using this whenever necessary
sns.distplot(Yt)


# In[ ]:


get_ipython().system('pip install dabl')


# In[ ]:


import dabl
dabl.plot(train, target_col = 'SalePrice')


# In[ ]:


msno.heatmap(train)


# ### Things to Focus on EDA is Missing data adn outliers.
