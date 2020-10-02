#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from keras.datasets import cifar10
from matplotlib import pyplot as plt
from scipy.misc import toimage


# In[ ]:


# Reading dataset


# In[ ]:


(X_train,y_train), (X_test, y_test) = cifar10.load_data()


# In[ ]:


for i in range(0,9):
    plt.subplot(330+1+i)
    plt.imshow(toimage(X_train[i]))
plt.show()


# In[ ]:


import numpy
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import max_norm
from keras.optimizers import SGD
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')


# In[ ]:


seed=7
numpy.random.seed(seed)


# In[ ]:


X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train = X_train / 255.0
X_test = X_test / 255.0


# In[ ]:


# one hot encoding. Explore more
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]


# In[ ]:


# Running the model
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(3, 32, 32), padding='same', activation='relu',kernel_constraint=max_norm(3.)))
#model.add(Conv2D(32, (3,3), input_shape=(3,32,32), padding='same', activation='relu', kernel_constrain=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Conv2D(32, (3,3), activation='relu', padding='same',kernel_constraint=max_norm(3.))) 
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))
# Compile model
epochs = 25
lrate = 0.01
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
print(model.summary())


# In[ ]:


# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=32)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))


# In[ ]:




