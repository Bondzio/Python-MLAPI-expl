#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
import math
import seaborn as sns
import cv2
import os
import matplotlib.pyplot as plt
from keras import optimizers, Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.utils import to_categorical
from tqdm import tqdm
import cv2
from sklearn.model_selection import train_test_split
get_ipython().run_line_magic('matplotlib', 'inline')
# Any results you write to the current directory are saved as output.


# In[ ]:


df_train = pd.read_csv('/kaggle/input/detect-emotions-of-your-favorite-toons/Dataset/Train.csv')


# In[ ]:


df_test = pd.read_csv('/kaggle/input/detect-emotions-of-your-favorite-toons/Dataset/Test.csv')


# In[ ]:


np.unique(df_train['Emotion'])


# In[ ]:


sns.countplot(df_train['Emotion'])


# In[ ]:


df_train['Emotion'].count()


# In[ ]:


df_test['Frame_ID'].count()


# In[ ]:


##Train Images
get_ipython().system('mkdir train_data')
count = 0
videoFile='/kaggle/input/detect-emotions-of-your-favorite-toons/Dataset/Train Tom and jerry.mp4'
cap = cv2.VideoCapture(videoFile)   # capturing the video from the given path
frameRate = cap.get(5) #frame rate
x=1
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        filename ="/kaggle/working/train_data/frame%d.jpg" % count;count+=1
        # frame=cv2.resize(frame,(32,32))
        cv2.imwrite(filename, frame)
cap.release()
print ("Done!")


# In[ ]:


## test images
get_ipython().system('mkdir test_data')
count = 0
videoFile='/kaggle/input/detect-emotions-of-your-favorite-toons/Dataset/Test Tom and Jerry.mp4'
cap = cv2.VideoCapture(videoFile)   # capturing the video from the given path
frameRate = cap.get(5) #frame rate
x=1
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        filename ="/kaggle/working/test_data/test%d.jpg" % count;count+=1
        frame=cv2.resize(frame,(32,32))
        cv2.imwrite(filename, frame)
cap.release()
print ("Done!")


# In[ ]:


from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()


# In[ ]:


df_train['Emotion'] = le.fit_transform(df_train['Emotion'])


# In[ ]:


np.unique(df_train['Emotion'])


# In[ ]:


(df_train.Emotion[df_train['Frame_ID']=='frame0.jpg'].values)[0]


# In[ ]:


data = []
pixel = 224
for i in tqdm(os.listdir('/kaggle/working/train_data')):
    path = '/kaggle/working/train_data/{}'.format(i)
    if '.jpg' in path:
        img = cv2.imread(path)
        img = img/255
        img = cv2.resize(img,(pixel,pixel))
        data.append(img)


# In[ ]:


data = np.array(data)
data.shape


# In[ ]:


for i in tqdm(range(5)):
    np.random.shuffle(data)


# In[ ]:


Y=np.array(df_train['Emotion'])


# In[ ]:


Y=Y.reshape(-1,1)
Y.shape


# In[ ]:


Y = to_categorical(Y)


# In[ ]:


Y.shape


# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(data, Y, test_size = 0.2, random_state = 42)


# In[ ]:


print(X_train.shape,'\t',Y_train.shape)
print(X_test.shape,'\t',Y_test.shape)


# In[ ]:


model = Sequential()
model.add(Conv2D(32, kernel_size=5, activation='relu', input_shape=(pixel,pixel,X_train.shape[3])))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(32, kernel_size=4, activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(5, activation='softmax'))


# In[ ]:


model.compile(optimizer='RMSPROP', loss='categorical_crossentropy', metrics=['accuracy'])


# In[ ]:


history = model.fit(X_train, Y_train,validation_split = 0.25, epochs=15,verbose=1)


# In[ ]:


model.evaluate(X_test,Y_test)


# In[ ]:


plt.plot(history.history['accuracy'])
plt.plot(history.history['loss'])
plt.plot(history.history['val_accuracy'])
plt.plot(history.history['val_loss'])
plt.xlabel('Epochs')
plt.ylabel('Values for Accuracy and Loss')
plt.legend(['Training Accuracy','Training Loss','Validation Accuracy','Validation Loss'])


# In[ ]:


test=[]
pixel = 224
for i in tqdm(os.listdir('/kaggle/working/test_data')):
    path = '/kaggle/working/test_data/{}'.format(i)
    if '.jpg' in path:
        img = cv2.imread(path)
        img = img/255
        img = cv2.resize(img,(pixel,pixel))
        test.append(img)


# In[ ]:


test = np.array(test)


# In[ ]:


test.shape


# In[ ]:


pred = np.argmax(model.predict(test),axis=1)


# In[ ]:


prediction = le.inverse_transform(pred)


# In[ ]:


np.unique(prediction)


# In[ ]:


submission = pd.DataFrame({'Frame_ID':df_test['Frame_ID'],'Emotion':prediction})


# In[ ]:


submission.to_csv('result.csv',index=False)


# In[ ]:




