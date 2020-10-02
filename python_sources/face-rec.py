#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#  Author: -- Rishi Jain --


# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:


#Import Keras framework for CNN
import warnings
warnings.filterwarnings('ignore')
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Conv2D, BatchNormalization
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils.np_utils import to_categorical


# In[ ]:


import os
os.chdir('../input/utk-face-cropped/')
os.chdir('utkcropped')
os.chdir('utkcropped')


# In[ ]:


from PIL import Image
im =Image.open('100_0_0_20170112213500903.jpg.chip.jpg')
im


# In[ ]:


#Since dataset contains some mislabed examples which are not in form of <age>_<gender>_<enthnicity>_<date>
#we remove those examples using fnmatch.
temp = os.listdir()
import fnmatch
dataset = fnmatch.filter(temp, '*_*_*_*')
m = len(dataset)
print(m)


# Since the cell contains images of age group in decreasing order, The images are not randomly distributed. We will use Shuffle() so that the distribution is random.

# In[ ]:


from random import shuffle
shuffle(dataset)


# Understanding dataset Each image is of dimension 200 x 200 x 3(RGB) The dataset contains entries like:
# 
# * Age       :is a Positive Integer, denoting age of person
# * Gender    :is denoted by 1(male) or 0(female)
# * Ethnicity :is an integer from 0 to 4, denoting White, Black, Asian, Indian, and Others.

# In[ ]:


#format of labelled images
dataset[:2]


# In[ ]:


age = [i.split('_')[0] for i in dataset]
gender = [i.split('_')[1] for i in dataset]
ethnicity = [i.split('_')[2] for i in dataset]


# In[ ]:


#top 2 entries in age
age[:2]


# Since ages are returned as string therefore converting them to integers

# In[ ]:


#Since ages are in strings we need to type cast to integer.
age = list(map(int, age))
gender = list(map(int,gender))
ethnicity = list(map(int,ethnicity))


# In[ ]:


age[:2]


# Ages are now converted to integers

# In[ ]:


gender_classes = to_categorical(gender, num_classes=2)
ethnicity_classes = to_categorical(ethnicity,num_classes=5)


# Types of Problem:
# 
# 1. AGE: Regression Problem
# 
# 2. GENDER: Binary Classification Problem
# 
# 3. ETHNICITY: Multiclass Classification Problem

# In[ ]:


#Resizing Images to 128 x 128
from scipy import misc
import cv2
X_data =[]
for file in dataset:
    face = misc.imread(file)
    face = cv2.resize(face, (128, 128) )
    X_data.append(face)
X = np.squeeze(X_data)


# In[ ]:


#Normalizing Images
X = X.astype('float32')
X /= 255


# In[ ]:


#Number of Training examples
len(X)


# Spliting data into Training Set, Validation Set and Test Set
# 
# Train Set Size : 18,000 examples
# 
# Validation Set Size : 3,000 examples
# 
# Test Set Size : 2,705 examples

# In[ ]:


(X_gender_train, y_gender_train), (X_gender_test, y_gender_test) = (X[:18000],gender_classes[:18000]) , (X[18000:] , gender_classes[18000:])
(X_gender_valid , y_gender_valid) = (X_gender_test[:3000], y_gender_test[:3000])
(X_gender_test, y_gender_test) = (X_gender_test[3000:], y_gender_test[3000:])

(X_ethnicity_train, y_ethnicity_train), (X_ethnicity_test, y_ethnicity_test) = (X[:18000],ethnicity_classes[:18000]) , (X[18000:] , ethnicity_classes[18000:])
(X_ethnicity_valid , y_ethnicity_valid) = (X_ethnicity_test[:3000], y_ethnicity_test[:3000])
(X_ethnicity_test, y_ethnicity_test) = (X_ethnicity_test[3000:], y_ethnicity_test[3000:])

(X_age_train, y_age_train), (X_age_test, y_age_test) = (X[:18000],age[:18000]) , (X[18000:] , age[18000:])
(X_age_valid , y_age_valid) = (X_age_test[:3000], y_age_test[:3000])
(X_age_test, y_age_test) = (X_age_test[3000:], y_age_test[3000:])


# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
plt.hist(gender)
plt.xlabel('Gender')
plt.ylabel('Frequency');


# In[ ]:


gender_model = Sequential()
gender_model.add(Convolution2D(16, 3, padding='same', activation='relu', input_shape=(128,128, 3)))
gender_model.add(MaxPooling2D(2, 2))
gender_model.add(BatchNormalization())

gender_model.add(Convolution2D(16, 3, padding='same', activation='relu'))
gender_model.add(MaxPooling2D(2, 2))
gender_model.add(BatchNormalization())

gender_model.add(Convolution2D(32, 3, padding='same', activation='relu'))
gender_model.add(MaxPooling2D(2, 2))

gender_model.add(Convolution2D(32, 3,  activation='relu'))
gender_model.add(MaxPooling2D(2, 2))


gender_model.add(Flatten())
gender_model.add(Dropout(0.30))

gender_model.add(Dense(512, activation='relu'))
gender_model.add(Dropout(0.50))

gender_model.add(Dense(128, activation='relu'))
gender_model.add(Dropout(0.50))

gender_model.add(Dense(32, activation='relu'))
gender_model.add(Dropout(0.50))

gender_model.add(Dense(2, activation='sigmoid', name='predictions'))


# In[ ]:


gender_model.summary()


# In[ ]:


gender_model.compile(loss='binary_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])


# In[ ]:


gender_history = gender_model.fit(X_gender_train,
         y_gender_train,
         batch_size=3000,
         epochs=30,
         validation_data=(X_gender_valid, y_gender_valid))


# In[ ]:


plt.plot(gender_history.history['loss'])
plt.plot(gender_history.history['val_loss'])
plt.title('model accuracy')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()


# In[ ]:


from keras.callbacks import ModelCheckpoint
gender_modelcheckpoint = ModelCheckpoint("gender.model")


# In[ ]:


# Plot a random sample of 5 test images, their predicted labels and ground truth
import matplotlib.pyplot as plt
labels = ['Male','Female']
figure = plt.figure(figsize=(15, 15))
y_gender_pred = gender_model.predict(X_gender_test)
for i, index in enumerate(np.random.choice(X_gender_test.shape[0], size=5, replace=False)):
    ax = figure.add_subplot(2, 5, i + 1, xticks=[], yticks=[])
    # Display each image
    ax.imshow(np.squeeze(X_gender_test[index]))
    predict_index = np.argmax(y_gender_pred[index])
    true_index = np.argmax(y_gender_test[index])
    # Set the title for each image
    ax.set_title("Predicted: {} ,\n Actual: {}".format(labels[predict_index], 
                                  labels[true_index]),
                                  color=("green" if predict_index == true_index else "red"))
plt.show()


# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
plt.hist(ethnicity)
plt.xlabel('Ethnicity')
plt.ylabel('Frequency');


# In[ ]:


ethnicity_model = Sequential()
ethnicity_model.add(Convolution2D(16, 3, padding='same', activation='relu', input_shape=(128, 128, 3)))
ethnicity_model.add(MaxPooling2D(2, 2))

ethnicity_model.add(Convolution2D(32, 3,padding='same' , activation='relu'))
ethnicity_model.add(MaxPooling2D(2, 2))

ethnicity_model.add(Convolution2D(32, 3,padding='same' , activation='relu'))
ethnicity_model.add(MaxPooling2D(2, 2))

ethnicity_model.add(Convolution2D(64, 3,padding='same' , activation='relu'))
ethnicity_model.add(MaxPooling2D(2, 2))

ethnicity_model.add(Convolution2D(64, 3,padding='same' , activation='relu'))
ethnicity_model.add(MaxPooling2D(2, 2))

ethnicity_model.add(Flatten())
ethnicity_model.add(Dropout(0.30))
ethnicity_model.add(Dense(256, activation='relu'))

ethnicity_model.add(Dropout(0.30))
ethnicity_model.add(Dense(64, activation='relu'))
ethnicity_model.add(Dense(5, activation='softmax'))


# In[ ]:


ethnicity_model.summary()


# In[ ]:


ethnicity_model.compile(loss='categorical_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])

ethnicity_history = ethnicity_model.fit(X_ethnicity_train,
         y_ethnicity_train,
         batch_size=3000,
         epochs=20,
         validation_data=(X_ethnicity_valid, y_ethnicity_valid))


# In[ ]:


plt.plot(ethnicity_history.history['loss'])
plt.plot(ethnicity_history.history['val_loss'])
plt.title('model accuracy')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()


# In[ ]:


# Plot a random sample of 5 test images, their predicted labels and ground truth
import matplotlib.pyplot as plt
labels = ['White','Black','Asian','Indian','Others']
figure = plt.figure(figsize=(25, 20))
y_ethnicity_pred = ethnicity_model.predict(X_ethnicity_test)
for i, index in enumerate(np.random.choice(X_ethnicity_test.shape[0], size=5, replace=False)):
    ax = figure.add_subplot(3, 5, i + 1, xticks=[], yticks=[])
    # Display each image
    ax.imshow(np.squeeze(X_ethnicity_test[index]))
    predict_index = np.argmax(y_ethnicity_pred[index])
    true_index = np.argmax(y_ethnicity_test[index])
    # Set the title for each image
    ax.set_title("Predicted: {}\n , Actual: {}".format(labels[predict_index], 
                                  labels[true_index]),
                                  color=("green" if predict_index == true_index else "red"))
plt.show()


# In[ ]:


ethnicity_modelcheckpoint = ModelCheckpoint("ethnicity.model")


# In[ ]:


age_model = Sequential()

age_model.add(Convolution2D(32, 3, padding='same', activation='relu', input_shape=(128, 128, 3)))
age_model.add(MaxPooling2D(2, 2))
age_model.add(BatchNormalization())

age_model.add(Convolution2D(32, 3, padding='same', activation='relu'))
age_model.add(MaxPooling2D(2, 2))

age_model.add(Convolution2D(32, 3, padding='same', activation='relu'))
age_model.add(MaxPooling2D(2, 2))

age_model.add(Flatten())
              
age_model.add(Dropout(0.50))
age_model.add(Dense(512, activation='relu'))
              
age_model.add(Dropout(0.50))
age_model.add(Dense(128, activation='relu'))

age_model.add(Dropout(0.50))
age_model.add(Dense(16, activation='relu'))

age_model.add(Dense(1, activation='linear',name='age_output'))
age_model.summary()


# In[ ]:


age_model.compile(loss='mse',
             optimizer='adam',
             metrics=['mae'])


# In[ ]:


age_history = age_model.fit(X_age_train,
         y_age_train,
         batch_size=1000,
         epochs=40,
         validation_data=(X_age_valid, y_age_valid))


# In[ ]:


plt.plot(age_history.history['loss'])
plt.plot(age_history.history['val_loss'])
plt.title('model accuracy')
plt.ylabel('Loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()


# In[ ]:


# Plot a random sample of 10 test images, their predicted labels and ground truth
import matplotlib.pyplot as plt
figure = plt.figure(figsize=(25, 20))
y_age_pred = age_model.predict(X_age_test)
for i, index in enumerate(np.random.choice(X_age_test.shape[0], size=5, replace=False)):
    ax = figure.add_subplot(1, 5, i + 1, xticks=[], yticks=[])
    # Display each image
    ax.imshow(np.squeeze(X_age_test[index]))
    # Set the title for each image
    ax.set_title("Predicted: {} , Actual: {}".format(np.rint(y_age_pred[index]), 
                                  y_age_test[index]),
                                  color=("green" if abs(y_age_pred[index] - y_age_test[index])<=7  else "red"))
plt.show()


# In[ ]:


age_modelcheckpoint = ModelCheckpoint("age.model")


# In[ ]:




