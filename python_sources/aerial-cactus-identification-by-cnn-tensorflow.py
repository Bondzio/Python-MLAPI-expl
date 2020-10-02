#!/usr/bin/env python
# coding: utf-8

# # Aerial Cactus Identification

# ## Competition Description from Kaggle
# To assess the impact of climate change on Earth's flora and fauna, it is vital to quantify how human activities such as logging, mining, and agriculture are impacting our protected natural areas. Researchers in Mexico have created the VIGIA project, which aims to build a system for autonomous surveillance of protected areas. A first step in such an effort is the ability to recognize the vegetation inside the protected areas. In this competition, you are tasked with creation of an algorithm that can identify a specific type of cactus in aerial imagery.

# ### Data Format
# <ol>
#     <li>A folder containing 32x32 images.</li>
#     <li>Files train.csv and test.csv containing name of file as key, and a binary column has_cactus, which is 0 if no cactus in image and 1 if there is cactus in image.</li>
# </ol>
# 
# ### Target
# Take images and classify whether the image contains cactus or not.

# 
# ## First Steps

# ### Import Data From Kaggle

# In[ ]:


import tensorflow as tf
import tensorflow.keras as keras
import matplotlib.pyplot as plt
import os
from PIL import Image
import pathlib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pathlib
import math

tf.enable_eager_execution()

get_ipython().run_line_magic('matplotlib', 'inline')

INPUT_DIR = '../input'
TRAIN_IMG_DIR = INPUT_DIR+'/train/train'
PRED_IMG_DIR = INPUT_DIR+'/test/test'

AUTOTUNE = tf.data.experimental.AUTOTUNE

np.random.seed(1000)


# ### Import Required Libraries

# In[ ]:


df = pd.read_csv(INPUT_DIR+'/train.csv')
df.head()


# In[ ]:


# Split the dataset into training and testing set.
train_df, test_df = train_test_split(df, train_size=0.70, random_state=0)

# Find the number of items in each dataset
n_training_items = train_df['id'].count()
n_testing_items = test_df['id'].count()


# In[ ]:


def img_path(img_file, img_type=0):
    """ 
    img_file: name of image file
    img_type: 0 if for training, 1 for evaluation dataset.
    """
    if img_type==0:
        return TRAIN_IMG_DIR+'/'+img_file
    else:
        return PRED_IMG_DIR+'/'+img_file
    
# Find the filename and corresponding labels of all images in training dataset.
train_image_paths = [img_path(x) for x in train_df['id']]
train_image_labels = [x for x in train_df['has_cactus']]
    
# Find the filename and corresponding labels of all images in testing dataset.
test_image_paths = [img_path(x) for x in test_df['id']]
test_image_labels = [x for x in test_df['has_cactus']]

# Find the filenames of all prediction files.
path = os.listdir(PRED_IMG_DIR)
pred_images_paths = [img_path(x, 1) for x in path]
n_pred_items = len(pred_images_paths)


# ## Check Image Type

# In[ ]:


im = Image.open(train_image_paths[0])
print(im.format, im.size, im.mode)
imgplot = plt.imshow(im)


# The images are JPEG images of 32x32 resolution with 3 channels.

# ## Data Preprocessing

# In[ ]:


def load_and_preprocess_image(imagefile):
    
    def preprocess_image(image):
        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.resize(image, [32, 32])
        image /= 255.0  # normalize to [0,1] range
        return image
    
    image = tf.read_file(imagefile)
    return preprocess_image(image)

def load_and_preprocess_from_path_label(path, label):
    return load_and_preprocess_image(path), label


# ## Creating Input Pipiline

# In[ ]:


# Tensorflow Dataset containing all image paths and labels
train_ds = tf.data.Dataset.from_tensor_slices((train_image_paths, train_image_labels))
test_ds = tf.data.Dataset.from_tensor_slices((test_image_paths, test_image_labels))
pred_ds = tf.data.Dataset.from_tensor_slices(pred_images_paths)

# Load the images into dataset from the path in the dataset
train_ds = train_ds.map(load_and_preprocess_from_path_label)
test_ds = test_ds.map(load_and_preprocess_from_path_label)
pred_ds = pred_ds.map(load_and_preprocess_image)

train_ds


# In[ ]:


BATCH_SIZE = 32
steps_per_epoch = int(math.ceil(n_training_items/BATCH_SIZE))
# Training Dataset
train_ds1 = (train_ds.cache()
             .apply(
                 tf.data.experimental.shuffle_and_repeat(buffer_size=n_training_items)
             )
             .batch(BATCH_SIZE)
             .prefetch(buffer_size=AUTOTUNE)
            )

# Testing dataset
test_ds1 = (test_ds.cache()
            .apply(tf.data.experimental.shuffle_and_repeat(buffer_size=n_training_items))
            .batch(BATCH_SIZE)
            .prefetch(buffer_size=AUTOTUNE))

# Prediction dataset
pred_ds1 = (pred_ds
            .cache()
            .batch(BATCH_SIZE)
            .prefetch(buffer_size=AUTOTUNE)
           )

print(train_ds1, pred_ds1)


# ## Create Model
# Using VGG19 inspired model.

# In[ ]:


model = keras.Sequential([
    tf.layers.Conv2D(filters=12, strides=1, kernel_size=3, padding='valid',activation=tf.nn.leaky_relu, input_shape=(32,32,3)),
    tf.layers.Conv2D(filters=32, kernel_size=3, activation=tf.nn.leaky_relu, input_shape=(32,32,3), padding='same'),
    tf.layers.Conv2D(filters=32, kernel_size=3, activation=tf.nn.leaky_relu, padding='same'),
    tf.layers.AveragePooling2D(pool_size=3, strides=2),

    tf.layers.Conv2D(filters=64, kernel_size=3, activation=tf.nn.leaky_relu, padding='same'),
    tf.layers.Conv2D(filters=64, kernel_size=3, activation=tf.nn.leaky_relu, padding='same'),
    tf.layers.MaxPooling2D(pool_size=(2,2), strides=2),
    tf.layers.Flatten(),
    tf.layers.Dense(units=2, activation='softmax')
])

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()


# In[ ]:


### Fit and Evaluate


# In[ ]:



model.fit(train_ds1, epochs=6, steps_per_epoch=steps_per_epoch)


# In[ ]:


model.evaluate(test_ds1, steps=n_testing_items)


# We can see that the testing set accuracy is higher than training set accuracy. Hence the model generalizes well.

# ## Evaluate and Prepare Submission File

# In[ ]:


logits = model.predict(pred_ds1, steps=n_pred_items)
predictions = np.argmax(logits, axis=-1)


# In[ ]:


names = np.array([x for x in path])
pred_df = pd.DataFrame(
    {
        "id":names,
        "has_cactus":predictions
    })
pred_df.head()


# In[ ]:


pred_df.to_csv('submission.csv', index=False)

