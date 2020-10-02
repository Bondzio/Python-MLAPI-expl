#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')

get_ipython().run_line_magic('matplotlib', 'inline')

import keras
from keras.models import Sequential
from keras import regularizers
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
from keras.utils import to_categorical

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

print(os.listdir("../input"))


# In[ ]:


path = "../input/asl/asl"


# In[ ]:


dirs = os.listdir(path)


# In[ ]:


label_dict = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
    '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16,
    'h': 17, 'i': 18, 'j': 19, 'k': 20, 'l': 21, 'm': 22, 'n': 23, 'o': 24,
    'p': 25, 'q': 26, 'r': 27, 's': 28, 't': 29, 'u': 30, 'v': 31, 'w': 32,
    'x': 33, 'y': 34, 'z': 35,
}


# In[ ]:


size = 200,200

def load_dataset(path):
    image_data = list()
    labels = list()
    dirs = os.listdir(path)
    print("Loading images for: ", end =" ")
    for Dir in dirs:
        print("{} |".format(Dir), end=" ")
        path_img = path+'/'+Dir
        images = os.listdir(path_img)
        for image in images:
            temp_img = cv2.imread(path_img+'/'+image)
            temp_img = cv2.resize(temp_img, size)
            temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)
            image_data.append(temp_img)
            labels.append(label_dict[Dir])
    
    image_data = np.array(image_data)
    labels = to_categorical(labels)
    
    image_data, labels = shuffle(image_data, labels, random_state=1)

    X_train, X_test, y_train, y_test = train_test_split(image_data, labels, test_size=0.05)
    return X_train, y_train, X_test, y_test


# In[ ]:


X_train, y_train, X_test, y_test = load_dataset(path)


# In[ ]:


print("Shape of X_train: ", X_train.shape)
print("shape of y_train/labels: ", y_train.shape)
print("Shape of X_test: ", X_test.shape)
print("shape of y_test/labels: ", y_test.shape)


# In[ ]:


samples = np.random.choice(len(X_train), 8)


# In[ ]:


def show_images(images, cols = 1, titles = None):
    """Display a list of images in a single figure with matplotlib.
    
    Parameters
    ---------
    images: List of np.arrays compatible with plt.imshow.
    
    cols (Default = 1): Number of columns in figure (number of rows is 
                        set to np.ceil(n_images/float(cols))).
    
    titles: List of titles corresponding to each image. Must have
            the same length as titles.
    """
    assert((titles is None)or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None: titles = ['Image (%d)' % i for i in range(1,n_images + 1)]
    fig = plt.figure()
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images/float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        a.set_title(title, fontsize=50)
        a.grid(False)
        a.axis("off")
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
plt.show()
    


# In[ ]:


sample_images = []
sample_labels = []
for sample in samples:
    sample_images.append(X_train[sample])
    for key, val in label_dict.items():
        if np.argmax(y_train[sample]) == val:
            sample_labels.append(key)


# In[ ]:


show_images(sample_images, 2, titles=sample_labels)


# ### Model

# In[ ]:


def create_model():
    
    model = Sequential()
    
    model.add(Conv2D(64, kernel_size = [3,3], padding = 'same', activation = 'relu', input_shape = (200,200,3)))
    model.add(Conv2D(64, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(MaxPool2D(pool_size = [3,3]))
    
    model.add(Conv2D(128, kernel_size = [5,5], padding = 'same', activation = 'relu'))
    model.add(Conv2D(128, kernel_size = [5,5], padding = 'same', activation = 'relu'))
    model.add(MaxPool2D(pool_size = [3,3]))
    
    model.add(Conv2D(256, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(Conv2D(256, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(Conv2D(256, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(MaxPool2D(pool_size = [3,3]))
    
    model.add(Conv2D(512, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(Conv2D(512, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(MaxPool2D(pool_size = [3,3]))
    
    model.add(Conv2D(512, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(MaxPool2D(pool_size = [2,2]))
    
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dropout(0.5))
    
    model.add(Dense(1024, activation = 'relu', kernel_regularizer = regularizers.l2(0.001)))
    model.add(Dense(512, activation = 'relu', kernel_regularizer = regularizers.l2(0.001)))
    model.add(Dense(36, activation = 'softmax'))
    
    print("MODEL CREATED")
    return model


# In[ ]:


model = create_model()


# In[ ]:


model.summary()


# In[ ]:


model.compile(optimizer = 'adam', loss = keras.losses.categorical_crossentropy, metrics = ["accuracy"])


# In[ ]:


model_hist = model.fit(X_train, y_train, batch_size = 32, epochs = 12, validation_data=(X_test, y_test))

