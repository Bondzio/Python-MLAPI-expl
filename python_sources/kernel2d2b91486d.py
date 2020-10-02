#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sns
import os


# In[ ]:


g = pd.read_csv(r"../input/isotc213/ISO_TC 213.csv")


# In[ ]:


g


# In[ ]:


g['Status'].value_counts().plot(kind='barh')
plt.ylabel("Number of standards")


# In[ ]:


stat = g['Status'].value_counts()
stat


# In[ ]:


op = g.price_CF.sum()
print( "Overall cost of published standard %s CF %s Euro" %(op,op*0.91))


# In[ ]:


g.Number_of_pages.sum()


# In[ ]:


g['year'] = (np.where(g['Publication_date'].str.contains('-'),
                  g['Publication_date'].str.split('-').str[0],
                  g['Publication_date']))


# In[ ]:


gs = g.sort_values(by=['year'])
years = gs['year'].value_counts(sort=False)


# In[ ]:


years[sorted(years.index)].plot(kind='bar')


# In[ ]:


h = pd.read_csv("../input/isotc213/ISO_TC 213_CH.csv")
h.describe()


# In[ ]:


op = h.price_CF.sum()
print( "Overall cost of published standard %s CF %s Euro" %(op,op*0.91))


# In[ ]:


h['Status'].value_counts().plot(kind='barh')
plt.ylabel("Number of standards")


# In[ ]:


h


# In[ ]:


stat = h['Status'].value_counts()
stat


# In[ ]:




