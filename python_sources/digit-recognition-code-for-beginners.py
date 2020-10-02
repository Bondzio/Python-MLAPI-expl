#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


#Importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


# Load the data
train = pd.read_csv("../input/digit-recognizer/train.csv")
test = pd.read_csv("../input/digit-recognizer/test.csv")


# In[ ]:


train.tail()


# In[ ]:


#converting the data into array
training = np.array(train, dtype = 'float32')
testing = np.array(test, dtype = 'float32')


# In[ ]:


plt.imshow(training[10, 1:].reshape(28, 28))


# In[ ]:


x_train = training[:, 1:]/255
y_train = training[:, 0]


# In[ ]:


x_test = testing/255


# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_validate, y_train, y_validate = train_test_split(x_train, y_train, test_size = 0.1, random_state = 0)


# In[ ]:


x_train = x_train.reshape(x_train.shape[0],28,28,1)
x_test = x_test.reshape(x_test.shape[0],28,28,1)
x_validate = x_validate.reshape(x_validate.shape[0],28,28,1)


# In[ ]:


x_train.shape


# In[ ]:


x_test.shape


# In[ ]:


x_validate.shape


# In[ ]:


import keras


# In[ ]:


from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.optimizers import Adam
from keras.callbacks import TensorBoard


# In[ ]:


model = Sequential()


# In[ ]:


model.add(Conv2D(64, 3, 3, input_shape = (28, 28, 1), activation ='relu'))
model.add(Conv2D(64, 3, 3, activation ='relu'))


# In[ ]:


model.add(MaxPooling2D(pool_size = (2,2)))


# In[ ]:


model.add(Flatten())


# In[ ]:


model.add(Dense(output_dim = 32, activation ='relu'))
model.add(Dense(output_dim = 10, activation ='softmax'))


# In[ ]:


model.add(Dropout(0.25))


# In[ ]:


model.compile(loss = 'sparse_categorical_crossentropy', optimizer = Adam(lr = 0.001), metrics =['accuracy'])


# In[ ]:


epochs = 50


# In[ ]:


model.fit(x_train,
         y_train,
         batch_size = 512,
         epochs = epochs,
         verbose = 1,
         validation_data = (x_validate, y_validate))


# In[ ]:


x_pred = model.predict(x_test)


# In[ ]:


x_pred = np.argmax(x_pred,axis = 1)
x_pred = pd.Series(x_pred,name="Label")


# In[ ]:


submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),x_pred],axis = 1)


# In[ ]:


submission.to_csv("cnn_mnist_datagen.csv",index=False)


# In[ ]:




