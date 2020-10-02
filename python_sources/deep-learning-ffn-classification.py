#!/usr/bin/env python
# coding: utf-8

# # Problem 1

# In[2]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.utils import to_categorical
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[5]:


dataset = pd.read_csv('../input/Sheet_1.csv')


# In[6]:


x_col = dataset.iloc[1:, 2] 
y_col = dataset.iloc[1:, 1] 


# In[7]:


num_classes = len(list(set(y_col)))
y_int_to_label = {idx:label for idx,label in enumerate(set(y_col))}
y_label_to_int = {label:idx for idx,label in enumerate(set(y_col))}
y_int = np.array([y_label_to_int[label] for label in y_col])
print(y_int)


# In[8]:


vectorizer = TfidfVectorizer()
x_vect = vectorizer.fit_transform(x_col)
y_vect = to_categorical(y_int)


# In[9]:


x_train, x_test, y_train, y_test = train_test_split(x_vect, y_vect, test_size=0.3)


# In[10]:


model = Sequential()
model.add(Dense(256, activation='tanh', input_dim=x_vect.shape[1]))
model.add(Dropout(0.4))
model.add(Dense(128, activation='tanh'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='tanh'))
model.add(Dropout(0.1))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()


# In[11]:


num_epochs=50
hist = model.fit(x_train, y_train, batch_size=10, epochs=num_epochs, verbose=2, validation_split=0.25)


# In[44]:


train_loss = hist.history['loss']
val_loss   = hist.history['val_loss']
train_acc  = hist.history['acc']
val_acc    = hist.history['val_acc']
xc         = range(num_epochs)
plt.figure()
plt.plot(xc, train_loss, color='red')
plt.plot(xc, val_loss, color='green')
plt.show()


# In[12]:


score = model.evaluate(x_test, y_test)
print('Accuracy ', score[1])


# # Problem 2

# In[13]:


dataset = pd.read_csv('../input/Sheet_2.csv', engine='python')


# In[14]:


x_col = dataset.iloc[1:, 2] 
y_col = dataset.iloc[1:, 1] 


# In[15]:


num_classes = len(list(set(y_col)))
y_int_to_label = {idx:label for idx,label in enumerate(set(y_col))}
y_label_to_int = {label:idx for idx,label in enumerate(set(y_col))}
y_int = np.array([y_label_to_int[label] for label in y_col])
print(y_int)


# In[16]:


vectorizer = TfidfVectorizer()
x_vect = vectorizer.fit_transform(x_col)
y_vect = to_categorical(y_int)


# In[17]:


x_train, x_test, y_train, y_test = train_test_split(x_vect, y_vect, test_size=0.3)


# In[18]:


model = Sequential()
model.add(Dense(256, activation='tanh', input_dim=x_vect.shape[1]))
model.add(Dropout(0.4))
model.add(Dense(128, activation='tanh'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='tanh'))
model.add(Dropout(0.1))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()


# In[19]:


num_epochs=50
hist = model.fit(x_train, y_train, batch_size=10, epochs=num_epochs, verbose=2, validation_split=0.25)


# In[20]:


train_loss = hist.history['loss']
val_loss   = hist.history['val_loss']
train_acc  = hist.history['acc']
val_acc    = hist.history['val_acc']
xc         = range(num_epochs)
plt.figure()
plt.plot(xc, train_loss, color='red')
plt.plot(xc, val_loss, color='green')
plt.show()


# In[21]:


score = model.evaluate(x_test, y_test)
print('Accuracy ', score[1])


# In[ ]:




