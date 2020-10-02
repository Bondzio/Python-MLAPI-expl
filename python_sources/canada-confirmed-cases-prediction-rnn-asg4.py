#!/usr/bin/env python
# coding: utf-8

# # This code is submitted by Jason Hsu(20835712) and Kasra Sadatsharifi(20812219) 

# # Canada Confirmed Cases Predictions
# >In this prediction, our goal is to predict daily confirmed cases in Canada. Seven days of daily confirmed cases would be predicted based on our model. 
# 
# >A recurrent neural network (RNN) based long short-term memory (LSTM) structure has been implemented. We have scaled the features in order to be in the same range as a preprocessing step. Furthermore, one layer of LSTM was implemented and dense and adam optimization were designed to get better results. In the training mode, past five-days of the data were fed to the train data and prediction is done on the sixth-day of data. Assessing the accuracy of the model was attained by mean absolute percentage error. In the end, seven days of daily confirmed cases in Canada were forecast.
# 
# 
# 
# 

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


url = "../input/time-series-covid19-confirmed-global/time_series_covid19_confirmed_global.csv"
df_confirmed = pd.read_csv(url)
# df_confirmed.head()


# In[ ]:


country = "Canada"
df_confirmed1 = df_confirmed[df_confirmed["Country/Region"] == country]
df_confirmed1


# In[ ]:


df_confirmed2 = pd.DataFrame(df_confirmed1[df_confirmed1.columns[4:]].sum(),columns=["confirmed"])
df_confirmed2.index = pd.to_datetime(df_confirmed2.index,format='%m/%d/%y')
df_new = df_confirmed2[["confirmed"]]
df_new.tail(10)


# In[ ]:


# Get train and test
len(df_new)
x = len(df_new)-5
print(x)
train=df_new.iloc[:x]
test = df_new.iloc[x:]
print(len(df_new))


# ## Data preprocessing
# 
# >We tried the other moethod for scaling the data, standard scaler, However it did not work so well on our data thus we switched to minmaxscaler. The accuracy using minmax was 97% and 23% for standard scaler. We can conclude that scaling the data is a very impactful method that need to be chosen wisely.  

# In[ ]:


from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
scaler = MinMaxScaler()
scaler.fit(train) #find max value
MinMaxScaler(copy=True, feature_range=(0, 1))
scaled_train = scaler.transform(train) # divide every point by max value
scaled_test = scaler.transform(test)
print(scaled_train[-5:])


# In[ ]:


from keras.preprocessing.sequence import TimeseriesGenerator
scaled_train.shape
n_input = 5   ## number of steps five days to train the model
n_features = 1  ## number of features you want to predict (for univariate time series n_features=1)
generator = TimeseriesGenerator(scaled_train,scaled_train,length = n_input,batch_size=1) #generates batches of temporal data.
generator[0][0].shape,generator[0][1].shape


# ## LSTM model
# >As shown the model is a simple RNN with a LSTM and a dense layer. The last dense layer is to output one number which is our prediction for the future days. 

# In[ ]:


from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation

model = Sequential()
model.add(LSTM(150,activation="relu",input_shape=(n_input,n_features)))
model.add(Dense(75,activation='relu'))
model.add(Dense(1))
model.compile(optimizer="adam",loss="mse")


# In[ ]:


model.summary()


# In[ ]:


# creating a validation set in order to validate the model
validation_set = np.append(scaled_train[55],scaled_test)
validation_set = validation_set.reshape(6,1)
validation_set


# In[ ]:


n_input = 5
n_features = 1
validation_gen = TimeseriesGenerator(validation_set,validation_set,length=5,batch_size=1)
validation_gen[0][0].shape,validation_gen[0][1].shape


# ## Model fit

# In[ ]:


from tensorflow.keras.callbacks import EarlyStopping,ModelCheckpoint
model.fit_generator(generator,validation_data=validation_gen,epochs=100,steps_per_epoch=10)


# In[ ]:


pd.DataFrame(model.history.history).plot(title="loss vs epochs curve")
model.history.history.keys()
myloss = model.history.history["val_loss"]
plt.title("validation loss vs epochs")
plt.plot(range(len(myloss)),myloss)


# ## Prediction

# In[ ]:


test_prediction = []

##last n points from training set
first_eval_batch = scaled_train[-n_input:]
current_batch = first_eval_batch.reshape(1,n_input,n_features)
current_batch.shape


# In[ ]:


for i in range(len(test)+7):
    current_pred = model.predict(current_batch)[0]
    test_prediction.append(current_pred)
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)
test_prediction


# ## Result of the prediction

# In[ ]:


true_prediction = scaler.inverse_transform(test_prediction)
print(true_prediction[:,0])
time_series_array = test.index
for k in range(0,7):
    time_series_array = time_series_array.append(time_series_array[-1:] + pd.DateOffset(1))

df_forecast = pd.DataFrame(columns=["confirmed","confirmed_predicted"],index=time_series_array)
df_forecast.loc[:,"confirmed_predicted"] = true_prediction[:,0]
df_forecast.loc[:,"confirmed"] = test["confirmed"]
df_forecast


# ## Accuracy

# In[ ]:


MAPE = 1 - np.mean(np.abs(np.array(df_forecast["confirmed"][:5]) - np.array(df_forecast["confirmed_predicted"][:5]))/np.array(df_forecast["confirmed"][:5]))
print("accuracy is " + str(MAPE*100) + " %")
sum_errs = np.sum((np.array(df_forecast["confirmed"][:5]) - np.array(df_forecast["confirmed_predicted"][:5]))**2)
print('sum of errors: ' + str(sum_errs))
stdev = np.sqrt(1/(5-2) * sum_errs)
print('standard deviation:'+ str(stdev))
# calculate prediction interval
interval = 1.96 * stdev
print('interval: '+ str(interval))

