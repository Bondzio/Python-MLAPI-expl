#!/usr/bin/env python
# coding: utf-8

# # 1.0

# ### 1.1. Import the libraries & data

# In[ ]:


import pandas as pd
import numpy as np
from pandas import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


consumption = pd.read_csv('/kaggle/input/electric-power-consumption-data-set/household_power_consumption.txt', sep = ';', parse_dates= ['Date'], infer_datetime_format=True, low_memory=False,  na_values=['nan','?'])


# In[ ]:


consumption.head()


# In[ ]:


consumption.describe()


# In[ ]:


consumption.info()


# In[ ]:


consumption.isna().sum()


# ### Drop the null values

# In[ ]:


consumption = consumption.dropna()
consumption.isna().sum()


# ## Average consumption of each day in 4 years

# In[ ]:


mean_consumption_gby_date = consumption.groupby(['Date']).mean()


# In[ ]:


fig, axs = plt.subplots(3, 2, figsize = (30, 25))
columns = mean_consumption_gby_date.columns
axs[0, 0].plot(mean_consumption_gby_date[columns[0]])
axs[0, 0].set_title(columns[0], fontweight = 'bold', size = 20)

axs[0, 1].plot(mean_consumption_gby_date[columns[1]])
axs[0, 1].set_title(columns[1], fontweight = 'bold', size = 20)

axs[1, 0].plot(mean_consumption_gby_date[columns[2]])
axs[1, 0].set_title(columns[2], fontweight = 'bold', size = 20)

axs[1, 1].plot(mean_consumption_gby_date[columns[3]])
axs[1, 1].set_title(columns[3], fontweight = 'bold', size = 20)

axs[2, 0].plot(mean_consumption_gby_date[columns[4]])
axs[2, 0].set_title(columns[4], fontweight = 'bold', size = 20)

axs[2, 1].plot(mean_consumption_gby_date[columns[5]])
axs[2, 1].set_title(columns[5], fontweight = 'bold', size = 20)

fig, axs = plt.subplots( figsize = (20, 4))
axs.plot(mean_consumption_gby_date[columns[6]])
axs.set_title(columns[6], fontweight = 'bold', size = 15)


# ## Average consumption in each month

# In[ ]:


mean_consumption_gby_month = consumption.groupby(consumption['Date'].dt.strftime('%B')).mean()
reorderlist = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]
mean_consumption_gby_month = mean_consumption_gby_month.reindex(reorderlist)


# In[ ]:


fig, axs = plt.subplots(3, 2, figsize = (30, 25))
columns = mean_consumption_gby_month.columns

axs[0, 0].plot(mean_consumption_gby_month[columns[0]])
axs[0, 0].set_title(columns[0], fontweight = 'bold', size = 20)

axs[0, 1].plot(mean_consumption_gby_month[columns[1]])
axs[0, 1].set_title(columns[1], fontweight = 'bold', size = 20)

axs[1, 0].plot(mean_consumption_gby_month[columns[2]])
axs[1, 0].set_title(columns[2], fontweight = 'bold', size = 20)

axs[1, 1].plot(mean_consumption_gby_month[columns[3]])
axs[1, 1].set_title(columns[3], fontweight = 'bold', size = 20)


axs[2, 0].plot(mean_consumption_gby_month[columns[4]])
axs[2, 0].set_title(columns[4], fontweight = 'bold', size = 20)

axs[2, 1].plot(mean_consumption_gby_month[columns[5]])
axs[2, 1].set_title(columns[5], fontweight = 'bold', size = 20)

fig, axs = plt.subplots( figsize = (20, 4))
axs.plot(mean_consumption_gby_month[columns[6]])
axs.set_title(columns[6], fontweight = 'bold', size = 15)


# # 2.0

# **Please restart the kernel before starting the portion below.**

# In[ ]:


import pandas as pd
import numpy as np
from pandas import datetime as dt
import matplotlib.pyplot as plt
pd.plotting.register_matplotlib_converters()


# In[ ]:


consumption_2 = pd.read_csv('/kaggle/input/electric-power-consumption-data-set/household_power_consumption.txt', sep=';', 
                 parse_dates={'dt' : ['Date', 'Time']}, infer_datetime_format=True, 
                 low_memory=False, na_values=['nan','?'], index_col='dt')


# ## Average consumption of each day in a month

# In[ ]:


mean_consumption_gby_day_month = consumption_2.groupby(consumption_2.index.day).mean()


# In[ ]:


fig, axs = plt.subplots(3, 2, figsize = (30, 25))
columns = mean_consumption_gby_day_month.columns

axs[0, 0].plot(mean_consumption_gby_day_month[columns[0]])
axs[0, 0].set_title(columns[0], fontweight = 'bold', size = 20)

axs[0, 1].plot(mean_consumption_gby_day_month[columns[1]])
axs[0, 1].set_title(columns[1], fontweight = 'bold', size = 20)

axs[1, 0].plot(mean_consumption_gby_day_month[columns[2]])
axs[1, 0].set_title(columns[2], fontweight = 'bold', size = 20)

axs[1, 1].plot(mean_consumption_gby_day_month[columns[3]])
axs[1, 1].set_title(columns[3], fontweight = 'bold', size = 20)

axs[2, 0].plot(mean_consumption_gby_day_month[columns[4]])
axs[2, 0].set_title(columns[4], fontweight = 'bold', size = 20)

axs[2, 1].plot(mean_consumption_gby_day_month[columns[5]])
axs[2, 1].set_title(columns[5], fontweight = 'bold', size = 20)

fig, axs = plt.subplots( figsize = (20, 4))
axs.plot(mean_consumption_gby_day_month[columns[6]])
axs.set_title(columns[6], fontweight = 'bold', size = 15)


# ## Average consumption of each day in a week 

# In[ ]:


days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
mean_consumption_gby_day_week = consumption_2.groupby(consumption_2.index.day_name()).mean().reindex(days)


# In[ ]:


fig, axs = plt.subplots(3, 2, figsize = (30, 25))
columns = mean_consumption_gby_day_week.columns

axs[0, 0].plot(mean_consumption_gby_day_week[columns[0]])
axs[0, 0].set_title(columns[0], fontweight = 'bold', size = 20)

axs[0, 1].plot(mean_consumption_gby_day_week[columns[1]])
axs[0, 1].set_title(columns[1], fontweight = 'bold', size = 20)

axs[1, 0].plot(mean_consumption_gby_day_week[columns[2]])
axs[1, 0].set_title(columns[2], fontweight = 'bold', size = 20)

axs[1, 1].plot(mean_consumption_gby_day_week[columns[3]])
axs[1, 1].set_title(columns[3], fontweight = 'bold', size = 20)

axs[2, 0].plot(mean_consumption_gby_day_week[columns[4]])
axs[2, 0].set_title(columns[4], fontweight = 'bold', size = 20)

axs[2, 1].plot(mean_consumption_gby_day_week[columns[5]])
axs[2, 1].set_title(columns[5], fontweight = 'bold', size = 20)

fig, axs = plt.subplots( figsize = (20, 4))
axs.plot(mean_consumption_gby_day_week[columns[6]])
axs.set_title(columns[6], fontweight = 'bold', size = 15)


# ## Average consumption of each hour in a day

# In[ ]:


consumption_resampled_in_a_day = consumption_2.resample('H').sum()
consumption_resampled_in_a_day.index = consumption_resampled_in_a_day.index.time
mean_consumption_gby_time = consumption_resampled_in_a_day.groupby(consumption_resampled_in_a_day.index).mean()


# In[ ]:


fig, axs = plt.subplots(3, 2, figsize = (30, 25))
columns = mean_consumption_gby_time.columns

axs[0, 0].plot(mean_consumption_gby_time[columns[0]])
axs[0, 0].set_title(columns[0], fontweight = 'bold', size = 20)

axs[0, 1].plot(mean_consumption_gby_time[columns[1]])
axs[0, 1].set_title(columns[1], fontweight = 'bold', size = 20)

axs[1, 0].plot(mean_consumption_gby_time[columns[2]])
axs[1, 0].set_title(columns[2], fontweight = 'bold', size = 20)

axs[1, 1].plot(mean_consumption_gby_time[columns[3]])
axs[1, 1].set_title(columns[3], fontweight = 'bold', size = 20)

axs[2, 0].plot(mean_consumption_gby_time[columns[4]])
axs[2, 0].set_title(columns[4], fontweight = 'bold', size = 20)

axs[2, 1].plot(mean_consumption_gby_time[columns[5]])
axs[2, 1].set_title(columns[5], fontweight = 'bold', size = 20)

fig, axs = plt.subplots( figsize = (20, 4))
axs.plot(mean_consumption_gby_time[columns[6]])
axs.set_title(columns[6], fontweight = 'bold', size = 15)


# ## Average consumption of each month in 4 years

# In[ ]:


mean_consumption_resampled_mnthly = consumption_2.resample('M').mean()


# In[ ]:


fig, axs = plt.subplots(3, 2, figsize = (30, 25))
columns = mean_consumption_resampled_mnthly.columns

axs[0, 0].plot(mean_consumption_resampled_mnthly[columns[0]])
axs[0, 0].set_title(columns[0], fontweight = 'bold', size = 20)

axs[0, 1].plot(mean_consumption_resampled_mnthly[columns[1]])
axs[0, 1].set_title(columns[1], fontweight = 'bold', size = 20)

axs[1, 0].plot(mean_consumption_resampled_mnthly[columns[2]])
axs[1, 0].set_title(columns[2], fontweight = 'bold', size = 20)

axs[1, 1].plot(mean_consumption_resampled_mnthly[columns[3]])
axs[1, 1].set_title(columns[3], fontweight = 'bold', size = 20)

axs[2, 0].plot(mean_consumption_resampled_mnthly[columns[4]])
axs[2, 0].set_title(columns[4], fontweight = 'bold', size = 20)

axs[2, 1].plot(mean_consumption_resampled_mnthly[columns[5]])
axs[2, 1].set_title(columns[5], fontweight = 'bold', size = 20)

fig, axs = plt.subplots( figsize = (20, 4))
axs.plot(mean_consumption_resampled_mnthly[columns[6]])
axs.set_title(columns[6], fontweight = 'bold', size = 15)


# ## Augmented Dickey-Fuller Test (ADF Test)/unit root test to check stationarity

# In[ ]:



from statsmodels.tsa.stattools import adfuller
def adf_test(ts, signif=0.05):
    dftest = adfuller(ts, autolag='AIC')
    adf = pd.Series(dftest[0:4], index=['Test Statistic','p-value','# Lags','# Observations'])
    for key,value in dftest[4].items():
       adf['Critical Value (%s)'%key] = value
    print (adf)
    
    p = adf['p-value']
    if p <= signif:
        print(f" Series is Stationary")
    else:
        print(f" Series is Non-Stationary")


# In[ ]:


adf_test(mean_consumption_resampled_mnthly["Global_active_power"])


# In[ ]:


adf_test(mean_consumption_resampled_mnthly['Global_reactive_power'])


# In[ ]:


adf_test(mean_consumption_resampled_mnthly['Voltage'])


# In[ ]:


adf_test(mean_consumption_resampled_mnthly['Global_intensity'])


# In[ ]:


adf_test(mean_consumption_resampled_mnthly['Sub_metering_1'])


# In[ ]:


adf_test(mean_consumption_resampled_mnthly['Sub_metering_2'])


# In[ ]:


adf_test(mean_consumption_resampled_mnthly['Sub_metering_3'])


# ## Differencing to remove non-stationarity

# In[ ]:


def difference(dataset, interval=1):
    diff = list()
    diff.append(0)
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return diff

mean_consumption_resampled_mnthly['Voltage'] = difference(mean_consumption_resampled_mnthly['Voltage'])


# In[ ]:


adf_test(mean_consumption_resampled_mnthly['Voltage'])


# ## VAR model

# In[ ]:


model = VAR(mean_consumption_resampled_mnthly)
model_fit = model.fit()
pred = model_fit.forecast(model_fit.y, steps=4)

