#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import gc
import json
import math
import cv2
import PIL
from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import scipy
from tqdm import tqdm
import pandas as pd

get_ipython().run_line_magic('matplotlib', 'inline')


# ## Reading data

# In[ ]:


df_train = pd.read_csv("../input/siim-isic-melanoma-classification/train.csv")
df_test = pd.read_csv("../input/siim-isic-melanoma-classification/test.csv")
m_train = df_train.shape[0]
print('number of training images ',m_train)
df_train.head()


# In[ ]:


m_test = df_test.shape[0]
print('number of testing images ',m_test)
df_test.head()


# In[ ]:


df_train.describe(include ='O')


# ## Classes
# 

# In[ ]:


malignant_df = df_train[df_train['target']==1]
print('number of malignant images ', len(malignant_df))
benign_df = df_train[df_train['target']==0]
print('number of benign images ', len(benign_df))


# In[ ]:


# classes
sns.set_style('whitegrid')
sns.countplot(x='benign_malignant',data=df_train)
plt.show()


# ## Images Visualization

# ### Samples of malignant images
# 

# In[ ]:


fig,axes = plt.subplots(4,4,figsize=[10,10])
for i,iax in enumerate( axes.flatten()):
    ind = np.random.randint(0,500)
    fname = malignant_df.image_name.tolist()[ind]
    img = Image.open('../input/siim-isic-melanoma-classification/jpeg/train/'+fname+'.jpg')
    iax.imshow(img)
    iax.set_xticks([])
    iax.set_yticks([])
fig.show()


# ### Samples of benign images
# 

# In[ ]:


fig,axes = plt.subplots(4,4,figsize=[10,10])
for i,iax in enumerate( axes.flatten()):
    ind = np.random.randint(0,10000)
    fname = benign_df.image_name.tolist()[ind]
    img = Image.open('../input/siim-isic-melanoma-classification/jpeg/train/'+fname+'.jpg')
    iax.imshow(img)
    iax.set_xticks([])
    iax.set_yticks([])
fig.show()


# ## Histogram of benign  images with sex

# In[ ]:


sns.countplot(x='sex',data=benign_df)
plt.show()


# ## Histogram of malignant  images with sex

# In[ ]:


sns.countplot(x='sex',data=malignant_df)
plt.show()


# ## Histogram of benign  images with Age

# In[ ]:


benign_df['age_approx'].hist(bins = 16)


# ## Histogram of malignant  images with Age
# 

# In[ ]:


malignant_df['age_approx'].hist(bins = 16)


# In[ ]:


plt.figure(figsize=(12, 7))
sns.boxplot(x='target',y='age_approx',data=df_train,palette='winter')


# ## Histogram of benign images with diagnosis

# In[ ]:


sns.countplot(y='diagnosis',data=benign_df,orient = 'h')
plt.show()


# In[ ]:


benign_df.groupby('diagnosis')['image_name'].nunique()


# ## The diagnosis of malignant images is melanoma 

# In[ ]:


malignant_df.groupby('diagnosis')['image_name'].nunique()


# ## Histogram of benign images with images' location

# In[ ]:


sns.countplot(y='anatom_site_general_challenge',data=benign_df,orient = 'h')
plt.show()


# ## Histogram of malignant images with images' location

# In[ ]:


sns.countplot(y='anatom_site_general_challenge',data=malignant_df,orient = 'h')
plt.show()


# ## Missing values

# In[ ]:


# training
print(df_train.isnull().sum())
print(len(df_train))


# In[ ]:


# testing
print(df_test.isnull().sum())
print(m_test)


# In[ ]:




