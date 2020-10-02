#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA
from pandas.tseries.offsets import DateOffset

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# Suppress warnings 
import warnings
warnings.filterwarnings('ignore')


# ## Loading in a data

# In[ ]:


df = pd.read_csv('../input/industrial-production-index-in-usa/INDPRO.csv')
df.head()


# In[ ]:


df.columns = ['Date', 'IPI']
df.head()


# In[ ]:


# to check NAs
df.info()
df.isnull().sum()


# In[ ]:


df['Date'] = pd.to_datetime(df['Date'])


# In[ ]:


#setting up Date column as an Index
df.set_index ('Date', inplace = True)
df.index


# In[ ]:


#Date slicing
df_new = df['1998-01-01':]
df_new.tail()


# In[ ]:


df_new.describe().transpose()


# In[ ]:


f, ax = plt.subplots(figsize = (16,10))
ax.plot(df_new, c = 'r');


# In[ ]:


# rot = rotates labels at the bottom
# fontsize = labels size
# grid False or True

df_new.boxplot('IPI', rot = 80, fontsize = '12',grid = True);


# ## Stationarity

# The mean, varience and covarience of the i-th and the (i+m)-th term of the series should not depend on time. Most statistical methods assume or require the series to be stationary.

# In[ ]:


time_series = df_new['IPI']
type(time_series)


# In[ ]:


time_series.rolling(12).mean().plot(label = '12 Months Rolling Mean', figsize = (16,10))
time_series.rolling(12).std().plot(label = '12 Months Rolling Std')
time_series.plot()
plt.legend();


# Since rolling mean and rolling standard deviation increase over time, the time series are non-stationary.

# ## Dickey-Fuller Test
# Null hypothesis that the series are non-stationary.
# Alternative hypothesis: series are stationary. The data is considered to be stationary if the p-value is less than 0.05 and ADF Statistic is close to the critical values. 

# In[ ]:


result = adfuller(df_new['IPI'])


# In[ ]:


#to make it readable
def adf_check(time_series):
    
    result = adfuller(time_series)
    print('Augmented Dickey-Fuller Test')
    labels = ['ADF Test Statistic', 'p-value', '# of lags', 'Num of Obs used']
    
    print('Critical values:')
    for key,value in result[4].items():
        print('\t{}: {}'.format(key, value) )
    
    for value, label in zip(result,labels):
        print(label+ ' : '+str(value))
    
    if ((result[1] <= 0.05 and  result[0] <= result[4]['1%']) or
    (result[1] <= 0.05 and  result[0] <= result[4]['5%']) or
        (result[1] <= 0.05 and  result[0] <= result[4]['10%'])):
        print('Reject null hypothesis')
        print ('Data has no unit root and is stationary')
   
    else:
        print('Fail to reject null hypothesis')
        print('Data has a unit root and it is non-stationary')


# In[ ]:


adf_check(df_new['IPI'])


# ADF statistic is higher than Critical values and p-value is above 0.05. Conclusion: This data is non-stationary

# ## How to make it stationary

# In order to conclude that the series is stationary, the p-value has to be less than the significance level. As well as, ADF t-statistic must be below the Critical values.

# ### 1. Taking the first difference

# In[ ]:


df_new['Dif_1'] = df_new['IPI'] - df_new['IPI'].shift(1)
df_new['Dif_1'].plot(rot = 80, figsize = (14,8));


# #### Checking for stationarity again:

# In[ ]:


adf_check(df_new['Dif_1'].dropna())


# In[ ]:


#If need to take a second difference

#df_new['Dif_2'] = df_new['Dif_1'] - df_new['Dif_1'].shift(1)
#adf_check(df_new['Dif_2'].dropna())


# ### 2. Seasonal Difference

# #### 2.1 Taking seasonal difference

# In[ ]:


df_new['Dif_Season'] = df_new['IPI'] - df_new['IPI'].shift(12)
df_new['Dif_Season'].plot(rot = 80, figsize = (14,8));


# In[ ]:


adf_check(df_new['Dif_Season'].dropna())


# Even though T-stats value is close to the Critical values, p-value is too high. Result: The data is non-stationary.

# #### 2.2 Seasonal effect of the first difference:

# In[ ]:


df_new['Dif_Season_1'] = df_new['Dif_1'] - df_new['Dif_1'].shift(12)
df_new['Dif_Season_1'].plot(rot = 80, figsize = (14,8));


# In[ ]:


adf_check(df_new['Dif_Season_1'].dropna())


# 2.3 Mean Difference

# In[ ]:


df_new['Dif_mean'] = df_new['IPI'] - df_new['IPI'].rolling(12).mean()
df_new['Dif_mean'].plot(rot = 80, figsize = (14,8));


# In[ ]:


adf_check(df_new['Dif_mean'].dropna())


# ## Conclusion:

# Out of all ADF test results, the best result will be taking the seasonal difference of the 1st difference. So, in our case, this is df_new['Dif_Season_1'].

# ## Seasonal Decomposition of Time Series Components
# 
# #### Trend: 
# Upward or downward movement of the data over time
# #### Seasonality: 
# Seasonal varience
# #### Noise: 
# Spikes and drops at random intervals

# In[ ]:


#freq can be set to True or number of periods. Ex: 12 months
decomp = seasonal_decompose(time_series, freq = 12)
fig = decomp.plot()
fig.set_size_inches(15,8)


# ## Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF)

# Since df_log['Dif_1'] in ADF test gave the most prefereable results, I would plot AC and PAC plots only for this data. Autocorrelation function is used to determine number of MA terms, and Partial Autocorrelation is for AR terms.

# In[ ]:


acf_seasonal = plot_acf(df_new['Dif_Season_1'].dropna(), lags = 40, color = "purple", marker = "^")
pacf_plot = plot_pacf(df_new['Dif_Season_1'].dropna(), lags = 30, color = "Green", marker = "*")


# ## ARIMA Model

# Based on the AC and PAC graphs, we can choose the AR and MA orders for the ARIMA model. Also, for AR it is the number of lag observations from ADF result. And for MA it is the size of the MA window.

# Note:
# * If the autocorrelation plot shows positive autocorrelation at the first lag (lag-1), then it suggests to use the AR terms in relation to the lag.
# * If the autocorrelation plot shows negative autocorrelation at the first lag, then it suggests using MA terms.

# In[ ]:


#model = ARIMA(df_new['IPI'], order = (14,1,12))
model = sm.tsa.statespace.SARIMAX(df_new['IPI'],order=(14,1,12), seasonal_order=(1,1,1,12))
model_result = model.fit()
print(model_result.summary());


# In[ ]:


#to plot residuals:
model_result.resid.plot(rot = 80);


# #KDE plot:
# model_result.resid.plot(kind = 'kde');

# In[ ]:


#create additional future dates:
forecast_dates = [df_new.index[-1] + DateOffset(months=x) for x in range(1,24)]
df_future = pd.DataFrame(index=forecast_dates, columns = df_new.columns)
df_final = pd.concat([df_new, df_future])


# In[ ]:


df_final['Forecast'] = model_result.predict(start=220,end=280, alpha = 0.05)
df_final[['IPI','Forecast']].plot(figsize = (12,8));


# ## Diagnostic Plots

# We want the residuals to be white noise process

# In[ ]:


y = model_result.plot_diagnostics(figsize = (10,6))


# ### To add Confidence Ingtervals:

# In[ ]:


forecast = model_result.get_forecast(steps = 60)
conf_int = forecast.conf_int()


# In[ ]:


ax = df_final[['IPI','Forecast']].plot(figsize = (12,8))
ax.fill_between(conf_int.index,
               conf_int.iloc[:, 0],
               conf_int.iloc[:,1], color = 'grey', alpha = 0.5)
ax.set_xlabel('Time')
ax.set_ylabel('Industrial Production Index')
ax.set_title('SARIMA Forecast')
plt.legend();


# And here we go! My forecast for the US Industrial Production Index. I am pretty happy with my results. However, the confidence interval is very wide.
