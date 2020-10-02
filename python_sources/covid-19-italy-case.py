#!/usr/bin/env python
# coding: utf-8

# # COVID-19 Novel Coronavirus: EDA & Forecast Number of Cases

# ## COVID Analysis
# 
# Inspired by COVID-19 Novel Coronavirus EDA & Forecasting Cases

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.graph_objects as go
from fbprophet import Prophet
import pycountry
import plotly.express as px


# # Data Import, Preprocessing and EDA

# In[ ]:


df = pd.read_csv('../input/novel-corona-virus-2019-dataset/covid_19_data.csv',parse_dates=['Last Update'])
df.rename(columns={'ObservationDate':'Date', 'Country/Region':'Country'}, inplace=True)

df_confirmed = pd.read_csv("/kaggle/input/novel-corona-virus-2019-dataset/time_series_covid_19_confirmed.csv")
df_recovered = pd.read_csv("/kaggle/input/novel-corona-virus-2019-dataset/time_series_covid_19_recovered.csv")
df_deaths = pd.read_csv("/kaggle/input/novel-corona-virus-2019-dataset/time_series_covid_19_deaths.csv")

df_confirmed.rename(columns={'Country/Region':'Country'}, inplace=True)
df_recovered.rename(columns={'Country/Region':'Country'}, inplace=True)
df_deaths.rename(columns={'Country/Region':'Country'}, inplace=True)


# In[ ]:


df.head(10)


# ## Percentages of Deaths and Recovered over Confirmed

# In[ ]:


df['Date']


# In[ ]:


last_day=df.query('Date == "03/13/2020"')
last_day


# In[ ]:


#Country=last_day['Country','Date','Confirmed','Deaths','Recovered']
Country = last_day.sort_values("Confirmed",ascending=False).reset_index()
Country.head()


# In[ ]:


Perc_rec = (Country['Recovered'] / Country['Confirmed']) * 100
Perc_death = (Country['Deaths'] / Country['Confirmed']) * 100
Country['Percentage_recovery'] = Perc_rec
Country['Percentage_deaths'] = Perc_death


# In[ ]:


Country['Country']


# In[ ]:


plt.bar(Country['Country'][0:5], Country['Percentage_deaths'][0:5],align='center', alpha=0.5)
#plt.xticks(y_pos, objects)
plt.ylabel('Usage')
plt.title('Programming language usage')

plt.show()


# In[ ]:


plt.bar(Country['Country'][0:5], Country['Percentage_recovery'][0:5],align='center', alpha=0.5)
#plt.xticks(y_pos, objects)
plt.ylabel('Usage')
plt.title('Programming language usage')

plt.show()


# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(x=Country['Country'][0:5],
                y=Country['Percentage_deaths'][0:5],
                name='Deaths[%]',
                marker_color='red'
                ))
fig.add_trace(go.Bar(x=Country['Country'][0:5],
                y=Country['Percentage_recovery'][0:5],
                name='Recovered[%]',
                marker_color='green'
                ))


fig.update_layout(
    title='Worldwide Corona Virus Cases - Bar Chart',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Percentages [%]',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
fig.show()


# ## Italy

# In[ ]:


ItalyDF=df.query('Country=="Italy"').groupby("Date")


# ## Latest Cases

# In[ ]:


ItalyDF.head()


# ## Italy View // China view

# In[ ]:


Italy=df.query('Country=="Italy"').groupby("Date")[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()
China=df.query('Country=="Mainland China"').groupby("Date")[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()


# In[ ]:


Italy.tail()


# # Visualizations

# In[ ]:


Italy.groupby('Confirmed').sum()


# In[ ]:


confirmed_IT = Italy.groupby('Date').sum()['Confirmed'].reset_index()
deaths_IT = Italy.groupby('Date').sum()['Deaths'].reset_index()
recovered_IT = Italy.groupby('Date').sum()['Recovered'].reset_index()

confirmed_CHN = China.groupby('Date').sum()['Confirmed'].reset_index()
deaths_CHN = China.groupby('Date').sum()['Deaths'].reset_index()
recovered_CHN = China.groupby('Date').sum()['Recovered'].reset_index()


# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(x=confirmed_CHN['Date'],
                y=confirmed_CHN['Confirmed'],
                name='Confirmed CHN',
                marker_color='red'
                ))
fig.add_trace(go.Bar(x=confirmed_IT['Date'],
                y=confirmed_IT['Confirmed'],
                name='Confirmed ITA',
                marker_color='green'
                ))


fig.update_layout(
    title='Worldwide Corona Virus Cases - Confirmed China / Italy',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
fig.show()


# In[ ]:


new_cases_CHN = confirmed_CHN['Confirmed'].diff()
new_cases_IT = confirmed_IT['Confirmed'].diff()


# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(x=confirmed_CHN['Date'],
                y=new_cases_CHN,
                name='Confirmed CHN',
                marker_color='red'
                ))
fig.add_trace(go.Bar(x=confirmed_IT['Date'],
                y=new_cases_IT,
                name='Confirmed ITA',
                marker_color='green'
                ))


fig.update_layout(
    title='Worldwide Corona Virus Cases - Confirmed China / Italy',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of New Cases',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
fig.show()


# In[ ]:


from plotly.subplots import make_subplots
fig = make_subplots(rows=1, cols=2)
#fig = go.Figure()
fig.add_trace(go.Bar(x=confirmed_CHN['Date'],
                y=new_cases_CHN,
                name='Confirmed CHN',
                marker_color='red'),
                1, 1
                )
fig.add_trace(go.Bar(x=confirmed_IT['Date'],
                y=new_cases_IT,
                name='Confirmed ITA',
                marker_color='green'),
                1, 2
                )


fig.update_layout(
    title='Worldwide Corona Virus Cases - Confirmed China / Italy',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
fig.show()


# ## Summary Plot of Italy Cases - Confirmed, Deaths & Recovered

# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(x=confirmed_IT['Date'],
                y=confirmed_IT['Confirmed'],
                name='Confirmed',
                marker_color='blue'
                ))
fig.add_trace(go.Bar(x=deaths_IT['Date'],
                y=deaths_IT['Deaths'],
                name='Deaths',
                marker_color='Red'
                ))
fig.add_trace(go.Bar(x=recovered_IT['Date'],
                y=recovered_IT['Recovered'],
                name='Recovered',
                marker_color='Green'
                ))

fig.update_layout(
    title='Italy Corona Virus Cases - Confirmed, Deaths, Recovered (Bar Chart)',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
fig.show()


# ## Transforming Data for Forecasting

# In[ ]:


confirmed = Italy.groupby('Date').sum()['Confirmed'].reset_index()
deaths = Italy.groupby('Date').sum()['Deaths'].reset_index()
recovered = Italy.groupby('Date').sum()['Recovered'].reset_index()


# In[ ]:


confirmed.columns = ['ds','y']
#confirmed['ds'] = confirmed['ds'].dt.date
confirmed['ds'] = pd.to_datetime(confirmed['ds'])


# In[ ]:


confirmed.head()


# # Forecasting Total Number of Cases Worldwide
# 
# ## Prophet
# 
# We use Prophet, a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. 

# ## Forecasting Confirmed Cases Worldwide with Prophet (Baseline)
# 
# We perform a week's ahead forecast with Prophet, with 95% prediction intervals. Here, no tweaking of seasonality-related parameters and additional regressors are performed.

# In[ ]:


m = Prophet(interval_width=0.95)
m.fit(confirmed)
future = m.make_future_dataframe(periods=7)
future.tail()


# In[ ]:


forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


# In[ ]:


confirmed_forecast_plot = m.plot(forecast)


# In[ ]:





# ## Forecasting Deaths Worldwide with Prophet (Baseline)
# 
# We perform a week's ahead forecast with Prophet, with 95% prediction intervals. Here, no tweaking of seasonality-related parameters and additional regressors are performed.

# In[ ]:


deaths.columns = ['ds','y']
deaths['ds'] = pd.to_datetime(deaths['ds'])


# In[ ]:


m = Prophet(interval_width=0.95)
m.fit(deaths)
future = m.make_future_dataframe(periods=7)
future.tail()


# In[ ]:


forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


# In[ ]:


deaths_forecast_plot = m.plot(forecast)


# ## Forecasting Recovered Cases Worldwide with Prophet (Baseline)
# 
# We perform a week's ahead forecast with Prophet, with 95% prediction intervals. Here, no tweaking of seasonality-related parameters and additional regressors are performed.

# In[ ]:


recovered.columns = ['ds','y']
recovered['ds'] = pd.to_datetime(recovered['ds'])


# In[ ]:


m = Prophet(interval_width=0.95)
m.fit(recovered)
future = m.make_future_dataframe(periods=14)
future.tail()


# In[ ]:


forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


# In[ ]:


recovered_forecast_plot = m.plot(forecast)


# ### Time Series Forecasting TEST

# In[ ]:


#confirmed_CHN


# In[ ]:


confirmed_CHN2 = confirmed_CHN
confirmed_CHN2 = confirmed_CHN2.drop(['Date'], axis=1)
confirmed_CHN2.index = pd.DatetimeIndex(confirmed_CHN['Date'])


# In[ ]:


type(confirmed_CHN2['Confirmed'][0])


# In[ ]:


from pylab import rcParams
import statsmodels.api as sm
mod = sm.tsa.statespace.SARIMAX(confirmed_CHN2['Confirmed'],
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])


# In[ ]:


results.plot_diagnostics(figsize=(16, 8))
plt.show()


# In[ ]:


pred = results.get_prediction(start=pd.to_datetime('2020-02-20'), dynamic=False)
pred_ci = pred.conf_int()


# In[ ]:


pred_ci.head()
#mean_values = pred_ci['upper Confirmed'] - pred_ci['lower Confirmed'] / 2
#mean_values


# In[ ]:


fig, ax = plt.subplots()
ax.plot(pred_ci.index, pred.predicted_mean, '-')
ax.plot(pred_ci.index, confirmed_CHN2['Confirmed'][-24:], '-',color='red')
ax.fill_between(pred_ci.index, pred_ci['lower Confirmed'], pred_ci['upper Confirmed'], alpha=0.2)
#ax.plot(x, y, 'o', color='tab:brown')


# In[ ]:


pred_uc = results.get_forecast(steps=20)
pred_ci_next = pred_uc.conf_int()
#pred_uc.predicted_mean


# In[ ]:


fig, ax = plt.subplots()
ax.plot(pred_ci_next.index, pred_uc.predicted_mean, '-')
#ax.plot(pred_ci.index, confirmed_CHN2['Confirmed'][-24:], '-',color='red')
ax.fill_between(pred_ci_next.index, pred_ci_next['lower Confirmed'], pred_ci_next['upper Confirmed'], alpha=0.2)
#ax.plot(x, y, 'o', color='tab:brown')


# ### Forecast ITALY

# In[ ]:


confirmed_IT2 = confirmed_IT
confirmed_IT2 = confirmed_IT2.drop(['Date'], axis=1)
confirmed_IT2.index = pd.DatetimeIndex(confirmed_IT['Date'])


# In[ ]:


mod2 = sm.tsa.statespace.SARIMAX(confirmed_IT2['Confirmed'],
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod2.fit()
print(results.summary().tables[1])


# In[ ]:


results.plot_diagnostics(figsize=(16, 8))
plt.show()


# In[ ]:


pred = results.get_prediction(start=pd.to_datetime('2020-02-20'), dynamic=False)
pred_ci = pred.conf_int()


# In[ ]:


fig, ax = plt.subplots()
ax.plot(pred_ci.index, pred.predicted_mean, '-')
ax.plot(pred_ci.index, confirmed_IT2['Confirmed'][-24:], '-',color='red')
ax.fill_between(pred_ci.index, pred_ci['lower Confirmed'], pred_ci['upper Confirmed'], alpha=0.2)
#ax.plot(x, y, 'o', color='tab:brown')


# In[ ]:


pred_uc = results.get_forecast(steps=20)
pred_ci_next = pred_uc.conf_int()
#pred_uc.predicted_mean


# In[ ]:


fig, ax = plt.subplots()
ax.plot(pred_ci_next.index, pred_uc.predicted_mean, '-')
#ax.plot(pred_ci.index, confirmed_CHN2['Confirmed'][-24:], '-',color='red')
ax.fill_between(pred_ci_next.index, pred_ci_next['lower Confirmed'], pred_ci_next['upper Confirmed'], alpha=0.2)
#ax.plot(x, y, 'o', color='tab:brown')


# In[ ]:


new_cases_forecast = pred_uc.predicted_mean.diff()
new_cases_forecast


# In[ ]:


from plotly.subplots import make_subplots
fig = go.Figure()
fig.add_trace(go.Bar(x=pred_ci_next.index,
                y=new_cases_forecast,
                name='Confirmed CHN',
                marker_color='red'),
                )



fig.update_layout(
    title='Worldwide Corona Virus Cases - Confirmed China / Italy',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
fig.show()


# In[ ]:


df.head(4)


# In[ ]:


import matplotlib.pyplot as plt
plt.plot(df.Date,df.Confirmed)


# In[ ]:





# In[ ]:


df['Country'].value_counts()


# In[ ]:


my_dataset = ['Date','Country', 'Confirmed', 'Deaths','Recovered']


# In[ ]:


my_dataset_df = df[my_dataset]


# In[ ]:


my_dataset_df.head()


# In[ ]:


df_Italy = my_dataset_df.where(my_dataset_df['Country']=='Italy').dropna(axis=0)


# In[ ]:


df_Italy.head()


# In[ ]:


print(df_Italy['Confirmed'].min())
print(df_Italy['Confirmed'].max())


# In[ ]:


df_Italy.shape


# In[ ]:


import matplotlib.pyplot as plt
plt.plot(df_Italy.Date,df_Italy.Confirmed)


# In[ ]:


df = df_Italy


# In[ ]:


TRAIN_SPLIT = int(0.7*(df.shape[0]))
print(TRAIN_SPLIT)


# In[ ]:


def univariate_data(dataset, start_index, end_index, history_size, target_size):
  data = []
  labels = []

  start_index = start_index + history_size
  if end_index is None:
    end_index = len(dataset) - target_size

  for i in range(start_index, end_index):
    indices = range(i-history_size, i)
    # Reshape data from (history_size,) to (history_size, 1)
    data.append(np.reshape(dataset[indices], (history_size, 1)))
    labels.append(dataset[i+target_size])
  return np.array(data), np.array(labels)


# In[ ]:





# In[ ]:


uni_data = df["Confirmed"]
uni_data.index = df["Date"]
uni_data.head()


# In[ ]:


uni_data = uni_data.values


# In[ ]:


uni_train_mean = uni_data[:TRAIN_SPLIT].mean()
uni_train_std = uni_data[:TRAIN_SPLIT].std()
uni_data = (uni_data-uni_train_mean)/uni_train_std


# In[ ]:


univariate_past_history = 300
univariate_future_target = 30

univariate_past_history = 5
univariate_future_target = 3

x_train_uni, y_train_uni = univariate_data(uni_data, 0, TRAIN_SPLIT,
                                           univariate_past_history,
                                           univariate_future_target)
x_val_uni, y_val_uni = univariate_data(uni_data, TRAIN_SPLIT, None,
                                       univariate_past_history,
                                       univariate_future_target)


# In[ ]:


def create_time_steps(length):
  return list(range(-length, 0))


# In[ ]:


def show_plot(plot_data, delta, title):
  labels = ['History', 'True Future', 'Model Prediction']
  marker = ['.-', 'rx', 'go']
  time_steps = create_time_steps(plot_data[0].shape[0])
  if delta:
    future = delta
  else:
    future = 0

  plt.title(title)
  for i, x in enumerate(plot_data):
    if i:
      plt.plot(future, plot_data[i], marker[i], markersize=10,
               label=labels[i])
    else:
      plt.plot(time_steps, plot_data[i].flatten(), marker[i], label=labels[i])
  plt.legend()
  plt.xlim([time_steps[0], (future+5)*2])
  plt.xlabel('Time-Step')
  return plt


# In[ ]:


try:
  # %tensorflow_version only exists in Colab.
  get_ipython().run_line_magic('tensorflow_version', '2.x')
  print(tf.__version__)
except Exception:
  pass


# In[ ]:


import tensorflow as tf
from tensorflow.keras.layers import (Input, Activation, Dense, Flatten, Conv1D, LSTM,
                                     MaxPooling1D, Dropout, BatchNormalization)


# In[ ]:


BATCH_SIZE = 16
BUFFER_SIZE = 10000

train_univariate = tf.data.Dataset.from_tensor_slices((x_train_uni, y_train_uni))
train_univariate = train_univariate.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

val_univariate = tf.data.Dataset.from_tensor_slices((x_val_uni, y_val_uni))
val_univariate = val_univariate.batch(BATCH_SIZE).repeat()


# In[ ]:


x_train_uni.shape[-2:]


# In[ ]:


#Define the model

class model (tf.keras.Model):
    
    def __init__(self):
       
        super(model, self).__init__()
        
        self.conv_1 = Conv1D(32, kernel_size=5,
                      strides=1, padding="causal",
                      activation="relu",
                      input_shape=x_train_uni.shape[-2:]) 
        
        self.LSTM_1 = LSTM(64, return_sequences=True)
        self.LSTM_2 = LSTM(64, return_sequences=True) 
  
        self.flatten = tf.keras.layers.Flatten()
 
        self.dense_1 = tf.keras.layers.Dense(units=30, activation='relu')
        self.dense_2 = tf.keras.layers.Dense(units=10, activation='relu')
        self.dense_3 = tf.keras.layers.Dense(units=1)
        
    def call(self, inputs):

        x = self.conv_1(inputs)
        x = self.LSTM_1(x)
        x = self.LSTM_2(x)
                
        x = self.flatten(x)
        x = self.dense_1(x)     
        x = self.dense_2(x)
        x = self.dense_3(x)
        
        return x


# In[ ]:


simple_lstm_model = model()


# In[ ]:


simple_lstm_model.compile(optimizer='adam', loss='mae')


# In[ ]:


EVALUATION_INTERVAL = 20
EPOCHS = 10

simple_lstm_model.fit(train_univariate, epochs=EPOCHS,
                      steps_per_epoch=EVALUATION_INTERVAL,
                      validation_data=val_univariate, validation_steps=50)


# In[ ]:


for x, y in val_univariate.take(3):
  plot = show_plot([x[0].numpy(), y[0].numpy(),
                    simple_lstm_model.predict(x)[0]], 0, 'Simple LSTM model')
  plot.show()


# In[ ]:


df.columns


# In[ ]:


features_considered = ['Confirmed','Deaths', 'Recovered']


# In[ ]:


features = df[features_considered]
features.index = df['Date']


# In[ ]:


def multivariate_data(dataset, target, start_index, end_index, history_size,
                      target_size, step, single_step=False):
  data = []
  labels = []

  start_index = start_index + history_size
  if end_index is None:
    end_index = len(dataset) - target_size

  for i in range(start_index, end_index):
    indices = range(i-history_size, i, step)
    data.append(dataset[indices])

    if single_step:
      labels.append(target[i+target_size])
    else:
      labels.append(target[i:i+target_size])

  return np.array(data), np.array(labels)


# In[ ]:


BATCH_SIZE = 256
BUFFER_SIZE = 10000
EVALUATION_INTERVAL = 200
EPOCHS = 10


# In[ ]:


dataset = features.values
data_mean = dataset[:TRAIN_SPLIT].mean(axis=0)
data_std = dataset[:TRAIN_SPLIT].std(axis=0)

dataset = (dataset-data_mean)/data_std


# In[ ]:


def multivariate_data(dataset, target, start_index, end_index, history_size,
                      target_size, step, single_step=False):
  data = []
  labels = []

  start_index = start_index + history_size
  if end_index is None:
    end_index = len(dataset) - target_size

  for i in range(start_index, end_index):
    indices = range(i-history_size, i, step)
    data.append(dataset[indices])

    if single_step:
      labels.append(target[i+target_size])
    else:
      labels.append(target[i:i+target_size])

  return np.array(data), np.array(labels)


# In[ ]:


BATCH_SIZE = 256
BUFFER_SIZE = 10000
EVALUATION_INTERVAL = 200
EPOCHS = 10


# In[ ]:


past_history = 410
future_target = 100
STEP = 6

past_history = 5
future_target = 3
STEP = 6

x_train_multi, y_train_multi = multivariate_data(dataset, dataset[:, 1], 0,
                                                 TRAIN_SPLIT, past_history,
                                                 future_target, STEP)
x_val_multi, y_val_multi = multivariate_data(dataset, dataset[:, 1],
                                             TRAIN_SPLIT, None, past_history,
                                             future_target, STEP)


# In[ ]:


print(x_train_multi.shape)
print(y_train_multi.shape)
print(x_val_multi.shape)
print(y_val_multi.shape)


# In[ ]:


train_data_multi = tf.data.Dataset.from_tensor_slices((x_train_multi, y_train_multi))
train_data_multi = train_data_multi.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

val_data_multi = tf.data.Dataset.from_tensor_slices((x_val_multi, y_val_multi))
val_data_multi = val_data_multi.batch(BATCH_SIZE).repeat()


# In[ ]:


#Define the model

class model (tf.keras.Model):
    
    def __init__(self):
       
        super(model, self).__init__()
        
        self.conv_1 = Conv1D(32, kernel_size=5,
                      strides=1, padding="causal",
                      activation="relu",
                      input_shape=x_train_multi.shape[-2:]) 
        
        self.LSTM_1 = LSTM(32, return_sequences=True)
        self.LSTM_2 = LSTM(16, return_sequences=True) 
  
        self.flatten = tf.keras.layers.Flatten()
 
        self.dense_1 = tf.keras.layers.Dense(units=500, activation='relu')
      ##  self.dense_2 = tf.keras.layers.Dense(units=100, activation='relu')
        self.dense_2 = tf.keras.layers.Dense(units=3, activation='relu')
     ##   self.dense_3 = tf.keras.layers.Dense(units=1)
        
    def call(self, inputs):

        x = self.conv_1(inputs)
        x = self.LSTM_1(x)
        x = self.LSTM_2(x)
                
        x = self.flatten(x)
        x = self.dense_1(x)     
        x = self.dense_2(x)
   ##     x = self.dense_3(x)
        
        return x


# In[ ]:


multi_step_model = model()


# In[ ]:


multi_step_model.compile(optimizer=tf.keras.optimizers.RMSprop(clipvalue=1.0), loss='mae')


# In[ ]:


multi_step_history = multi_step_model.fit(train_data_multi, epochs=EPOCHS,
                                          steps_per_epoch=EVALUATION_INTERVAL,
                                          validation_data=val_data_multi,
                                          validation_steps=50)


# In[ ]:


def multi_step_plot(history, true_future, prediction):
  plt.figure(figsize=(12, 6))
  num_in = create_time_steps(len(history))
  num_out = len(true_future)

  plt.plot(num_in, np.array(history[:, 1]), label='History')
  plt.plot(np.arange(num_out)/STEP, np.array(true_future), 'bo',
           label='True Future')
  if prediction.any():
    plt.plot(np.arange(num_out)/STEP, np.array(prediction), 'ro',
             label='Predicted Future')
  plt.legend(loc='upper left')
  plt.show()


# In[ ]:


def create_time_steps(length):
  return list(range(-length, 0))


# In[ ]:


for x, y in val_data_multi.take(3):
  multi_step_plot(x[0], y[0], multi_step_model.predict(x)[0])


# In[ ]:




