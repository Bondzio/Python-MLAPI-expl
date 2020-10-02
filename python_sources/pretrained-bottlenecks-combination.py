#!/usr/bin/env python
# coding: utf-8

# ## Summary
# We have tried different pretrained models (Xception, Vgg16, Rest50) to obtain bottleneck features and build a new model. The best performance has been obtained combining the bottlenecks of all of these models. 

# ## Data loading and fast analysis

# In[56]:


import warnings
warnings.simplefilter("ignore", category=FutureWarning)

import os
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
import random as rn
from keras import backend as K

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score


# In[2]:


os.environ['PYTHONHASHSEED'] = '0'

SEED = 1
np.random.seed(SEED)
rn.seed(SEED)


# In[3]:


data_dir = "../input/plant-seedlings-classification/"

img_rows, img_cols, img_channel = 117, 117, 3
target_size = (img_rows, img_cols)
target_dims = (img_rows, img_cols, img_channel) # add channel for RGB
n_classes = 12
val_frac = 0.1
batch_size = 256

LAYERS_TO_FREEZE = 18


# In[4]:


import cv2
from glob import glob
from matplotlib import pyplot as plt
from numpy import floor
import random


# In[5]:


base_path = os.path.join(data_dir, "train")
classes = os.listdir(base_path)


# In[6]:


sample_images = []
plants = {}
for plant in classes:
    img_path = os.path.join(base_path, plant, '**') 
    path_contents = glob(img_path)
    total_plants = len(path_contents)
    plants[plant] = total_plants
    img = random.sample(path_contents, 1)
    sample_images.append(img)


# Let's check some images:

# In[7]:


fig = plt.figure(figsize=(10,10))
for i in range(0, 12):
    fig.add_subplot(4, 4, i+1)
    fig.tight_layout()
    img = cv2.imread(sample_images[i][0])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)     
    plt.imshow(img)
    plt.axis('off')
    plt.title(classes[i])    
plt.show()


# The dataset is not full balanced:

# In[8]:


plt.figure(figsize=(10, 8))
plt.title("Number of cases per fruit (Training data)")
plt.bar(range(n_classes), list(plants.values()))
plt.xticks(range(n_classes), classes, rotation=90)
plt.show()


# In[9]:


print("width: {} | length: {} | min value: {} | max value: {}".format(img.shape[0], img.shape[1], img.min(), img.max()))


# ## Models

# In[10]:


from keras.layers import Conv2D, Dense, Dropout, Flatten, BatchNormalization
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from keras.optimizers import Adam
from keras import applications
from keras.models import Sequential, Model, load_model
from keras import applications
from keras import optimizers
from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D


# In[11]:


cache_dir = os.path.expanduser(os.path.join('~', '.keras'))
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# Create symbolic links for trained models.
models_symlink = os.path.join(cache_dir, 'models')
if not os.path.exists(models_symlink):
    os.symlink('/kaggle/input/keras-pretrained-models/', models_symlink)


# In[12]:


def create_generators(preprocess_input, data_path, target_size, batch_size, seed=1):
    data_augmentor = ImageDataGenerator(preprocessing_function=preprocess_input,
                                        validation_split=0.2)  
    
    train_generator = data_augmentor.flow_from_directory(data_path, 
                                                     target_size=target_size, 
                                                     batch_size=batch_size, 
                                                     subset="training", 
                                                     shuffle=False, seed=seed)
    val_generator = data_augmentor.flow_from_directory(data_path, 
                                                       target_size=target_size, 
                                                       batch_size=batch_size, 
                                                       subset="validation", 
                                                       shuffle=False, 
                                                       seed=seed)
    return train_generator, val_generator


# In[13]:


SEED_NN = 123456
np.random.seed(SEED_NN)
rn.seed(SEED_NN)
session_conf = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
tf.set_random_seed(SEED_NN)
sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
K.set_session(sess)    


# ## Xception bottleneck

# In[14]:


def get_bottleneck_xception(data_path, target_dims, batch_size, seed=SEED):
    preprocess_input = applications.xception.preprocess_input    
    img_rows, img_cols, img_channel = target_dims
    target_size = (img_rows, img_cols)
    target_dims = (img_rows, img_cols, img_channel) 
    train_generator, val_generator = create_generators(preprocess_input, data_path, target_size, batch_size, seed=SEED)
    
    model_xception = applications.Xception(weights='imagenet', 
                                           include_top=False, 
                                           pooling='avg',
                                           input_shape=target_dims)
    
    x_train = model_xception.predict_generator(train_generator, verbose=0)
    y_train = train_generator.classes
    
    x_val = model_xception.predict_generator(val_generator, verbose=0)
    y_val = val_generator.classes

    return x_train, x_val, y_train, y_val


# In[23]:


data_path = data_dir + "train"


# In[24]:


x_xception_train, x_xception_val, y_xception_train, y_xception_val =     get_bottleneck_xception(data_path, (299, 299, 3), batch_size, seed=SEED)


# In[32]:


lr = LogisticRegression(multi_class='multinomial', solver='lbfgs', random_state=SEED)
lr.fit(x_xception_train, y_xception_train)
y_xception_pred = lr.predict(x_xception_val)
accuracy_score(y_xception_val, y_xception_pred)


# ## Vgg16 bottleneck

# In[33]:


def get_bottleneck_vgg16(data_path, target_dims, batch_size, seed=SEED):
    preprocess_input = applications.vgg16.preprocess_input    
    img_rows, img_cols, img_channel = target_dims
    target_size = (img_rows, img_cols)
    target_dims = (img_rows, img_cols, img_channel) 
    train_generator, val_generator = create_generators(preprocess_input, data_path, target_size, batch_size, seed=SEED)


    model_xception = applications.VGG16(weights='imagenet', 
                                        include_top=False, 
                                        pooling='avg',
                                        input_shape=target_dims)
    
    x_train = model_xception.predict_generator(train_generator, verbose=0)
    y_train = train_generator.classes
    
    x_val = model_xception.predict_generator(val_generator, verbose=0)
    y_val = val_generator.classes

    return x_train, x_val, y_train, y_val


# In[34]:


x_vgg16_train, x_vgg16_val, y_vgg16_train, y_vgg16_val = get_bottleneck_vgg16(data_path, (224, 224, 3), batch_size, seed=SEED)


# In[35]:


lr = LogisticRegression(multi_class='multinomial', solver='lbfgs', random_state=SEED)
lr.fit(x_vgg16_train, y_vgg16_train)
y_vgg16_pred = lr.predict(x_vgg16_val)
accuracy_score(y_vgg16_val, y_vgg16_pred)


# ## Resnet50 bottleneck

# In[62]:


def get_bottleneck_resnet50(data_path, target_dims, batch_size, seed=SEED):
    preprocess_input = applications.resnet50.preprocess_input    
    img_rows, img_cols, img_channel = target_dims
    target_size = (img_rows, img_cols)
    target_dims = (img_rows, img_cols, img_channel) 
    train_generator, val_generator = create_generators(preprocess_input, data_path, target_size, batch_size, seed=SEED)

    model_xception = applications.ResNet50(weights='imagenet', 
                                           include_top=False, 
                                           pooling='avg',
                                           input_shape=target_dims)
    
    x_train = model_xception.predict_generator(train_generator, verbose=0)
    y_train = train_generator.classes
    
    x_val = model_xception.predict_generator(val_generator, verbose=0)
    y_val = val_generator.classes

    return x_train, x_val, y_train, y_val


# In[37]:


x_resnet50_train, x_resnet50_val, y_resnet50_train, y_resnet50_val =     get_bottleneck_resnet50(data_path, (224, 224, 3), batch_size, seed=SEED)


# In[38]:


lr_resnet50 = LogisticRegression(multi_class='multinomial', solver='lbfgs', random_state=SEED)
lr_resnet50.fit(x_resnet50_train, y_resnet50_train)
y_resnet50_pred = lr_resnet50.predict(x_resnet50_val)
accuracy_score(y_resnet50_val, y_resnet50_pred)


# ## Mix model
# we are going to combine all the previous bottlenecks to build a new model

# In[39]:


x_train = np.hstack([x_vgg16_train, x_xception_train, x_resnet50_train])
x_val = np.hstack([x_vgg16_val, x_xception_val, x_resnet50_val])


# In[40]:


x_train.shape


# In[41]:


np.logical_and((y_xception_val==y_vgg16_val).all(), (y_vgg16_val==y_resnet50_val).all())


# In[42]:


np.logical_and((y_xception_train==y_vgg16_train).all(), (y_vgg16_train==y_resnet50_train).all())


# In[43]:


y_train = y_vgg16_train
y_val = y_vgg16_val


# ### Logistic Regression
# We are going to try Logistic Regression to combine all the bottlenecks:

# In[50]:


from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

lr = LogisticRegression(multi_class='multinomial', class_weight="balanced", solver='lbfgs', random_state=SEED)
pipeline = make_pipeline(StandardScaler(), lr)

pipeline.fit(x_train, y_train)
y_pred = pipeline.predict(x_val)
accuracy_score(y_val, y_pred)


# ### SVM
# We are going to try SVM to combine all the bottlenecks. We are going to have a better performance:

# In[51]:


from sklearn.svm import SVC
svc = SVC(kernel="linear", class_weight="balanced", random_state=SEED)
pipeline_svc = make_pipeline(StandardScaler(), svc)

pipeline_svc.fit(x_train, y_train)
y_svc_pred = pipeline_svc.predict(x_val)
accuracy_score(y_val, y_svc_pred)


# In[54]:


print(classification_report(y_val, y_svc_pred))


# In[55]:


import scikitplot as skplt
skplt.metrics.plot_confusion_matrix(y_val, y_svc_pred, normalize=False, figsize=(10, 10))
plt.show()

