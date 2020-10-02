#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
# for dirname, _, filenames in os.walk('/kaggle/input'):
#     for filename in filenames:
#         print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import cv2
import os
import h5py
import matplotlib.pyplot as plt
import skimage.io
from skimage.transform import resize
from imgaug import augmenters as iaa
from tqdm import tqdm
import PIL
from PIL import Image, ImageOps
from sklearn.utils import class_weight, shuffle
from keras.losses import binary_crossentropy, categorical_crossentropy
from keras.applications.resnet50 import preprocess_input
import keras.backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import tensorflow as tf
from sklearn.metrics import f1_score, fbeta_score, cohen_kappa_score, accuracy_score
from keras.utils import Sequence
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


def fd_histogram(image, mask=None):
    # convert the image to HSV color-space
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # compute the color histogram
    hist  = cv2.calcHist([image], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
    # normalize the histogram
    cv2.normalize(hist, hist)
    # return the histogram
    return hist.flatten()

def fd_sift(image) :
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kps, des = sift.detectAndCompute(image, None)
    return des if des is not None else np.array([]).reshape(0, 128)


# In[ ]:


os.listdir('/kaggle/input/animals10/animals/raw-img')
foldernames = os.listdir('/kaggle/input/animals10/animals/raw-img')
categories = []
files = []
labels = []
i = 0
for folder in foldernames:
    labels.append(folder)
    filenames = os.listdir("../input/animals10/animals/raw-img/" + folder);
    for file in filenames:
        files.append("../input/animals10/animals/raw-img/" + folder + "/" + file)
        categories.append(i)
    i = i + 1
        
        
df = pd.DataFrame({
    'filename': files,
    'category': categories
})


# In[ ]:


# df.head


# In[ ]:


y = df['category']
df['category'].value_counts()


# In[ ]:


train_df = df
train_df.head()


# In[ ]:


x = train_df['filename']
y = train_df['category']

x, y = shuffle(x, y, random_state=8)
y.hist()


# In[ ]:


x.shape,y.shape


# In[ ]:


sift = cv2.ORB_create()


# In[ ]:


def fd_sift(image) :
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kps, des = sift.detectAndCompute(image, None)
    return des if des is not None else np.array([]).reshape(0, 128)


# In[ ]:


# train_x, valid_x, train_y, valid_y = train_test_split(x, y, test_size=0.1, stratify=y, random_state=8)
# print(train_x.shape)
# print(train_y.shape)
# print(valid_x.shape)
# print(valid_y.shape)


# TRAINING

# In[ ]:


global_features = []
labels          = y
fixed_size = (500,500,3)
for file in x[:1000]:
    image = cv2.imread(file)
    image.resize(fixed_size)
    fv_sift = fd_sift(image)
    global_feature = np.hstack([fv_sift])
    global_feature.resize(fixed_size)
    global_features.append(global_feature)


# In[ ]:


for i in global_features[:10]:
    print(i.shape)


# In[ ]:


targetNames = np.unique(labels)
targetNames


# In[ ]:


le          = LabelEncoder()
target      = le.fit_transform(labels)
le,target


# In[ ]:


# global_features


# In[ ]:


scaler            = MinMaxScaler(feature_range=(0, 1))
# rescaled_features = scaler.fit_transform(global_features)


# TEST

# In[ ]:


X_train = np.array(global_features)
X_train = X_train.reshape(len(X_train),500*500*3)
Y_train = np.array(y[0:1000])
len(X_train),X_train.shape


# In[ ]:


train_x, valid_x, train_y, valid_y = train_test_split(X_train, Y_train, 
                                                      test_size=0.1, 
                                                      stratify=Y_train, 
                                                      random_state=8)
print(train_x.shape)
print(train_y.shape)
print(valid_x.shape)
print(valid_y.shape)


# In[ ]:


model = KNeighborsClassifier(n_neighbors = 10, p = 1)
model.fit(train_x,train_y)


# In[ ]:


# y_pred = model.predict(valid_x)
# print(accuracy_score(valid_y, y_pred)*100)


# In[ ]:


test_x = x[:-28200]
test_y = y[:-28200]
for i,j in zip(test_x[:10],test_y[:10]):
    sample = cv2.imread(i)
    print(j)
    print(i)
    plt.imshow(sample)
    plt.show()
    sample.resize(fixed_size)


# In[ ]:


test_X_reshape = np.array(test_x)
# test_X_reshape = test_X_reshape.reshape(len(test_X_reshape),500*500*3)
# y_pred = model.predict()
test_X_reshape
all_samples = []
for file in test_x:
    sample = cv2.imread(file)
    sample.resize(fixed_size)
    fv_sift = fd_sift(image)
    all_sample = np.hstack([fv_sift])
    all_sample.resize(fixed_size)
    all_samples.append(all_sample)

samples = np.array(all_samples)
samples = samples.reshape(len(samples),500*500*3)
len(samples),samples.shape


# In[ ]:


res = model.predict(samples)


# In[ ]:


res


# In[ ]:


# # boxplot algorithm comparison
# fig = pyplot.figure()
# fig.suptitle('Machine Learning algorithm comparison')
# ax = fig.add_subplot(111)
# pyplot.boxplot(results)
# ax.set_xticklabels(names)
# pyplot.show()

