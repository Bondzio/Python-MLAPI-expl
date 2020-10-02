#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import keras
keras.__version__
import tensorflow as tf
tf.__version__


# In[ ]:


# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

# data visualisation and manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
 
#configure
# sets matplotlib to inline and displays graphs below the corressponding cell.
get_ipython().run_line_magic('matplotlib', 'inline')
style.use('fivethirtyeight')
sns.set(style='whitegrid',color_codes=True)

#model selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix,roc_curve,roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder

#preprocess.
from keras.preprocessing.image import ImageDataGenerator

#dl libraraies
from keras import backend as K
from keras import regularizers
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
from keras.optimizers import Adam,SGD,Adagrad,Adadelta,RMSprop
from keras.utils import to_categorical
from keras.callbacks import ReduceLROnPlateau

# specifically for cnn
from keras.layers import Dropout, Flatten,Activation
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.layers import InputLayer
 
import tensorflow as tf
import random as rn

# specifically for manipulating zipped images and getting numpy arrays of pixel values of images.
import cv2                  
import numpy as np  
from tqdm import tqdm
import os                   
from random import shuffle  
from zipfile import ZipFile
from PIL import Image

from keras.applications.resnet50 import ResNet50


# In[ ]:


os.listdir('../input/test-dataset/Fire-Detection')


# In[ ]:


def assign_label(img,label):
    return label


# In[ ]:


def make_train_data(label,DIR):
    for img in tqdm(os.listdir(DIR)):
        path = os.path.join(DIR,img)
        img = cv2.imread(path,cv2.IMREAD_COLOR)
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
        
        X.append(np.array(img))
        Z.append(str(label))


# In[ ]:


X=[]
Z=[]
IMG_SIZE=150
NOTFIRE='../input/test-dataset/Fire-Detection/0'
FIRE='../input/test-dataset/Fire-Detection/1'

make_train_data('NOTFIRE',NOTFIRE)
make_train_data('FIRE',FIRE)


# In[ ]:


fig,ax=plt.subplots(2,5)
plt.subplots_adjust(bottom=0.3, top=0.7, hspace=0)
fig.set_size_inches(10,10)

for i in range(2):
    for j in range (5):
        l=rn.randint(0,len(Z))
        ax[i,j].imshow(X[l][:,:,::-1])
        ax[i,j].set_title(Z[l])
        ax[i,j].set_aspect('equal')


# In[ ]:


le=LabelEncoder()
Y=le.fit_transform(Z)
Y=to_categorical(Y,2)
print(Y)
X=np.array(X)
#X=X/255

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25,random_state=1337)

np.random.seed(42)
rn.seed(42)
#tf.set_random_seed(42)


# In[ ]:


base_model=ResNet50(include_top=False, weights='imagenet',input_shape=(150,150,3), pooling='max')
base_model.summary()


# In[ ]:


model=Sequential()
model.add(base_model)
model.add(Dropout(0.20))
model.add(Dense(2048,activation='relu'))
model.add(Dense(1024,activation='relu'))
model.add(Dense(512,activation='relu'))
model.add(Dense(2,activation='softmax'))


# In[ ]:


epochs=100
batch_size=128
red_lr=ReduceLROnPlateau(monitor='val_acc', factor=0.1, min_delta=0.0001, patience=2, verbose=1)
base_model.trainable=True # setting the VGG model to be trainable.
model.compile(optimizer=Adam(lr=1e-5),loss='categorical_crossentropy',metrics=['accuracy'])
model.summary()


# In[ ]:


History = model.fit(x_train, y_train, epochs=epochs, validation_data=(x_test,y_test))


# In[ ]:


model.save('../working/model.h5')


# In[ ]:


plt.plot(History.history['accuracy'])
plt.plot(History.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend(['train', 'test'])
plt.show()


# In[ ]:


plt.plot(History.history['loss'])
plt.plot(History.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend(['train', 'test'])
plt.show()


# In[ ]:


path="../input/test-dataset/Fire-Detection/1/"
files=os.listdir(path)
for i in files:
    X=cv2.imread(path+i)
    X=cv2.resize(X,(150,150))
#     plt.figure()
#     plt.imshow(X[:,:,::-1]) 
#     plt.show()  # display it


    X = np.array(X)
   # X = X/255
    X = np.expand_dims(X, axis=0)

    print(np.round(model.predict(X)))


# In[ ]:


path="../input/test-dataset/Fire-Detection/0/"
files=os.listdir(path)
for i in files:
    X=cv2.imread(path+i)
    X=cv2.resize(X,(150,150))
#     plt.figure()
#     plt.imshow(X[:,:,::-1]) 
#     plt.show()  # display it


    X = np.array(X)
   # X = X/255

    X = np.expand_dims(X, axis=0)

    print(np.round(model.predict(X)))

