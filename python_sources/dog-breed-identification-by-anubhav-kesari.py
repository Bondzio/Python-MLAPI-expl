#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


from tensorflow.python.keras.applications import ResNet50
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, GlobalAveragePooling2D, Activation, Flatten, Dropout, BatchNormalization

import h5py


# In[ ]:


traindf=pd.read_csv('../input/dog-breed-identification/labels.csv')
testdf=pd.read_csv('../input/dog-breed-identification/sample_submission.csv')


# ## Is there any missing class:

# In[ ]:




traindf.isnull().values.any()


# ## Is there a problem of Class Imbalance ?

# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(13, 6))
traindf['breed'].value_counts().plot(kind='bar')
plt.show()


# In[ ]:


def class_percentages(labels):
    class_map={}
    for i in labels:
        if str(i) not in class_map:
            class_map[str(i)]=1
        else:
            class_map[str(i)]+=1
    #     print(class_map)
    return class_map

p=class_percentages(traindf.breed.values)
# print(p)
# for i in p.items():
#     print(i)

print("Class with maximum images-"+str(max(p, key=p.get))+"  "+str(p[max(p, key=p.get)]))
print("Class with maximum images-"+str(min(p,key=p.get)) +"  "+str(p[min(p, key=p.get)]))


# ## Clearly , there is some amount of class imbalance ,
# ## as biggest class contains almost double of smallest class

# In[ ]:


traindf.head(10)


# 
# ## My Model using extracted features from ResNet Pretrained
# 
# 

# In[ ]:


num_classes = 120
resnet_weights_path = '../input/resnet50/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'

my_new_model = Sequential()
my_new_model.add(ResNet50(include_top=False, pooling='avg', weights=resnet_weights_path))
my_new_model.add(Dense(512))
my_new_model.add(Activation('relu'))
my_new_model.add(Dropout(0.5))
my_new_model.add(Dense(num_classes, activation='softmax'))

# Say not to train first layer (ResNet) model. It is already trained
my_new_model.layers[0].trainable = False

my_new_model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])


# ## Data Preperation

# In[ ]:


from tensorflow.python.keras.applications.resnet50 import preprocess_input
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator

image_size = 224
datagen = ImageDataGenerator(preprocessing_function=preprocess_input, 
                             rescale=1./255.,
                             horizontal_flip=True,
                             width_shift_range = 0.2,
                             height_shift_range = 0.2,
                             validation_split=0.2)


# In[ ]:


train_generator=datagen.flow_from_dataframe(
                        dataframe=traindf,
                        directory="../input/dog-breed-identification/train/",
                        x_col="id",
                        y_col="breed",
                        has_ext=False,
                        subset="training",
                        batch_size=32,
                        seed=50,
                        shuffle=True,
                        class_mode="categorical",
                        target_size=(image_size, image_size))


# In[ ]:


valid_generator=datagen.flow_from_dataframe(
                        dataframe=traindf,
                        directory="../input/dog-breed-identification/train/",
                        x_col="id",
                        y_col="breed",
                        has_ext=False,
                        subset="validation",
                        batch_size=1,
                        seed=42,
                        shuffle=True,
                        class_mode="categorical",
                        target_size=(image_size, image_size))


# ## Test Data Preperation

# In[ ]:


test_datagen=ImageDataGenerator(preprocessing_function=preprocess_input,rescale=1./255.)

test_generator=test_datagen.flow_from_dataframe(
                            dataframe=testdf,
                            directory="../input/dog-breed-identification/test/",
                            x_col="id",
                            y_col=None,
                            has_ext=False,
                            batch_size=1,
                            seed=42,
                            shuffle=False,
                            class_mode=None,
                            target_size=(image_size, image_size))


# In[ ]:


STEP_SIZE_TRAIN=train_generator.n
STEP_SIZE_VALID=valid_generator.n

print(STEP_SIZE_TRAIN)
print(STEP_SIZE_VALID)

my_new_model.fit_generator(generator=train_generator,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_generator,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=3
)


# In[ ]:



my_new_model.evaluate_generator(generator=valid_generator)


# In[ ]:


test_generator.reset()
pred=my_new_model.predict_generator(test_generator,verbose=1)


# In[ ]:


labels = (train_generator.class_indices)
labels = list(labels.keys())
df = pd.DataFrame(data=pred,
                 columns=labels)

columns = list(df)
columns.sort()
df = df.reindex(columns=columns)

filenames = testdf["id"]
df["id"]  = filenames

cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]
df.head(5)


# 
# ## Saving Test Data Output to 'submission.csv'

# In[ ]:


df.to_csv("submission.csv",index=False)


# In[ ]:




