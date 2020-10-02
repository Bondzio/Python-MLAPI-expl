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


data_dir = '../input/'
fname = os.path.join(data_dir,'jena_climate_2009_2016.csv')


# In[ ]:


f = open(fname)
data = f.read()
f.close


lines = data.split('\n')
header = lines[0].split(',')
lines = lines[1:]

print(header)
print(len(lines))
print(lines[0])


# In[ ]:


float_data = np.zeros((len(lines),len(header)-1))

for i, line in enumerate(lines):
    values = [float(x) for x in line.split(',')[1:]]
    float_data[i,:] = values

print(float_data.shape)


# In[ ]:


import matplotlib.pyplot as plt

temp = float_data[:,1]
plt.figure(figsize=(30,15))
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(range(len(temp)),temp)
plt.show()


# In[ ]:


plt.figure(figsize=(30,15))
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(range(1440),temp[:1440])
plt.show()


# In[ ]:


mean = float_data[:200000].mean(axis=0)
float_data -= mean
std = float_data[:200000].std(axis=0)
float_data /= std


# In[ ]:


def generator(data, lookback, delay, min_index, max_index,shuffle=False, batch_size=128, step=6):
    if max_index is None:
        max_index = len(data) - delay - 1
    
    i = min_index + lookback
    while True:
        if shuffle:
            rows = np.random.randint(min_index + lookback, max_index, size = batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + lookback
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)
        samples = np.zeros((len(rows),lookback//step,data.shape[1]))
            
        targets = np.zeros((len(rows),))
        #print('Rows:',rows[:3])
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            targets[j] = data[rows[j] + delay][1]
        yield samples, targets


# In[ ]:


lookback = 1440
step = 6
delay = 144
batch_size = 128

train_gen = generator(float_data,
                        lookback = lookback,
                        delay=delay,
                        min_index=0,
                        max_index=200000,
                        shuffle=True,
                        step=step,
                        batch_size=batch_size)

val_gen = generator(float_data,
                        lookback = lookback,
                        delay=delay,
                        min_index=200001,
                        max_index=300000,
                        shuffle=True,
                        step=step,
                        batch_size=batch_size)

val_gen = generator(float_data,
                        lookback = lookback,
                        delay=delay,
                        min_index=300001,
                        max_index=None,
                        shuffle=True,
                        step=step,
                        batch_size=batch_size)

val_steps = (300000-200001-lookback) // batch_size
test_stpes = (len(float_data)-300001-lookback) // batch_size


# In[ ]:


def evaluate_naive_method():
    batch_maes = []
    for step in range(val_steps):
        samples, targets = next(val_gen)
        #print(samples.shape)
        #print(targets.shape)
        preds = samples[:,-1,1]
        mae = np.mean(np.abs(preds - targets))
        batch_maes.append(mae)
    print(np.mean(batch_maes))
evaluate_naive_method()


# In[ ]:


celsius_mae = 0.3 * std[1]
celsius_mae


# # Dense

# In[ ]:


from keras.models import Sequential
from keras.layers import Flatten,Dense
from keras.optimizers import RMSprop

model = Sequential()
model.add(Flatten(input_shape=(lookback//step,float_data.shape[-1])))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))
model.compile(optimizer=RMSprop(),loss='mae')
model.summary()


# In[ ]:


history = model.fit_generator(train_gen,steps_per_epoch=500,epochs=20,validation_data=val_gen,validation_steps=val_steps)


# In[ ]:


import matplotlib.pyplot as plt
def show_all(history):
    def show(history,acc,val_acc,label):
        epochs = range(1, len(history.history[acc])+1)
        plt.plot(epochs,history.history[acc],label='Training '+label)
        plt.plot(epochs,history.history[val_acc],label='Validation '+label)
        plt.legend()
        
    plt.figure(figsize=(15,5))
    
    #plt.subplot(121)
    #show(history,'acc','val_acc','acc')
    #plt.subplot(122)
    show(history,'loss','val_loss','loss')
show_all(history)


# # GRU

# In[ ]:


from keras.layers import GRU

model_2 = Sequential()
model_2.add(GRU(32,input_shape=(None,float_data.shape[-1])))
model_2.add(Dense(1))
model_2.compile(optimizer=RMSprop(),loss='mae')
history_2 = model_2.fit_generator(train_gen,steps_per_epoch=500,epochs=20,validation_data=val_gen,validation_steps=val_steps)
show_all(history_2)


# In[ ]:


'''model_3 = Sequential()
model_3.add(GRU(32,dropout=0.1,recurrent_dropout=0.5,return_sequences=True,input_shape=(None, float_data.shape[-1])))
model_3.add(GRU(64,activation='relu',dropout=0.1,recurrent_dropout=0.5))
model_3.add(Dense(1))
model_3.compile(optimizer=RMSprop(),loss='mae')
history_3 = model_3.fit_generator(train_gen,steps_per_epoch=500,epochs=40,validation_data=val_gen,validation_steps=val_steps)
show_all(history_3)'''


# In[ ]:




