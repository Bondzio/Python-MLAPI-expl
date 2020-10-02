#!/usr/bin/env python
# coding: utf-8

# # Building a strong image classification model using keras

# ## importing libraries and constants for Preprocessing

# In[ ]:


import cv2                 # working with, mainly resizing, images
import numpy as np         # dealing with arrays
import os                  # dealing with directories
from random import shuffle # mixing up or currently ordered data that might lead our network astray in training.

train_dir = '../input/train'
test_dir = '../input/test'


# ## conversion to one-hot array for cat it is [1,0] and for dog it is [0,1]

# In[ ]:


def get_label(img):
    label = img.split('.')[0]
    if label == 'cat': 
        return [1,0]
    elif label == 'dog': 
        return [0,1]


# ## Building  another function to fully process the training images and their labels into arrays:-

# In[ ]:


from tqdm import tqdm      # a nice pretty percentage bar for tasks.

def making_train_data():
    training_data = []
    
    for img in tqdm(os.listdir(train_dir)):
        label = get_label(img)
        path = os.path.join(train_dir,img)
        img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (50,50))
        training_data.append([np.array(img),np.array(label)])
        
    shuffle(training_data)
    np.save('train_data.npy', training_data)
    return training_data


# In[ ]:


def making_test_data():
    testing_data = []
    
    for img in tqdm(os.listdir(test_dir)):
        path = os.path.join(test_dir , img)
        img_num = img.split('.')[0]
        img = cv2.imread(path , cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img , (50,50))
        testing_data.append([np.array(img), img_num])
        
    shuffle(testing_data)
    np.save('test_data.npy', testing_data)
    return testing_data


# In[ ]:


train_data = making_train_data()


# **Split the train_data into train(having 20,000 images) and test(having 5,000 images) **

# In[ ]:


train = train_data[0:20000]
test = train_data[20000:25000]


# In[ ]:


X = np.array([i[0] for i in train]).reshape(-1,1,50,50)
Y = [i[1] for i in train]

test_x = np.array([i[0] for i in test]).reshape(-1,1,50,50)
test_y = [i[1] for i in test]


# ## Data Augmentation to prevent Overfitting

# In[ ]:


from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
        featurewise_center=False,  
        samplewise_center=False,  
        featurewise_std_normalization=False,  
        samplewise_std_normalization=False,  
        zca_whitening=False,  
        rotation_range=10,  
        zoom_range = 0.0,  
        width_shift_range=0.1,  
        height_shift_range=0.1,  
        horizontal_flip=False, 
        vertical_flip=False)  

datagen.fit(X)


# In[ ]:


Y = np.asarray(Y)
Y.reshape(len(Y) , 2)


# In[ ]:


test_y = np.asarray(test_y)
test_y.reshape(len(test_y) , 2)


# In[ ]:


test_x = test_x.reshape(-1, 1, 50, 50)


# In[ ]:


test_x = test_x / 255
X = X / 255


# ****We will be using the Sequential model from Keras to form the Neural Network. Sequential Model is used to construct simple models with linear stack of layers.****
# 
# ****More info on Sequential model and Keras in general at https://keras.io/getting-started/sequential-model-guide/ and https://github.com/keras-team/keras****

# In[ ]:


from keras.models import Sequential
from keras.layers import Dense , Activation
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers import Convolution2D
from keras.layers import Conv2D , BatchNormalization
from keras.layers import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')


# ## Building the ConvNet Model

# In[ ]:


# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Convolution2D(32, 3, 3, input_shape = (1,50,50), activation = 'relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Convolution2D(32, 3, 3, activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))



# Adding a third convolutional layer
classifier.add(Convolution2D(64, 3, 3, activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))




# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(output_dim = 64, activation = 'relu'))
classifier.add(Dropout(0.4))
classifier.add(Dense(output_dim = 2, activation = 'sigmoid'))


# ## Compiling the Keras Model

# In[ ]:


# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


# ## Summary of the Model

# In[ ]:


classifier.summary()


# ## Fitting on the Training set and making predcitons on the Validation set

# In[ ]:


batch_size = 128
epochs = 20

classifier.compile(loss='binary_crossentropy', optimizer='adam' , metrics=['accuracy'])
steps_per_epoch = len(train_data) // batch_size
validation_steps = len((test_x, test_y)) // batch_size


# In[ ]:


history = classifier.fit_generator(datagen.flow(X, Y, batch_size=batch_size),
                    steps_per_epoch=X.shape[0] // batch_size,
                    validation_data=(test_x, test_y),
                    epochs = epochs, verbose = 2)


# In[ ]:


test_data = making_test_data()


# In[ ]:


score = classifier.evaluate(test_x, test_y, verbose=0)
print('valid loss:', score[0])
print('valid accuracy:', score[1])


# In[ ]:


with open('submission_file.csv','w') as f:
    f.write('id,label\n')
            
with open('submission_file.csv','a') as f:
    for data in tqdm(test_data):
        img_num = data[1]
        img_data = data[0]
        orig = img_data
        data = img_data.reshape(1,1,50,50)
        model_out = classifier.predict([data])[0]
        f.write('{},{}\n'.format(img_num,model_out[1]))


# In[ ]:


import pandas as pd
aa = pd.read_csv('submission_file.csv')
aa


# In[ ]:





# In[ ]:





# In[ ]:




