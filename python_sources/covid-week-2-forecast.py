#!/usr/bin/env python
# coding: utf-8

# # EDA

# In[ ]:


import numpy as np
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from sklearn import preprocessing
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler

get_ipython().run_line_magic('matplotlib', 'inline')

train_df = pd.read_csv('/kaggle/input/covid19-global-forecasting-week-2/train.csv')
test_df = pd.read_csv('/kaggle/input/covid19-global-forecasting-week-2/test.csv')

display(train_df.info())
display(test_df.info())

display(train_df.head())
display(test_df.head())

display(train_df.isnull().sum())


# ## Following Country having Province State

# In[ ]:


train_df[~train_df['Province_State'].isnull()]['Country_Region'].value_counts()


# In[ ]:


train_df[train_df['Province_State'].isnull()]['Country_Region'].value_counts()


# In[ ]:


train_df['Date'].describe()


# In[ ]:


test_df['Date'].min()


# In[ ]:


test_df['Date'].describe()


# In[ ]:


show_cum = train_df.groupby(by='Country_Region')[['ConfirmedCases','Fatalities']].max().reset_index()
plt.figure(figsize=(20,10))
#sns.set()
sns.barplot(x='ConfirmedCases',y='Country_Region',data=show_cum[show_cum['ConfirmedCases'] != 0].sort_values(by='ConfirmedCases',ascending=False).head(30))


# In[ ]:


plt.figure(figsize=(20,10))
sns.barplot(x='Fatalities',y='Country_Region',data=show_cum[show_cum['Fatalities'] != 0].sort_values(by='Fatalities',ascending=False).head(30))


# # Pre-process Data for DNN

# In[ ]:


days_df = train_df['Date'].apply(lambda dt: datetime.datetime.strptime(dt, '%Y-%m-%d') - datetime.datetime.strptime('2020-01-21', '%Y-%m-%d')).apply(lambda x : str(x).split()[0]).astype(int)

train_df['Days'] = days_df
train_df.drop(['Date','Id'],axis=1,inplace=True)

train_df.fillna('0',inplace=True)


# In[ ]:


days_df = test_df['Date'].apply(lambda dt: datetime.datetime.strptime(dt, '%Y-%m-%d') - datetime.datetime.strptime('2020-01-21', '%Y-%m-%d')).apply(lambda x : str(x).split()[0]).astype(int)

test_df['Days'] = days_df
after_use = test_df.copy()
test_df.drop(['Date','ForecastId'],axis=1,inplace=True)

test_df.fillna('10101',inplace=True)


# In[ ]:


# enc = preprocessing.OneHotEncoder()
# enc.fit(train_df[['Province_State','Country_Region']])
# enc_cntry_pvstate = enc.transform(train_df[['Province_State','Country_Region']]).toarray()
# #display(enc_cntry_pvstate)


# In[ ]:


# enc_test = preprocessing.OneHotEncoder()
# enc_test.fit(test_df[['Province_State','Country_Region']])
# enc_cntry_pvstate_test = enc_test.transform(test_df[['Province_State','Country_Region']]).toarray()
# #display(enc_cntry_pvstate)


# In[ ]:


enc = preprocessing.OrdinalEncoder()
enc.fit(train_df[['Province_State','Country_Region']])
enc_cntry_pvstate = enc.transform(train_df[['Province_State','Country_Region']])#.toarray()
#display(enc_cntry_pvstate)


# In[ ]:


enc_test = preprocessing.OrdinalEncoder()
enc_test.fit(test_df[['Province_State','Country_Region']])
enc_cntry_pvstate_test = enc_test.transform(test_df[['Province_State','Country_Region']])#.toarray()
#display(enc_cntry_pvstate)


# In[ ]:


train_df.drop(['Province_State','Country_Region'],axis=1,inplace=True)

train_df['Province_State'] = enc_cntry_pvstate[:,0]
train_df['Country_Region'] = enc_cntry_pvstate[:,1]

display(train_df.tail())
display(train_df.describe())

train_label_cc = train_df['ConfirmedCases'].to_numpy()
train_label_fa = train_df['Fatalities'].to_numpy()

#normed_train_data = preprocessing.normalize(ncc)
train_data_cc = train_df[['Days','Province_State','Country_Region']]
train_data_fa = train_df[['Days','Province_State','Country_Region','ConfirmedCases']]

plt.figure(figsize=(12,8))
display(sns.distplot(train_label_cc,bins=100))

scaler = MinMaxScaler()
train_data_cc = scaler.fit_transform(train_data_cc)
#X_test = scaler.transform(X_test)


# In[ ]:


test_df.drop(['Province_State','Country_Region'],axis=1,inplace=True)

test_df['Province_State'] = enc_cntry_pvstate_test[:,0]
test_df['Country_Region'] = enc_cntry_pvstate_test[:,1]

#normed_train_data = preprocessing.normalize(ncc)
test_data_cc = test_df[['Days','Province_State','Country_Region']]
test_data_cc = scaler.transform(test_data_cc)


# # Deep Learning - time series - ANN

# In[ ]:


import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)


# In[ ]:


# def build_model(cc_input_size):
#   model = keras.Sequential([
#     layers.Dense(128, activation='relu', input_shape=cc_input_size),
#     layers.Dropout(0.2),
#     layers.Dense(64, activation='relu'),
#     layers.Dropout(0.2),
#     layers.Dense(32, activation='relu'),
#     layers.Dropout(0.2),
#     layers.Dense(16, activation='relu'),
#     layers.Dropout(0.2),
#     layers.Dense(8, activation='relu'),
#     layers.Dropout(0.2),
#     layers.Dense(8, activation='relu'),
#     layers.Dropout(0.2),
#     layers.Dense(4, activation='relu'),
#     layers.Dropout(0.2),
#     layers.Dense(2, activation='relu'),
#     layers.Dense(1)
#   ])

#   #optimizer = tf.keras.optimizers.RMSprop(0.001)
#   optimizer = tf.keras.optimizers.Adam()

#   model.compile(loss='mse',
#                 optimizer=optimizer,
#                 metrics=['mae', 'mse'])
#   return model


# In[ ]:


# def add_layers(num_of_ly):
#     for i in range():
#         layers.Dense(64, activation='relu'),
#     layers.Dropout(0.2),


# In[ ]:


def build_model(cc_input_size):
  model = keras.Sequential([
    layers.Dense(512, activation='relu', input_shape=cc_input_size),
    layers.Dropout(0.5),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),
#     layers.Dense(512, activation='relu'),
#     layers.Dropout(0.2),
#     layers.Dense(512, activation='relu'),
#     layers.Dropout(0.2),
#     layers.Dense(512, activation='relu'),
#     layers.Dropout(0.2),
    layers.Dense(1)
  ])

  #optimizer = tf.keras.optimizers.RMSprop(0.001)
  optimizer = tf.keras.optimizers.Adam()

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model


# In[ ]:


cc_input_size = [3]
model_cc = build_model(cc_input_size)

EPOCHS = 250

callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
history = model_cc.fit(
  train_data_cc, train_label_cc,
  epochs=EPOCHS, batch_size=16, callbacks=[callback],verbose=2)

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
display(hist.tail())


# In[ ]:


hist[['mae']].plot()
plt.ylabel('Confirmaed Cases / Infected ')


# In[ ]:


hist[['mse']].plot()
plt.ylabel('Confirmaed Cases / Infected ')


# In[ ]:


# Train Fatality Model

cc_input_size = [4]
model_fa = build_model(cc_input_size)

EPOCHS = 250

callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

history = model_fa.fit(
  train_data_fa, train_label_fa,
  epochs=EPOCHS, validation_split = 0.3, batch_size=16,callbacks=[callback],verbose=2)

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
display(hist.tail())


# In[ ]:


hist[['mae']].plot()
plt.ylabel('Confirmaed Cases / Infected ')


# In[ ]:


hist[['mse']].plot()
plt.ylabel('Confirmaed Cases / Infected ')


# In[ ]:


# model.save('saved_model/my_model')

# new_model = tf.keras.models.load_model('saved_model/my_model')

# # Check its architecture
# new_model.summary()


# # Prediction

# In[ ]:


# test_predictions_cc = {}
# i = 0

# for ids in after_use['ForecastId'].to_list():
#     tmp = pd.DataFrame(test_data_cc.iloc[i]).transpose()
#     test_predictions_cc[ids] = model_cc.predict(tmp)
#     i +=1


# In[ ]:


test_predictions_cc = model_cc.predict(test_data_cc)


# In[ ]:


#Fatality
test_data_fa = test_df[['Days','Province_State','Country_Region']]
#,'ConfirmedCases'
test_data_fa['ConfirmedCases'] = test_predictions_cc

normed_test_data = test_data_fa

test_predictions = model_fa.predict(normed_test_data)


# In[ ]:


submit_df = pd.DataFrame()
submit_df['ForecastId'] = after_use['ForecastId']
submit_df['ConfirmedCases'] = pd.DataFrame(test_predictions_cc)
submit_df['ConfirmedCases'] = submit_df['ConfirmedCases'].astype(int)
submit_df['Fatalities'] = pd.DataFrame(test_predictions)
submit_df['Fatalities'] = submit_df['Fatalities'].astype(int)
#submit_df.info()
submit_df.to_csv('submission.csv',index=False)


# In[ ]:


submit_df.head()


# In[ ]:


submit_df.describe().transpose()


# In[ ]:


model_cc.save('saved_model/model_cc')
model_cc.save('saved_model/model_fa')


# In[ ]:




