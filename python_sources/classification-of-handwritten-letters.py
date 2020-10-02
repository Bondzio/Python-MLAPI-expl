#!/usr/bin/env python
# coding: utf-8

# # Import Necessary Packages

# In[ ]:


import numpy as np 
import pandas as pd

import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, BatchNormalization
from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping


from sklearn.utils import shuffle
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import matplotlib.pyplot as plt


# # Data Collection and Preprocessing 

# In[ ]:


letters = pd.read_csv("../input/classification-of-handwritten-letters/letters.csv")
letters2 = pd.read_csv("../input/classification-of-handwritten-letters/letters2.csv")
letters3 = pd.read_csv("../input/classification-of-handwritten-letters/letters3.csv")


# In[ ]:


source = pd.Series([])

letters["source"] = source
letters2["source"] = source
letters3["source"] = source
for i in range(len(letters)): 
    letters["source"][i] = "/letters"

for i in range(len(letters2)): 
    letters2["source"][i] = "/letters2"
    
for i in range(len(letters3)):
    letters3["source"][i] = "/letters3"


# In[ ]:


data = pd.concat((letters, letters2, letters3), axis = 0, ignore_index = True)


# In[ ]:


data.shape


# In[ ]:


data.head()


# In[ ]:


data.tail()


# In[ ]:


data = shuffle(data, random_state = 42).reset_index(drop = True)


# In[ ]:


data.head()


# In[ ]:


data.tail()


# In[ ]:


dirname = "../input/classification-of-handwritten-letters"
imgs = []
for i in range(len(data)):
    imgs.append(load_img(os.path.join(dirname + data["source"][i], data["file"][i]), target_size = (32, 32)))


# In[ ]:


imgs_array = np.array([img_to_array(img) for img in imgs])/255


# In[ ]:


imgs_array.shape


# Both the letter and the background are considered as labels.
# 
# Targets is a list of 2 element lists where the first element is the letter and the second is the background. 

# In[ ]:


targets = []
for i, row in data.iterrows(): 
    t = [data.letter[i], data.background[i]]
    targets.append(t)


# In[ ]:


targets_array = np.array(targets)


# Scikir-learn library's MultiLabelBinarizer allows to one-hot encode features with multiple labels. 

# In[ ]:


X_train, X_val, y_train, y_val = train_test_split(imgs_array, targets_array, 
                                                test_size=0.2,  
                                                random_state=42)


# In[ ]:


mlb = MultiLabelBinarizer()
y_train = mlb.fit_transform(y_train)
y_val = mlb.transform(y_val)


# In[ ]:


for (i, target) in enumerate(mlb.classes_):
    print("{}. {}".format(i + 1, target))


# There are 33 distinct letters and 4 different backgrounds. 
# 
# Backrground Labels: 
# * 0 => striped
# * 1 => gridded
# * 2 => no background
# * 3 => graph paper

# In[ ]:


def display_image(images, list_of_labels = np.arange(15)): 
    plt.figure(figsize=(12,12))
    for i in list_of_labels: 
        plt.subplot(3, 5, i+1)
        plt.title('Letter: %s \n'%targets[i][0]+                    'Background: %s\n'%targets[i][1],
                         fontsize=18)
        plt.imshow(imgs[i])
        
    plt.subplots_adjust(bottom = 0.001)
    plt.subplots_adjust(top = 0.99)
    plt.show()
   


# In[ ]:


display_image(imgs_array)


# In[ ]:


print("shape of X_train: {} \nshape of X_val: {} \nshape of y_train: {} \nshape of y_val: {}".format(
    X_train.shape, X_val.shape, y_train.shape, y_val.shape))


# # The CNN Model

# In[ ]:


img_rows = 32
img_cols = 32
channels = 3
classes = len(mlb.classes_)

model = Sequential()

model.add(Conv2D(64, kernel_size = (3, 3), padding = 'Same',
                     activation = 'relu',
                     input_shape = (img_rows, img_cols, channels)))
model.add(BatchNormalization(axis=-1))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Conv2D(64, (3, 3), padding = 'Same', activation = 'relu'))
model.add(BatchNormalization(axis=-1))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(128, (3, 3), padding = 'Same', activation = 'relu'))
model.add(BatchNormalization(axis=-1))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Conv2D(128, (3, 3), padding = 'Same', activation = 'relu'))
model.add(BatchNormalization(axis=-1))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(1024, activation = 'relu'))
model.add(Dropout(0.25))
model.add(Dense(classes, activation='sigmoid'))

model.summary()



# In[ ]:


model.compile(loss=keras.losses.binary_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])


# In[ ]:


aug = ImageDataGenerator(
        rotation_range=5, 
        zoom_range = 0.2, 
        width_shift_range=0.2,  
        height_shift_range=0.2 
        )


# In[ ]:


from tensorflow.keras.callbacks import EarlyStopping
early_stop = EarlyStopping(monitor = 'val_loss', mode = 'min', verbose = 1, patience = 10)


# In[ ]:


BS = 32
EPOCHS = 100
history = model.fit(x=aug.flow(X_train, y_train, batch_size = BS),
                    steps_per_epoch = len(X_train)//BS,   
                    epochs = EPOCHS,
                    verbose = 1,
                    validation_data = (X_val, y_val), callbacks=[early_stop])


# # Model Evaluation

# In[ ]:


loss_accuracy = pd.DataFrame(model.history.history)


# In[ ]:


loss_accuracy.plot()
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="upper left")


# In[ ]:


predictions = model.predict(X_val)


# In[ ]:


predictions[predictions>0.5] = 1
predictions[predictions<=0.5] = 0


# In[ ]:


print(classification_report(y_val, predictions))


# In[ ]:


pred_results = mlb.inverse_transform(predictions)
true_results = mlb.inverse_transform(y_val)


# In[ ]:


correct = 0 
total = 0 
for i in range(len(y_val)):
    if pred_results[i] == true_results[i]:
        correct += 1
        
    total += 1 
    
print("Accuracy: ", round(correct/total, 3))


# In[ ]:


def display_predicted_image(images, list_of_labels = np.arange(15)): 
    plt.figure(figsize=(12,12))
    for i in list_of_labels:
        if len(pred_results[i]) != 2:
            print("Sorry, prediction {} has the wrong size, WRONG PREDICTION".format(i+1))
        else:
            plt.subplot(3, 5, i+1)
            plt.title('Prediction %s \n'%(i+1)+                        'True Letter: %s \n'%true_results[i][1]+                            'True Background: %s\n'%true_results[i][0]+                                'Predicted Letter: %s \n'%pred_results[i][1]+                                  'Predicted Background: %s \n'%pred_results[i][0],
                                     fontsize=18)
        
            plt.imshow(images[i])
        
    plt.subplots_adjust(bottom = 0.005)
    plt.subplots_adjust(top = 1.5)
    plt.subplots_adjust(left = 0.125)
    plt.subplots_adjust(right = 1.5)
    plt.show()


# In[ ]:


display_predicted_image(X_val, list_of_labels = np.arange(15))


# # Saving the model

# In[ ]:


model.save("handwritten_classification_model.h5")
print("Saved model to disk")

