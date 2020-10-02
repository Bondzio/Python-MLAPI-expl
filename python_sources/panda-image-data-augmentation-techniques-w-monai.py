#!/usr/bin/env python
# coding: utf-8

# <div class="jumbotron">
#   <h1 class="display-4">PANDA: Image Data Augmentation Techniques w/ MONAI</h1>
#   <p class="lead">Hello there!
# 
# This is a notebook of mine whose aim is to find out suitable preprocessing methods for this competition on prostate cancer detection. Prostate cancer is a deadly form of cancer which affects the *prostate gland* in men. Here I try to describe the best possible methods for preprocessing the images in the competition and I'll try to cover as many images as well as preprocessing/data augmentation techniques that are possible in this notebook.</p>
#   <hr class="my-4">
#   <p>I shall try to cover a lot of methods of preprocessing/data augmentation and i'll also try to use a variety of libraries including MONAI which is a very useful library for medical image processing and segmentation. </p>

# <div class="alert alert-block alert-warning">
# Credit goes to Marco Vasquez for his HTML notebook.
# </div>

# <div class="list-group" id="list-tab" role="tablist">
#   <h3 class="list-group-item list-group-item-action active" data-toggle="list"  role="tab" aria-controls="home">Table of Contents</h3>
#   <a class="list-group-item list-group-item-action" data-toggle="list" href="#affine" role="tab" aria-controls="profile">1. The Affine Transform<span class="badge badge-primary badge-pill">1</span></a>
#   <a class="list-group-item list-group-item-action" data-toggle="list" href="#eldef" role="tab" aria-controls="messages">2. Elastic Deformation <span class="badge badge-primary badge-pill">2</span></a>
#   <a class="list-group-item list-group-item-action"  data-toggle="list" href="#flip" role="tab" aria-controls="settings">3. Flipped images<span class="badge badge-primary badge-pill">3</span></a>
#   <a class="list-group-item list-group-item-action" data-toggle="list" href="#spapad" role="tab" aria-controls="settings">4. Spatial Padding<span class="badge badge-primary badge-pill">4</span></a> 
#   <a class="list-group-item list-group-item-action" data-toggle="list" href="#aptos" role="tab" aria-controls="settings">5. Experimental Method from APTOS<span class="badge badge-primary badge-pill">5</span></a> 
#   <a class="list-group-item list-group-item-action" data-toggle="list" href="#app1" role="tab" aria-controls="settings">Appendix A: Libraries and Resources.<span class="badge badge-primary badge-pill">A</span></a> 

# In[ ]:


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openslide
import os
get_ipython().system('pip install monai')
import torch


# In[ ]:


train = pd.read_csv('../input/prostate-cancer-grade-assessment/train.csv')
gpu = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
gpu


# ## Our Image Reading Function

# This is our simple function to show/read images (from Gabriel's kernel). It is going to be very useful for our image processing and we will use many variations of these functions later on for our different transforms.

# In[ ]:


def show_images(df, read_region=(1780,1950)):
    data = df
    f, ax = plt.subplots(3,3, figsize=(16,18))
    for i,data_row in enumerate(data.iterrows()):
        image = str(data_row[1][0])+'.tiff'
        image_path = os.path.join('../input/prostate-cancer-grade-assessment',"train_images",image)
        image = openslide.OpenSlide(image_path)
        spacing = 1 / (float(image.properties['tiff.XResolution']) / 10000)
        patch = image.read_region(read_region, 0, (256, 256))
        ax[i//3, i%3].imshow(patch) 
        image.close()       
        ax[i//3, i%3].axis('off')
        ax[i//3, i%3].set_title(f'ID: {data_row[1][0]}\nSource: {data_row[1][1]} ISUP: {data_row[1][2]} Gleason: {data_row[1][3]}')

    plt.show()
images = [
    '059cbf902c5e42972587c8d17d49efed', '06a0cbd8fd6320ef1aa6f19342af2e68', '06eda4a6faca84e84a781fee2d5f47e1',
    '037504061b9fba71ef6e24c48c6df44d', '035b1edd3d1aeeffc77ce5d248a01a53', '046b35ae95374bfb48cdca8d7c83233f',
    '074c3e01525681a275a42282cd21cbde', '05abe25c883d508ecc15b6e857e59f32', '05f4e9415af9fdabc19109c980daf5ad']   
data_sample = train.loc[train.image_id.isin(images)]
show_images(data_sample)


# <h1 id="affine">1. <b>The Affine Transform</b></h1>
# 
# The affine transform is any function than can preserve collinearity. There are multiple examples of affine transforms which you would have heard in high school mathematics:
# + Shear
# + Translate
# + Reflect
# + Rotate
# + Geometric contraction 
# 
# et. al.
# 
# We can apply a simple affine transform to our images over here (not necessarily one of the geometric transforms given above).

# In[ ]:


from monai.transforms import *

def show_images_affine(df, read_region=(1780,1950)):
    data = df
    f, ax = plt.subplots(3,3, figsize=(16,18))
    for i,data_row in enumerate(data.iterrows()):
        image = str(data_row[1][0])+'.tiff'
        image_path = os.path.join('../input/prostate-cancer-grade-assessment',"train_images",image)
        image = openslide.OpenSlide(image_path)
        spacing = 1 / (float(image.properties['tiff.XResolution']) / 10000)
        patch = image.read_region(read_region, 0, (256, 256))
        patch = np.array(patch)
        # MONAI transforms always take channel-first data: [channel x H x W]
        im_data = np.moveaxis(patch, -1, 0)  # make them channel first
        # create an Affine transform
        affine = Affine(rotate_params=np.pi/4, scale_params=(1.2, 1.2), translate_params=(200, 40), 
                padding_mode='zeros', device=torch.device('cuda:0'))
        # convert both image and segmentation using different interpolation mode
        new_img = affine(im_data, (256, 256), mode='bilinear')
        
        ax[i//3, i%3].imshow(np.moveaxis(new_img.astype(int), 0, -1)) 
        image.close()       
        ax[i//3, i%3].axis('off')
        ax[i//3, i%3].set_title(f'Affine Transformed\n Gleason: {data_row[1][3]}')
    plt.show()
    
images = [
    '059cbf902c5e42972587c8d17d49efed', '06a0cbd8fd6320ef1aa6f19342af2e68', '06eda4a6faca84e84a781fee2d5f47e1',
    '037504061b9fba71ef6e24c48c6df44d', '035b1edd3d1aeeffc77ce5d248a01a53', '046b35ae95374bfb48cdca8d7c83233f',
    '074c3e01525681a275a42282cd21cbde', '05abe25c883d508ecc15b6e857e59f32', '05f4e9415af9fdabc19109c980daf5ad']   
data_sample = train.loc[train.image_id.isin(images)]
show_images_affine(data_sample)


# **YOU ARE HERE:**
# <div class="progress">
#   <div class="progress-bar" role="progressbar" style="width: 25%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">20%</div>
# </div>

# <h1 id="eldef"> <b>2. Elastic Deformation</b></h1>
# 
# Elastic deformation basically applies an invisible "stress" to our image in such a manner that the image gets deformed due to the virtual stress applied. We can simulate this sort of "stress" with MONAI's `Rand2DElastic` transform. This transform actually is a concept in real life: apply stress to an object in such a way that the original position is recoverable even after having applied stress (elasticity basically).
# 
# This is an example of strain in real life:
# ![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/DeformationOfRod_plain.svg/400px-DeformationOfRod_plain.svg.png)
# 
# We can similarly apply such virtual stress to our image to deform it.
# 
# We can use 2-dimensional elastic deformation where the strain is the measure of deformation. The strain can be simply represented by:
# ![](https://wikimedia.org/api/rest_v1/media/math/render/svg/77b3bbb9d1485775abe0dc7069df39c807ba6988)
# 
# For more on the mathematical side, you can see the Wikipedia page [here](https://en.wikipedia.org/wiki/Deformation_(mechanics)).

# In[ ]:


def show_images_elastic2d(df, read_region=(1780,1950)):
    data = df
    f, ax = plt.subplots(3,3, figsize=(16,18))
    for i,data_row in enumerate(data.iterrows()):
        image = str(data_row[1][0])+'.tiff'
        image_path = os.path.join('../input/prostate-cancer-grade-assessment',"train_images",image)
        image = openslide.OpenSlide(image_path)
        spacing = 1 / (float(image.properties['tiff.XResolution']) / 10000)
        patch = image.read_region(read_region, 0, (256, 256))
        patch = np.array(patch)
        im_data = np.moveaxis(patch, -1, 0)  # make them channel first
        # create an elastic transform
        deform = Rand2DElastic(prob=1.0, spacing=(30, 30), magnitude_range=(5, 6),
                       rotate_range=(np.pi/4,), scale_range=(0.2, 0.2), translate_range=(100, 100), 
                       padding_mode='zeros', device=torch.device('cuda:0'))
        new_img = deform(im_data, (256, 256), mode='nearest')
        
        ax[i//3, i%3].imshow(np.moveaxis(new_img.astype(int), 0, -1)) 
        image.close()       
        ax[i//3, i%3].axis('off')
        ax[i//3, i%3].set_title(f'Deformed Transformed\n Gleason: {data_row[1][3]}')
    plt.show()
    
images = [
    '059cbf902c5e42972587c8d17d49efed', '06a0cbd8fd6320ef1aa6f19342af2e68', '06eda4a6faca84e84a781fee2d5f47e1',
    '037504061b9fba71ef6e24c48c6df44d', '035b1edd3d1aeeffc77ce5d248a01a53', '046b35ae95374bfb48cdca8d7c83233f',
    '074c3e01525681a275a42282cd21cbde', '05abe25c883d508ecc15b6e857e59f32', '05f4e9415af9fdabc19109c980daf5ad']   
data_sample = train.loc[train.image_id.isin(images)]
show_images_elastic2d(data_sample)


# **YOU ARE HERE:**
# <div class="progress">
#   <div class="progress-bar" role="progressbar" style="width: 40%;" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100">40%</div>
# </div>

# <h1 id="flip"> 3. <b>Flipped images</b> </h1>

# Flipping as a transform is rather self explanatory. We can either flip our set of images across the x-axis or we can flip our set of images across the y-axis.
# 
# ![An x-axis flip](data:image/jpeg;base64,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)
# 
# The above image flips across the x-axis.

# In[ ]:


def show_images_rotate(df, read_region=(1780,1950)):
    data = df
    f, ax = plt.subplots(3,3, figsize=(16,18))
    for i,data_row in enumerate(data.iterrows()):
        image = str(data_row[1][0])+'.tiff'
        image_path = os.path.join('../input/prostate-cancer-grade-assessment',"train_images",image)
        image = openslide.OpenSlide(image_path)
        spacing = 1 / (float(image.properties['tiff.XResolution']) / 10000)
        patch = image.read_region(read_region, 0, (256, 256))
        patch = np.array(patch)
        im_data = np.moveaxis(patch, -1, 0)  # make them channel first
        rotater = Flip(spatial_axis=1)
        new_img = rotater(im_data)
        
        ax[i//3, i%3].imshow(np.moveaxis(new_img.astype(int), 0, -1)) 
        image.close()       
        ax[i//3, i%3].axis('off')
        ax[i//3, i%3].set_title(f'Rotated Transformed\n Gleason: {data_row[1][3]}')
    plt.show()
    
images = [
    '059cbf902c5e42972587c8d17d49efed', '06a0cbd8fd6320ef1aa6f19342af2e68', '06eda4a6faca84e84a781fee2d5f47e1',
    '037504061b9fba71ef6e24c48c6df44d', '035b1edd3d1aeeffc77ce5d248a01a53', '046b35ae95374bfb48cdca8d7c83233f',
    '074c3e01525681a275a42282cd21cbde', '05abe25c883d508ecc15b6e857e59f32', '05f4e9415af9fdabc19109c980daf5ad']   
data_sample = train.loc[train.image_id.isin(images)]
show_images_rotate(data_sample)


# **YOU ARE HERE:**
# <div class="progress">
#   <div class="progress-bar" role="progressbar" style="width: 60%;" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100">60%</div>
# </div>

# <h1 id="spapad"> <b>4. Spatial Padding</b></h1>
# 
# Spatial padding is used in Convolutional layers. Why? Well, convolutional layers often tend to lose pixels on the side of the image sometimes. With a small amount of Convolutional layers, it's fine but with many convolutional layers the pixel loss tends to add up over and over again and it can eventually spiral out of control.
# 
# One simple solution to this is to add some extra pixels around the borders so that even if we lose information in pixels it will not affect our model much. To keep it relatively useless besides being a dummy (in a metaphorical sense) we keep most of the values 0. The following image gives a good demo of padding:
# ![](https://d2l.ai/_images/conv-pad.svg)
# 
# In the above image we have a padded input, which is then processed into a kernel and then comes out as a 4 x 4.
# 
# Convolutional layers often pad with odd numbers such as 1, 3, 5 or 7. Thus, we can preserve the spatial dimensionality by padding with odd numbers. But don't think padding is only used in Convolutional layers, we can also use padding as a transform with MONAI.

# In[ ]:


def show_images_rotate(df, read_region=(1780,1950)):
    data = df
    f, ax = plt.subplots(3,3, figsize=(16,18))
    for i,data_row in enumerate(data.iterrows()):
        image = str(data_row[1][0])+'.tiff'
        image_path = os.path.join('../input/prostate-cancer-grade-assessment',"train_images",image)
        image = openslide.OpenSlide(image_path)
        spacing = 1 / (float(image.properties['tiff.XResolution']) / 10000)
        patch = image.read_region(read_region, 0, (256, 256))
        patch = np.array(patch)
        im_data = np.moveaxis(patch, -1, 0)  # make them channel first
        rotater = SpatialPad(spatial_size=(300, 300), mode='mean')
        new_img = rotater(im_data)
        
        ax[i//3, i%3].imshow(np.moveaxis(new_img.astype(int), 0, -1)) 
        image.close()       
        ax[i//3, i%3].axis('off')
        ax[i//3, i%3].set_title(f'Rotated Transformed\n Gleason: {data_row[1][3]}')
    plt.show()
    
images = [
    '059cbf902c5e42972587c8d17d49efed', '06a0cbd8fd6320ef1aa6f19342af2e68', '06eda4a6faca84e84a781fee2d5f47e1',
    '037504061b9fba71ef6e24c48c6df44d', '035b1edd3d1aeeffc77ce5d248a01a53', '046b35ae95374bfb48cdca8d7c83233f',
    '074c3e01525681a275a42282cd21cbde', '05abe25c883d508ecc15b6e857e59f32', '05f4e9415af9fdabc19109c980daf5ad']   
data_sample = train.loc[train.image_id.isin(images)]
show_images_rotate(data_sample)


# We can see dummy pixels being placed at the end (borders) of our images. Padding in action, baby!

# **YOU ARE HERE:**
# <div class="progress">
#   <div class="progress-bar" role="progressbar" style="width: 80%;" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100">80%</div>
# </div>

# <h1 id="aptos">5. Experimental Method from APTOS</h1>
# <hr>
# 
# I have read Neuron Engineer's notebook on APTOS and I have also read about a very useful preprocessing method used in that competition to great effect. I am not exactly sure of how well it will work but I am willing to try it out.

# In[ ]:


import cv2
 
image = cv2.imread('../input/panda-resize-and-save-train-data/0005f7aaab2800f6170c399693a96917.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
image = cv2.resize(image, (256, 256))
image=cv2.addWeighted ( image,4, cv2.GaussianBlur( image , (0,0) , 256/10) ,-4 ,128) # the trick is to add this line
plt.imshow(image)
plt.title('Ben Graham Method\n Transformed image')
plt.show()


# **YOU ARE HERE:**
# <div class="progress">
#   <div class="progress-bar" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">100%</div>
# </div>

# <h1 id="app1"> APPENDIX A: A list of useful resources and credits</h1>
# 
# ## Credits to the libraries used:
# 
# + **Pandas: https://pandas.pydata.org/ **
# + **Numpy: https://numpy.org/**
# + **Openslide: https://openslide.org/api/python/**
# * **Matplotlib: https://matplotlib.org/**
# + **Monai: https://monai.readthedocs.io/en/latest/index.html**
# 
# ## Useful resources
# 
# + **https://www.urologyhealth.org/urologic-conditions/prostate-cancer**
# + **https://www.healthline.com/health/prostate-cancer**
