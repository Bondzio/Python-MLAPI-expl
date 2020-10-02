#!/usr/bin/env python
# coding: utf-8

# # We are using RNN here

# Here we are using LSTM 
# this will predict upward and downward trends of Google stock prices

# Importing the libraries

# In[ ]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


# Importing the training set

# In[ ]:


training_data=pd.read_csv('../input/Google_Stock_Price_Train.csv')
training_set=training_data.iloc[:,1:2].values
print(training_data)
print(training_set)


# Feature scaling

# In[ ]:


from sklearn.preprocessing import MinMaxScaler
sc=MinMaxScaler(feature_range=(0, 1))
training_set_scaler=sc.fit_transform(training_set)
print(training_set_scaler)


# Creating a data structure with 60 timesteps and 1 output

# In[ ]:


x_train=[]
y_train =[]
for i in range(60,1258):
    x_train.append(training_set_scaler[i-60:i,0])
    y_train.append(training_set_scaler[i,0])
x_train,y_train=np.array(x_train),np.array(y_train)    
print(x_train)
print(y_train)


# Reshaping

# In[ ]:


x_train=np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
print(x_train)


# ## ***Building RNN***
# Dropout Regularization will be used to prevent overfitting

# Importing the keras libraries

# In[ ]:


from keras.models import Sequential 
#sequential claas is used to create nueral network object representing sequencning of layers
from keras.layers import Dense
#dense claas is used to add output layer
from keras.layers import LSTM
#LSTM claas is used to add LSTM layer
from keras.layers import Dropout
#Dropout class is used to create dropout regularization


# Initialising the RNN

# In[ ]:


regressor=Sequential()


# Adding the first LSTM layer and some Dropout Regularization

# In[ ]:


regressor.add(LSTM(units=50,return_sequences=True,input_shape=(x_train.shape[1],1)))
regressor.add(Dropout(0.2))


# Adding the first 2nd layer and some Dropout Regularization

# In[ ]:


regressor.add(LSTM(units=50,return_sequences=True))
regressor.add(Dropout(0.2))


# Adding the first 3rd layer and some Dropout Regularization

# In[ ]:


regressor.add(LSTM(units=50,return_sequences=True))
regressor.add(Dropout(0.2))


# Adding the first 4th layer and some Dropout Regularization

# In[ ]:


regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))


# Adding the output layer

# In[ ]:


regressor.add(Dense(units=1))


# Compiling the RNN

# In[ ]:


regressor.compile(optimizer='adam',loss='mean_squared_error')


# Fitting the RNN to the training set

# In[ ]:


regressor.fit(x_train,y_train,epochs=100,batch_size=32)


# # Making the prediction and visualising the result

# Getting the real stock price of 2017

# In[ ]:


test_data=pd.read_csv('../input/Google_Stock_Price_Test.csv')
real_stock_price=test_data.iloc[:,1:2].values
print(test_data)
print(real_stock_price)


# Getting the predicted stock price of 2017

# In[ ]:


dataset_total=pd.concat((training_data['Open'],test_data['Open']),axis=0)
# axis=0 for vertical concatination
# axis=1 for horizontal concatination
inputs=dataset_total[len(dataset_total)-len(test_data)-60:].values
inputs=inputs.reshape(-1,1)
inputs=sc.transform(inputs)
x_test=[]
for i in range(60,80):
    x_test.append(inputs[i-60:i,0])
x_test=np.array(x_test)    
x_test=np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))
pridected_stock_prices=regressor.predict(x_test)
pridected_stock_prices=sc.inverse_transform(pridected_stock_prices)
print(pridected_stock_prices)


# In[ ]:


#Visualising the results
plt.plot(real_stock_price,color='red',label='Real google stock price')
plt.plot(pridected_stock_prices,color='blue',label='Predicted google stock price')
plt.title('Google stock price prediction')
plt.xlabel('Time')
plt.ylabel('Google stock price')
plt.legend()
plt.show()

