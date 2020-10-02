#!/usr/bin/env python
# coding: utf-8

# This kernel is essentially copy-paste from another kerenl:
# [https://www.kaggle.com/bguberfain/elastic-transform-for-data-augmentation](http://)
# written by Bruno G. do Amaral. I'm relatively new to Kaggle system, so if there is a way to fork kernel from different competition, please let me know.
# 
# It demonstrate the use of elastic_transform as suggested by the authors of the original U-Net article as a mean for data augmentation :
# [https://arxiv.org/abs/1505.04597](http://)
# 
# Note that the current implementation support only gray-scale images. Some work need to be done in order to use it for color images.
# 
# 

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import skimage.io
from skimage import color
from skimage import io
import glob
import cv2
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt


# In[ ]:


image_id = "0d3640c1f1b80f24e94cc9a5f3e1d9e8db7bf6af7d4aba920265f46cadc25e37"
image_dir = "../input/stage1_train/{image_id}/masks/".format(image_id=image_id)
image_sb20182 = skimage.io.imread("../input/stage1_train/{image_id}/images/{image_id}.png".format(image_id=image_id),as_gray=True)
image_sb2018= color.rgb2gray(image_sb20182)


# In[ ]:


all_masks_files = glob.glob(image_dir+"*.png")
final_mask = []
for item in all_masks_files:
    image_sb2018_mask = cv2.imread(item,-1)
    final_mask.append(image_sb2018_mask)
image_sb2018_mask= np.max(final_mask,axis=0) 
image_sb2018_mask = image_sb2018_mask/np.max(image_sb2018_mask)
plt.imshow(image_sb2018_mask)


# In[ ]:


#taken from: https://www.kaggle.com/bguberfain/elastic-transform-for-data-augmentation
# Function to distort image
def elastic_transform(image, alpha, sigma, alpha_affine, random_state=None):
    """Elastic deformation of images as described in [Simard2003]_ (with modifications).
    .. [Simard2003] Simard, Steinkraus and Platt, "Best Practices for
         Convolutional Neural Networks applied to Visual Document Analysis", in
         Proc. of the International Conference on Document Analysis and
         Recognition, 2003.

     Based on https://gist.github.com/erniejunior/601cdf56d2b424757de5
    """
    if random_state is None:
        random_state = np.random.RandomState(None)

    shape = image.shape
    shape_size = shape[:2]
    
    # Random affine
    center_square = np.float32(shape_size) // 2
    square_size = min(shape_size) // 3
    pts1 = np.float32([center_square + square_size, [center_square[0]+square_size, center_square[1]-square_size], center_square - square_size])
    pts2 = pts1 + random_state.uniform(-alpha_affine, alpha_affine, size=pts1.shape).astype(np.float32)
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(image, M, shape_size[::-1], borderMode=cv2.BORDER_REFLECT_101)

    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dz = np.zeros_like(dx)

    x, y, z = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]), np.arange(shape[2]))
    indices = np.reshape(y+dy, (-1, 1)), np.reshape(x+dx, (-1, 1)), np.reshape(z, (-1, 1))

    return map_coordinates(image, indices, order=1, mode='reflect').reshape(shape)


# In[ ]:


# Define function to draw a grid
def draw_grid(im, grid_size):
    # Draw grid lines
    for i in range(0, im.shape[1], grid_size):
        cv2.line(im, (i, 0), (i, im.shape[0]), color=(1,))
    for j in range(0, im.shape[0], grid_size):
        cv2.line(im, (0, j), (im.shape[1], j), color=(1,))

# Load images
im = image_sb2018
im_mask = image_sb2018_mask

# Draw grid lines
draw_grid(im, 50)
draw_grid(im_mask, 50)

# Merge images into separete channels (shape will be (cols, rols, 2))
im_merge = np.concatenate((im[...,None], im_mask[...,None]), axis=2)
# im_merge = np.concatenate((im[...,None]), axis=2)

get_ipython().run_line_magic('matplotlib', 'inline')

# Apply transformation on image
im_merge_t = elastic_transform(im_merge, im_merge.shape[1] * 2, im_merge.shape[1] * 0.08, im_merge.shape[1] * 0.08)

# Split image and mask
im_t = im_merge_t[...,0]
im_mask_t = im_merge_t[...,1]

# Display result
plt.figure(figsize = (16,14))
plt.imshow(np.c_[np.r_[im, im_mask], np.r_[im_t, im_mask_t]], cmap='gray')
# plt.imshow(np.c_[np.r_[im], np.r_[im_t]], cmap='gray')


# In[ ]:




