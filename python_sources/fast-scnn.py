#!/usr/bin/env python
# coding: utf-8

# # About this kernel
# 
# * **Preprocessing**: Discard all of the training data that have all 4 masks missing. We will only train on images that have at least 1 mask, so that our classifier does not overfit on empty masks.
# * **Step 1 - Discard Images**: Use the DenseNet classifier trained in [this kernel](https://www.kaggle.com/xhlulu/severstal-steel-predict-missing-masks) to predict all of the test images that will have all 4 masks missing. We will automatically set the RLEs of those images to null.
# * **Step 2 - U-Net**: Train the same model from [Simple Keras U-Net Boilerplate](https://www.kaggle.com/xhlulu/severstal-simple-keras-u-net-boilerplate) on the "filtered" training data. Then, perform inference only on test images that were not discarded in step 1.
# * **Submission**: We will now combine the dataframe containing the discarded test images with the dataframe containing test images predicted in step 2, and submit everything.
# 
# 
# ## Changelog
# * V8: Changed sign of the `missing_model` threshold, since we are only keeping the ones with low probability of having no defect.
# * V9: Fixed import for the discarding CNNs, which was updated to DenseNet.
# 
# 
# ## References
# * Data generator: https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly
# * RLE encoding and decoding: https://www.kaggle.com/paulorzp/rle-functions-run-lenght-encode-decode
# * Architecture: https://www.kaggle.com/jesperdramsch/intro-chest-xray-dicom-viz-u-nets-full-data
# * Mask encoding: https://www.kaggle.com/c/siim-acr-pneumothorax-segmentation/data
# * Step 1 Original Kernel: https://www.kaggle.com/xhlulu/severstal-steel-predict-missing-masks
# * Step 2 Original Kernel: https://www.kaggle.com/xhlulu/severstal-simple-keras-u-net-boilerplate

# In[ ]:


import os
import json
import gc

import cv2
import keras
from keras import backend as K
from keras import layers
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model, load_model
from keras.layers import Input
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate
from keras.optimizers import Adam
# from tf.keras.callbacks import Callback, ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.callbacks import Callback, ModelCheckpoint


# # Preprocessing

# In[ ]:


train_df = pd.read_csv('../input/severstal-steel-defect-detection/train.csv')
train_df['ImageId'] = train_df['ImageId_ClassId'].apply(lambda x: x.split('_')[0])
train_df['ClassId'] = train_df['ImageId_ClassId'].apply(lambda x: x.split('_')[1])
train_df['hasMask'] = ~ train_df['EncodedPixels'].isna()

print(train_df.shape)
train_df.head()


# In[ ]:


mask_count_df = train_df.groupby('ImageId').agg(np.sum).reset_index()
mask_count_df.sort_values('hasMask', ascending=False, inplace=True)
print(mask_count_df.shape)
mask_count_df.head()


# In[ ]:


sub_df = pd.read_csv('../input/severstal-steel-defect-detection/sample_submission.csv')
sub_df['ImageId'] = sub_df['ImageId_ClassId'].apply(lambda x: x.split('_')[0])
test_imgs = pd.DataFrame(sub_df['ImageId'].unique(), columns=['ImageId'])
test_imgs.head()


# In[ ]:


non_missing_train_idx = mask_count_df[mask_count_df['hasMask'] > 0]
non_missing_train_idx.head()


# # Step 1: Remove test images without defects
# 
# Most of the stuff below is hidden, since it's copied from my previous kernels.

# In[ ]:


def load_img(code, base, resize=True):
    path = f'{base}/{code}'
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if resize:
        img = cv2.resize(img, (256, 256))
    
    return img

def validate_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


# In[ ]:


BATCH_SIZE = 64
def create_test_gen():
    return ImageDataGenerator(rescale=1/255.).flow_from_dataframe(
        test_imgs,
        directory='../input/severstal-steel-defect-detection/test_images',
        x_col='ImageId',
        class_mode=None,
        target_size=(256, 256),
        batch_size=BATCH_SIZE,
        shuffle=False
    )

test_gen = create_test_gen()


# In[ ]:


remove_model = load_model('../input/severstal-predict-missing-masks/model.h5')
remove_model.summary()


# Beware: Messy code below!

# In[ ]:


test_missing_pred = remove_model.predict_generator(
    test_gen,
    steps=len(test_gen),
    verbose=1
)

test_imgs['allMissing'] = test_missing_pred
test_imgs.head()


# In[ ]:


filtered_test_imgs = test_imgs[test_imgs['allMissing'] < 0.5]
print(filtered_test_imgs.shape)
filtered_test_imgs.head()


# `filtered_sub_df` contains all of the images with at least one mask. `null_sub_df` contains all the images with exactly 4 missing masks.

# In[ ]:


filtered_mask = sub_df['ImageId'].isin(filtered_test_imgs["ImageId"].values)
filtered_sub_df = sub_df[filtered_mask].copy()
null_sub_df = sub_df[~filtered_mask].copy()
null_sub_df['EncodedPixels'] = null_sub_df['EncodedPixels'].apply(
    lambda x: ' ')

filtered_sub_df.reset_index(drop=True, inplace=True)
filtered_test_imgs.reset_index(drop=True, inplace=True)

print(filtered_sub_df.shape)
print(null_sub_df.shape)

filtered_sub_df.head()


# # Step 2: Keras U-Net
# 
# Most of the stuff below is hidden, since it's copied from my previous kernels.

# ## Utility Functions

# In[ ]:


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

def build_masks(rles, input_shape):
    depth = len(rles)
    masks = np.zeros((*input_shape, depth))
    
    for i, rle in enumerate(rles):
        if type(rle) is str:
            masks[:, :, i] = rle2mask(rle, input_shape)
    
    return masks

def build_rles(masks):
    width, height, depth = masks.shape
    
    rles = [mask2rle(masks[:, :, i])
            for i in range(depth)]
    
    return rles


# ## Data Generator

# In[ ]:


class DataGenerator(tf.keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, df, target_df=None, mode='fit',
                 base_path='../input/severstal-steel-defect-detection/train_images',
                 batch_size=32, dim=(256, 1600), n_channels=1,
                 n_classes=4, random_state=2019, shuffle=True):
        self.dim = dim
        self.batch_size = batch_size
        self.df = df
        self.mode = mode
        self.base_path = base_path
        self.target_df = target_df
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.random_state = random_state
        
        self.on_epoch_end()

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
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        
        # Generate data
        for i, ID in enumerate(list_IDs_batch):
            im_name = self.df['ImageId'].iloc[ID]
            img_path = f"{self.base_path}/{im_name}"
            img = self.__load_grayscale(img_path)
            
            # Store samples
            X[i,] = img

        return X
    
    def __generate_y(self, list_IDs_batch):
        y = np.empty((self.batch_size, *self.dim, self.n_classes), dtype=int)
        
        for i, ID in enumerate(list_IDs_batch):
            im_name = self.df['ImageId'].iloc[ID]
            image_df = self.target_df[self.target_df['ImageId'] == im_name]
            
            rles = image_df['EncodedPixels'].values
            masks = build_masks(rles, input_shape=self.dim)
            
            y[i, ] = masks

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


# In[ ]:


BATCH_SIZE = 16

train_idx, val_idx = train_test_split(
    non_missing_train_idx.index,  # NOTICE DIFFERENCE
    random_state=2019, 
    test_size=0.15
)

train_generator = DataGenerator(
    train_idx, 
    df=mask_count_df,
    target_df=train_df,
    batch_size=BATCH_SIZE, 
    n_classes=4
)

val_generator = DataGenerator(
    val_idx, 
    df=mask_count_df,
    target_df=train_df,
    batch_size=BATCH_SIZE, 
    n_classes=4
)


# ## Model

# In[ ]:


def dice_coef(y_true, y_pred, smooth=1):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


# In[ ]:


# def build_model(input_shape):
#     inputs = Input(input_shape)

#     c1 = Conv2D(8, (3, 3), activation='relu', padding='same') (inputs)
#     c1 = Conv2D(8, (3, 3), activation='relu', padding='same') (c1)
#     p1 = MaxPooling2D((2, 2)) (c1)

#     c2 = Conv2D(16, (3, 3), activation='relu', padding='same') (p1)
#     c2 = Conv2D(16, (3, 3), activation='relu', padding='same') (c2)
#     p2 = MaxPooling2D((2, 2)) (c2)

#     c3 = Conv2D(32, (3, 3), activation='relu', padding='same') (p2)
#     c3 = Conv2D(32, (3, 3), activation='relu', padding='same') (c3)
#     p3 = MaxPooling2D((2, 2)) (c3)

#     c4 = Conv2D(64, (3, 3), activation='relu', padding='same') (p3)
#     c4 = Conv2D(64, (3, 3), activation='relu', padding='same') (c4)
#     p4 = MaxPooling2D(pool_size=(2, 2)) (c4)

#     c5 = Conv2D(64, (3, 3), activation='relu', padding='same') (p4)
#     c5 = Conv2D(64, (3, 3), activation='relu', padding='same') (c5)
#     p5 = MaxPooling2D(pool_size=(2, 2)) (c5)

#     c55 = Conv2D(128, (3, 3), activation='relu', padding='same') (p5)
#     c55 = Conv2D(128, (3, 3), activation='relu', padding='same') (c55)

#     u6 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same') (c55)
#     u6 = concatenate([u6, c5])
#     c6 = Conv2D(64, (3, 3), activation='relu', padding='same') (u6)
#     c6 = Conv2D(64, (3, 3), activation='relu', padding='same') (c6)

#     u71 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same') (c6)
#     u71 = concatenate([u71, c4])
#     c71 = Conv2D(32, (3, 3), activation='relu', padding='same') (u71)
#     c61 = Conv2D(32, (3, 3), activation='relu', padding='same') (c71)

#     u7 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same') (c61)
#     u7 = concatenate([u7, c3])
#     c7 = Conv2D(32, (3, 3), activation='relu', padding='same') (u7)
#     c7 = Conv2D(32, (3, 3), activation='relu', padding='same') (c7)

#     u8 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same') (c7)
#     u8 = concatenate([u8, c2])
#     c8 = Conv2D(16, (3, 3), activation='relu', padding='same') (u8)
#     c8 = Conv2D(16, (3, 3), activation='relu', padding='same') (c8)

#     u9 = Conv2DTranspose(8, (2, 2), strides=(2, 2), padding='same') (c8)
#     u9 = concatenate([u9, c1], axis=3)
#     c9 = Conv2D(8, (3, 3), activation='relu', padding='same') (u9)
#     c9 = Conv2D(8, (3, 3), activation='relu', padding='same') (c9)

#     outputs = Conv2D(4, (1, 1), activation='sigmoid') (c9)

#     model = Model(inputs=[inputs], outputs=[outputs])
#     model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[dice_coef])
    
#     return model


# In[ ]:


def conv_block(inputs, conv_type, kernel, kernel_size, strides, padding='same', relu=True):
    if(conv_type == 'ds'):
        x = tf.keras.layers.SeparableConv2D(kernel, kernel_size, padding=padding, strides = strides)(inputs)
    else:
        x = tf.keras.layers.Conv2D(kernel, kernel_size, padding=padding, strides = strides)(inputs)  
  
    x = tf.keras.layers.BatchNormalization()(x)
  
    if (relu):
        x = tf.keras.activations.relu(x)
  
    return x

# Input Layer
num_classes=4
input_layer = tf.keras.layers.Input(shape=(256, 1600, 1), name = 'input_layer')

lds_layer = conv_block(input_layer, 'conv', 32, (3, 3), strides = (2, 2))
lds_layer = conv_block(lds_layer, 'ds', 48, (3, 3), strides = (2, 2))
lds_layer = conv_block(lds_layer, 'ds', 64, (3, 3), strides = (2, 2))

def _res_bottleneck(inputs, filters, kernel, t, s, r=False):
    
    
    tchannel = tf.keras.backend.int_shape(inputs)[-1] * t

    x = conv_block(inputs, 'conv', tchannel, (1, 1), strides=(1, 1))

    x = tf.keras.layers.DepthwiseConv2D(kernel, strides=(s, s), depth_multiplier=1, padding='same')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.activations.relu(x)

    x = conv_block(x, 'conv', filters, (1, 1), strides=(1, 1), padding='same', relu=False)

    if r:
        x = tf.keras.layers.add([x, inputs])
    return x

def bottleneck_block(inputs, filters, kernel, t, strides, n):
    x = _res_bottleneck(inputs, filters, kernel, t, strides)
  
    for i in range(1, n):
        x = _res_bottleneck(x, filters, kernel, t, 1, True)

    return x

def pyramid_pooling_block(input_tensor, bin_sizes):
    concat_list = [input_tensor]
    w = 8
    h = 50

    for bin_size in bin_sizes:
        x = tf.keras.layers.AveragePooling2D()(input_tensor)
        x = tf.keras.layers.Conv2D(128, 3, 2, padding='same')(input_tensor)
        x = tf.keras.layers.Lambda(lambda x: tf.image.resize(x, (w,h)))(x)
#         print(x.shape)

        concat_list.append(x)
    print("abccc:",concat_list)

    return tf.keras.layers.concatenate(concat_list)

gfe_layer = bottleneck_block(lds_layer, 64, (3, 3), t=6, strides=2, n=3)
gfe_layer = bottleneck_block(gfe_layer, 96, (3, 3), t=6, strides=2, n=3)
gfe_layer = bottleneck_block(gfe_layer, 128, (3, 3), t=6, strides=1, n=3)
gfe_layer = pyramid_pooling_block(gfe_layer, [2,4,6,8])

ff_layer1 = conv_block(lds_layer, 'conv', 128, (1,1), padding='same', strides= (1,1), relu=False)

ff_layer2 = tf.keras.layers.UpSampling2D((4, 4))(gfe_layer)
ff_layer2 = tf.keras.layers.DepthwiseConv2D((3,3), strides=(1, 1), depth_multiplier=1, padding='same')(ff_layer2)
ff_layer2 = tf.keras.layers.BatchNormalization()(ff_layer2)
ff_layer2 = tf.keras.activations.relu(ff_layer2)
ff_layer2 = tf.keras.layers.Conv2D(128, 1, 1, padding='same', activation=None)(ff_layer2)

ff_final = tf.keras.layers.add([ff_layer1, ff_layer2])
ff_final = tf.keras.layers.BatchNormalization()(ff_final)
ff_final = tf.keras.activations.relu(ff_final)

classifier = tf.keras.layers.SeparableConv2D(128, (3, 3), padding='same', strides = (1, 1), name = 'DSConv1_classifier')(ff_final)
classifier = tf.keras.layers.BatchNormalization()(classifier)
classifier = tf.keras.activations.relu(classifier)

classifier = tf.keras.layers.SeparableConv2D(128, (3, 3), padding='same', strides = (1, 1), name = 'DSConv2_classifier')(classifier)
classifier = tf.keras.layers.BatchNormalization()(classifier)
classifier = tf.keras.activations.relu(classifier)


classifier = conv_block(classifier, 'conv', num_classes, (1, 1), strides=(1, 1), padding='same', relu=False)

classifier = tf.keras.layers.Dropout(0.3)(classifier)

classifier = tf.keras.layers.UpSampling2D((8, 8))(classifier)
classifier = tf.keras.activations.softmax(classifier)

fast_scnn = tf.keras.Model(inputs = input_layer , outputs = classifier, name = 'Fast_SCNN')
optimizer = tf.keras.optimizers.SGD(lr=0.001)
fast_scnn.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=[dice_coef])


# In[ ]:


# model = build_model((256, 1600, 1))
# model.summary()


# In[ ]:


fast_scnn.summary()


# In[ ]:


# checkpoint = ModelCheckpoint(
#     'model.h5', 
#     monitor='val_loss', 
#     verbose=0, 
#     save_best_only=True, 
#     save_weights_only=False,
#     mode='auto'
# )

history = fast_scnn.fit_generator(
    train_generator,
    validation_data=val_generator,
    use_multiprocessing=False,
    workers=1,
    epochs=10
)


# In[ ]:


# fast_scnn.save("model.h5")


# In[ ]:


# history = fast_scnn.fit_generator(
#     train_generator,
#     validation_data=val_generator,
#     use_multiprocessing=False,
#     workers=1,
#     epochs=20
# )


# In[ ]:


img=cv2.imread("../input/severstal-steel-defect-detection/train_images/ac2b13f3f.jpg",0)
img=img.reshape((1,256,1600,1))
a=fast_scnn.predict(img)
d=build_masks(a,(256,1600))
d=d.reshape((256,1600))


# In[ ]:


import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# In[ ]:


imgplot = plt.imshow(d)


# ## Evaluation

# In[ ]:


# with open('history.json', 'w') as f:
#     json.dump(history.history, f)

# history_df = pd.DataFrame(history.history)
# history_df[['loss', 'val_loss']].plot()
# history_df[['dice_coef', 'val_dice_coef']].plot()


# ## Predict masks on non-discarded images

# In[ ]:


# fast_scnn.load_weights('model.h5')
test_df = []

for i in range(0, filtered_test_imgs.shape[0], 300):
    batch_idx = list(
        range(i, min(filtered_test_imgs.shape[0], i + 300))
    )
    
    test_generator = DataGenerator(
        batch_idx,
        df=filtered_test_imgs,
        shuffle=False,
        mode='predict',
        base_path='../input/severstal-steel-defect-detection/test_images',
        target_df=filtered_sub_df,
        batch_size=1,
        n_classes=4
    )
    
    batch_pred_masks = fast_scnn.predict_generator(
        test_generator, 
        workers=1,
        verbose=1,
        use_multiprocessing=False
    )
    
    for j, b in tqdm(enumerate(batch_idx)):
        filename = filtered_test_imgs['ImageId'].iloc[b]
        image_df = filtered_sub_df[filtered_sub_df['ImageId'] == filename].copy()
        
        pred_masks = batch_pred_masks[j, ].round().astype(int)
        pred_rles = build_rles(pred_masks)
        
        image_df['EncodedPixels'] = pred_rles
        test_df.append(image_df)
        
    gc.collect()


# # Submission

# In[ ]:


test_df = pd.concat(test_df)
print(test_df.shape)
test_df.head()


# Now, we combine results from the predicted masks with the rest of images that our first CNN classified as having all 4 masks missing.

# In[ ]:


final_submission_df = pd.concat([test_df, null_sub_df])
print(final_submission_df.shape)
final_submission_df.head()


# In[ ]:


final_submission_df[['ImageId_ClassId', 'EncodedPixels']].to_csv('submission.csv', index=False)


# In[ ]:


# os.listdir() 


# In[ ]:




