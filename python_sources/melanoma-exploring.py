#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
# for dirname, _, filenames in os.walk('/kaggle/input'):
#     for filename in filenames:
#         print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image


# In[ ]:


df_train = pd.read_csv('/kaggle/input/siim-isic-melanoma-classification/train.csv')
df_test = pd.read_csv('/kaggle/input/siim-isic-melanoma-classification/test.csv')


# In[ ]:


print(df_train.info())
print(50*'*')
print(df_test.info())


# In[ ]:


df_train.head()


# In[ ]:


df_train.tail()


# In[ ]:


print(df_train.target.value_counts())
sns.countplot(x='target', data=df_train)


# In[ ]:


print(df_train['sex'].value_counts())
sns.countplot(x='sex',data=df_train)


# In[ ]:


print('Training data image count:', df_train['image_name'].count())
print('Testing data image count:', df_test['image_name'].count())


# In[ ]:


df_train.groupby(['anatom_site_general_challenge']).mean()


# occurrences of cancer is more in the head/neck region 

# In[ ]:


get_ipython().system('ls')


# In[ ]:


get_ipython().system('ls /kaggle/input/siim-isic-melanoma-classification')


# In[ ]:


def resizing_image(img, size):
    img = Image.open(img)
    img = img.resize((size, size), resample=Image.LANCZOS)
    return img


# In[ ]:


#Number of images in train dataset
N = df_train.shape[0]
size = 512
x_train = np.empty((N,size,size,3), dtype=np.uint8)

for i, image_id in enumerate(df_train['image_name']):
    if i < 10:
        img_path = f'/kaggle/input/siim-isic-melanoma-classification/jpeg/train/{image_id}.jpg'
        x_train[i, :, :, :] = resizing_image(img_path, size)
    else:
        break


# In[ ]:


for i in range(9):
    plt.subplot(3,3,i+1)
    plt.subplots_adjust(hspace=0.9)
    plt.imshow(x_train[i,:,:,:])


# In[ ]:


from tensorflow.keras.preprocessing.image import ImageDataGenerator

def visualize(original, augmented):
  fig = plt.figure()
  plt.subplot(1,2,1)
  plt.title('Original image')
  plt.imshow(original)

  plt.subplot(1,2,2)
  plt.title('Augmented image')
  plt.imshow(augmented)


# In[ ]:


image = x_train[2,:,:,:]
flipped = tf.image.flip_left_right(image)
visualize(image, flipped)


# In[ ]:


rotated = tf.image.rot90(image)
visualize(image, rotated)


# In[ ]:


saturated = tf.image.adjust_saturation(image, -1)
visualize(image, saturated)


# In[ ]:


import glob
img_path = '/kaggle/input/siim-isic-melanoma-classification/jpeg/train/*.jpg'
images_list = glob.glob(img_path)
print(images_list[0:5])


# In[ ]:


import cv2
x_images = []
for i in images_list[0:10]:
    img = cv2.imread(i)
    x_images.append(img)


# In[ ]:


print(x_images[0])


# In[ ]:




