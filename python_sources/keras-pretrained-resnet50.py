#!/usr/bin/env python
# coding: utf-8

# # Humpback Whale Identification - CNN with Keras
# This kernel is based on [Anezka Kolaceke](https://www.kaggle.com/anezka)'s awesome work: [CNN with Keras for Humpback Whale ID](https://www.kaggle.com/anezka/cnn-with-keras-for-humpback-whale-id)

# In[ ]:


import numpy as np 
import pandas as pd 
import os
import matplotlib.pyplot as plt
import matplotlib.image as mplimg
from matplotlib.pyplot import imshow

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

from keras import layers
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.layers import Input, Dense, Activation, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalAveragePooling2D
from keras.models import Model

import keras.backend as K
from keras.models import Sequential

import warnings
warnings.simplefilter("ignore", category=DeprecationWarning)


# In[ ]:


os.listdir("../input/")


# In[ ]:


train_df = pd.read_csv("../input/train.csv")
train_df.head()


# In[ ]:


img_size = 100


# In[ ]:


def prepareImages(data, m, dataset):
    print("Preparing images")
    X_train = np.zeros((m, img_size, img_size, 3))
    count = 0
    
    for fig in data['Image']:
        img = image.load_img("../input/"+dataset+"/"+fig, target_size=(img_size, img_size, 3))
        x = image.img_to_array(img)
        x = preprocess_input(x)

        X_train[count] = x
        if (count%500 == 0):
            print("Processing image: ", count+1, ", ", fig)
        count += 1
    
    return X_train


# In[ ]:


def prepare_labels(y):
    values = np.array(y)
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    # print(integer_encoded)

    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    # print(onehot_encoded)

    y = onehot_encoded
    # print(y.shape)
    return y, label_encoder


# In[ ]:


X = prepareImages(train_df, train_df.shape[0], "train")
X /= 255


# In[ ]:


y, label_encoder = prepare_labels(train_df['Id'])


# In[ ]:


y.shape


# In[ ]:


from keras.applications.resnet50 import ResNet50
from keras.metrics import categorical_accuracy, top_k_categorical_accuracy, categorical_crossentropy
from keras.optimizers import Adam

def top_5_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=5)


# In[ ]:


def pre_model():
    base_model = ResNet50(input_shape=(img_size, img_size, 3), weights=None, classes=5005)
    base_model.compile(optimizer=Adam(lr=0.002), loss='categorical_crossentropy', metrics=[categorical_crossentropy, categorical_accuracy, top_5_accuracy])
    return base_model


# In[ ]:


model = pre_model()
model.summary()


# In[ ]:


from keras.callbacks import EarlyStopping, ReduceLROnPlateau


# In[ ]:


early_stopping = EarlyStopping(monitor='val_loss', mode='min', restore_best_weights=False)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3)

callback = [reduce_lr]


# In[ ]:


history = model.fit(X, y, epochs=100, batch_size=128, verbose=1, validation_split=0.1, callbacks=callback)


# In[ ]:


plt.plot(history.history['top_5_accuracy'])
plt.plot(history.history['val_top_5_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.show()


# In[ ]:


test = os.listdir("../input/test/")
print(len(test))


# In[ ]:


col = ['Image']
test_df = pd.DataFrame(test, columns=col)
test_df['Id'] = ''


# In[ ]:


X = prepareImages(test_df, test_df.shape[0], "test")
X /= 255


# In[ ]:


predictions = model.predict(np.array(X), verbose=1)


# In[ ]:


for i, pred in enumerate(predictions):
    test_df.loc[i, 'Id'] = ' '.join(label_encoder.inverse_transform(pred.argsort()[-5:][::-1]))


# In[ ]:


test_df.head(10)
test_df.to_csv('submission.csv', index=False)

