#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os


# In[ ]:


import keras.backend as K


# ### Loss Function - Quadratic Weighted Kappa
# 

# In[ ]:


def quadratic_kappa_coefficient(y_true, y_pred):
    y_true = K.cast(y_true, "float32")
    n_classes = K.cast(y_pred.shape[-1], "float32")
    weights = K.arange(0, n_classes, dtype="float32") / (n_classes - 1)
    weights = (weights - K.expand_dims(weights, -1)) ** 2

    hist_true = K.sum(y_true, axis=0)
    hist_pred = K.sum(y_pred, axis=0)

    E = K.expand_dims(hist_true, axis=-1) * hist_pred
    E = E / K.sum(E, keepdims=False)

    O = K.transpose(K.transpose(y_true) @ y_pred)  # confusion matrix
    O = O / K.sum(O)

    num = weights * O
    den = weights * E

    QWK = (1 - K.sum(num) / K.sum(den))
    return QWK

def quadratic_kappa_loss(scale=2.0):
    def _quadratic_kappa_loss(y_true, y_pred):
        QWK = quadratic_kappa_coefficient(y_true, y_pred)
        loss = -K.log(K.sigmoid(scale * QWK))
        return loss
        
    return _quadratic_kappa_loss


# ### Build the model
# 
# Perform transfer learning from VGG16 with imagenet weights. 
# In order to load the weights and use it without activating the internet, in the notebook, go to "Data" -> "Add data" and search "keras" then select "Keras Pretrained Models".
# 
# Freeze the conv layers and only train the top layers.

# In[ ]:


from keras.applications.vgg16 import VGG16
from keras import models, Model
from keras.layers import Input,Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy


# In[ ]:


input_shape = (256, 256, 3)

base_net = VGG16(weights='../input/keras-pretrained-models/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5', include_top=False, input_shape=input_shape)
for layer in base_net.layers:
    layer.trainable = False


# We choose a softmax activation on the last layer because our classes are mutually exclusive. We want the algorithm to choose only one class, the one with the highest probability, therefore the probabilities must sum up to 1. 
# 
# (in contrast, the sigmoid activation function will output independent probabilities and can be used when Eg. a patient might have multiple diseases - the output might be multiple classes)

# In[ ]:


model = models.Sequential()
model.add(base_net)

model.add(Flatten())
model.add(Dense(256, activation = "relu"))
model.add(Dropout(0.5))
model.add(Dense(6, activation = "softmax"))
model.summary()


# In[ ]:


model = Model(inputs = model.input, outputs = model.output)


# In[ ]:


#loss = categorical_crossentropy,
model.compile(optimizer = Adam(lr=1e-3), loss = quadratic_kappa_loss(scale=6.0),              metrics = ['accuracy',quadratic_kappa_coefficient])


# ### Create a data generator
# 
# 1. Create a DF which contains the image path + the label of that image. We will not use the masks at all at this stage.
# 2. Use the 3rd version o the data (smallest size array) to speed up the process
# 3. Create a labels array (Y) and a data array (X)
# 4. Split the data in train & validation (use validation to also test at this stage)

# In[ ]:


from pathlib import Path
import pandas as pd
import numpy as np
import skimage.io
import cv2

import random
from sklearn.model_selection import train_test_split
from keras.callbacks.callbacks import ModelCheckpoint, EarlyStopping

from sklearn.preprocessing import OneHotEncoder

from matplotlib.pyplot import imshow


# In[ ]:


HOME = Path("../input/prostate-cancer-grade-assessment")
TRAIN = Path("train_images")


# In[ ]:


train_ann = pd.read_csv(HOME/'train.csv')
train_ann['image_path'] = [str(HOME/TRAIN/image_name) + ".tiff"                            for image_name in train_ann['image_id']]
train_ann.head()


# ### Data Encoder for the labels
# 
# ... as we need them to be represented as dummy variables. Each response will be an array of length 6. Eg. class 3 will be represented as [0,0,0,1,0,0]

# In[ ]:


enc = OneHotEncoder(handle_unknown = 'ignore')


# In[ ]:


enc_labels = pd.DataFrame(enc.fit_transform(train_ann[['isup_grade']]).toarray())

train_ann = pd.merge(train_ann, enc_labels, left_index=True, right_index=True)
train_ann.head(8)


# ### Data Generator
# 
# - First of all, take either train of val pandaDF. 
# - Shuffle the rows and randomly select a number, equal to your batch size.
# - Read the selected images (from the path column) and resize them in get_image()
# - Output the data array as well as the labels corresponding to that data.

# In[ ]:


# Function to get one image

def get_image(image_location):
    image = skimage.io.MultiImage(image_location)
    # take the smallest image size
    image = image[-1]
    # resize the image to the desired size
    image = cv2.resize(image, (input_shape[0], input_shape[1]))
    
    return image


# In[ ]:


# Function that shuffles annotation rows and chooses batch_size samples
#sequence = range(len(annotation_file))

def get_batch_ids(sequence, batch_size):
    sequence = list(sequence)
    random.shuffle(sequence)
    batch = random.sample(sequence, batch_size)
    return batch


# In[ ]:


# Basic data generator -> Next: add augmentation = False

def data_generator(data, batch_size):
    while True:
        data = data.reset_index(drop=True)
        indices = list(data.index)

        batch_ids = get_batch_ids(indices, batch_size)
        batch = data.iloc[batch_ids]['image_path']

        X = [get_image(x) for x in batch]
        Y = data[[0, 1, 2, 3, 4, 5]].values[batch_ids]

        # Convert X and Y to arrays
        X = np.array(X)
        Y = np.array(Y)

        yield X, Y

# data: should be a pandas DF (train or val) obtained from train_test_split
# batch_size: is the size of the number of images passed through the net in one step


# ### Split the data set in train and validation

# In[ ]:


# Train -  Validation Split function
train, val = train_test_split(train_ann,                               test_size = 0.1,                               random_state = 42)


# In[ ]:


# Some checkpoints
model_checkpoint = ModelCheckpoint('./model_01.h5', monitor = 'val_loss', verbose=0, save_best_only=True, save_weights_only=True)
early_stop = EarlyStopping(monitor='val_loss',patience=5,verbose=True)


# ### Fit the model (Train)

# In[ ]:


EPOCHS = 30 
BS = 100

history = model.fit_generator(generator = data_generator(train, BS),
                              validation_data = data_generator(val, BS),
                              epochs = EPOCHS,
                              verbose = 1,
                              #steps_per_epoch = len(train)// BS,\
                              steps_per_epoch = 20,
                              validation_steps = 20, 
                              #validation_steps = len(val)// BS,\
                              callbacks =[model_checkpoint, early_stop])


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


# ## Predict on the Test Data 
# - sample submission

# In[ ]:


initial_sample_submission = pd.read_csv('../input/prostate-cancer-grade-assessment/sample_submission.csv')
TEST = Path("test_images")
test_ann = pd.read_csv(HOME/'test.csv')


# In[ ]:


if os.path.exists(f'../input/prostate-cancer-grade-assessment/test_images/'):
    print('inference!')

    predictions = []
    for img_id in test_ann['image_id']:
        img = str(HOME/TEST/img_id) + ".tiff"
        print(img)
        image = get_image(img)
        image = image[np.newaxis,:]
        prediction = model.predict(image)
        # if we have 1 at multiple locations
        ind = np.where(prediction == np.amax(prediction))
        final_prediction = random.sample(list(ind[1]), 1)[0].astype(int)
        predictions.append(final_prediction)

    sample_submission = pd.DataFrame()
    sample_submission['image_id'] = test_ann['image_id']
    sample_submission['isup_grade'] = predictions
    sample_submission

    sample_submission.to_csv('submission.csv', index=False)
    sample_submission.head()
else:
    print('Test Images folder does not exist! Save the sample_submission.csv!')
    initial_sample_submission.to_csv('submission.csv', index=False)

