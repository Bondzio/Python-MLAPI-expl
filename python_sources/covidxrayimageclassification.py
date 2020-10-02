#!/usr/bin/env python
# coding: utf-8

# # Detecting Pnemonia and Covid
# 
# This Notebook showcases a CNN for Multiclass Classification using Keras. This model classifies Chest X Ray data into three categories NORMAL,COVID & PNEMONIA.
# 
# This model is trained over dataset provided by Praveen which contains collection of Chest X Ray of Healthy vs Pneumonia (Corona) affected patients infected patients along with few other categories such as SARS (Severe Acute Respiratory Syndrome ) ,Streptococcus & ARDS (Acute Respiratory Distress Syndrome)
# 
# This model performas with high accuracy(above 94 percent) on the test dataset.

# ## 1. Necessary Imports

# In[ ]:


import numpy as np 
import pandas as pd 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
import keras
from keras.models import Sequential
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras.datasets import cifar10
from keras import regularizers
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# Reading the metadata files with data information

data_df = pd.read_csv('../input/coronahack-chest-xraydataset/Chest_xray_Corona_Metadata.csv')
meta_df = pd.read_csv('../input/coronahack-chest-xraydataset/Chest_xray_Corona_dataset_Summary.csv')


# ## 2. Data Analysis

# In[ ]:


data_df


# In[ ]:


meta_df


# the frequency distribution of categories can be seen in the **meta_df**

# In[ ]:


# paths to data directories

test_dir ='../input/coronahack-chest-xraydataset/Coronahack-Chest-XRay-Dataset/Coronahack-Chest-XRay-Dataset/test'
train_dir = '../input/coronahack-chest-xraydataset/Coronahack-Chest-XRay-Dataset/Coronahack-Chest-XRay-Dataset/train'


# In[ ]:


#Divindig the dataset based on column 'Dataset type' into TRAIN and TEST

train_data = data_df[train_df['Dataset_type'] == 'TRAIN']
test_data = data_df[train_df['Dataset_type'] == 'TEST']


# In[ ]:


#Plotting and image

from PIL import Image
im = Image.open(train_dir+'/person588_virus_1135.jpeg')
plt.imshow(im)


# In[ ]:


sample_df = train_data[train_data['Label_2_Virus_category'] == 'COVID-19'].sample(3)
sample_df1 = train_data[train_data['Label'] == 'Normal'].sample(3)
sample_df2 = train_data[train_data['Label'] == 'Pnemonia'].sample(3)


# ## 3. Image and Histogram Visualization for COVID

# In[ ]:


fig, ax = plt.subplots(3, 2, figsize=(16, 16))


plt.figure(figsize = (15,15))

for i,image in enumerate(sample_df['X_ray_image_name']):
    im = plt.imread(train_dir+'/'+image)
    ax[i, 0].imshow(im)
    ax[i,1].hist(im.ravel(),256,[0,256])
    ax[0, 0].set_title('COVID')



#plt.tight_layout()


# ## 4. Image and Histogram Visualization for PNEMONIA

# 

# In[ ]:


fig, ax = plt.subplots(3, 2, figsize=(16, 16))
for i,image in enumerate(sample_df2['X_ray_image_name']):
    im = plt.imread(train_dir+'/'+image)
    ax[i, 0].imshow(im)
    ax[i,1].hist(im.ravel(),256,[0,256])
    ax[0, 0].set_title('PNEMONIA')


# ## 5. Image and Histogram Visualization for PNEMONIA

# In[ ]:


fig, ax = plt.subplots(3, 2, figsize=(16, 16))
for i,image in enumerate(sample_df1['X_ray_image_name']):
    im = plt.imread(train_dir+'/'+image)
    ax[i, 0].imshow(im)
    ax[i,1].hist(im.ravel(),256,[0,256])
    ax[0, 0].set_title('NORMAL')


# ## 6. Train and Test data

# In[ ]:


#Replacing missing values with NA and merging Label and Label_2_Virus_category as label to filter out the image data of the three classes

train_data.fillna('NA', inplace = True)
train_data['Label'] = train_data['Label']+"/"+train_data['Label_2_Virus_category']


# In[ ]:


#Filtering out the data belonging to the following three labels and shuffling the data

train_dff = train_data[(train_data['Label'] =='Pnemonia/COVID-19') | (train_data['Label'] == 'Normal/NA')                        | (train_data['Label'] == 'Pnemonia/NA')]
train_dff = train_dff.sample(frac = 1)
print(len(train_dff))


# In[ ]:


#Similar as above for test data

test_data.fillna('NA', inplace = True)
test_data['Label'] = test_data['Label']+"/"+test_data['Label_2_Virus_category']
test_df = test_data[(test_data['Label'] =='Pnemonia/COVID-19') | (test_data['Label'] == 'Normal/NA')                        | (test_data['Label'] == 'Pnemonia/NA')]

test_df = test_df.sample(frac = 1)
print(len(test_df))


# In[ ]:


test_df[test_df['Label']=='Normal/NA'].sample(2)


# In[ ]:


test_df[test_df['Label']=='Pnemonia/NA'].sample(2)


# In[ ]:


test_df[test_df['Label']=='Pnemonia/COVID-19']


# As seen the **test_df** does not have any covid samples and might not give us information about covid prediction accuracy. Hence we take a slice of 600 images from **train_dff** as **test_df_covid** to test the accuracy of our model.

# In[ ]:


test_df_covid = train_dff[-600:]
train_dff = train_dff[:-600]
print(len(test_df_covid))
print(len(train_dff))


# In[ ]:


test_df_covid[test_df_covid['Label']=='Pnemonia/COVID-19']


# Now our **test_df_covid** has COVID samples present. This dataset should work fine as a test dataset.

# ## 7. Data Augmentation

# In[ ]:


image_gen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.15,
    height_shift_range=0.15,
    brightness_range=None,
    zoom_range=0.10,
    channel_shift_range=0.0,
    fill_mode="nearest",
    cval=0.0,
    horizontal_flip=True,
    rescale=1./255,
    preprocessing_function=None,
    validation_split=0.2,
    dtype=None,
)


# In[ ]:


train_datagen = image_gen.flow_from_dataframe(
    dataframe=train_dff,
    directory=train_dir,
    x_col="X_ray_image_name",
    y_col="Label",
    target_size=(256, 256),
    color_mode="rgb",
    class_mode="categorical",
    batch_size=32,
    seed=25,
    shuffle=True,
    subset='training'
)

valid_datagen = image_gen.flow_from_dataframe(
    dataframe=train_dff,
    directory=train_dir,
    x_col="X_ray_image_name",
    y_col="Label",
    target_size=(256, 256),
    color_mode="rgb",
    class_mode="categorical",
    batch_size=32,
    seed=25,
    shuffle=True,
    subset='validation'
)


# In[ ]:


test_datagen_covid = image_gen.flow_from_dataframe(
    dataframe=test_df_covid,
    directory=train_dir,
    x_col="X_ray_image_name",
    y_col="Label",
    classes = ['Normal/NA','Pnemonia/COVID-19','Pnemonia/NA'],
    target_size=(256, 256),
    color_mode="rgb",
    class_mode="categorical",
    batch_size=32,
    seed=25,
    shuffle=True
)


# In[ ]:


test_datagen = image_gen.flow_from_dataframe(
    dataframe=test_df,
    directory=test_dir,
    x_col="X_ray_image_name",
    y_col="Label",
    classes = ['Normal/NA','Pnemonia/COVID-19','Pnemonia/NA'],
    target_size=(256, 256),
    color_mode="rgb",
    class_mode="categorical",
    batch_size=32,
    seed=25,
    shuffle=True
)


# ## 9. Visualizing the Augmented Data

# In[ ]:


fig, ax = plt.subplots(3, 2, figsize=(16, 16))
for i,j in enumerate(train_datagen):
    
    
    for k in range(6):
        plt.subplot(3,2,k+1)
        plt.imshow((j[0])[k])
        ax[0,0].set_title((j[1])[k])
        
        
    #print(j[1])
    if i == 0:
        break
        


# ## 10. Model Development

# In[ ]:


weight_decay = 1e-4
model = Sequential()
model.add(Conv2D(32, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay), input_shape=[256,256,3]))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Conv2D(32, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))
 
model.add(Conv2D(64, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Conv2D(64, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.3))

model.add(Conv2D(128, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(128, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.4))

model.add(Flatten())
model.add(Dense(3, activation='softmax'))
 
model.summary()


# ## 11. Training

# In[ ]:


opt = tf.keras.optimizers.Adam(learning_rate=0.0005)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

records = model.fit_generator(train_datagen, steps_per_epoch = 3740/32, epochs =20,validation_data = valid_datagen, validation_steps = 935/32)


# In[ ]:


opt = tf.keras.optimizers.Adam(learning_rate=0.0002)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

records = model.fit_generator(train_datagen, steps_per_epoch = 3740/32, epochs = 15,validation_data = valid_datagen, validation_steps = 935/32)


# In[ ]:


opt = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

records = model.fit_generator(train_datagen, steps_per_epoch = 3740/32, epochs = 8,validation_data = valid_datagen, validation_steps =935/32)


# ## 12. Trainig and Validation Accuracy Plots

# In[ ]:


acc = records.history['accuracy']
val_acc = records.history['val_accuracy']
loss = records.history['loss']
val_loss = records.history['val_loss']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()


# ## Model Testing 

# In[ ]:


log=model.evaluate(
    test_datagen_covid,
    batch_size=32,
    verbose=1,
    sample_weight=None,
    steps=600/32,
    callbacks=None,
    max_queue_size=10,
    workers=1,
    use_multiprocessing=False,
    return_dict=False,
)


# In[ ]:


log=model.evaluate(
    test_datagen,
    batch_size=32,
    verbose=1,
    sample_weight=None,
    steps=624/32,
    callbacks=None,
    max_queue_size=10,
    workers=1,
    use_multiprocessing=False,
    return_dict=False,
)


# ## 13. Saving And Loading the model

# In[ ]:


# save model structure to JSON (no weights)
model_json = model.to_json()
with open("/kaggle/working/model_CNN4", "w") as json_file:
    json_file.write(model_json)
# saving the model weight separately
model.save_weights("/kaggle/working/model_weights_CNN4.h5")


# In[ ]:


from keras.models import model_from_json
json_file = open('../input/models/model_CNN', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("../input/models/model.h5")
print("Loaded model from disk")

