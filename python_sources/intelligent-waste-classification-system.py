#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from PIL import Image
import numpy as np


# In[ ]:


Image.open('/kaggle/input/waste-classification-data/dataset/DATASET/TEST/O/O_13001.jpg')


# In[ ]:


Image.open('/kaggle/input/waste-classification-data/dataset/DATASET/TEST/R/R_10005.jpg')


# In[ ]:


# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3),
                      activation = 'relu'))

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
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy',
                   metrics = ['accuracy'])


# In[ ]:


train_datagen = ImageDataGenerator(rescale = 1./255)
test_datagen = ImageDataGenerator(rescale = 1./255)


# In[ ]:


training_set = train_datagen.flow_from_directory('/kaggle/input/waste-classification-data/dataset/DATASET/TRAIN',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

test_set = test_datagen.flow_from_directory('/kaggle/input/waste-classification-data/dataset/DATASET/TEST',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')


# In[ ]:


classifier.fit_generator(training_set,
                         steps_per_epoch = 706,
                         epochs = 4,
                         validation_data = test_set,
                         validation_steps = 2000)


# In[ ]:


# organic image
test_image = image.load_img('/kaggle/input/waste-classification-data/dataset/DATASET/TEST/O/O_13209.jpg',
                            target_size = (64, 64))


# In[ ]:


test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)


# In[ ]:


training_set.class_indices


# In[ ]:


if result[0][0] == 1:
    prediction = 'Recyclable'
else:
    prediction = 'Organic'


# In[ ]:


prediction

