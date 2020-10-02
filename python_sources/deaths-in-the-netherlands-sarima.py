#!/usr/bin/env python
# coding: utf-8

# ## Import the modules

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX


# First I ignore the non-complete weeks, which can cause some small inconsistencies. 
# 
# 1995 starts with a Sunday and has a full week in this dataset, so in this dataset, a week starts on Sunday. This is `%U` in `strftime`[[1]](https://strftime.org/).

# ## Load data

# In[ ]:


data_pre = pd.read_csv("/kaggle/input/weekly-deaths-in-the-netherlands/deaths_NL.csv")

data_pre = data_pre[data_pre["Week"].str.len()<20]

data_pre["Week"] = data_pre["Week"].str.replace("*", "")

data_pre["Week"] = pd.to_datetime(data_pre["Week"]+'0', format="%Y week %U%w")
data = data_pre.set_index('Week')
data.index = pd.DatetimeIndex(data.index.values,
                               freq=data.index.inferred_freq)


# In[ ]:


n = 100 # number of predictions


# ## Define model

# In[ ]:



my_order = (2, 1, 1)
my_seasonal_order = (1, 1, 1, 52)  # this will cause me problems as some years will have less than 52 weeks
# define model
model = SARIMAX(data['All ages: both sexes'], order=my_order, seasonal_order=my_seasonal_order)

#TODO
# Do something with this error: ValueWarning: A date index has been provided, but it has no associated frequency information 
# and so will be ignored when e.g. forecasting.


# ## Fit model and forecast

# In[ ]:


model_fit = model.fit()


# In[ ]:


yhat = model_fit.forecast(n)


# In[ ]:


base = data.index[-1]
date_list = [base + datetime.timedelta(days=x*7) for x in range(n)]

plt.figure(figsize=(12,8));
plt.plot(data.index, data["All ages: both sexes"], label="Measured");
plt.plot(date_list,yhat, label = "Predicted");
plt.xlabel("Date");
plt.ylabel("Total deaths per week");
plt.title("Deaths per week in The Netherlands - measured and predicted by SARIMAX (2,1,1)");
plt.legend();

