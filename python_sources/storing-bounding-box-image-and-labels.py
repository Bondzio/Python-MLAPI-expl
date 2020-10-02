#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import xml.etree.ElementTree as ET
import glob
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
from IPython.display import clear_output
glob.glob("../input/all-dogs/*")


# **Taking all the path of annotation files**

# In[ ]:


annoPaths = glob.glob('../input/annotation/Annotation/*/*')
imgPaths = "../input/all-dogs/all-dogs/"
imgSize = (64, 64)


# In[ ]:


print("Total annotation files: ",len(annoPaths))


# ** Looking at annotation file **

# In[ ]:


get_ipython().system('cat ../input/annotation/Annotation/n02105855-Shetland_sheepdog/n02105855_19944')


# ** Function to crop image **
# 
# param : Image Path, Image Name, Coordinates
# 
# return : Cropped Image or None if image not found

# In[ ]:


def makeData(iPath, imgName, bbox):
    imgPath = iPath+imgName+".jpg"
    try:
        img = cv2.cvtColor(cv2.imread(imgPath), cv2.COLOR_BGR2RGB)
        cropped = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        sized = cv2.resize(cropped, (64,64))
    except:
        print(imgName)
        return None
        
    return sized


# ** Function To Fetch Bounding Box from XML File **
# 
# param : All annotation path, Image parent folder path
# 
# return : Cropped Images, Labels to that images

# In[ ]:


def getImgLab(aPath, iPath):
    imgs = []
    labels = []
    for itr, xmlPath in enumerate(aPath):
        tree = ET.parse(xmlPath)
        root = tree.getroot()
        objTags = root.findall('object')
        imgName = xmlPath.split('/')[-1]
        for obj in objTags:
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            label = obj.find('name').text
            bbox = (xmin, ymin, xmax, ymax)
            img = makeData(iPath, imgName, bbox)
            if img is not None:
                imgs.append(img) 
                labels.append(label)
        if itr%500==0:
            clear_output()
            print((itr/len(aPath))*100)     
    return imgs, labels


# In[ ]:


start_time = time.time()
imgs, labels = getImgLab(annoPaths, imgPaths)
print("--- %s minutes ---" % ((time.time() - start_time)/60))


# In[ ]:


fig, ax = plt.subplots(3,3, figsize = (10,10))
for itr, i in enumerate(ax.ravel()):
    i.imshow(imgs[itr])

