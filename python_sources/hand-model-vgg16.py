#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os
import cv2
import keras
from random import shuffle
from tqdm import tqdm
from keras.layers import Dense
from keras.optimizers import SGD, Adam
from keras.applications import vgg16
from joblib import dump, load
print("done")


# In[ ]:


print(os.listdir("../input/xr_hand_train"))


# In[ ]:


TRAIN_DIR = "../input/xr_hand_train/XR_HAND_TRAIN"
TEST_DIR = "../input/xr_hand_valid/XR_HAND_VALID"


postive = 1
negative = 0
IMG_SIZE = 224


# In[ ]:


def craete_label(class_name):
    label = np.zeros(2)
    label[class_name] = 1
    return label

def create_data(path):
    x = []
    y = []
    for item in tqdm(os.listdir(path)):
        patient_path = os.path.join(path, item)
        for patient_study in os.listdir(patient_path):
            type_of_study = patient_study.split('_')[1]
            if type_of_study == "positive":
                class_name = postive
            else:
                class_name = negative

            p_path = os.path.join(patient_path, patient_study)
            label = craete_label(class_name)
            for patient_image in os.listdir(p_path):
                image_path = os.path.join(p_path, patient_image)
                bgr = cv2.imread(image_path)
                lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
                lab_planes = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                lab_planes[0] = clahe.apply(lab_planes[0])
                lab = cv2.merge(lab_planes)
                bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
                img = cv2.resize(bgr, (IMG_SIZE, IMG_SIZE))
                img = np.divide(img, 255)
                x.append(np.array(img))
                y.append(label)
    return np.array(x).reshape(-1, IMG_SIZE, IMG_SIZE, 3), np.array(y)


# In[ ]:


x, y = create_data(TRAIN_DIR)
print(len(x))
print(len(y))
print(x.shape)
print(y.shape)


# In[ ]:


from keras.applications import VGG16


# In[ ]:


vgg_con = VGG16(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))


# In[ ]:


from keras import models
from keras import layers
from keras import optimizers
# for layer in vgg_con.layers[:-4]:
#     layer.trainable = False
for layer in vgg_con.layers:
    print(layer, layer.trainable)
vgg_con.summary()


# In[ ]:


model = models.Sequential()
model.add(vgg_con)


# In[ ]:


model.summary()
model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(2, activation='softmax'))
print("-----------------------------")
model.summary()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# from keras.preprocessing.image import ImageDataGenerator
# train_datagen = ImageDataGenerator(
#       rescale=1./255,
#       rotation_range=20,
#       width_shift_range=0.2,
#       height_shift_range=0.2,
#       horizontal_flip=True,
#       fill_mode='nearest')
# validation_datagen = ImageDataGenerator(rescale=1./255)
# train_batchsize = 100
# val_batchsize = 10
# train_generator = train_datagen.flow_from_directory(
#         train_dir,
#         target_size=(IMG_SIZE, IMG_SIZE),
#         batch_size=train_batchsize,
#         class_mode='categorical')
# validation_generator = validation_datagen.flow_from_directory(
#         validation_dir,
#         target_size=(IMG_SIZE, IMG_SIZE),
#         batch_size=val_batchsize,
#         class_mode='categorical',
#         shuffle=False)


# In[ ]:


sgd = SGD(lr=0.01, decay=1e-6, nesterov=True)


# In[ ]:


model.compile(optimizer=sgd, loss="categorical_crossentropy", metrics=["accuracy"])


# In[ ]:


model.fit(x, y, validation_split=0.2, epochs=100)


# In[ ]:





# In[ ]:


x_test, y_test = create_data(TEST_DIR)


# In[ ]:


print(x_test.shape)
print(y_test.shape)


# In[ ]:


result = model.predict(x_test)


# In[ ]:


len(result)


# In[ ]:


result_v1 = model.predict_classes(x_test)


# In[ ]:


result_v1


# In[ ]:





# In[ ]:


res = np.zeros(len(y_test))
for i in range(len(y_test)):
    res[i] = np.argmax(y_test[i])
print(res[0])
print(result_v1[0])
print(len(res))
print(len(result_v1))


# In[ ]:


count = 0
for i in range(len(res)):
    if int(res[i]) == result_v1[i] :
        count += 1
        
print("Test Accuracy : ", count / len(res) * 100 , "%")


# In[ ]:


model.save("model.h5")


# In[ ]:




