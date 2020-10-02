#!/usr/bin/env python
# coding: utf-8

# # **About Notebook**
# 
# This notebook explores the data through the lens of Whole Slide Images - i.e. across sizes, total pixels and a couple of other provided data columns in the train csv file using plotly.
# 
# Let me know if you found these valuable.
# 

# In[ ]:


get_ipython().system('pip install itk --quiet')
get_ipython().system('pip install itkwidgets --quiet')


# In[ ]:


import os
import numpy as np 
import pandas as pd 

import openslide
import gc
import matplotlib.pyplot as plt
from collections import defaultdict

from PIL import Image
from tqdm import tqdm

import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from IPython.display import FileLinks

import itk
import itkwidgets
from ipywidgets import interact , interactive , IntSlider , ToggleButtons
from ipywidgets import interact
plotly.offline.init_notebook_mode (True)


# **Path to the Directory**

# In[ ]:


train_images_dir = '../input/prostate-cancer-grade-assessment/train_images/'
train_images     = os.listdir (train_images_dir)


# In[ ]:


train_csv = pd.read_csv ('../input/prostate-cancer-grade-assessment/train.csv')


# **Dataframe construction with Image Dimensions**

# In[ ]:


train_images  = []

for i , image in enumerate(tqdm(os.listdir (train_images_dir))):
    img             =  image 
    img_size_MB     = f"{os.stat(train_images_dir+image).st_size / 1024 **2 : 1.2f} " 
    wsi             = openslide.OpenSlide (train_images_dir + image)
    train_images.append((img ,  
                         img_size_MB ,
                         wsi.level_dimensions[0] , 
                         wsi.level_dimensions[1] , 
                         wsi.level_dimensions[2] , 
                         np.product(wsi.level_dimensions[0]) * 3, 
                         np.product(wsi.level_dimensions[1]) * 3, 
                         np.product(wsi.level_dimensions[2]) * 3
                        ))
    gc.collect()
    


# **Converting the above results to a DataFrame**

# In[ ]:


train_images = pd.DataFrame ( train_images , 
                              columns = ['img' , 
                                  'Image Size (MB)' ,
                                  'Image Shape Level0' ,
                                  'Image Shape Level1' , 
                                  'Image Shape Level2' , 
                                  'Total Pixels Level0' , 
                                  'Total Pixels Level1' , 
                                  'Total Pixels Level2']
                            )


# **The below dataframe details the information across WSI's in the training dataset.**

# In[ ]:


train_images.head()


# In[ ]:


train_images['Image Size (MB)'] = train_images['Image Size (MB)'].astype('float32')


# **Remove .tiff from the 'img' column in Dataframe**

# In[ ]:


def image_name(img) :
    return img.split('.')[0]

train_images['img'] = train_images['img'].map(image_name)


# In[ ]:


train_images.shape  , train_csv.shape , train_images['img'].nunique()  , train_csv['image_id'].nunique()


# **Merging the Whole slide images information with the Train DataFrame.**

# In[ ]:


train_df = train_csv.merge (train_images , 
                            left_on = "image_id" , 
                            right_on = "img")


# In[ ]:


train_df.shape


# In[ ]:


#Drop duplicate column
train_df.drop('img', axis = 1, inplace= True)


# In[ ]:


train_df.head()


# Above dataframe will be used futher for data insights through visualization

# **Dropping the intermediate created datasets**

# In[ ]:


del train_images , train_csv


# # Image Size Distribution

# **Fetching the image width and height for plots**

# In[ ]:


def get_width (image) :
    return image[0]
def get_height (image) :
    return image[1]


# **Below are the scatter plots of Image pixels across height and width for all 3 levels**

# In[ ]:


width  = train_df['Image Shape Level0'].map(get_width)
height = train_df['Image Shape Level0'].map(get_height) 

fig    = px.scatter (train_df , 
            x =  width , 
            y = height , 
            color = width,
           title = 'Image Size in Pixels - Level 0 (highest) Resolution)')

fig.update_layout ( yaxis=dict(title_text="Height") , 
                    xaxis=dict(title_text="Width") , 
                    title_font_family="Open Sans"
                  )


# In[ ]:


width  = train_df['Image Shape Level1'].map(get_width)
height = train_df['Image Shape Level1'].map(get_height) 
fig    =  px.scatter (train_df , 
            x =  width , 
            y = height , 
            color = width , 
            title = 'Image Size in Pixels - Level 1 Resolution)')

fig.update_layout (yaxis=dict(title_text="Height") , 
                    xaxis=dict(title_text="Width") , 
                    title_font_family="Open Sans")


# In[ ]:


width  = train_df['Image Shape Level2'].map(get_width)
height = train_df['Image Shape Level2'].map(get_height) 
fig    = px.scatter (train_df , 
            x =  width , 
            y = height , 
            color = width , 
            title = 'Image Size in Pixels - Level 2 (lowest) Resolution)')
fig.update_layout (yaxis=dict(title_text="Height") , 
                    xaxis=dict(title_text="Width") , 
                    title_font_family="Open Sans")


# **What do the Image Size plots tell ?**
# 1. Image width & height for level 0 lies in range of tens of thousands , level1 until tens of 1000's and the last one i.e. level2 is concentrated in range of a few thousands majorily.
# 2. There are a few outliers in terms of sizes among above 3 levels.

# # **Toggle Level**

# **Below one is an interactive plot to switch among 3 levels quickly and get an overview of the distribution**

# In[ ]:


def change_level (level):
    width  = train_df[f'Image Shape Level{level}'].map(get_width)
    height = train_df[f'Image Shape Level{level}'].map(get_height) 
    fig = px.scatter (train_df , 
            x =  width , 
            y = height , 
            color = width , 
            title = f'Image Size in Pixels - Level {level} (Lowest Resolution)')
    
    fig.update_layout ( yaxis=dict(title_text="Height") , 
                    xaxis=dict(title_text="Width") , 
                    title_font_family="Open Sans")
    fig.show()
    return level


# In[ ]:


interact (change_level , level = (0 , 2))


# # **Pixel Distribution**
# 

# **Below plots visualise the pixel**

# In[ ]:


fig = px.histogram (train_df ,
              x = ['Total Pixels Level0'] ,
              hover_data = ['gleason_score' , 'isup_grade'],
              color = 'data_provider' ,
              marginal = 'rug',
              title = 'Pixel Distribution at Level 0')

fig.update_layout ( yaxis=dict(title_text="Images Count") , 
                    xaxis=dict(title_text="Total Number of Pixels") , 
                    title_font_family="Open Sans")
fig.show()


# In[ ]:


fig = px.histogram (train_df ,
              x = ['Total Pixels Level1'] ,
              hover_data = ['gleason_score' , 'isup_grade'],
              color = 'data_provider' ,
              marginal = 'rug',
              title = 'Pixel Distribution at Level 1')
fig.update_layout ( yaxis=dict(title_text="Images Count") , 
                    xaxis=dict(title_text="Pixel Size") , 
                    title_font_family="Open Sans")
fig.show()


# In[ ]:


fig = px.histogram (train_df ,
              x = ['Total Pixels Level2'] ,
              hover_data = ['gleason_score' , 'isup_grade'],
              color = 'data_provider' ,
              marginal = 'rug',
              title = 'Pixel Distribution at Level 2'
                   )

fig.update_layout ( yaxis=dict(title_text="Images Count") , 
                    xaxis=dict(title_text="Pixel Size") , 
                    title_font_family="Open Sans")
fig.show()


# **What do the Total Pixel's plots tell us ?**
# 1. Image data size do vary as provided by the 2 data providers.
# 2. In all the 3 levels , Karolinska provided datasets are comparatively larger than in size.

# **Above distinction among data providers can be more clearly seen in the below scatter plot**

# # **Toggle Level**

# In[ ]:


def change_level (level):
    width  = train_df[f'Image Shape Level{level}'].map(get_width)
    height = train_df[f'Image Shape Level{level}'].map(get_height) 
    fig = px.scatter (train_df , 
            x =  width , 
            y = height , 
            color = train_df['data_provider'] , 
            title = f'Image Size Distribution across Data providers')
    fig.update_traces(marker=dict(size=12,
                      line=dict(width=2,color='DarkSlateGrey')),
                      selector=dict(mode='markers')
                  )

    fig.show()
    return level


# In[ ]:


interact (change_level , level = (0 , 2))


# **Note : Above interactive plot might not be visible in comit notebook.**

# **Below plot analyses if the Gradings vary with image size (i.e. Total number of Pixels) at a given resolution level ?**

# In[ ]:


fig = make_subplots(rows=1, 
                    cols=3 , 
                    subplot_titles=("Level 0", 
                                    "Level 1" , 
                                    "Level 2")
                   )
fig.add_trace(go.Violin(
                        x = train_df['isup_grade'] ,
                        y = train_df['Total Pixels Level0'], 
                        points = 'all', name = "Level 0"
                ), row = 1, col = 1 )

fig.add_trace(go.Violin(
                        x = train_df['isup_grade'] ,
                        y = train_df['Total Pixels Level1'], 
                        points = 'all' , name = "Level 1"
                ) , row = 1, col = 2 )


fig.add_trace(go.Violin(
                        x = train_df['isup_grade'] ,
                        y = train_df['Total Pixels Level2'], 
                        points = 'all', name = "Level 2" 
                ), row =1  , col = 3 )

fig.update_layout(
    autosize=True , 
    width=2000,
    height=500 , 
    title = 'Total Pixels distribution by Grading '
)


# Here, we note that distribution is similar across the image sizes.
