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


train_csv = pd.read_csv('/kaggle/input/digit-recognizer/train.csv')
test_csv = pd.read_csv('/kaggle/input/digit-recognizer/test.csv')


# In[ ]:


print(train_csv.shape)
print(test_csv.shape)


# In[ ]:


import matplotlib.pyplot  as plt
plt.imshow(np.array(train_csv.iloc[2:3,:].drop('label',axis=1)).reshape((28,28)))


# In[ ]:


train_csv.head()


# In[ ]:


from sklearn.utils import shuffle
train_csv = shuffle(train_csv)


# In[ ]:


train_csv.head()


# In[ ]:


train_csv.reset_index(inplace=True, drop=True)


# In[ ]:


df = pd.concat((train_csv,test_csv))
df.shape


# In[ ]:


df2 = df.drop('label',axis=1)/255
df2


# In[ ]:


X_train = df2[:len(train_csv)]
X_test = df2[len(train_csv):]
y_train = df['label'][:len(train_csv)]

print(X_train.shape)
print(X_test.shape)
print(len(y_train))


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical


# In[ ]:


model = Sequential()
model.add(Dense(64, activation = 'relu' , input_dim=784))
model.add(Dense(64, activation = 'relu' ))
model.add(Dense(10, activation = 'softmax'))


# In[ ]:


model.compile(
optimizer='adam',loss = 'categorical_crossentropy',metrics=['accuracy'])


# In[ ]:


model.fit(
    X_train,
    to_categorical(y_train),
    epochs = 10,
    batch_size = 32
)


# In[ ]:


predictions = model.predict(X_test)
predictions


# In[ ]:


predictions = np.argmax(predictions,axis=1)


# In[ ]:


pd.DataFrame({"ImageId":list(range(1,len(predictions)+1)),
              "Label":predictions}).to_csv("mnist_sumbmission.csv",
                                           index=False,
                                           header=True)


# In[ ]:




