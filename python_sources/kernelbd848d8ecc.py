#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# Input data files are available in the "../input/" directory.

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import h5py
import scipy
from PIL import Image
from scipy import ndimage
import os
import datetime as dt
from glob import glob
#from IPython.display import Image
import matplotlib.pylab as plb
import cv2
imgt = cv2.imread("../input/dataset/dataset/test/rottenapples/rotated_by_60_Screen Shot 2018-06-08 at 2.35.25 PM.png")[...,::-1]
plt.imshow(imgt)


# In[ ]:





# In[ ]:


def png_to_hdf5(set_type, file_name):
    if set_type == 0:
        set_name = "train"
    else:
        set_name = "test"
    
    #getting data paths for each set of images  
    start = dt.datetime.now()
    PATH = os.path.abspath(os.path.join('..', 'input'))
    SOURCE_IMAGES_GOOD = os.path.join(PATH, "dataset", "dataset", set_name, "freshapples")
    SOURCE_IMAGES_ROTTEN  = os.path.join(PATH, "dataset", "dataset", set_name, "rottenapples")
    rotten_image_paths = glob(os.path.join(SOURCE_IMAGES_ROTTEN, "*.png"))
    good_image_paths = glob(os.path.join(SOURCE_IMAGES_GOOD, "*.png"))
    
    #We are starting with good images first. This is important to remember for labeling purposes
    all_image_paths = good_image_paths + rotten_image_paths
    
    #size of data
    NUM_Rotten_Images = len(rotten_image_paths)
    NUM_Good_Images = len(good_image_paths)
    NUM_Images = len(all_image_paths)
    HEIGHT = 256
    WIDTH = 256
    CHANNELS = 3
    SHAPE = (HEIGHT, WIDTH, CHANNELS)
    
    SAVE_PATH = os.path.join(file_name)
    
    with h5py.File(SAVE_PATH, 'w') as hf:
        for i, img in enumerate(all_image_paths):
            image = cv2.imread(img)[...,::-1]
            image = cv2.resize(image, (WIDTH,HEIGHT), interpolation=cv2.INTER_CUBIC)
 
            
            Xset = hf.create_dataset(
                name='X'+str(i),
                data=image,
                shape=(HEIGHT, WIDTH, CHANNELS),
                maxshape=(HEIGHT, WIDTH, CHANNELS),
                compression="gzip",
                compression_opts=9)
            
            #labels
            label = 0
            if(i < NUM_Good_Images):
                label = 1
            else:
                label = 0
            
            Yset = hf.create_dataset(
                name='Y'+str(i),
                data = label,
                shape=(1,),
                maxshape=(None,),
                compression="gzip",
                compression_opts=9)
            
            end=dt.datetime.now()
            
        print("\r", i, ": ", (end-start).seconds, "seconds", end="")


# In[ ]:


png_to_hdf5(0, "trainSet")
png_to_hdf5(1, "testSet")


# In[ ]:


get_ipython().system('ls -lha')


# In[ ]:


with h5py.File('trainSet', 'r') as hf:
    plt.imshow(hf["X1"])
    print(hf["Y1"].value)


# In[ ]:


print(hf)


# ## Introduction
# 
# In this tutorial, you will be building a neural network to recognize good fruit from rotten fruit.
# 
# **Building a Neural Network**
# Building a neural network has 5 main steps:
# 
# 1. Initialize parameters
# 2. Define the model and hyperparameters (# of hidden layers, # of hidden units for each layer, activation functions, learning rate, etc.)
# 3. Forward propogation
#     - In this step you compute the computation graph in the forward direction to obtain classification probabilities given the input and compute a cost function
# 4. Backward propogation
# 5. Updating Parameters
# 
# After you have a trained neural network. You can use it for future predictions.
# 
# - In this notebook, you will implement all the functions required to build a deep neural network.
# - In the next assignment, you will use these functions to build a deep neural network for image classification.
# 
# **After this assignment you will be able to:**
# - Use non-linear units like ReLU to improve your model
# - Build a deeper neural network (with more than 1 hidden layer)
# - Implement an easy-to-use neural network class
# 
# **Notation**:
# - Superscript $[l]$ denotes a quantity associated with the $l^{th}$ layer. 
#     - Example: $a^{[L]}$ is the $L^{th}$ layer activation. $W^{[L]}$ and $b^{[L]}$ are the $L^{th}$ layer parameters.
# - Superscript $(i)$ denotes a quantity associated with the $i^{th}$ example. 
#     - Example: $x^{(i)}$ is the $i^{th}$ training example.
# - Lowerscript $i$ denotes the $i^{th}$ entry of a vector.
#     - Example: $a^{[l]}_i$ denotes the $i^{th}$ entry of the $l^{th}$ layer's activations).
# 
# Let's get started!

# In[ ]:





# In[ ]:




