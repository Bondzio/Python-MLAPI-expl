#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tensorflow.keras import applications
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential, Model 
from tensorflow.keras.layers import Dropout, Flatten, Dense,Conv2D,MaxPooling2D
import pandas as pd
import numpy as np
import os


# In[ ]:


import tensorflow as tf
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))


# In[ ]:


a = "../input/ashish/data_final"


# In[ ]:


dir_path = "../input/ashish/data_final"


# In[ ]:


import os
os.listdir(dir_path)


# In[ ]:


tf.keras.backend.clear_session()


# In[ ]:


traindf=pd.read_csv("../input/ashish/labels_final.csv",dtype=str)


# In[ ]:


traindf.tail()


# In[ ]:


datagen=ImageDataGenerator(rescale=1./255.,validation_split=0.25,rotation_range=30,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)


# In[ ]:


train_generator=datagen.flow_from_dataframe(
dataframe=traindf,
directory=dir_path,
x_col="path",
y_col="label",
subset="training",
batch_size=128,
seed=42,
shuffle=True,
class_mode="categorical",
target_size=(156,156))


# In[ ]:


valid_generator=datagen.flow_from_dataframe(
dataframe=traindf,
directory=dir_path,
x_col="path",
y_col="label",
subset="validation",
batch_size=128,
seed=42,
shuffle=True,
class_mode="categorical",
target_size=(156,156))


# In[ ]:


model = applications.VGG19(weights = "imagenet", include_top=False, input_shape = (156,156, 3))
model.summary()


# In[ ]:


for layer in model.layers[:-6]:
    layer.trainable = False
for layer in model.layers:
    print(layer, layer.trainable)    


# In[ ]:


modell=model.output
modell=Conv2D(4096, (4, 4), padding="valid", activation="relu")(modell)
modell=Conv2D(4096, (1, 1), padding="valid", activation="relu")(modell)
modell=Flatten()(modell)
modell=Dense(16,activation="softmax")(modell)
final_model=Model(inputs = model.input, outputs = modell)
final_model.summary()


# In[ ]:


for layer in final_model.layers:
    print(layer, layer.trainable)    


# In[ ]:


final_model.compile(loss = "categorical_crossentropy", optimizer = optimizers.SGD(lr=0.01, momentum=0.88), metrics=["accuracy"])


# In[ ]:


get_ipython().run_line_magic('load_ext', 'tensorboard')


# In[ ]:


import tensorflow as tf
import datetime


# In[ ]:


get_ipython().system('rm -rf ./logs/ ')


# In[ ]:


logdir = os.path.join("logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)


# In[ ]:


ls


# In[ ]:


final_model.fit_generator(
train_generator,
epochs = 1,
validation_data = valid_generator,callbacks=[tensorboard_callback])


# In[ ]:


get_ipython().run_line_magic('tensorboard', '--logdir logs')


# In[ ]:




