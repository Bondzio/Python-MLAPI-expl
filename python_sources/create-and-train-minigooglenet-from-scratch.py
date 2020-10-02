#!/usr/bin/env python
# coding: utf-8

# Based on the good response of my first notebook on creating and training a ResNet50 from scratch, I am continuing this series with creating MiniGoogLeNet from scratch using Tensorflow. You can find my original kernel on building ResNet50 from scratch here:
# https://www.kaggle.com/sandy1112/create-and-train-resnet50-from-scratch
# 
# If you are liking this series of building popular architectures from scratch, please upvote. That would motivate me to add more architectures in upcoming versions
# 
# This kernel just uses top 100 classes. For actual competition we would need to model all classes with neccessary methods to handle class imbalance

# **The MiniGoogLeNet architecture is based on the paper - 'Understanding deep learning requires rethinking generalization' by Chiyuan Zhang, Samy Bengio, Moritz Hardt, Benjamin Recht, Oriol Vinyals, published in 2016**
# 
# The link for the original paper can be found here:
# 
# https://arxiv.org/abs/1611.03530
# 
# The snapshot of the architecture is given below:

# In[ ]:


from IPython.display import Image
Image("../input/minigooglenetarch/minigooglenet_architecture.png")


# **Importing the required libraries**

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
import tensorflow as tf
import cv2
import skimage.io
from skimage.transform import resize
from imgaug import augmenters as iaa
from sklearn import preprocessing
from sklearn.preprocessing import LabelBinarizer,LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras import layers
from tensorflow.keras.layers import Input, Add, Dense, Dropout, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D,GlobalAveragePooling2D,Concatenate,concatenate, ReLU, LeakyReLU,Reshape, Lambda
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, load_model, Model
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import metrics
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.initializers import glorot_uniform
from tqdm import tqdm
import imgaug as ia
from imgaug import augmenters as iaa
from PIL import Image
import keras.backend as K
K.set_image_data_format('channels_last')
K.set_learning_phase(1)


# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# **Path retrieval**
# 
# 
# Taken from the public kernel...thanks for sharing this. It was quite helpful for me. Please upvote that kernel if you also found that helpful
# https://www.kaggle.com/derinformatiker/landmark-retrieval-all-paths

# In[ ]:


train = pd.read_csv("../input/landmark-retrieval-2020/train.csv")
def get_paths(sub):
    index = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

    paths = []

    for a in index:
        for b in index:
            for c in index:
                try:
                    paths.extend([f"../input/landmark-retrieval-2020/{sub}/{a}/{b}/{c}/" + x for x in os.listdir(f"../input/landmark-retrieval-2020/{sub}/{a}/{b}/{c}")])
                except:
                    pass

    return paths


# In[ ]:


train_path = train

rows = []
for i in tqdm(range(len(train))):
    row = train.iloc[i]
    path  = list(row["id"])[:3]
    temp = row["id"]
    row["id"] = f"../input/landmark-retrieval-2020/train/{path[0]}/{path[1]}/{path[2]}/{temp}.jpg"
    rows.append(row["id"])
    
rows = pd.DataFrame(rows)
train_path["id"] = rows


# **Setting up some basic model specs**

# In[ ]:


batch_size = 128
seed = 42
shape = (64, 64, 3) ##desired shape of the image for resizing purposes
val_sample = 0.1 # 10 % as validation sample


# In[ ]:


train_labels = pd.read_csv('../input/landmark-retrieval-2020/train.csv')
train_labels.head()


# In[ ]:


k =train[['id','landmark_id']].groupby(['landmark_id']).agg({'id':'count'})
k.rename(columns={'id':'Count_class'}, inplace=True)
k.reset_index(level=(0), inplace=True)
freq_ct_df = pd.DataFrame(k)
freq_ct_df.head()


# In[ ]:


train_labels = pd.merge(train,freq_ct_df, on = ['landmark_id'], how='left')
train_labels.head()


# In[ ]:


freq_ct_df.sort_values(by=['Count_class'],ascending=False,inplace=True)
freq_ct_df.head()


# **Due to Kernel runtime limits, for illustrating the example let's run this for top 100 landmark categories**

# In[ ]:


freq_ct_df_top100 = freq_ct_df.iloc[:100]
top100_class = freq_ct_df_top100['landmark_id'].tolist()


# In[ ]:


top100class_train = train_path[train_path['landmark_id'].isin (top100_class) ]
top100class_train.shape


# **Setting up some helper functions**

# In[ ]:


def getTrainParams():
    data = top100class_train.copy()
    le = preprocessing.LabelEncoder()
    data['label'] = le.fit_transform(data['landmark_id'])
    lbls = top100class_train['landmark_id'].tolist()
    lb = LabelBinarizer()
    labels = lb.fit_transform(lbls)
    
    return np.array(top100class_train['id'].tolist()),np.array(labels),le


# Credit to Michal Haltuf from whose kernel I had first learnt Data Generators two years back.
# You can check out his kernel here: https://www.kaggle.com/rejpalcz/cnn-128x128x4-keras-from-scratch-lb-0-328

# In[ ]:


class Landmark2020_DataGenerator(tf.keras.utils.Sequence):
    def __init__(self, paths, labels, batch_size, shape, shuffle = False, use_cache = False, augment = False):
        self.paths, self.labels = paths, labels
        self.batch_size = batch_size
        self.shape = shape
        self.shuffle = shuffle
        self.use_cache = use_cache
        self.augment = augment
        if use_cache == True:
            self.cache = np.zeros((paths.shape[0], shape[0], shape[1], shape[2]), dtype=np.float16)
            self.is_cached = np.zeros((paths.shape[0]))
        self.on_epoch_end()
    
    def __len__(self):
        return int(np.ceil(len(self.paths) / float(self.batch_size)))
    
    def __getitem__(self, idx):
        indexes = self.indexes[idx * self.batch_size : (idx+1) * self.batch_size]

        paths = self.paths[indexes]
        X = np.zeros((paths.shape[0], self.shape[0], self.shape[1], self.shape[2]))
        # Generate data
        if self.use_cache == True:
            X = self.cache[indexes]
            for i, path in enumerate(paths[np.where(self.is_cached[indexes] == 0)]):
                image = self.__load_image(path)
                self.is_cached[indexes[i]] = 1
                self.cache[indexes[i]] = image
                X[i] = image
        else:
            for i, path in enumerate(paths):
                X[i] = self.__load_image(path)

        y = self.labels[indexes]
                
        if self.augment == True:
            seq = iaa.Sequential([
                iaa.OneOf([
                    iaa.Fliplr(0.5), # horizontal flips
                    
                    iaa.ContrastNormalization((0.75, 1.5)),
                    iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
                    iaa.Multiply((0.8, 1.2), per_channel=0.2),
                    
                    iaa.Affine(rotate=0),
                    #iaa.Affine(rotate=90),
                    #iaa.Affine(rotate=180),
                    #iaa.Affine(rotate=270),
                    iaa.Fliplr(0.5),
                    #iaa.Flipud(0.5),
                ])], random_order=True)

            X = np.concatenate((X, seq.augment_images(X), seq.augment_images(X), seq.augment_images(X)), 0)
            y = np.concatenate((y, y, y, y), 0)
        
        return X, y
    
    def on_epoch_end(self):
        
        # Updates indexes after each epoch
        self.indexes = np.arange(len(self.paths))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __iter__(self):
        """Create a generator that iterate over the Sequence."""
        for item in (self[i] for i in range(len(self))):
            yield item
            
    def __load_image(self, path):
        image_norm = skimage.io.imread(path)/255.0
        

        im = resize(image_norm, (shape[0], shape[1],shape[2]), mode='reflect')
        return im


# In[ ]:


nlabls = top100class_train['landmark_id'].nunique()


# **Let's build the building blocks of a MiniGoogLNet model one by one**
# 
# Credit: Dr. Adrain Rosebrock for his course on Computer Vision. It helped me a lot in clearing my concepts. You may check out his course on:
# https://www.pyimagesearch.com/
# 
# 

# The entire MiniGoogLeNet architecture is built on three main modules:
# 
# 1. Conv Module - this module is responsible for applying a convolution, followed by Batch Normalization and finally with an activation.
# 2. Inception Module - this is more like a mini-inception module which consists of two branches. The first branch is a conv module  that learns 1X1 filters. The second brandch is also a Conv Module that learns 3X3 filters.
# 3. Downsample Module - this module is responsible for reducing the spatial dimensions of an input volume. The first branch of this module learns a set of K, 3X3 filters using stride of 2X2. On top of this Max pooling is applied with window size of 3X3 and stride of 2X2. Finally outputs of Conv 3X3 and Pool are concated.
# 
# The architecture can now be compiled as follows:
# 
# 
# Input --> Conv Module --> Inception Module --> Inception Module --> Downsample Module -->Inception Module-->Inception Module-->Inception Module-->Inception Module-->Downsample Module-->Inception Module-->Inception Module-->Average pooling-->Dropout-->Flatten-->Dense-->Activation

# In[ ]:


def conv_module(x,K,kX,kY, stride, chanDim, padding="same"):
        x = Conv2D(K, (kX, kY), strides=stride, padding=padding)(x)
        x = BatchNormalization(axis=chanDim)(x)
        x = Activation("relu")(x)
        return x

def inception_module(x, numK1x1, numK3x3, chanDim):
    conv_1x1 = conv_module(x, numK1x1, 1, 1,(1, 1), chanDim)
    conv_3x3 = conv_module(x, numK3x3, 3, 3,(1, 1), chanDim)
    x = concatenate([conv_1x1, conv_3x3], axis=chanDim)
    return x

def downsample_module(x, K, chanDim):
    conv_3x3 = conv_module(x, K, 3, 3, (2, 2),-1, padding="valid")
    pool = MaxPooling2D((3, 3), strides=(2, 2))(x)
    x = concatenate([conv_3x3, pool], axis=chanDim)
    return x


# In[ ]:


def build(width, height, depth, classes):
    inputShape = (height, width, depth)
    chanDim = -1
    
    inputs = Input(shape=inputShape)
    x = conv_module(inputs, 96, 3, 3, (1, 1),chanDim)
    x = inception_module(x, 32, 32, chanDim)
    x = inception_module(x, 32, 48, chanDim)
    x = downsample_module(x, 80, chanDim)
    x = inception_module(x, 112, 48, chanDim)
    x = inception_module(x, 96, 64, chanDim)
    x = inception_module(x, 80, 80, chanDim)
    x = inception_module(x, 48, 96, chanDim)
    x = downsample_module(x, 96, chanDim)
    x = inception_module(x, 176, 160, chanDim)
    x = inception_module(x, 176, 160, chanDim)
    x = AveragePooling2D((7, 7))(x)
    x = Dropout(0.5)(x)
    x = Flatten()(x)
    x = Dense(classes)(x)
    x = Activation("softmax")(x)
    model = Model(inputs, x, name="googlenet")
    return model


# In[ ]:


from tensorflow.keras.metrics import categorical_accuracy,top_k_categorical_accuracy
def top_5_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=5)


# In[ ]:


model = build(shape[0],shape[1],shape[2], nlabls)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc',top_5_accuracy])
model.summary()


# In[ ]:


paths, labels,_ = getTrainParams()


# In[ ]:


keys = np.arange(paths.shape[0], dtype=np.int)  
np.random.seed(seed)
np.random.shuffle(keys)
lastTrainIndex = int((1-val_sample) * paths.shape[0])

pathsTrain = paths[0:lastTrainIndex]
labelsTrain = labels[0:lastTrainIndex]

pathsVal = paths[lastTrainIndex:]
labelsVal = labels[lastTrainIndex:]

print(paths.shape, labels.shape)
print(pathsTrain.shape, labelsTrain.shape, pathsVal.shape, labelsVal.shape)


# In[ ]:


train_generator = Landmark2020_DataGenerator(pathsTrain, labelsTrain, batch_size, shape, use_cache=False, augment = True, shuffle = True)
val_generator = Landmark2020_DataGenerator(pathsVal, labelsVal, batch_size, shape, use_cache=False, shuffle = False)


# Since the idea of this kernel was to illustrate the architecture in depth and how to create it from scratch, we will run this for only one epoch. In real world, one will need to train this over a large number of epochs to get good results.

# In[ ]:


epochs = 1
use_multiprocessing = True 
workers = 1 


# In[ ]:


base_cnn = model.fit_generator(
    train_generator,
    steps_per_epoch=len(train_generator),
    validation_data=val_generator,
    validation_steps=64,
    #class_weight = class_weights,
    epochs=epochs,
    #callbacks = [clr],
    use_multiprocessing=use_multiprocessing,
    #workers=workers,
    verbose=1)


# In[ ]:


model.save('MiniGoogLeNet.h5')


# **If you found this useful, an upvote would be much appreciated.**
