#!/usr/bin/env python
# coding: utf-8

# # This is Image Classification for Cute

# Get the current working directory

# In[1]:


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


# In[2]:


PATH=os.getcwd()
print(PATH)


# In[3]:


PATH="../input/image-classification/image/Image/10_categories"


# In[4]:


print(os.listdir(PATH))


# In[5]:


img_rows=224
img_cols=224
num_channel=3

num_epoch=3
batch_size=32

img_data_list=[]
classes_names_list=[]
data_dir_list=os.listdir(PATH)


# In[6]:


import cv2

for dataset in data_dir_list:
    classes_names_list.append(dataset) 
    print ('Loading images from {} folder\n'.format(dataset)) 
    img_list=os.listdir(PATH+'/'+ dataset)
    for img in img_list:
        input_img=cv2.imread(PATH + '/'+ dataset + '/'+ img )
        input_img_resize=cv2.resize(input_img,(img_rows, img_cols))
        img_data_list.append(input_img_resize)


# In[7]:


num_classes = len(classes_names_list)
print(num_classes)


# In[8]:


import numpy as np

img_data = np.array(img_data_list)
img_data = img_data.astype('float32')
img_data /= 255


# In[9]:


num_of_samples = img_data.shape[0]
input_shape = img_data[0].shape


# In[10]:


print (img_data.shape)
print(num_of_samples)
print(input_shape)


# In[11]:


classes = np.ones((num_of_samples,), dtype='int64')

classes[0:239]=0
classes[239:367]=1
classes[367:490]=2
classes[490:690]=3
classes[690:1490]=4
classes[1490:1958]=5
classes[1958:2393]=6
classes[2393:2828]=7
classes[2828:3626]=8
classes[3626:]=9


# In[12]:


from keras.utils import to_categorical

classes = to_categorical(classes, num_classes)


# In[13]:


print(classes.shape)
print(classes)


# In[14]:


from sklearn.utils import shuffle

X, Y = shuffle(img_data, classes, random_state=2)


# In[15]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=2)


# In[16]:


y_test.shape


# In[17]:


from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D


# In[18]:


model = Sequential()

model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))


# In[19]:


model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=["accuracy"])


# In[20]:


num_epoch=12


# In[21]:


from keras.preprocessing.image import ImageDataGenerator

data_gen = ImageDataGenerator(
    rotation_range=20,
    shear_range=0.5, 
    zoom_range=0.4, 
    rescale=1./255,
    vertical_flip=True, 
    validation_split=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True) 


# In[22]:


#TRN_AUGMENTED = os.path.join(PATH  , 'Trn_Augmented_Images')
#TST_AUGMENTED = os.path.join(PATH  , 'Tst_Augmented_Images')


# In[23]:


train_generator = data_gen.flow_from_directory(
        PATH,
        target_size=(img_rows, img_cols), 
        batch_size=batch_size,
        class_mode='categorical',
        color_mode='rgb', 
        shuffle=True)

 #       save_to_dir=TRN_AUGMENTED, 
 #       save_prefix='TrainAugmented', 
 #       save_format='png', 
 #       subset="training")


# In[24]:


train_generator.class_indices


# In[25]:


test_generator = data_gen.flow_from_directory(
        PATH,
        target_size=(img_rows, img_cols),
        batch_size=32,
        class_mode='categorical',
        color_mode='rgb', 
        shuffle=True, 
        seed=None)

#        save_to_dir=TST_AUGMENTED, 
#        save_prefix='TestAugmented', 
#        save_format='png',
#        subset="validation")


# In[26]:


test_generator.class_indices


# In[27]:


model.fit_generator(train_generator, epochs=num_epoch, validation_data=test_generator,steps_per_epoch = len(X_train)/batch_size,validation_steps=len(X_test)/batch_size)


# In[28]:


model.evaluate_generator(train_generator,steps = len(X_train)/batch_size,verbose=1)


# In[29]:


Y_pred = model.predict(X_test)
print(Y_pred)
Y_train_result = model.predict(X_train)
print(Y_train_result)


# In[30]:


y_pred = np.argmax(Y_pred, axis=1)
print(y_pred)
y_train_result = np.argmax(Y_train_result, axis=1)
print(y_train_result)


# In[31]:


from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report,accuracy_score


# In[32]:



y_true=np.argmax(y_test,axis=1)
y_true_train=np.argmax(y_train,axis=1)


# In[33]:


print(classification_report(y_pred,y_true))
print(classification_report(y_train_result,y_true_train))
print("test accuracy = ",accuracy_score(y_pred,y_true))
print("validation accuracy = ",accuracy_score(y_train_result,y_true_train))


# In[34]:


#from IPython.display import Image
#Image(filename='vgg16.png')


# In[35]:


from tensorflow.keras.layers import Input, Dense


# In[36]:


# Custom_vgg_model_1
#Training the classifier alone
image_input = Input(shape=(img_rows, img_cols, num_channel))


# In[37]:


from tensorflow.keras.applications.vgg16 import VGG16

print(os.listdir("../input/vgg16-weights"))


# In[38]:


from keras import applications
model = VGG16(input_tensor=image_input, include_top=True, weights='../input/vgg16-weights/vgg16_weights_tf_dim_ordering_tf_kernels.h5', )


# In[39]:


last_layer = model.get_layer('fc2').output
out = Dense(num_classes, activation='softmax', name='output')(last_layer)


# In[40]:


from tensorflow.keras.models import Model

custom_vgg_model = Model(image_input, out)
custom_vgg_model.summary()


# In[41]:


for layer in custom_vgg_model.layers[:-1]:
    layer.trainable = False


# In[42]:


custom_vgg_model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])


# In[43]:


num_epoch = 100
custom_vgg_model.fit(X_train, y_train, batch_size=512, epochs=num_epoch, verbose=1, validation_data=(X_test, y_test))


# In[44]:


from keras.models import load_model

custom_vgg_model.save('Image_Class_Cute5.h5')


# In[45]:


(loss, accuracy) = custom_vgg_model.evaluate(X_train, y_train, batch_size=batch_size, verbose=1)

print("[INFO] loss={:.4f}, accuracy: {:.4f}%".format(loss, accuracy * 100))


# In[46]:


Y_train_pred = custom_vgg_model.predict(X_test)


# In[47]:


y_train_pred = np.argmax(Y_train_pred, axis=1)
print(y_train_pred)


# In[48]:


from sklearn.metrics import classification_report,accuracy_score
print("test accuracy = ",accuracy_score(y_train_pred ,np.argmax(y_test, axis=1),))
#print("test accuracy = ",accuracy_score(y_pred,y_true))

