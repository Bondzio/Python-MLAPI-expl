#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os


# In[ ]:


train = pd.read_csv("../input/plant-pathology-2020-fgvc7/train.csv")
test = pd.read_csv("../input/plant-pathology-2020-fgvc7/test.csv")


# In[ ]:


train


# In[ ]:


test


# In[ ]:


import cv2
import matplotlib.pyplot as plt


# In[ ]:


base_path = "../input/plant-pathology-2020-fgvc7/images/"
def read_img(img_path):
    img = cv2.imread(base_path + img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


# In[ ]:


import tqdm
# height = []
# width = []
# channels = []
# for file in tqdm.tqdm(train["image_id"]):
#     img = read_img(file + ".jpg")
#     height.append(img.shape[0])
#     width.append(img.shape[1])
#     channels.append(img.shape[2])

# for file in train["image_id"]:
#     img = read_img(file + ".jpg")
#     height.append(img.shape[0])
#     width.append(img.shape[1])
#     channels.append(img.shape[2])


# In[ ]:


# train["height"] = height
# train["width"] = width
# train["channels"] = channels


# In[ ]:


# train["height"].hist()


# In[ ]:


# train["height"].value_counts()


# In[ ]:


# train["width"].hist()


# In[ ]:


# train["width"].value_counts()


# In[ ]:


# train["channels"].hist()


# In[ ]:


img_size = 256
def resize_to_square(im, img_size = img_size):
    old_size = im.shape[:2] # old_size is in (height, width) format
    ratio = float(img_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])
    # new_size should be in (width, height) format
    im = cv2.resize(im, (new_size[1], new_size[0]), cv2.INTER_NEAREST)
    delta_w = img_size - new_size[1]
    delta_h = img_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)
    color = [0, 0, 0]
    new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,value=color)
    return new_im


# In[ ]:


# del test_imgs
train_imgs = np.zeros([train.shape[0], 256, 256, 3])
for i, file in enumerate(tqdm.tqdm(train["image_id"])):
    img = read_img(file + ".jpg")
    img = resize_to_square(img)
    train_imgs[i] = img


# In[ ]:


from tensorflow import keras


# In[ ]:


img_input = keras.layers.Input(shape=(256,256,3))
hidden1 = keras.layers.Conv2D(8, kernel_size = (3,3), activation="relu")(img_input)
hidden1 = keras.layers.MaxPool2D()(hidden1)
hidden1 = keras.layers.Conv2D(16, kernel_size = (3,3), activation="relu")(hidden1)
hidden1 = keras.layers.MaxPool2D()(hidden1)
hidden1 = keras.layers.Conv2D(32, kernel_size = (3,3), activation="relu")(hidden1)
hidden1 = keras.layers.MaxPool2D()(hidden1)
hidden1 = keras.layers.Conv2D(64, kernel_size = (3,3), activation="relu")(hidden1)
hidden1 = keras.layers.MaxPool2D()(hidden1)
hidden1 = keras.layers.Conv2D(128, kernel_size = (3,3), activation="relu")(hidden1)
hidden1 = keras.layers.MaxPool2D()(hidden1)
hidden1 = keras.layers.Conv2D(256, kernel_size = (3,3), activation="relu")(hidden1)
hidden1 = keras.layers.GlobalMaxPooling2D()(hidden1)
hidden1 = keras.layers.Dense(64)(hidden1)
hidden1 = keras.layers.Dense(32)(hidden1)
hidden1 = keras.layers.Dropout(.2)(hidden1)
output = keras.layers.Dense(4, activation = "softmax")(hidden1)
model = keras.models.Model(inputs=[img_input], outputs=[output])


# In[ ]:


model.summary()


# In[ ]:


target_cols = ["healthy", "multiple_diseases","rust", "scab"]


# In[ ]:


y_train = train[target_cols].values


# In[ ]:


train_imgs.shape


# In[ ]:


model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(lr=.001), metrics = ["accuracy"])
history = model.fit(train_imgs, y_train, epochs=20, batch_size = 128)


# In[ ]:


del train_imgs
test_imgs = np.zeros([test.shape[0], 256, 256, 3])  
for i, file in enumerate(tqdm.tqdm(test["image_id"])):
    img = read_img(file + ".jpg")
    img = resize_to_square(img)
    test_imgs[i] = img


# In[ ]:


test_preds = model.predict(test_imgs, batch_size = 128, verbose = True)


# In[ ]:


test_preds.shape


# In[ ]:


test[target_cols] = pd.DataFrame(test_preds, columns = target_cols)


# In[ ]:


test.to_csv("submission.csv", index = False)


# In[ ]:


test


# In[ ]:


sample_sub = pd.read_csv("../input/plant-pathology-2020-fgvc7/sample_submission.csv")


# In[ ]:


sample_sub


# In[ ]:


for col in target_cols:
    print(col)
    test[col].hist(bins = 20)
    plt.show()


# In[ ]:




