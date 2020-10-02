#!/usr/bin/env python
# coding: utf-8

# 
# 
# ## Information
# * In this code train a model and check the results in the last cells, where can be seen  the true positives and false positives of the network's outout
# * The model used is `vanilla  unet` since seems it trains faster and get better results from other config tested in **V5**
# * The data set is augmented while training
# * The model is evaluated with the validation set without augmentation
# 
# ## Log
# 
# * **V10** test applyig dropout
# * **V5** Comparison of different network configuration number of kernels and layers
# 
# 
# 
# ## Inprovements from last version
# 
# * The data generator have been updated to save in memory all images and masks before training.
# * Images have been undersize to fit the entire set in the 13GB memory of the GPU:
#     1. Images are converted to gray scale to have only one channel
#     2. Images have been set to 128x128
# 
# 
# ## References
# 
# * EDA of albumentations: https://www.kaggle.com/artgor/segmentation-in-pytorch-using-convenient-tools
# * Data generator: https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly
# * RLE encoding and decoding: https://www.kaggle.com/paulorzp/rle-functions-run-lenght-encode-decode
# * Architecture: https://www.kaggle.com/jesperdramsch/intro-chest-xray-dicom-viz-u-nets-full-data
# * Mask encoding: https://www.kaggle.com/c/siim-acr-pneumothorax-segmentation/data
# * My original Kernel U-Net: https://www.kaggle.com/xhlulu/severstal-simple-keras-u-net-boilerplate

# # Import

# In[ ]:


import os
import json

import gc

import albumentations as albu
import cv2
import keras
from keras import backend as K
from keras.models import Model
from keras.layers import Input
from keras.layers import Dropout
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate
from keras.losses import binary_crossentropy
from keras.optimizers import Adam, Nadam
from keras.callbacks import Callback, ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split


# # Preprocessing

# In[ ]:


train_df = pd.read_csv('/kaggle/input/understanding_cloud_organization/train.csv')
train_df['ImageId'] = train_df['Image_Label'].apply(lambda x: x.split('_')[0])
train_df['ClassId'] = train_df['Image_Label'].apply(lambda x: x.split('_')[1])
train_df['hasMask'] = ~ train_df['EncodedPixels'].isna()

print(train_df.shape)
train_df.head()


# In[ ]:


mask_count_df = train_df.groupby('ImageId').agg(np.sum).reset_index()
mask_count_df.sort_values('hasMask', ascending=False, inplace=True)
print(mask_count_df.shape)
mask_count_df.head()


# In[ ]:


sub_df = pd.read_csv('/kaggle/input/understanding_cloud_organization/sample_submission.csv')
sub_df['ImageId'] = sub_df['Image_Label'].apply(lambda x: x.split('_')[0])
test_imgs = pd.DataFrame(sub_df['ImageId'].unique(), columns=['ImageId'])


# # Utility Functions
# 
# Source: https://www.kaggle.com/paulorzp/rle-functions-run-lenght-encode-decode
# 
# Unhide below for the definition of `np_resize`, `build_masks`, `build_rles`.

# In[ ]:


def np_resize(img, input_shape):
    """
    Reshape a numpy array, which is input_shape=(height, width), 
    as opposed to input_shape=(width, height) for cv2
    """
    height, width = input_shape
    return cv2.resize(img, (width, height))
    
def mask2rle(img):
    '''
    img: numpy array, 1 - mask, 0 - background
    Returns run length as string formated
    '''
    pixels= img.T.flatten()
    pixels = np.concatenate([[0], pixels, [0]])
    runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
    runs[1::2] -= runs[::2]
    return ' '.join(str(x) for x in runs)

def rle2mask(rle, input_shape):
    width, height = input_shape[:2]
    
    mask= np.zeros( width*height ).astype(np.uint8)
    
    array = np.asarray([int(x) for x in rle.split()])
    starts = array[0::2]
    lengths = array[1::2]

    current_position = 0
    for index, start in enumerate(starts):
        mask[int(start):int(start+lengths[index])] = 1
        current_position += lengths[index]
        
    return mask.reshape(height, width).T

def build_masks(rles, input_shape, reshape=None):
    depth = len(rles)
    if reshape is None:
        masks = np.zeros((*input_shape, depth))
    else:
        masks = np.zeros((*reshape, depth))
    
    for i, rle in enumerate(rles):
        if type(rle) is str:
            if reshape is None:
                masks[:, :, i] = rle2mask(rle, input_shape)
            else:
                mask = rle2mask(rle, input_shape)
                reshaped_mask = np_resize(mask, reshape)
                masks[:, :, i] = reshaped_mask
    
    return masks

def build_rles(masks, reshape=None):
    width, height, depth = masks.shape
    
    rles = []
    
    for i in range(depth):
        mask = masks[:, :, i]
        
        if reshape:
            mask = mask.astype(np.float32)
            mask = np_resize(mask, reshape).astype(np.int64)
        
        rle = mask2rle(mask)
        rles.append(rle)
        
    return rles


# # Visualization functions

# In[ ]:


def visualize(image, mask, mask_prediction):
    fontsize = 14
    class_dict = {0: 'Fish', 1: 'Flower', 2: 'Gravel', 3: 'Sugar'}
    f, ax = plt.subplots(2, 5, figsize=(24,8))

    ax[0, 0].imshow(image.reshape(image.shape[0],image.shape[1]))
    ax[0, 0].set_title('Original image', fontsize=fontsize)

    for i in range(4):
        ax[0, i + 1].imshow(mask[:, :, i],vmin = 0, vmax = 1)
        ax[0, i + 1].set_title(f'Original mask {class_dict[i]}', fontsize=fontsize)
    
    ax[1, 0].imshow(image.reshape(image.shape[0],image.shape[1]))
    ax[1, 0].set_title('Original image', fontsize=fontsize)

    for i in range(4):
        ax[1, i + 1].imshow(mask_prediction[:, :, i],vmin = 0, vmax = 1)
        ax[1, i + 1].set_title(f'Prediction {class_dict[i]}', fontsize=fontsize)


# ## RAdam
# 
# Unhide below to see definition of `RAdam`:

# In[ ]:


class RAdam(keras.optimizers.Optimizer):
    """RAdam optimizer.
    # Arguments
        lr: float >= 0. Learning rate.
        beta_1: float, 0 < beta < 1. Generally close to 1.
        beta_2: float, 0 < beta < 1. Generally close to 1.
        epsilon: float >= 0. Fuzz factor. If `None`, defaults to `K.epsilon()`.
        decay: float >= 0. Learning rate decay over each update.
        weight_decay: float >= 0. Weight decay for each param.
        amsgrad: boolean. Whether to apply the AMSGrad variant of this
            algorithm from the paper "On the Convergence of Adam and
            Beyond".
        total_steps: int >= 0. Total number of training steps. Enable warmup by setting a positive value.
        warmup_proportion: 0 < warmup_proportion < 1. The proportion of increasing steps.
        min_lr: float >= 0. Minimum learning rate after warmup.
    # References
        - [Adam - A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980v8)
        - [On the Convergence of Adam and Beyond](https://openreview.net/forum?id=ryQu7f-RZ)
        - [On The Variance Of The Adaptive Learning Rate And Beyond](https://arxiv.org/pdf/1908.03265v1.pdf)
    """

    def __init__(self, lr=0.001, beta_1=0.9, beta_2=0.999,
                 epsilon=None, decay=0., weight_decay=0., amsgrad=False,
                 total_steps=0, warmup_proportion=0.1, min_lr=0., **kwargs):
        super(RAdam, self).__init__(**kwargs)
        with K.name_scope(self.__class__.__name__):
            self.iterations = K.variable(0, dtype='int64', name='iterations')
            self.lr = K.variable(lr, name='lr')
            self.beta_1 = K.variable(beta_1, name='beta_1')
            self.beta_2 = K.variable(beta_2, name='beta_2')
            self.decay = K.variable(decay, name='decay')
            self.weight_decay = K.variable(weight_decay, name='weight_decay')
            self.total_steps = K.variable(total_steps, name='total_steps')
            self.warmup_proportion = K.variable(warmup_proportion, name='warmup_proportion')
            self.min_lr = K.variable(min_lr, name='min_lr')
        if epsilon is None:
            epsilon = K.epsilon()
        self.epsilon = epsilon
        self.initial_decay = decay
        self.initial_weight_decay = weight_decay
        self.initial_total_steps = total_steps
        self.amsgrad = amsgrad

    def get_updates(self, loss, params):
        grads = self.get_gradients(loss, params)
        self.updates = [K.update_add(self.iterations, 1)]

        lr = self.lr

        if self.initial_decay > 0:
            lr = lr * (1. / (1. + self.decay * K.cast(self.iterations, K.dtype(self.decay))))

        t = K.cast(self.iterations, K.floatx()) + 1

        if self.initial_total_steps > 0:
            warmup_steps = self.total_steps * self.warmup_proportion
            lr = K.switch(
                t <= warmup_steps,
                lr * (t / warmup_steps),
                self.min_lr + (lr - self.min_lr) * (1.0 - K.minimum(t, self.total_steps) / self.total_steps),
            )

        ms = [K.zeros(K.int_shape(p), dtype=K.dtype(p), name='m_' + str(i)) for (i, p) in enumerate(params)]
        vs = [K.zeros(K.int_shape(p), dtype=K.dtype(p), name='v_' + str(i)) for (i, p) in enumerate(params)]

        if self.amsgrad:
            vhats = [K.zeros(K.int_shape(p), dtype=K.dtype(p), name='vhat_' + str(i)) for (i, p) in enumerate(params)]
        else:
            vhats = [K.zeros(1, name='vhat_' + str(i)) for i in range(len(params))]

        self.weights = [self.iterations] + ms + vs + vhats

        beta_1_t = K.pow(self.beta_1, t)
        beta_2_t = K.pow(self.beta_2, t)

        sma_inf = 2.0 / (1.0 - self.beta_2) - 1.0
        sma_t = sma_inf - 2.0 * t * beta_2_t / (1.0 - beta_2_t)

        for p, g, m, v, vhat in zip(params, grads, ms, vs, vhats):
            m_t = (self.beta_1 * m) + (1. - self.beta_1) * g
            v_t = (self.beta_2 * v) + (1. - self.beta_2) * K.square(g)

            m_corr_t = m_t / (1.0 - beta_1_t)
            if self.amsgrad:
                vhat_t = K.maximum(vhat, v_t)
                v_corr_t = K.sqrt(vhat_t / (1.0 - beta_2_t) + self.epsilon)
                self.updates.append(K.update(vhat, vhat_t))
            else:
                v_corr_t = K.sqrt(v_t / (1.0 - beta_2_t) + self.epsilon)

            r_t = K.sqrt((sma_t - 4.0) / (sma_inf - 4.0) *
                         (sma_t - 2.0) / (sma_inf - 2.0) *
                         sma_inf / sma_t)

            p_t = K.switch(sma_t >= 5, r_t * m_corr_t / v_corr_t, m_corr_t)

            if self.initial_weight_decay > 0:
                p_t += self.weight_decay * p

            p_t = p - lr * p_t

            self.updates.append(K.update(m, m_t))
            self.updates.append(K.update(v, v_t))
            new_p = p_t

            # Apply constraints.
            if getattr(p, 'constraint', None) is not None:
                new_p = p.constraint(new_p)

            self.updates.append(K.update(p, new_p))
        return self.updates

    def get_config(self):
        config = {
            'lr': float(K.get_value(self.lr)),
            'beta_1': float(K.get_value(self.beta_1)),
            'beta_2': float(K.get_value(self.beta_2)),
            'decay': float(K.get_value(self.decay)),
            'weight_decay': float(K.get_value(self.weight_decay)),
            'epsilon': self.epsilon,
            'amsgrad': self.amsgrad,
            'total_steps': float(K.get_value(self.total_steps)),
            'warmup_proportion': float(K.get_value(self.warmup_proportion)),
            'min_lr': float(K.get_value(self.min_lr)),
        }
        base_config = super(RAdam, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


# ## Loss function
# 
# Source for `bce_dice_loss`: https://lars76.github.io/neural-networks/object-detection/losses-for-segmentation/

# In[ ]:


def dice_coef(y_true, y_pred, smooth=1):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

def dice_loss(y_true, y_pred):
    smooth = 1.
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = y_true_f * y_pred_f
    score = (2. * K.sum(intersection) + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)
    return 1. - score

def bce_dice_loss(y_true, y_pred):
    return binary_crossentropy(y_true, y_pred) + dice_loss(y_true, y_pred)


# # Data Generator

# Unhide below for the definition of `DataGenerator`:

# In[ ]:


class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, df, target_df=None, mode='fit',
                 base_path='/kaggle/input/understanding_cloud_organization/train_images',
                 batch_size=32, dim=(1400, 2100), n_channels=1, reshape=None,
                 augment=False, n_classes=4, random_state=2019, shuffle=True):
        self.dim = dim
        self.batch_size = batch_size
        self.df = df
        self.mode = mode
        self.base_path = base_path
        self.target_df = target_df
        self.list_IDs = list_IDs
        self.reshape = reshape
        self.n_channels = n_channels
        self.augment = augment
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.random_state = random_state
        
        self.on_epoch_end()
        np.random.seed(self.random_state)
        
        
        ###
        self.imgs = {}
        keys = list_IDs
        
        for k in keys:
            im_name = self.df['ImageId'].iloc[k]
            img_path = f"{self.base_path}/{im_name}"
            if self.reshape is None:
                self.imgs[k] = self.__load_grayscale(img_path)
            else:
                self.imgs[k] = np_resize(self.__load_grayscale(img_path), self.reshape)
            
            self.imgs[k] = self.imgs[k].reshape((self.imgs[k].shape[0],self.imgs[k].shape[1],1))

        #
        
        self.masks = {}
        
        for k in keys:
            im_name = self.df['ImageId'].iloc[k]
            img_path = f"{self.base_path}/{im_name}"
            if self.reshape is None:
                self.imgs[k] = self.__load_grayscale(img_path)
            else:
                self.imgs[k] = np_resize(self.__load_grayscale(img_path), self.reshape)
                
            self.imgs[k] = self.imgs[k].reshape((self.imgs[k].shape[0],self.imgs[k].shape[1],1))
            
        for k in keys:
            im_name = self.df['ImageId'].iloc[k]
            image_df = self.target_df[self.target_df['ImageId'] == im_name]
            
            rles = image_df['EncodedPixels'].values
            
            if self.reshape is not None:
                masks = build_masks(rles, input_shape=self.dim, reshape=self.reshape)
            else:
                masks = build_masks(rles, input_shape=self.dim)
            
            self.masks[k] = masks

        #
        

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        list_IDs_batch = [self.list_IDs[k] for k in indexes]
        
        X = self.__generate_X(list_IDs_batch)
        
        if self.mode == 'fit':
            y = self.__generate_y(list_IDs_batch)
            
            if self.augment:
                X, y = self.__augment_batch(X, y)
            
            return X, y
        
        elif self.mode == 'predict':
            return X

        else:
            raise AttributeError('The mode parameter should be set to "fit" or "predict".')
        
    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.seed(self.random_state)
            np.random.shuffle(self.indexes)
    
    def __generate_X(self, list_IDs_batch):
        'Generates data containing batch_size samples'
        # Initialization
        if self.reshape is None:
            X = np.empty((self.batch_size, *self.dim, self.n_channels))
        else:
            X = np.empty((self.batch_size, *self.reshape, self.n_channels))
        
        # Generate data
        for i, ID in enumerate(list_IDs_batch):
            im_name = self.df['ImageId'].iloc[ID]
            img_path = f"{self.base_path}/{im_name}"
            img = self.imgs[ID]

            X[i,] = img

        return X
    
    def __generate_y(self, list_IDs_batch):
        if self.reshape is None:
            y = np.empty((self.batch_size, *self.dim, self.n_classes), dtype=int)
        else:
            y = np.empty((self.batch_size, *self.reshape, self.n_classes), dtype=int)
        
        for i, ID in enumerate(list_IDs_batch):
            
            y[i, ] = self.masks[ID]

        return y
    
    def __load_grayscale(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = img.astype(np.float32) / 255.
        img = np.expand_dims(img, axis=-1)

        return img
    
    def __load_rgb(self, img_path):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.

        return img
    
    def __random_transform(self, img, masks):
        composition = albu.Compose([
            albu.HorizontalFlip(),
            albu.VerticalFlip(),
            albu.ShiftScaleRotate(rotate_limit=45, shift_limit=0.15, scale_limit=0.15)
        ])
        
        composed = composition(image=img, mask=masks)
        aug_img = composed['image']
        aug_masks = composed['mask']
        
        return aug_img, aug_masks
    
    def __augment_batch(self, img_batch, masks_batch):
        for i in range(img_batch.shape[0]):
            img_batch[i, ], masks_batch[i, ] = self.__random_transform(
                img_batch[i, ], masks_batch[i, ])
        
        return img_batch, masks_batch
    
    def getitem(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        list_IDs_batch = [self.list_IDs[k] for k in indexes]
        
        X = self.__generate_X(list_IDs_batch)
        
        if self.mode == 'fit':
            y = self.__generate_y(list_IDs_batch)
            
            if self.augment:
                X, y = self.__augment_batch(X, y)
            
            return X, y
        
        elif self.mode == 'predict':
            return X

        else:
            raise AttributeError('The mode parameter should be set to "fit" or "predict".')


# # Model Architecture

# ** Vanilla Unet**

# In[ ]:


def vanilla_unet(input_shape):

    inputs = Input(input_shape)
    c1 = Conv2D(8, (3, 3), activation='elu', padding='same') (inputs)
    c1 = Conv2D(8, (3, 3), activation='elu', padding='same') (c1)
    p1 = MaxPooling2D((2, 2), padding='same') (c1)

    c2 = Conv2D(16, (3, 3), activation='elu', padding='same') (p1)
    c2 = Conv2D(16, (3, 3), activation='elu', padding='same') (c2)
    p2 = MaxPooling2D((2, 2), padding='same') (c2)

    c3 = Conv2D(32, (3, 3), activation='elu', padding='same') (p2)
    c3 = Conv2D(32, (3, 3), activation='elu', padding='same') (c3)
    p3 = MaxPooling2D((2, 2), padding='same') (c3)

    c4 = Conv2D(64, (3, 3), activation='elu', padding='same') (p3)
    c4 = Conv2D(64, (3, 3), activation='elu', padding='same') (c4)
    p4 = MaxPooling2D((2, 2), padding='same') (c4)

    c5 = Conv2D(64, (3, 3), activation='elu', padding='same') (p4)
    c5 = Conv2D(64, (3, 3), activation='elu', padding='same') (c5)
    p5 = MaxPooling2D((2, 2), padding='same') (c5)

    c55 = Conv2D(128, (3, 3), activation='elu', padding='same') (p5)
    c55 = Conv2D(128, (3, 3), activation='elu', padding='same') (c55)

    u6 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same') (c55)
    u6 = concatenate([u6, c5])
    c6 = Conv2D(64, (3, 3), activation='elu', padding='same') (u6)
    c6 = Conv2D(64, (3, 3), activation='elu', padding='same') (c6)

    u71 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same') (c6)
    u71 = concatenate([u71, c4])
    c71 = Conv2D(32, (3, 3), activation='elu', padding='same') (u71)
    c61 = Conv2D(32, (3, 3), activation='elu', padding='same') (c71)

    u7 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same') (c61)
    u7 = concatenate([u7, c3])
    c7 = Conv2D(32, (3, 3), activation='elu', padding='same') (u7)
    c7 = Conv2D(32, (3, 3), activation='elu', padding='same') (c7)

    u8 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same') (c7)
    u8 = concatenate([u8, c2])
    c8 = Conv2D(16, (3, 3), activation='elu', padding='same') (u8)
    c8 = Conv2D(16, (3, 3), activation='elu', padding='same') (c8)

    u9 = Conv2DTranspose(8, (2, 2), strides=(2, 2), padding='same') (c8)
    u9 = concatenate([u9, c1], axis=3)
    c9 = Conv2D(8, (3, 3), activation='elu', padding='same') (u9)
    c9 = Conv2D(8, (3, 3), activation='elu', padding='same') (c9)

    outputs = Conv2D(4, (1, 1), activation='sigmoid') (c9)

    model = Model(inputs=[inputs], outputs=[outputs])
    
    return model


# **Vanilla with dropout:** dropout can be adjusted

# In[ ]:


def vanilla_unet_dropout(input_shape, dropout):

    inputs = Input(input_shape)
    c1 = Conv2D(8, (3, 3), activation='elu', padding='same') (inputs)
    c1 = Dropout(dropout)(c1)
    c1 = Conv2D(8, (3, 3), activation='elu', padding='same') (c1)
    p1 = MaxPooling2D((2, 2), padding='same') (c1)

    c2 = Conv2D(16, (3, 3), activation='elu', padding='same') (p1)
    c2 = Dropout(dropout)(c2)

    c2 = Conv2D(16, (3, 3), activation='elu', padding='same') (c2)
    p2 = MaxPooling2D((2, 2), padding='same') (c2)

    c3 = Conv2D(32, (3, 3), activation='elu', padding='same') (p2)
    c3 = Dropout(dropout)(c3)
    c3 = Conv2D(32, (3, 3), activation='elu', padding='same') (c3)
    p3 = MaxPooling2D((2, 2), padding='same') (c3)

    c4 = Conv2D(64, (3, 3), activation='elu', padding='same') (p3)
    c4 = Dropout(dropout)(c4)
    c4 = Conv2D(64, (3, 3), activation='elu', padding='same') (c4)
    p4 = MaxPooling2D((2, 2), padding='same') (c4)

    c5 = Conv2D(64, (3, 3), activation='elu', padding='same') (p4)
    c5 = Conv2D(64, (3, 3), activation='elu', padding='same') (c5)
    p5 = MaxPooling2D((2, 2), padding='same') (c5)

    c55 = Conv2D(128, (3, 3), activation='elu', padding='same') (p5)
    c55 = Conv2D(128, (3, 3), activation='elu', padding='same') (c55)

    u6 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same') (c55)
    u6 = concatenate([u6, c5])
    c6 = Conv2D(64, (3, 3), activation='elu', padding='same') (u6)
    c6 = Dropout(dropout)(c6)
    c6 = Conv2D(64, (3, 3), activation='elu', padding='same') (c6)

    u71 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same') (c6)
    u71 = concatenate([u71, c4])
    c71 = Conv2D(32, (3, 3), activation='elu', padding='same') (u71)
    c61 = Conv2D(32, (3, 3), activation='elu', padding='same') (c71)

    u7 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same') (c61)
    u7 = concatenate([u7, c3])
    c7 = Conv2D(32, (3, 3), activation='elu', padding='same') (u7)
    c7 = Dropout(dropout)(c7)
    c7 = Conv2D(32, (3, 3), activation='elu', padding='same') (c7)

    u8 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same') (c7)
    u8 = concatenate([u8, c2])
    c8 = Conv2D(16, (3, 3), activation='elu', padding='same') (u8)
    c8 = Dropout(dropout)(c8)
    c8 = Conv2D(16, (3, 3), activation='elu', padding='same') (c8)

    u9 = Conv2DTranspose(8, (2, 2), strides=(2, 2), padding='same') (c8)
    u9 = concatenate([u9, c1], axis=3)
    c9 = Conv2D(8, (3, 3), activation='elu', padding='same') (u9)
    c9 = Dropout(dropout)(c9)
    c9 = Conv2D(8, (3, 3), activation='elu', padding='same') (c9)

    outputs = Conv2D(4, (1, 1), activation='sigmoid') (c9)

    model = Model(inputs=[inputs], outputs=[outputs])
    
    return model


# # Load dataset

# In[ ]:


get_ipython().run_cell_magic('time', '', 'BATCH_SIZE = 16\nSUFFLE = True\nAUGMENT = True\n\ntrain_idx, val_idx = train_test_split(\n    mask_count_df.index, random_state=2019, test_size=0.2\n)\ntrain_generator = DataGenerator(\n    train_idx, \n    df=mask_count_df,\n    target_df=train_df,\n    batch_size=BATCH_SIZE,\n    reshape=(128, 128),\n    augment=AUGMENT,\n    shuffle=SUFFLE,\n    n_channels=1,\n    n_classes=4\n)\nprint("Train generator load")\n\nval_generator = DataGenerator(\n    val_idx, \n    df=mask_count_df,\n    target_df=train_df,\n    batch_size=BATCH_SIZE, \n    reshape=(128, 128),\n    augment=False,\n    shuffle=SUFFLE,\n    n_channels=1,\n    n_classes=4,\n\n)\nprint("Validation generator load")\n\ncheck_generator = DataGenerator(\n    #val_idx[0:10],\n    val_idx,\n    df=mask_count_df, \n    target_df=train_df,\n    #mode=\'predict\',\n    shuffle=False,\n    reshape=(128, 128),\n    augment=False,\n    n_channels=1,\n    n_classes=4,\n    batch_size=1,\n)\nprint("Check generator load")')


# Unhide below for summary of model architecture.

# # Training and evaluation of Unet no Dropout

# In[ ]:


model = vanilla_unet((128, 128,1))

model.compile(optimizer=Nadam(lr=0.0002), loss=bce_dice_loss, metrics=[dice_coef])
model.summary()


# In[ ]:


get_ipython().run_cell_magic('time', '', "checkpoint = ModelCheckpoint('model_0.h5', save_best_only=True)\n\nhistory0 = model.fit_generator(\n    train_generator,\n    validation_data=val_generator,\n    callbacks=[checkpoint],\n    epochs=100\n)")


# In[ ]:


with open('history_0.json', 'w') as f:
    json.dump(str(history0.history), f)

history_df = pd.DataFrame(history0.history)
history_df[['loss', 'val_loss']].plot()
history_df[['dice_coef', 'val_dice_coef']].plot()


# In[ ]:


model.load_weights('model_0.h5')

batch_pred_masks = model.predict_generator(
    check_generator, 
    workers=1,
    verbose=1
)

    
    


# Images of results for the first 10 images in validation set

# In[ ]:


for i in range(4):
    visualize(check_generator.getitem(i)[0][0,:,:,:],check_generator.getitem(i)[1][0,:,:,:],batch_pred_masks[i])


# In[ ]:


#evaluation
evaluation = model.evaluate_generator(
    check_generator, 
    workers=1,
    verbose=1
)
evaluation0 = evaluation
print(f"Best val loss: {evaluation[0]:.3f} dice : {evaluation[1]:.3f}")


# # Results

# A threshold of 0,5 is aplied to the output of the network pixel by pixel.
# Then result is compared with the ground truth 

# In[ ]:


dice_label_result = np.zeros((len(batch_pred_masks),4))
k = 1
n_labeles_gt = np.array([0,0,0,0])
for i in range(len(batch_pred_masks)):
    for l in range(4):
        a = batch_pred_masks[i][:,:,l]
        a[a>=0.5] = 1
        a[a<0.5] = 0
        a = a.astype(int)
        b = check_generator.getitem(i)[1][0,:,:,l]
        
        dice_label_result[i,l] = np.sum(a[b==k])*2.0 / (np.sum(a) + np.sum(b))
        
        #count labels in ground truth
        if check_generator.getitem(i)[1][0,:,:,l].max() == 1:
            n_labeles_gt[l] = n_labeles_gt[l]+1
            


# In[ ]:


l0 = len(dice_label_result[dice_label_result[:,0] > 0.5])/n_labeles_gt[0]
l1 = len(dice_label_result[dice_label_result[:,1] > 0.5])/n_labeles_gt[1]
l2 = len(dice_label_result[dice_label_result[:,2] > 0.5])/n_labeles_gt[2]
l3 = len(dice_label_result[dice_label_result[:,3] > 0.5])/n_labeles_gt[3]

label_name = ("Fish","Flower","Gravel","Sugar")
y_pos = np.arange(len(label_name))
labels = [l0,l1,l2,l3]

plt.bar(y_pos, labels, align='center', alpha=0.5)
plt.xticks(y_pos, label_name)
plt.ylabel('% of hits')
plt.title('% of outputs match ground truth dice 0.5')

plt.show()


# # Fish detected

# In[ ]:


label_name = ("Fish","Flower","Gravel","Sugar")
for i in range (100):
    if(dice_label_result[i,0] >0.7):
        visualize(check_generator.getitem(i)[0][0,:,:,:],check_generator.getitem(i)[1][0,:,:,:],batch_pred_masks[i])
        break
        


# # Fish false positive
# 

# In[ ]:


for i in range (100):
    if(dice_label_result[i,0] < 0.3):
        visualize(check_generator.getitem(i)[0][0,:,:,:],check_generator.getitem(i)[1][0,:,:,:],batch_pred_masks[i])
        break


# # Flower detected

# In[ ]:


for i in range (100):
    if(dice_label_result[i,1] >0.7):
        visualize(check_generator.getitem(i)[0][0,:,:,:],check_generator.getitem(i)[1][0,:,:,:],batch_pred_masks[i])
        break


# # Flower false positive

# In[ ]:


for i in range (100):
    if(dice_label_result[i,1] < 0.3) and (dice_label_result[i,1] != 0):
        visualize(check_generator.getitem(i)[0][0,:,:,:],check_generator.getitem(i)[1][0,:,:,:],batch_pred_masks[i])
        break


# # Gravel detectd

# In[ ]:


for i in range (100):
    if(dice_label_result[i,2] >0.7):
        visualize(check_generator.getitem(i)[0][0,:,:,:],check_generator.getitem(i)[1][0,:,:,:],batch_pred_masks[i])
        break


# # Gravel false positive

# In[ ]:


for i in range (100):
    if(dice_label_result[i,2] < 0.3) and (dice_label_result[i,2] != 0):
        visualize(check_generator.getitem(i)[0][0,:,:,:],check_generator.getitem(i)[1][0,:,:,:],batch_pred_masks[i])
        break


# # Sugar detected

# In[ ]:


for i in range (100):
    if(dice_label_result[i,3] >0.7):
        visualize(check_generator.getitem(i)[0][0,:,:,:],check_generator.getitem(i)[1][0,:,:,:],batch_pred_masks[i])
        break


# # Sugar false positive

# In[ ]:


for i in range (500):
    if(dice_label_result[i,3] < 0.3) and (dice_label_result[i,3] != 0):
        visualize(check_generator.getitem(i)[0][0,:,:,:],check_generator.getitem(i)[1][0,:,:,:],batch_pred_masks[i])
        break


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




