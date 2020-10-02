#!/usr/bin/env python
# coding: utf-8

# ## Github link
# Link: [https://github.com/SABadhon/Covid-19-Case-prediction-using-Facebook-Prophet](http://)

# ## Import Libraries

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from fbprophet import Prophet


# ### Read and see the data.

# In[ ]:


covid_df = pd.read_csv('../input/covid19-global/covid19_global.csv')
covid_df.info()


# ### Check for NULL values

# In[ ]:


covid_df.isnull().sum()


# ### Visualize the data
# 

# In[ ]:


covid_df.sort_values('Date')
plt.figure(figsize = (10,10))
plt.plot(covid_df['Date'],covid_df['Confirmed'])


# ### Extract the data

# In[ ]:


covid_df = covid_df[covid_df['Country']=='Bangladesh']
covid_df = covid_df[['Date','Confirmed']]


# In[ ]:


covid_df = covid_df.rename(columns = {'Date':'ds', 'Confirmed':'y'})
covid_df.head()


# ## Train the model
# 

# In[ ]:


m = Prophet()
m.fit(covid_df)


# In[ ]:


future = m.make_future_dataframe(periods=60)  # prediction for next 60 days
forecast = m.predict(future)


# In[ ]:


# visualize the result
figure = m.plot(forecast, xlabel = 'Date', ylabel = 'No of Cases')
plt.title('Covid-19 Cases Forecasting - Bangladesh')


# In[ ]:


# check the data 
forecast.head()

