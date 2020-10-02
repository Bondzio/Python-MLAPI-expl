#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


get_ipython().run_cell_magic('time', '', "\ntrain_set=pd.read_csv('../input/train.csv')\ntest_set=pd.read_csv('../input/test.csv')")


# In[ ]:


train_set.shape


# In[ ]:


test_set.shape


# In[ ]:


X_train=train_set.drop(['label'], axis=1)
Y_train=train_set['label']
print(X_train.shape, Y_train.shape)


# In[ ]:


train_set.head()


# In[ ]:


sample1=X_train.iloc[0]
sr = sample1.values.reshape(28,28)
plt.imshow(sr)


# In[ ]:


fig=plt.figure(figsize=(8,8))
rows=4
columns=5
for i in range(1,rows*columns+1):  
    fig.add_subplot(rows,columns,i)
    plt.imshow(X_train.iloc[i].values.reshape(28,28))


# In[ ]:


X_train_reshaped = X_train.values.reshape(-1,28,28,1)
# Y_train_
print(X_train_reshaped.shape, Y_train.shape)


# In[ ]:


# split training dataset in training and validation sets
x_train, x_val, y_train, y_val = train_test_split(X_train_reshaped,Y_train, test_size=0.3)
print(x_train.shape, y_train.shape, x_val.shape, y_val.shape)


# In[ ]:


from keras.utils import to_categorical
y_train_binary = to_categorical(y_train)
y_val_binary = to_categorical(y_val)
print(y_train_binary.shape, y_val_binary.shape)


# In[ ]:


model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', padding='same', input_shape=(28, 28, 1)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Flatten(),
    
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    
    tf.keras.layers.Dense(10, activation='softmax')
])


model.compile(loss='categorical_crossentropy',
              optimizer=Adam(0.0001),
              metrics=['acc'])


# In[ ]:


model.summary()


# In[ ]:


train_datagen = ImageDataGenerator(
        rotation_range=10,
        zoom_range = 0.1, 
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        )

train_datagen.fit(x_train)


# In[ ]:


get_ipython().run_cell_magic('time', '', 'bs=32 ## gives the best accuracy value for the validation\n## slight overfitting for 33\nhistory = model.fit_generator(\n        train_datagen.flow(x_train, y_train_binary, batch_size=bs),\n        epochs=20,\n        validation_data=(x_val, y_val_binary),\n        )')


# In[ ]:


from pprint import pprint
pprint(history.history)


# In[ ]:


plt.plot(history.history['acc'])
# plt.subplot(221)
plt.plot(history.history['val_acc'])


# ### testing the model

# In[ ]:


get_ipython().run_cell_magic('time', '', 'X_test = test_set.values.reshape(-1,28,28,1)\n# model.evaluate(X_test)\npredict = model.predict(X_test)\nprint(predict.shape)')


# In[ ]:


predict #the predict array includes the probability for every number to be the the value of the digit in the pic


# In[ ]:


get_ipython().run_cell_magic('time', '', '\npredictions = []\nfor i in range(28000):\n    predictions.append(np.argmax(predict[i]))\nfig=plt.figure(figsize=(8,8))\nrows=4\ncolumns=5\nfor i in range(1,rows*columns+1):  \n    fig.add_subplot(rows,columns,i)    \n    plt.title(str(predictions[i]))\n    plt.imshow(test_set.iloc[i].values.reshape(28,28))')


# In[ ]:




