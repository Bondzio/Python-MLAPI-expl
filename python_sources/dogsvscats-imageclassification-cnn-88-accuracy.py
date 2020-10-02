#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sea


# In[ ]:


from keras.datasets.mnist import load_data
from keras.layers import Dense,Embedding,Conv2D,MaxPooling2D,Flatten,Dropout
from keras.models import Sequential
from keras.losses import binary_crossentropy
from keras.optimizers import SGD,rmsprop,RMSprop
from keras.metrics import binary_accuracy
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator


# We will use ImageDataGenerator for generating data from the image set.
# 
# We already know that small the size the size of computational data, faster is the processing of neural network. So we will scale the image by factor of 1/255 to bring all the RGB values in range [0,1].

# In[ ]:


trainDataGen=ImageDataGenerator(rescale=1./255)
testDataGen=ImageDataGenerator(rescale=1./255)


# Lets generate the image data for training set and test set.

# In[ ]:


trainData=trainDataGen.flow_from_directory("/kaggle/input/cat-and-dog/training_set/training_set",batch_size=20,class_mode='binary')
testData=testDataGen.flow_from_directory("/kaggle/input/cat-and-dog/test_set/test_set",batch_size=20,class_mode='binary')


# In[ ]:


trainData.image_shape


# So from above block of code we found out that image size is 256x256 and in 3 channel. We can resize the images to smaller size lets say 150x150 so as to decrease the size of feature map generated by CovNets. We can pass **target_size** parameter to flow_from_directory to get the desired size.
# 
# 
# Here lets continue with the original size i.e 256x256

# In[ ]:


Y_train=to_categorical(trainData.classes)
Y_test=to_categorical(testData.classes)


# In[ ]:


Y_train.shape


# In[ ]:


sea.countplot(trainData.classes)


# In[ ]:


sea.countplot(testData.classes)


# So both training set and test set have equal number of samples for both category.

# Now lets begin with network creation.
# 
# We will use CovNet with 3x3 window,128 channel and activation function as 'Relu'

# In[ ]:


network=Sequential()
network.add(Conv2D(128,(3,3),activation='relu',input_shape=(256,256,3)))
network.add(MaxPooling2D((2,2)))
network.add(Conv2D(128,(3,3),activation='relu'))
network.add(MaxPooling2D((2,2)))
network.add(Conv2D(128,(3,3),activation='relu'))
network.add(MaxPooling2D((2,2)))
network.add(Conv2D(128,(3,3),activation='relu'))
network.add(MaxPooling2D((2,2)))
network.add(Conv2D(128,(3,3),activation='relu'))
network.add(Flatten())
network.add(Dropout(0.9))
network.add(Dense(256,activation='relu'))
network.add(Dropout(0.5))
network.add(Dense(256,activation='relu'))
network.add(Dropout(0.5))
network.add(Dense(256,activation='relu'))
network.add(Dense(1,activation='sigmoid'))


# Lets see the summary of our network.

# In[ ]:


network.summary()


# Here we will use RMSprop as optimizers. Its default learning rate is 0.001. I had set it to 0.0001.
# 
# You can also use SGD and set the learning rate and momentum.

# In[ ]:


network.compile(loss='binary_crossentropy',optimizer=RMSprop(lr=0.0001),metrics=['acc'])


# Here we will use fit_generator instead of fit as input to network is going too be generator.
# 
# steps_per_epoch is 250 and epochs is 40. This is going to be highly computationally expensive.

# In[ ]:


network.fit_generator(trainData,steps_per_epoch=250,epochs=40)


# In[ ]:


network.evaluate_generator(testData,steps=250)


# I have added few dropout layers in model to handle overfitting. This has decreased the training accuracy but increased the testing accuracy. 
# 
# Feel free to change the dropout values to see the affect on the accuracy of model.
# 
# Overfitting can also be handlled by bringing in more data which can be done by Data Augmentation. This involves generating more data from existing data.
# 
# For example, a sample image can be rotated,flipped,zoomed or transformed to generate more data.

# This can be done by adding more parameter to the ImageGenerator function to generated image with transformation
# 
# for example:-
# 
# ImageDataGenerator(rescale=1./255,zca_whitening=True,rotation_range=30,vertical_flip=True)

# ****
# ****

# Lets see how to visualize the output of layers of CovNet

# In[ ]:


filename="/kaggle/input/cat-and-dog/training_set/training_set/cats/cat.1.jpg"
plt.imshow(plt.imread(filename))


# Lets create the 4D tensor for image

# In[ ]:


from keras.preprocessing import image

img=image.load_img(filename,target_size=(256,256))
imgArray=image.img_to_array(img)
imgTensor=np.expand_dims(imgArray,axis=0)/255


# In[ ]:


imgTensor.shape


# Lets generate the output of model for our input
# 
# Taking output of first 4 layer

# In[ ]:


from keras import models
layer_output=[layer.output for layer in network.layers[:4]]
activationModel=models.Model(inputs=network.input,output=layer_output)


# For 3rd layer or 2nd CovNet layer

# In[ ]:


activation=activationModel.predict(imgTensor)[2]
activation.shape


# activation output have 128 channel and with size of 254x254

# Plotting the output of 4th channel

# In[ ]:


plt.matshow(activation[0,:,:,4])


# Plotting output for 50th channel

# In[ ]:


plt.matshow(activation[0,:,:,50])


# In[ ]:




