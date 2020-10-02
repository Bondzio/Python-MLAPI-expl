#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import keras
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator

import os
print(os.listdir("../input"))


# # Data preparation
# Data is prepared in such maner:
# 1. The label is removed from training data, processed to categorical values and assigned to y.
# 2. Training data is reshaped into a numpy array with dimensions of 42000 (number of images), 28, 28 (height & width)
# 3. All of training data is divided by 255 so values fit between 0 and 1
# 4. Training data is multiplied to three dimensions so ResNet50 could work with it
# 5. Training data is split into train and val sets for training and validations respectively
# 6. A data augmentation generator is created for train data set

# In[ ]:


nbr_of_clases = 10
validation_percentage = 0.2
resnet_path = '../input/resnet50/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'

training_data = pd.read_csv('../input/digit-recognizer/train.csv')


# In[ ]:


def prepare_data_for_resnet50(data_to_transform):
    data = data_to_transform.copy().values
    data = data.reshape(-1, 28, 28) / 255
    data = X_rgb = np.stack([data, data, data], axis=-1)
    return data


# In[ ]:


y = training_data.pop('label').values
X = training_data

y = keras.utils.to_categorical(y, nbr_of_clases)
X_rgb = prepare_data_for_resnet50(X)

X_train, X_val, y_train, y_val = train_test_split(X_rgb, y, test_size=validation_percentage)


# # Model creation
# ResNet50 model is used for convolutional part of the network

# In[ ]:


from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.applications.resnet50 import ResNet50

model = Sequential()
model.add(ResNet50(include_top=False, pooling='avg', weights=resnet_path))

# model.add(Dense(256, activation='relu'))
# model.add(Dropout(0.25))
# model.add(Dense(124, activation='relu'))
model.add(Dropout(0.50))
model.add(Dense(nbr_of_clases, activation='softmax'))

# model.layers[0].trainable = False

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# # Training

# In[ ]:


def fit_model(model, epochs=1, train_test_split=0.0):
    model.fit(X_rgb, y, epochs=epochs, validation_split=train_test_split)
    
def get_fitted_data_generator(data):
    data_generator = ImageDataGenerator(rotation_range=10, width_shift_range=0.1,
                                   height_shift_range=0.1, zoom_range=0.1)
    data_generator.fit(data)
    return data_generator
    
def fit_model_generator(model, X_train, y_train, epochs=1, batch=32, validation_data=False, X_val=None, y_val=None):
    image_nbr = np.size(X_train, 0)
    training_data_generator = get_fitted_data_generator(X_train)
    
    if validation_data:
        return model.fit_generator(training_data_generator.flow(X_train, y_train, batch_size=batch), steps_per_epoch=(image_nbr//batch),
                        epochs=epochs, validation_data=(X_val, y_val), verbose=1)
    else:
        return model.fit_generator(training_data_generator.flow(X_train, y_train, batch_size=batch), steps_per_epoch=(image_nbr//batch),
                        epochs=epochs, verbose=1)


# In[ ]:


model_history = fit_model_generator(model, X_train, y_train, epochs=1, 
                                    validation_data=True, X_val=X_val, y_val=y_val)


# # Model accuracy analysis

# In[ ]:


def get_predictions(model, data):
    return np.array([np.argmax(prediction) for prediction in model.predict(data)])


# Check what are the most common numbers in training dataset

# In[ ]:


predicted = get_predictions(model, X_val)
pd.Series(predicted).value_counts()


# In[ ]:


pd.Series([np.argmax(i) for i in y_val]).value_counts()


# In[ ]:


show_images = 10

for i in range(show_images):
    plt.subplot(show_images // 5 + 1, 5, i + 1)
    plt.title(str(predicted[i]))
    plt.imshow(X_val[i, :, :, 1].reshape(28, 28))


# # Predictions
# 1. Firstly train the model with all of the data  
# 2. Then generate predictions for test data set  
# 3. Write predictions to an output file  

# In[ ]:


# Hyper params
final_epochs = 30


# In[ ]:


# Fit on all data
full_data_model = fit_model_generator(model, X_rgb, y, epochs=final_epochs, validation_data=False)


# In[ ]:


# Making predictions
testing_data = pd.read_csv('../input/digit-recognizer/test.csv')
testing_data = prepare_data_for_resnet50(testing_data)

final_predictions = get_predictions(model, testing_data)


# In[ ]:


# Output file generation
submission_filename = 'submission.csv'
answers = pd.DataFrame({'ImageId':range(1, final_predictions.size + 1),
                        'Label':final_predictions})
answers.to_csv(submission_filename, index=False)

