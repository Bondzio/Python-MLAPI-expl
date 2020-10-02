#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


AMD_train = pd.read_csv("../input/AMD_train.csv")
BABA_train = pd.read_csv("../input/BABA_train.csv")
NFLX_train = pd.read_csv("../input/NFLX_train.csv")


# In[ ]:


AMD_train


# In[ ]:


BABA_train


# In[ ]:


NFLX_train


# In[ ]:


AMD_training_set = AMD_train.iloc[:,1:2].values
BABA_training_set = BABA_train.iloc[:,1:2].values
NFLX_training_set = NFLX_train.iloc[:,1:2].values


# In[ ]:


from sklearn.preprocessing import MinMaxScaler

sc = MinMaxScaler(feature_range = (0,1))

AMD_training_scaled = sc.fit_transform(AMD_training_set)

BABA_training_scaled = sc.fit_transform(BABA_training_set)

NFLX_training_scaled = sc.fit_transform(NFLX_training_set)


# In[ ]:


amd_x_train = []
amd_y_train = []
nflx_x_train = []
nflx_y_train = []

for i in range(60,1259):
    amd_x_train.append(AMD_training_scaled[i-60:i,0])
    amd_y_train.append(AMD_training_scaled[i,0])
    nflx_x_train.append(NFLX_training_scaled[i-60:i,0])
    nflx_y_train.append(NFLX_training_scaled[i,0])
    
amd_x_train,amd_y_train,nflx_x_train,nflx_y_train = np.array(amd_x_train),np.array(amd_y_train),np.array(nflx_x_train),np.array(nflx_y_train)


# In[ ]:


baba_x_train = []
baba_y_train = []

for y in range(60,827):
    baba_x_train.append(BABA_training_scaled[y-60:y,0])
    baba_y_train.append(BABA_training_scaled[y,0])
    
baba_x_train,baba_y_train = np.array(baba_x_train),np.array(baba_y_train)


# In[ ]:


amd_x_train.shape


# In[ ]:


baba_x_train.shape


# In[ ]:


nflx_x_train.shape


# ***Convert to 3D***

# In[ ]:


amd_x_train = np.reshape(amd_x_train,(amd_x_train.shape[0],amd_x_train.shape[1],1))
baba_x_train = np.reshape(baba_x_train,(baba_x_train.shape[0],baba_x_train.shape[1],1))
nflx_x_train = np.reshape(nflx_x_train,(nflx_x_train.shape[0],nflx_x_train.shape[1],1))


# ***Using LSTM***

# In[ ]:


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


# ***Adding Hidden Layers for AMD***

# In[ ]:


amdregressor = Sequential()
amdregressor.add(LSTM(units = 50,return_sequences = True,input_shape = (amd_x_train.shape[1],1)))
amdregressor.add(Dropout(0.2))
amdregressor.add(LSTM(units = 50, return_sequences = True))
amdregressor.add(Dropout(0.2))
amdregressor.add(LSTM(units = 50, return_sequences = True))
amdregressor.add(Dropout(0.2))
amdregressor.add(LSTM(units = 50))
amdregressor.add(Dropout(0.2))
amdregressor.add(Dense(units = 1))


# ***Adding Hidden Layers for BABA***

# In[ ]:


babaregressor = Sequential()
babaregressor.add(LSTM(units = 50, return_sequences = True, input_shape = (baba_x_train.shape[1],1)))
babaregressor.add(Dropout(0.2))
babaregressor.add(LSTM(units = 50, return_sequences = True))
babaregressor.add(Dropout(0.2))
babaregressor.add(LSTM(units = 50, return_sequences = True))
babaregressor.add(Dropout(0.2))
babaregressor.add(LSTM(units = 50))
babaregressor.add(Dropout(0.2))
babaregressor.add(Dense(units = 1))


# ***Adding Hidden Layers for NFLX***

# In[ ]:


nflxregressor = Sequential()
nflxregressor.add(LSTM(units = 50, return_sequences = True, input_shape = (nflx_x_train.shape[1],1)))
nflxregressor.add(Dropout(0.2))
nflxregressor.add(LSTM(units = 50, return_sequences = True))
nflxregressor.add(Dropout(0.2))
nflxregressor.add(LSTM(units = 50, return_sequences = True))
nflxregressor.add(Dropout(0.2))
nflxregressor.add(LSTM(units = 50))
nflxregressor.add(Dropout(0.2))
nflxregressor.add(Dense(units = 1))


# In[ ]:


amdregressor.compile(optimizer = 'adam',loss = 'mean_squared_error')
babaregressor.compile(optimizer = 'adam', loss = 'mean_squared_error')


# In[ ]:


nflxregressor.compile(optimizer = 'adam', loss = 'mean_squared_error')


# In[ ]:


amdregressor.fit(amd_x_train,amd_y_train,epochs = 100, batch_size = 32)


# In[ ]:


babaregressor.fit(baba_x_train,baba_y_train,epochs = 100,batch_size = 32)


# In[ ]:


nflxregressor.fit(nflx_x_train,nflx_y_train,epochs = 150, batch_size = 32)


# ***Convert testdata to match trainset format***

# In[ ]:


amd_test =pd.read_csv("../input/AMD_test.csv")
baba_test = pd.read_csv("../input/BABA_test.csv")
nflx_test = pd.read_csv("../input/NFLX_test.csv")


# In[ ]:


amd_real_stock_price = amd_test.iloc[:,1:2].values
baba_real_stock_price = baba_test.iloc[:,1:2].values
nflx_real_stock_price = nflx_test.iloc[:,1:2].values


# In[ ]:


amd_total = pd.concat((AMD_train['Open'],amd_test['Open']),axis = 0)
baba_total = pd.concat((BABA_train['Open'],baba_test['Open']),axis = 0)
nflx_total = pd.concat((NFLX_train['Open'],nflx_test['Open']),axis = 0)


# In[ ]:


amdinputs = amd_total[len(amd_total) - len(amd_test)-60:].values
babainputs = baba_total[len(baba_total) - len(baba_test) - 60:].values
nflxinputs = nflx_total[len(nflx_total) - len(nflx_test) - 60:].values


# ***Converting to 2D** as it is always better if it is in higher dimension*

# In[ ]:


amdinputs = amdinputs.reshape(-1,1)
babainputs = babainputs.reshape(-1,1)
nflxinputs = nflxinputs.reshape(-1,1)


# In[ ]:


amdinputs = sc.transform(amdinputs)
babainputs = sc.transform(babainputs)
nflxinputs = sc.transform(nflxinputs)


# In[ ]:


amdinputs.shape


# In[ ]:


nflxinputs.shape


# In[ ]:


babainputs.shape


# In[ ]:


amd_x_test = []
for i in range(60,164):
    amd_x_test.append(amdinputs[i-60:i,0])
    
baba_x_test = []
for y in range(60,164):
    baba_x_test.append(babainputs[y-60:y,0])
    
nflx_x_test = []
for z in range(60,164):
    nflx_x_test.append(nflxinputs[z-60:z,0])


# In[ ]:


amd_x_test = np.array(amd_x_test)
amd_x_test.shape


# In[ ]:


baba_x_test = np.array(baba_x_test)
baba_x_test.shape


# In[ ]:


nflx_x_test = np.array(nflx_x_test)
nflx_x_test.shape


# ***Converting to 3D***

# In[ ]:


amd_x_test = np.reshape(amd_x_test, (amd_x_test.shape[0],amd_x_test.shape[1],1))
amd_x_test.shape


# In[ ]:


baba_x_test = np.reshape(baba_x_test, (baba_x_test.shape[0],baba_x_test.shape[1],1))
baba_x_test.shape


# In[ ]:


nflx_x_test = np.reshape(nflx_x_test, (nflx_x_test.shape[0],nflx_x_test.shape[1],1))
nflx_x_test.shape


# ***Prediction***

# In[ ]:


amd_predicted_price = amdregressor.predict(amd_x_test)
baba_predicted_price = babaregressor.predict(baba_x_test)


# In[ ]:


nflx_predicted_price = nflxregressor.predict(nflx_x_test)


# ***Convert back from z score format***

# In[ ]:


amd_predicted_price = sc.inverse_transform(amd_predicted_price)
baba_predicted_price = sc.inverse_transform(baba_predicted_price)


# In[ ]:


nflx_predicted_price = sc.inverse_transform(nflx_predicted_price)


# ***AMD plot***

# In[ ]:


plt.plot(amd_real_stock_price,color = 'red', label = 'Real Price')
plt.plot(amd_predicted_price, color = 'blue', label = 'Predicted Price')
plt.title('AMD Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('AMD Stock Price')
plt.legend()
plt.show()


# ***BABA plot***

# In[ ]:


plt.plot(baba_real_stock_price, color = 'red',label = 'Real Price')
plt.plot(baba_predicted_price, color = 'blue', label = 'Predicted Price')
plt.title('BABA Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('BABA Stock Price')
plt.legend()
plt.show()


# ***NFLX plot***

# In[ ]:


plt.plot(nflx_real_stock_price, color = 'red', label = 'Real Price')
plt.plot(nflx_predicted_price, color = 'blue', label = 'Predicted Price')
plt.title('NFLX Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('NFLX Stock Price')
plt.legend()
plt.show()

