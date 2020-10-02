#!/usr/bin/env python
# coding: utf-8

# Loading Data and Modules

# In[102]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from tqdm import tqdm


from keras.layers import Input,Concatenate
from keras.models import Model, Sequential
from keras.layers.core import Dense, Dropout
from keras.layers.advanced_activations import LeakyReLU
from keras.datasets import mnist
from keras.optimizers import Adam
from keras import initializers
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split



# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[92]:


train=pd.read_csv("../input/X_train.csv")


# In[93]:


sub=pd.read_csv("../input/sample_submission.csv")


# In[94]:


y=pd.read_csv("../input/y_train.csv")


# In[95]:


y.head()


# Mergigng Train and Target Datasets

# In[96]:


train=train.merge(y,on='series_id',how='left')


# In[97]:


train.head()


# In[98]:


train['surface'].value_counts()


# Label encoding target variable

# In[100]:




target = train['surface']
n_labels = target.nunique()
labels_names = target.unique()
le = LabelEncoder()
target = le.fit_transform(target.values)
target = to_categorical(target)


# Train Test split

# In[103]:


features = ['orientation_X', 'orientation_Y', 'orientation_Z', 'orientation_W', 
            'angular_velocity_X', 'angular_velocity_Y', 'angular_velocity_Z', 
            'linear_acceleration_X', 'linear_acceleration_Y', 'linear_acceleration_Z']

X_train, X_val, Y_train, Y_val = train_test_split(train[features], target, test_size=0.2, random_state=0)
print('Train shape', X_train.shape)
print('Validation shape', X_val.shape)
display(X_train.head())


# Model 

# In[104]:


model = Sequential()
model.add(Dense(20, activation='relu', input_dim=10))
model.add(Dense(20, activation='relu'))
model.add(Dense(9, activation="softmax"))
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.summary()


# In[105]:


model.fit(X_train.values, Y_train, validation_data=(X_val.values, Y_val), verbose=2,epochs=7,batch_size=128)


# Predictions on Test 

# In[106]:


test=pd.read_csv("../input/X_test.csv")


# In[ ]:


test.head()


# In[107]:


Test=test[['orientation_X','orientation_Y','orientation_Z','orientation_W','angular_velocity_X','angular_velocity_Y','angular_velocity_Z','linear_acceleration_X','linear_acceleration_Y','linear_acceleration_Z']]


# In[108]:


y_pred=model.predict(Test)


# In[109]:


out=pd.DataFrame(y_pred)


# In[110]:


out1=out.idxmax(axis=1)


# In[111]:


out1.tail()


# In[112]:


out1.value_counts()


# Confusion Matrix

# In[115]:


from sklearn.metrics import confusion_matrix
import seaborn as sns

cnf_matrix = confusion_matrix(np.argmax(Y_train, axis=1), model.predict_classes(X_train))
cnf_matrix_norm = cnf_matrix.astype('float') / cnf_matrix.sum(axis=1)[:, np.newaxis]
df_cm = pd.DataFrame(cnf_matrix_norm, index=labels_names, columns=labels_names)

plt.figure(figsize=(20, 7))
ax = plt.axes()
ax.set_title('Train')
sns.heatmap(df_cm, annot=True, fmt='.2f', cmap="Blues", ax=ax)
plt.show()

cnf_matrix = confusion_matrix(np.argmax(Y_val, axis=1), model.predict_classes(X_val))
cnf_matrix_norm = cnf_matrix.astype('float') / cnf_matrix.sum(axis=1)[:, np.newaxis]
df_cm = pd.DataFrame(cnf_matrix_norm, index=labels_names, columns=labels_names)

plt.figure(figsize=(20, 7))
ax = plt.axes()
ax.set_title('Validation')
sns.heatmap(df_cm, annot=True, fmt='.2f', cmap="Blues", ax=ax)
plt.show()


# In[116]:


predictions = model.predict_classes(test[features].values)
test['surface'] = le.inverse_transform(predictions)
df = test[['series_id', 'surface']]
df = df.groupby('series_id', as_index=False).agg(lambda x:x.value_counts().index[0])
df.to_csv('submission.csv', index=False)
df.head(10)

