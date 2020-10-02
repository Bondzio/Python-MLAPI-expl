#!/usr/bin/env python
# coding: utf-8

# # Overview
# We try to train a simple model from scratch to see how well we can classify different diseases in the X-Rays. The notebook just shows how to use the HDF5 output to make getting started easier

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from glob import glob
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import h5py
from keras.utils.io_utils import HDF5Matrix


# Show the dataset and different field we can work with

# In[ ]:


h5_path = '../input/create-a-mini-xray-dataset-equalized/chest_xray.h5'
disease_vec_labels = ['Atelectasis','Cardiomegaly','Consolidation','Edema','Effusion','Emphysema','Fibrosis',
 'Hernia','Infiltration','Mass','Nodule','Pleural_Thickening','Pneumonia','Pneumothorax']
disease_vec = []
with h5py.File(h5_path, 'r') as h5_data:
    all_fields = list(h5_data.keys())
    for c_key in all_fields:
        print(c_key, h5_data[c_key].shape, h5_data[c_key].dtype)
    for c_key in disease_vec_labels:
        disease_vec += [h5_data[c_key][:]]
disease_vec = np.stack(disease_vec,1)
print('Disease Vec:', disease_vec.shape)


# In[ ]:


img_ds = HDF5Matrix(h5_path, 'images')
split_idx = img_ds.shape[0]//2
train_ds = HDF5Matrix(h5_path, 'images', end = split_idx)
test_ds = HDF5Matrix(h5_path, 'images', start = split_idx)
train_dvec = disease_vec[0:split_idx]
test_dvec = disease_vec[split_idx:]
print('Train Shape', train_ds.shape, 'test shape', test_ds.shape)


# In[ ]:


from keras.applications.mobilenet import MobileNet
from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout, BatchNormalization, AveragePooling2D
raw_model = MobileNet(input_shape=(None, None, 1), include_top = False, weights = None)
full_model = Sequential()
full_model.add(AveragePooling2D((2,2), input_shape = img_ds.shape[1:]))
full_model.add(BatchNormalization())
full_model.add(raw_model)
full_model.add(Flatten())
full_model.add(Dropout(0.5))
full_model.add(Dense(64))
full_model.add(Dense(disease_vec.shape[1], activation = 'sigmoid'))
full_model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['acc'])
full_model.summary()


# In[ ]:


from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau
file_path="weights.best.hdf5"
checkpoint = ModelCheckpoint(file_path, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
early = EarlyStopping(monitor="val_acc", mode="max", patience=3)
callbacks_list = [checkpoint, early] #early


# In[ ]:


full_model.fit(train_ds, train_dvec, 
               validation_data = (test_ds, test_dvec),
               epochs=5, 
               verbose = True,
              shuffle = 'batch',
              callbacks = callbacks_list)


# In[ ]:




