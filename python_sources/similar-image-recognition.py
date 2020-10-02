#!/usr/bin/env python
# coding: utf-8

# In[78]:


import numpy as np
import os, os.path
from PIL import Image


# **get_images_arr** function reads '.jpg' and '.png' files from chosen directory and scale it to ***size*** width

# In[79]:


def get_images_arr(path, size):
    imgs = []
    valid_images = ['.jpg', '.png']
    names = []
    for img in os.listdir(path):
        ext = os.path.splitext(img)[1]
        if ext.lower() not in valid_images:
            continue
        image = Image.open(path + img)
        imgs.append(scale_image(np.asarray(image), size) / 255)
        names.append(image.filename[len(path):])
    return imgs, names


# **Scale_image** function scales picture into size of input parameter ***size***<p> 
# it divides image on ***size***$^2$ areas and avaraging pixel colors in thouse areas

# In[80]:


def scale_image(image, size):
    pix_h = int(image.shape[1] / size)
    pix_w = int(image.shape[0] / size)
    color = np.array([0, 0, 0])
    pxs = np.array([[]])
    pixels = np.zeros((size, size, 3))
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            color[0] = np.average(image[pix_w * (j - 1):pix_w * j, pix_h * (i - 1): pix_h * i, 0])
            color[1] = np.average(image[pix_w * (j - 1):pix_w * j, pix_h * (i - 1): pix_h * i, 1])
            color[2] = np.average(image[pix_w * (j - 1):pix_w * j, pix_h * (i - 1): pix_h * i, 2])
            if (j == 1):
                pxs = np.array(color)
            else:
                pxs = np.vstack((pxs, color))
        pixels[i - 1] = pixels[i - 1] + pxs
    return (pixels)


# **calc_diff** calculates [Euclidian distance](https://en.wikipedia.org/wiki/Euclidean_distance) between images correspinding pixel colors

# In[81]:


def calc_diff(img, img1):
    diff = pow(sum(pow((img - img1), 2)), 1/2)[0]
    return (np.average(diff))


# **print_similar** finds similar images in ***images*** array and prints their names

# In[82]:


def print_similar(images, names):
    i = 0
    for img in images:
        j = 0
        for comp_img in images:
            if (j < i):
                j = j + 1
                continue
            if (j < len(names) and names[i] != names[j] and calc_diff(img, comp_img) < 0.1):
                    print(names[i], names[j])
            j = j + 1
        i = i + 1


# ***Loading images to list of np.array*** <p>
#     by making size to 4 we divide small errors in images by summarising pixel colors in bigger areas
#     and improving speed becouse of small array (4, 4, 3) calculation 

# In[85]:


images, names = get_images_arr("../input/", 4)


# In[86]:


print_similar(images, names)


# In[ ]:




