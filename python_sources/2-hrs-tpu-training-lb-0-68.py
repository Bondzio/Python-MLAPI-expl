#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install -qq ../input/efficientnetrepo110/efficientnet-1.1.0-py3-none-any.whl')


# In[ ]:


import os
import cv2
import skimage.io
import numpy as np
import pandas as pd
import math
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model
from matplotlib import pyplot as plt
import efficientnet.tfkeras as efn

print(tf.__version__)
print(tf.keras.__version__)


# In[ ]:


img_size = 512
nb_classes = 6


# # Load Model

# In[ ]:


def get_model():
    base_model =  efn.EfficientNetB7(weights = None, include_top=False, pooling='avg', input_shape=(img_size, img_size, 3))
    x = base_model.output
    predictions = Dense(nb_classes, activation="softmax")(x)
    return Model(inputs=base_model.input, outputs=predictions)

model = get_model()
model.load_weights('../input/model-efn-tpu-2/model.h5')


# # Get image from image name

# In[ ]:


def get_image(img_name, data_dir='../input/prostate-cancer-grade-assessment/test_images'):
    img_path = os.path.join(data_dir, f'{img_name}.tiff')
    img = skimage.io.MultiImage(img_path)
    img = cv2.resize(img[-1], (img_size,img_size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img/255.0
    return img


# # TTA
# 
# Function to generate different images from given image and do predictions on them

# In[ ]:


def TTA(img):
    img1 = img
    img2 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img3 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img4 = cv2.rotate(img, cv2.ROTATE_180)
    images = [img1, img2, img3, img4]
    
    return model.predict(np.array(images), batch_size=4)


# # Post-process TTA predictions

# In[ ]:


def post_process(preds):
    avg = np.sum(preds,axis = 0)
    label = np.argmax(avg)
    return label


# # Predicting on test images

# In[ ]:


from tqdm import tqdm


# In[ ]:


data_dir = '../input/prostate-cancer-grade-assessment/test_images'
sample_submission = pd.read_csv('../input/prostate-cancer-grade-assessment/sample_submission.csv')
# data_dir = '../input/prostate-cancer-grade-assessment/train_images'
# sample_submission = pd.read_csv('../input/prostate-cancer-grade-assessment/train.csv').head(1000)

test_images = sample_submission.image_id.values
labels = []

try:    
    for image in tqdm(test_images):
        img = get_image(image, data_dir)
        preds = TTA(img)
        label = post_process(preds)
        labels.append(label)
    sample_submission['isup_grade'] = labels
except:
    print('Test dir not found')
    
sample_submission['isup_grade'] = sample_submission['isup_grade'].astype(int)
sample_submission.to_csv('submission.csv', index=False)
sample_submission.head()


# Click [here](https://www.kaggle.com/prateekagnihotri/image-augmentation-on-tpu) for Training kernel.

# Thanks for reading. Please upvote if you like it.
# 
# For QWK metric, TTA, image augmentations, Transfer learning.. visit my kernels [1](https://www.kaggle.com/prateekagnihotri/efficientnet-keras-train-qwk-loss-augmentation), [2](https://www.kaggle.com/prateekagnihotri/efficientnet-keras-infernce-tta), and [3](https://www.kaggle.com/prateekagnihotri/transfer-learning-starter-kernel).
