#!/usr/bin/env python
# coding: utf-8

# We've noticed our dataset contains images of different sizes, so it would be a good idea to scale them all to one size. 250x250px comes as a logical choice, being that a large number of our images are already in that shape. 
# Some images have colour, others don't. So perhaps convert them all to grayscale. I'm not sure about this, perhaps there are more benefits in extra information from color than there are from making data uniform. But let's go like this for a start, it's easier. 

# In[92]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from tqdm import tqdm
from matplotlib import pyplot as plt

import skimage.io
import skimage.transform
import skimage.color
import skimage.exposure

# Any results you write to the current directory are saved as output.


# In[93]:


trainPath = '../input/stage1_train/'
testPath = '../input/stage1_test/'


# In[94]:


def mergeMasks(imageRoot,imageDirName):
    
    rM,dM,fM=os.walk(imageRoot+imageDirName+"/masks/").__next__()
    maskList=[rM+mask for mask in fM]
    masks=skimage.io.imread_collection(maskList).concatenate()
    s=masks.shape
    
   # Start with a matrix of size the same as the image (or masks)
    labels=np.zeros((s[1],s[2]),np.uint16)
    for i in range(s[0]):
        labels[masks[i]>0]=i+1
        
    return labels


# ## Resize to uniform and convert to grayscale

# In[95]:


height=250
width=250
desiredShape=(height,width)

resizedImagesTrain=[]
resizedMasksTrain=[]
resizedImagesTest=[]

rootTrain,dirsTrain,filesTrain=os.walk(trainPath).__next__()

rootTest,dirsTest,filesTest=os.walk(testPath).__next__()


# Resize train set
print("Processing images in the training directory...")
for id in tqdm(dirsTrain):
    tempImg=skimage.io.imread(rootTrain+id+"/images/"+id+".png")
    tempImg=skimage.transform.resize(tempImg,desiredShape)
    tempImg=skimage.color.rgb2gray(tempImg)
    resizedImagesTrain.append(tempImg)
    
# Resize train masks
print("Resizing masks in the training directory...")
for id in tqdm(dirsTrain):
    allInOneMasks=mergeMasks(rootTrain,id)
    tempImg=skimage.transform.resize(allInOneMasks,desiredShape)
    resizedMasksTrain.append(tempImg)

# Resize test set 
print("Processing images in the test directory...")    
for id in tqdm(dirsTest):
    tempImg=skimage.io.imread(rootTest+id+"/images/"+id+".png")
    tempImg=skimage.transform.resize(tempImg,desiredShape)
    tempImg=skimage.color.rgb2gray(tempImg)
    resizedImagesTest.append(tempImg)
    


# In[48]:


# So our data is now in resizedImagesTrain, resizedMasksTrain and resizedImagesTest
print("--- Resized Images Train --- \n count: {} \n data type: {} \n image shape: {}".format(len(resizedImagesTrain),
                                                                                         type(resizedImagesTrain[0]),
                                                                                         resizedImagesTrain[0].shape))
print("--- Resized Masks Train --- \n count: {} \n data type: {} \n image shape: {}".format(len(resizedMasksTrain),
                                                                                        type(resizedMasksTrain[0]),
                                                                                        resizedMasksTrain[0].shape))
print("--- Resized Images Test --- \n count: {} \n data type: {} \n image shape: {}".format(len(resizedImagesTest),
                                                                                        type(resizedImagesTest[0]),
                                                                                        resizedImagesTest[0].shape))


# In[96]:


plt.subplot(121)
plt.imshow(skimage.io.imread(rootTrain+dirsTrain[44]+"/images/"+dirsTrain[44]+".png"))
plt.title("Original image")

plt.subplot(122)
plt.imshow(resizedImagesTrain[44],cmap="gray")
plt.title("Resized and cast to gray")
plt.show()


# ## Image enhancements?
# Enhance contrast by equalizing the image histograms. Skimage.exposure offers an adaptive version that seems cool.

# In[97]:


# Histogram equalization

print("Equalizing training images...")
equalizedTrain=[skimage.exposure.equalize_adapthist(x) for x in tqdm(resizedImagesTrain)]

print("Equalizing test images...")
equalizedTest=[skimage.exposure.equalize_adapthist(x) for x in tqdm(resizedImagesTest)]



# In[98]:


# check on an example
imId=458

plt.subplot(1,3,1)
plt.imshow(resizedImagesTrain[imId],cmap="gray")

plt.subplot(1,3,2)
plt.imshow(equalizedTrain[imId],cmap="gray")

plt.subplot(1,3,3)
plt.imshow(resizedMasksTrain[imId])
plt.show()


# 
