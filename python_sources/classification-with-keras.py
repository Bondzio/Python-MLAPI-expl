#!/usr/bin/env python
# coding: utf-8

# In this experiment I will try to classify the breast cancer using a neuronal network. Any comment is appreciated.
# 
# Based in this great tutorial
# https://github.com/savarin/neural-networks 

# In[ ]:


#imports
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.models import Sequential
from keras.layers import Dense, Activation
from sklearn.cross_validation import  train_test_split
from matplotlib import pyplot
from sklearn import metrics
from sklearn.cross_validation import KFold, cross_val_score
from xgboost import XGBClassifier
from xgboost import plot_importance
from xgboost import plot_tree
from time import time
from sklearn.preprocessing import StandardScaler


# ## Loading the data and removing id and the weird Unnamed: 32 feature

# In[ ]:


dataset =  pd.read_csv('../input/data.csv', header=0)
dataset = dataset.drop("id",1)
dataset = dataset.drop("Unnamed: 32",1)
d = {'M' : 0, 'B' : 1}
dataset['diagnosis'] = dataset['diagnosis'].map(d)
features = list(dataset.columns[1:31])


# ## Let's find something against compete with...

# In[ ]:


XGBmodel = XGBClassifier()
X_train, X_test, y_train, y_test = train_test_split(dataset[features], dataset['diagnosis'].values, test_size=0.30, random_state=42)
XGBmodel.fit(X_train,y_train)
predictions = XGBmodel.predict(X_test)     

print ("accuracy" , metrics.accuracy_score(y_test, predictions))


# # Creating neuronal networks

# ## Let's create a neuronal network with 1 layer and test it

# In[ ]:


model = Sequential()
model.add(Dense(input_dim=30, output_dim=2))
model.add(Activation("softmax"))

model.compile(loss='sparse_categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])


# In[ ]:


scaler = StandardScaler()
model.fit(scaler.fit_transform(X_train.values), y_train)


# In[ ]:


y_prediction = model.predict_classes(scaler.transform(X_test.values))
print ("\n\naccuracy" , np.sum(y_prediction == y_test) / float(len(y_test)))


# ## Let's create a neuronal network with 3 layers and test it

# In[ ]:


model = Sequential()
model.add(Dense(input_dim=30, output_dim=30))
model.add(Dense(input_dim=30, output_dim=30))
model.add(Dense(input_dim=30, output_dim=2))
model.add(Activation("softmax"))

model.compile(loss='sparse_categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])


# In[ ]:


model.fit(scaler.fit_transform(X_train.values), y_train)


# In[ ]:


y_prediction = model.predict_classes(scaler.transform(X_test.values))
print ("\n\naccuracy" , np.sum(y_prediction == y_test) / float(len(y_test)))


# ### Conclusions
# NN seems very powerful and can reach XGB accuracy without too much effort.
# 
# Next step... playing with images
