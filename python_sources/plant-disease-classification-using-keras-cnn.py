#!/usr/bin/env python
# coding: utf-8

# # Plant Disease Classification Using Keras CNN

# In[ ]:


get_ipython().system('pip install --user imblearn')


# In[ ]:


import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Dense, Flatten, Dropout, Activation, MaxPooling2D, BatchNormalization
from tensorflow.keras.models import Sequential
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.utils import compute_class_weight
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils import class_weight
from tensorflow.keras.callbacks import EarlyStopping
from imblearn.over_sampling import SMOTE 
from tensorflow.keras.callbacks import ReduceLROnPlateau


# In[ ]:


train_data = pd.read_csv("../input/plant-pathology-2020-fgvc7/train.csv", engine = 'python')


# In[ ]:


train_data.head()


# ## Basic EDA & Image Preprocessing

# In[ ]:


train_data.drop(columns=['image_id']).sum().plot.bar()
plt.xlabel("Classes")
plt.ylabel('Counts')


# In[ ]:


height = 1365
width = 2048
color_channels = 3
new_height = 224
new_width = 224


# In[ ]:


images = np.ndarray(shape=(len(train_data), new_height, new_width, color_channels), dtype=np.float32)


# In[ ]:


for i in range(len(train_data)):
    print("Image: " + str(i))
    image = tf.keras.preprocessing.image.load_img("../input/plant-pathology-2020-fgvc7/images/"+train_data['image_id'].iloc[i]+'.jpg')
    image = image.resize((new_width, new_height))
    image = tf.keras.preprocessing.image.img_to_array(image)
    print(image.shape)
    images[i] = image


# In[ ]:


def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip(images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.show()


# In[ ]:


plotImages(images[:5] / 255)


# In[ ]:


labels = train_data.drop(columns=['image_id'])


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(images, np.array(labels.values), test_size=0.20, random_state=42)


# ### Use SMOTE to obtain a balanced dataset

# In[ ]:


sm = SMOTE(random_state=42)


# In[ ]:


X_train, y_train = sm.fit_resample(X_train.reshape((-1, new_height * new_width * 3)), y_train)


# In[ ]:


X_train = X_train.reshape((-1, new_height, new_width, 3))


# ### Image Data Generator Augments images by rotating, changing lighting, etc.

# In[ ]:


train_datagen = ImageDataGenerator(
    rotation_range=45, width_shift_range=0.25,
    height_shift_range=0.25, shear_range=0.5, 
    zoom_range=0.25,horizontal_flip=True, vertical_flip=True, brightness_range=[0.5, 1.5],
    fill_mode="nearest", rescale=1./255)
train_datagen.fit(X_train)


# In[ ]:


test_datagen = ImageDataGenerator(
    rotation_range=45, width_shift_range=0.1,
    height_shift_range=0.1, shear_range=0.2, 
    zoom_range=0.2,horizontal_flip=True, vertical_flip=True, brightness_range=[0.5, 1.5],
    fill_mode="nearest", rescale=1./255)
test_datagen.fit(X_test)


# ### Define Model and Train

# In[ ]:


model = Sequential()
model.add(Conv2D(64, (3, 3), activation ='relu', padding = 'same', input_shape = images.shape[1:]))
model.add(BatchNormalization())
model.add(Conv2D(64, (3, 3), activation ='relu', padding = 'same'))
model.add(BatchNormalization())
model.add(MaxPooling2D((3, 3)))
model.add(Conv2D(128, (3, 3), activation ='relu', padding = 'same'))
model.add(BatchNormalization())
model.add(Conv2D(128, (3, 3), activation ='relu', padding = 'same'))
model.add(BatchNormalization())
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(256, (3, 3), activation ='relu', padding = 'same'))
model.add(BatchNormalization())
model.add(Conv2D(256, (3, 3), activation ='relu', padding = 'same'))
model.add(BatchNormalization())
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(512, (3, 3), activation ='relu', padding = 'same'))
model.add(BatchNormalization())
model.add(Conv2D(512, (3, 3), activation ='relu', padding = 'same'))
model.add(BatchNormalization())
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(512, activation = "relu"))
model.add(BatchNormalization())
model.add(Dense(4, activation = "softmax"))
model.summary()


# In[ ]:


model.compile(loss='categorical_crossentropy', 
              optimizer=tf.keras.optimizers.Adam(),
              metrics=['accuracy'])


# In[ ]:


LR_reduce=ReduceLROnPlateau(monitor='val_accuracy',
                            patience=5,
                            verbose=1)


# In[ ]:


ES_monitor=EarlyStopping(monitor='val_loss',
                          patience=10)


# In[ ]:


history = model.fit(train_datagen.flow(X_train, y_train, batch_size=32), 
                    steps_per_epoch=X_train.shape[0] // 32,
                    epochs=400, 
                    validation_data=test_datagen.flow(X_test, y_test, batch_size=32),
                    validation_steps=X_test.shape[0] // 32, callbacks=[ES_monitor,LR_reduce])


# In[ ]:


plt.figure()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Convolutional Network Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'validation'])
plt.show()


# ### Save Model and Classify Test Images

# In[ ]:


model.save('plant_disease_model.h5')


# In[ ]:


classifier = tf.keras.models.load_model('plant_disease_model.h5')


# In[ ]:


test_data = pd.read_csv("../input/plant-pathology-2020-fgvc7/test.csv")


# In[ ]:


test_data.head()


# In[ ]:


test_images = np.ndarray(shape=(len(train_data), new_height, new_width, color_channels), dtype=np.float32)


# In[ ]:


for i in range(len(test_data)):
    print("Image: " + str(i))
    image = tf.keras.preprocessing.image.load_img("../input/plant-pathology-2020-fgvc7/images/"+test_data['image_id'].iloc[i]+'.jpg')
    image = image.resize((new_width, new_height))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = image/255
    print(image.shape)
    test_images[i] = image


# In[ ]:


pred = classifier.predict(test_images)

res = pd.DataFrame()
res['image_id'] = test_data['image_id']
res['healthy'] = pred[:, 0]
res['multiple_diseases'] = pred[:, 1]
res['rust'] = pred[:, 2]
res['scab'] = pred[:, 3]
res.to_csv('submission.csv', index=False)
res.head(10)

