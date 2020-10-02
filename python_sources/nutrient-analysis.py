#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
print(os.listdir("../input"))


# In[ ]:


# What are the Nutrient demands with respect to Plant Types?


# In[ ]:


data = '../input/crops.csv'
df = pd.read_csv(data)
df.head()


# In[ ]:


df.CropCategory.unique()


# In[ ]:


df1 = df.groupby('CropCategory')
df_TreeFruit = df1.get_group('Tree and fruit')
df_TreeFruit['NuContAvailable'].value_counts().plot(kind='bar')


# In[ ]:


df_Forage = df1.get_group('Forage')
df_Forage['NuContAvailable'].value_counts().plot(kind='bar')


# In[ ]:


df_Veggie = df1.get_group('Vegetable')
df_Veggie['NuContAvailable'].value_counts().plot(kind='bar')


# In[ ]:


df_CerealOil = df1.get_group('Cereal and oil')
df_CerealOil['NuContAvailable'].value_counts().plot(kind='bar')


# In[ ]:


df_FiberMisc = df1.get_group('Fiber and miscellaneous')
df_FiberMisc['NuContAvailable'].value_counts().plot(kind='bar')


# In[ ]:




