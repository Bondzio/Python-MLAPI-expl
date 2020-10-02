#!/usr/bin/env python
# coding: utf-8

# # Hello Guys
# I'll simply put my code. For explanation, there are quite a lot of kernels you can refer to. Thanks a lot.

# In[ ]:


import csv
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from os import getcwd


# In[ ]:


import pandas as pd
df_train = pd.read_csv("../input/digit-recognizer/train.csv")
df_test = pd.read_csv("../input/digit-recognizer/test.csv")
df_train.head()


# In[ ]:


train_labels = df_train['label']
del df_train['label']
df_train.head()


# In[ ]:


train_set = df_train.values
train_set = train_set.reshape(42000,28,28)
test_set = df_test.values
test_set = test_set.reshape(28000,28,28)
print(train_set.shape, test_set.shape)


# In[ ]:


from sklearn.model_selection import train_test_split
random_seed = 7
training_set, validation_set, training_labels, validation_labels = train_test_split(train_set, train_labels, test_size = 0.10, random_state=random_seed)
print(len(validation_labels))


# In[ ]:


training_images = np.expand_dims(training_set, axis=-1)
testing_images = np.expand_dims(test_set, axis=-1)
validation_images = np.expand_dims(validation_set, axis=-1)


# Create an ImageDataGenerator and do Image Augmentation
train_datagen = ImageDataGenerator(rescale=1.0/255,
                                   rotation_range=10,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   zoom_range=0.1)

validation_datagen = ImageDataGenerator(rescale=1.0/255)
    
print(training_images.shape)
print(testing_images.shape)
print(validation_images.shape)


# In[ ]:


# Define the model
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import ReduceLROnPlateau
ankitz = ReduceLROnPlateau(monitor='val_accuracy', patience = 3, verbose=1,factor=0.5, min_lr=0.00001)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (5, 5), activation='relu', input_shape=(28, 28, 1),padding='same'),
    tf.keras.layers.Conv2D(32, (5, 5), activation='relu', padding='same'),
    tf.keras.layers.MaxPool2D(pool_size=(2, 2),strides=(2,2)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D(64, (5, 5), activation='relu', padding='same'),
    tf.keras.layers.Conv2D(64, (5, 5), activation='relu', padding='same'),
    tf.keras.layers.MaxPool2D(pool_size=(2, 2),strides=(2,2)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation=tf.nn.relu),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')])
model.summary()


# In[ ]:


# Compile Model. 
model.compile(optimizer=tf.optimizers.Adam(),
             loss='sparse_categorical_crossentropy',
             metrics=['accuracy'])

# Train the Model
history = model.fit_generator(train_datagen.flow(training_images, training_labels, batch_size=86),
                              epochs = 25,
                              steps_per_epoch=training_images.shape[0] // 86,
                              validation_data=validation_datagen.flow(validation_images, validation_labels),
                             callbacks = [ankitz])


# In[ ]:


predictions = model.predict_classes(testing_images)
predictions = pd.Series(predictions, name='Label')
predictions[:4]


# In[ ]:


submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),predictions],axis = 1)

submission.to_csv("my_results_final.csv",index=False)


# In[ ]:


# Plot the chart for accuracy and loss on both training and validation
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
acc = history.history['accuracy']
loss = history.history['loss']
val_acc = history.history['val_accuracy']
val_loss = history.history['val_loss']
epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training accuracy and Validation Accuracy')
plt.legend()
plt.figure()

plt.plot(epochs, loss, 'r', label='Training Loss')
plt.plot(epochs, val_loss, 'b', label='Training Loss')
plt.title('Training loss and Validation loss')
plt.legend()

plt.show()


# In[ ]:




