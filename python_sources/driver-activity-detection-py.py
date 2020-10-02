#!/usr/bin/env python
# coding: utf-8

# # Machine Learning Engineer Nanodegree
# 
# ## Capstone Project
# 
# ## Project: Write an Algorithm for Distracted Driver Detection 
# 
# ---
# 
# 
# 
# >**Note:** Code and Markdown cells can be executed using the **Shift + Enter** keyboard shortcut.  Markdown cells can be edited by double-clicking the cell to enter edit mode.
# 
# 
# 
# ---
# 
# ### The Road Ahead
# 
# The notebook is broken into separate steps as shown below.
# 
# * [Step 0](#step0): Import Datasets
# * [Step 1](#step1): Create and train a CNN to Classify Driver Images (from Scratch)
# * [Step 2](#step3): Train a CNN with Transfer Learning (Using Fine-tuned VGG16)
# * [Step 3](#step4): Kaggle Results
# 
# 
# 

# In[55]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import os

import keras
import numpy
from keras.preprocessing.image import ImageDataGenerator


# In[56]:


import keras
import numpy
from keras.preprocessing.image import ImageDataGenerator


# <a id="step0"></a>
# ## Step 0: Import Datasets
# 
# ### Import Driver Dataset
# 
# In the following code cell, we create a instance of ImageDataGenerator which does all preprocessing operations on images that we are going to feed to our CNN

# In[57]:


train_datagen = ImageDataGenerator(
        rescale=1./255, validation_split=0.2)
#         shear_range=0.2,
#         zoom_range=0.2,
#         horizontal_flip=True)


# In the following code, we are loading only 32 images at once into memory and performing all the preprocessing operations on loaded images. The flow_from_directory loads a defined set of images from the location of images, instead of loading all images at once into memory.
# 
# - train_generator contains training set
# - val_generator contains validation set

# In[58]:


train_data = '../input/state-farm-distracted-driver-detection/train'
test_data = '../input/state-farm-distracted-driver-detection/test'
train_generator = train_datagen.flow_from_directory(
        train_data,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='training')

val_generator = train_datagen.flow_from_directory(
        train_data,
        target_size=(224,224),
        batch_size=32,
        class_mode='categorical',
        subset='validation')


# In[59]:


from PIL import Image

ac_labels=  ["c0: safe driving",
"c1: texting - right",
"c2: talking on the phone - right",
"c3: texting - left",
"c4: talking on the phone - left",
"c5: operating the radio",
"c6: drinking",
"c7: reaching behind",
"c8: hair and makeup",
"c9: talking to passenger"]


# In[60]:


imgs, labels = next(train_generator)


# ## Dataset Exploration
# - Following code block explores and reveals the dataset

# In[61]:


import functools

def list_counts(start_dir):
    lst = sorted(os.listdir(start_dir))
    out = [(fil, len(os.listdir( os.path.join(start_dir, fil)))) for fil in lst if os.path.isdir(os.path.join(start_dir,fil))]
    return out

out = list_counts(train_data)
labels, counts = zip(*out)
print("Total number of images : ",functools.reduce(lambda a,b : a+b, counts))
out


# ## Data Visualization
# Following code block. displays images and their respective labels of training/ validation dataset

# In[97]:



import matplotlib.pyplot as plt
import pandas as pd
# Pretty display for notebooks
get_ipython().run_line_magic('matplotlib', 'inline')


y = np.array(counts)
width = 1/1.5
N = len(y)
x = range(N)

fig = plt.figure(figsize=(20,15))
ay = fig.add_subplot(211)

plt.xticks(x, labels, size=15)
plt.yticks(size=15)

ay.bar(x, y, width, color="blue")

plt.title('Bar Chart',size=25)
plt.xlabel('classname',size=15)
plt.ylabel('Count',size=15)

plt.show()



def showImages(imgs ,inlabels=None, single=True):
    if single:
        aim = (imgs * 255 ).astype(np.uint8)
        img = Image.fromarray(aim)
        if labels is not None:
            print("Label : ", ac_labels[np.argmax(inlabels)])
        plt.imshow(img)
        plt.show()
    else:
        for i,img in enumerate(imgs):
            lbl = None
            if inlabels is not None:
                lbl = labels[i]
            showImages(img, lbl)

ind = 1
showImages(imgs[:ind], inlabels=labels[:ind], single = False)


# ---
# <a id='step1'></a>
# ## Step 1: Create a CNN to Classify Driver Images (from Scratch)
# 
# 
# 
# A CNN is created to classify driver images.  At the end of the code cell block, the layers of the model are summarized by executing the line:
#     
#         model.summary()
# 
# We have created 6 convolutional layers with 1 max pooling layer and 1 GlobalAveragePooling in between. Filters were increased from 8 to 512 in total convolutional layers. Also dropout was used along with Global average pooling layer before using the fully connected layer. Number of nodes in the last fully connected layer were setup as 10 along with softmax activation function. ReLU activation function was used for all other layers.
# 
# 6 convolutional layers were used to learn hierarchy of high level features. Max pooling layer is added to reduce the dimensionality. Global Average Pooling layer is added to reduce the dimensionality as well as the matrix to row vector. This is because fully connected layer only accepts row vector. Dropout layers were added to reduce overfitting and ensure that the network generalizes well. The last fully connected layer with softmax activation function is added to obtain probabilities of the prediction.
# 

# In[63]:


from keras.layers import ZeroPadding2D, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
from keras.layers import GlobalAveragePooling2D, MaxPooling2D
from keras.models import Model, Sequential
from keras.callbacks import ModelCheckpoint
from keras import regularizers


# In[64]:


input_layer = Input(shape=(224,224, 3))

conv = Conv2D(filters=8, kernel_size=2)(input_layer)
conv = Conv2D(filters=16, kernel_size=2, activation='relu')(conv)
conv = Conv2D(filters=32, kernel_size=2, activation='relu')(conv)
conv = MaxPooling2D()(conv)

conv = Conv2D(filters=64, kernel_size=2, activation='relu')(conv)
conv = Conv2D(filters=128, kernel_size=2, activation='relu')(conv)
conv = Conv2D(filters=512, kernel_size=2, activation='relu')(conv)

conv = GlobalAveragePooling2D()(conv)
dense = Dense(units=500, activation='relu')(conv)
dense = Dropout(0.1)(dense)
dense = Dense(units=100, activation='relu')(dense)
dense = Dropout(0.1)(dense)
output = Dense(units=10, activation='softmax')(dense)

model = Model(inputs=input_layer, outputs = output)


# In[65]:


model.summary()


# ### Compile CNN from scratch Model

# In[66]:


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# ### (IMPLEMENTATION) Train the Model
# 
# The model is trained in the code cell below. Model checkpointing is used to save the model that attains the best validation loss.
# 

# In[67]:


#model.load_weights('best_model_1.hdf5')
checkpoint = ModelCheckpoint('best_model_1.hdf5', save_best_only=True, verbose=1)

history = model.fit_generator(train_generator, steps_per_epoch=len(train_generator),
                    epochs=10,
                   validation_data = val_generator,
                   validation_steps=len(val_generator),
                    callbacks=[checkpoint] )


# - In the following code block, we are plotting the loss value of training and validation to see whether the model is learning or not

# In[68]:


plt.plot(history.history['val_loss'])
plt.show()
plt.plot(history.history['loss'])


# #### Loading test dataset into memory and predict on test images
# - Following code block contains a method, that loads all test images into memory by batches, each batch with 32 images when it is called each time

# In[69]:



get_ipython().system('ls ../input/state-farm-distracted-driver-detection/')
import os
# model.load_weights('../input/best_model_1.hdf5')
#Test Images
batch_index = 0
files_list = os.listdir("../input/state-farm-distracted-driver-detection/test/")
def load_test_images(batch_size=32, src='../input/state-farm-distracted-driver-detection/test/'):
    global batch_index, files_list
    imgs_list = files_list[batch_index: batch_index+batch_size]
    batch_index += len(imgs_list)
    batch_imgs = []
    for img_name in imgs_list:
        img = Image.open(src+img_name)
        im = img.resize((224,224))
        batch_imgs.append(np.array(im)/255.)
#     plt.imshow()
#     plt.show()
    return np.array(batch_imgs)


# - Following code block predicts on test images by loading 32 images a batch using load_test_images function

# In[70]:


#Test Images write
import sys
preds_list = np.array([])
batch_index=0
batch_size = 32
while True:
    tst_imgs = load_test_images(batch_size=batch_size)
    if(tst_imgs.shape[0] <= 0  ):
        print("Batchsize is less : ",batch_index)
        break
    preds = model.predict(tst_imgs)
    print("\r {},  batch_size : {}, nth_batch/all_batch : {}/{}".format(preds_list.shape,batch_size, batch_index, len(files_list)),end="")    
    sys.stdout.flush()
    if len(preds_list) == 0:
        preds_list = np.array(preds)
    else:
        preds_list = np.append(preds_list, preds, axis=0)


# ## Convert the predicted output to submittable output file

# In[72]:


titles = "img,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9".split(",")
names = pd.DataFrame(files_list[:len(preds_list)])
names.columns=["img"]
df = pd.DataFrame(preds_list)
df.columns=titles[1:]
df['img']=names['img']
df = df[titles]
df.tail()
df.to_csv('sub.csv',index=False)


# ## Predictions by scratch CNN on some sample images
# - Seems like the predictions are not so accurate because of less training

# In[98]:


indices = [1,24]
for index in indices:
#     display(df.iloc[index])
    cls = np.argmax(list(df.iloc[index][1:]))
    print("label : ",ac_labels[cls])
    im_test = Image.open('../input/state-farm-distracted-driver-detection/test/'+df.iloc[index]['img'])
    plt.imshow(np.array(im_test))
    plt.show()


# ---
# <a id="step2"></a>
# ##  Step 2: Train a CNN with Transfer Learning (Using Fine-tuned VGG16 Model)
# 
# - In the following steps, we are going to load a VGG16 model, without top Fully connected layers, with its trained weights
# - Then we are going add Fully Connected Layers on top of GlobalAveragePooling layer with Dropout layers in between
# - The following code block contains a method load_VGG16, which loads VGG16 model with weights loaded when weights file location is given

# In[ ]:



def load_VGG16(weights_path=None, no_top=True):

    input_shape = (224, 224, 3)

    #Instantiate an empty model
    img_input = Input(shape=input_shape)   # Block 1
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')(img_input)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)
    x = GlobalAveragePooling2D()(x)
    vmodel = Model(img_input, x, name='vgg16')
    if weights_path is not None:
        print("Weights have been loaded.")
        vmodel.load_weights(weights_path)

    return vmodel


# - In the following code block, we have added 3 Dense layers with dropout layers on top of VGG16 CNN model.

# In[84]:


vgg_model_raw = load_VGG16('../input/vgg16-weights/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5')

vgg_model = vgg_model_raw.output
#vgg_model = Flatten()(vgg_model)
vgg_model = Dense(5000, activation='relu',kernel_regularizer=regularizers.l2(0.00001))(vgg_model)
#vgg_model = Dropout(0.1)(vgg_model)
#vgg_model = Dense(1000, activation='relu')(vgg_model)
vgg_model = Dropout(0.1)(vgg_model)
vgg_model = Dense(500, activation='relu',kernel_regularizer=regularizers.l2(0.00001))(vgg_model)
vgg_model = Dropout(0.1)(vgg_model)
vgg_model = Dense(10, activation='softmax')(vgg_model)
vgg_m = Model(inputs=vgg_model_raw.input, outputs= vgg_model)


# In[85]:


vgg_m.layers[16].get_weights()


# ### Compile the vgg16 model with categorical crossentropy as loss function and SGD as optimizer

# In[86]:


vgg_m.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.SGD(0.001), metrics=['accuracy'])


# In[96]:


vgg_m.summary()


# - Create a Checkpoint to save best weights, when loss in improvised
# - Train the model for 6 epochs

# In[87]:



checkpoint = ModelCheckpoint('vgg_model.h5', save_best_only=True, verbose=1)

history = vgg_m.fit_generator(train_generator, steps_per_epoch=len(train_generator),
                   epochs=6,
                   validation_data = val_generator,
                   validation_steps=len(val_generator),
                   callbacks=[checkpoint] )


# In[88]:


plt.plot(history.history['val_loss'])
plt.show()
plt.plot(history.history['loss'])


# - Following method gives a batch of 32 images at each call, just like a generator

# In[95]:


get_ipython().system('ls')
import os
#model.load_weights('../input/best_model_1.hdf5')
#Test Images
batch_index = 0
#files_lst = os.listdir("../input/state-farm-distracted-driver-detection/test")
files_list = os.listdir("../input/state-farm-distracted-driver-detection/test")
def load_test_images(batch_size=32, src='../input/state-farm-distracted-driver-detection/test/'):
    global batch_index, files_list
    imgs_list = files_list[batch_index: batch_index+batch_size]
    batch_index += len(imgs_list)
    batch_imgs = []
    for img_name in imgs_list:
        img = Image.open(src+img_name)
        im = img.resize((224,224))
        batch_imgs.append(np.array(im)/255.)
#     plt.imshow()
#     plt.show()
    return np.array(batch_imgs)


# In[90]:


#Test Images write
import sys
preds_list = np.array([])
batch_index=0
batch_size = 32

mm_raw = load_VGG16()

mm_model = mm_raw.output
mm_model = Dense(5000, activation='relu',kernel_regularizer=regularizers.l2(0.00001))(mm_model)
mm_model = Dropout(0.1)(mm_model)
mm_model = Dense(500, activation='relu',kernel_regularizer=regularizers.l2(0.00001))(mm_model)
mm_model = Dropout(0.1)(mm_model)
mm_model = Dense(10, activation='softmax')(mm_model)
mm = Model(inputs=vgg_model_raw.input, outputs= vgg_model)

mm.load_weights('vgg_model.h5')



while True:
    tst_imgs = load_test_images(batch_size=batch_size)
    if(tst_imgs.shape[0] <= 0  ):
        print("Batchsize is less : ",batch_index)
        break
    preds = mm.predict(tst_imgs)
    print("\r {},  batch_size : {}, nth_batch/all_batch : {}/{}".format(preds_list.shape,batch_size, batch_index, len(files_list)),end="")    
    sys.stdout.flush()
    if len(preds_list) == 0:
        preds_list = np.array(preds)
    else:
        preds_list = np.append(preds_list, preds, axis=0)


# In[91]:



titles = "img,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9".split(",")
names = pd.DataFrame(files_list[:len(preds_list)])
names.columns=["img"]
df = pd.DataFrame(preds_list)
df.columns=titles[1:]
df['img']=names['img']
df = df[titles]
df.tail()


# In[92]:


df.to_csv('sub_VGG16.csv',index=False)


# In[99]:


indices = [10,24]
for index in indices:
#     display(df.iloc[index])
    cls = np.argmax(list(df.iloc[index][1:]))
    print("label : ",ac_labels[cls])
    im_test = Image.open('../input/state-farm-distracted-driver-detection/test/'+df.iloc[index]['img'])
    plt.imshow(np.array(im_test))
    plt.show()


# In[94]:


get_ipython().system('cat sub_VGG16.csv | head -10')


# In[ ]:




