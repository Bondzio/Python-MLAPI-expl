#!/usr/bin/env python
# coding: utf-8

# In[39]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[40]:


get_ipython().system('ls ../input -R ')


# In[41]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import os
from glob import glob


# In[42]:


all_files = sorted(glob('../input/nmc_90wt_0bar/NMC_90wt_0bar/grayscale/*.tif'))
print(len(all_files), all_files[0])


# In[43]:


from skimage.io import imread
from skimage import img_as_float
first_image = imread(all_files[0])
first_image_float = img_as_float(first_image)


# In[44]:


import matplotlib.pyplot as plt
plt.imshow(first_image_float, cmap = plt.cm.ocean)


# In[45]:


fig, ax1 = plt.subplots(1, 1, figsize = (10, 10))
img_plot_view = ax1.imshow(first_image_float[700:1000, 300:700], cmap = 'gray')
plt.colorbar(img_plot_view)


# In[46]:


fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (20, 10))
ax1.hist(first_image_float[300:700, 300:700].ravel(), 50)
img_plot_view = ax2.imshow(first_image_float[300:700, 300:700], cmap = 'gray')
plt.colorbar(img_plot_view)


# In[47]:


middle_image = imread(all_files[110])
middle_image_float = img_as_float(middle_image)


# In[48]:


fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (20, 10))
ax1.hist(middle_image_float[300:700, 300:700].ravel(), 50)
img_plot_view = ax2.imshow(middle_image_float[300:700, 300:700], cmap = 'gray')
plt.colorbar(img_plot_view)


# In[49]:


roi_image = middle_image_float[300:700, 300:700]
plt.imshow(roi_image>0.5)


# In[50]:


from skimage.measure import regionprops
from skimage.morphology import label
def try_threshold(thresh_val):
    roi_img = middle_image_float[300:700, 300:700]
    seg_img = roi_img>thresh_val
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize = (21, 7))
    ax1.hist(roi_img.ravel(), 50)
    ax1.axvline(thresh_val, color = 'red')
    ax1.set_title('Intensity Distribution')
    ax2.imshow(seg_img)
    ax2.set_title('Threshold Image')
    ax3.hist([c_reg.major_axis_length for c_reg in regionprops(label(seg_img))])
    ax3.set_title('Object Diameters')
    img_plot_view = ax4.imshow(roi_img, cmap = 'gray')
    ax4.set_title('ROI Image')
    plt.colorbar(img_plot_view)
    fig.savefig('thresh_image.pdf')
    return seg_img


# In[51]:


try_threshold(0.5);


# In[52]:


from skimage.filters import try_all_threshold


# In[53]:


try_all_threshold(middle_image_float[300:700, 300:700], figsize = (10,20))


# In[54]:


from skimage.morphology import label
seg_img = try_threshold(0.55)
lab_img = label(seg_img)
print('Objects Found', lab_img.max()+1)


# In[55]:


plt.imshow(lab_img, cmap = 'jet')


# In[56]:


from skimage.segmentation import mark_boundaries
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (15, 7))
ax1.imshow(lab_img, cmap = 'jet')
ax2.imshow(mark_boundaries(middle_image_float[300:700, 300:700], label_img=lab_img))


# #note
#  see paper for voxel size 0.37 x 0.37 x 0.37 micron ^3

# In[58]:



from skimage.measure import regionprops
all_radii = []
for c_reg in regionprops(lab_img):
    all_radii += [c_reg.major_axis_length*0.37]
plt.hist(all_radii, 20)


# In[60]:


np.mean(all_radii)


# Investigate really big particles 
# particles more than 2x the average radius are probably combined or touching in someway.

# In[67]:


big_particles = []
nd_isin = lambda x, ids: np.isin(x.ravel(),ids).reshape(x.shape)
for c_reg in regionprops(lab_img):
    if c_reg.major_axis_length*0.37>20:
        big_particles += [c_reg.label]
plt.imshow(nd_isin(lab_img, big_particles))


# comparing to second sample at 2000 bar 

# In[69]:


hp_files = sorted(glob('../input/nmc_90wt_2000bar/NMC_90wt_2000bar/grayscale/*tif'))
print(len(hp_files), hp_files[0])


# In[70]:


hp_slice = imread(hp_files[110])
hp_slice_float = img_as_float(hp_slice)
hp_slice_float


# In[71]:


fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (20, 10))
ax1.hist(middle_image_float[300:700, 300:700].ravel(), 50)
img_plot_view = ax2.imshow(hp_slice_float[300:700, 300:700], cmap = 'gray')
plt.colorbar(img_plot_view)


# In[72]:


roi_image = hp_slice_float[300:700, 300:700]
plt.imshow(roi_image>0.5)


# In[73]:


from skimage.measure import regionprops
from skimage.morphology import label
def try_threshold(thresh_val):
    roi_img = hp_slice_float[300:700, 300:700]
    seg_img = roi_img>thresh_val
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize = (21, 7))
    ax1.hist(roi_img.ravel(), 50)
    ax1.axvline(thresh_val, color = 'red')
    ax1.set_title('Intensity Distribution')
    ax2.imshow(seg_img)
    ax2.set_title('Threshold Image')
    ax3.hist([c_reg.major_axis_length for c_reg in regionprops(label(seg_img))])
    ax3.set_title('Object Diameters')
    img_plot_view = ax4.imshow(roi_img, cmap = 'gray')
    ax4.set_title('ROI Image')
    plt.colorbar(img_plot_view)
    fig.savefig('thresh_image.pdf')
    return seg_img


# In[74]:


try_threshold(0.5);


# In[76]:


seg_hp_img = hp_slice_float[300:700,300:700]>0.50
lab_hp_img = label(seg_hp_img)
print('Objects Found', lab_hp_img.max()+1)


# In[77]:



from skimage.measure import regionprops
all_hp_radii = []
for c_reg in regionprops(lab_hp_img):
    all_hp_radii += [c_reg.major_axis_length*0.37]
plt.hist(all_hp_radii, 20)


# In[78]:


fig, ax1 = plt.subplots(1,1, figsize = (10,10))
ax1.hist(all_radii, np.linspace(0, 30, 20), label = '0 bar')
ax1.hist(all_hp_radii, np.linspace(0, 30, 20), label = '2000 bar', alpha = 0.5)
ax1.legend()


# In[79]:


from scipy.stats import ttest_ind
ttest_ind(all_radii, all_hp_radii)


# In[ ]:




