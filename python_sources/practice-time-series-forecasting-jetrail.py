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


# Time Series problem involving prediction of number of commuters of JetRail, a new high speed rail service by Unicorn Investors. We are provided with 2 years of data(Aug 2012-Sept 2014) and using this data we have to forecast the number of commuters

# In[ ]:


import pandas as pd


# In[ ]:


data = pd.read_csv('../input/timeseries/Train.csv')


# In[ ]:


data.head()


# In[ ]:


data.shape


# In[ ]:


#Defining the train and test in 80-20 split
train = data[0:14630]
test = data[14630:]


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


#Function to do some processing
def processing(df):
        df.Timestamp = pd.to_datetime(df.Datetime,format='%d-%m-%Y %H:%M') 
        df.index = df.Timestamp 
        df = df.resample('D').mean()
        df.drop('ID',1,inplace = True)
        return df


# In[ ]:


#Passing through the function
train = processing(train)
test =processing(test)
data = processing(data)


# In[ ]:


from statsmodels.tsa.seasonal import seasonal_decompose
decompose = seasonal_decompose(data, model='multiplicative')
fig = plt.figure()
fig = decompose.plot()
#There is seasonality in the below data, there is also trend


# In[ ]:


#Deriving the function of Dickey fuller test for checking the stationarity
from statsmodels.tsa.stattools import adfuller
def adf_test(series):
    result = adfuller(series.dropna(),autolag='AIC')
    if result[1] <= 0.05:
        print("Data  is stationary")
    else:
        print("Data  is non-stationary")


# In[ ]:


adf_test(data["Count"])


# In[ ]:


#Seasonal difference
data["Count diff"] = data["Count"]- data["Count"].shift(12)
data["Count c"].dropna(inplace=True)


# In[ ]:


adf_test(data["Count diff"])


# In[ ]:


#Auto correlation plot and Partial correlation plot
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plot_acf(data["Count diff"], lags= 60, alpha=0.05);
plot_pacf(data["Count diff"], lags= 60, alpha=0.05);


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt
#Plotting data
train.Count.plot(figsize=(15,8), title= 'Daily Commuters', fontsize=14)
test.Count.plot(figsize=(15,8), title= 'Daily Commuters', fontsize=14)
plt.show()


# Naive Approach

# In[ ]:


dd= np.asarray(train.Count)
y_hat = test.copy()
y_hat['naive'] = dd[len(dd)-1]
plt.figure(figsize=(12,8))
plt.plot(train.index, train['Count'], label='Train')
plt.plot(test.index,test['Count'], label='Test')
plt.plot(y_hat.index,y_hat['naive'], label='Naive Forecast')
plt.legend(loc='best')
plt.title("Naive Forecast")
plt.show()
#Clearly this is not helping, this could be usefull if wer are using a stable data 


# Simple Average

# In[ ]:


y_hat_avg = test.copy()
y_hat_avg['avg_forecast'] = train['Count'].mean()
plt.figure(figsize=(12,8))
plt.plot(train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['avg_forecast'], label='Average Forecast')
plt.legend(loc='best')
plt.show()


# Moving Average

# In[ ]:


y_hat_avg = test.copy()
y_hat_avg['moving_avg_forecast'] = train['Count'].rolling(60).mean().iloc[-1]
plt.figure(figsize=(16,8))
plt.plot(train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['moving_avg_forecast'], label='Moving Average Forecast')
plt.legend(loc='best')
plt.show()


# Simple Exponential smoothing

# In[ ]:


from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
y_hat_avg = test.copy()
fit2 = SimpleExpSmoothing(np.asarray(train['Count'])).fit(smoothing_level=0.1,optimized=False)
y_hat_avg['SES'] = fit2.forecast(len(test))
plt.figure(figsize=(16,8))
plt.plot(train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['SES'], label='SES')
plt.legend(loc='best')
plt.show()


# Holt's Linear trend method

# In[ ]:


import statsmodels.api as sm
sm.tsa.seasonal_decompose(train.Count).plot()
result = sm.tsa.stattools.adfuller(train.Count)
plt.show()


# In[ ]:


y_hat_avg = test.copy()

fit1 = Holt(np.asarray(train['Count'])).fit(smoothing_level = 0.3,smoothing_slope = 0.1)
y_hat_avg['Holt_linear'] = fit1.forecast(len(test))

plt.figure(figsize=(16,8))
plt.plot(train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['Holt_linear'], label='Holt_linear')
plt.legend(loc='best')
plt.show()


# Holt's Winter 

# In[ ]:


y_hat_avg = test.copy()
fit1 = ExponentialSmoothing(np.asarray(train['Count']) ,seasonal_periods=7 ,trend='add', seasonal='add',).fit()
y_hat_avg['Holt_Winter'] = fit1.forecast(len(test))
plt.figure(figsize=(16,8))
plt.plot( train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['Holt_Winter'], label='Holt_Winter')
plt.legend(loc='best')
plt.show()


# Arima

# In[ ]:


#order = (p,d,q)
#p- acf plot lag
#q- pacf plot lag
#d- diffencing
y_hat_avg = test.copy()
fit1 = sm.tsa.statespace.SARIMAX(train.Count, order=(0, 0,9 ),seasonal_order=(0,1,1,7)).fit()
y_hat_avg['SARIMA'] = fit1.predict(start="2014-04-26", end="2014-09-25	", dynamic=True)
plt.figure(figsize=(16,8))
plt.plot( train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['SARIMA'], label='SARIMA')
plt.legend(loc='best')
plt.show()


# In[ ]:


import warnings
from pandas import read_csv
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# evaluate an ARIMA model for a given order (p,d,q) and return RMSE
def evaluate_arima_model(X, arima_order):
	# prepare training dataset
	X = X.astype('float32')
	train_size = int(len(X) * 0.50)
	train, test = X[0:train_size], X[train_size:]
	history = [x for x in train]
	# make predictions
	predictions = list()
	for t in range(len(test)):
		model = ARIMA(history, order=arima_order)
		model_fit = model.fit(disp=0)
		yhat = model_fit.forecast()[0]
		predictions.append(yhat)
		history.append(test[t])
	# calculate out of sample error
	mse = mean_squared_error(test, predictions)
	rmse = sqrt(mse)
	return rmse

# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
	dataset = dataset.astype('float32')
	best_score, best_cfg = float("inf"), None
	for p in p_values:
		for d in d_values:
			for q in q_values:
				order = (p,d,q)
				try:
					mse = evaluate_arima_model(dataset, order)
					if mse < best_score:
						best_score, best_cfg = mse, order
					print('ARIMA%s MSE=%.3f' % (order,mse))
				except:
					continue
	print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))

# load dataset
dataset = pd.read_csv('../input/timeseries/Train.csv')
series = processing(dataset)
# evaluate parameters
p_values = range(0,13)
d_values = range(0, 4)
q_values = range(0, 13)
warnings.filterwarnings("ignore")
evaluate_models(series.values, p_values, d_values, q_values)


# In[ ]:




