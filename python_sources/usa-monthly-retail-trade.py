#!/usr/bin/env python
# coding: utf-8

# In this notebook, we will use a time series dataset(published by US Sensus Bureau) that is made up of retail and food services related monthly figures(in USD) for the period Jan 1992 to April 2020.
# 
# Sales data are adjusted for seasonal, holiday, and trading-day differences. So recover the original data by applying the seasonal factors.

# In[ ]:


import pandas as pd
import numpy as np
from statsmodels.tools.eval_measures import rmse
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf 
from statsmodels.tsa.seasonal import seasonal_decompose 
#from pmdarima import auto_arima                        
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


df_adjusted = pd.read_excel('../input/salesdata/Retail and Food Services.xlsx')
df_seasonal = pd.read_excel('../input/salesdata/Seasonal Factors.xlsx')


# In[ ]:


df_adjusted.tail()


# Both the dataframes need to be converted into time series format.Hence, the below code tranforms df_adjusted into df1

# In[ ]:


df_1 = pd.melt(df_adjusted, id_vars=['YEAR'], value_vars=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'], var_name='MONTH')
df_1['ds'] = pd.to_datetime(df_1['YEAR'].astype(str) + df_1['MONTH'], format='%Y%b')
df_1 = df_1.drop(['YEAR','MONTH'], axis=1)
df_1.columns = ['y', 'ds']
df_1 = df_1[['ds', 'y']]
df_1 = df_1.sort_values(['ds'], ascending=True)
df_1 = df_1.reset_index(drop=True)
df_1.tail(10)


# In[ ]:


df1 = df_1.iloc[0:340]


# Line chart for Monthly adjusted sales 

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
df1.set_index('ds').plot(figsize=(15,8))


# In[ ]:


df_2 = pd.melt(df_seasonal, id_vars=['YEAR'], value_vars=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'], var_name='MONTH')
df_2['ds'] = pd.to_datetime(df_2['YEAR'].astype(str) + df_2['MONTH'], format='%Y%b')
df_2 = df_2.drop('YEAR', axis=1)
df_2 = df_2.drop('MONTH', axis=1)
df_2.columns = ['factor', 'ds']
df_2 = df_2[['ds', 'factor']]
df_2 = df_2.sort_values(['ds'], ascending=True)
df_2 = df_2.reset_index(drop=True)
df_2.tail(10)


# In[ ]:


df2 = df_2.iloc[0:340]


# Monthly adjustment factor for each year in a single line chart

# In[ ]:


d3 = pd.DataFrame(df2, columns=['ds', 'factor']).set_index('ds')
d3.index = [d3.index.month, d3.index.year]
d3 = d3.factor.unstack().interpolate()
plot = d3.plot(legend=0, figsize=(12,6))


# We can now recover the unadjusted monthly sales 

# In[ ]:


df = pd.DataFrame(df1[['ds']], index=df1.index, columns=['ds'])
df['y'] = df1['y'] * df2['factor']
df.head()


# Now, we wil log tranform the unadjusted monthly sales and plot the resulting time series

# In[ ]:


df.y = np.log(df.y)
ts = df.copy()


# In[ ]:


ts.set_index('ds').plot(figsize=(15,8))


# In[ ]:


train_data = ts[:len(ts)-12]
test_data = ts[len(ts)-12:]


# # ARIMA
# https://www.statisticshowto.com/autoregressive-model/

# Let's run auto_arima() function to get best p,d,q,P,D,Q values

# In[ ]:


# auto_arima(ts['y'], seasonal=True, m=12,max_p=7, max_d=5,max_q=7, max_P=4, max_D=4,max_Q=4).summary()


# In[ ]:


arima_model = SARIMAX(train_data['y'], order = (2,1,2), seasonal_order = (4,0,0,12))
arima_result = arima_model.fit()
arima_result.summary()  


# In[ ]:


arima_pred = arima_result.predict(start = len(train_data), end = len(ts)-1, typ="levels").rename("ARIMA Predictions")
arima_pred


# In[ ]:


test_data['y'].plot(figsize = (16,5), legend=True)
arima_pred.plot(legend = True)


# In[ ]:


arima_rmse_error = rmse(test_data['y'], arima_pred)
arima_mse_error = arima_rmse_error**2
mean_value = ts['y'].mean()

print(f'MSE Error: {arima_mse_error}\nRMSE Error: {arima_rmse_error}\nMean: {mean_value}')


# In[ ]:


test_data['ARIMA_Predictions'] = arima_pred


# # Prophet
# **Reason:**
# It works best with time series that have strong seasonal effects and several seasons of historical data and robust to missing data,shifts in the trend, and typically handles outliers well.

# In[ ]:


import datetime
import matplotlib.pyplot as plt
from fbprophet import Prophet

model = Prophet()
model.fit(train_data)


# In[ ]:


future = model.make_future_dataframe(periods=22, freq='MS')
forecast = model.predict(future)


# In[ ]:


plot = model.plot(forecast)


# In[ ]:


plot = model.plot_components(forecast)


# In[ ]:


df_visualise = pd.merge(test_data, forecast, left_on='ds', right_on='ds', how='outer')
df_visualise = df_visualise.set_index('ds')
df_visualise[['y','yhat']].plot(figsize=(15,8),)


# In[ ]:


prophet_pred = pd.DataFrame({"Date" : forecast[-12:]['ds'], "Pred" : forecast[-12:]["yhat"]})


# In[ ]:


prophet_pred = prophet_pred.set_index("Date")


# In[ ]:


test_data["Prophet_Predictions"] = prophet_pred['Pred'].values


# In[ ]:


prophet_rmse_error = rmse(test_data['y'], test_data["Prophet_Predictions"])
prophet_mse_error = prophet_rmse_error**2
mean_value = test_data['y'].mean()

print(f'MSE Error: {prophet_mse_error}\nRMSE Error: {prophet_rmse_error}\nMean: {mean_value}')


# In[ ]:


rmse_errors = [arima_rmse_error, prophet_rmse_error]
mse_errors = [arima_mse_error, prophet_mse_error]
errors = pd.DataFrame({"Models" : ["ARIMA", "Prophet"],"RMSE Errors" : rmse_errors, "MSE Errors" : mse_errors})


# In[ ]:


plt.figure(figsize=(16,9))
plt.plot_date(test_data.index, test_data["y"], linestyle="-")
plt.plot_date(test_data.index, test_data["ARIMA_Predictions"], linestyle="-.")
plt.plot_date(test_data.index, test_data["Prophet_Predictions"], linestyle=":")
plt.legend(['Actual','ARIMA','PROPHET'])
plt.show()


# In[ ]:


print(f"Mean: {test_data['y'].mean()}")
errors


# In[ ]:


test_data


# Hence, the RMSE is quite good and both the algorithms are performing real good, but i am taking ARIMA because of visual explanation.

# In[ ]:


d_f = pd.DataFrame(df_1[['ds']], index=df_1.index, columns=['ds'])
d_f['y'] = df_1['y'] * df_2['factor']
d_f


# In[ ]:


d_f.y = np.log(d_f.y)
t_s = d_f.copy()


# In[ ]:


t_s.tail(9)


# In[ ]:


ts_pred = t_s.iloc[340:]


# In[ ]:


arima_pred = arima_result.predict(start = 340, end = 347, typ="levels").rename("ARIMA Predictions")
arima_pred


# In[ ]:


ts_pred['exp_yhat'] = np.exp(arima_pred)


# In[ ]:


ts_pred

