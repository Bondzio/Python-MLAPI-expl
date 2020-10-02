#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
get_ipython().run_line_magic('reset', '-f')

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:


from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import load_img


# In[ ]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense


# In[ ]:


from tensorflow.keras import backend as K
from tensorflow.keras.models import model_from_json


# In[ ]:


import os
import matplotlib.pyplot as plt
import time


# In[ ]:


from sklearn import metrics
from PIL import Image


# In[ ]:


print(os.listdir("../input"))


# In[ ]:


main_dir =os.listdir("../input")
print(main_dir)


# In[ ]:


training_folder= "../input/chest-xray-pneumonia/chest_xray/train/"
validation_folder = "../input/chest-xray-pneumonia/chest_xray/val/"
testing_folder = "../input/chest-xray-pneumonia/chest_xray/test/"


# In[ ]:


training_n = training_folder+'NORMAL/'
training_p = training_folder+'PNEUMONIA/'


# In[ ]:


img_width, img_height = 200, 200


# In[ ]:


nb_train_samples = 16


# In[ ]:


batch_size = 48


# In[ ]:


epochs = 3


# In[ ]:


print(training_n)


# In[ ]:


print(training_p)


# In[ ]:


r_norm=np.random.randint(0,len(os.listdir(training_n)))
r_norm 
normal_pic=os.listdir(training_n)[r_norm]
normal_pic
normal_pic_addr=training_n+normal_pic
normal_pic_addr
rand_ppic=np.random.randint(0,len(os.listdir(training_p)))
sick_pic=os.listdir(training_p)[r_norm]
sick_addr = training_p+sick_pic
sick_addr
normal_load=Image.open(normal_pic_addr)
normal_load
sick_load=Image.open(sick_addr)
sick_load


# In[ ]:



f=plt.figure(figsize=(12,8))
a1=f.add_subplot(2,4,1)
img_plot=plt.imshow(normal_load)
a1.set_title('Normal XRay')

a2=f.add_subplot(2,4,4)
img_plot=plt.imshow(sick_load)
a2.set_title('Pneumonia XRay')


# In[ ]:


test_generator_samples = 624
test_batch_size = 32


# In[ ]:


K.image_data_format()
K.backend()


# In[ ]:


if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)


# In[ ]:


model = Sequential()


# In[ ]:


model.add(Conv2D(
	             filters=48,                        
                 kernel_size=(3, 3),              
	             strides = (1,1),                 
	             input_shape=input_shape,          
	             use_bias=True,                    
	             padding='same',                  
	             name="Ist_conv_layer",
				 activation='relu'
	             )
         )


# In[ ]:


model.summary()


# In[ ]:


model.add(Conv2D(
	             filters=64,                       	                                             
	             kernel_size=(3, 3),               
	             strides = (1,1),            
	             use_bias=True,                     
	             padding='same',                   
	             name="IInd_conv_layer",
				 activation='relu'              ##sigmoid 
	             )
         )


# In[ ]:


model.summary()


# In[ ]:


model.add(MaxPool2D())


# In[ ]:


model.summary()


# In[ ]:


model.add(Conv2D(
	             filters=16,                       # For every filter there is set of weights
	                                               # For each filter, one bias. So total bias = 16
	             kernel_size=(3, 3),               # For each filter there are 3*3=9 kernel_weights
	             strides = (1,1),                  # So output shape will be 148 X 148 (W-F+1).
	                                               # Default strides is 1 only
	             use_bias=True,                     # Default value is True
	             padding='same',                   # 'valid' => No padding. This is default.
	             name="IIIrd_conv_layer"
	             )
         )


# In[ ]:


model.summary()


# In[ ]:


model.add(Flatten(name = "FlattenedLayer"))
model.add(Dense(105))
model.add(Activation('relu'))
model.add(Dense(78))
model.add(Activation('relu'))

model.add(Dense(1))
model.add(Activation('sigmoid'))
model.summary()


# In[ ]:


model.summary()
model.compile(
              loss='binary_crossentropy',  
              optimizer='rmsprop',         
              metrics=['accuracy'])
model.summary()


# In[ ]:


def preprocess(img):

    return img


# In[ ]:


tr_dtgen = ImageDataGenerator(
                              rescale=1. / 255,      # Normalize colour intensities in 0-1 range
                              shear_range=0.2,       # Shear varies from 0-0.2
                              zoom_range=0.2,
                              horizontal_flip=True,
                              preprocessing_function=preprocess
                              )


# In[ ]:


train_generator = tr_dtgen.flow_from_directory(
                                               training_folder,
                                               target_size=(img_width, img_height),  # Resize images
                                               batch_size=batch_size,  # Return images in batches
                                               class_mode='binary'   # Output labels will be 1D binary labels
                                                                     # [1,0,0,1]
                                                                     # If 'categorical' output labels will be
                                                                     # 2D OneHotEncoded: [[1,0],[0,1],[0,1],[1,0]]
                                                                     # If 'binary' use 'sigmoid' at output
                                                                     # If 'categorical' use softmax at output

                                                )


# In[ ]:


val_dtgen = ImageDataGenerator(rescale=1. / 255)


# In[ ]:


validation_generator = val_dtgen.flow_from_directory(
                                                     validation_folder,
                                                     target_size=(img_width, img_height),   # Resize images
                                                     batch_size=batch_size,    # batch size to augment at a time
                                                     class_mode='binary'  # Return 1D array of class labels
                                                     )


# In[ ]:


start = time.time()   # 6 minutes
for e in range(epochs):
    print('Epoch', e)
    batches = 0
    for x_batch, y_batch in train_generator:
        model.fit(x_batch, y_batch)
        batches += 1
        print ("Epoch: {0} , Batches: {1}".format(e,batches))
        if batches > 200:    # 200 * 16 = 3200 images
            # we need to break the loop by hand because
            # the generator loops indefinitely
            break

end = time.time()
(end - start)/60


# In[ ]:


result = model.evaluate(validation_generator,
                                  verbose = 1,
                                  steps = 4        
                                  )


# In[ ]:


result

