#!/usr/bin/env python
# coding: utf-8

# This is my first public kernel and I would really appreciate your feedback.
# 
# The dataset contains 6000 images of banknote each of shape ( 1280, 720, 3 ). Each banknote category is divided into folders. Our task is to build a model which recognize the banknote.

# Import data, preprocess the images and manage their label

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import cv2

import os

from PIL import Image

X = []

labels = []

for dirname, _, filenames in os.walk('/kaggle/input'):
    
    for filename in filenames:
        
        if( len( str( os.path.join( dirname, filename ) ).split( '/' ) ) > 5 ) :
            
            image = cv2.imread( os.path.join( dirname,filename ) )
            
            img_array = Image.fromarray( image, 'RGB' )
            
            resized_img = img_array.resize( ( 64, 64 ) )
            
            X.append( np.array( resized_img ) ) 
            
            label = str( os.path.join( dirname,filename ) ).split( '/' )[-2]
            
            if( label == '5' ) :
                
                labels.append( 0 )
                
            elif( label == '10' ) :
                
                labels.append( 1 )
             
            elif( label == '20' ) :
                
                labels.append( 2 )
                
            elif( label == '50' ) :
                
                labels.append( 3 )
                
            elif( label == '100' ) :
                
                labels.append( 4 )
                
            else :
                
                labels.append( 5 )
            
# Any results you write to the current directory are saved as output.


# In[ ]:


print( 'Number of images : %d' % len( X ) )

print( 'Associated labels : %d' % len( labels ) )


# In[ ]:


X = np.array( X )

print( 'Shape of X : ', X.shape )


# In[ ]:


Y = np.array( labels )

Y = np.reshape( Y, ( 6000, 1 ) )

print( 'Shape of Y : ', Y.shape )


# split dataset into train and test set

# In[ ]:


from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split( X, Y, random_state = 10, test_size = 0.2 )


# In[ ]:


print( X_train.shape )

print( Y_train.shape )


# Change Y_train into categorical

# In[ ]:


from keras.utils import to_categorical


# In[ ]:


Y_train = np.reshape( Y_train, ( 4800, 1 ) )

Y_train = to_categorical( Y_train, 6 )

Y_train.shape


# create model

# In[ ]:


from keras import Sequential

from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Activation, ZeroPadding2D, AveragePooling2D

from keras.layers.advanced_activations import LeakyReLU

from keras.layers.normalization import BatchNormalization


# In[ ]:


from keras import backend as K

K.clear_session()

model = Sequential()

model.add( ZeroPadding2D( input_shape = ( 64, 64, 3 ), padding = ( 3, 3 ) ) )

model.add ( Conv2D( 32, ( 7, 7 ), strides = (  1, 1 ) ) )

model.add( BatchNormalization( axis = 3 ) )
 
model.add( Activation( 'relu' ) )

model.add( MaxPooling2D( ( 2, 2 ) ) )

model.add( Flatten() )

model.add( Dense( 6 ) )

model.add( Activation( 'softmax' ) )

model.summary()


# In[ ]:


model.compile( loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'] )


# model training

# In[ ]:


model.fit( X_train, Y_train, batch_size = 64, epochs = 20 )


# prediction on test set

# In[ ]:


Y_predict = model.predict_classes( X_test )


# accuracy on test set

# In[ ]:


from sklearn.metrics import accuracy_score


# In[ ]:


accuracy_score( Y_test, Y_predict )


# In[ ]:


from sklearn.metrics import classification_report

print( classification_report( Y_test, Y_predict ) )

