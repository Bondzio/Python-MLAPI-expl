#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # data Visualization
import seaborn as sns # data Visualization

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Importing the datasets
df_train = pd.read_csv('/kaggle/input/cat-in-the-dat-ii/train.csv')
df_test = pd.read_csv('/kaggle/input/cat-in-the-dat-ii/test.csv')
df_sub = pd.read_csv('/kaggle/input/cat-in-the-dat-ii/sample_submission.csv')


# Check the target variable

# In[ ]:


sns.countplot(x=df_train['target'], data=df_train)
plt.title("TARGET DISTRIBUTION", fontsize = 20)
plt.xlabel("Target Values", fontsize = 15)
plt.ylabel("Count", fontsize = 15)
plt.show()


# From above graph we note that target variable is not balanced

# In[ ]:


df_train.sort_index(inplace=True)
df_train.head()


# In[ ]:


y_train = df_train['target']
test_id = df_test['id']
df_train.drop(['target', 'id'], axis=1, inplace=True)
df_test.drop('id', axis=1, inplace=True)


# In[ ]:


cat_feat_to_encode = df_train.columns.tolist()
smoothing=0.20
import category_encoders as ce
oof = pd.DataFrame([])
from sklearn.model_selection import StratifiedKFold
for tr_idx, oof_idx in StratifiedKFold(n_splits=5, random_state= 1024, shuffle=True).split(df_train, y_train):
    ce_target_encoder = ce.TargetEncoder(cols = cat_feat_to_encode, smoothing=smoothing)
    ce_target_encoder.fit(df_train.iloc[tr_idx, :], y_train.iloc[tr_idx])
    oof = oof.append(ce_target_encoder.transform(df_train.iloc[oof_idx, :]), ignore_index=False)
ce_target_encoder = ce.TargetEncoder(cols = cat_feat_to_encode, smoothing=smoothing)
ce_target_encoder.fit(df_train, y_train)
df_train = oof.sort_index()
df_test = ce_target_encoder.transform(df_test)


# In[ ]:


#Lets take our matrics of features
x_train = df_train.iloc[:,:].values
x_test = df_test.iloc[:,:].values


# In[ ]:


from sklearn.utils import class_weight
cw = class_weight.compute_class_weight('balanced',np.unique(y_train),y_train)


# In[ ]:


#Import Keras model for NN
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping


# In[ ]:


# define model
classifier = Sequential()
classifier.add(Dense(units = 512, kernel_initializer = 'uniform', activation = 'relu', input_dim = 23))
classifier.add(Dense(units = 256, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(units = 128, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(units = 64, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))
classifier.compile(loss=keras.losses.binary_crossentropy,
              optimizer=keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False))


# In[ ]:


# Applying early stopping
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)


# In[ ]:


# Fitting the ANN to the Training set
classifier.fit(x_train, y_train, batch_size = 1000, epochs = 100, verbose=0,callbacks=[es], class_weight=cw)


# In[ ]:


#Predicting the Test set result
y_pred = classifier.predict_proba(x_test)[:,0]


# In[ ]:


#Sumbmission the result
df_sub = pd.DataFrame()
df_sub['id'] = test_id
df_sub['target'] = y_pred
df_sub.to_csv('submission.csv', index=False)


# In[ ]:


df_sub.head(20)


# In[ ]:




