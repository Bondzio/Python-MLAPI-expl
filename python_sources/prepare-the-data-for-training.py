#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tensorflow as tf
import numpy as np 
import pandas as pd
import os
print(os.listdir("../input"))
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


train_df = pd.read_csv('../input/train.csv',usecols=[1,3,4,5,6])
train_df


# ## Very unreasonalble
# Why will the fee < 0 or why will the fee be 93963.36?
# Why will the latitude and longitude be zero?

# ## So let's drop the unreasonalble data

# In[ ]:


test_array, test_label = [], []
val_array, val_label = [], []
for i in range(len(train_df)):
    temp = train_df.iloc[i].tolist()
    choose = np.random.randint(0,5)  #if 0 then make the data into val set so about 80% of the data will be the train data
    if temp[0]>2.5 and temp[0]<=20.5 and temp.count(0)==0:
        if choose == 0:
            val_label.append(temp.pop(0))
            val_array.append(np.array(temp, dtype='float64'))
        else:
            test_label.append(temp.pop(0))
            test_array.append(np.array(temp, dtype='float64'))
test_array = np.array(test_array)
test_label = np.array(test_label, dtype='float64')
val_array = np.array(val_array)
val_label = np.array(val_label, dtype='float64')


# In[ ]:


np.save("test_data.npy", test_array)
np.save("test_label.npy", test_label)
np.save("val_data.npy", val_array)
np.save("val_label.npy", val_label)

