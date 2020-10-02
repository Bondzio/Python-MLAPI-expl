#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing the necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


# Reading the test dataset
df = pd.read_csv('../input/covid19-global-forecasting-week-2/train.csv')


# In[ ]:


# Taking a look at the dataset
df.head(15)


# In[ ]:


# Information about the dataset
df.info()


# In[ ]:


# Converting the 'Date' column into DataTime object
df['Date'] = pd.to_datetime(df['Date'])


# In[ ]:


for i in range(len(df)):
    if df['Date'][i] == pd.to_datetime('2020-03-29') or df['Date'][i] == pd.to_datetime('2020-03-30'):
        df.drop(index=i, inplace=True)
        
df.reset_index(drop=True, inplace=True)


# In[ ]:


# Copying the dataframe to another dataframe
df2 = df.copy()


# In[ ]:


df3 = df.copy()


# In[ ]:


df3.head(8)


# In[ ]:


# Filling NaN value in Province_State with character string 'Unknown'
for i in range(len(df3)):
    if pd.isnull(df3['Province_State'][i]):
        df3['Province_State'][i] = 'Unknown'


# In[ ]:


# Let's check how many countries we have
df3['Country_Region'].unique()


# There are total **173** unique countries.

# In[ ]:


# Let's check how many unique dates we have
df3['Date'].dt.strftime('%Y-%m-%d').unique()


# The data is given from **Jan 22** to **Mar 28**.

# So, now we are going to index the data first by **'Country_Region'**  then by **Province_State** then by **'Date'**.

# In[ ]:


df3_country = df3['Country_Region'].unique()
df3_province = df3['Province_State'].unique()
df3_date = df3['Date'].unique()
df3_date = pd.to_datetime(df3_date)


# In[ ]:


df3.set_index(['Country_Region', 'Province_State', 'Date'], inplace=True)


# In[ ]:


df3.loc['United Kingdom', 'Bermuda']


# Now we are going to define a column **'IncrementCases'** that will constitute the daily increment in number of cases.

# In[ ]:


df3['IncrementCases'] = 0
df3['IncrementFatalities'] = 0


# In[ ]:


df3


# In[ ]:


# Filtering Country and Provinces which will aid in filtering and calculation
country_province = []
for index in df3.index:
    country_province.append(index[0:2])
country_province = list(set(country_province))


# In[ ]:


for index in country_province:
    for i in range(67):
        if i == 0:
            df3.loc[index]['IncrementCases'][i] = df3.loc[index]['ConfirmedCases'][i]
            df3.loc[index]['IncrementFatalities'][i] = df3.loc[index]['Fatalities'][i]
        else:
            df3.loc[index]['IncrementCases'][i] = df3.loc[index]['ConfirmedCases'][i] - df3.loc[index]['ConfirmedCases'][i-1]
            df3.loc[index]['IncrementFatalities'][i] = df3.loc[index]['Fatalities'][i] - df3.loc[index]['Fatalities'][i-1]


# Now, we are going to plot the **Daily Confirmed Cases of COVID-19 around the World** as a Time Series.

# In[ ]:


daily_cases = df3['IncrementCases'].groupby(level="Date").sum()


# In[ ]:


plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = [15, 5]
plt.plot(daily_cases)
plt.title('Line Plot of Daily Confirmed Cases of COVID-19 around the World')
plt.ylabel('Daily Cases')
plt.xlabel('Date')
plt.show()


# Now, we are going to plot the **Total Confirmed Cases of COVID-19 around the World** as a Time Series.

# In[ ]:


cumulative_cases = daily_cases.cumsum()


# In[ ]:


plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = [15, 5]
plt.plot(cumulative_cases)
plt.title('Line Plot of Total Confirmed Cases of COVID-19 around the World')
plt.ylabel('Total Number of Cases')
plt.xlabel('Date')
plt.show()


# ## Time Series Analysis

# Now, it is difficult to predict the number of fatalities with the given data. But the data is good enough for forecasting the **Daily Cases of COVID-19 around the World** i.e. we are going to use Econometric Time Series analysis.
# Consider the seasonal decomposition with a **Additive Model**.

# In[ ]:


import statsmodels.api as sm
sm.tsa.seasonal_decompose(daily_cases, model='add').plot()
plt.show()


# Here, we observe that there is an upward trend in the Time Series.
# We are going to fit an exponential smoothing method and the make predictions.

# In[ ]:


from statsmodels.tsa.holtwinters import ExponentialSmoothing


# In[ ]:


daily_fit = ExponentialSmoothing(daily_cases, freq='D', trend='add', seasonal=None).fit()


# In[ ]:


daily_fit.summary()


# In[ ]:


daily_predict = daily_fit.predict(start='2020-01-22', end='2020-04-03')
test_predict = daily_fit.predict(start='2020-03-19', end='2020-04-30')


# ### Plotting the prediction form ExponentialSmoothing

# In[ ]:


plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = [15, 5]
plt.plot(daily_cases, color='steelblue')
plt.plot(daily_predict, color='red', linewidth=0.8)
plt.legend(['Actual Cases', 'Predicted Cases'])
plt.title('Line Plot of Daily and Predicted Cases of COVID-19 around the World')
plt.ylabel('Daily Cases')
plt.xlabel('Date')
plt.show()


# Now that we have the picture of Daily affected cases, we can now go for prediction for the world!

# Consider the fact that the Total Daily cases witnessed is afterall the linear combination of individual Country/ Province. Hence, we can try to fit a Linear Model where,
# $$Y~is~the~Total~Daily~Cases$$ and $$X_i~is~Country~/~Province$$

# We can also do the above analysis for each country separately.

# In[ ]:


final = []
for i in range(len(country_province)):
    id = df3.loc[country_province[i]]['Id'].astype(int)
    
    data = df3.loc[country_province[i]]['IncrementCases']
    fit = ExponentialSmoothing(data, freq='D', trend='add', seasonal=None).fit()
    pred = fit.predict(start='2020-03-19', end='2020-04-30')
    pred = round(abs(pred))
    pred = pd.Series(pred, name='Predicted Daily Cases')
    cum_pred = pred.cumsum()
    cum_pred = pd.Series(cum_pred, name='Cumulative Case')
    
    fatality_data = df3.loc[country_province[i]]['IncrementFatalities']
    fit2 = ExponentialSmoothing(fatality_data, freq='D', trend='add', seasonal=None).fit()
    pred2 = fit2.predict(start='2020-03-19', end='2020-04-30')
    pred2 = round(abs(pred2))
    pred2 = pd.Series(pred2, name='Prediction Fatality')
    cum_pred2 = pred2.cumsum()
    cum_pred2 = pd.Series(cum_pred2, name='Cumulative Fatalities')
    
    final_df = pd.concat([id, pred, cum_pred, pred2, cum_pred2], axis=1)
    final_df.dropna(subset=['Predicted Daily Cases'], axis=0 , inplace=True)
    final.append(final_df)


# In[ ]:


for i in range(len(final)):
    final[i]['Id'] = np.arange(final[i]['Id'][0], final[i]['Id'][0]+43)
    final[0]['Id'] = final[i]['Id'].astype(int)


# In[ ]:


a = pd.concat([df for df in final])


# In[ ]:


a.sort_values(by='Id', inplace=True)


# In[ ]:


a['Id'] = np.arange(1, 12643)


# In[ ]:


a


# In[ ]:


b = a[['Id', 'Cumulative Case', 'Cumulative Fatalities']]


# In[ ]:


b.columns = ['ForecastId', 'ConfirmedCases', 'Fatalities']


# In[ ]:


b.to_csv('submission.csv', index=False)


# In[ ]:




