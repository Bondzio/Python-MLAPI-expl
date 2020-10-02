#!/usr/bin/env python
# coding: utf-8

# # Importing Neccessary Libraries

# In[ ]:


import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D,MaxPool2D,Dense,Flatten,BatchNormalization,Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image


# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[ ]:


from sklearn.model_selection import train_test_split
from tqdm import tqdm


# # Reading the Dataset

# In[ ]:


df = pd.read_csv('../input/movie-classifier/Multi_Label_dataset/train.csv')


# In[ ]:


# Taking 30 percentage of the dataset for this project as using whole dataset crashes the memory threshold of kaggle kernels
df = df.head(2300)


# In[ ]:


df.head()


# # Converting the images into Numpy array to train the CNN

# In[ ]:


width = 350
height = 350
X = []
for i in tqdm(range(df.shape[0])):
  path = '../input/movie-classifier/Multi_Label_dataset/Images/'+df['Id'][i]+'.jpg'
  img = image.load_img(path,target_size=(width,height,3))
  img = image.img_to_array(img)
  img = img/255.0
  X.append(img)

X = np.array(X)


# In[ ]:


X.shape


# In[ ]:


y = df.drop(['Id','Genre'],axis=1)
y = y.to_numpy()
y.shape


# In[ ]:


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.1)


# # Preparing the model

# In[ ]:


model = Sequential()
model.add(Conv2D(16,kernel_size=(3,3),activation='relu',input_shape=X_train[0].shape))
model.add(BatchNormalization())
model.add(MaxPool2D(2,2))
model.add(Dropout(0.3))

model.add(Conv2D(32,kernel_size=(3,3),activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(2,2))
model.add(Dropout(0.3))


model.add(Conv2D(64,kernel_size=(3,3),activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(2,2))
model.add(Dropout(0.4))

model.add(Flatten())

model.add(Dense(128,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(25,activation='sigmoid'))


# In[ ]:


model.summary()


# In[ ]:


model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])


# In[ ]:


history = model.fit(X_train,y_train,epochs=5,validation_data=(X_test,y_test))


# In[ ]:


def plotLearningCurve(history,epochs):
  epochRange = range(1,epochs+1)
  plt.plot(epochRange,history.history['accuracy'])
  plt.plot(epochRange,history.history['val_accuracy'])
  plt.title('Model Accuracy')
  plt.xlabel('Epoch')
  plt.ylabel('Accuracy')
  plt.legend(['Train','Validation'],loc='best')
  plt.show()

  plt.plot(epochRange,history.history['loss'])
  plt.plot(epochRange,history.history['val_loss'])
  plt.title('Model Loss')
  plt.xlabel('Epoch')
  plt.ylabel('Loss')
  plt.legend(['Train','Validation'],loc='best')
  plt.show()


# In[ ]:


plotLearningCurve(history,5)


# # Applying the trained model to Predict the Genre of the input image

# In[ ]:


img = image.load_img('../input/movie-classifier/Multi_Label_dataset/Images/tt0088247.jpg',target_size=(width,height,3))
plt.imshow(img)
img = image.img_to_array(img)
img = img/255.0
img = img.reshape(1,width,height,3)
classes = df.columns[2:]
y_pred = model.predict(img)
top3=np.argsort(y_pred[0])[:-4:-1]
for i in range(3):
  print(classes[top3[i]])


# # As you can see from the above output Model predicted the "Drama", "Thriller" and "Action" genre of the film from the poster of the image.

# In[ ]:




