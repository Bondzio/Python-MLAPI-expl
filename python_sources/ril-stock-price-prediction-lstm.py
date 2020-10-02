#!/usr/bin/env python
# coding: utf-8

# # RIL Stock Price Prediction using Long Short Term Memory (LSTM)
# 
# This program uses an artificial recurrent neural network called Long Short Term Memory (LSTM) to predict the closing stock price of a corporation (Reliance Industries Limited) using the past days stock price.

# # Import the libraries

# In[ ]:



import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from datetime import datetime
import math


from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# # Read the data

# In[ ]:




ril_price= pd.read_csv("../input/reliance-industries-ril-share-price-19962020/Reliance Industries 1996 to 2020.csv")
#Show the data 
ril_price


# Lots of rows have NaN value. lets delete those

# In[ ]:


ril_price=ril_price.dropna()
ril_price


# Even after removing NaN values, we have 2200+ rows and 9+ years of data. good enough for the analysis

# In[ ]:


ril_price.info()


# date is a string object not a date. lets fix this

# In[ ]:


ril_price["Date"]=pd.to_datetime(ril_price["Date"], format="%d-%m-%Y")


ril_price["Date"]

ril_price.set_index('Date', inplace=True)
ril_price.info()


# In[ ]:


ril_price.describe()


# # Create a Chart to visualize the data.

# In[ ]:


#Visualize the closing price history
plt.figure(figsize=(16,8))
plt.title('Reliance Industries Close Price History')
plt.plot(ril_price['Close'])
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price INR',fontsize=18)
plt.show()


# In[ ]:


#Create a new dataframe with only the 'Close' column
data = ril_price.filter(['Close'])
#Converting the dataframe to a numpy array
dataset = data.values
#Get /Compute the number of rows to train the model on
training_data_len = math.ceil( len(dataset) *.8) 


# In[ ]:


#Scale the all of the data to be values between 0 and 1 
scaler = MinMaxScaler(feature_range=(0, 1)) 
scaled_data = scaler.fit_transform(dataset)


# In[ ]:


#Create the scaled training data set 
train_data = scaled_data[0:training_data_len  , : ]
#Split the data into x_train and y_train data sets
x_train=[]
y_train = []
for i in range(60,len(train_data)):
    x_train.append(train_data[i-60:i,0])
    y_train.append(train_data[i,0])


# In[ ]:


#Convert x_train and y_train to numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)


# In[ ]:


#Reshape the data into the shape accepted by the LSTM
x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))


# Build the LSTM model to have two LSTM layers with 50 neurons and two Dense layers, one with 25 neurons and the other with 1 neuron.

# In[ ]:


#Build the LSTM network model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dense(units=25))
model.add(Dense(units=1))


# Compile the model using the mean squared error (MSE) loss function and the adam optimizer.

# In[ ]:


#Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')


# In[ ]:


#Train the model
model.fit(x_train, y_train, batch_size=1, epochs=1)


# In[ ]:


#Test data set
test_data = scaled_data[training_data_len - 60: , : ]
#Create the x_test and y_test data sets
x_test = []
y_test =  dataset[training_data_len : , : ] #Get all of the rows from index 1603 to the rest and all of the columns (in this case it's only column 'Close'), so 2003 - 1603 = 400 rows of data
for i in range(60,len(test_data)):
    x_test.append(test_data[i-60:i,0])


# In[ ]:


#Convert x_test to a numpy array 
x_test = np.array(x_test)


# In[ ]:


#Reshape the data into the shape accepted by the LSTM
x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))


# In[ ]:


#Getting the models predicted price values
predictions = model.predict(x_test) 
predictions = scaler.inverse_transform(predictions)#Undo scaling


# In[ ]:


#Calculate/Get the value of RMSE
rmse=np.sqrt(np.mean(((predictions- y_test)**2)))
rmse


# In[ ]:


#Plot/Create the data for the graph
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions
#Visualize the data
plt.figure(figsize=(16,8))
plt.title('RIL Share Price Prediction Model using LSTM')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price INR', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()


# In[ ]:


#Show the valid and predicted prices
valid


# In[ ]:


new_df = ril_price.filter(['Close'])


# In[ ]:


#Get the last 60 day closing price 
last_60_days = new_df[-60:].values

#Scale the data to be values between 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)

#Create an empty list
X_test = []

#Append teh past 60 days
X_test.append(last_60_days_scaled)

#Convert the X_test data set to a numpy array
X_test = np.array(X_test)

#Reshape the data
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

#Get the predicted scaled price
pred_price = model.predict(X_test)

#undo the scaling 
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)

