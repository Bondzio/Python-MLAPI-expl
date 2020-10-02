#!/usr/bin/env python
# coding: utf-8

# **Artificial Neural Network using Keras Demostrations**
#                                                        
#  This Kernal demostrate how we can use Keras to implement ANN.
#  **Problem Statement:** Predicting admission from important parameters. The end result is a model using with a student can predict the changes of his admission in the university

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
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns

# importing data
data = pd.read_csv('../input/Admission_Predict_Ver1.1.csv')


# Lets check the data by viewing a few records

# In[ ]:


data.columns = [c.replace(' ', '_') for c in data.columns]
data.columns = [c.replace('LOR_', 'LOR') for c in data.columns]
data.columns = [c.replace('Chance_of_Admit_', 'Chance_of_Admit') for c in data.columns]
data.columns = [c.replace('Chance_of_Admit', 'Admit') for c in data.columns]
data.head()


# Here 'Chance of Admit' tells us what are the changes of a student getting admitted  to university, so lets convert this column to 1 and 0

# In[ ]:


data.loc[data['Admit']>=0.5,['Admit']]=1
data.loc[data['Admit']<0.5,['Admit']]=0


# Feature scaling

# In[ ]:


data["GRE_Score"] = data["GRE_Score"]/data["GRE_Score"].max()
data["TOEFL_Score"] = data["TOEFL_Score"]/data["TOEFL_Score"].max()
data["University_Rating"] = data["University_Rating"]/data["University_Rating"].max()
data["SOP"] = data["SOP"]/data["SOP"].max()
data["LOR"] = data["LOR"]/data["LOR"].max()
data["CGPA"] = data["CGPA"]/data["CGPA"].max()


# In[ ]:


import keras

X=data[['GRE_Score','TOEFL_Score','University_Rating','SOP','LOR','CGPA','Research']]
# labels y are one-hot encoded, so it appears as two classes 
y = keras.utils.to_categorical(np.array(data["Admit"]))


# We now split our data in X training features and y labels

# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.7,random_state=100)


# Defining a model

# In[ ]:


from keras.models import Sequential
from keras.layers.core import Dense, Activation


model = Sequential()
model.add(Dense(128, input_dim=7))
model.add(Activation('sigmoid'))
model.add(Dense(32))
model.add(Activation('sigmoid'))
model.add(Dense(2))
model.add(Activation('sigmoid'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()


# Training the model

# In[ ]:


model.fit(X_train, y_train, epochs=1000, batch_size=100, verbose=0)


# Evaluating the model

# In[ ]:


score = model.evaluate(X_test, y_test)
print(score)

