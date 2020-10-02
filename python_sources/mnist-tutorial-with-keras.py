#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense, Dropout, Lambda, Flatten
from keras.optimizers import Adam, RMSprop
from sklearn.model_selection import train_test_split


# In[ ]:


train = pd.read_csv("../input/train.csv")
test_images = (pd.read_csv("../input/test.csv").values).astype('float32')


# In[ ]:


train_images = (train.ix[:, 1:].values).astype('float32')
train_labels = train['label'].values.astype('int32')


# In[ ]:


train_labels


# In[ ]:


train_images.shape


# In[ ]:


train_images = train_images.reshape(train_images.shape[0], 28, 28)

for i in range(4,9):
    plt.subplot(330 + (i+1))
    plt.imshow(train_images[i], cmap=plt.get_cmap('gray'))
    plt.title(train_labels[i])


# In[ ]:


train_images = train_images.reshape((42000, 28 * 28))


# In[ ]:


train_labels


# In[ ]:


train_images = train_images/255
test_images = test_images/255


# In[ ]:


from keras.utils.np_utils import to_categorical
train_labels = to_categorical(train_labels)
num_classes = train_labels.shape[1]
num_classes


# In[ ]:


plt.title(train_labels[9])
plt.plot(train_labels[9])
plt.xticks(range(10));


# In[ ]:


seed = 43
np.random.seed(seed)


# In[ ]:


train_images.shape


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense, Dropout


# In[ ]:


model = Sequential()
model.add(Dense(32, activation='relu', input_dim=(28*28)))
model.add(Dense(16, activation='relu'))
model.add(Dense(10, activation='softmax'))


# In[ ]:


from keras.optimizers import RMSprop


# In[ ]:


model.compile(optimizer=RMSprop(lr=0.001),
             loss='categorical_crossentropy',
             metrics=['accuracy'])


# In[ ]:


history=model.fit(train_images, train_labels, validation_split=0.05,
                 epochs=25, batch_size=64)


# In[ ]:


history_dict = history.history
history_dict.keys()


# In[ ]:


loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
epochs = range(1, len(loss_values) + 1)


# In[ ]:


plt.plot(epochs, loss_values, 'bo')
plt.plot(epochs, val_loss_values, 'b+')
plt.xlabel('Epochs')
plt.ylabel('Loss')


# In[ ]:


acc_values = history_dict['acc']
val_acc_values = history_dict['val_acc']


# In[ ]:


plt.plot(epochs, acc_values, 'bo')
plt.plot(epochs, val_acc_values, 'b+')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')

plt.show()


# In[ ]:


model = Sequential()
model.add(Dense(64, activation='relu', input_dim=(28*28)))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.15))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.15))
model.add(Dense(10, activation='softmax'))

model.compile(optimizer=RMSprop(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
history=model.fit(train_images, train_labels, epochs=15, batch_size=64)


# In[ ]:


predictions = model.predict_classes(test_images, verbose=0)
submissions=pd.DataFrame({'ImageId':list(range(1,len(predictions) + 1)), "Label": predictions})
submissions.to_csv("DR.csv", index=False, header=True)


# In[ ]:




