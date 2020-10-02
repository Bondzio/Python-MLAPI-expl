#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import cv2 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


get_ipython().system('cd ../input/cat-dog-images/CATS_DOGS')


# In[ ]:


sample = cv2.imread("../input/cat-dog-images/CATS_DOGS/train/DOG/8317.jpg")
sample = cv2.cvtColor(sample,cv2.COLOR_BGR2RGB)
plt.imshow(sample)


# In[ ]:


sample = cv2.imread("../input/cat-dog-images/CATS_DOGS/train/CAT/4.jpg")
sample = cv2.cvtColor(sample,cv2.COLOR_BGR2RGB)
plt.imshow(sample)


# In[ ]:


#image data generator from keras
from keras.preprocessing.image import ImageDataGenerator


# In[ ]:


#some amount of data augmentation will help to train the model
image_gen = ImageDataGenerator(rotation_range=30,
                              width_shift_range=0.1,
                              height_shift_range=0.1,
                              rescale=1/255, #it takes of normalization
                              shear_range=0.2,
                              zoom_range=0.2,
                              horizontal_flip=True,
                              fill_mode='nearest', #needed especially when stretching the image
                              )


# In[ ]:


#the transformation is random and the above values are just the upper ranges
plt.imshow(image_gen.random_transform(sample))


# In[ ]:


image_gen.flow_from_directory('../input/cat-dog-images/CATS_DOGS/train')


# In[ ]:


from keras.models import Sequential


# In[ ]:


from keras.layers import Activation,Dropout,Flatten,Conv2D,MaxPooling2D,Dense


# In[ ]:


input_shape = (150,150,3)


# In[ ]:


model = Sequential()

model.add(Conv2D(filters=32,kernel_size=(3,3),
                input_shape=input_shape,
                activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(filters=64,kernel_size=(3,3),
                input_shape=input_shape,
                activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(filters=64,kernel_size=(3,3),
                input_shape=input_shape,
                activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(128))
model.add(Activation('relu'))

model.add(Dropout(0.5))

model.add(Dense(1))
model.add(Activation('sigmoid'))


# In[ ]:


model.compile(loss='binary_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])


# In[ ]:


model.summary()


# In[ ]:


batch_size = 16

train_image_gen = image_gen.flow_from_directory('../input/cat-dog-images/CATS_DOGS/train',
                                               target_size = input_shape[:2],
                                               batch_size = batch_size,
                                               class_mode = 'binary')


# In[ ]:


test_image_gen = image_gen.flow_from_directory('../input/cat-dog-images/CATS_DOGS/test',
                                               target_size = input_shape[:2],
                                               batch_size = batch_size,
                                               class_mode = 'binary')


# In[ ]:


train_image_gen.class_indices


# In[ ]:


import warnings
warnings.filterwarnings('ignore')
result = model.fit_generator(train_image_gen,epochs=50,steps_per_epoch=200,
                            validation_data=test_image_gen,
                            validation_steps=12)


# In[ ]:


plt.plot(result.history['accuracy'])


# In[ ]:


#predicting on a new image
dog_file = '../input/cat-dog-images/CATS_DOGS/test/DOG/9408.jpg'


# In[ ]:


from keras.preprocessing import image


# In[ ]:


dog_img = image.load_img(dog_file,target_size=input_shape[:2])


# In[ ]:


dog_img = image.img_to_array(dog_img)


# In[ ]:


dog_img.shape


# In[ ]:


#WE NEED TO MAKE THIS IMAGE AS A BATCH WITH 1 IMAGE
dog_img = np.expand_dims(dog_img,axis=0)


# In[ ]:


dog_img.shape


# In[ ]:


dog_img = dog_img/255


# In[ ]:


print("DOG") if model.predict_classes(dog_img) else print("CAT")


# In[ ]:


#how sure was the above model
model.predict(dog_img)


# In[ ]:


model.save("custom_one.h5")


# In[ ]:




