#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os


# # Welcome 
# 
# ![](https://miro.medium.com/max/1210/0*Utma-dS47hSoQ6Zt)
# 
# ** This kernel is based on Image Augmentation and the following is applied :**
# * Horizontal Flip
# * Width Shift
# * Random 45 degree rotation
# * Filling
# * Random Zoom (10%)

# In[ ]:


from tensorflow.keras.preprocessing.image import ImageDataGenerator

Image_path='/kaggle/input/siim-isic-melanoma-classification/jpeg/'
# dtype string because its reads in string format
train_csv=pd.read_csv('/kaggle/input/siim-isic-melanoma-classification/train.csv',dtype=str)
test_csv=pd.read_csv('/kaggle/input/siim-isic-melanoma-classification/test.csv',dtype=str)


# # It's Augment time.
# 
# **We can use various augmentation and even add preprocessing filters**

# In[ ]:


train_augmenter=ImageDataGenerator(
    rescale=1./255, 
    #rotation range and fill mode only
    #samplewise_center=True, 
    #samplewise_std_normalization=True, 
    horizontal_flip = True, 
    #vertical_flip = True, 
    #height_shift_range= 0.05, 
    width_shift_range=0.1, 
    rotation_range=45, 
    #shear_range = 0.1,
    fill_mode = 'nearest',
    zoom_range=0.10,
    #preprocessing_function=function_name,
    )

test_augmenter=ImageDataGenerator(
    rescale=1./255
    )


# We need to add the format of the images in the end or Use glob for flexibility

# In[ ]:


def jpg_tag(image_name):
    return image_name+'.jpg'

train_csv['image_name']=train_csv['image_name'].apply(jpg_tag)
test_csv['image_name']=test_csv['image_name'].apply(jpg_tag)


# In[ ]:


#displaying of new dataframe
test_csv


# In[ ]:


batch_size=16
IMG_size=224
train_generator=train_augmenter.flow_from_dataframe(
dataframe=train_csv,
directory=Image_path+'train',
#save_to_dir='augmented',
#save_prefix='_aug'
#save_format='jpg'
x_col='image_name',
y_col='target',
batch_size=batch_size,
seed=42,
shuffle=True,
class_mode='binary',
target_size=(IMG_size,IMG_size)
)

test_generator=test_augmenter.flow_from_dataframe(
dataframe=test_csv,
directory=Image_path+'test',
x_col='image_name',
batch_size=batch_size, #preffered 1
shuffle=False,
class_mode=None,
target_size=(IMG_size,IMG_size)
)


# **Success reading all the Images **

# # OUTPUT OF AUGMENTATED IMAGES

# In[ ]:


import matplotlib.pyplot as plt
def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
    plt.tight_layout()
    plt.show()
    
    
augmented_images = [train_generator[0][0][0] for i in range(5)]
plotImages(augmented_images)


# # VOILA DONE , use this in fit function now

# Image source: Medium
