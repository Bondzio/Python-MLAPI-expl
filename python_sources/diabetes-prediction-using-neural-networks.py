#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import sklearn
import matplotlib
import keras
import sys
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import seaborn as sns


# # 1.Importing the Dataset

# In[ ]:


# read the csv
df = pd.read_csv('/kaggle/input/diabetes-pimaindiansdiabetesdatabase/diabetes.csv')


# In[ ]:


df.head()


# In[ ]:


df.info()


# In[ ]:


# print the shape of the DataFrame, so we can see how many examples we have
print( 'Shape of DataFrame: {}'.format(df.shape))
print (df.loc[1])


# In[ ]:


# print the last twenty or so data points
df.loc[748:]


# In[ ]:


# remove missing data (indicated with a "?")
data = df[~df.isin(['?'])]
data.loc[1:]


# In[ ]:


# drop rows with NaN values from DataFrame
data = data.dropna(axis=0)
data.loc[1:]


# In[ ]:


# print the shape and data type of the dataframe
print(data.shape)
print(data.dtypes)


# **Transform data to numeric to enable further analysis**

# In[ ]:


# transform data to numeric to enable further analysis
data = data.apply(pd.to_numeric)
data.dtypes


# ** Data characteristics, usings pandas built-in describe() function**

# In[ ]:


# print data characteristics, usings pandas built-in describe() function
data.describe()


# ** Histograms for each variable**

# In[ ]:


# plot histograms for each variable
data.hist(figsize = (12, 12))
plt.show()


# In[ ]:


pd.crosstab(data.Age,data.Outcome).plot(kind="bar",figsize=(20,8))
plt.title('Diabetes Frequency for Ages')
plt.xlabel('Age',color='red',size=25)
plt.ylabel('Frequency',color='red',size=25)
plt.show()


# **Heatmap for each variable**

# In[ ]:


plt.figure(figsize=(10,10))
sns.heatmap(data.corr(),annot=True,fmt='.1f')
plt.show()


# **Age vs DiabetesPedigreeFunction**

# In[ ]:


age_unique=sorted(data.Age.unique())
age_DiabetesPedigreeFunction_values=data.groupby('Age')['DiabetesPedigreeFunction'].count().values
mean_DiabetesPedigreeFunction=[]
for i,Age in enumerate(age_unique):
    mean_DiabetesPedigreeFunction.append(sum(data[data['Age']==Age].DiabetesPedigreeFunction)/age_DiabetesPedigreeFunction_values[i])
    
plt.figure(figsize=(25,10))
sns.pointplot(x=age_unique,y=mean_DiabetesPedigreeFunction,color='red',alpha=0.9)
plt.xlabel('Age',fontsize = 25,color='black')

plt.ylabel('DiabetesPedigreeFunction',fontsize = 20,color='black')
plt.title('Age vs DiabetesPedigreeFunction',fontsize = 35,color='black')
plt.grid()
plt.show()


# # 2.Create Training and Testing Datasets

# **Now that we have preprocessed the data appropriately, we can split it into training and testings datasets. We will use Sklearn's train_test_split() function to generate a training dataset (80 percent of the total data) and testing dataset (20 percent of the total data).**
# 
# 

# In[ ]:


X = np.array(data.drop(['Outcome'],1))
y = np.array(data['Outcome'])


# In[ ]:


X[0]


# In[ ]:


mean = X.mean(axis=0)
X -= mean
std = X.std(axis=0)
X /= std


# In[ ]:


X[0]


# In[ ]:


# create X and Y datasets for training
from sklearn import model_selection

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, stratify=y, random_state=42, test_size = 0.75)


# In[ ]:


# convert the data to categorical labels
from keras.utils.np_utils import to_categorical

Y_train = to_categorical(y_train, num_classes=None)
Y_test = to_categorical(y_test, num_classes=None)
print (Y_train.shape)
print (Y_train[:768])


# In[ ]:


X_train[0]


# # 3.Building and Training the Neural Network

# **Now that we have our data fully processed and split into training and testing datasets, we can begin building a neural network to solve this classification problem. Using keras, we will define a simple neural network with one hidden layer. Since this is a categorical classification problem, we will use a softmax activation function in the final layer of our network and a categorical_crossentropy loss during our training phase.**

# In[ ]:


from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.layers import Dropout
from keras import regularizers

# define a function to build the keras model
def create_model():
    # create model
    model = Sequential()
    model.add(Dense(64, input_dim=8, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001), activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(64, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001), activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(2, activation='softmax'))
    
    # compile model
    adam = Adam(lr=0.001)
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model

model = create_model()

print(model.summary())


# In[ ]:


# fit the model to the training data
history=model.fit(X_train, Y_train, validation_data=(X_test, Y_test),epochs= 50,batch_size=10)


# **Model accuracy**

# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# Model accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'])
plt.show()


# **Model Losss**

# In[ ]:


# Model Losss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'])
plt.show()


# # 4.Improving Results - A Binary Classification Problem

# In[ ]:


# convert into binary classification problem - outcome
Y_train_binary = y_train.copy()
Y_test_binary = y_test.copy()

Y_train_binary[Y_train_binary > 0] = 1
Y_test_binary[Y_test_binary > 0] = 1

print(Y_train_binary[:768])


# In[ ]:


# define a new keras model for binary classification
def create_binary_model():
    # create model
    model = Sequential()
    model.add(Dense(80, input_dim=8, kernel_initializer='normal',  kernel_regularizer=regularizers.l2(0.001),activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(80, kernel_initializer='normal',  kernel_regularizer=regularizers.l2(0.001),activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(1, activation='sigmoid'))
    
    # Compile model
    adam = Adam(lr=0.001)
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model

binary_model = create_binary_model()

print(binary_model.summary())


# In[ ]:


# fit the binary model on the training data
history=binary_model.fit(X_train, Y_train_binary, validation_data=(X_test, Y_test_binary), epochs=50, batch_size=10)


# **Model accuracy**

# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# Model accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'])
plt.show()


# In[ ]:


# Model Losss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'])
plt.show()


# # 5.Results and Metrics

# In[ ]:


# generate classification report using predictions for categorical model
from sklearn.metrics import classification_report, accuracy_score

categorical_pred = np.argmax(model.predict(X_test), axis=1)

print('Results for Categorical Model')
print(accuracy_score(y_test, categorical_pred))
print(classification_report(y_test, categorical_pred))


# In[ ]:


# generate classification report using predictions for binary model
from sklearn.metrics import classification_report, accuracy_score
# generate classification report using predictions for binary model 
binary_pred = np.round(binary_model.predict(X_test)).astype(int)

print('Results for Binary Model')
print(accuracy_score(Y_test_binary, binary_pred))
print(classification_report(Y_test_binary, binary_pred))

