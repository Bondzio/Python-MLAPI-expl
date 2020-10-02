#!/usr/bin/env python
# coding: utf-8

# In[17]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.optimizers import Adam
from keras.callbacks import TensorBoard

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import load_model
from keras.preprocessing.image import img_to_array, array_to_img
from keras.utils.vis_utils import plot_model
# Any results you write to the current directory are saved as output.


# In[18]:


train_df=pd.read_csv('../input/train.csv')
test_df=pd.read_csv('../input/test.csv')


# In[19]:


train_df.head(5)


# In[20]:


train_data = np.array(train_df, dtype='float32')
test_data = np.array(test_df, dtype='float32')


# In[ ]:





# In[21]:


X_train = train_data[:, 1:] / 255
y_train = train_data[:, 0]
x_test = test_data[:, :] / 255


# In[ ]:





# In[ ]:





# In[22]:


im_rows = 28
im_cols = 28
batch_size = 512
im_shape = (im_rows, im_cols, 1)


# In[23]:


X_train = X_train.reshape(-1, *im_shape)
X_train.shape


# In[24]:


x_test.shape


# In[25]:


x_test = x_test.reshape(-1, *im_shape)
x_test.shape


# In[ ]:





# In[26]:


image = x_validate[10, :].reshape(28,28)
plt.imshow(image)
plt.show()
print(image)


# In[27]:


print('X_train shape: {}'.format(x_train.shape))
print('x_validate shape: {}'.format(x_validate.shape))


# In[43]:


##model building
model = Sequential()
#convolutional layer with rectified linear unit activation
model.add(Conv2D(filters=16, kernel_size=2,padding='same'
                , activation='relu',
                 input_shape=im_shape))
model.add(MaxPooling2D(pool_size=(2, 2)))

#32 convolution filters used each of size 3x3
#again
model.add(Conv2D(filters=32, kernel_size=2,padding='same'
                , activation='relu'))
#64 convolution filters used each of size 3x3
#choose the best features via pooling
model.add(MaxPooling2D(pool_size=(2, 2)))

#randomly turn neurons on and off to improve convergence
model.add(Conv2D(filters=64, kernel_size=2,padding='same'
                , activation='relu'))
model.add(Dropout(0.2))
#flatten since too many dimensions, we only want a classification output
model.add(Flatten())
#fully connected to get all relevant data
model.add(Dense(500, activation='relu'))
#one more dropout for convergence' sake :) 
model.add(Dropout(0.2))
#output a softmax to squash the matrix into output probabilities
model.add(Dense(10, activation='softmax'))


# In[44]:


model.compile(loss='sparse_categorical_crossentropy',
    optimizer=Adam(lr=0.01),
    metrics=['accuracy'])


# In[30]:





# In[ ]:





# In[51]:


from keras.callbacks import ModelCheckpoint 
checkPoint=ModelCheckpoint('filepath=aug.model.weight.best.hdf5', verbose=1,save_weights_only=True)


# In[ ]:





# In[67]:



model_log=model.fit(
    x=X_train, y=y_train, batch_size=batch_size,
    epochs=10, verbose=1,validation_split=.2,
    callbacks=[checkPoint]
     
)


# In[71]:


model.summary()




# In[72]:


# plotting the metrics
fig = plt.figure()
plt.subplot(2,1,1)
plt.plot(model_log.history['acc'])
#plt.plot(model_log.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='lower right')


# In[73]:


model.save('model.h5')
model.save_weights('model_weight.h5')


# In[59]:


new_model=load_model('model.h5')


# In[74]:


image = x_train[50, :].reshape(28,28)
plt.imshow(image)
plt.show()
print(image)
img2 = np.reshape(image,[1,28,28,1])
prediction=new_model.predict_classes(img2)
prediction


# In[75]:




plot_model(new_model, show_shapes=True, show_layer_names=True, to_file='model.png')
from IPython.display import Image
Image(retina=True, filename='model.png')


# In[ ]:





# In[ ]:





# In[76]:


y_pred = new_model.predict(x_test)


# In[77]:


x_test.shape,y_pred.shape


# In[78]:


test_pred = pd.DataFrame(new_model.predict(x_test, batch_size=100))
test_pred = pd.DataFrame(test_pred.idxmax(axis = 1))
test_pred.index.name = 'ImageId'
test_pred = test_pred.rename(columns = {0: 'Label'}).reset_index()
test_pred['ImageId'] = test_pred['ImageId'] + 1


# In[81]:


test_pred.head()


# In[82]:


test_pred.to_csv('mnist_submission.csv', index = False)


# In[ ]:





# In[ ]:




