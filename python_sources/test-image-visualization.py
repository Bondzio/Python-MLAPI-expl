#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd 
import cv2
import seaborn as sns

from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

## load two csv files
df = pd.read_csv('../input/tuning_labels.csv', header=None, 
                 names=['img_id', 'labels'])
description = pd.read_csv('../input/class-descriptions.csv')

## make a dictionary file
d={}
for i,j in zip(description.label_code.values, description.description.values):
    d[i]=j


# In[ ]:


count = pd.DataFrame(df['labels'].str.split().apply(lambda x:len(x)))
sns.countplot(data=count,x='labels')
plt.title('number of labels')


# > ## Images with more than 6 labels

# In[ ]:


temp = df[count['labels']>6]
list = ['../input/stage_1_test_images/{}.jpg'.format(img_id) for img_id in temp.img_id.values]
ax=plt.figure(figsize=(12,12))
for num,i in enumerate(temp['labels'].apply(lambda x: x.split()).values):
    plt.subplot(3,2,2*num+1)
    plt.axis('off')
    filename = list[num]
    img = cv2.imread(filename)
    plt.imshow(img)
    names = [d[j] for j in i]
    for n,i in enumerate(names):
        plt.text(1500,10+n*100,i,fontsize=14,horizontalalignment='right')


# In[ ]:


## create a function called "plot_images"
def plot_images(num_label,max=60):
    temp = df[count['labels']==num_label]
    print(len(temp))
    if len(temp) > 60:
        temp = temp[:60]
    list = ['../input/stage_1_test_images/{}.jpg'.format(img_id) for img_id in temp.img_id.values]
    ax=plt.figure(figsize=(12,60))
    for num,i in enumerate(temp['labels'].apply(lambda x: x.split()).values):
        filename = list[num]
        img = cv2.imread(filename)
        img = cv2.resize(img, dsize=(1024, 600), interpolation=cv2.INTER_CUBIC)
        plt.subplot(30,4,2*num+1)
        plt.axis('off')
        plt.imshow(img)
        names = [d[j] for j in i]
        for n,i in enumerate(names):
            plt.text(1500,10+n*100,i,fontsize=10,horizontalalignment='left')


# ## Images with 6 labels

# In[ ]:


plot_images(6)


# ## Images with 5 labels

# In[ ]:


plot_images(5)


# ## Images with 4 labels

# In[ ]:


plot_images(4)


# ## Images with 3 labels

# In[ ]:


plot_images(3)


# ## Images with 2 labels

# In[ ]:


plot_images(2)


# ## Images with only one label!

# In[ ]:


plot_images(1)

