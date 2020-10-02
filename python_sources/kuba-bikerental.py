#!/usr/bin/env python
# coding: utf-8

# # Libs import

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import rcParams
import math
import os
import tensorflow as tf
from sklearn.preprocessing import StandardScaler


# # File loading

# In[ ]:


# Loading
train = pd.read_csv('../input/bike-rental-prediction/train.csv', sep=r'\s*,\s*', header=0, encoding='ascii', engine='python')
test = pd.read_csv('../input/bike-rental-prediction/test.csv', sep=r'\s*,\s*', header=0, encoding='ascii', engine='python')
train_org = train.copy()
test_ids = test['instant']

# Cleaning
y_train = train.pop('cnt')

dropCols = ['instant']

train = train.drop(dropCols + ['casual', 'registered'], 1)
test = test.drop(dropCols, 1)


# # Data analysis

# ## Null data - check for empty cols

# In[ ]:


print(train.count())
print(test.count())

train_org['cnt'].max()


# ## Corellation matrix

# In[ ]:


plt.figure(figsize=(15, 10))
corr = train_org.corr()
sns.heatmap(corr, annot=True)


# Low corellation to the cnt:
# 
# 
# High corellation between columns:
# 
# *  Mnth and season - **0.83**
# *  Temp and atemp - **0.99**
# 
# Season and temp will be removed first (due to lower variance)
# 
# 
# 
# 

# ### Distribution

# In[ ]:


distCols = ['atemp', 'hum', 'windspeed']

cols = len(distCols)

plt.figure(2, figsize=(30, 10))
for idx, col in enumerate(distCols):
  plt.subplot(1, cols, idx+1)
  sns.countplot(x=col, data=train_org)
  plt.ylabel('{}'.format(col))


# ## Cnt vs Features

# In[ ]:


train_org[(train_org['holiday'] == 1) & (train_org['workingday'] == 0)]


# In[ ]:


noiseTrain = train.copy()
variances = noiseTrain.var()

cols = 4
rows = math.ceil(len(noiseTrain.columns)/4)

plt.figure(1, figsize=(30, 30))
for idx, col in enumerate(noiseTrain.columns):
  plt.subplot(rows, cols, idx+1)
  plt.plot(noiseTrain[col], y_train, 'o')
  plt.ylabel('Cnt')
  plt.xlabel('{}. Variance: {}'.format(col,variances[col]))

print(variances)


# ### Other thoughts

# Maybe year should be removed since there are only two possible values
# 
# Maybe workday should be removed - data from there should be attainable from weekday column
# 
# Atemp, humidity, windspeed - weathersit - maybe weathersit should be removed since it can be judged based on atemp, humidity, windspeed (or atemp, humidity and windspeed)
# 
# Humidity is very very noisy

# ### After first run

# Maybe year shouldn't be removed as we're removing some data
# 
# Maybe humidity should be removed - very noisy
# 
# Windspeed is weird
# 
# Weekday is not important as long as we got workingday and holiday columns
# 
# Group hours into different categories - morning, workingHours, evening?

# # Data preparation

# ## Missing windspeed filling

# In[ ]:


# Calc medians for each day
medians = train.groupby('dteday')['windspeed'].median()

# Create dataFrame for medians
cols = []

for day in train['dteday']:
  cols.append([day, medians[day]])

median_df = pd.DataFrame(cols, columns=['dteday', 'windspeed'])

# Combine dataFrames
fillZeros = lambda v1, v2: v2 if v1 == 0 else v1

train['windspeed'] = train['windspeed'].combine(median_df['windspeed'], fillZeros)


# ## Dropping cols

# In[ ]:


analysisColDrops = ['season', 'temp', 'dteday']

train = train.drop(analysisColDrops, 1)
test = test.drop(analysisColDrops, 1)

train.head()


# ## Month 1-12 -> 0-11

# In[ ]:


train['mnth'] = train['mnth'] - 1
train['mnth'].head()

test['mnth'] = test['mnth'] - 1
test['mnth'].head()


# ## Hour, month cycling

# In[ ]:


# Cycling for train data

train['hr_sin'] = np.sin(train.hr*(2.*np.pi/24))
train['hr_cos'] = np.cos(train.hr*(2.*np.pi/24))

train['mnth_sin'] = np.sin((train.mnth-1)*(2.*np.pi/12))
train['mnth_cos'] = np.cos((train.mnth-1)*(2.*np.pi/12))

train['weekday_sin'] = np.sin(train.weekday*(2.*np.pi/7))
train['weekday_cos'] = np.cos(train.weekday*(2.*np.pi/7))


# In[ ]:


# Cycling for test data

test['hr_sin'] = np.sin(test.hr*(2.*np.pi/24))
test['hr_cos'] = np.cos(test.hr*(2.*np.pi/24))

test['mnth_sin'] = np.sin((test.mnth-1)*(2.*np.pi/12))
test['mnth_cos'] = np.cos((test.mnth-1)*(2.*np.pi/12))

test['weekday_sin'] = np.sin(test.weekday*(2.*np.pi/7))
test['weekday_cos'] = np.cos(test.weekday*(2.*np.pi/7))


# ## One-hot encoding for weathersit
# 
# 

# In[ ]:


train = pd.get_dummies(train, columns=["weathersit"], prefix=["weather"])
test = pd.get_dummies(test, columns=["weathersit"], prefix=["weather"])


# # Polynomial features - tried, but apparently didn't save in the notebook

# # Data normalization

# In[ ]:


scaler = StandardScaler()

valueCols = ['atemp', 'hum', 'windspeed', 'hr_sin', 'hr_cos', 'mnth_sin', 'mnth_cos', 'weekday_sin', 'weekday_cos']

for col in valueCols:
  train[col] = train[col].astype('float64')
  train[col] = scaler.fit_transform(train[col].values.reshape(-1, 1))

for testCol in valueCols:
  test[testCol] = test[testCol].astype('float64')
  test[testCol] = scaler.fit_transform(test[testCol].values.reshape(-1, 1))

train.head()


# # Training

# ## Model setup for TensorFlow

# In[ ]:


mnth = tf.feature_column.categorical_column_with_identity("mnth", 12)
hr = tf.feature_column.categorical_column_with_identity("hr", 24)
holiday = tf.feature_column.categorical_column_with_identity("holiday", 2)
weekday = tf.feature_column.categorical_column_with_identity("weekday", 7)
workingday = tf.feature_column.categorical_column_with_identity("workingday", 2)
atemp = tf.feature_column.numeric_column("atemp")
hum = tf.feature_column.numeric_column("hum")
windspeed = tf.feature_column.numeric_column("windspeed")
year = tf.feature_column.categorical_column_with_vocabulary_list("year", [2011, 2012])
hr_sin = tf.feature_column.numeric_column("hr_sin")
hr_cos = tf.feature_column.numeric_column("hr_cos")
mnth_sin = tf.feature_column.numeric_column("mnth_sin")
mnth_cos = tf.feature_column.numeric_column("mnth_cos")
weekday_sin = tf.feature_column.numeric_column("weekday_sin")
weekday_cos = tf.feature_column.numeric_column("weekday_cos")
weather_1 = tf.feature_column.categorical_column_with_identity("weather_1", 2)
weather_2 = tf.feature_column.categorical_column_with_identity("weather_2", 2)
weather_3 = tf.feature_column.categorical_column_with_identity("weather_3", 2)
weather_4 = tf.feature_column.categorical_column_with_identity("weather_4", 2)

feature_cols = [mnth, hr, holiday, weekday, workingday, atemp, hum, windspeed, year, hr_sin, hr_cos, mnth_sin, mnth_cos, weekday_sin, weekday_cos, weather_1, weather_2, weather_3, weather_4]

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x=train, y=y_train, batch_size=100, num_epochs=None, shuffle=True)


# ### Classifier

# In[ ]:


model = tf.estimator.LinearClassifier(feature_columns = feature_cols, n_classes=1000)


# ### Regressor

# In[ ]:


model = tf.estimator.LinearRegressor(feature_columns = feature_cols)


# ## Training

# In[ ]:


model.train(input_fn=input_func, max_steps=10000)


# ## Predictions

# ### Preds Classifier

# In[ ]:


pred_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x=test, y=None, batch_size=len(test), shuffle=False)

predictions = list(model.predict(input_fn=pred_func))
preds = []
for entry in predictions:
  preds.append(entry['class_ids'][0])


# ### Preds Regressor

# In[ ]:


pred_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x=test, y=None, batch_size=len(test), shuffle=False)

predictions = list(model.predict(input_fn=pred_func))
preds = []
for entry in predictions:
  preds.append(entry['predictions'][0] if entry['predictions'][0] else 0)

preds


# In[ ]:


#from google.colab import files

data = [test_ids, pd.Series(preds, dtype=object)]
headers = ["instant", "cnt"]
resultsDf = pd.concat(data, axis=1, keys=headers)

resultsDf.to_csv('results.csv', index=False)
#files.download('results.csv')

