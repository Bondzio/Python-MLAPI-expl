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


import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split


# In[ ]:


# Data loading 

train=pd.read_csv('/kaggle/input/digit-recognizer/train.csv')
test_images=pd.read_csv('/kaggle/input/digit-recognizer/test.csv')

#Splitting the Training part into X_Train and Y_train

#X_Train Here we are dropping the label column, axis=1 will perform the action along column 
train_images=train.drop('label',axis=1)

#Y_Train
train_labels=train['label']

train_images.head()


# In[ ]:


# Checking for the missing values 

train_images.isnull().any().describe()


# In[ ]:


# Data Normalization by performing a grayscale normalization. Moreover the CNNs converge faster on [0..1] data

train_images=train_images/255.0
test_images=test_images/255.0


# In[ ]:


# We know that train images have been stocked as a 1D vector of 784 values. We have to reshape all the data to 28x28x1, i.e., 3D matrices 
# Reshape image in 3 dimensions (height = 28px, width = 28px , canal = 1 (as it is gray scale))

train_images=train_images.values.reshape(len(train_images),28,28,1)
test_images=test_images.values.reshape(len(test_images),28,28,1)

X_train, X_val, Y_train, Y_val = train_test_split(train_images, train_labels, test_size = 0.1, random_state=2)


# In[ ]:


# Using the matplot library to view the dataset

plt.imshow(train_images[78][:,:,0])


# Building Model
# 
# I will be using Keras for building CNN model and using hyperparameters with the help of Keras Tuner for optimization.
# Here is the Link to documentation of Keras Tuner on how to use Hyperparameters https://keras-team.github.io/keras-tuner/

# In[ ]:


import tensorflow as tf
from tensorflow import keras


# In[ ]:


def build_model(hp):
    model=keras.Sequential([
        keras.layers.Conv2D(
            filters=hp.Int('conv_1_filter', min_value=32, max_value=128, step=16),   # hp.Int will choose the value in range[min_value,max_value]
            kernel_size=hp.Choice('conv_1_kernel', values = [3,5,7]),                # hp.Choice will choose the best values from values
            activation='relu',
            input_shape=(28,28,1)                                                    # This is the shape of input image
        ),
         keras.layers.Conv2D(
            filters=hp.Int('conv_2_filter', min_value=32, max_value=128, step=16),
            kernel_size=hp.Choice('conv_2_kernel', values = [3,5,7]),
            activation='relu'
         ),
         keras.layers.Flatten(),
         keras.layers.Dense(
             units=hp.Int('dense_1_units', min_value=32, max_value=128, step=16),
             activation='relu'
             ),
        keras.layers.Dense(10, activation='softmax')     
        ])
    model.compile(optimizer=keras.optimizers.Adam(hp.Choice('learning_rate', values=[1e-2, 1e-3])),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
  
    return model


# Next, we will instantiate a tuner. You should specify the model-building function, the name of the objective to optimize (whether to minimize or maximize is automatically inferred for built-in metrics), the total number of trials (max_trials) to test, and the number of models that should be built and fit for each trial (executions_per_trial).
# 
# Available tuners are RandomSearch and Hyperband.  We will be using RandomSearch
# 
# Note: the purpose of having multiple executions per trial is to reduce results variance and therefore be able to more accurately assess the performance of a model. If you want to get results faster, you could set executions_per_trial=1 (single round of training for each model configuration).

# In[ ]:


from kerastuner import RandomSearch
from kerastuner.engine.hyperparameters import HyperParameters


# In[ ]:


tuner_search=RandomSearch(build_model,
                          max_trials=5,
                          objective='val_accuracy')


# Start the search for the best hyperparameter configuration. The call to search has the same signature as model.fit()
# 
# Here's what happens in search: models are built iteratively by calling the model-building function, which populates the hyperparameter space (search space) tracked by the hp object. The tuner progressively explores the space, recording metrics for each configuration.

# In[ ]:


# This step is really amazing it will display the accuracy for number of trials and the hyperparameters used for each trials.

tuner_search.search(train_images,train_labels,epochs=3,validation_split=0.1,verbose=2)


# In[ ]:


# When search is over, you can retrieve the best model(s):

model=tuner_search.get_best_models(num_models=1)[0]
model.summary()


# # Data Augmentation 
# 
# Data Augmentation is a method of artificially creating a new dataset for training from the existing training dataset to improve the performance of deep learning neural networks with the amount of data available. It is a form of regularization which makes our model generalize better than before.
# Here we have used a Keras ImageDataGenerator object to apply data augmentation for randomly translating, resizing, rotating, etc the images. Each new batch of our data is randomly adjusting according to the parameters supplied to ImageDataGenerator.
# 
# For the data augmentation, i choosed to :
# 1. Randomly rotate some training images by 10 degrees
# 2. Randomly Zoom by 10% some training images.
# 3. Randomly shift images horizontally by 10% of the width.
# 4. Randomly shift images vertically by 10% of the height
# 
# I did not apply a vertical_flip nor horizontal_flip since it could have lead to misclassify symetrical numbers such as 6 and 9.
# 
# * Before Data Augmentation- Accuracy 98.7
# * After Data Augmentation - Axxuracy 99.8

# In[ ]:


from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau

datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=10,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range = 0.1, # Randomly zoom image 
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=False,  # randomly flip images
        vertical_flip=False)  # randomly flip images


datagen.fit(train_images)


# In[ ]:


# Now our best model is prepared and we will fit our Augmented training Data

model.fit_generator(datagen.flow(train_images,train_labels, batch_size=80),
                              epochs = 5, validation_data = (X_val,Y_val),
                              verbose = 2
                              )


# In[ ]:


# Predidtions for the test_ images
test_pred = pd.DataFrame(model.predict(test_images, batch_size=200))
test_pred = pd.DataFrame(test_pred.idxmax(axis = 1))
test_pred.index.name = 'ImageId'
test_pred = test_pred.rename(columns = {0: 'Label'}).reset_index()
test_pred['ImageId'] = test_pred['ImageId'] + 1

test_pred.head()


# In[ ]:


#Converting to csv format
test_pred.to_csv('/kaggle/working/DR_submission.csv', index = False)

