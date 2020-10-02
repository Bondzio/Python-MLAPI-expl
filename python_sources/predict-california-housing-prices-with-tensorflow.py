#!/usr/bin/env python
# coding: utf-8

# **Predict California Housing Prices with TensorFlow**

# *Step 1: Import Python Packages*

# In[ ]:


import numpy as np
import pandas as pd
import tensorflow as tf
import math
import shutil
from IPython.core import display as ICD


# *Step 2: Perform Basic Matrix Operations Using TensorFlow*

# In[ ]:


# Matrix addition with Numpy
a = np.array([4, 3, 6])
b = np.array([3, -1, 2])
c = np.add(a, b)
print(c)
# Matrix addition with TensorFlow
a = tf.constant([4, 3, 6])
b = tf.constant([3, -1, 2])
c = tf.add(a, b)
with tf.Session() as sess:
  result = sess.run(c)
  print(result)


# *Step 3: Load and Describe Data*

# In[ ]:


df = pd.read_csv("../input/housing.csv", sep=",")
print('Original Dataset:')
ICD.display(df.head(15))
a = pd.DataFrame(df.isnull().sum())
a['# of null values'] = a[0]
b = a[['# of null values']]
print('Before Dropping Null Values:')
print('# of Rows, Columns: ',df.shape)
ICD.display(b)
df = df.dropna(axis=0)
a = pd.DataFrame(df.isnull().sum())
a['# of null values'] = a[0]
b = a[['# of null values']]
print('After Dropping Null Values:')
print('# of Rows, Columns: ',df.shape)
ICD.display(b)


# In[ ]:


c = pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(17, 17), diagonal='hist')
c;


# *Step 4: Feature Engineering*

# In[ ]:


df['num_rooms'] = df['total_rooms'] / df['households']
df['num_bedrooms'] = df['total_bedrooms'] / df['households']
df['persons_per_house'] = df['population'] / df['households']
df.drop(['total_rooms', 'total_bedrooms', 'population', 'households'], axis = 1, inplace = True)

featcols = {
  colname : tf.feature_column.numeric_column(colname) \
    for colname in 'housing_median_age,median_income,num_rooms,num_bedrooms,persons_per_house'.split(',')
}
# Bucketize lat, lon so it's not so high-res; California is mostly N-S, so more lats than lons
featcols['longitude'] = tf.feature_column.bucketized_column(tf.feature_column.numeric_column('longitude'),
                                                   np.linspace(-124.3, -114.3, 5).tolist())
featcols['latitude'] = tf.feature_column.bucketized_column(tf.feature_column.numeric_column('latitude'),
                                                  np.linspace(32.5, 42, 10).tolist())

# Split into train and eval
msk = np.random.rand(len(df)) < 0.8
traindf = df[msk]
evaldf = df[~msk]

SCALE = 100000
BATCH_SIZE=100
train_input_fn = tf.estimator.inputs.pandas_input_fn(x = traindf[list(featcols.keys())],
                                                    y = traindf["median_house_value"] / SCALE,
                                                    num_epochs = 1,
                                                    batch_size = BATCH_SIZE,
                                                    shuffle = True)
eval_input_fn = tf.estimator.inputs.pandas_input_fn(x = evaldf[list(featcols.keys())],
                                                    y = evaldf["median_house_value"] / SCALE,  # note the scaling
                                                    num_epochs = 1, 
                                                    batch_size = len(evaldf), 
                                                    shuffle=False)
print('# of Rows, Columns: ',df.shape)
ICD.display(df.head(15))


# In[ ]:


c = pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(17, 17), diagonal='hist')
c;


# *Step 5: Evaluate Regressors Using a Reduced Feature Space*

# In[ ]:


def print_rmse(model, name, input_fn):
  metrics = model.evaluate(input_fn=input_fn, steps=1)
  print ('RMSE on {} dataset = {} USD'.format(name, np.sqrt(metrics['average_loss'])*SCALE))


# [LinearRegressor()](https://www.tensorflow.org/api_docs/python/tf/estimator/LinearRegressor) with only a single feature (num_rooms).

# In[ ]:


SCALE = 100000
train_fn = tf.estimator.inputs.pandas_input_fn(x = df[["num_rooms"]],
                                              y = df["median_house_value"] / SCALE,  # note the scaling
                                              num_epochs = 1,
                                              shuffle = True)

features = [tf.feature_column.numeric_column('num_rooms')]
outdir = './housing_trained'
shutil.rmtree(outdir, ignore_errors = True) # start fresh each time
myopt = tf.train.AdamOptimizer(learning_rate = 0.01)
model = tf.estimator.LinearRegressor(model_dir = outdir, feature_columns = features, optimizer = myopt)
model.train(input_fn = train_fn, steps = 300)
print_rmse(model, 'training', train_fn)


# [DNNRegressor()](https://www.tensorflow.org/api_docs/python/tf/estimator/DNNRegressor) with only a single feature (num_rooms).

# In[ ]:


SCALE = 100000
train_fn = tf.estimator.inputs.pandas_input_fn(x = df[["num_rooms"]],
                                              y = df["median_house_value"] / SCALE,  # note the scaling
                                              num_epochs = 1,
                                              shuffle = True)

features = [tf.feature_column.numeric_column('num_rooms')]
outdir = './housing_trained'
shutil.rmtree(outdir, ignore_errors = True) # start fresh each time
myopt = tf.train.AdamOptimizer(learning_rate = 0.03)
model = tf.estimator.DNNRegressor(model_dir = outdir,
                                hidden_units = [50, 50, 20],
                                feature_columns = features,
                                optimizer = myopt,
                                dropout = 0.05)
model.train(input_fn = train_fn, steps = 300)
print_rmse(model, 'training', train_fn)


# *Step 6: Evaluate Regressors Using the Full Feature Space*

# [LinearRegressor()](https://www.tensorflow.org/api_docs/python/tf/estimator/LinearRegressor) using the full feature space.

# In[ ]:


outdir = './housing_trained'
shutil.rmtree(outdir, ignore_errors = True) # start fresh each time
myopt = tf.train.AdamOptimizer(learning_rate = 0.01)
model = tf.estimator.LinearRegressor(model_dir = outdir, feature_columns = featcols.values(), optimizer = myopt)
#NSTEPS = (100 * len(traindf)) / BATCH_SIZE
NSTEPS = 3000
model.train(input_fn = train_input_fn, steps = NSTEPS)
print_rmse(model, 'eval', eval_input_fn)


# [DNNRegressor()](https://www.tensorflow.org/api_docs/python/tf/estimator/DNNRegressor) using the full feature space.

# In[ ]:


outdir = './housing_trained'
shutil.rmtree(outdir, ignore_errors = True) # start fresh each time
myopt = tf.train.AdamOptimizer(learning_rate = 0.01)
model = tf.estimator.DNNRegressor(model_dir = outdir,
                                hidden_units = [50, 50, 20],
                                feature_columns = featcols.values(),
                                optimizer = myopt,
                                dropout = 0.1)
#NSTEPS = (100 * len(traindf)) / BATCH_SIZE
NSTEPS = 3000
model.train(input_fn = train_input_fn, steps = NSTEPS)
print_rmse(model, 'eval', eval_input_fn)


# **Summary:
# **
# 
# In the end, we were able to predict California housing prices using a TensorFlow DNNRegressor and we saw an error (RMSE) of approximately $80,000.  In the future, I will optimize the model hyper-parameters and I will add additional evaluation metrics in order to make these predictions more accurate.

# Credit: Many of these functions are adaptations from the following tutorials ([Link #1](https://github.com/GoogleCloudPlatform/training-data-analyst/blob/master/courses/machine_learning/deepdive/03_tensorflow/a_tfstart.ipynb), [Link #2](https://github.com/GoogleCloudPlatform/training-data-analyst/blob/master/courses/machine_learning/deepdive/05_artandscience/a_handtuning.ipynb), [Link #3](https://github.com/GoogleCloudPlatform/training-data-analyst/blob/master/courses/machine_learning/deepdive/05_artandscience/c_neuralnetwork.ipynb)).
