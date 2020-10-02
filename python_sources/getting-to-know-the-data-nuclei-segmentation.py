#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import skimage.io

from tqdm import tqdm
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# ### Data
# 
# This dataset contains a large number of segmented nuclei images. The images were acquired under a variety of conditions and vary in the cell type, magnification, and imaging modality (brightfield vs. fluorescence). The dataset is designed to challenge an algorithm's ability to generalize across these variations.
# 
# Each image is represented by an associated ImageId. Files belonging to an image are contained in a folder with this ImageId. Within this folder are two subfolders:
# 
# **images **contains the image file.
# **masks** contains the segmented masks of each nucleus. This folder is only included in the training set. Each mask contains one nucleus. Masks are not allowed to overlap (no pixel belongs to two masks).
# 
# You'll notice the images and masks are in a zip archive. Kaggle says: 
# ZIP archive files will be uncompressed and their contents available at the root folder when this dataset is used in Kernels.
# You can see this by listing the archive (Showing the first 5 names here).
# But what you wanna do is "walking" the archive - this does not return a value, it's a generator object. Navigate with __next__() method.

# In[2]:


dataTrainPath="../input/stage1_train/"
dataTestPath="../input/stage1_test/"

root,dirs,files=os.walk(dataTrainPath).__next__()


# Your folder names look like this:

# In[ ]:


print(dirs[0:5],"\n")
print("And there are {} of them".format(len(dirs)))


# Each directory contains the following directories:

# In[ ]:


print(os.listdir(root+dirs[0]))


# And what's inside of them? Here's an example:

# In[3]:


rIm,dIm,fIm=os.walk(root+dirs[0]+"/images/").__next__()
print("This is an example image file name: ",fIm)
rM,dM,fM=os.walk(root+dirs[0]+"/masks/").__next__()
print("Example mask file name: \n ",fM)
print("Well, look at that, multiple masks for one image file. \nAll .png format.")


# Okay, so what do they look like?

# In[4]:


print("This is an image")
im=mpimg.imread(rIm+fIm[0])
plt.imshow(im)
plt.show()


# In[5]:


print("These are the corresponding masks")
for mask in fM:
    iMask=mpimg.imread(rM+mask)
    plt.imshow(iMask)
    plt.show()


# So um...all masks are saved separately :/ Can we view them aggregated?
# Apparently, scikitlearn has a useful image processing collection of algorithms: skimage (you'll find it loaded in the beginning)

# In[6]:


maskList=[rM+mask for mask in fM]
masks=skimage.io.imread_collection(maskList).concatenate()
s=masks.shape
print("Shape of this squashed masks ndarray: ",s) #so number of masks, dimension1, dimension2

# Start with a matrix of size the same as the image (or masks)
labels=np.zeros((s[1],s[2]),np.uint16)

for i in range(s[0]):
    labels[masks[i]>0]=i+1

# And there you have it
print("MASKS all together:")
plt.imshow(labels)
plt.show()

# Just to compare again with the original image:
print("IMAGE:")
plt.imshow(im)
plt.show()


# ### How many masks (nuclei) per image?

# In[7]:


numMasks=np.zeros(len(dirs),np.uint16)
for i,dirName in enumerate(dirs):
    tempR,tempD,tempF=os.walk(root+dirName+"/masks/").__next__()
    numMasks[i]=len(tempF)
plt.hist(numMasks,40)
plt.xlabel("Number of masks per image")
plt.show()

dfNumMasks=pd.DataFrame(numMasks,columns=["NumNuclei"])
dfNumMasks.describe()


# Okay, all directories contain at least one mask, so no need to worry about that. 
# Most of them have below 54, but some have as many as 375! I wanna see those.

# In[8]:


# Let me adapt the above code for merging masks into a function
def mergeNPlotMasks(imageRoot,imageDirName):
    imageFileName=imageRoot+imageDirName+"/images/"+imageDirName+".png"
    image=skimage.io.imread(imageFileName)
    
    rM,dM,fM=os.walk(imageRoot+imageDirName+"/masks/").__next__()
    maskList=[rM+mask for mask in fM]
    masks=skimage.io.imread_collection(maskList).concatenate()
    s=masks.shape
    
   # Start with a matrix of size the same as the image (or masks)
    labels=np.zeros((s[1],s[2]),np.uint16)
    for i in range(s[0]):
        labels[masks[i]>0]=i+1

    # And there you have it
    print("MASKS all together:")
    plt.imshow(labels)
    plt.show()

    # Just to compare again with the original image:
    print("IMAGE:")
    plt.imshow(image)
    plt.show()


# In[9]:


for i,dirName in enumerate(dirs):
    tempR,tempD,tempF=os.walk(root+dirName+"/masks/").__next__()
    if len(tempF)>300:
        print("#",i)
        mergeNPlotMasks(root,dirName)


# Look at that nasty little rascal at #198!

# ### What about image sizes?

# In[10]:


imageAreas=[]
imageLevels=[]
for dirName in dirs:
    tempImage=skimage.io.imread(root+dirName+"/images/"+dirName+".png")
    imageAreas.append(tempImage.shape[0]*tempImage.shape[1])
    imageLevels.append(tempImage.shape[2])
plt.hist(imageAreas,20)
plt.xlabel("Image area [pixels]")
plt.show()

plt.hist(imageLevels,20)
plt.xlabel("Levels")
plt.show()

dfImageSizes=pd.DataFrame(imageAreas,columns=["image_area_pxls"])
dfImageSizes.describe()


# So there are images of substantially different sizes, though most of them are small
# 
# And all of them have 4 levels. Hm, four? Sanity check? 
# 
# RGBA, I suppose. Let's see the values of this 4th item.

# In[12]:


alphaMeans=[]
for dirName in tqdm(dirs):
    tempImage=skimage.io.imread(root+dirName+"/images/"+dirName+".png")
    tempAlpha=[tempImage[i,j,3] for i in range(0,tempImage.shape[0])for j in range(0,tempImage.shape[1])]
    alphaMeans.append(np.mean(tempAlpha))
dfAlphaMeans=pd.DataFrame(alphaMeans,columns=["Alpha levels"])
dfAlphaMeans.describe()


# Okay, apparently there is no other value of this fourth parameter than 255, so we should not take it into consideration when training a model, as it contains no useful info.
