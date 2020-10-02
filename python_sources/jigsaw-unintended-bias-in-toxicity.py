#!/usr/bin/env python
# coding: utf-8

# In[33]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("dark")
import warnings
warnings.filterwarnings("ignore")

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[34]:


df = pd.read_csv("../input/train.csv")


# In[35]:


df.shape


# In[36]:


df.sample(100).head(10)


# In[37]:


df.isna().sum() / df.shape[0] * 100


# In[38]:



df.severe_toxicity.mean(), df.severe_toxicity.max(), df.severe_toxicity.min()


# In[39]:


plt.figure(figsize=(15, 10))

plt.subplot(221)
sns.kdeplot(df.severe_toxicity.values, shade=True)
plt.title("Severe Toxicity")

plt.subplot(222)
sns.kdeplot(df.identity_attack.values, shade=True)
plt.title("Identity Attack")

plt.subplot(223)
sns.kdeplot(df.obscene.values, shade=True)
plt.title("Obscene")

plt.subplot(224)
sns.kdeplot(df.insult.values, shade=True)
plt.title("Insult")

plt.plot()


# In[48]:


df.asian.min(), df.asian.max(), df.asian.mean()


# In[47]:


df.iloc[:, 8:32].sum(axis=0)


# In[ ]:




