#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:


train_fname = '../input/digit-recognizer/train.csv'

df_train = pd.read_csv(train_fname)
df_train.head()


# In[ ]:


test_fname = '../input/digit-recognizer/test.csv'

df_test = pd.read_csv(test_fname)
df_test.head()


# In[ ]:


sample_fname = '../input/digit-recognizer/sample_submission.csv'

df_sample = pd.read_csv(sample_fname)
df_sample.head()


# # Pra-pemrosesan

# In[ ]:


y_train = df_train['label'].to_numpy()

del df_train['label']
X_train = df_train.to_numpy()

X_test = df_test.to_numpy()


# In[ ]:


y_train.shape, X_train.shape, X_test.shape


# In[ ]:


X_train = X_train.reshape((-1, 28, 28, 1))
X_test = X_test.reshape((-1, 28, 28, 1))


# In[ ]:


y_train.shape, X_train.shape, X_test.shape


# In[ ]:


X_train = X_train / 255
X_test = X_test / 255


# In[ ]:


from tensorflow.keras.utils import to_categorical

y_train = to_categorical(y_train)


# # Desain Arsitektur Deep Learning

# In[ ]:


from tensorflow.keras import layers
from tensorflow.keras import models

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))


# In[ ]:


model.summary()


# In[ ]:


model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))


# In[ ]:


model.summary()


# # Fase Training

# In[ ]:


model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])


# In[ ]:


model.fit(X_train, y_train, epochs=5, batch_size=64,
          validation_split=0.2);


# # Prediksi X_test

# In[ ]:


y_test = model.predict_classes(X_test)


# In[ ]:


y_test.shape


# In[ ]:


df_pred = pd.DataFrame({
    'ImageId': range(1, y_test.shape[0] + 1),
    'Label': y_test
})


# In[ ]:


df_pred.head()


# In[ ]:


df_pred.shape


# In[ ]:


df_pred.to_csv('submission.csv', index=False)

