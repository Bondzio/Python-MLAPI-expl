#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from keras.datasets import cifar10


# In[ ]:


(train_data,train_labels),(test_data,test_labels) = cifar10.load_data()


# In[ ]:


batch_size = 500
image_size =(512,512) 
input_shape = (512,512,3)


# In[ ]:


global graph,model
import tensorflow as tf
graph = tf.get_default_graph()


# In[ ]:


from keras.applications.xception import Xception, preprocess_input
model_without_top = Xception(include_top=False,weights='imagenet',pooling=None,input_shape=input_shape)


# In[ ]:


from keras.layers import Dense, Activation, GlobalAveragePooling2D
from keras.models import Sequential

model = Sequential()
model.add(GlobalAveragePooling2D(input_shape=(16,16,2048)))
model.add(Dense(2048))
model.add(Activation('relu'))
model.add(Dense(10))
model.add(Activation('softmax'))


# In[ ]:


model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])


# In[ ]:


from keras.utils import np_utils
import cv2
import numpy as np
def data_generator(data,labels,msg,batch_size=batch_size):
    print("startint generator... ",msg)
    while True:
        for i in range(0,labels.shape[0] // batch_size):
            temp_batch_data = data[batch_size*i:batch_size*(i+1)]
            temp_batch_labels = labels[batch_size*i:batch_size*(i+1)]
            batch_data = []
            for j in range(0, len(temp_batch_data)):
                batch_data.append(cv2.resize(temp_batch_data[j],image_size,interpolation=cv2.INTER_CUBIC))
            batch_labels = np_utils.to_categorical(temp_batch_labels,10)
            c = np.array(batch_data).astype('float32')
            a = preprocess_input(c)
            with graph.as_default():
                b = model_without_top.predict(a)
            yield b,batch_labels


# In[ ]:


model.fit_generator(data_generator(train_data,train_labels,'train'),steps_per_epoch=train_labels.shape[0]//batch_size,validation_data=data_generator(test_data,test_labels,'test'),validation_steps=test_labels.shape[0]//batch_size)


# In[ ]:




