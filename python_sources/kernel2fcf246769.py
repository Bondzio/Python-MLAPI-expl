#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dense(units = 1, activation = 'sigmoid'))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('/kaggle/input/training', target_size = (64, 64), batch_size = 32, class_mode = 'binary')

test_set = test_datagen.flow_from_directory('/kaggle/input/test', target_size = (64, 64), batch_size = 32, class_mode = 'binary')

# classifier.fit_generator(training_set, steps_per_epoch = 500, epochs = 5, validation_data = test_set, validation_steps = 2000)


# In[ ]:





# In[ ]:


import pandas as pd
labels_foldered = pd.read_csv("../input/flood-images/labels-foldered.csv")


# In[ ]:


import pandas as pd
labels_foldered = pd.read_csv("../input/flood-images/labels-foldered.csv")

