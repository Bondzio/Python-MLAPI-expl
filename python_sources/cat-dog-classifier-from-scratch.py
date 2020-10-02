#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2                                         
import numpy as np                                  
import os                                          
from random import shuffle                          
from keras.models import Sequential                 
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten,Activation
from keras.optimizers import Adam
from keras.preprocessing import image              
import matplotlib.pyplot as plt                    
import warnings
warnings.filterwarnings('ignore')
import os
from tqdm import tqdm


# In[ ]:


TRAIN_DIR = '../input/cat-and-dog/training_set/training_set'
TEST_DIR = '../input/cat-and-dog/test_set/test_set'
IMG_SIZE = 150,150


# In[ ]:


image_names = []
data_labels = []
data_images = []


# In[ ]:


def  create_data(DIR):
     for folder in (os.listdir(DIR)):
            for file in tqdm(os.listdir(os.path.join(DIR,folder))):
                if file.endswith("jpg"):

    #                 image_names.append(os.path.join(TRAIN_DIR,folder,file))
                    data_labels.append(folder)
                    img = cv2.imread(os.path.join(DIR,folder,file))
                    im = cv2.resize(img,IMG_SIZE)
                    data_images.append(im)
                else:
                    continue


# In[ ]:


create_data(TRAIN_DIR)
create_data(TEST_DIR)


# In[ ]:


data = np.array(data_images)


# In[ ]:


from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils

from keras.utils import to_categorical


le = LabelEncoder()
label = le.fit_transform(data_labels)
print(label.shape)
encoded = to_categorical(label)
print(encoded.shape)


# In[ ]:


label[0]
encoded[0]


# In[ ]:


from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

X_train,X_val,y_train,y_val=train_test_split(data,encoded,test_size=0.20,random_state=42)



print("X_train shape",X_train.shape)
print("X_test shape",X_val.shape)
print("y_train shape",y_train.shape)
print("y_test shape",y_val.shape)


# In[ ]:


model = Sequential()

model.add(Conv2D( 32, (3,3), padding='Same', input_shape=(150,150,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))


model.add(Conv2D( 64, (3,3), padding='Same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))


model.add(Conv2D( 64, (3,3), padding='Same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))
          
model.add(Conv2D( 128, (3,3), padding='Same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D( 128, (3,3), padding='Same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))
          
model.add(Flatten())

model.add(Dense(128))          
model.add(Activation('relu'))    

model.add(Dense(32))          
model.add(Activation('relu'))
model.add(Dropout(0.5))


# model.add(Dense(1, activation='sigmoid'))
model.add(Dense(2, activation='softmax'))  
          
model.compile(optimizer=Adam(),loss='categorical_crossentropy',metrics=['accuracy'])

model.summary()


# In[ ]:


history = model.fit(X_train,y_train,validation_data=(X_val,y_val), batch_size=128, epochs=30, verbose=1)


# In[ ]:


import matplotlib.pyplot as plt

plt.xlabel('Epochs')
plt.ylabel('Accuracy')

plt.plot(history.history['val_accuracy'],label='val')
plt.plot(history.history['accuracy'],label='train')
plt.legend(('val_accuracy', 'train_accuracy'),
           shadow=True, loc=(0.01, 1), handlelength=1.5, fontsize=10)


# In[ ]:


plt.plot(history.history['val_loss'],label='val')
plt.plot(history.history['loss'],label='train')
plt.legend(('val_loss', 'train_loss'),
           shadow=True, loc=(0.01, 0.01), handlelength=1.5, fontsize=10)


# In[ ]:


# model.save('new_catdog_scratch.h5')


# In[ ]:


pred = model.predict_classes(X_val)


# In[ ]:


y_val=np.argmax(y_val,axis=1)


# you can play with accuracy by increasing epochs, changing batch size, add/removing layers in model. 

# In[ ]:


from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


cm = confusion_matrix(pred,y_val)

acc_sc = accuracy_score(pred,y_val)
print('accuracy_score:',acc_sc)
cm


# In[ ]:




