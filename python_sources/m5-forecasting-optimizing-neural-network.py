#!/usr/bin/env python
# coding: utf-8

# ## Optimizing the Neural Network
# This aim of this jupyter notebook is to build a simple Neural Network and optimize it, not to solve the uncertainty problem in the m5 forecasting dataset. Please don't try notebook for M5 forecasting competition. Learning source: **[Introduction to Deep Learning](https://learn.datacamp.com/courses/introduction-to-deep-learning-in-python) ** in Python from DataCamp
# 

# ![](https://imgur.com/0aY4rqr.png)

# ### Import necessary dataset & libraries

# In[ ]:


# Clear previous memories
from IPython import get_ipython
get_ipython().magic('reset -sf')

# Import necessary libraries
import pandas as pd

# Import the dataset
data_calendar = pd.read_csv('../input/m5-forecasting-uncertainty/calendar.csv')
data_sales_train_evaluation = pd.read_csv('../input/m5-forecasting-uncertainty/sales_train_evaluation.csv')
data_sales_train_validation = pd.read_csv('../input/m5-forecasting-uncertainty/sales_train_validation.csv')
data_sample_submission = pd.read_csv('../input/m5-forecasting-uncertainty/sample_submission.csv')
data_sell_prices = pd.read_csv('../input/m5-forecasting-uncertainty/sell_prices.csv')


# In[ ]:


# Shape of the datasets
print('data_calendar \nShape: ', data_calendar.shape,)
print('data_sales_train_evaluation \nShape: ', data_sales_train_evaluation.shape)
print('data_sales_train_validation \nShape: ', data_sales_train_validation.shape)
print('data_sample_submission \nShape: ', data_sample_submission.shape)
print('data_sell_prices \nShape: ', data_sell_prices.shape)


# In[ ]:


#print('data_calendar \nShape: ', data_calendar.shape, '\n', data_calendar.head())
#print('---------------\ndata_sales_train_evaluation \nShape: ', data_sales_train_evaluation.shape, '\n', data_sales_train_evaluation.head())
print('---------------\ndata_sales_train_validation \nShape: ', data_sales_train_validation.shape, '\n', data_sales_train_validation.head())
#print('---------------\ndata_sample_submission \nShape: ', data_sample_submission.shape, '\n', data_sample_submission.head())
#print('---------------\ndata_sell_prices \nShape: ', data_sell_prices.shape, '\n', data_sell_prices.head())


# In[ ]:


# print('---------------\ndata_sales_train_evaluation \nShape: ', data_sales_train_evaluation.shape, '\n', data_sales_train_evaluation.head())
# I know it almost does not make sense to build the following dataset, but I am doing it just to implement the NN I learnt from the "Intro to Deep Learning" course.
# I am just slicing last column as response & previous 10 columns as predictors
predictors = data_sales_train_evaluation.iloc[:,1936:1945]
predictors.head()
response = data_sales_train_evaluation.iloc[:,1946]


# ### Model Building - Neural Network

# Note: Recurrent Neural Network or Bayesian Neural Network would be more appropriate. But, I am going to implement a simple generic NN anyway.

# ### Specifying a Model

# In[ ]:


# Import necessary modules
import keras
from keras.layers import Dense
from keras.models import Sequential
# Save the number of columns in predictors: 
n_cols = predictors.shape[1]
# Set up the model: model
model = Sequential()
# Add the first layer
model.add(Dense(50, activation='relu', input_shape=(n_cols,)))
# Add the second layer
model.add(Dense(32, activation='relu', input_shape=(n_cols,)))
# Add the output layer
model.add(Dense(1, input_shape=(n_cols,)))


# ### Compile & Fit the model

# In[ ]:


# fitting a model 
# Applying backpropagation and gradient descent with your data to update the weights.
model.compile(optimizer='sgd', loss='mean_squared_error')
model.fit(predictors, response)
# Scale the data before fitting can ease optimization
model.summary()


# So, our MSE is 31.50 at first epoch. We may run 10 epoch to get a better performance! Lets optimize

# ### Optimizing the Neural Network

# In[ ]:


model_1_training = model.fit(predictors, response, epochs=30, validation_split=0.2, verbose=False)
model_1_training


# In[ ]:


# But technically we may not need 10 epoch or may be more epoch. Running extra epoch is definitely computationally costly. 
# Lets perform Early Stopping
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

# Compile the Model
model.compile(optimizer='sgd', loss='mean_squared_error')
# Define early_stopping_monitor
early_stopping_monitor = EarlyStopping(patience=3)

# Fit model_2
model_2_training = model.fit(predictors, response, epochs=20, validation_split=0.3, callbacks=[early_stopping_monitor], verbose=False)

# Create the plot
plt.plot(model_1_training.history['val_loss'], 'r', model_2_training.history['val_loss'], 'b')
plt.xlabel('Epochs')
plt.ylabel('Validation score')
plt.show()


# ### Using models
# * Save
# * Reload
# * Make prediction

# In[ ]:


from keras.models import load_model
model.save('model_file_M5.h5')
nn_model = load_model('model_file_M5.h5')
# predictions = nn_model.predict(data_to_predict_with)

