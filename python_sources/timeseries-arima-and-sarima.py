#!/usr/bin/env python
# coding: utf-8

# Using previous years data of Alcohol sales Forecated 12 months data using ARIMA, SARIMA and Holt-Winters method (additive and multiplicative)

# In[ ]:


import warnings 
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

color = sns.color_palette()
sns.set_style('darkgrid')


# Parsing the date as the years was given as 92,93,94 and so on. NOTE %y is for 2 digit year and %Y is for 4 digit year

# In[ ]:


data = pd.read_csv('../input/liquor.csv')
data['Period'] = pd.to_datetime(data['Period'], format="%m/%d/%y")

data.head()


# In[ ]:


int(0.75*(len(data)))


# Taking train set as 75% 219 months

# In[ ]:


train = data[:int(0.75*(len(data)))]
valid = data[int(0.75*(len(data))):]


# In[ ]:


print("Length of test dataset ",len(valid))
valid.head()


# In[ ]:


train_df = train
train_df['Value'] = train_df['Value'].astype(float)

train_df.head()


# In[ ]:


#plotting full data
sns.lineplot(x="Period", y="Value",legend = 'full' , data=data)


# In[ ]:


#plotting Train data
sns.lineplot(x="Period", y="Value",legend = 'full' , data=train_df)


# In[ ]:


#checking the seasonality of the data and the trend.
from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(train_df['Value'], model='additive', freq=12)

fig = plt.figure()  
fig = result.plot()  
fig.set_size_inches(11, 7)


# Looks like there is an upward trend in data with similar seasonality.
# Below is a function to test stationarity of data using Dickey Fuller test and also plotting the rolling statistics.
# In Dickey Fuller test checking the p value if it less than 5% then the series is considered to be stationary.

# In[ ]:


from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries, window = 12, cutoff = 0.01):

    #Determing rolling statistics
    rolmean = timeseries.rolling(window).mean()
    rolstd = timeseries.rolling(window).std()

    #Plot rolling statistics:
    fig = plt.figure(figsize=(12, 8))
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()
    
    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC', maxlag = 20 )
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    pvalue = dftest[1]
    if pvalue < cutoff:
        print('p-value = %.4f. The series is likely stationary.' % pvalue)
    else:
        print('p-value = %.4f. The series is likely non-stationary.' % pvalue)
    
    print(dfoutput)


# In[ ]:


test_stationarity(train_df['Value'])


# In[ ]:


first_diff = train_df.Value - train_df.Value.shift(1)
first_diff = first_diff.dropna(inplace = False)
test_stationarity(first_diff, window = 12)


# Plotting autocorrelation(ACF) and partial autocorrelation(PACF) plots of undifferenced and differenced series

# In[ ]:


fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(train_df.Value, lags=40, ax=ax1) 
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(train_df.Value, lags=40, ax=ax2)


# In[ ]:


fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(first_diff, lags=24, ax=ax1)#plotting till 24 lags coz after 24 lags we get unsually high values
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(first_diff, lags=24, ax=ax2)


# In[ ]:


arima_mod = sm.tsa.ARIMA(train_df.Value, (0,1,1)).fit()
print(arima_mod.summary())


# In[ ]:


#Residuals plot
from pandas import DataFrame
resid = DataFrame(arima_mod.resid)
resid.plot()


# In[ ]:


#Residuals distribution
resid.plot(kind='kde')


# In[ ]:


#the residual mean is near 0 therefore acceptable
resid.describe()


# In[ ]:


# forecasting with model formed on train data
forecast = arima_mod.forecast(steps = len(valid))


# In[ ]:


forecast[0]


# In[ ]:


#plotting the forcasted values against validation dataset
forecast_1 = pd.DataFrame(forecast[0],index = valid.index,columns=['Prediction'])
plt.plot(train.Value, label='Train')
plt.plot(valid.Value, label='Valid')
plt.plot(forecast_1, label='Prediction')
plt.legend()
plt.show()


# In[ ]:


len(valid)


# In[ ]:


len(forecast_1)


# In[ ]:


from math import sqrt
from sklearn.metrics import mean_squared_error

rms = sqrt(mean_squared_error(valid.Value,forecast_1))
print("Validation RMS",rms)


# In[ ]:


#defining MAPE function
import numpy as np
def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


# In[ ]:


#Checking the validity of the forecast 
mape = mean_absolute_percentage_error(valid.Value,forecast_1)
print("The MAPE for Validation is ",mape)


# In[ ]:


forecast = arima_mod.forecast(steps = 100)
print(forecast[0])


# In[ ]:


#predicting alcohol sales for next 12 months
forecast_2 = pd.DataFrame(forecast[0],index = np.array(range(206,306)),columns=['Prediction'])
plt.plot(data.Value, label='Observed')
plt.plot(forecast_2, label='Prediction')
plt.legend()
plt.show()


# In[ ]:


#Including seasonality in ARIMA model
#Checking the best possible combinations for seasonal ARIMA model.
import itertools
p = d = q = range(0, 3)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))


# In[ ]:


#getting AIC value for possible combination of ARIMA and seasonality parameters
cnt = 0
for param in pdq:
    for param_seasonal in seasonal_pdq:
        
        mod = sm.tsa.statespace.SARIMAX(train.Value,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
        results = mod.fit()
        cnt += 1
        if cnt % 50 :
            print('Current Iter - {}, ARIMA{}x{} 12 - AIC:{}'.format(cnt, param, param_seasonal, results.aic))


# In[ ]:


#choosing ARIMA model with lowest AIC value
#Current Iter - 711, ARIMA(2, 2, 2)x(0, 2, 2, 12) 12 - AIC:1920.01953
mod = sm.tsa.statespace.SARIMAX(train_df.Value,
                                order=(2, 2, 2),
                                seasonal_order=(0, 2, 2, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])


# In[ ]:


## Validating Forecast on Test data
pred = results.get_prediction(start=175, dynamic=False)
pred_ci = pred.conf_int()
ax = train.Value.plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Index')
ax.set_ylabel('Sales')
plt.legend()


# In[ ]:


pred_uc = results.get_forecast(steps=len(valid))
pred_ci = pred_uc.conf_int()
ax = valid.Value.plot(label='observed')
pred_uc.predicted_mean.plot(ax=ax, label='Forecast', figsize=(12, 8))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Index')
ax.set_ylabel('Sales')
plt.legend()


# In[ ]:


y_forecasted = pred_uc.predicted_mean
y_truth = valid.Value
rms = sqrt(mean_squared_error(y_truth,y_forecasted))
print("RMS of SARIMAX ",rms)


# In[ ]:


mape = mean_absolute_percentage_error(y_truth,y_forecasted)
print("The MAPE of SARIMAX {}",mape)


# In[ ]:


#predicting alcohol sales for next 12 months
pred_uc = results.get_forecast(steps=86)
pred_ci = pred_uc.conf_int()
ax = data.Value.plot(label='observed')
pred_uc.predicted_mean.plot(ax=ax, label='Forecast', figsize=(12, 8))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Index')
ax.set_ylabel('Sales')
plt.legend()


# In[ ]:


from statsmodels.tsa.api import ExponentialSmoothing
y_hat_avg = valid.copy()
fit1 = ExponentialSmoothing(np.asarray(train_df['Value']) ,seasonal_periods=12 ,trend='add', seasonal='add',).fit()
y_hat_avg['Holt_Winter'] = fit1.forecast(len(valid))
plt.figure(figsize=(16,8))
plt.plot(train_df['Value'], label='Train')
plt.plot(valid['Value'], label='Test')
plt.plot(y_hat_avg['Holt_Winter'], label='Holt_Winter')
plt.legend(loc='best')
plt.show()


# In[ ]:


y_forecasted = y_hat_avg['Holt_Winter']
y_truth = valid.Value
rms = sqrt(mean_squared_error(y_truth,y_forecasted))
print("RMS of Holt-Winter ADDITIVE",rms)
mape = mean_absolute_percentage_error(y_truth,y_forecasted)
print("The MAPE of Holt-Winter ADDITIVE {}",mape)


# In[ ]:



y_hat_avg = valid.copy()
fit1 = ExponentialSmoothing(np.asarray(train_df['Value']) ,seasonal_periods=12 ,trend='add', seasonal='mul',).fit()
y_hat_avg['Holt_Winter'] = fit1.forecast(len(valid))
plt.figure(figsize=(16,8))
plt.plot(train_df['Value'], label='Train')
plt.plot(valid['Value'], label='Test')
plt.plot(y_hat_avg['Holt_Winter'], label='Holt_Winter')
plt.legend(loc='best')
plt.show()


# In[ ]:


y_forecasted = y_hat_avg['Holt_Winter']
y_truth = valid.Value
rms = sqrt(mean_squared_error(y_truth,y_forecasted))
print("RMS of Holt-Winters Multiplicative ",rms)
mape = mean_absolute_percentage_error(y_truth,y_forecasted)
print("The MAPE of Holt-Winters Multiplicative  {}",mape)


# Forecasting with Holt-Winters Multiplicative model 12 months in future

# In[ ]:


y_forecasted_holt = pd.DataFrame()
y_forecasted_holt['forecasted'] = fit1.forecast(len(valid)+12)
y_forecasted_holt.index = range(219,305)
ax = data.Value.plot(label='observed')
y_forecasted_holt.plot(ax=ax, label='Forecast', figsize=(12, 8))
ax.set_xlabel('Index')
ax.set_ylabel('Sales')
plt.legend()

