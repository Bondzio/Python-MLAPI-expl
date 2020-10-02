#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"
import warnings 
warnings.filterwarnings('ignore')
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams

from datetime import datetime


# In[ ]:


data = pd.read_csv('../input/covid19-corona-virus-india-dataset/complete.csv')
data1 = data.rename(columns={'Name of State / UT':'State','Cured/Discharged/Migrated':'Cured','Total Confirmed cases':'Confirmed'})
data2=data1.groupby('Date')[['Confirmed','Death']].sum().reset_index()
data2


# In[ ]:


today=data1['Date'].max()
df1 = pd.melt(data2, id_vars=['Date'], value_vars=['Confirmed','Death'])
fig = px.line(df1, x="Date", y='value', color='variable', title=f"Confirmed cases as on {today}")
fig.show()


# In[ ]:


train=data1.groupby(['Date','State'])[['Confirmed','Death']].sum().reset_index()
train.head()


# In[ ]:


today= data1['Date'].max()
today


# In[ ]:


df1=data1.groupby('State')[['Confirmed','Death']].sum().reset_index()
top_states = df1.sort_values('Confirmed', ascending=False).iloc[:5]['State'].unique()
top_df= data1[data1['State'].isin(top_states)]
fig = px.line(top_df, x="Date", y="Confirmed", color="State", title=f"Top 5 states as on {today}")
fig.show()


# In[ ]:


state_wise = data1.query('(Date == @today)').sort_values('Confirmed',ascending= False)
state_wise_df = pd.melt(state_wise, id_vars='State', value_vars='Confirmed')
fig = px.bar(state_wise_df, x="State", y='value', color='variable', title=f"Confirmed cases as on {today}")
fig.show()


# In[ ]:


data2['New']= data2['Confirmed']-data2['Confirmed'].shift(1) 
data2


# In[ ]:


data2['New'].max()


# In[ ]:


#Found one missing value in the data set. That need to be adjusted by replacing with the roling mean value.
df2= pd.melt(data2,id_vars=['Date'], value_vars=['New'])
fig = px.bar(df2, x="Date", y="value", color='variable', title=f"Daily new cases as on {today}")
fig.show()


# In[ ]:


states = data1['State'].unique()
print(f'{len(states)} States are in dataset:\n{states}')


# In[ ]:


today = data1['Date'].max()
print('Date: ', today)
for i in [1, 10, 100, 1000]:
    n_states = len(data1.query('(Date == @today) & Confirmed > @i'))
    print(f'{n_states} States have more than {i} Confirmed')


# In[ ]:


dt = data1[data1['State']=='Odisha']
dt.head()


# In[ ]:


today=data1['Date'].max()
df11 = pd.melt(dt, id_vars=['Date'], value_vars=['Confirmed','Death'])
fig = px.line(df11, x="Date", y='value', color='variable', title=f"Confirmed cases in Odisha as on {today}")
fig.show()


# In[ ]:


dt.drop(dt[dt['Confirmed']==0].index,inplace=True)
dt['New']=dt['Confirmed']-dt['Confirmed'].shift(1)
df12 = pd.melt(dt, id_vars=['Date'], value_vars=['New'])
fig = px.bar(df12, x="Date", y='value', color='variable', title=f"Daily new Confirmed cases in Odisha as on {today}")
fig.show()


# In[ ]:


df13 = pd.melt(dt, id_vars=['Date'], value_vars=['New'])
fig = px.line(df13, x="Date", y='value', color='variable', title=f"Daily new cases in Odisha as on {today}")
fig.show()


# According to the reaserch work COVID19 has affected 0.16% of the total population of US, 0.34% population of Spain, 0.15% population of Germany,0.14% of France and 0.24% of Italy. The total population of Odisha is around 43700000 that is near equal to the population of Spain.
# Accordingly the COVID19 cases in Odisha would have been 87,400 (0.15% of 43700000). Due to the lock-down the number of confined cases right now 60.

# In[ ]:


train3=dt.drop(['State','Total Confirmed cases (Indian National)','Total Confirmed cases ( Foreign National )','Cured','Latitude','Longitude','Death','Confirmed'], axis = 1)
train3['Mean']= train3.rolling(window=3).mean()
train3['Mean'].fillna(0.1, inplace=True)
train3['Mean'].replace(to_replace =0.0,value =0.2, inplace=True)
train1= train3.drop(['New'], axis=1)
train1


# In[ ]:


train1['Date']= pd.to_datetime(train1['Date'])
train2=train1.set_index('Date')
plt.xlabel('Date')
plt.ylabel('NewCases')
plt.plot(train2['Mean'])


# In[ ]:


rolmean = train2['Mean'].rolling(window=2).mean()
rolstd = train2['Mean'].rolling(window =2).std()


# In[ ]:


from statsmodels.tsa.stattools import adfuller
print('Dicky fuller taste')
dftest = adfuller(train2['Mean'],autolag='AIC')
dfout = pd.Series(dftest[0:4],index=['Test statistics','P-value','#Lags used','Number of observations'])
for key,values in dftest[4].items():
    dfout['Critical values(%s)'%key]=values
print(dfout)


# In[ ]:


train2_logscale = np.log(train2['Mean'])
train2_logscale.dropna(inplace=True)
plt.plot(train2_logscale)


# In[ ]:


movingAverage = train2_logscale.rolling(window=2).mean()
movingSTD = train2_logscale.rolling(window =2).std()
plt.plot(train2_logscale)
plt.plot(movingAverage,color='red')


# In[ ]:


tm_log_avg = train2_logscale-movingAverage
tm_log_avg.dropna(inplace=True)
def test_stationary(timeseries):
    movingAverage =timeseries.rolling(window=3).mean()
    movingSTD = timeseries.rolling(window=3).std()
    orig = plt.plot(timeseries,color='blue',label='Orginal')
    avg = plt.plot(movingAverage,color='black',label='Moving Average')
    std = plt.plot(movingSTD,color='red',label='Rollong std')
    plt.legend(loc='best')
    plt.title('Rolling mean and rolling std')
    plt.show()
    
    print('Dicky fuller taste')
    dftest = adfuller(train2['Mean'],autolag='AIC')
    dfout = pd.Series(dftest[0:4],index=['Test statistics','P-value','#Lags used','Number of observations'])
    for key,values in dftest[4].items():
        dfout['Critical values(%s)'%key]=values
        print(dfout)


# In[ ]:


test_stationary(tm_log_avg)


# In[ ]:


exponential= train2_logscale.ewm(halflife=1,min_periods=0,adjust=True).mean()
plt.plot(train2_logscale)
plt.plot(exponential, color='red')


# In[ ]:


mexponential = train2_logscale-exponential
test_stationary(mexponential)


# In[ ]:


datashifting = train2_logscale-train2_logscale.shift(1)
plt.plot(datashifting)


# In[ ]:


datashifting.dropna(inplace=True)
test_stationary(datashifting)


# In[ ]:


from statsmodels.tsa.arima_model import ARIMA
model =ARIMA(train2_logscale,order=(1,1,0))
results_AR=model.fit(disp=-1)
plt.plot(datashifting)
plt.plot(results_AR.fittedvalues,color='red')
plt.title('RSS:%4F'%sum(results_AR.fittedvalues - datashifting**2))
print('Plotting AR model')


# In[ ]:


model =ARIMA(train2_logscale,order=(1,1,0))
results_MA =model.fit(disp=-1)
plt.plot(datashifting)
plt.plot(results_MA.fittedvalues,color='red')
print('Plotting MR model') 


# In[ ]:


model = ARIMA(train2_logscale,order=(2,0,1))
results_ARIMA= model.fit(disp=-1)
plt.plot(datashifting)
plt.plot(results_ARIMA.fittedvalues,color='red')


# In[ ]:


predictions_ARIMA_diff= pd.Series(results_ARIMA.fittedvalues,copy=True)
print(predictions_ARIMA_diff.head())


# In[ ]:


prediction_ARIMA_log=pd.Series(train2_logscale.ix[0],index= train2_logscale.index)
prediction_ARIMA_log=prediction_ARIMA_log.add(predictions_ARIMA_diff,fill_value=0)
prediction_ARIMA_log.head()


# In[ ]:


predictions_ARIMA = np.exp(prediction_ARIMA_log)
plt.plot(train2)
plt.plot(predictions_ARIMA)


# In[ ]:


sns.set(rc={'figure.figsize':(16, 8)})
results_ARIMA.plot_predict(1,70)
x=results_ARIMA.forecast(steps=70)


# The data has been taken form 16th marh upto 16th April i.e. for 31 days and the number of COVID19 cases has been predicted for next 39 days. The pick will reach around the 40th day i.e. 25th to 30th April. The maximum number of daily new cases will be around 30 at the pick. The number of daily cases woill come to zero around first week of June. 
# The Cumulative confirmed cases would be around 150.We can expect 75 to 90 new cases in our state. 

# In[ ]:


cases= np.exp(x[1])
cases


# In[ ]:


k1= np.exp(3.5)
k1


# In[ ]:


cases0 = np.exp(x[0])
cases0


# In[ ]:


cases.sum() - cases0.sum()- (15*7)


# In[ ]:


x[2]


# In[ ]:


k2=np.exp(-3.6)
k2


# In[ ]:


k5 = np.exp(7.5)
k5


# In[ ]:




