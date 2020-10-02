#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load
+98999
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


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


train = pd.read_csv('../input/digit-recognizer/train.csv')
test = pd.read_csv('../input/digit-recognizer/test.csv')


# In[ ]:


train.head()


# In[ ]:


X = train.drop('label', axis = 1)
y = train['label']
del train


# In[ ]:


sns.countplot(y)


# # Visualizing the Data

# In[ ]:


some_value = X.values[27]
some_value = some_value.reshape(28,28)
sns.heatmap(some_value, cmap= 'binary', yticklabels=False, xticklabels= False)


# In[ ]:


display(y.values[27])


# # Normalization

# In[ ]:


np.unique(X.values)


# In[ ]:


X = X / 255.0
test = test / 255.0


# # Reshape the training and test images
# 
# Keras required images to be order 3 tensors. Thus, we require an additional dimension in our data. Apart from this, the images needs to go inside in batches and thus requires another dimension to specify that

# In[ ]:


X = X.values.reshape(-1,28,28,1)
test = test.values.reshape(-1,28,28,1)


# In[ ]:


#converting y into one hot encoding
labels = pd.get_dummies(y)
labels = labels.values


# # Training and Validation Set

# In[ ]:


from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(X, labels, test_size = 0.1,random_state=42)


# In[ ]:


display(X_train.shape)
display(y_train.shape)


# # Data Augmentation

# In[ ]:


from keras.preprocessing.image import ImageDataGenerator


# In[ ]:


datagen = ImageDataGenerator(shear_range= 0.2, zoom_range= 0.2)
datagen.fit(X_train)


# # Creating a CNN Model

# In[ ]:


#import the required libraries

from keras.layers import Dropout, Conv2D, MaxPool2D, Dense, Flatten
from keras.models import Sequential


# In[ ]:


model = Sequential()

#First Layer
#Convolutional Layers
model.add(Conv2D(filters = 64, kernel_size = 5,activation ='relu', input_shape = (28,28,1)))
model.add(Conv2D(filters = 64, kernel_size = 5,activation ='relu'))
#Pooling
model.add(MaxPool2D(pool_size=(2,2)))
#Dropout
model.add(Dropout(0.2))

#Second Layer
#Convolutional Layers
model.add(Conv2D(filters = 32, kernel_size = 3,activation ='relu'))
model.add(Conv2D(filters = 32, kernel_size = 3,activation ='relu'))
#Pooling
model.add(MaxPool2D(pool_size=(2,2)))
#Dropout
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(256, activation = "relu"))
model.add(Dropout(0.2))
model.add(Dense(10, activation = "softmax"))


# In[ ]:


#compile the model
model.compile(optimizer= 'adam', loss= 'categorical_crossentropy', metrics= ['accuracy'])


# # Fit the Model

# In[ ]:


performance = model.fit_generator(datagen.flow(X_train,y_train, batch_size=64), epochs = 30, 
                                  validation_data = (X_val,y_val), verbose = 3)


# In[ ]:


loss = pd.DataFrame(performance.history)
#plotting
fig, axes = plt.subplots(2,1, figsize = (10,12))
axes[0].plot(loss['loss'], "r", label = 'Training loss')
axes[0].plot(loss['val_loss'], "b", label = 'Validation loss')
legend = axes[0].legend()

axes[1].plot(loss['accuracy'], "r", label = 'Training Accuracy')
axes[1].plot(loss['val_accuracy'], "b", label = 'Validation Accuracy')
legend = axes[1].legend()


# In[ ]:


from sklearn.metrics import confusion_matrix, classification_report


# In[ ]:


#creating confusion matrix
pred = model.predict(X_val)


# In[ ]:


# Convert predictions classes to one hot vectors 
pred_classes = np.argmax(pred,axis = 1) 
# Convert validation observations to one hot vectors
y_true = np.argmax(y_val,axis = 1)


# In[ ]:


conf = confusion_matrix(y_true, pred_classes)
plt.figure(figsize= (10,8))
sns.heatmap(conf, annot= True)


# In[ ]:


print(classification_report(y_true, pred_classes))


# # Submissions

# In[ ]:


test_preds = model.predict(test)
test_preds = np.argmax(test_preds,axis = 1)
test_preds = pd.Series(test_preds,name="Label")


# In[ ]:


submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),test_preds],axis = 1)
submission.to_csv("cnn_mnist.csv",index=False)


# In[ ]:




