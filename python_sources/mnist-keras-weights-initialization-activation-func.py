#!/usr/bin/env python
# coding: utf-8

# ##### In this notebook we'll initialize our ANN model with different weights and activation functions and check how it's works.
#     1. Create a ANN model with default weights
#     2. Building a Model with He Initialization and LeakyRelu activation
#     3. Building a Model with Variance scaling Initialization and LeakyRelu activation
#     4. Building a Model with He Initialization and PReLU activation
#     5. Building a Model with He Initialization and eLU activation
#     6. Building a Model with lecun_normal initialization and seLU activation 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


# importing all the necessary libraries

import scipy
import warnings
import datetime

from scipy import misc
warnings.filterwarnings("ignore")


# In[ ]:


# import libraries

import keras
from keras import utils
from keras import models
from keras.layers.core import (Dense, Dropout, Activation, Flatten)
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras import optimizers

print("Keras version: {}".format(keras.__version__))


# In[ ]:


# loading the training data

train_df = pd.read_csv("../input/train.csv")


# In[ ]:


# loading the testing data

test = pd.read_csv("../input/test.csv")


# In[ ]:


train_df.head()


# In[ ]:


test.head()


# In[ ]:


# dividing the data into traing and target

train = train_df.drop('label', axis=1)
target = train_df['label']


# In[ ]:


train.head()


# In[ ]:


target.head()


# #### Some baisc EDA and stadardization of training and testing data

# In[ ]:


# importing seaborn and matplotlib

import seaborn as sns
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


sns.distplot(target)


# In[ ]:


sns.countplot(target)


# In[ ]:


# misc., properties

BATCH_SIZE = 64
NB_EPOCHS = 10
NB_CLASSES = 10
VERBOSE = 1
VALIDATION_SPLIT = 0.25
OPTIMIZER = optimizers.RMSprop()


# In[ ]:


# standardizing the data
import sklearn
from sklearn import preprocessing

scaler = preprocessing.StandardScaler()


# In[ ]:


# standardizing the training data

# train = scaler.fit_transform(train)
train /= 255


# In[ ]:


# standardizing the testing data

# test = scaler.fit_transform(test)
test /= 255


# In[ ]:


# reshaping the traning and testing data

train = train.values.reshape(-1, 28, 28, 1)
test = test.values.reshape(-1, 28, 28, 1)


# In[ ]:


# Label Encoding
from keras.utils import np_utils

target = np_utils.to_categorical(target, NB_CLASSES)


# In[ ]:


target[:5]


# In[ ]:


# sample example

plt.imshow(test[42][:, :, 0])


# ## Model Building using Keras Library

# In[ ]:


# splitting the data into train and test
from sklearn import model_selection

X_train, X_val, y_train, y_val = model_selection.train_test_split(train, target, test_size=0.25, random_state=42)


# In[ ]:


print("X training data shape: {}".format(X_train.shape))
print("Y training data shape: {}".format(y_train.shape))


# In[ ]:


print("X validation data shape: {}".format(X_val.shape))
print("Y validation data shape: {}".format(y_val.shape))


# ### 1. Building a Model with default weights

# In[ ]:


from keras.preprocessing import image
from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, BatchNormalization, Activation, Dropout, LeakyReLU
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras import optimizers

NB_OUTPUT_FUNC = "softmax"
DROPOUT_FIRST = 0.25
DROPOUT_SECOND = 0.20


# In[ ]:


model = Sequential()
model.add(Conv2D(32, (5, 5), padding='same', input_shape=(28, 28, 1)))
model.add(LeakyReLU(alpha=0.02))
model.add(Conv2D(32, (5, 5)))
model.add(LeakyReLU(alpha=0.02))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(DROPOUT_FIRST))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(LeakyReLU(alpha=0.02))
model.add(Conv2D(64, (3, 3)))
model.add(LeakyReLU(alpha=0.02))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(DROPOUT_FIRST))

model.add(Flatten())
model.add(Dense(128))
model.add(LeakyReLU(alpha=0.02))
model.add(Dropout(DROPOUT_SECOND))

model.add(Dense(128))
model.add(LeakyReLU(alpha=0.02))
model.add(Dropout(DROPOUT_SECOND))

model.add(Dense(NB_CLASSES))
model.add(Activation(NB_OUTPUT_FUNC))


# In[ ]:


model.summary()


# In[ ]:


# creating optimizer

# optimizer = optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
optimizer = optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-06, decay=0.0)


# In[ ]:


# compiling the model

model.compile(optimizer=optimizer, 
              loss='categorical_crossentropy', 
              metrics=['categorical_accuracy'])


# In[ ]:


# creating a generator to pull the data as batches in a lazy format - Data augumentation

generator = image.ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=10,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,
    vertical_flip=False,
    horizontal_flip=False)


# In[ ]:


num_train_sequences = len(X_train)
num_val_sequences = len(X_val)

print("# training sequences: {}".format(num_train_sequences))
print("# validation sequences: {}".format(num_val_sequences))


# In[ ]:


# calculating number of training and validation steps per epoch
# for training
if (num_train_sequences % BATCH_SIZE) == 0:
    steps_per_epoch = int(num_train_sequences / BATCH_SIZE)
else:
    steps_per_epoch = int(num_train_sequences / BATCH_SIZE) + 1
    
# for validation    
if (num_val_sequences % BATCH_SIZE) == 0:
    validation_steps = int(num_val_sequences / BATCH_SIZE)
else:
    validation_steps = int(num_val_sequences / BATCH_SIZE) + 1    
    
print("# number of steps required for training: {}".format(steps_per_epoch))
print("# number of steps required for validation: {}".format(validation_steps))


# In[ ]:


import datetime

current_dt_time = datetime.datetime.now()
model_name = 'model_init' + '_' + str(current_dt_time).replace(' ', '').replace(':', '_') + '/'

if not os.path.exists(model_name):
    os.mkdir(model_name)
    
file_path = model_name + "model-{epoch:05d}-{loss:.5f}-{categorical_accuracy:.5f}-{val_loss:.5f}-{val_categorical_accuracy:.5f}.h5"
checkpoint = ModelCheckpoint(filepath=file_path, monitor='val_categorical_accuracy', verbose=1, save_best_only=True,
                             save_weights_only=False, mode='auto', period=1)
LR = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=2, min_lr=0.000001, verbose=1, cooldown=1)
callbacks = [checkpoint, LR]


# In[ ]:


# fitting the model

history = model.fit_generator(generator.flow(X_train, y_train, batch_size=BATCH_SIZE), 
                             validation_data=generator.flow(X_val, y_val, batch_size=BATCH_SIZE),
                             epochs=NB_EPOCHS,
                             verbose=VERBOSE,
                             steps_per_epoch=steps_per_epoch,
                             validation_steps=validation_steps,
                             class_weight=None,
                             initial_epoch=0,
                             callbacks=callbacks)


# In[ ]:


# best accuracy found
# best model: saving model to model_init_2019-07-0108_08_42.188814/model-00009-0.21558-0.93310-0.12834-0.96155.h5

values = {}
models = os.listdir(model_name)

for model in models:
    converted = model.replace(".h5", "")
    accuracy = float(converted.split("-")[-1])
    values.update({accuracy: model})
    
key = max(values, key = values.get)
best = values.get(key)

print("Best model found: {}".format(best))


# In[ ]:


# all data in history

history.history.keys()


# In[ ]:


plt.plot(history.history['categorical_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# In[ ]:


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# In[ ]:


### all available initialization

[name for name in dir(keras.initializers) if not name.startswith("_")]


# ### 2. Building a Model with He Initialization and LeakyRelu activation

# In[ ]:


he_model = Sequential()
he_model.add(Conv2D(32, (5, 5), padding='same', input_shape=(28, 28, 1), kernel_initializer='he_normal'))
he_model.add(LeakyReLU(alpha=0.02))
he_model.add(Conv2D(32, (5, 5), kernel_initializer='he_normal'))
he_model.add(LeakyReLU(alpha=0.02))
he_model.add(MaxPooling2D(pool_size=(2, 2)))
he_model.add(Dropout(DROPOUT_FIRST))

he_model.add(Conv2D(64, (3, 3), padding='same', kernel_initializer='he_normal'))
he_model.add(LeakyReLU(alpha=0.02))
he_model.add(Conv2D(64, (3, 3), kernel_initializer='he_normal'))
he_model.add(LeakyReLU(alpha=0.02))
he_model.add(MaxPooling2D(pool_size=(2, 2)))
he_model.add(Dropout(DROPOUT_FIRST))

he_model.add(Flatten())
he_model.add(Dense(128, kernel_initializer='he_normal'))
he_model.add(LeakyReLU(alpha=0.02))
he_model.add(Dropout(DROPOUT_SECOND))

he_model.add(Dense(128, kernel_initializer='he_normal'))
he_model.add(LeakyReLU(alpha=0.02))
he_model.add(Dropout(DROPOUT_SECOND))

he_model.add(Dense(NB_CLASSES))
he_model.add(Activation(NB_OUTPUT_FUNC))


# In[ ]:


he_model.summary()


# In[ ]:


# compiling the model

he_model.compile(optimizer=optimizer, 
              loss='categorical_crossentropy', 
              metrics=['categorical_accuracy'])


# In[ ]:


# fitting the model

history = he_model.fit_generator(generator.flow(X_train, y_train, batch_size=BATCH_SIZE), 
                             validation_data=generator.flow(X_val, y_val, batch_size=BATCH_SIZE),
                             epochs=NB_EPOCHS,
                             verbose=VERBOSE,
                             steps_per_epoch=steps_per_epoch,
                             validation_steps=validation_steps,
                             class_weight=None,
                             initial_epoch=0,
                             callbacks=callbacks)


# In[ ]:


plt.plot(history.history['categorical_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# In[ ]:


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# ### 3. Building a Model with Variance scaling Initialization and LeakyRelu activation

# In[ ]:


initializer = keras.initializers.VarianceScaling(scale=2.0, mode="fan_avg", distribution="uniform")
keras.layers.Dense(10, activation="relu", kernel_initializer=initializer)


# In[ ]:


vs_model = Sequential()
vs_model.add(Conv2D(32, (5, 5), padding='same', input_shape=(28, 28, 1), kernel_initializer=initializer))
vs_model.add(LeakyReLU(alpha=0.02))
vs_model.add(Conv2D(32, (5, 5), kernel_initializer=initializer))
vs_model.add(LeakyReLU(alpha=0.02))
vs_model.add(MaxPooling2D(pool_size=(2, 2)))
vs_model.add(Dropout(DROPOUT_FIRST))

vs_model.add(Conv2D(64, (3, 3), padding='same', kernel_initializer=initializer))
vs_model.add(LeakyReLU(alpha=0.02))
vs_model.add(Conv2D(64, (3, 3), kernel_initializer=initializer))
vs_model.add(LeakyReLU(alpha=0.02))
vs_model.add(MaxPooling2D(pool_size=(2, 2)))
vs_model.add(Dropout(DROPOUT_FIRST))

vs_model.add(Flatten())
vs_model.add(Dense(128, kernel_initializer=initializer))
vs_model.add(LeakyReLU(alpha=0.02))
vs_model.add(Dropout(DROPOUT_SECOND))

vs_model.add(Dense(128, kernel_initializer=initializer))
vs_model.add(LeakyReLU(alpha=0.02))
vs_model.add(Dropout(DROPOUT_SECOND))

vs_model.add(Dense(NB_CLASSES))
vs_model.add(Activation(NB_OUTPUT_FUNC))


# In[ ]:


vs_model.summary()


# In[ ]:


# compiling the model

vs_model.compile(optimizer=optimizer, 
              loss='categorical_crossentropy', 
              metrics=['categorical_accuracy'])


# In[ ]:


# fitting the model

history = vs_model.fit_generator(generator.flow(X_train, y_train, batch_size=BATCH_SIZE), 
                             validation_data=generator.flow(X_val, y_val, batch_size=BATCH_SIZE),
                             epochs=NB_EPOCHS,
                             verbose=VERBOSE,
                             steps_per_epoch=steps_per_epoch,
                             validation_steps=validation_steps,
                             class_weight=None,
                             initial_epoch=0,
                             callbacks=callbacks)


# In[ ]:


plt.plot(history.history['categorical_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# In[ ]:


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# ### 4. Building a Model with He Initialization and PReLU activation

# In[ ]:


pre_he_model = Sequential()
pre_he_model.add(Conv2D(32, (5, 5), padding='same', input_shape=(28, 28, 1), kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(Conv2D(32, (5, 5), kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(MaxPooling2D(pool_size=(2, 2)))
pre_he_model.add(Dropout(DROPOUT_FIRST))

pre_he_model.add(Conv2D(64, (3, 3), padding='same', kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(Conv2D(64, (3, 3), kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(MaxPooling2D(pool_size=(2, 2)))
pre_he_model.add(Dropout(DROPOUT_FIRST))

pre_he_model.add(Flatten())
pre_he_model.add(Dense(128, kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(Dropout(DROPOUT_SECOND))

pre_he_model.add(Dense(128, kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(Dropout(DROPOUT_SECOND))

pre_he_model.add(Dense(NB_CLASSES))
pre_he_model.add(Activation(NB_OUTPUT_FUNC))


# In[ ]:


pre_he_model.summary()


# In[ ]:


# compiling the model

pre_he_model.compile(optimizer=optimizer, 
              loss='categorical_crossentropy', 
              metrics=['categorical_accuracy'])


# In[ ]:


# fitting the model

history = pre_he_model.fit_generator(generator.flow(X_train, y_train, batch_size=BATCH_SIZE), 
                             validation_data=generator.flow(X_val, y_val, batch_size=BATCH_SIZE),
                             epochs=NB_EPOCHS,
                             verbose=VERBOSE,
                             steps_per_epoch=steps_per_epoch,
                             validation_steps=validation_steps,
                             class_weight=None,
                             initial_epoch=0,
                             callbacks=callbacks)


# In[ ]:


plt.plot(history.history['categorical_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# In[ ]:


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# ### 5. Building a Model with He Initialization and eLU activation

# In[ ]:


elu_model = Sequential()
elu_model.add(Conv2D(32, (5, 5), padding='same', input_shape=(28, 28, 1), kernel_initializer='he_normal'))
elu_model.add(Activation("elu"))
elu_model.add(Conv2D(32, (5, 5), kernel_initializer='he_normal'))
elu_model.add(Activation("elu"))
elu_model.add(MaxPooling2D(pool_size=(2, 2)))
elu_model.add(Dropout(DROPOUT_FIRST))

elu_model.add(Conv2D(64, (3, 3), padding='same', kernel_initializer='he_normal'))
elu_model.add(Activation("elu"))
elu_model.add(Conv2D(64, (3, 3), kernel_initializer='he_normal'))
elu_model.add(Activation("elu"))
elu_model.add(MaxPooling2D(pool_size=(2, 2)))
elu_model.add(Dropout(DROPOUT_FIRST))

elu_model.add(Flatten())
elu_model.add(Dense(128, kernel_initializer='he_normal'))
elu_model.add(Activation("elu"))
elu_model.add(Dropout(DROPOUT_SECOND))

elu_model.add(Dense(128, kernel_initializer='he_normal'))
elu_model.add(Activation("elu"))
elu_model.add(Dropout(DROPOUT_SECOND))

elu_model.add(Dense(NB_CLASSES))
elu_model.add(Activation(NB_OUTPUT_FUNC))


# In[ ]:


elu_model.summary()


# In[ ]:


# compiling the model

elu_model.compile(optimizer=optimizer, 
              loss='categorical_crossentropy', 
              metrics=['categorical_accuracy'])


# In[ ]:


# fitting the model

history = elu_model.fit_generator(generator.flow(X_train, y_train, batch_size=BATCH_SIZE), 
                             validation_data=generator.flow(X_val, y_val, batch_size=BATCH_SIZE),
                             epochs=NB_EPOCHS,
                             verbose=VERBOSE,
                             steps_per_epoch=steps_per_epoch,
                             validation_steps=validation_steps,
                             class_weight=None,
                             initial_epoch=0,
                             callbacks=callbacks)


# In[ ]:


plt.plot(history.history['categorical_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# In[ ]:


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# ### 6. Building a Model with lecun_normal initialization and seLU activation 

# In[ ]:


selu_model = Sequential()
selu_model.add(Conv2D(32, (5, 5), padding='same', input_shape=(28, 28, 1), kernel_initializer='lecun_normal'))
selu_model.add(Activation("selu"))
selu_model.add(Conv2D(32, (5, 5), kernel_initializer='lecun_normal'))
selu_model.add(Activation("selu"))
selu_model.add(MaxPooling2D(pool_size=(2, 2)))
selu_model.add(Dropout(DROPOUT_FIRST))

selu_model.add(Conv2D(64, (3, 3), padding='same', kernel_initializer='lecun_normal'))
selu_model.add(Activation("selu"))
selu_model.add(Conv2D(64, (3, 3), kernel_initializer='lecun_normal'))
selu_model.add(Activation("selu"))
selu_model.add(MaxPooling2D(pool_size=(2, 2)))
selu_model.add(Dropout(DROPOUT_FIRST))

selu_model.add(Flatten())
selu_model.add(Dense(128, kernel_initializer='lecun_normal'))
selu_model.add(Activation("selu"))
selu_model.add(Dropout(DROPOUT_SECOND))

selu_model.add(Dense(128, kernel_initializer='lecun_normal'))
selu_model.add(Activation("selu"))
selu_model.add(Dropout(DROPOUT_SECOND))

selu_model.add(Dense(NB_CLASSES))
selu_model.add(Activation(NB_OUTPUT_FUNC))


# In[ ]:


selu_model.summary()


# In[ ]:


# compiling the model

selu_model.compile(optimizer=optimizer, 
              loss='categorical_crossentropy', 
              metrics=['categorical_accuracy'])


# In[ ]:


# fitting the model

history = selu_model.fit_generator(generator.flow(X_train, y_train, batch_size=BATCH_SIZE), 
                             validation_data=generator.flow(X_val, y_val, batch_size=BATCH_SIZE),
                             epochs=NB_EPOCHS,
                             verbose=VERBOSE,
                             steps_per_epoch=steps_per_epoch,
                             validation_steps=validation_steps,
                             class_weight=None,
                             initial_epoch=0,
                             callbacks=callbacks)


# In[ ]:


plt.plot(history.history['categorical_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# In[ ]:


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# ### Exponential Decay function

# In[ ]:


def exponential_decay_fn(epoch):
    return 0.01 * 0.1**(epoch / 20)


# In[ ]:


def exponential_decay(lr, s):
    def exponential_decay_fn(epoch):
        return lr * 0.1**(epoch / s)
    return exponential_decay_fn

exponential_decay_fn = exponential_decay(lr=0.001, s=20)


# In[ ]:


pre_he_model = Sequential()
pre_he_model.add(Conv2D(32, (5, 5), padding='same', input_shape=(28, 28, 1), kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(Conv2D(32, (5, 5), kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(MaxPooling2D(pool_size=(2, 2)))
pre_he_model.add(Dropout(DROPOUT_FIRST))

pre_he_model.add(Conv2D(64, (3, 3), padding='same', kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(Conv2D(64, (3, 3), kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(MaxPooling2D(pool_size=(2, 2)))
pre_he_model.add(Dropout(DROPOUT_FIRST))

pre_he_model.add(Flatten())
pre_he_model.add(Dense(128, kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(Dropout(DROPOUT_SECOND))

pre_he_model.add(Dense(128, kernel_initializer='he_normal'))
pre_he_model.add(keras.layers.PReLU())
pre_he_model.add(Dropout(DROPOUT_SECOND))

pre_he_model.add(Dense(NB_CLASSES))
pre_he_model.add(Activation(NB_OUTPUT_FUNC))


# In[ ]:


NB_EPOCHS=25


# In[ ]:


# compiling the model

pre_he_model.compile(optimizer=optimizer, 
              loss='categorical_crossentropy', 
              metrics=['categorical_accuracy'])


# In[ ]:


lr_scheduler = keras.callbacks.LearningRateScheduler(exponential_decay_fn)


# In[ ]:


callbacks = [checkpoint, LR, lr_scheduler]


# In[ ]:


# fitting the model

history = pre_he_model.fit_generator(generator.flow(X_train, y_train, batch_size=BATCH_SIZE), 
                             validation_data=generator.flow(X_val, y_val, batch_size=BATCH_SIZE),
                             epochs=NB_EPOCHS,
                             verbose=VERBOSE,
                             steps_per_epoch=steps_per_epoch,
                             validation_steps=validation_steps,
                             class_weight=None,
                             initial_epoch=0,
                             callbacks=callbacks)


# In[ ]:


# best accuracy found
# best model: saving model to model_init_2019-07-0108_08_42.188814/model-00009-0.21558-0.93310-0.12834-0.96155.h5

values = {}
models = os.listdir(model_name)

for model in models:
    converted = model.replace(".h5", "")
    accuracy = float(converted.split("-")[-1])
    values.update({accuracy: model})
    
key = max(values, key = values.get)
best = values.get(key)

print("Best model found: {}".format(best))


# In[ ]:


# all data in history

history.history.keys()


# In[ ]:


plt.plot(history.history['categorical_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# In[ ]:


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# In[ ]:


# summarize history for lr
plt.plot(history.history['lr'])
plt.title('Learning Rate')
plt.ylabel('lr')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# In[ ]:


# loading the best model
from keras.models import load_model

best_model_path = model_name + best
print("Full path found: {}".format(best_model_path))

best_model = load_model(best_model_path)


# In[ ]:


best_model.summary()


# In[ ]:


results = best_model.predict(test)


# In[ ]:


results[:5]


# In[ ]:


convert = np.argmax(results, axis=1)


# In[ ]:


results = pd.Series(convert, name='Label')


# In[ ]:


submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"), results],axis = 1)


# In[ ]:


submission.to_csv("submissions-10epochs.csv", index=False)


# In[ ]:


get_ipython().system('ls -lrt')


# In[ ]:




