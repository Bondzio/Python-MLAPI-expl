#!/usr/bin/env python
# coding: utf-8

# # ** Breast cancer Prediction: Using Python - Keras ML**

# In this notebook you will find out breasy cancer prediction using python keras ML (backend TenserFlow) library.

# # ***Step 1: All libraries needed for this model***

# In[ ]:


from keras.models import Sequential #used for creating model
from keras.layers import Dense #used for creating layers
import numpy as np 
import pandas as pd

from sklearn.model_selection import train_test_split #used for split the data in to train and test
from sklearn.preprocessing import StandardScaler #used for the scal the data


# # Step 2: Load data set

# In[ ]:


data = pd.read_csv('../input/breast-cancer-wisconsin-data/data.csv') #load data from csv in to variable using pandas read_csv funcion


# In[ ]:


data.head() #take brief look in to fetched data


# # Step 3: Data Pre-processing(Prepare data for processing)

# In[ ]:


#differentiate input data and result data from dataset

##for input data take all the columns excluding ['ID', 'Diagnosis' , 'UNNAMED:32'] Columns 
input_Data = data.drop(columns=['id','diagnosis','Unnamed: 32']) 

##for result data take diagnosis column values as "0 for M('Malignant')" and "1 for B('Benign')"
result_Data = data['diagnosis'].map({'M':0,'B':1})


# In[ ]:


# here we does not have any Test-Set data & Training-Set data
# So we will differentiate teat & traing data from input and result data which we prepared
# that can be done by using sklearn library's model_selection module's function train_test_split()

train_data, test_data, train_label, test_label = train_test_split(input_Data, result_Data, test_size=0.30)


# In[ ]:


# Now scal the data in between 0 to 1 for prosessing
# using StandardScaler() module of sklearn.preprocessing

scaler = StandardScaler()
N_train_data = scaler.fit_transform(train_data) # this is normalized training data
N_test_data = scaler.fit_transform(test_data) # this is normalized testing data


# In[ ]:


# let find the input dim for creating Sequential models first layer 
input_dim = len(train_data.axes[1])


# # Step 4: Now Design Neural Network

# In[ ]:


# create model Sequential using Dense layers
model = Sequential([
    Dense(8, activation='relu', input_shape=(input_dim,)),
    Dense(32, activation='relu'),
    Dense(32, activation='relu'),
    Dense(32, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid'),
])


# In[ ]:


# Compile created model
# using optimizer as adam
# loss function as binary_crossentropy (because our output or prediction have only two values 0 & 1)

model.compile(
  optimizer='adam',
  loss='binary_crossentropy',
  metrics=['accuracy'],
)


# # Step 5: Now Train & Test Model

# In[ ]:


# Now fit the Training data set into over model
# define epochs 11
# and batch_size pro processing 32

model.fit(
  N_train_data,
  train_label,
  epochs=20,
  batch_size=32,
)


# In[ ]:


# Now evaluate over model using test data
model.evaluate(
  N_test_data,
  test_label
)


# # Step 6: Now save the current model weights

# In[ ]:


# save this model weights for further predictions
# you can use this saved weights of this model in other model using
# model.load_weights('Breast_Cancer_Possibilities')
model.save_weights('Breast_Cancer_Possibilities')


# In[ ]:


model.summary()

