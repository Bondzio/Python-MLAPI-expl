#!/usr/bin/env python
# coding: utf-8

# ### This is a notebook for Cat dog image classfication with tensorflow CNN model with data augmentation, drop out.
# 
# ### 1.load package - > 2.download data -> 3.data augmentation -> 4.define model -> 5.train model -> 6.model performance - > 7.save model

# # 1.load package

# ### import tensorflow package and check tensorflow version

# In[ ]:


import tensorflow as tf

print(tf.__version__)


# ### import all other pakcage

# In[ ]:



import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import tqdm
import urllib.request

import os
import zipfile
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator,load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import Adam


# # 2.download cat dog data

# ### download cat and dog picture from microsoft

# In[ ]:


urllib.request.urlretrieve("https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip", "cat_dog.zip")
#zip = ZipFile('cat_dog.zip')
#zip.extractall()


# ### unzip the file

# In[ ]:


import zipfile
zip_ref = zipfile.ZipFile('cat_dog.zip', 'r')
zip_ref.extractall('../output/')
zip_ref.close()

import os
os.listdir('../output/PetImages')

print('total  dog images :', len(os.listdir('../output/PetImages/Dog') ))
print('total  cat images :', len(os.listdir('../output/PetImages/Cat') ))

os.remove('../output/PetImages/Cat/666.jpg')
os.remove('../output/PetImages/Dog/11702.jpg')


# ## Dog picture

# In[ ]:


os.listdir('../output/PetImages/Dog')[1:10]


# In[ ]:


image = load_img('../output/PetImages/Dog/4644.jpg')
plt.imshow(image)


# ## Cat picture

# In[ ]:


os.listdir('../output/PetImages/Cat')[1:10]


# In[ ]:


image = load_img('../output/PetImages/Cat/8962.jpg')
plt.imshow(image)


# # 3.load data with ImageDataGenerator

# 
# <img src="https://www.pyimagesearch.com/wp-content/uploads/2019/07/keras_data_augmentation_in_place.png" width="600">

# In[ ]:


img_width=150
img_height=150
batch_size=20
input_shape = (img_width, img_height, 3)


# In[ ]:


# clean data
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# All images will be rescaled by 1./255.
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.3,
    zoom_range=[0.6,1.0],
    brightness_range=[0.6,1.0],
    rotation_range=90,
    horizontal_flip=True,
    validation_split=0.2
)

#---------------------------------------------

train_generator = train_datagen.flow_from_directory(
    '../output/PetImages',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    seed = 42,
    subset='training'
    
)

#---------------------------------------------

valid_generator = train_datagen.flow_from_directory(
    '../output/PetImages',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    #class_mode='binary',
    class_mode='categorical',
    seed = 42,
    subset='validation'
    
)
#X, y = next(train_generator)


# ## show picture after augmentation

# In[ ]:


plt.figure(figsize=(12, 12))
for i in range(0, 15):
    plt.subplot(5, 3, i+1)
    for X_batch, Y_batch in train_generator:
        image = X_batch[0]
        plt.imshow(image)
        break
plt.tight_layout()
plt.show()


# # 4.define model

# ### create CNN model

# 
# <img src="https://pythonprogramming.net/static/images/machine-learning/artificial-neural-network-model.png" width="600">

# <img src="https://pythonprogramming.net/static/images/machine-learning/convolution-new-featuremap.png" width="600">
# 

# In[ ]:


# Feel free to add more layers or neurons if you have enough computing power
model = Sequential()
model.add(Conv2D(128, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), padding="same"))

model.add(Conv2D(128, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), padding="same"))

model.add(Conv2D(128, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), padding="same"))

model.add(Dropout(0.30))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation("relu"))
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.30))
model.add(Dense(2))
model.add(Activation("softmax"))


# ### compile model with Adam optimizer 

# In[ ]:


optimizer = Adam(lr=0.0003)
#model.compile(loss='binary_crossentropy',
model.compile(loss='binary_crossentropy',
              optimizer=optimizer,
              metrics=['acc'])


# ### set up callbacks with earlystop

# In[ ]:


from keras.callbacks import EarlyStopping, ReduceLROnPlateau,TensorBoard

earlystop=EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=5, verbose=0, mode='auto')

#tensorboard_callback = TensorBoard(log_dir)

callbacks = [earlystop]


# # 5.trainning model

# ### train model with 50 epochs

# In[ ]:


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf


# In[ ]:


history=model.fit_generator(
    train_generator,
    #steps_per_epoch=nb_train_samples // batch_size,
    validation_data=valid_generator,
    epochs=50
    ,callbacks=callbacks
  
)


# # 6.model result

# In[ ]:



#-----------------------------------------------------------
# Retrieve a list of list results on training and test data
# sets for each training epoch
#-----------------------------------------------------------
import matplotlib.image  as mpimg
import matplotlib.pyplot as plt
acc      = history.history[     'acc' ]
val_acc  = history.history[ 'val_acc' ]
loss     = history.history[    'loss' ]
val_loss = history.history['val_loss' ]

epochs   = range(len(acc)) # Get number of epochs

#------------------------------------------------
# Plot training and validation accuracy per epoch
#------------------------------------------------
plt.plot  ( epochs,     acc )
plt.plot  ( epochs, val_acc )
plt.title ('Training and validation accuracy')
plt.figure()

#------------------------------------------------
# Plot training and validation loss per epoch
#------------------------------------------------
#plt.plot  ( epochs,     loss )
#plt.plot  ( epochs, val_loss )
#plt.title ('Training and validation loss'   )


# # 7.save model and load model

# In[ ]:


get_ipython().system('pip install -q pyyaml h5py')


# In[ ]:


# save model
from keras.models import load_model
model.save('dog_cat_cnn_model.h5')


# In[ ]:


from IPython.display import FileLink
FileLink(r'dog_cat_cnn_model.h5')


# ### load the saved model

# In[ ]:


import keras
new_model = keras.models.load_model('dog_cat_cnn_model.h5')


# ### make prediction on test data

# In[ ]:


val_loss, val_acc = model.evaluate(valid_generator)  # evaluate the out of sample data with model
#print(val_loss)  # model's loss (error)
print(val_acc)  # model's accuracy


# ### make prediction on one image

# 
# <img src="https://dcist.com/wp-content/uploads/sites/3/2019/04/Gem2-768x689.jpg" width="400">

# In[ ]:


urllib.request.urlretrieve('https://dcist.com/wp-content/uploads/sites/3/2019/04/Gem2-768x689.jpg', "image.jpg")


# In[ ]:


import numpy as np
import pandas as pd
#from keras_preprocessing import image
#import PIL.Image as Image
import tensorflow as tf
#import cv2
import PIL.Image as Image
x = Image.open('image.jpg').resize((150, 150))
x = np.array(x)/255.0
new_model = tf.keras.models.load_model ('dog_cat_cnn_model.h5')
result = new_model.predict(x[np.newaxis, ...])
df = pd.DataFrame(data =result,columns=['cat','dog'])
df


# # 8 Reference
# 
# * https://pythonprogramming.net/convolutional-neural-network-deep-learning-python-tensorflow-keras/
# * https://www.coursera.org/specializations/tensorflow-in-practice
# * https://www.udacity.com/course/intro-to-tensorflow-for-deep-learning--ud187
# * https://www.datacamp.com/courses/introduction-to-tensorflow-in-python
