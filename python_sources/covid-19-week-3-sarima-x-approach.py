#!/usr/bin/env python
# coding: utf-8

# One of the most widely used forecasting approaches for univariate time series data forecasting is Autoregressive Integrated Moving Average (ARIMA). Although the method can take into account time series data with existing trends, however, it does not support time series data with a seasonal component. In order to combat this drawback, an extension to ARIMA model that supports the direct modeling of the seasonal component will be used, denoted by S(Seasonal)ARIMA.
# 
# In my approach for the COVID-19 global forecasting competition (week 3), I will discuss the following:
# 
# ARIMA Model Limitations SARIMA Model SARIMA Model in Python Grid Search for SARIMA Hyperparameters
# 
# ARIMA Model Limitations
# ARIMA model supports both an autoregressive and moving average components. The integrated element refers to differencing method to support time series data with trend. However, the limitation of this model is that it does not support seasonal data and expects time series data that is either not seasonal or has the seasonal component removed, e.g., seasonally adjusted through seasonal differencing method.The ARIMA model is denoted by ARIMA(p,d,q), where p is the number of lag observations included in the model (also referred to as the lag order), d is the number of times that the raw observations are differenced (also called the the degree of differencing), and q that is the size of the moving average window (also called the order of moving average).
# 
# SARIMA Model
# In order to overcome the drawbacks of the ARIMA model, SARIMA or Seasonal ARIMA is considered as the modeling approach that explicitly supports univariate time series data with a seasonal component. The flexibility of this model is that it adds three new hyperparameters to specify the autoregression (AR), differencing (I), and moving average (MA) for the seasonal component of the time series data, as well as an additional parameter for the period of seasonality. The SARIMA model is denoted by SARIMA(p,d,q)(P,D,Q)m, where p is the trend autoregression order, d is the trend difference order, q is the trend moving average order, P is the seasonal autoregressive order, D is the seasonal difference order, Q is the seasonal moving average order, and m is the numbe of time steps for a single seasonal period. Configuring a SARIMA model requires selecting hyperparameters for both the seasonal and the trend components of the series.
# 
# SARIMA Model in Python
# The SARIMA model in Python is supported by the Statsmodels library.To use SARIMA model there are three steps, they are as follows:
# 
# Define the model An instance of the SARIMAX class can be created by providing the training data and the selection of model configuration parameters (also called hyperparameters of the model). The implementation is called SARIMAX instead of SARIMA since the 'X' addition means that the implementation also supports 'exogenous' variable(s).
# 
# Fit Model Make Prediction
# 
# Grid Search for SARIMA Hyperparameters
# The SARIMA model requires careful analysis and domain expertise in order to configure the model hyperparameters. An alternative approach to configuring the model is to "grid search" a suite of hyperparameter configurations in order to discover an ideal scenario.
# 
# The SARIMA model can subsume the ARIMA, ARMA, AR, and MA models through model configuration parameters. The trend and seasonal hyperparameters of the model can be configured by analyzing autocorrelation and partial autocorrelation plots (ACF & PACF), and this can take some expertise. An alternative approach is to grid search a suite of model configurations and discover which configuration work best for a specific univariate time series. For more information, please refer to the following link (https://machinelearningmastery.com/how-to-grid-search-sarima-model-hyperparameters-for-time-series-forecasting-in-python/).

# In[ ]:


# Import the necessary libraris #
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import warnings
warnings.filterwarnings(action='ignore')
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARIMA
# Define the directory for the input files (train + test + submission) #
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


# Define the criteria to evaluate the accuracy for the final forecasting model #
def RMSLE(pred,actual):
    return np.sqrt(np.mean(np.power((np.log(pred+1)-np.log(actual+1)),2)))
pd.set_option('mode.chained_assignment', None)
# Import the train & test data for COVID-19 (Week 3) #
test = pd.read_csv("../input/covid19-global-forecasting-week-3/test.csv")
train = pd.read_csv("../input/covid19-global-forecasting-week-3/train.csv")
# Replace the missing values in the train & test data sets #
train['Province_State'].fillna('', inplace=True)
test['Province_State'].fillna('', inplace=True)
# Convert the "Date" Variable in the training & test sets #
train['Date'] =  pd.to_datetime(train['Date'])
test['Date'] =  pd.to_datetime(test['Date'])
# Sort values in the training & test sets #
train = train.sort_values(['Country_Region','Province_State','Date'])
test = test.sort_values(['Country_Region','Province_State','Date'])


# In[ ]:


# Defining key dates for reference purposes #
feature_day = [1,20,50,100,200,500,1000]
def CreateInput(data):
    feature = []
    for day in feature_day:
        data.loc[:,'Number day from ' + str(day) + ' case'] = 0
        if (train[(train['Country_Region'] == country) & (train['Province_State'] == province) & (train['ConfirmedCases'] < day)]['Date'].count() > 0):
            fromday = train[(train['Country_Region'] == country) & (train['Province_State'] == province) & (train['ConfirmedCases'] < day)]['Date'].max()        
        else:
            fromday = train[(train['Country_Region'] == country) & (train['Province_State'] == province)]['Date'].min()       
        for i in range(0, len(data)):
            if (data['Date'].iloc[i] > fromday):
                day_denta = data['Date'].iloc[i] - fromday
                data['Number day from ' + str(day) + ' case'].iloc[i] = day_denta.days 
        feature = feature + ['Number day from ' + str(day) + ' case']
    
    return data[feature]


# In[ ]:


pred_data_all = pd.DataFrame()
for country in train['Country_Region'].unique():
    for province in train[(train['Country_Region'] == country)]['Province_State'].unique():
        df_train = train[(train['Country_Region'] == country) & (train['Province_State'] == province)]
        df_test = test[(test['Country_Region'] == country) & (test['Province_State'] == province)]
        X_train = CreateInput(df_train)
        y_train_confirmed = df_train['ConfirmedCases'].ravel()
        y_train_fatalities = df_train['Fatalities'].ravel()
        X_pred = CreateInput(df_test)        
        for day in sorted(feature_day,reverse = True):
            feature_use = 'Number day from ' + str(day) + ' case'
            idx = X_train[X_train[feature_use] == 0].shape[0]     
            if (X_train[X_train[feature_use] > 0].shape[0] >= 20):
                break      
        adjusted_X_train = X_train[idx:][feature_use].values.reshape(-1, 1)
        adjusted_y_train_confirmed = y_train_confirmed[idx:]
        adjusted_y_train_fatalities = y_train_fatalities[idx:] #.values.reshape(-1, 1)
        idx = X_pred[X_pred[feature_use] == 0].shape[0]    
        adjusted_X_pred = X_pred[idx:][feature_use].values.reshape(-1, 1)
        pred_data = test[(test['Country_Region'] == country) & (test['Province_State'] == province)]
        max_train_date = train[(train['Country_Region'] == country) & (train['Province_State'] == province)]['Date'].max()
        min_test_date = pred_data['Date'].min()
        model = SARIMAX(adjusted_y_train_confirmed, order=(1,1,0), 
                        measurement_error=True).fit(disp=False)
        y_hat_confirmed = model.forecast(pred_data[pred_data['Date'] > max_train_date].shape[0])
        y_train_confirmed = train[(train['Country_Region'] == country) & (train['Province_State'] == province) & (train['Date'] >=  min_test_date)]['ConfirmedCases'].values
        y_hat_confirmed = np.concatenate((y_train_confirmed,y_hat_confirmed), axis = 0)
               
        model = SARIMAX(adjusted_y_train_fatalities, order=(1,1,0), 
                        measurement_error=True).fit(disp=False)
        y_hat_fatalities = model.forecast(pred_data[pred_data['Date'] > max_train_date].shape[0])
        y_train_fatalities = train[(train['Country_Region'] == country) & (train['Province_State'] == province) & (train['Date'] >=  min_test_date)]['Fatalities'].values
        y_hat_fatalities = np.concatenate((y_train_fatalities,y_hat_fatalities), axis = 0)
        pred_data['ConfirmedCases_hat'] =  y_hat_confirmed
        pred_data['Fatalities_hat'] = y_hat_fatalities
        pred_data_all = pred_data_all.append(pred_data)


# In[ ]:


df_val = pd.merge(pred_data_all,train[['Date','Country_Region','Province_State','ConfirmedCases','Fatalities']],on=['Date','Country_Region','Province_State'], how='left')
df_val.loc[df_val['Fatalities_hat'] < 0,'Fatalities_hat'] = 0
df_val.loc[df_val['ConfirmedCases_hat'] < 0,'ConfirmedCases_hat'] = 0
df_val_3 = df_val.copy()
submission = df_val[['ForecastId','ConfirmedCases_hat','Fatalities_hat']]
submission.columns = ['ForecastId','ConfirmedCases','Fatalities']
submission.to_csv('submission.csv', index=False)

