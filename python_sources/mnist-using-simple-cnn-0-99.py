#!/usr/bin/env python
# coding: utf-8

# # Digit Recognizer

# *upvote if find anything helpful*

# # 1) Data Collection

# In[ ]:


# these are usuful libs for modeling
from keras import models, layers
import numpy as np
from keras.utils import to_categorical
import pandas as pd
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dropout, BatchNormalization, Dense, Lambda
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


import os
os.chdir('../')    # current was '/kaggle/working' so we going to backward '/kaggle'
os.listdir('input')


# In[ ]:


# reading csvs files
train = pd.read_csv("input/digit-recognizer/train.csv")
test = pd.read_csv("input/digit-recognizer/test.csv")
submisssion = pd.read_csv("input/digit-recognizer/sample_submission.csv")


# # 2) Prepare Data for Training

# In[ ]:


# scalling the value in 0-1 , so /255. 
X = train.iloc[:,1:]/255.
y = train.iloc[:,0]
test = test/255.


# In[ ]:


# reshaping 784 to 28,28,1
X = X.values.reshape(train.shape[0],28,28,1)
test = test.values.reshape(test.shape[0],28,28,1)


# In[ ]:


# one hot of target values using keras's to_categorical class
y = to_categorical(y)

# splits train/test set 
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size =0.3,random_state=29)


# In[ ]:


Xtrain.shape, ytrain.shape, Xtest.shape, ytest.shape


# In[ ]:


# in model i am using BatchNormalization so for first step, i menualy normalize the batch
mean_px = Xtrain.mean().astype(np.float32)
std_px = Xtrain.std().astype(np.float32)

def standardize(x): 
    return (x-mean_px)/std_px


# # 3) Modeling and Training

# In[ ]:


# this is a model with dropouts layers
def cnn():
    model = models.Sequential()
    model.add(Lambda(standardize,input_shape=(28,28,1)))
    model.add(Convolution2D(32,(3,3), activation = 'relu'))
    model.add(BatchNormalization(axis=1))   
    model.add(Convolution2D(64,(3,3), activation = 'relu'))
    model.add(MaxPooling2D())
    model.add(Convolution2D(128,(3,3), activation = 'relu'))
    model.add(BatchNormalization(axis=1))
    model.add(Convolution2D(128,(2,2), activation = 'relu'))
    model.add(MaxPooling2D())
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(10, activation='softmax'))          
    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model          


# In[ ]:


classifier = cnn()
# traing the model with 20 epochs and 1000 batch size
classifier.fit(Xtrain, ytrain, epochs=20,batch_size=1000,validation_data=(Xtest,ytest))


# # 4) Prediction and Submission

# In[ ]:


#prediction of submission_test set
prediction = classifier.predict(test) 
predictions = np.argmax(prediction, axis=1)


# In[ ]:


# submission
submissions=pd.DataFrame({"ImageId": list(range(1,len(predictions)+1)),
                         "Label": predictions})
submissions.to_csv("working/simple_cnn_kaggle.csv", index=False, header=True)
submissions.shape


# ### Thank you , please upvote
