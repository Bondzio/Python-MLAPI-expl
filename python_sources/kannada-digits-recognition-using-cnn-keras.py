#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPool2D
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:


train_data = pd.read_csv('/kaggle/input/Kannada-MNIST/train.csv')
test_data = pd.read_csv('/kaggle/input/Kannada-MNIST/test.csv')


# In[ ]:


test_data


# In[ ]:


if not test_data.get('label'):
    print('Brak y_test')


# In[ ]:


y_train = train_data['label']
print("Labels: ", np.unique(y_train))
print("y_train shape: ", y_train.shape)


# <pre>
# Process the y_train to one-hot encoding.
# e.g
#     for label=2 => [0,0,1,0,0,0,0,0,0,0]
# </pre>

# In[ ]:


# one-hot encoding
y_train = to_categorical(y_train, 10)
print(y_train.shape)


# In[ ]:


x_train = train_data.iloc[:,1:].values
x_test = test_data.iloc[:,1:].values
print("x_train shape: ", x_train.shape)


# In[ ]:


x_train = x_train.reshape(x_train.shape[0], 28, 28)
x_test = x_test.reshape(x_test.shape[0], 28, 28)
print("x_train shape: ", x_train.shape)
print("x_test shape: ", x_test.shape)


# Plot he sample image

# In[ ]:


plt.figure()
plt.imshow(x_train[0])
plt.show()
y_train[0]


# Images are in gray scale so the shape of the particular one should be (29, 28, 1)

# In[ ]:


x_train = np.expand_dims(x_train, axis=3)
x_test = np.expand_dims(x_test, axis=3)
x_train.shape


# In[ ]:


model = Sequential([
    Conv2D(32, input_shape=x_train[0].shape, kernel_size=(4,4), activation='relu'),
    MaxPool2D(),
    Conv2D(64, kernel_size=(2,2), activation='relu'),
    MaxPool2D(),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(10, activation='softmax')
])
model.summary()


# In[ ]:


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[ ]:


history = model.fit(x=x_train, y=y_train, epochs=16, batch_size=32)


# In[ ]:


plt.plot(history.history['accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.show()


# In[ ]:


predictions = model.predict_classes(x_test)
predictions
submission = pd.read_csv('/kaggle/input/Kannada-MNIST/sample_submission.csv')
submission['label'] = predictions
print(submission.head(5))
submission.to_csv('submission.csv', index=False)


# In[ ]:


model.save('model.h5')

