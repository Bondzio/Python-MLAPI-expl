#!/usr/bin/env python
# coding: utf-8

# <hr>
# 
# ### Context
# * Google Stock Price
# 
# ### Content of Dataset
# * Historical stock prices (last 5 years) for all companies currently found on the S&P 500 index.
# 
# * All the files have the following columns:
#   * Date - in format: yy-mm-dd
#   * Open - price of the stock at market open (this is NYSE data so all in USD)
#   * High - Highest price reached in the day
#   * Low Close - Lowest price reached in the day
#   * Volume - Number of shares traded
#   * Name - the stock's ticker name
#   
# <hr>

# ## Content of Kernel
# * [Load Libraries](#1)
# * [Loading and Preprocessing Data](#2)
# * [Feature Scaling](#3)
# * [Data Ploting](#4)
# * [Creating a Data Structure for Train and Test](#5)
# * [Create RNN Model](#6)
#     * [Predictions and Visualising RNN Model](#7)
# * [Univariate LSTM Models](#8) 
#     * [Preprocessing Data](#9)
#     * [1 - Vanilla LSTM](#10)
#     * [2 - Stacked LSTM](#11)
#     * [3 - Bidirectional LSTM](#12)
#     * [4 - CNN LSTM](#13)
# * [Reference](#14) 
# 
# <hr>

# <a id="1"></a>
# ## Load Libraries

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import SimpleRNN
from keras.layers import Dropout
#
import plotly.graph_objs as go
import plotly.offline as offline
#
import warnings
warnings.filterwarnings('ignore')
#
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# <a id="2"></a>
# ## Loading and Preprocessing Data

# In[ ]:


data = pd.read_csv("/kaggle/input/sandp500/individual_stocks_5yr/individual_stocks_5yr/GOOG_data.csv")
data.head()


# In[ ]:


data.shape


# In[ ]:


data.info()


# In[ ]:


trace_high = go.Scatter(x=data.date,
                        y=data.high,
                        
                        name = "Google High",
                        
                        line = dict(color = '#6699FF')
                       )
trace_low = go.Scatter( x=data.date,
                        y=data.low,
                        
                        name = "Google Low",
                        
                        line = dict(color = '#FF6633')
                       )
trace_open = go.Scatter( x=data.date,
                        y=data.open,
                        
                        name = "Google Open",
                        
                        line = dict(color = 'red')
                       )
trace_close = go.Scatter( x=data.date,
                        y=data.close,
                        
                        name = "Google Close",
                        
                        line = dict(color = 'black')
                       )
data_figure = [trace_open,trace_high, trace_low,trace_close]
layout = dict(
    
    title = 'Google Stock Price Data ',
    
    xaxis = dict(rangeselector = dict(buttons = list([dict(count = 1,
                                                           label = '1m',
                                                           step = 'month',
                                                           stepmode = 'todate',
                                                          visible = True),
                                                      
                                                  dict(count = 3,
                                                           label = '3m',
                                                           step = 'month',
                                                           stepmode = 'backward',
                                                          visible = True),
                                                      
                                                      dict(count = 6,
                                                           label = '6m',
                                                           step = 'month',
                                                           stepmode = 'backward',
                                                          visible = True),
                                                  
                                                      dict(step = 'all')])
                                     ),
                 
                 rangeslider=dict(visible = True),
                 type='date'
    )
)
fig = dict(data=data_figure, 
           layout=layout)

offline.iplot(fig)


# #### Plot the candlesticks
# The plot has the following components:
# * A bounding box whose y values represent the range between the stock's open and close prices 
# * A green box represents a higher close value than open (i.e. stock price went up that day)
# * The box is red when the stock closed lower
# * The vertical lines (bars above and below the box) show the range of intra-day high and low prices
# * The vertical lines are capped at the top by horizontal lines called whiserks. By default, the width of the whisker is 0 which is why we don't see them
# 
# Notice that a slider appears by default along the X axis

# In[ ]:


data_temp = data.iloc[965:975,:]
trace = go.Candlestick(x = data_temp.date,                       
                       open = data_temp.open,                       
                       high = data_temp.high,                       
                       low = data_temp.low,                       
                       close = data_temp.close,
                      increasing = dict(fillcolor = 'greenyellow', 
                                         line = dict(color = 'green', 
                                                     width = 3
                                                    )),
                       decreasing = dict(fillcolor = 'lightcoral'),                       
                       whiskerwidth = 0.2)
data_figure_2 = [trace]
layout = dict(title = 'Google Stock Price Data ')
fig = dict(data=data_figure_2, 
           layout=layout)
offline.iplot(fig)


# ## Open Price Animation

# In[ ]:


data_temp = data.iloc[875:975,:]
data_open = list(data_temp['open'])
dateList = list(data_temp['date'])
xList = []
yList = []
framesList = []
for i in range(len(dateList)):
    
    xList.append(dateList[i])
    yList.append(data_open[i])
    
    framesList.append(dict(data = [dict(x = xList.copy(), y = yList.copy())]))
#
playButton = dict(label = 'Play',
                  method= 'animate',
                  args= [None, 
                         dict(fromcurrent = True, 
                              transition = dict(duration = 200), 
                              frame = dict(duration = 100)
                             )
                        ]
                 )
#
pauseButton = dict(label = 'Pause',
                  method= 'animate',
                  args= [[None], dict(mode = 'immediate')]
                 )
#
layout = go.Layout(xaxis = dict(range = [dateList[0], dateList[-1]]), 
                   yaxis = dict(range = [0, 1 + max(data_open)]),
                   
                   updatemenus = [dict(type = 'buttons',
                                       buttons = [playButton, pauseButton]
                                       )
                                 ]
                  )
#
fig = dict(data=[{}], 
           layout=layout, 
           frames = framesList)

offline.iplot(fig)


# <hr>

# In[ ]:


# Split Data
dataset_train = data.loc[0:750,:]
dataset_test  = data.loc[750:,:]


# <a id="3"></a>
# ## Feature Scaling

# In[ ]:


scaler = MinMaxScaler(feature_range = (0, 1))
train_scaled = scaler.fit_transform(dataset_train.loc[:,["open"]].values)
train_scaled


# <a id="4"></a>
# ## Data Ploting

# In[ ]:


f,ax = plt.subplots(figsize = (30,7))
plt.plot(train_scaled)
plt.show()


# <a id="5"></a>
# ## Creating a data structure with 50 timesteps and 1 output

# In[ ]:


X_train = []
y_train = []
timesteps = 50
for i in range(timesteps, 751):
    X_train.append(train_scaled[i-timesteps:i, 0])
    y_train.append(train_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)


# In[ ]:


# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
print("X:",X_train)
print("X size:",X_train.size)


# In[ ]:


print("Y:",y_train)
print("Y size:",y_train.size)


# <a id="6"></a>
# ## Create RNN Model

# In[ ]:


# Initialising the RNN
regressor = Sequential()

# Adding the first RNN layer and some Dropout regularisation
regressor.add(SimpleRNN(units = 50,activation='tanh', return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

# Adding a second RNN layer and some Dropout regularisation
regressor.add(SimpleRNN(units = 50,activation='tanh', return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a third RNN layer and some Dropout regularisation
regressor.add(SimpleRNN(units = 50,activation='tanh', return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a fourth RNN layer and some Dropout regularisation
regressor.add(SimpleRNN(units = 50))
regressor.add(Dropout(0.2))

# Adding the output layer
regressor.add(Dense(units = 1))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
regressor.fit(X_train, y_train, epochs = 250, batch_size = 32)


# <a id="7"></a>
# ## Predictions and Visualising RNN Model

# In[ ]:


dataset_test.head()


# In[ ]:


real_stock_price = dataset_test.loc[:,["open"]].values
real_stock_price


# In[ ]:


# Getting the predicted stock price of 2017
dataset_total = pd.concat((dataset_train['open'], dataset_test['open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - timesteps:].values.reshape(-1,1)
inputs = scaler.transform(inputs)  # min max scaler
inputs


# In[ ]:


X_test = []
for i in range(timesteps, 275):
    X_test.append(inputs[i-timesteps:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)

# Visualising the results
f,ax = plt.subplots(figsize = (30,7))
plt.plot(real_stock_price, color = 'red', label = 'Real Google Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()


# <a id="8"></a>
# ## Univariate LSTM Models

# In[ ]:


import numpy
import math
from keras.layers import Bidirectional
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


# In[ ]:


data = pd.read_csv("/kaggle/input/sandp500/individual_stocks_5yr/individual_stocks_5yr/GOOG_data.csv")
data.head()


# <a id="9"></a>
# ## Preprocessing Data
# * reshape
# * change type
# * scaling
# * train test split
# * Create dataset

# In[ ]:


# reshape
# Choice "open" feature:
dataset = data.iloc[:,1].values
dataset = dataset.reshape(-1,1) # (975,) sometimes can be problem
dataset = dataset.astype("float32")
dataset.shape


# In[ ]:


# scaling 
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)


# In[ ]:


# train test split
train_size = int(len(dataset) * 0.75) # Split dataset 75% for train set, 25% for test set
test_size = len(dataset) - train_size
train = dataset[0:train_size,:]
test = dataset[train_size:len(dataset),:]
print("train size: {}, test size: {} ".format(len(train), len(test)))


# In[ ]:


time_stemp = 10
dataX = []
dataY = []
for i in range(len(train)-time_stemp-1):
    a = train[i:(i+time_stemp), 0]
    dataX.append(a)
    dataY.append(train[i + time_stemp, 0])
trainX = numpy.array(dataX)
trainY = numpy.array(dataY)  


# In[ ]:


dataX = []
dataY = []
for i in range(len(test)-time_stemp-1):
    a = test[i:(i+time_stemp), 0]
    dataX.append(a)
    dataY.append(test[i + time_stemp, 0])
testX = numpy.array(dataX)
testY = numpy.array(dataY)  


# In[ ]:


trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))


# <a id="10"></a>
# ## 1 - Vanilla LSTM
# * A Vanilla LSTM is an LSTM model that has a single hidden layer of LSTM units, and an output layer used to make a prediction.

# In[ ]:


# model
model = Sequential()
model.add(LSTM(10, input_shape=(1, time_stemp))) # 10 lstm neuron(block)
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=50, batch_size=1)


# In[ ]:


trainPredict = model.predict(trainX)
testPredict = model.predict(testX)
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore_vanilla = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore_vanilla))


# In[ ]:


# shifting train
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[time_stemp:len(trainPredict)+time_stemp, :] = trainPredict
# shifting test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict)+(time_stemp*2)+1:len(dataset)-1, :] = testPredict
# plot baseline and predictions
f,ax = plt.subplots(figsize = (30,7))
plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()


# <a id="11"></a>
# ## 2 - Stacked LSTM
# * Multiple hidden LSTM layers can be stacked one on top of another in what is referred to as a Stacked LSTM model.

# In[ ]:


# Need to Preprocessing 
data = pd.read_csv("/kaggle/input/sandp500/individual_stocks_5yr/individual_stocks_5yr/GOOG_data.csv")
dataset = data.iloc[:,1].values
dataset = dataset.reshape(-1,1) # (975,) sometimes can be problem
dataset = dataset.astype("float32")
# scaling 
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)
# train test split
train_size = int(len(dataset) * 0.75) # Split dataset 75% for train set, 25% for test set
test_size = len(dataset) - train_size
train = dataset[0:train_size,:]
test = dataset[train_size:len(dataset),:]
time_stemp = 10
dataX = []
dataY = []
for i in range(len(train)-time_stemp-1):
    a = train[i:(i+time_stemp), 0]
    dataX.append(a)
    dataY.append(train[i + time_stemp, 0])
trainX = numpy.array(dataX)
trainY = numpy.array(dataY)  
dataX = []
dataY = []
for i in range(len(test)-time_stemp-1):
    a = test[i:(i+time_stemp), 0]
    dataX.append(a)
    dataY.append(test[i + time_stemp, 0])
testX = numpy.array(dataX)
testY = numpy.array(dataY)  
trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))


# In[ ]:


# define model
model = Sequential()
model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(1,time_stemp)))
model.add(LSTM(50, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
model.fit(trainX, trainY, epochs=50, batch_size=1)


# In[ ]:


trainPredict = model.predict(trainX)
testPredict = model.predict(testX)
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore_Stacked = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore_Stacked))


# In[ ]:


# shifting train
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[time_stemp:len(trainPredict)+time_stemp, :] = trainPredict
# shifting test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict)+(time_stemp*2)+1:len(dataset)-1, :] = testPredict
# plot baseline and predictions
f,ax = plt.subplots(figsize = (30,7))
plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()


# <a id="12"></a>
# ## 3 - Bidirectional LSTM
# * On some sequence prediction problems, it can be beneficial to allow the LSTM model to learn the input sequence both forward and backwards and concatenate both interpretations.

# In[ ]:


# Need to Preprocessing 
data = pd.read_csv("/kaggle/input/sandp500/individual_stocks_5yr/individual_stocks_5yr/GOOG_data.csv")
dataset = data.iloc[:,1].values
dataset = dataset.reshape(-1,1) # (975,) sometimes can be problem
dataset = dataset.astype("float32")
# scaling 
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)
# train test split
train_size = int(len(dataset) * 0.75) # Split dataset 75% for train set, 25% for test set
test_size = len(dataset) - train_size
train = dataset[0:train_size,:]
test = dataset[train_size:len(dataset),:]
time_stemp = 10
dataX = []
dataY = []
for i in range(len(train)-time_stemp-1):
    a = train[i:(i+time_stemp), 0]
    dataX.append(a)
    dataY.append(train[i + time_stemp, 0])
trainX = numpy.array(dataX)
trainY = numpy.array(dataY)  
dataX = []
dataY = []
for i in range(len(test)-time_stemp-1):
    a = test[i:(i+time_stemp), 0]
    dataX.append(a)
    dataY.append(test[i + time_stemp, 0])
testX = numpy.array(dataX)
testY = numpy.array(dataY)  
trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))


# In[ ]:


# define model
model = Sequential()
model.add(Bidirectional(LSTM(50, activation='relu'), input_shape=(1,time_stemp)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
model.fit(trainX, trainY, epochs=50, batch_size=1)


# In[ ]:


trainPredict = model.predict(trainX)
testPredict = model.predict(testX)
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore_bidirectional = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore_bidirectional))


# In[ ]:


# shifting train
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[time_stemp:len(trainPredict)+time_stemp, :] = trainPredict
# shifting test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict)+(time_stemp*2)+1:len(dataset)-1, :] = testPredict
# plot baseline and predictions
f,ax = plt.subplots(figsize = (30,7))
plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()


# <a id="13"></a>
# ## 4 - CNN LSTM
# * A CNN model can be used in a hybrid model with an LSTM backend where the CNN is used to interpret subsequences of input that together are provided as a sequence to an LSTM model to interpret.

# In[ ]:


# Need to Preprocessing 
data = pd.read_csv("/kaggle/input/sandp500/individual_stocks_5yr/individual_stocks_5yr/GOOG_data.csv")
dataset = data.iloc[:,1].values
dataset = dataset.reshape(-1,1) # (975,) sometimes can be problem
dataset = dataset.astype("float32")
# scaling 
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)
# train test split
train_size = int(len(dataset) * 0.75) # Split dataset 75% for train set, 25% for test set
test_size = len(dataset) - train_size
train = dataset[0:train_size,:]
test = dataset[train_size:len(dataset),:]
time_stemp = 10
dataX = []
dataY = []
for i in range(len(train)-time_stemp-1):
    a = train[i:(i+time_stemp), 0]
    dataX.append(a)
    dataY.append(train[i + time_stemp, 0])
trainX = numpy.array(dataX)
trainY = numpy.array(dataY)  
dataX = []
dataY = []
for i in range(len(test)-time_stemp-1):
    a = test[i:(i+time_stemp), 0]
    dataX.append(a)
    dataY.append(test[i + time_stemp, 0])
testX = numpy.array(dataX)
testY = numpy.array(dataY)  
trainX = numpy.reshape(trainX, (trainX.shape[0], 1,1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1,1, testX.shape[1]))


# In[ ]:


from keras.layers import Flatten
from keras.layers import TimeDistributed
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D


# In[ ]:


model = Sequential()
model.add(TimeDistributed(Conv1D(filters=64, kernel_size=1, activation='relu'), input_shape=(None,1, time_stemp)))
model.add(TimeDistributed(MaxPooling1D(pool_size=2, padding='same')))
model.add(TimeDistributed(Flatten()))
model.add(LSTM(50, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
model.fit(trainX, trainY, epochs=50,batch_size=1)


# In[ ]:


trainPredict = model.predict(trainX)
testPredict = model.predict(testX)
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore_cnn = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore_cnn))


# In[ ]:


# shifting train
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[time_stemp:len(trainPredict)+time_stemp, :] = trainPredict
# shifting test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict)+(time_stemp*2)+1:len(dataset)-1, :] = testPredict
# plot baseline and predictions
f,ax = plt.subplots(figsize = (30,7))
plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()


# <a id="14"></a>
# ## Reference

# https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/
