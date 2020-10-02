#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import gc
import math
import numpy as np
import pandas as pd
from tqdm import tqdm
import random
pd.set_option('mode.chained_assignment', None)
import keras
import tensorflow as tf
from keras import backend as K

K.set_image_data_format('channels_last')
from keras.models import Model, Input, load_model
from keras.layers import Input
from keras.layers.core import Dropout, Lambda
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers.normalization import BatchNormalization
from keras.layers import Activation, Dense
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# Let us convert the problem into a standard Neural Network Image problem whereby we take an input image and produce an output image - have a look at the many kaggle comptetions that use RLE or run length encoding!
# 
# The idea here is to create "images" for every molecule
# 
# We will then create a target output "image" for each molecule and you should then train your favourite NN to reproduce the output target images
# 
# Once you have done that, you can grab the actual scalar coupling constants by just looking up there values from the 2d matrix output from your neural network
# 
# (As these matrices are symmetric you should average over (x,y) and (y,x) indices)
# 
# Note I am producing the smallest possible matrices to save memory - it will be up to you to create a generator to expand them to 29 by 29.
# 
# Good Luck

# In[ ]:


from sklearn.metrics import mean_absolute_error
def group_mean_log_mae(y_true, y_pred, types, floor=1e-9):
    """
    Fast metric computation for this competition: https://www.kaggle.com/c/champs-scalar-coupling
    Code is from this kernel: https://www.kaggle.com/uberkinder/efficient-metric
    """
    maes = (y_true-y_pred).abs().groupby(types).mean()
    return np.log(maes.map(lambda x: max(x, floor))).mean()


# In[ ]:


train = pd.read_csv('../input/train.csv')
molecules = train.molecule_name.unique()
train=train[train.molecule_name.isin(molecules[:10000])]


# In[ ]:


structures = pd.read_csv('../input/structures.csv')
structures = structures[structures.molecule_name.isin(train.molecule_name)]


# In[ ]:


structures.shape


# In[ ]:


train.head()


# In[ ]:


typedict = train[['molecule_name','atom_index_0','atom_index_1','type']]
typedict = typedict.set_index(['molecule_name','atom_index_0','atom_index_1'])
typedict = typedict['type'].map({'2JHH': 1,
                                 '3JHH': 2,
                                 '1JHC': 3,
                                 '2JHC': 4,
                                 '3JHC': 5,
                                 '1JHN': 6,
                                 '2JHN': 7,
                                 '3JHN': 8 })

typedict = typedict.to_dict()
typedict[('dsgdb9nsd_000001',1,0)]


# In[ ]:


structures.head()


# In[ ]:


def TypeMunger(x):
    if (x.molecule_name,x.atom_index_x,x.atom_index_y) in typedict:
        return typedict[(x.molecule_name,x.atom_index_x,x.atom_index_y)]
    elif (x.molecule_name,x.atom_index_y,x.atom_index_x) in typedict:
        return typedict[(x.molecule_name,x.atom_index_y,x.atom_index_x)]
    return 0


# In[ ]:


rawimagedata = {}
sizesofmatrices = {}

for k,groupdf in tqdm((structures.groupby('molecule_name'))):
    # I am just mapping the atom types to numerics as an example feel free to one hot encode them
    groupdf.atom =  groupdf.atom.map({'H': 1, 'C': 2, 'N':3,'O':4,'F':5})
    inputimage = groupdf.merge(groupdf,on=['molecule_name'],how='outer')
    #Fermi Contact seems to love r^-3!
    inputimage['recipdistancecubed'] = 1/np.sqrt((inputimage.x_x-inputimage.x_y)**2+
                                                 (inputimage.y_x-inputimage.y_y)**2+
                                                 (inputimage.z_x-inputimage.z_y)**2)**3
    inputimage.recipdistancecubed = inputimage.recipdistancecubed.replace(np.inf,0)
    inputimage['H1'] = (inputimage.atom_x==1).astype(int)
    inputimage['C1'] = (inputimage.atom_x==2).astype(int)
    inputimage['N1'] = (inputimage.atom_x==3).astype(int)
    inputimage['O1'] = (inputimage.atom_x==4).astype(int)
    inputimage['F1'] = (inputimage.atom_x==5).astype(int)
    inputimage['H2'] = (inputimage.atom_y==1).astype(int)
    inputimage['C2'] = (inputimage.atom_y==2).astype(int)
    inputimage['N2'] = (inputimage.atom_y==3).astype(int)
    inputimage['O2'] = (inputimage.atom_y==4).astype(int)
    inputimage['F2'] = (inputimage.atom_y==5).astype(int)
    inputimage['bondtype'] = inputimage.apply(lambda x: TypeMunger(x),axis=1)
    inputimage['2JHH'] = (inputimage.atom_y==1).astype(int)
    inputimage['3JHH'] = (inputimage.atom_y==2).astype(int)
    inputimage['1JHC'] = (inputimage.atom_y==3).astype(int)
    inputimage['2JHC'] = (inputimage.atom_y==4).astype(int)
    inputimage['3JHC'] = (inputimage.atom_y==5).astype(int)
    inputimage['1JHN'] = (inputimage.atom_y==6).astype(int)
    inputimage['2JHN'] = (inputimage.atom_y==7).astype(int)
    inputimage['3JHN'] = (inputimage.atom_y==8).astype(int)
    
    
    sizesofmatrices[k] = int(math.sqrt(inputimage.shape[0]))
    rawimagedata[k] = inputimage[['H1','C1','N1','O1','F1',
                                  'H2','C2','N2','O2','F2',
                                  '2JHH','3JHH','1JHC','2JHC','3JHC','1JHN','2JHN','3JHN',
                                  'recipdistancecubed']].values.reshape(sizesofmatrices[k],sizesofmatrices[k],19)


# In[ ]:


targetimages = {}
for k,groupdf in tqdm((train.groupby('molecule_name'))):

    outputimage = pd.DataFrame({'molecule_name':k,'atom_index':np.arange(sizesofmatrices[k])})
    outputimage = outputimage.merge(outputimage,on=['molecule_name'],how='outer')
    outputimage = outputimage.merge(groupdf,
                                    left_on=['molecule_name','atom_index_x','atom_index_y'],
                                    right_on=['molecule_name','atom_index_0','atom_index_1'],how='left')
    outputimage = outputimage.merge(groupdf,
                                    left_on=['molecule_name','atom_index_x','atom_index_y'],
                                    right_on=['molecule_name','atom_index_1','atom_index_0'],how='left')
    outputimage['sc'] = outputimage.scalar_coupling_constant_x.fillna(0)+outputimage.scalar_coupling_constant_y.fillna(0)
    targetimages[k] = outputimage[['sc']].values.reshape(sizesofmatrices[k],sizesofmatrices[k],1)


# Note the output target matrix is symmetric so you will get better results averaging (x,y) with (y,x)

# In[ ]:


def train_generator(mymoleculearr, batch_size=16, number_of_batches=None, shuffle=False):
    if number_of_batches is None:
        number_of_batches = np.ceil(len(mymoleculearr) / batch_size)

    counter = 0
    while True:
        idx_start = batch_size * counter
        idx_end = batch_size * (counter + 1)
        x_batch = []
        y_batch = []
        for key in mymoleculearr[idx_start:idx_end]:   
            localimage = rawimagedata[key]
            a = np.zeros((32,32,19))
            a[:localimage.shape[0],:localimage.shape[1]] = localimage
            x_batch.append(a)
            localmask = targetimages[key]
            b = np.zeros((32,32,1))
            b[:localmask.shape[0],:localmask.shape[1]] = localmask
            y_batch.append(b)
        
        yield (np.array(x_batch),np.array(y_batch))
        counter += 1
        if (counter == number_of_batches):
            counter = 0
            if shuffle:
                np.random.shuffle(mymoleculearr)
           
def test_generator(testmoleculearr, batch_size=16, number_of_batches=None):
    if number_of_batches is None:
        number_of_batches = np.ceil(len(testmoleculearr) / batch_size)
        print(number_of_batches)
    counter = 0
    while True:
        idx_start = batch_size * counter
        idx_end = batch_size * (counter + 1)
        x_batch = []
        for key in testmoleculearr[idx_start:idx_end]:    
            localimage = rawimagedata[key]
            a = np.zeros((32,32,19))
            a[:localimage.shape[0],:localimage.shape[1]] = localimage
            x_batch.append(a)
                
        yield (np.array(x_batch))
        counter += 1
        if (counter == number_of_batches):
            counter = 0


# In[ ]:


allmolecules = [*targetimages]
np.random.shuffle(allmolecules)
splitlen = int(len(allmolecules)*.8)
print(splitlen)
trainmolarr = allmolecules[:splitlen]
valmolarr = allmolecules[splitlen:]


# In[ ]:


BATCH_SIZE = 16
NO_OF_TRAINING_IMAGES = len(trainmolarr)
NO_OF_VAL_IMAGES = len(valmolarr)


# In[ ]:


def show_sample():
    batch = next(train_generator(allmolecules, 16))
    x = batch[0][0]
    y = batch[1][0]
    size = (5, 5)
    plt.figure(figsize=size)
    plt.imshow(x[:, :, 0], cmap='gray')
    plt.show()
    plt.figure(figsize=size)
    plt.imshow(y[:, :, 0], cmap='gray')
    plt.show();
    return


# In[ ]:


show_sample()


# In[ ]:


def conv2d_block(input_tensor, n_filters, kernel_size=3, batchnorm=True):
    # first layer
    x = Conv2D(filters=n_filters, kernel_size=(kernel_size, kernel_size), kernel_initializer="he_normal",
               padding="same")(input_tensor)
    if batchnorm:
        x = BatchNormalization()(x)
    x = Activation("elu")(x)
    # second layer
    x = Conv2D(filters=n_filters, kernel_size=(kernel_size, kernel_size), kernel_initializer="he_normal",
               padding="same")(x)
    if batchnorm:
        x = BatchNormalization()(x)
    x = Activation("elu")(x)
    return x

def get_unet(input_img, n_filters=16, dropout=0.5, batchnorm=False):
    # contracting path
    c1 = conv2d_block(input_img, n_filters=n_filters*1, kernel_size=3, batchnorm=batchnorm)
    p1 = MaxPooling2D((2, 2)) (c1)
    p1 = Dropout(dropout*0.5)(p1)

    c2 = conv2d_block(p1, n_filters=n_filters*2, kernel_size=3, batchnorm=batchnorm)
    p2 = MaxPooling2D((2, 2)) (c2)
    p2 = Dropout(dropout)(p2)

    c3 = conv2d_block(p2, n_filters=n_filters*4, kernel_size=3, batchnorm=batchnorm)
    p3 = MaxPooling2D((2, 2)) (c3)
    p3 = Dropout(dropout)(p3)

    c4 = conv2d_block(p3, n_filters=n_filters*8, kernel_size=3, batchnorm=batchnorm)
    p4 = MaxPooling2D(pool_size=(2, 2)) (c4)
    p4 = Dropout(dropout)(p4)
    
    c5 = conv2d_block(p4, n_filters=n_filters*16, kernel_size=3, batchnorm=batchnorm)
    
    # expansive path
    u6 = Conv2DTranspose(n_filters*8, (3, 3), strides=(2, 2), padding='same') (c5)
    u6 = concatenate([u6, c4])
    u6 = Dropout(dropout)(u6)
    c6 = conv2d_block(u6, n_filters=n_filters*8, kernel_size=3, batchnorm=batchnorm)

    u7 = Conv2DTranspose(n_filters*4, (3, 3), strides=(2, 2), padding='same') (c6)
    u7 = concatenate([u7, c3])
    u7 = Dropout(dropout)(u7)
    c7 = conv2d_block(u7, n_filters=n_filters*4, kernel_size=3, batchnorm=batchnorm)

    u8 = Conv2DTranspose(n_filters*2, (3, 3), strides=(2, 2), padding='same') (c7)
    u8 = concatenate([u8, c2])
    u8 = Dropout(dropout)(u8)
    c8 = conv2d_block(u8, n_filters=n_filters*2, kernel_size=3, batchnorm=batchnorm)

    u9 = Conv2DTranspose(n_filters*1, (3, 3), strides=(2, 2), padding='same') (c8)
    u9 = concatenate([u9, c1], axis=3)
    u9 = Dropout(dropout)(u9)
    c9 = conv2d_block(u9, n_filters=n_filters*1, kernel_size=3, batchnorm=batchnorm)
    
    outputs = Conv2D(1, (1, 1), activation='linear') (c9)
    model = Model(inputs=[input_img], outputs=[outputs])
    return model


# In[ ]:


def mymetric(y_true,y_pred):
    y_true = K.flatten(y_true)
    y_pred = K.flatten(y_pred)
    a = K.gather(y_true,tf.where((y_true>0)|(y_true<0)))
    b = K.gather(y_pred,tf.where((y_true>0)|(y_true<0)))
    return K.mean(K.abs(a-b))
 
def myloss(y_true,y_pred):
    y_true = K.flatten(y_true)
    y_pred = K.flatten(y_pred)
    a = K.gather(y_true,tf.where((y_true>0)|(y_true<0)))
    b = K.gather(y_pred,tf.where((y_true>0)|(y_true<0)))
    return K.mean(K.square(a-b))


# In[ ]:


model = get_unet(Input((32,32,19)), n_filters=16, dropout=0.0, batchnorm=False)
model.summary()


# In[ ]:


model.compile(optimizer=Adam(lr=0.001),loss=[myloss],metrics=[mymetric] )


# In[ ]:


BATCH_SIZE = 16


# In[ ]:


K.tensorflow_backend._get_available_gpus()


# In[ ]:


train_gen = train_generator(trainmolarr,  batch_size=BATCH_SIZE, number_of_batches=None, shuffle=True)
val_gen = train_generator(valmolarr, batch_size=BATCH_SIZE, number_of_batches=None, shuffle=False)

callbacks = [
            EarlyStopping(monitor='val_loss', patience=10, verbose=0),
       ]

results = model.fit_generator(train_gen, epochs=100, 
                          steps_per_epoch = len(trainmolarr)//BATCH_SIZE,
                          validation_data=val_gen, 
                          validation_steps =  len(valmolarr)//BATCH_SIZE,   
                          callbacks=callbacks)
model.save('Model.h5')


# In[ ]:


#model.load_weights('Model.h5')


# In[ ]:


val_gen = test_generator(valmolarr, batch_size=BATCH_SIZE, number_of_batches = np.ceil(len(valmolarr) / BATCH_SIZE))


# In[ ]:


out = model.predict_generator(val_gen, np.ceil(len(valmolarr) / BATCH_SIZE))


# In[ ]:


out.shape


# In[ ]:


lookuptable = {}
for i,m in enumerate(valmolarr[:out.shape[0]]):
    lookuptable[m] = out[i]


# In[ ]:


o =train[train.molecule_name.isin(valmolarr[:out.shape[0]])]
o.head()


# In[ ]:


def LookUp(a):

    return ((lookuptable[a.molecule_name][a.atom_index_0][a.atom_index_1]+lookuptable[a.molecule_name][a.atom_index_1][a.atom_index_0])/2)[0]

o['predictions'] = o.apply(lambda x: LookUp(x),axis=1)


# In[ ]:


o[o.molecule_name==valmolarr[0]]


# In[ ]:


for typ in o.type.unique():
    print(typ,group_mean_log_mae(o[o.type==typ].scalar_coupling_constant,
                               o[o.type==typ].predictions,o[o.type==typ].type))


# In[ ]:


group_mean_log_mae(o.scalar_coupling_constant,o.predictions,o.type)


# In[ ]:




