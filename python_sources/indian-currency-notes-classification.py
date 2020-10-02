#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import the libraries as shown below

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Conv2D

import numpy as np
from glob import glob


# In[ ]:


# re-size all the images to this
IMAGE_SIZE = [224, 224]

train_path = '../input/indian-currency-notes-classifier/Train'
valid_path = '../input/indian-currency-notes-classifier/Test'


# In[ ]:


# useful for getting number of output classes
folders = glob('../input/indian-currency-notes-classifier/Train/*')


# In[ ]:


folders


# In[ ]:


Classifier=Sequential()

Classifier.add(Conv2D(32,(3,3), input_shape=(224,224,3), activation='relu'))
Classifier.add(MaxPooling2D(pool_size=(2,2)))

Classifier.add(Conv2D(32,(3,3),activation='relu'))
Classifier.add(MaxPooling2D(pool_size=(2,2)))

Classifier.add(Flatten())

Classifier.add(Dense(units = 128, activation = 'relu'))
Classifier.add(Dense(units = 7, activation = 'softmax'))


# In[ ]:


# tell the model what cost and optimization method to use
Classifier.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)


# In[ ]:


# Use the Image Data Generator to import the images from the dataset
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   height_shift_range=0.2,
                                   featurewise_center=True,
                                   rotation_range=0.4,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255,)


# In[ ]:


# Make sure you provide the same target size as initialied for the image size
training_set = train_datagen.flow_from_directory('../input/indian-currency-notes-classifier/Train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')


# In[ ]:


test_set = test_datagen.flow_from_directory('../input/indian-currency-notes-classifier/Test',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')


# In[ ]:


# fit the model
from PIL import _imaging
from PIL import Image
import PIL
# Run the cell. It will take some time to execute
r = Classifier.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=50,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)


# In[ ]:


r.history


# In[ ]:


import matplotlib.pyplot as plt
# plot the loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# plot the accuracy
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')


# In[ ]:


# save it as a h5 file


from tensorflow.keras.models import load_model

Classifier.save('model_Classifier.h5')


# In[ ]:


y_pred = Classifier.predict(test_set)


# In[ ]:


y_pred


# In[ ]:


import numpy as np
y_pred = np.argmax(y_pred, axis=1)


# In[ ]:


y_pred


# In[ ]:


from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


# In[ ]:


model=load_model('model_Classifier.h5')


# In[ ]:


img=image.load_img('../input/indian-currency-notes-classifier/Test/1Hundrednote/1.jpg',target_size=(224,224))


# In[ ]:


img


# In[ ]:


test_image=image.img_to_array(img)
test_image=np.expand_dims(test_image, axis = 0)


# In[ ]:


result = Classifier.predict(test_image)
result


# In[ ]:


a=np.argmax(model.predict(test_image), axis=1)


# In[ ]:


a==5


# In[ ]:


a==0


# In[ ]:




