#!/usr/bin/env python
# coding: utf-8

# ## File Directory and Import Libraries

# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


import pandas as pd
import numpy as np
import helpers
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
sns.set()
np.random.seed(42)


# ## Data Fetching

# Define stock symbol

# In[ ]:


symbol = 'DJIA'


# Define output dataset size, `compact` return the last 100 trading days and `full` return the entire history.

# In[ ]:


output_size = 'full'


# Query API

# In[ ]:


df_raw = helpers.fetch_data(symbol, output_size)
df_full = df_raw.copy()


# In[ ]:


# # Fetch local data 
# input_directory = '/kaggle/input/simulation-project-fall2019-sfsu/'
# df_raw = pd.read_csv(input_directory+'daily_adjusted_'+symbol+'.csv')
# df_full = df_raw.copy()


# In[ ]:


df_full = df_full.sort_values(by='timestamp').set_index('timestamp')
df_full = df_full.drop(['dividend_amount', 'split_coefficient'], axis=1)
print('df_full shape:', df_full.shape)
df_full.head()


# Retain only the past 1001 trading days, about 4 years of record.

# In[ ]:


df = df_full.tail(1001)
df.head()


# ## Data Visualization

# In[ ]:


x_ticks_interval = np.arange(0, 1001, 120)
x_ticks_value = df.index[::120]
print('x_ticks_interval.shape:', x_ticks_interval.shape)
print('x_ticks_value.shape', x_ticks_value.shape)


# In[ ]:


plt.style.use(['ggplot'])
plt.figure(figsize=(15,7), dpi=300)
plt.plot(df['close'])
plt.title(symbol+' Close Price Past 1001 Trading Days')
plt.xticks(x_ticks_interval, x_ticks_value)
plt.show()


# ## Create X and y Datasets

# Create X dataset

# In[ ]:


X_pre_shift = df[['open', 'high', 'low', 'close', 'adjusted_close', 'volume']]
print('X_pre_shift shape:', X_pre_shift.shape)
X_pre_shift.head()


# Shift X dataset by 1 period backward

# In[ ]:


X_shifted = helpers.time_series_shift(X_pre_shift)
print('X_shifted.shape', X_shifted.shape)
X_shifted.head()


# Validate shift X values

# In[ ]:


helpers.test_shift_X_values(X_shifted, 0)


# Retain X data at only t-1 period

# In[ ]:


X_pre_transform = X_shifted[X_shifted.columns[:6]]
X_pre_transform.columns = [i+' (t-1)' for i in X_pre_shift.columns.tolist()]
print('X_pre_transform.shape', X_pre_transform.shape)
X_pre_transform.head()


# Create y dataset

# In[ ]:


y_pre_transform = df['close'][1:]
print('y_pre_transform shape:', y_pre_transform.shape)
y_pre_transform.head()


# Validate shape between X and y

# In[ ]:


helpers.test_shape(X_pre_transform, y_pre_transform)


# ## Train, Dev, Test Set Split

# Split dataset first and then transform dataset separetely to prevent information leakage. 

# In[ ]:


X_train_pre_transform, X_dev_pre_transform, X_test_pre_transform = np.split(X_pre_transform, [int(.8 * len(X_pre_transform)), int(.9 * len(X_pre_transform))])


# In[ ]:


print('X_train_pre_transform.shape', X_train_pre_transform.shape)
print('X_dev_pre_transform.shape', X_dev_pre_transform.shape)
print('X_test_pre_transform.shape', X_test_pre_transform.shape)


# In[ ]:


y_train_pre_transform, y_dev_pre_transform, y_test_pre_transform = np.split(y_pre_transform, [int(0.8 * len(y_pre_transform)), int(0.9 * len(y_pre_transform))])


# In[ ]:


print('y_train_pre_transform.shape', y_train_pre_transform.shape)
print('y_dev_pre_transform.shape', y_dev_pre_transform.shape)
print('y_test_pre_transform.shape', y_test_pre_transform.shape)


# Validate shape between X and y

# In[ ]:


X_pre_transform_list = [X_train_pre_transform, X_dev_pre_transform, X_test_pre_transform]
y_pre_transform_list = [y_train_pre_transform, y_dev_pre_transform, y_test_pre_transform]


# In[ ]:


np.all([helpers.test_shape(X, y) for X, y in zip(X_pre_transform_list, y_pre_transform_list)])


# ## Data Transformation

# Standardize X 

# In[ ]:


X_train_pre_sequence, X_dev_pre_sequence, X_test_pre_sequence = [helpers.transform_X('StandardScaler', dataset) for dataset in X_pre_transform_list]


# In[ ]:


print('X_train_pre_sequence.shape', X_train_pre_sequence.shape)
X_train_pre_sequence.head()


# Standardize Y

# In[ ]:


y_train_pre_sequence, y_dev_pre_sequence, y_test_pre_sequence = [helpers.transform_y('StandardScaler', dataset) for dataset in y_pre_transform_list]


# In[ ]:


print('y_train_pre_sequence.shape', y_train_pre_sequence.shape)
print('y_dev_pre_sequence.shape', y_dev_pre_sequence.shape)
print('y_test_pre_sequence.shape', y_test_pre_sequence.shape)


# In[ ]:


y_train_pre_sequence.head()


# Validate transform values

# In[ ]:


X_pre_sequence = [X_train_pre_sequence, X_dev_pre_sequence, X_test_pre_sequence]
y_pre_sequence = [y_train_pre_sequence, y_dev_pre_sequence, y_test_pre_sequence]


# In[ ]:


# Validate X transform values
np.all([helpers.test_transform_values(pre_transform, transformed) for pre_transform, transformed in zip(X_pre_transform_list, X_pre_sequence)])


# In[ ]:


# Validate y transform values
np.all([helpers.test_transform_values(pre_transform, transformed) for pre_transform, transformed in zip(y_pre_transform_list, y_pre_sequence)])


# ## Create Data Sequence

# Define sequence size

# In[ ]:


sequence_length = 10
print('model will look at', sequence_length, 'trading days at a time')


# Create X sequence

# In[ ]:


X_train_sequence, X_dev_sequence, X_test_sequence = [np.array(list(helpers.gen_sequence_X(dataset, sequence_length))) for dataset in X_pre_sequence]


# In[ ]:


print('X_train_sequence.shape', X_train_sequence.shape)
print('X_dev_sequence.shape', X_dev_sequence.shape)
print('X_test_sequence.shape', X_test_sequence.shape)


# Shift y by 1 period backward and create y sequence

# In[ ]:


y_train_sequence = helpers.gen_sequence_y(y_train_pre_sequence, sequence_length)
y_train_sequence.shape


# In[ ]:


y_train_sequence, y_dev_sequence, y_test_sequence = [helpers.gen_sequence_y(dataset, sequence_length) for dataset in y_pre_sequence]


# In[ ]:


print('y_train_sequence.shape', y_train_sequence.shape)
print('y_dev_sequence.shape', y_dev_sequence.shape)
print('y_test_sequence.shape', y_test_sequence.shape)


# Validate X sequence values

# In[ ]:


X_sequence = [X_train_sequence, X_dev_sequence, X_test_sequence]


# In[ ]:


np.all([helpers.test_sequence_X_values(pre_sequence_X, sequence_X, 0) for pre_sequence_X, sequence_X in zip(X_pre_sequence, X_sequence)])


# ## Make Copies of Data

# In[ ]:


X_train, X_dev, X_test = X_train_sequence.copy(), X_dev_sequence.copy(), X_test_sequence.copy()


# In[ ]:


y_train, y_dev, y_test = y_train_sequence.copy(), y_dev_sequence.copy(), y_test_sequence.copy()


# ## Benchmark Model

# In[ ]:


X_train_bench, X_dev_bench, X_test_bench = (helpers.transform_bench_X(X_train), 
                                                       helpers.transform_bench_X(X_dev), 
                                                       helpers.transform_bench_X(X_test))


# In[ ]:


y_train_bench, y_dev_bench, y_test_bench = (helpers.transform_bench_y(y_train), 
                                                       helpers.transform_bench_y(y_dev), 
                                                       helpers.transform_bench_y(y_test))


# In[ ]:


print('X_train_bench.shape:', X_train_bench.shape)
print('y_train_bench.shape:', y_train_bench.shape)


# In[ ]:


from sklearn.linear_model import LinearRegression
linear_regression = LinearRegression()


# In[ ]:


linear_regression.fit(X_train_bench, y_train_bench)


# In[ ]:


y_pred_train_bench = linear_regression.predict(X_train_bench)
y_pred_dev_bench = linear_regression.predict(X_dev_bench)
y_pred_test_bench = linear_regression.predict(X_test_bench)


# In[ ]:


# X_pre_transform_list = [X_train_pre_transform, X_dev_pre_transform, X_test_pre_transform]
# y_pre_transform_list = [y_train_pre_transform, y_dev_pre_transform, y_test_pre_transform]


# In[ ]:


y_pred_train_bench = helpers.inverse_transform_StandardScaler(y_train_pre_transform.to_numpy(), y_pred_train_bench)
y_pred_dev_bench = helpers.inverse_transform_StandardScaler(y_dev_pre_transform.to_numpy(), y_pred_dev_bench)
y_pred_test_bench = helpers.inverse_transform_StandardScaler(y_test_pre_transform.to_numpy(), y_pred_test_bench)


# In[ ]:


r2_train_bench = r2_score(y_train, y_pred_train_bench) 
r2_dev_bench  = r2_score(y_dev, y_pred_dev_bench) 
r2_test_bench = r2_score(y_test, y_pred_test_bench)
print('r2_train_bench:', r2_train_bench)
print('r2_dev_bench:', r2_dev_bench)
print('r2_test_bench:', r2_test_bench)


# In[ ]:


mse_train_bench = mean_squared_error(y_train, y_pred_train_bench)
mse_dev_bench = mean_squared_error(y_dev, y_pred_dev_bench)
mse_test_bench = mean_squared_error(y_test, y_pred_test_bench)
print('root mse_train_bench value:', np.sqrt(mse_train_bench))
print('root mse_dev_bench value:', np.sqrt(mse_dev_bench))
print('root mse_test_bench value:', np.sqrt(mse_test_bench))


# In[ ]:


print('root mse_train_bench percent:', (np.sqrt(mse_train_bench)/np.mean(y_train_pre_transform))*100)
print('root mse_dev_bench percent:', (np.sqrt(mse_dev_bench)/np.mean(y_dev_pre_transform))*100)
print('root mse_test_bench percent:', (np.sqrt(mse_test_bench)/np.mean(y_test_pre_transform))*100)


# ## LSTM

# In[ ]:


from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras import regularizers

num_features = X_train.shape[2]

model = Sequential()

model.add(LSTM(input_shape=(sequence_length, num_features), 
               units=256, return_sequences=True, 
               kernel_regularizer=regularizers.l2(0.01)))

model.add(Dropout(0.5))

model.add(LSTM(units=128, return_sequences=True, kernel_regularizer=regularizers.l2(0.01)))

model.add(Dropout(0.5))

model.add(LSTM(units=64, return_sequences=False, kernel_regularizer=regularizers.l2(0.01)))

model.add(Dropout(0.5))

model.add(Dense(1))

model.compile(loss='mae', optimizer='nadam', metrics=['mean_squared_error'])


# In[ ]:


history = model.fit(X_train, y_train, epochs=100, batch_size=64, validation_data=[X_dev, y_dev], verbose=0)


# In[ ]:


helpers.plot_result(history)


# ## Predict

# In[ ]:


y_pred_test_normalized = np.squeeze(model.predict(X_test))


# In[ ]:


y_test_actual = helpers.inverse_transform_StandardScaler(y_test_pre_transform.to_numpy(), y_test)
y_pred_test_actual = helpers.inverse_transform_StandardScaler(y_test_pre_transform.to_numpy(), y_pred_test_normalized)


# In[ ]:


print('LSTM RMSE train value:', np.sqrt(helpers.inverse_transform_StandardScaler(y_train_pre_transform.to_numpy(), history.history['mean_squared_error'])[-1]))
print('LSTM RMSE dev: value', np.sqrt(helpers.inverse_transform_StandardScaler(y_dev_pre_transform.to_numpy(), history.history['val_mean_squared_error'])[-1]))
print('LSTM RMSE test: value', np.sqrt(mean_squared_error(y_test_actual, y_pred_test_actual)))


# In[ ]:


LSTM_RMSE_value_train = np.sqrt(helpers.inverse_transform_StandardScaler(y_train_pre_transform.to_numpy(), history.history['mean_squared_error'])[-1])
LSTM_RMSE_value_dev = np.sqrt(helpers.inverse_transform_StandardScaler(y_dev_pre_transform.to_numpy(), history.history['val_mean_squared_error'])[-1])
LSTM_RMSE_value_test = np.sqrt(mean_squared_error(y_test_actual, y_pred_test_actual))
print('LSTM RMSE train percent:', LSTM_RMSE_value_train/(np.mean(y_train_pre_transform))*100)
print('LSTM RMSE dev: percent', LSTM_RMSE_value_dev/(np.mean(y_dev_pre_transform))*100)
print('LSTM RMSE test: percent', LSTM_RMSE_value_test/(np.mean(y_test_pre_transform))*100)


# In[ ]:


last_quarter_timestamp = df_full.index.to_list()[-90:]


# In[ ]:


plt.style.use(['seaborn'])
plt.figure(figsize=(15,7), dpi=300)
plt.plot(y_test_actual, label='Truth')
plt.legend(loc='upper left')
plt.plot(y_pred_test_actual, label='Prediction')
plt.legend(loc='upper left')
plt.title('Truth vs Prediction', color='black')
plt.ylabel('Price')
plt.xlabel('Time')
plt.xticks(ticks=np.arange(0, 90, 3), labels=last_quarter_timestamp[::3], rotation='vertical')
plt.show()


# ----

# In[ ]:




