#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import os
print(os.listdir("../input"))


# In[2]:


train = pd.read_csv('../input/imgs_train.csv')
print(train.shape)
train.head()


# In[3]:


# Sample code for loading an image

from PIL import Image
from pathlib import Path
im_p = Path('../input/all_images/image_moderation_images')
Image.open(im_p/train.images_id.iloc[0])

