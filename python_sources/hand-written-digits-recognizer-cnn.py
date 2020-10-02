#!/usr/bin/env python
# coding: utf-8

# In this notebook I used the following refrences :
# 
# 1. https://www.kaggle.com/yassineghouzam/introduction-to-cnn-keras-0-997-top-6
# 2. https://machinelearningmastery.com/handwritten-digit-recognition-using-convolutional-neural-networks-python-keras/
# 

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator

from keras import backend as K
K.set_image_dim_ordering('th')

from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
get_ipython().run_line_magic('matplotlib', 'inline')


# 1) Load the data:

# In[ ]:


# Load the data
train = pd.read_csv("../input/train.csv")
test = pd.read_csv("../input/test.csv")


# 2)  Divide the data to labels and features, split the training data to training and valiation data and explore it:

# In[ ]:


y_train = train["label"]
X_train = train.drop(labels = ["label"],axis = 1)

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

#split the data to train and validation data
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = 0.2, random_state=seed)

n_train = len(X_train)
n_train_y = len(y_train)
n_test = len(test)

counter_train = Counter(y_train)
counter_valid = Counter(y_val)

n_classes = len(counter_train.keys())

print("Number of training examples =", n_train)
print("Number of labels in training examples =", n_train_y)
print("Number of testing examples =", n_test)
print("Number of classes =", n_classes)


# In[ ]:


X_train.isnull().any().describe()


# In[ ]:


test.isnull().any().describe()


# 3) Visualize the frequency of the digits in the training data

# In[ ]:


frequency = sns.countplot(y_train)


# 4) Reshape the vecotres to fit into the model

# In[ ]:


X_train = X_train.values.reshape(-1,1,28,28).astype('float32')
X_val = X_val.values.reshape(-1,1,28,28).astype('float32')
test = test.values.reshape(-1,1,28,28).astype('float32')


# 4) Shaffle the data to avoid bais based on the order of the data and visualise the digits images: 

# In[ ]:


### Data exploration visualization
X_train, y_train = shuffle(X_train, y_train)

fig = plt.figure()
fig.suptitle('Example images of the German Traffic Signs', fontsize=18)

for i in range(50):
    image = X_train[i].squeeze()
    plt.axis("off")
    plt.subplot(5,10,i+1)
    plt.imshow(image,cmap='gray')


# 5) Preprocess the data : normalize it and one hot encode the lables:

# In[ ]:


# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_val = X_val / 255
test = test / 255
# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_val = np_utils.to_categorical(y_val)


# 6) Define the CNN model with keras:

# In[ ]:


# define the model
def model():
# create model
    model = Sequential()
    model.add(Conv2D(30, (5, 5), input_shape=(1, 28, 28), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(15, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(n_classes, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


# 7) Fit the data in the model and evaluate the accuracy using the validation data: 

# In[ ]:


# build the model
model = model()
# Fit the model

epochs=38
batch_size=200

# Fit the model
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size, verbose=0)

scores = model.evaluate(X_val, y_val, verbose=0)
print("CNN Error: %.2f%%" % (100-scores[1]*100))


# 8) Predict the results of the test data:

# In[ ]:


# predict results
results = model.predict(test)
# select the indix with the maximum probability
results = np.argmax(results,axis = 1)
results = pd.Series(results,name="Label")


# 9) Create a submission file:

# In[ ]:


submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),results],axis = 1)
submission.to_csv("digits.csv",index=False)

