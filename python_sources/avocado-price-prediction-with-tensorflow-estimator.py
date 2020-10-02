#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ### Import libraries

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
# launch tensorboard to track model performance
get_ipython().run_line_magic('load_ext', 'tensorboard')
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
tf.__version__


# In[ ]:


MODEL_OUT_DIR = '/model' # model will be saved here
get_ipython().system('rm -rf ./models/ # remove previous model and summaries')
get_ipython().run_line_magic('tensorboard', '--logdir ./models/ # tensorbaord loads data from here')


# ### Load data using pandas

# In[ ]:


data = pd.read_csv('../input/avocado-prices/avocado.csv')
data.head()


# In[ ]:


# fix column names with spaces, to avoid issues in training. names in dataframe will be updated with corresponding names in columns list
columns = ["Unnamed","Date" ,"AveragePrice","Total_Volume","4046","4225","4770","Total_Bags","Small_Bags","Large_Bags","XLarge_Bags","type","year","region"]
data.columns = columns


# ### Train-Evaluation split

# In[ ]:


def get_random_split(data):
    msk = np.random.rand(len(data)) < 0.8
    return data[msk], data[~msk]
train_df, eval_df = get_random_split(data)


# ### Find out how various columns relate to AveragePrice

# #### average prices of different types

# In[ ]:


train_df.groupby('year').mean().plot(y='AveragePrice', kind='bar')


# #### average prices of different types

# In[ ]:


train_df.groupby('type').mean().plot(y='AveragePrice', kind='bar')


# #### Average prices per Region

# In[ ]:


train_df.groupby('region').mean().plot(y='AveragePrice', kind='bar')


# #### Price vs volume sold

# In[ ]:


train_df.plot.scatter(x='Total_Volume', y='AveragePrice')


# ### Create Feature Columns

# In[ ]:


DENSE_COLUMNS = [
    'Total_Volume',
    '4046',
    '4225',
    '4770',
    'Total_Bags',
    'Small_Bags',
    'Large_Bags',
    'XLarge_Bags'
]

SPARSE_COLUMNS = ['type', 'year', 'region']

feature_columns = []
for feature in DENSE_COLUMNS:
    feature_columns.append(tf.feature_column.numeric_column(feature))
for feature in SPARSE_COLUMNS:
    vocab = data[feature].unique()
    categorical_feature = tf.feature_column.categorical_column_with_vocabulary_list(feature, vocab)
    feature_columns.append(tf.feature_column.indicator_column(categorical_feature))


# ### Create dataset
# Estimator will use input_function to parse dataset. This is also the place to play any transformation required on dataset

# In[ ]:


def make_input_fn(df, epochs=500, shuffle=True, batch_size=32):
    df = df.copy()
    labels = df.pop('AveragePrice')
    def input_function():
        # create dataset from inmemory pandas dataframe        
        dataset = tf.data.Dataset.from_tensor_slices((dict(df), labels))
        if shuffle:
            dataset = dataset.shuffle(buffer_size=len(df))
        
        dataset = dataset.batch(batch_size).repeat(epochs)
        return dataset
    return input_function

train_input_fn = make_input_fn(train_df)
eval_input_fn = make_input_fn(eval_df, epochs=1, shuffle=False)


# ### Finally build an Estimator

# In[ ]:


linear_regressor = tf.estimator.LinearRegressor(
    feature_columns=feature_columns,
    model_dir='./models'
)
linear_regressor.train(train_input_fn)


# ### Try it on Evaluation Set

# In[ ]:


linear_regressor.evaluate(eval_input_fn)

