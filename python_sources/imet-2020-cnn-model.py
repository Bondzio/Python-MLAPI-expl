#!/usr/bin/env python
# coding: utf-8

# # Some CNN Bois
# 
# First, thanks for some useful notebook
# 
# 
# https://www.kaggle.com/dimakyn/multi-label-keras
# 
# https://github.com/lmoroney/dlaicourse
# 
# https://github.com/salmanhiro/Galaxy-Zoo-CNN
# 
# Then I would like to hear some music
# 
# 
# [![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/z9mH-OZ2B-Y/0.jpg)](https://www.youtube.com/watch?v=z9mH-OZ2B-Y)
# 

# # Loading

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

#Ugh, so long
#import os
#for dirname, _, filenames in os.walk('/kaggle/input'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


df_train = pd.read_csv('/kaggle/input/imet-2020-fgvc7/train.csv')
df_label = pd.read_csv('/kaggle/input/imet-2020-fgvc7/labels.csv')
submission = pd.read_csv('/kaggle/input/imet-2020-fgvc7/sample_submission.csv')


# In[ ]:


df_train['id'] += '.png'


# In[ ]:


df_train.head(1)


# In[ ]:


df_label.head(1)


# In[ ]:


submission['id'] += '.png'


# In[ ]:


submission.head(1)


# ## Gonna make the `attribute_ids` to list
# 
# Thanks to [dimakyn](https://www.kaggle.com/dimakyn/multi-label-keras) idea

# In[ ]:


df_train["attribute_ids"] = df_train["attribute_ids"].apply(lambda x:x.split())


# In[ ]:


df_train.head(1)


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# # Take a look

# In[ ]:


img = mpimg.imread('/kaggle/input/imet-2020-fgvc7/train/000040d66f14ced4cdd18cd95d91800f.png')
plt.imshow(img)
plt.axis('Off')
plt.show()


# In[ ]:


from keras_preprocessing.image import ImageDataGenerator


# # Construct Generator

# In[ ]:


training_datagen = ImageDataGenerator(rescale = 1./255,
                                      rotation_range=180,
                                      width_shift_range=0.2,
                                      height_shift_range=0.2,
                                      shear_range=0.2,
                                      zoom_range=0.2,
                                      horizontal_flip=True,
                                      fill_mode='nearest')


# In[ ]:


test_datagen = ImageDataGenerator(rescale=1./255.)


# In[ ]:


train_generator = training_datagen.flow_from_dataframe(dataframe=df_train,
                                                       directory='/kaggle/input/imet-2020-fgvc7/train/',
                                                       x_col='id',
                                                       y_col='attribute_ids',
                                                       batch_size=128,
                                                       seed=17,
                                                       shuffle=True,
                                                       class_mode="categorical",
                                                       target_size=(128,128))


# In[ ]:


test_generator = test_datagen.flow_from_dataframe(dataframe=submission,
                                                       directory='/kaggle/input/imet-2020-fgvc7/test/',
                                                       x_col='id',
                                                       batch_size=1,
                                                       seed=17,
                                                       shuffle=False,
                                                       class_mode=None,
                                                       target_size=(128,128))


# # Construct Model

# In[ ]:


from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping
from keras.models import Sequential


# In[ ]:


input_shape = (128, 128, 3)


# In[ ]:


model = Sequential()

model.add(Conv2D(32, (3, 3), padding="same",input_shape=input_shape, activation = 'relu'))
model.add(BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(32, (3, 3), padding="same", activation = 'relu'))
model.add(BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(512, activation = 'relu'))
model.add(BatchNormalization())
model.add(Dropout(0.2))

model.add(Dense(3471, activation='sigmoid')) 

model.compile(optimizer = 'adam',loss="binary_crossentropy",metrics=["accuracy"])


# In[ ]:


model.summary()


# # Training

# In[ ]:


early_stopping_callback = EarlyStopping(monitor='val_loss', patience=10)

model.fit_generator(generator = train_generator,
                    steps_per_epoch = train_generator.n//train_generator.batch_size,
                    callbacks = [early_stopping_callback],
                    epochs = 3,
                    verbose = 1)


# # Predicting

# I use the predict generator as used in https://www.kaggle.com/dimakyn/multi-label-keras

# In[ ]:


test_generator.reset()
pred = model.predict_generator(test_generator,
                               steps=test_generator.n//test_generator.batch_size,
                               verbose=1)

pred_bool = (pred >0.2)

predictions=[]

labels = train_generator.class_indices

labels = dict((v,k) for k,v in labels.items())

for row in pred_bool:
    l=[]
    for index,cls in enumerate(row):
        if cls:
            l.append(labels[index])
    predictions.append(" ".join(l))
    
filenames = test_generator.filenames

results = pd.DataFrame({"id":filenames,"attribute_ids":predictions})
results["id"] = results["id"].apply(lambda x:x.split(".")[0])
results.to_csv("submission.csv",index=False)

