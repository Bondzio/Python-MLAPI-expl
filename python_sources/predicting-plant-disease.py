#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import cupy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


# Downloading Necessary libraries
get_ipython().system('pip install tensor-dash')


# In[ ]:


# Importing Necessary Libraries
import tensorflow as tf
import tensorflow.keras as keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensordash.tensordash import Tensordash
from kaggle_secrets import UserSecretsClient
import plotly.express as px
from tqdm import tqdm
import json
import skimage.io as io
user_secrets = UserSecretsClient()
secret_value_0 = user_secrets.get_secret("email")
secret_value_1 = user_secrets.get_secret("pin")


# In[ ]:


# Reading the Training Data
dataset = pd.read_csv('/kaggle/input/plant-pathology-2020-fgvc7/train.csv')


# In[ ]:


dataset


# # Data Exploration and Visualisation

# ## Data Exploration

# In[ ]:


# Checking if there are any null values in the dataset
dataset.isnull().any()


# In[ ]:


# Checking the column data type
dataset.dtypes


# In[ ]:


# Adding .jpg extension to every image_id
dataset['image_id'] = dataset['image_id']+'.jpg'


# In[ ]:


dataset


# ## Data Visualisation

# ## Classes Distribution

# In[ ]:


dataset.healthy.hist()
plt.title('Healthy Classes')


# In[ ]:


dataset.multiple_diseases.hist()
plt.title('Multiple Diseases Classes')


# In[ ]:


dataset.rust.hist()
plt.title('Rust Classes')


# In[ ]:


dataset.scab.hist()
plt.title('Scab Classes')


# ## Class Image Visualisation

# In[ ]:


w=10
h=10
fig=plt.figure(figsize=(20, 14))
columns = 4
rows = 4
plt.title('Image Class')
plt.axis('off')
for i in range(1, columns*rows +1):
    img = plt.imread(f'/kaggle/input/plant-pathology-2020-fgvc7/images/Train_{i}.jpg')
    fig.add_subplot(rows, columns, i)
    
    if dataset.healthy[i] == 1:
        plt.title('Healthy')
    elif dataset.multiple_diseases[i] == 1:
        plt.title('Multiple Disease')
    elif dataset.rust[i] == 1:
        plt.title('Rust')
    else:
        plt.title('Scab')
    plt.imshow(img)
    plt.axis('off')
plt.show()


# # Image Segmentation

# Multiple Histogram for different pixles intensity values

# In[ ]:


w=10
h=10
fig=plt.figure(figsize=(20, 14))
columns = 4
rows = 4
plt.axis('off')
for i in range(1, columns*rows +1):
    img = plt.imread(f'/kaggle/input/plant-pathology-2020-fgvc7/images/Train_{i}.jpg')
    fig.add_subplot(rows, columns, i)
    plt.hist(img.ravel(), bins=32, range=[0, 256])
plt.show()


# # Centre Cropping

# In[ ]:


import numpy as np
from scipy.ndimage import zoom


def clipped_zoom(img, zoom_factor=1.7):

    h, w = img.shape[:2]

    # For multichannel images we don't want to apply the zoom factor to the RGB
    # dimension, so instead we create a tuple of zoom factors, one per array
    # dimension, with 1's for any trailing dimensions after the width and height.
    zoom_tuple = (zoom_factor,) * 2 + (1,) * (img.ndim - 2)

    # Zooming in
    # Bounding box of the zoomed-in region within the input array
    zh = int(np.round(h / zoom_factor))
    zw = int(np.round(w / zoom_factor))
    top = (h - zh) // 2
    left = (w - zw) // 2

    out = zoom(img[top:top+zh, left:left+zw], zoom_tuple)

    # `out` might still be slightly larger than `img` due to rounding, so
    # trim off any extra pixels at the edges
    trim_top = ((out.shape[0] - h) // 2)
    trim_left = ((out.shape[1] - w) // 2)
    out = out[trim_top:trim_top+h, trim_left:trim_left+w]

    return out

w=10
h=10
fig=plt.figure(figsize=(20, 14))
columns = 4
rows = 4
plt.axis('off')
for i in range(1, columns*rows +1):
    img = plt.imread(f'/kaggle/input/plant-pathology-2020-fgvc7/images/Train_{i}.jpg')
    fig.add_subplot(rows, columns, i)
    plt.imshow(clipped_zoom(img))
plt.show()


# Clipped Zooming is working preety well!

# # Making Training Data

# ## Reading data from Keras Generators

# In[ ]:


datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=180,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range = 0.15, # Randomly zoom image 
        width_shift_range=0.15,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.15,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=True, # randomly flip images
        preprocessing_function=clipped_zoom
)  


# In[ ]:


X_train, X_valid = train_test_split(dataset, test_size=0.05, shuffle=False)


# ## Making a Tensorflow Dataset

# In[ ]:


BATCH_SIZE = 8

train_generator = datagen.flow_from_dataframe(dataset, 
                    directory='/kaggle/input/plant-pathology-2020-fgvc7/images/',
                    x_col='image_id',
                    y_col=['healthy', 'multiple_diseases', 'rust', 'scab'] , 
                    target_size=(512, 512), 
                    class_mode='raw',
                    batch_size=BATCH_SIZE, shuffle=False)

valid_generator = datagen.flow_from_dataframe(X_valid, 
                    directory='/kaggle/input/plant-pathology-2020-fgvc7/images/',
                    x_col='image_id',
                    y_col=['healthy', 'multiple_diseases', 'rust', 'scab'] , 
                    target_size=(512, 512), 
                    class_mode='raw',
                    batch_size=BATCH_SIZE, shuffle=False) 


# ## Generator Images Visualisations

# In[ ]:


w=10
h=10
fig=plt.figure(figsize=(20, 14))
columns = 2
rows = 4
plt.title('Image Class')
plt.axis('off')
for i in range(1, columns*rows):
    
    img_batch, label_batch = train_generator.next()
    fig.add_subplot(rows, columns, i)
    
    if label_batch[i][0] == 1:
        plt.title('Healthy')
    elif label_batch[i][1] == 1:
        plt.title('Multiple Disease')
    elif label_batch[i][2] == 1:
        plt.title('Rust')
    else:
        plt.title('Scab')
        
    plt.imshow(img_batch[i])
    plt.axis('off')
plt.show()


# # Making The Models

# ## Xception Model

# In[ ]:



xception_model = tf.keras.models.Sequential([
  tf.keras.applications.xception.Xception(include_top=False, weights='imagenet', input_shape=(512, 512, 3)),
   tf.keras.layers.GlobalAveragePooling2D(),
   tf.keras.layers.Dense(4,activation='softmax')
])
xception_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
xception_model.summary()


# In[ ]:


tf.keras.utils.plot_model(xception_model, to_file='xception_model.png')


# ## DenseNet121

# In[ ]:



densenet_model = tf.keras.models.Sequential([
    tf.keras.applications.densenet.DenseNet121(include_top=False, weights='imagenet',input_shape=(512, 512, 3)),
   tf.keras.layers.GlobalAveragePooling2D(),
   tf.keras.layers.Dense(4,activation='softmax')
])
densenet_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
densenet_model.summary()


# In[ ]:


tf.keras.utils.plot_model(densenet_model, to_file='densenet_model.png')


# # Ensembling the Models

# In[ ]:


inputs = tf.keras.Input(shape=(512, 512, 3))

xception_output = xception_model(inputs)
densenet_output = densenet_model(inputs)

outputs = tf.keras.layers.average([densenet_output, xception_output])


model = tf.keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()


# In[ ]:


tf.keras.utils.plot_model(model, to_file='model.png')


# ## Setting the hyperparameters & Callbacks

# In[ ]:


LR_START = 0.00001
LR_MAX = 0.0001 
LR_MIN = 0.00001
LR_RAMPUP_EPOCHS = 15
LR_SUSTAIN_EPOCHS = 3
LR_EXP_DECAY = .8
EPOCHS = 25

def lrfn(epoch):
    if epoch < LR_RAMPUP_EPOCHS:
        lr = (LR_MAX - LR_START) / LR_RAMPUP_EPOCHS * epoch + LR_START
    elif epoch < LR_RAMPUP_EPOCHS + LR_SUSTAIN_EPOCHS:
        lr = LR_MAX
    else:
        lr = (LR_MAX - LR_MIN) * LR_EXP_DECAY**(epoch - LR_RAMPUP_EPOCHS - LR_SUSTAIN_EPOCHS) + LR_MIN
    return lr
    
lr_callback = tf.keras.callbacks.LearningRateScheduler(lrfn, verbose=True)

rng = [i for i in range(EPOCHS)]
y = [lrfn(x) for x in rng]
plt.plot(rng, y)
print("Learning rate schedule: {:.3g} to {:.3g} to {:.3g}".format(y[0], max(y), y[-1]))


# In[ ]:


model_checkpoint = tf.keras.callbacks.ModelCheckpoint('model.h5', monitor='val_accuracy', verbose=2, save_best_only=True)

# Tensordash is used for getting live model training status, like accuracy or loss, in your phone, sure to checkout here: https://github.com/CleanPegasus/TensorDash
histories = Tensordash(
    email = secret_value_0, 
    password = secret_value_1, 
    ModelName = "Plant Disease Model")


# # Training the Model

# In[ ]:


# Model training 
model_history = model.fit_generator(train_generator, epochs=EPOCHS, validation_data=valid_generator, callbacks=[model_checkpoint,lr_callback, histories])


# ### Saving History

# In[ ]:


# Saving model history
pd.DataFrame(model_history.history).to_csv('ModelHistory.csv')


# ### Model History Visualisation

# In[ ]:


plt.plot(pd.DataFrame(model_history.history)['accuracy'])
plt.title("accuracy Plot")


# In[ ]:


plt.plot(pd.DataFrame(model_history.history)['loss'])
plt.title("Loss Plot")


# In[ ]:


plt.plot(pd.DataFrame(model_history.history)['val_accuracy'])
plt.title("Validation Accuracy Plot")


# In[ ]:


plt.plot(pd.DataFrame(model_history.history)['val_loss'])
plt.title("Validation Accuracy Plot")


# # Predicting Classes

# In[ ]:


# Reading testing and submission data
test_dataset = pd.read_csv('/kaggle/input/plant-pathology-2020-fgvc7/test.csv')
submission = pd.read_csv('/kaggle/input/plant-pathology-2020-fgvc7/sample_submission.csv')
test_dataset


# In[ ]:


# Adding .jpg extension to image_id
test_dataset['image_id'] = test_dataset['image_id']+'.jpg'


# In[ ]:


test_gen = datagen.flow_from_dataframe(test_dataset, 
                    directory='/kaggle/input/plant-pathology-2020-fgvc7/images/',
                    x_col='image_id',
                    target_size=(512, 512), 
                    class_mode=None,
                    shuffle=False,
                    batch_size=8)


# In[ ]:


# Predicting class 
predictions = model.predict_generator(test_gen)


# In[ ]:


submission['healthy'] = predictions[:, 0]
submission['multiple_diseases'] = predictions[:, 1]
submission['rust'] = predictions[:, 2]
submission['scab'] = predictions[:, 3]


# In[ ]:


submission


# In[ ]:


submission.to_csv('submission.csv', index=False)


# In[ ]:




