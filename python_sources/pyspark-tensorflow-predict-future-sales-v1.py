#!/usr/bin/env python
# coding: utf-8

# <div class="alert alert-block alert-info">
# 
# <b>Note:</b> This is a work in progress notebook!   
# 
# </div>
# 
# 
# 
# - Lot can be done in the feature engineering.
# - Also passing Spark dataframe to Tensorflow without converting it to pandas.

# In[ ]:


get_ipython().system(' pip install pyspark')


# In[ ]:


get_ipython().system(' pip install tensorflow==2.0.0-alpha0')


# In[ ]:


import tensorflow as tf
from tensorflow.keras import Sequential, Model

from pyspark.sql import SparkSession
from pyspark.sql import functions as f

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


tf.__version__


# In[ ]:



spark = SparkSession.builder.getOrCreate()
spark


# # Read Inputs

# In[ ]:


sdf_shops = spark.read.csv('/kaggle/input/competitive-data-science-predict-future-sales/shops.csv', inferSchema=True, header=True)
col_shops = ['shop_name', 'shop_id']

sdf_item_categories = spark.read.csv('/kaggle/input/competitive-data-science-predict-future-sales/item_categories.csv', inferSchema=True, header=True)
col_item_categories = ['item_category_name', 'item_category_id']

sdf_sales_train = spark.read.csv('/kaggle/input/competitive-data-science-predict-future-sales/sales_train.csv', inferSchema=True, header=True)
col_sales_train = ['date', 'date_block_num', 'shop_id', 'item_id', 'item_cnt_day']

sdf_items = spark.read.csv('/kaggle/input/competitive-data-science-predict-future-sales/items.csv', inferSchema=True, header=True)
col_items = ['item_name', 'item_id', 'item_category_id']

sdf_test = spark.read.csv('/kaggle/input/competitive-data-science-predict-future-sales/test.csv', inferSchema=True, header=True)
col_test = ['ID', 'shop_id', 'item_id']

sdf_sample_submission = spark.read.csv('/kaggle/input/competitive-data-science-predict-future-sales/sample_submission.csv', inferSchema=True, header=True)
col_sample_submission = ['ID', 'item_cnt_month']

# sdf_sample_submission.limit(5).toPandas().T


# In[ ]:


# sdf_sales_train.withColumn('date', f.from_unixtime(f.unix_timestamp(sdf_sales_train['date'],'%d.%m.%Y')))
# # sdf_sales_train.limit(10).toPandas().T
# sales_data = sdf_sales_train.toPandas()
# sales_data.dtypes


# # Negative Values ( Returns ) exclude or predict ?
# change all of them to 0!

# In[ ]:


from pyspark.sql import functions as f


# In[ ]:


sdf_sales_train= sdf_sales_train.withColumn('item_cnt_day', 
                           f.when(sdf_sales_train['item_cnt_day'] < 0,0)
                           .otherwise(sdf_sales_train['item_cnt_day']))


# In[ ]:


sdf_sales_train = sdf_sales_train.withColumn('item_price',
                                            f.when(sdf_sales_train['item_price'] < 0, 0)
                                            .otherwise(sdf_sales_train['item_price']))


# In[ ]:


sdf_sales_train.where((sdf_sales_train['item_cnt_day'] < 0) | 
                     (sdf_sales_train['item_price'] < 0)).count()


# # Type casting / data cleaning

# In[ ]:


sales_data = sdf_sales_train.toPandas()
sales_data['date'] = pd.to_datetime(sales_data['date'],format = '%d.%m.%Y')


# In[ ]:


sales_data.dtypes
# sales_data.T


# In[ ]:


dataset = sales_data.pivot_table(index = ['shop_id','item_id'],values = ['item_cnt_day'],columns = ['date_block_num'],fill_value = 0,aggfunc='sum')


# In[ ]:


dataset.reset_index(inplace = True)
dataset.head()


# In[ ]:


test_data = sdf_test.toPandas()


# In[ ]:


dataset = pd.merge(test_data,dataset,on = ['item_id','shop_id'],how = 'left')


# In[ ]:


dataset.fillna(0,inplace = True)
dataset.head()


# In[ ]:


dataset.drop(['shop_id','item_id','ID'],inplace = True, axis = 1)
dataset.head()


# # Train Test Split

# In[ ]:


# X we will keep all columns execpt the last one 
X_train = np.expand_dims(dataset.values[:,:-1],axis = 2)
# the last column is our label
y_train = dataset.values[:,-1:]

# for test we keep all the columns execpt the first one
X_test = np.expand_dims(dataset.values[:,1:],axis = 2)

# lets have a look on the shape 
print(X_train.shape,y_train.shape,X_test.shape)


# # TF Model building

# In[ ]:


model  = tf.keras.models.Sequential()
model.add(tf.keras.layers.LSTM(32,input_shape=X_train.shape[-2:]))
model.add(tf.keras.layers.Dropout(0.4))
model.add(tf.keras.layers.Dense(1,activation='relu'))
model.compile(optimizer=tf.keras.optimizers.RMSprop(), loss='mae')
# model.compile(loss = 'mse',optimizer = 'adam', metrics = ['mean_squared_error'])

model.summary()


# In[ ]:


tf.keras.utils.plot_model(model,show_layer_names=True,show_shapes=True)


# # Train the model

# In[ ]:


model.fit(X_train,y_train,batch_size = 4096,epochs = 10)


# # Use trained model for Prediction

# In[ ]:


# creating submission file 
submission_pfs = model.predict(X_test)
# creating dataframe with required columns 
submission = pd.DataFrame({'ID':test_data['ID'],'item_cnt_month':submission_pfs.ravel()})
# creating csv file from dataframe
submission.T


# In[ ]:


submission.to_csv('submission.csv',index = False)


# Source:
# - https://www.kaggle.com/karanjakhar/simple-and-easy-aprroach-using-lstm
