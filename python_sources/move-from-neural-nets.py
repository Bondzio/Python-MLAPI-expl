#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:


data_path = '/kaggle/input/chessgame-move-from-piece/CHESS_DATA.csv'
data = pd.read_csv(data_path)


# In[ ]:


alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
x_columns = list()
for i in range(1, 9):
    for j in range(1, 9):
        x_columns.append(f'{alphabet[j-1]}{i}')


# In[ ]:


from sklearn.preprocessing import LabelEncoder
input_encoder = LabelEncoder()
output_encoder = LabelEncoder()


# In[ ]:


for col in x_columns:
    data[col] = output_encoder.fit_transform(data[col])
X = data[x_columns]


# In[ ]:


X


# In[ ]:


X.info()


# In[ ]:


y = np.array(data['MOVE_FROM'])
y = output_encoder.fit_transform(y)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_valid, y_train, y_valid= train_test_split(X, y, test_size=0.20, random_state=1)


# In[ ]:


INPUT = X_valid.shape[1]
OUTPUT = 64


# In[ ]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization 
model = Sequential()
model.add(Dense(INPUT, input_shape=(INPUT,), activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(OUTPUT, activation='softmax'))
model.compile(loss = 'sparse_categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])


# In[ ]:


from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
earlystop = EarlyStopping(patience=10)
learning_rate_reduction = ReduceLROnPlateau(monitor='val_acuracy', 
                                            patience=2, 
                                            verbose=1, 
                                            factor=0.5, 
                                            min_lr=0.00001)
callbacks = [earlystop, learning_rate_reduction]


# In[ ]:


history = model.fit(X_train, y_train, epochs = 100, validation_data=(X_valid,y_valid))


# In[ ]:


import matplotlib.pylab as plt


# In[ ]:


plt.plot(history.epoch,history.history.get('accuracy'),label='accuracy')
plt.plot(history.epoch,history.history.get('val_accuracy'),label='val_accuracy')
plt.legend()


# In[ ]:


plt.plot(history.epoch,history.history.get('loss'),label='loss')
plt.plot(history.epoch,history.history.get('val_loss'),label='val_loss')
plt.legend()

