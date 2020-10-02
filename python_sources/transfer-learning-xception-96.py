#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# del model
# del X_train,Y_train


# In[ ]:


import tensorflow as tf
from tensorflow import keras
from tensorflow import one_hot
from tensorflow.keras.applications import xception
from tensorflow.keras.preprocessing import image
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from IPython.display import clear_output
import gc


# In[ ]:


CATEGORIES = os.listdir("/kaggle/input/plant-seedlings-classification/train")
CATEGORIES


# In[ ]:



# initial_learning_rate = 0.003 #initial rate
# # Rate decay with exponential decay
# # new rate = initial_learning_rate * decay_rate ^ (step / decay_steps)
# #step per epoch = 95
# lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
#     initial_learning_rate,
#     decay_steps=480,
#     decay_rate=0.5,
#     staircase=False)


# In[ ]:


pretrained = xception.Xception(input_shape=[240,240, 3], include_top=False)


# In[ ]:


pretrained.trainable = False


# In[ ]:


model = tf.keras.Sequential([
    pretrained,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(100, activation="relu"),
    tf.keras.layers.BatchNormalization(trainable = True,axis=1),
    
    tf.keras.layers.Dropout(0.5),
    
    tf.keras.layers.Dense(50, activation="relu"),
    tf.keras.layers.BatchNormalization(trainable = True,axis=1),
    
    tf.keras.layers.Dense(12,activation='softmax')
])


# In[ ]:


model.summary()


# In[ ]:


model.compile(optimizer=tf.keras.optimizers.Nadam(learning_rate=0.001),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=['accuracy'])


# In[ ]:


train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    brightness_range=[0.4,1],
    rescale=1.0/255.0)

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0/255.0)
pathh = "/kaggle/input/plant-seedlings-classification/train/"


# In[ ]:


result = model.fit(train_datagen.flow_from_directory(pathh,
                                        target_size=(240, 240), 
                                        color_mode='rgb', 
                                        class_mode='categorical', 
                                        batch_size=64, 
                                        shuffle=True),
                    epochs=20,
                    verbose=1)


# In[ ]:


result.history.keys()


# In[ ]:


plt.plot(result.history['accuracy'], label='train')
# plt.plot(result.history['val_accuracy'], label='valid')
plt.legend(loc='upper left')
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.show()
plt.plot(result.history['loss'], label='train')
# plt.plot(result.history['val_loss'], label='test')
plt.legend(loc='upper right')
plt.title('Model Cost')
plt.ylabel('Cost')
plt.xlabel('Epoch')
plt.show()


# In[ ]:


pretrained.trainable = True
model.get_layer('xception').trainable


# In[ ]:


model.summary()


# In[ ]:


model.compile(optimizer=tf.keras.optimizers.Nadam(learning_rate=0.0006),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=['accuracy'])


# In[ ]:


result = model.fit(train_datagen.flow_from_directory(pathh,
                                        target_size=(240, 240), 
                                        color_mode='rgb', 
                                        class_mode='categorical', 
                                        batch_size=64, 
                                        shuffle=True),
                    epochs=40,
                    initial_epoch=20,
                    verbose=1)


# In[ ]:


plt.plot(result.history['accuracy'], label='train')
# plt.plot(result.history['val_accuracy'], label='valid')
plt.legend(loc='upper left')
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.show()
plt.plot(result.history['loss'], label='train')
# plt.plot(result.history['val_loss'], label='test')
plt.legend(loc='upper right')
plt.title('Model Cost')
plt.ylabel('Cost')
plt.xlabel('Epoch')
plt.show()


# In[ ]:


gc.collect()


# In[ ]:


model.compile(optimizer=tf.keras.optimizers.Nadam(learning_rate=0.000006),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=['accuracy'])


# In[ ]:


result = model.fit(train_datagen.flow_from_directory(pathh,
                                        target_size=(240, 240), 
                                        color_mode='rgb', 
                                        class_mode='categorical', 
                                        batch_size=64, 
                                        shuffle=True),
                    epochs=60,
                    initial_epoch=40,
                    verbose=1)


# In[ ]:


plt.plot(result.history['accuracy'], label='train')
plt.legend(loc='upper left')
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.show()
plt.plot(result.history['loss'], label='train')
# plt.plot(result.history['val_loss'], label='test')
plt.legend(loc='upper right')
plt.title('Model Cost')
plt.ylabel('Cost')
plt.xlabel('Epoch')
plt.show()


# In[ ]:


gc.collect()


# In[ ]:


valid = model.evaluate(test_datagen.flow_from_directory(pathh,
                                                        target_size=(240, 240), 
                                                        color_mode='rgb',
                                                        class_mode='categorical',))


# In[ ]:


a = test_datagen.flow_from_directory(pathh,
                                    target_size=(240, 240), 
                                    color_mode='rgb',
                                    class_mode='categorical',
                                    batch_size=1)


# In[ ]:


CATEGORIES = list(a.class_indices.keys())


# In[ ]:


CATEGORIES


# In[ ]:


R_categories = {y:x for x,y in a.class_indices.items()}
R_categories


# 140
# 0.0006
# 160
# 0.0001
# 180
# 0.00001

# In[ ]:


del valid
gc.collect()


# In[ ]:


X=[]
file = []
(IMG_S1, IMG_S2) = (240,240)
def createTestData():
    a=0
    pathh = "/kaggle/input/plant-seedlings-classification/"
    types = ["test"]
    for typ in types:
        PATH = os.path.join(pathh,typ)
        for img in os.listdir(PATH):
            file.append(img)
            image = os.path.join(PATH, img)
            image = cv2.imread(image, cv2.IMREAD_ANYCOLOR)
            image = cv2.resize(image , (IMG_S1, IMG_S2))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            X.append(image)
            a+=1
    print(a)

createTestData()
X = np.array(X)/255.0 #normalize the data 


# In[ ]:


species = model.predict_classes(X)


# In[ ]:


ans = pd.DataFrame(file,columns = ["file"])

ans = ans.join(pd.DataFrame(species,columns=["species"]))
ans["species"] = ans["species"].apply(lambda x: CATEGORIES[int(x)])
ans.head(20)


# In[ ]:


ans.to_csv("answers.csv",index=False)


# In[ ]:


model.save("saved_model")


# In[ ]:




