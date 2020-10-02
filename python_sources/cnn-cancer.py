#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense


# In[ ]:


# Building the CNN
# Initialising the CNN
classifier = Sequential()


# In[ ]:


# Convolution
classifier.add(Conv2D(32, (3, 3), input_shape = (32, 32, 3), activation = 'relu'))


# In[ ]:


# Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))


# In[ ]:


# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))


# In[ ]:


# Flattening
classifier.add(Flatten())


# In[ ]:


# Full connection
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dense(units = 1, activation = 'sigmoid'))


# In[ ]:


# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


# In[ ]:


# Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('/kaggle/input/cancer/train/',
                                                 target_size = (32, 32),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

test_set = test_datagen.flow_from_directory('/kaggle/input/cancer/validation/',
                                            target_size = (32, 32),
                                            batch_size = 32,
                                            class_mode = 'binary')


# In[ ]:


classifier.fit_generator(training_set,
                         steps_per_epoch = 1000,
                         epochs = 10,
                         validation_data = test_set,
                         validation_steps = 5)


# In[ ]:


classifier.fit_generator(training_set,
                         steps_per_epoch = 8000,
                         epochs = 25,
                         validation_data = test_set,
                         validation_steps = 2000)


# In[ ]:


classifier.fit_generator(training_set,
                         steps_per_epoch = 2000,
                         epochs = 30,
                         validation_data = test_set,
                         validation_steps = 1000)


# In[ ]:


import numpy as np
from keras.preprocessing import image

img_width, img_height = 32, 32


# In[ ]:


img = image.load_img('/kaggle/input/cancer/test/c2 (10007).jpeg', target_size = (img_width, img_height))
img = image.img_to_array(img)
img = np.expand_dims(img, axis = 0)
classifier.predict(img)


# https://keras.io/getting-started/faq/#how-can-i-save-a-keras-model

# In[ ]:


weights = classifier.get_weights() # returns a numpy list of weights


# In[ ]:


classifier.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'


# In[ ]:


# saving the weights of a model, you can do so in HDF5 with the code below:

classifier.save_weights('my_model_weights.h5')


# In[ ]:


# saving the architecture of a model, and not its weights or its training configuration

# save as JSON
json_string = classifier.to_json()

# save as YAML
yaml_string = classifier.to_yaml()


# In[ ]:


import pickle

# Save to file in the current working directory
pkl_filename = "my_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(classifier, file)


# In[ ]:


from sklearn.externals import joblib

# Save to file in the current working directory
joblib_file = "joblib_model.pkl"
joblib.dump(classifier, joblib_file)

