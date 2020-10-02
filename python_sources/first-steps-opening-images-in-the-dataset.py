#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os.path
import pydicom
import shutil


# In[ ]:


image_base_path = "../input/mamographysampleimages/sample_images/data_sample/train/"


# In[ ]:


raw_csv = pd.read_csv("../input/mamography-train-dataset/train.csv")


# In[ ]:


raw_csv.head()


# In[ ]:


# Here we filter the images that come in the sample dataset, this is NOT needed for the complete dataset
raw_csv = raw_csv[(image_base_path + raw_csv["image file path"]).apply(os.path.isfile)]


# In[ ]:


raw_csv['image file path'][0]


# In[ ]:


raw_csv['cropped image file path'][0]


# In[ ]:


raw_csv['ROI mask file path'][0]


# ### read .dcm images 

# In[ ]:


print(__doc__)

# FIXME: add a full-sized MR image in the testing data
filename = image_base_path + raw_csv['image file path'][0]
ds = pydicom.dcmread(filename)

# get the pixel information into a numpy array
data = ds.pixel_array
print('The image has {} x {} voxels'.format(data.shape[0],
                                            data.shape[1]))
data_downsampling = data[::8, ::8]
print('The downsampled image has {} x {} voxels'.format(
    data_downsampling.shape[0], data_downsampling.shape[1]))

# copy the data back to the original data set
ds.PixelData = data_downsampling.tobytes()
# update the information regarding the shape of the data array
ds.Rows, ds.Columns = data_downsampling.shape


# In[ ]:


ds0 = pydicom.dcmread(image_base_path + raw_csv['image file path'][0])
plt.imshow(ds0.pixel_array, cmap=plt.cm.bone)


# In[ ]:


ds1 = pydicom.dcmread(image_base_path + raw_csv['cropped image file path'][0])
plt.imshow(ds1.pixel_array, cmap=plt.cm.bone)


# In[ ]:



ds2 = pydicom.dcmread(image_base_path + raw_csv['ROI mask file path'][0])
plt.imshow(ds2.pixel_array, cmap=plt.cm.bone)


# In[ ]:


ds_masked = np.zeros(ds0.pixel_array.shape)
idx =  ds1.pixel_array==255
ds_masked[idx] = ds0.pixel_array[idx]
plt.imshow(ds_masked, cmap=plt.cm.bone)


# In[ ]:




