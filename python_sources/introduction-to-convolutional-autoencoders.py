#!/usr/bin/env python
# coding: utf-8

# ### The aim of this notebook is to provide an insight into how the autoencoder works and how you can also deploy it for your use. We will be using Convolutional autoencoders to regenerate the images fed to the network by creating a bottleneck as described in the original paper.

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


import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.keras as keras
get_ipython().run_line_magic('matplotlib', 'inline')


# ## We will use mnist dataset which already comes with Keras 

# In[ ]:


from tensorflow.keras.datasets import mnist, fashion_mnist

(xtrain,ytrain), (xtest, ytest)= mnist.load_data() 


# In[ ]:


#Rescaling the arrays
xtrain, xtest= xtrain/255 , xtest/255


# In[ ]:


##Visualizaing the images

import matplotlib.pyplot as plt
f, ax = plt.subplots(1,5)
f.set_size_inches(80, 40)
for i in range(5,10):
    ax[i-5].imshow(xtrain[i].reshape(28, 28))
plt.show()


# ## Now we will reshape the input according to the autoencoder model. 

# In[ ]:


xtrain= xtrain.reshape(-1,28,28,1)


# In[ ]:


xtest=xtest.reshape(-1,28,28,1)


# ## We will define the autoencoder model based on CNN and not normal neural network.
# 
# 

# Max pooling operations are non invertible in nature but the feature maps can be regenerated by recording the locations of the mxaima that were performed during MaxPooling. Upsampling leverages this property to establish the image from the bottleneck.

# In[ ]:


from keras.models import Sequential, Model
from keras.layers import Dense, Conv2D, MaxPooling2D,MaxPool2D ,UpSampling2D, Flatten, Input
from keras.optimizers import SGD, Adam, Adadelta, Adagrad
from keras import backend as K

def autoencoder():
    
    e0= Input(shape= (28,28,1))
    
    e1= Conv2D(64, (3,3), activation= 'relu', padding='same')(e0)
    e1= MaxPooling2D((2,2), padding= 'same')(e1)
    e2= Conv2D(32, (3,3), activation= 'relu', padding= 'same')(e1)
    e2= MaxPooling2D((2,2), padding= 'same')(e2)
    e3= Conv2D(16, (3,3), activation= 'relu', padding= 'same')(e2)
    
    latent= MaxPooling2D((2,2), padding= 'same')(e3)
    
    d1= Conv2D(16, (3,3), activation= 'relu', padding= 'same')(latent)
    d1= UpSampling2D((2,2))(d1)
    d2= Conv2D(32, (3,3), activation= 'relu', padding= 'same')(d1)   #Note that no padding is mentioned here...
    d2= UpSampling2D((2,2))(d2)
    d3= Conv2D(64, (3,3), activation= 'relu')(d2)
    d3= UpSampling2D((2,2))(d3)
    d4= Conv2D(1, (3,3), padding='same',activation= 'relu')(d3)
    
    model= Model(e0, d4)
    model.compile(optimizer= 'adam', loss= 'binary_crossentropy')
    
    return model



# In[ ]:


model= autoencoder()
model.summary()


# In[ ]:


xtrain.shape


# In[ ]:


import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))


# ## tf code for using GPU
# 
# Note that we have used Early stopping so you dont have to ponder on the problem of epochs and all.

# In[ ]:


import tensorflow as tf
from keras.callbacks import EarlyStopping

with tf.device('/device:GPU:0'):
    early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1, mode='auto')
    model.fit(xtrain, xtrain, epochs=40, batch_size=2048, validation_data=(xtest, xtest), callbacks=[early_stopping])


# ## It's good to see that model is doing well

# In[ ]:


pred= model.predict(xtest[:5])
def plot_predictions(y_true, y_pred):    
    f, ax = plt.subplots(2, 5)
    for i in range(5):
        ax[0][i].imshow(np.reshape(y_true[i], (28, 28)), aspect='auto')
        ax[1][i].imshow(np.reshape(y_pred[i], (28, 28)), aspect='auto')
    plt.tight_layout()
    
plot_predictions(xtest[:5], pred[:5])


# Some references I followed:-
# 
# https://www.analyticsvidhya.com/blog/2018/06/unsupervised-deep-learning-computer-vision/
# https://towardsdatascience.com/applied-deep-learning-part-3-autoencoders-1c083af4d798
# https://blog.keras.io/building-autoencoders-in-keras.html
# https://cs.stanford.edu/people/karpathy/convnetjs/demo/autoencoder.html
# https://machinelearningmastery.com/develop-encoder-decoder-model-sequence-sequence-prediction-keras/
