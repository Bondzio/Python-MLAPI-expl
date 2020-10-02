#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


print(os.listdir())


# In[ ]:


print(os.getcwd())


# In[ ]:


os.chdir('../input/')


# In[ ]:


print(os.listdir())


# In[ ]:


data_dir = '.'
fname = os.path.join(data_dir, 'jena_climate_2009_2016.csv')

f = open(fname)
data = f.read()
f.close()

lines = data.split('\n')
header = lines[0].split(',')
lines = lines[1:]

print(header)
print(len(lines))


# ### Parsing the Data

# In[ ]:


float_data = np.zeros((len(lines), len(header) - 1))
for i, line in enumerate(lines):
    values = [float(x) for x in line.split(',')[1:]]
    float_data[i, :] = values


# ### Plotting the Temperature TimeSeries

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


temp = float_data[:, 1]
plt.plot(range(len(temp)), temp)


# ### Plotting the first 10 days of the temperature timeseries

# In[ ]:


plt.plot(range(1440), temp[:1440])


# ### Normalize the data

# In[ ]:


mean = float_data[:200000].mean(axis=0)
float_data -= mean
std = float_data[:200000].std(axis=0)
float_data /= std


#  ### Generator Yielding Time Series Samples and their Targets

# In[ ]:


float_data.shape


# In[ ]:


def generator(data, lookback, delay, min_index, max_index, shuffle=False, batch_size=128, step=6):
    if max_index is None:
        max_index = len(data) - delay - 1
    i = min_index + lookback
    while 1:
        if shuffle:
            rows = np.random.randint(
            min_index + lookback, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + lookback
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)
            
        samples = np.zeros((len(rows),
                           lookback // step,
                           data.shape[-1]))
        targets = np.zeros((len(rows)))
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            targets[j] = data[rows[j] + delay][1]
        yield samples, targets
    


# ### Preparing the training, validation and test generators

# In[ ]:


lookback = 1440
step = 6
delay = 144
batch_size = 128


# In[ ]:


train_gen = generator(float_data,
                     lookback = lookback,
                     delay = delay,
                     min_index = 0,
                     max_index = 200000,
                     shuffle=True,
                     step = step,
                     batch_size = batch_size)

val_gen = generator(float_data,
                   lookback = lookback,
                   delay = delay,
                   min_index = 200001,
                   max_index = 300000,
                   step = step,
                   batch_size=batch_size)

test_gen = generator(float_data,
                    lookback=lookback,
                    delay=delay,
                    min_index=300001,
                    max_index=None,
                    step = step,
                    batch_size = batch_size)


# In[ ]:


val_steps = (300000 - 200001 - lookback)
test_steps = (len(float_data) - 300001 - lookback)


# ### Computing the common-sense baseline MAE

# In[ ]:


def evaluation_naive_method():
    batch_maes = []
    for step in range(val_steps):
        samples, targets = next(val_gen)
        preds = samples[:, -1, 1]
        mae = np.mean(np.abs(preds - targets))
        batch_maes.append(mae)
    print(np.mean(batch_maes))
    
evaluation_naive_method()


# ### Converting the MAE back to a celcius error

# In[ ]:


celsius_mae = 0.29 * std[1]
print(celsius_mae)


# ### Training and evaluating a densely connected model

# In[ ]:


from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop

model = Sequential()
model.add(layers.Flatten(input_shape=(lookback // step, float_data.shape[-1])))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1))

model.compile(optimizer=RMSprop(), loss='mae')

history = model.fit_generator(train_gen,
                             steps_per_epoch=500,
                             epochs=20,
                             validation_data=val_gen,
                             validation_steps=val_steps)


# In[ ]:




