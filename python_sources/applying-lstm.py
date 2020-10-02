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

import os
print(os.listdir("../input"))

from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler


# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


data = pd.read_csv('../input/coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv')
# df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
data = data.dropna()
cl = data['Weighted_Price']
print(cl.head(5))


# **reshape the data**

# In[ ]:


scl = MinMaxScaler()
print(cl.shape)
cl = cl.values.reshape(cl.shape[0], 1)
cl = scl.fit_transform(cl)
cl


# In[ ]:


#transform data into 7 days group. y is the 8th day price. X is [day1 price, day2 price....., day7 price]
def processData(data, dataLength):
    X, Y = [], []
    for i in range(len(data)-dataLength-1):
        X.append(data[i:(i+dataLength), 0])
        Y.append(data[(i+dataLength), 0])
    return np.array(X), np.array(Y)
X, y = processData(cl, 7)
X_train, X_test = X[:int(X.shape[0]*0.8)], X[int(X.shape[0]*0.8):]
y_train, y_test = y[:int(y.shape[0]*0.8)], y[int(y.shape[0]*0.8):]
print(X_train.shape[0])
print(X_test.shape[0])
print(y_train.shape[0])
print(y_test.shape[0])


# In[ ]:


#build the model
model = Sequential()
model.add(LSTM(256, input_shape=(7, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
history = model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test), shuffle=False)


# In[ ]:


print(X_train)


# In[ ]:


plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['loss', 'val_loss'])


# In[ ]:


print(X_test)


# In[ ]:


Xt = model.predict(X_test)
plt.plot(scl.inverse_transform(y_test.reshape(-1, 1)))
plt.plot(scl.inverse_transform(Xt))
plt.legend(['y_test', 'y_predict'])


# In[ ]:


z = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
print(z)
print(z.reshape(-1, 6))


# In[ ]:


print(X_test[249])
print(X_test[249].reshape(1, 7, 1))
X_prediction = model.predict(X_test[249].reshape([1, 7, 1]))
print('predictoin: {0}'.format(scl.inverse_transform(X_prediction)))
print('actual: {0}'.format(scl.inverse_transform(y_test[249].reshape(-1, 1))))


# Another model with activation function tanh

# In[ ]:


model2 = Sequential()
model2.add(LSTM(256, input_shape=(7, 1)))
model2.add(Dense(1, activation='tanh'))
model2.compile(optimizer='adam', loss='mse')
# X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
# X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
train_history2 = model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test), shuffle=False)


# In[ ]:


plt.plot(train_history2.history['loss'])
plt.plot(train_history2.history['val_loss'])
plt.title('thah model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')


# In[ ]:


Xt2 = model2.predict(X_test)
plt.plot(scl.inverse_transform(y_test.reshape(-1, 1)))
plt.plot(scl.inverse_transform(Xt2))
plt.legend(['y_test', 'y_predict'])


# In[ ]:


print(X_test[249])
print(X_test[249].reshape(1, 7, 1))
X_prediction2 = model2.predict(X_test[249].reshape([1, 7, 1]))
print('predictoin: {0}'.format(scl.inverse_transform(X_prediction)))
print('actual: {0}'.format(scl.inverse_transform(y_test[249].reshape(-1, 1))))

