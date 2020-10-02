#!/usr/bin/env python
# coding: utf-8

# ## Global Wheat Detection
# #### Can you help identify wheat heads using image analysis?
# 
# The roadmap we intend to follow:
# 1. Draw out some of the images and try to make some inferences via naked eye.
# 2. Then we will merge and prepapre the data for images and mark them with the labelled data from the CSV file.
# 3. Then we will approach MODELLING for our prepared dataset!.
# 4. We would like to try out few of the things mentioned below and will not be dissapointe few of the things don't work out:
#     1. Use Pretrained CNN Model to share the weights and prevent training from scratch.
#     2. Try to see out if we can apply Transfer Learning for better results.
#     3. Playing with Image Scaling, Number of Channels. My though process is that we should be processing the images in BLACK and WHITE channel as the riped crop will be having features like large size and larger height than the others. So we need to try this out!.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from PIL import Image
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


# We will use 2 images: -> 86b661ae0 and dc8b73725. First we will try to print the original images and then we'll print the same in B&W.

# We need to find the status of these 2 Images, what is the Target Value?

training_data = pd.read_csv('/kaggle/input/global-wheat-detection/train.csv')
unique_id=training_data['image_id'].value_counts()
source_86b661ae0 = training_data.loc[training_data['image_id'] == '86b661ae0']
source_dc8b73725 = training_data.loc[training_data['image_id'] == 'dc8b73725']
print(source_86b661ae0.source.value_counts())
print(source_dc8b73725.source.value_counts())
print(training_data.head())
unique_id


# In[ ]:


import pathlib
import imageio
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

plt.figure(figsize=(16,16))
plt.subplot(1,2,1)
img_array = np.array(Image.open('../input/global-wheat-detection/train/86b661ae0.jpg'))
index=np.where(training_data['image_id'] == '86b661ae0')
plt.title('arvalis_1');
plt.imshow(img_array);
plt.subplot(1,2,2)
img = Image.open('../input/global-wheat-detection/train/86b661ae0.jpg')
img.thumbnail((120, 120), Image.ANTIALIAS)
plt.title('arvalis_1');
imgplot = plt.imshow(img);
#plt.imshow(img_array);
print(index)


# In[ ]:


plt.figure(figsize=(16,16))
plt.subplot(1,2,1)
img_array = np.array(Image.open('../input/global-wheat-detection/train/dc8b73725.jpg'))
plt.title('arvalis_1');
plt.imshow(img_array);
plt.subplot(1,2,2)
img = Image.open('../input/global-wheat-detection/train/dc8b73725.jpg')
img.thumbnail((120, 120), Image.ANTIALIAS)
plt.title('arvalis_1');
imgplot = plt.imshow(img);


# In[ ]:


# Let's print the same images in B&W color!
plt.figure(figsize=(18,18))
plt.subplot(1,2,1)
images = ['../input/global-wheat-detection/train/dc8b73725.jpg','../input/global-wheat-detection/train/86b661ae0.jpg']
image_file = Image.open(images[0]) # open colour image
image_file = image_file.convert('1') # convert image to black and white
imgplot = plt.imshow(image_file);
plt.subplot(1,2,2)
image_file = Image.open(images[1]) # open colour image
image_file = image_file.convert('1') # convert image to black and white
imgplot = plt.imshow(image_file);

# We will be trying some more experiments, like checking out the resolution before getting into Modelling and try to print the features for these 2 images as sample!.


# In[ ]:


import ast 
import cv2
#print(training_data.iloc[index[0][0]])
plt.figure(figsize=(18,18))
img=cv2.imread(images[1])
for i in range(0,len(index[0])):
    string=training_data.iloc[index[0][i]]['bbox']
    #image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #image=cv2.resize(image,(120,120))
    array=ast.literal_eval(string)
    pt1=(array[0],array[1])
    pt2=(array[0]+array[2],array[1]+array[3])
    #print(array)
    img=cv2.rectangle(img,pt1,pt2,(255,0,0),10)
plt.imshow(img,cmap='gray');
#plt.savefig()


# In[ ]:


image=Image.open(images[0])
image1=Image.open(images[1])


# In[ ]:


histogram = image.histogram()
# Take only the Red counts
l1 = histogram[0:256]
# Take only the Blue counts
l2 = histogram[256:512]
# Take only the Green counts
l3 = histogram[512:768]


# In[ ]:


def getRed(redVal):
    return '#%02x%02x%02x' % (redVal, 0, 0)
def getGreen(greenVal):
    return '#%02x%02x%02x' % (0, greenVal, 0)
def getBlue(blueVal):
    return '#%02x%02x%02x' % (0, 0, blueVal)
plt.figure(0)
# R histogram

for i in range(0, 256):
    plt.bar(i, l1[i], color = getRed(i), edgecolor=getRed(i), alpha=0.3)

# G histogram
plt.figure(1)
for i in range(0, 256):
    plt.bar(i, l2[i], color = getGreen(i), edgecolor=getGreen(i),alpha=0.3)

# B histogram
plt.figure(2)
for i in range(0, 256):
    plt.bar(i, l3[i], color = getBlue(i), edgecolor=getBlue(i),alpha=0.3)
plt.figure(3)
plt.imshow(image)


plt.show()


# In[ ]:


histogram = image1.histogram()
# Take only the Red counts
l1 = histogram[0:256]
# Take only the Blue counts
l2 = histogram[256:512]
# Take only the Green counts
l3 = histogram[512:768]


# In[ ]:



plt.figure(0,figsize=(6,3))
# R histogram

for i in range(0, 256):
    
    plt.bar(i, l1[i], color = getRed(i), edgecolor=getRed(i), alpha=0.3)

# G histogram

plt.figure(1,figsize=(6,3))
for i in range(0, 256):
    
    plt.bar(i, l2[i], color = getGreen(i), edgecolor=getGreen(i),alpha=0.3)

# B histogram

plt.figure(2,figsize=(6,3))
for i in range(0, 256):
    
    plt.bar(i, l3[i], color = getBlue(i), edgecolor=getBlue(i),alpha=0.3)

plt.figure(3,figsize=(6,3))

plt.imshow(image1)
plt.show()


# In[ ]:


import os
os.mkdir("/kaggle/working/bboximages/")


# In[ ]:


tempdir='/kaggle/input/global-wheat-detection/train'
training_data = pd.read_csv('/kaggle/input/global-wheat-detection/train.csv')
file=os.listdir(tempdir)
len(file)


# In[ ]:


import ast
import cv2
from skimage.io import imsave
for i in range(0,len(file)):
    img=cv2.imread(os.path.join(tempdir,file[i]))
    text=file[i].split('.')[0]
    source= training_data.loc[training_data['image_id'] ==text]
    ind=np.where(training_data['image_id'] ==text)
    for j in range(0,len(ind[0])):
        string=training_data.iloc[ind[0][j]]['bbox']
        #image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #image=cv2.resize(image,(120,120))
        array=ast.literal_eval(string)
        pt1=(int(array[0]),int(array[1]))
        pt2=(int(array[0]+array[2]),int(array[1]+array[3]))
        #print(array)
        target_img=cv2.rectangle(img,pt1,pt2,(255,0,0),10)
    imsave('/kaggle/working/bboximages/target_{}.jpg'.format(text),target_img)


# In[ ]:


tempdir1='/kaggle/working/bboximages'

file1=os.listdir(tempdir1)
len(file1)


# So, i'll explain what we have done!
# 1. We have tried to Finalise the Channel for our Modelling and we figure out that **RED** to be the channel for modelling as pixel intensity is uniform across most of the images.
# 2. Then we plotted out the *bboxes* over the images as part of EDA.
# 3. Then we are saving the **images**of the booxes images which will be used for Modelling!.
# 4. Next, we'll just plot some 2 random images and then start working for preparing the data for Modelling!
# 5. Finally, we can see that the number of images are matching with the CSV Count.

# In[ ]:


#3248-45
# pritning two random images!
import matplotlib.pyplot as plt
plt.figure(figsize=(15,18))
image1 = file[10]
image2 = file1[2809]
plt.subplot(1,2,1)
print('Image: ',image1)
img_array_1 = np.array(Image.open(tempdir+'/' + image1))
plt.imshow(img_array_1);
plt.subplot(1,2,2)
print('Target: ',image2)
img_array_2 = np.array(Image.open(tempdir1+'/' + image2))
plt.imshow(img_array_2);


# In[ ]:


np.shape(img_array_2 )


# Wow, everything looks fine!. Guess Next What?
# Let's Start out Modelling process!

# In[ ]:


x=np.zeros((len(file),256,256,3))
y=np.zeros((len(file),256,256,3))
for i in range(0,len(file)):
    for j in range(0,len(file1)):
        if file[i]==file1[j][7:]:
            img=cv2.imread(os.path.join(tempdir,file[i]))
            image=cv2.resize(img,(256,256))
            tar=cv2.imread(os.path.join(tempdir1,file1[j]))
            target=cv2.resize(tar,(256,256))
            break
    x[i,:,:,:]=image
    y[i,:,:,:]=target
            


# In[ ]:


num=100
plt.figure(figsize=(15,18))
plt.subplot(1,2,1)
plt.imshow(x[num]/255)
plt.subplot(1,2,2)
plt.imshow(y[num]/255)
plt.show()

