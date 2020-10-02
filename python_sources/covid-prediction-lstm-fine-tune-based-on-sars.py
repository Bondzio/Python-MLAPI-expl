#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# **Recently, Covid-19 is spreading around the globe. There is an outbreak in almost everywhere around the world. There are lots of researches focusing on analyzing and predicting the diffusing of this kind of fatal virus, the same as I did in this project. The whole project could be separated into two main parts, EDA (Exploratory Data Analysis) and Prediction.**
# 
# **The first part includes data aggregation and data visualization. Because of the convenience of invoking, all the actions have been done in Pandas and Numpy. There is another type of data processing building in Pyspark at the top of Databricks.**
# 
# **The second part is the biggest difference compared with other same kinds of work. Normally, if people want to involve deep learning, only the LSTM model will be picked. But I also drew on the experience of transfer learning and built my own LSTM base model for Covid-19 in terms of the SARS-2003 dataset.**
# 
# **However, given that the lacks of data from both SARS and Covid-19 are irreversible, the final performance for transfer learning model is a little bit weak and it only shows the learning capacity from the base model, but the adjustable ability according to Covid-19 dataset is not enough. So there is quite a long way for this project to use transfer learning in a real prediction data science case.**
# 
# 
# >#  <font color='Blue'>Contents :</font>
# >1. [Necessary libraries](#0)
# >1. [Data Injection](#1)
# >1. [Data Aggregation & Data Visualization](#2)
# >>    1. [World Epidemic Progress ](#2.1)
# >>    1. [Global Case Map ](#2.2)
# >>    1. [Pie Chart of Global Distribution ](#2.3)
# >>    1. [Comparison between SARS and Covid-19 dataset ](#2.4)
# >>        1. [Confirmed Percentage](#2.41)
# >>        1. [Recovered Percentage](#2.42)
# >1. [Perdiction](#3)
# >>    1. [Base Model](#3.1)
# >>        1. [Feature Extraction](#3.11)
# >>        1. [Compile the Sars Model](#3.12)
# >>        1. [Train the Sars Model](#3.13)
# >>        1. [Learning Curves](#3.14)
# >>    1. [Fine Tuning](#3.2)
# >>        1. [Format the data](#3.21)
# >>        1. [Load the base model](#3.22)
# >>        1. [Freeze the bottom LSTM layers](#3.23)
# >>        1. [Re-train the model with Covid-19 dataset](#3.24)

# <a id="0"></a> <br>
# # Necessary Libraries
# * **Numpy:** Linear algebra
# * **Pandas:** Data processing and aggregation
# * **Matplotlib:** Simple visualization
# * **Plotly:** Interactive plots - World Epidemic Progress 
# * **Datetime:** Time data manuplation - Data Analysis, Predictions 
# * **Sklearn:** Machine Learning
# * **Keras:** Deep learning - Predictions, LSTM

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime
import requests
import warnings

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras import layers
from keras.models import model_from_json

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# <a id="1"></a> <br>
# # Data Injection

# In[ ]:


df_covid19=pd.read_csv('/kaggle/input/novel-corona-virus-2019-dataset/covid_19_data.csv')
df_covid19.drop(['SNo','Last Update','Province/State'],axis=1,inplace = True)
df_covid19['ObservationDate']=pd.to_datetime(df_covid19['ObservationDate'])


# In[ ]:


# Because there are several updates in the same day, we need a groupby function to merge the data in the same day 
df_covid19 = df_covid19.groupby(["ObservationDate","Country/Region"],as_index = False).sum()
df_covid19_compare = df_covid19
df_covid19 = df_covid19.set_index('ObservationDate')
df_covid19.tail()


# In[ ]:


df_sars = pd.read_csv('../input/sars-2003-complete-dataset-clean/sars_2003_complete_dataset_clean.csv')
df_sars.rename(columns={'Date':'ObservationDate', 'Country':'Country/Region', 'Cumulative number of case(s)':'Confirmed', 'Number of deaths':'Deaths','Number recovered':'Recovered' }, inplace=True)
df_sars['ObservationDate']=pd.to_datetime(df_sars['ObservationDate'])
df_sars_compare = df_sars
df_sars = df_sars.set_index('ObservationDate')


# In[ ]:


Sars_CA = df_sars[df_sars['Country/Region'] == 'China']
Sars_CA.tail()


# <a id="2"></a> <br>
# # Data Aggregation & Data Visualization

# <a id="2.1"></a> <br>
# ## World Epidemic Progress 

# In[ ]:


covid19_new=pd.read_csv('/kaggle/input/novel-corona-virus-2019-dataset/covid_19_data.csv')
covid19_new['Active'] = covid19_new['Confirmed'] - covid19_new['Deaths'] - covid19_new['Recovered']
covid19_new["ObservationDate"] = pd.to_datetime(covid19_new["ObservationDate"])
print("Active Cases Column Added Successfully")
covid19_new.head()


# In[ ]:


wep = covid19_new.groupby(["ObservationDate","Country/Region"])["Confirmed","Deaths","Recovered"].max()
wep = wep.reset_index()
wep["ObservationDate"] = wep["ObservationDate"].dt.strftime("%m,%d,%Y")
wep["Country"] = wep["Country/Region"]

choro_map = px.choropleth(wep, 
                          locations= "Country", 
                          locationmode = "country names",
                          color = "Confirmed", 
                          hover_name = "Country/Region",
                          projection = "natural earth",
                          animation_frame = "ObservationDate",
                          color_continuous_scale = "Blues",
                          range_color = [10000,200000])
choro_map.update_layout(
    title_text = 'Global Spread of Coronavirus',
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
    ))
    
choro_map.show()


# In[ ]:


covid19_new.rename(columns={'ObservationDate':'Date', 'Country/Region':'Country', 'Province/State':'Province' }, inplace=True)
covid19_new['Date']=pd.to_datetime(covid19_new['Date'])

maxdate=max(covid19_new['Date'])

fondate=maxdate.strftime("%Y-%m-%d")
print("The last observation date is {}".format(fondate))
ondate = format(fondate)


# <a id="2.2"></a> <br>
# ## Global Case Map 

# In[ ]:


date_list1 = list(covid19_new["Date"].unique())
confirmed = []
deaths = []
recovered = []
active = []
for i in date_list1:
    x = covid19_new[covid19_new["Date"] == i]
    confirmed.append(sum(x["Confirmed"]))
    deaths.append(sum(x["Deaths"]))
    recovered.append(sum(x["Recovered"]))
    active.append(sum(x["Active"]))
data_glob = pd.DataFrame(list(zip(date_list1,confirmed,deaths,recovered,active)),columns = ["Date","Confirmed","Deaths","Recovered","Active"])
data_glob.tail()


# In[ ]:


import plotly.graph_objs as go 
trace1 = go.Scatter(
x = data_glob["Date"],
y = data_glob["Confirmed"],
mode = "lines",
name = "Confirmed",
line = dict(width = 2.5),
marker = dict(color = [0, 1, 2, 3])
)

trace2 = go.Scatter(
x = data_glob["Date"],
y = data_glob["Deaths"],
mode = "lines",
name = "Deaths",
line = dict(width = 2.5),
marker = dict(color = [0, 1, 2, 3])
)

trace3 = go.Scatter(
x = data_glob["Date"],
y = data_glob["Recovered"],
mode = "lines",
name = "Recovered",
line = dict(width = 2.5),    
marker = dict(color = [0, 1, 2, 3])
)

trace4 = go.Scatter(
x = data_glob["Date"],
y = data_glob["Active"],
mode = "lines",
name = "Active",
line = dict(width = 2.5),
marker = dict(color = [0, 1, 2, 3])
)

data_plt = [trace1,trace2,trace3,trace4]
layout = go.Layout(title = "Global Case States",xaxis_title="Date",yaxis_title="Number of Total Cases",
                   legend=dict(
        x=0,
        y=1,),hovermode='x')
fig = go.Figure(data = data_plt,layout = layout)

fig.show()


# <a id="2.3"></a> <br>
# ## Pie Chart of Global Distribution 

# In[ ]:


labels = ["Recovered","Deaths","Active"]
values = [data_glob.tail(1)["Recovered"].iloc[0],data_glob.tail(1)["Deaths"].iloc[0],data_glob.tail(1)["Active"].iloc[0]]

fig = go.Figure(data = [go.Pie(labels = labels, values = values,textinfo='label+percent',insidetextorientation='radial')],layout = go.Layout(title = "Global Patient Percentage"))
fig.show()


# <a id="2.4"></a> <br>
# ## Comparison between SARS and Covid-19 dataset

# In[ ]:


df_covid19_compare.info()


# In[ ]:


df_sars_compare.info()


# 

# In[ ]:


date_list_cov_compare = list(df_covid19_compare["ObservationDate"].unique())
confirmed = []
deaths = []
recovered = []
for i in date_list_cov_compare:
    x = df_covid19_compare[df_covid19_compare["ObservationDate"] == i]
    confirmed.append(sum(x["Confirmed"]))
    deaths.append(sum(x["Deaths"]))
    recovered.append(sum(x["Recovered"]))
data_glob_cov = pd.DataFrame(list(zip(date_list_cov_compare,confirmed,deaths,recovered)),columns = ["Date","Confirmed","Deaths","Recovered"])
data_glob_cov.tail()


# In[ ]:


date_list_sars_compare = list(df_sars_compare["ObservationDate"].unique())
confirmed = []
deaths = []
recovered = []
for i in date_list_sars_compare:
    x = df_sars_compare[df_sars_compare["ObservationDate"] == i]
    confirmed.append(sum(x["Confirmed"]))
    deaths.append(sum(x["Deaths"]))
    recovered.append(sum(x["Recovered"]))
data_glob_sars = pd.DataFrame(list(zip(date_list_sars_compare,confirmed,deaths,recovered)),columns = ["Date","Confirmed","Deaths","Recovered"])
data_glob_sars.tail()


# <a id="2.41"></a> <br>
# ## Confirmed Percentage

# In[ ]:


from plotly import subplots
death_percent_sars = ((data_glob_sars["Deaths"]*100)/data_glob_sars["Confirmed"])
death_percent_cov = ((data_glob_cov["Deaths"]*100)/data_glob_cov["Confirmed"])

trace_death_sars = go.Scatter(x=data_glob_sars["Date"],
                                  y = death_percent_sars,
                                  mode = "lines",
                                  name = "Death Percentage for SARS",
                                  marker = dict(color = [0, 1, 2, 3]))
    
trace_death_cov = go.Scatter(x=data_glob_cov["Date"],
                                  y = death_percent_cov,
                                  mode = "lines",
                                  name = "Death Percentage for Covid-19",
                                  marker = dict(color = [0, 1, 2, 3]))
    
death_plt = [trace_death_sars,trace_death_cov]

fig = subplots.make_subplots(rows=1,cols=2)
fig.append_trace(trace_death_sars,1,1)
fig.append_trace(trace_death_cov,1,2)

fig.layout.width = 1000
fig.layout.height = 600
fig.show()


# <a id="2.42"></a> <br>
# ## Recovered Percentage

# In[ ]:


recover_percent_sars = ((data_glob_sars["Recovered"]*100)/data_glob_sars["Confirmed"])
recover_percent_cov = ((data_glob_cov["Recovered"]*100)/data_glob_cov["Confirmed"])

trace_recover_sars = go.Scatter(x=data_glob_sars["Date"],
                                  y = recover_percent_sars,
                                  mode = "lines",
                                  name = "Recover Percentage for SARS",
                                  marker = dict(color = [0, 1, 2, 3]))
    
trace_recover_cov = go.Scatter(x=data_glob_cov["Date"],
                                  y = recover_percent_cov,
                                  mode = "lines",
                                  name = "Recover Percentage for Covid-19",
                                  marker = dict(color = [0, 1, 2, 3]))
    
recover_plt = [trace_recover_sars,trace_recover_cov]

fig = subplots.make_subplots(rows=1,cols=2)
fig.append_trace(trace_recover_sars,1,1)
fig.append_trace(trace_recover_cov,1,2)
fig.layout.width = 1000
fig.layout.height = 600
fig.show()


# **The recovered percentage explains the probability of using Sars dataset as a base model to analyze Covid-19, because the left graph could clearly show the Sars outbreak had been finished until July 2003 and the recovery rate was almost 90% back then. However, the Coronavirus is still spreading until now. As a result, we could learn some potential distribution from the closed Sars model to model for the new Covid-19.**

# <a id="3"></a> <br>
# # Prediction

# **The main procedures for the prediction part has been shown below,**
# 
# * Input SARS_2003 data set to build our base model
# * Because the outbreak for SARS was mainly located in China, I built an RNN prediction model for SARS in China instead of Canada
# * Save the base model and load COVID-19 dataset
# * Load previous model I built, and its corresponding weights and weights
# * Fine tune that model to predict the cases for Coronavirus in Canada
# 
# 
# 
# 
# 
# 

# <a id="3.1"></a> <br>
# ## Base Model

# In[ ]:


# load Sars data set, and set the country as China
Sars_CA.tail()


# <a id="3.11"></a> <br>
# ## Feature Extraction

# In[ ]:


# data normalization

train_num_sars = int(len(Sars_CA)*0.8)

scaler_sars = MinMaxScaler()

train_origin = pd.DataFrame(Sars_CA.iloc[:train_num_sars,1])
test_origin = pd.DataFrame(Sars_CA.iloc[train_num_sars:,1])

scaler_sars.fit(train_origin)
scaled_train_sars = scaler_sars.transform(train_origin)
scaled_test_sars = scaler_sars.transform(test_origin)


# In[ ]:


# using 10 day lag to predict the model
n_input = 15
n_features = 1
generator_sars = TimeseriesGenerator(scaled_train_sars, scaled_train_sars, length=n_input, batch_size=1)


# In[ ]:


# show the format of our input data
for i in range(3):
    x, y = generator_sars[i]
    print('%s => %s' % (x, y))


# <a id="3.12"></a> <br>
# ## Compile the SARS model

# In[ ]:


# build 4-layer RNN model
# define model
model = Sequential([
    layers.LSTM(256, activation='relu', input_shape=(n_input, n_features),return_sequences=True),
    layers.LSTM(128, activation='relu', input_shape=(n_input, n_features),return_sequences=True),
    layers.LSTM(64, activation='relu', input_shape=(n_input, n_features)),
    layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse')
model.summary()


# <a id="3.14"></a> <br>
# ## Train the SARS model

# In[ ]:


# train the model
model.fit_generator(generator_sars,epochs=25)


# <a id="3.14"></a> <br>
# ## Learning Curves

# In[ ]:


# plot the loss curve
loss_per_epoch = model.history.history['loss']
fig = plt.figure(dpi = 120,figsize = (6,4))
ax = plt.axes()
ax.set(xlabel = 'Number of Epochs',ylabel = 'MSE Loss',title = 'Sars Loss Curve')
plt.plot(range(len(loss_per_epoch)),loss_per_epoch,lw = 1);


# In[ ]:


# test our model in test set
test_predictions = []

first_eval_batch = scaled_train_sars[-n_input:]
current_batch = first_eval_batch.reshape((1, n_input, n_features))

for i in range(len(test_origin)):
    
    # get prediction 1 time stamp ahead ([0] is for grabbing just the number instead of [array])
    current_pred = model.predict(current_batch)[0]
    
    # store prediction
    test_predictions.append(current_pred) 
    
    # update batch to now include prediction and drop first value
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)


# In[ ]:


# fill test table with prediction
true_predictions = scaler_sars.inverse_transform(test_predictions)
test_origin['Predictions'] = true_predictions
print(test_origin)


# In[ ]:


# plot the comparison between actual value and predicted value
fig = plt.figure(dpi = 120)
ax=plt.axes()
test_origin.plot(legend=True,figsize=(6,4),lw = 2,ax=ax)
plt.xlabel('Date')
plt.ylabel('Count of Cases')
plt.title('Comparision Test and Prediction')
plt.show();


# In[ ]:


# build complete SARS model with the whole data set (train+test)
scaler_sars = MinMaxScaler()

train_origin = pd.DataFrame(Sars_CA.iloc[:,1])


scaler_sars.fit(train_origin)
scaled_train_sars = scaler_sars.transform(train_origin)

n_input = 15
n_features = 1
generator_sars = TimeseriesGenerator(scaled_train_sars, scaled_train_sars, length=n_input, batch_size=1)

# define model
model_whole = Sequential([
    layers.LSTM(256, activation='relu', input_shape=(n_input, n_features),return_sequences=True),
    layers.LSTM(128, activation='relu', input_shape=(n_input, n_features),return_sequences=True),
    layers.LSTM(64, activation='relu', input_shape=(n_input, n_features)),
    layers.Dense(1)
])
model_whole.compile(optimizer='adam', loss='mse')

# fit model
model_whole.fit_generator(generator_sars,epochs=25)


# In[ ]:


# plot loss curve for complete model
loss_per_epoch = model_whole.history.history['loss']
fig = plt.figure(dpi = 120,figsize = (6,4))
ax = plt.axes()
ax.set(xlabel = 'Number of Epochs',ylabel = 'MSE Loss',title = 'Loss Curve of Base Model')
plt.plot(range(len(loss_per_epoch)),loss_per_epoch,lw = 2)
fig.show()


# In[ ]:


# save SARS model and its weights
json_config = model_whole.to_json()
with open('model_config.json', 'w') as json_file:
    json_file.write(json_config)
model_whole.save_weights('path_to_my_weights.h5')


# <a id="3.2"></a> <br>
# ## Fine Tuning

# <a id="3.21"></a> <br>
# ## Format the data

# In[ ]:


# load COVID-19 dataset, and set country as Canada
Covid_CA = df_covid19[df_covid19['Country/Region'] == 'Canada']
Covid_CA.head()


# In[ ]:


# normalization

train_num = int(len(Covid_CA)*0.8)

scaler = MinMaxScaler()

train = pd.DataFrame(Covid_CA.iloc[:train_num,1])
test = pd.DataFrame(Covid_CA.iloc[train_num:,1])

scaler.fit(train)
scaled_train = scaler.transform(train)
scaled_test = scaler.transform(test)


# In[ ]:


# show confirmation cases after normalization 
print("Scaled Train Set:", scaled_train[:3],"\n")
print("Scaled Test Set:", scaled_test[:3])


# In[ ]:


# equally, we set 10 day lag for modelling
n_input = 15
n_features = 1
generator = TimeseriesGenerator(scaled_train, scaled_train, length=n_input, batch_size=1)


# In[ ]:


# show data format
for i in range(3):
    x, y = generator[i]
    print('%s => %s' % (x, y))


# <a id="3.22"></a> <br>
# ## Load the Base Model

# In[ ]:


# load SARS model
model_cov = model_from_json(open('model_config.json').read())
model_cov.load_weights('path_to_my_weights.h5')
model_cov.summary()


# **Take a look at the Trainable params.**
# 
# **Up to now, we haven't freeze any layers of the model, so all of the params are trainable.**

# <a id="3.23"></a> <br>
# ## Freeze the Bottom LSTM Layers

# In[ ]:


# Let's take a look to see how many layers are in the base model
print("Number of layers in the base model: ", len(model_cov.layers))

# Fine-tune from this layer onwards
fine_tune_at = 1

# Freeze all the layers before the `fine_tune_at` layer
for layer in model_cov.layers[:fine_tune_at]:
  layer.trainable =  False


# In[ ]:


# now, we locked the first one layers of our network. The Non-trainable params is 66560+49408
model_cov.summary()


# In[ ]:


# compile the new model for training
model_cov.compile(optimizer='adam', loss='mse')


# <a id="3.24"></a> <br>
# ## Re-train the model with Covid-19 dataset

# In[ ]:


# fit model
model_cov.fit_generator(generator,epochs=25)


# In[ ]:


# plot loss curve for new model
loss_per_epoch = model_cov.history.history['loss']
fig = plt.figure(dpi = 120,figsize = (6,4))
ax = plt.axes()
ax.set(xlabel = 'Number of Epochs',ylabel = 'MSE Loss',title = 'Loss Curve - Fine Tuning')
plt.plot(range(len(loss_per_epoch)),loss_per_epoch,lw = 2);


# In[ ]:


test_predictions = []

first_eval_batch = scaled_train[-n_input:]
current_batch = first_eval_batch.reshape((1, n_input, n_features))

for i in range(len(test)):
    
    # get prediction 1 time stamp ahead ([0] is for grabbing just the number instead of [array])
    current_pred = model_cov.predict(current_batch)[0]
    
    # store prediction
    test_predictions.append(current_pred) 
    
    # update batch to now include prediction and drop first value
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)


# In[ ]:


true_predictions = scaler.inverse_transform(test_predictions)
test['Predictions'] = true_predictions
test.head()


# In[ ]:


fig = plt.figure(dpi = 120)
ax=plt.axes()
test.plot(legend=True,figsize=(6,4),lw = 2,ax=ax)
plt.xlabel('Date')
plt.ylabel('Count of Cases')
plt.show();

