#!/usr/bin/env python
# coding: utf-8

# # This kernel use simple transfer learning to detect ship exist or not
# *** For biginner, can get about 85% accuracy train on 10 epoch (~20min one epoch no GPU, ~100s one epoch have GPU)**
# * Use ResNet50 to do transfer learning 
# * Load 5000 picture to be training data 
# * Split 4000 training set , 1000 validate set  (0.2%)
# * Image size 256 x 256, RGB data
# * Using ImageGenerator to do data augumatation

# ## Load segmentation file

# In[ ]:


import os
import gc
print(os.listdir("../input"))
import numpy as np 
import pandas as pd
import time


# In[ ]:


train = pd.read_csv('../input/train_ship_segmentations_v2.csv')


# In[ ]:


train.head()


# ## Tranfer EncodedPixels to target 
# * have ship ==> 1
# * No ship ==> 0

# In[ ]:


train['exist_ship'] = train['EncodedPixels'].fillna(0)
train.loc[train['exist_ship']!=0,'exist_ship']=1
del train['EncodedPixels']


# ## We found there are some duplicate image in training data
# * groupby duplicate image 

# In[ ]:


print(len(train['ImageId']))
print(train['ImageId'].value_counts().shape[0])
train_gp = train.groupby('ImageId').sum().reset_index()
train_gp.loc[train_gp['exist_ship']>0,'exist_ship']=1


# ## Balance have chip and no chip data
# * Remove 100000 data of no chip

# In[ ]:


print(train_gp['exist_ship'].value_counts())
train_gp= train_gp.sort_values(by='exist_ship')
train_gp = train_gp.drop(train_gp.index[0:100000])


# ## Set Training set count
# * prevent large data cause much time 

# In[ ]:


print(train_gp['exist_ship'].value_counts())
train_sample = train_gp.sample(5000)
print(train_sample['exist_ship'].value_counts())
print (train_sample.shape)


# ## Load training data function
# * load training data to numpy array for training 

# In[ ]:


Train_path = '../input/train_v2/'
Test_path = '../input/test_v2/'


# In[ ]:


get_ipython().run_cell_magic('time', '', "training_img_data = []\ntarget_data = []\nfrom PIL import Image\ndata = np.empty((len(train_sample['ImageId']),256, 256,3), dtype=np.uint8)\ndata_target = np.empty((len(train_sample['ImageId'])), dtype=np.uint8)\nimage_name_list = os.listdir(Train_path)\nindex = 0\nfor image_name in image_name_list:\n    if image_name in list(train_sample['ImageId']):\n        imageA = Image.open(Train_path+image_name).resize((256,256)).convert('RGB')\n        data[index]=imageA\n        data_target[index]=train_sample[train_gp['ImageId'].str.contains(image_name)]['exist_ship'].iloc[0]\n        index+=1\n        \nprint(data.shape)\nprint(data_target.shape)")


# ## Doing One hot on target
# * Set target to one hot target for classification problem

# In[ ]:


from sklearn.preprocessing import OneHotEncoder
targets =data_target.reshape(len(data_target),-1)
enc = OneHotEncoder()
enc.fit(targets)
targets = enc.transform(targets).toarray()
print(targets.shape)


# ## Split Training data to training data and validate data to detect overfit 

# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(data,targets, test_size = 0.2)
x_train.shape, x_val.shape, y_train.shape, y_val.shape


# ## Data augumatation
# * Using ImageDataGenerator

# In[ ]:


from keras.preprocessing.image import ImageDataGenerator
img_gen = ImageDataGenerator(
    rescale=1./255,
    zca_whitening = False,
    rotation_range = 90,
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    brightness_range = [0.5, 1.5],
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True,
    vertical_flip = True
    
)


# ## Load ResNet50 model with Keras
# * on Kaggle kernel, please turn on the internet setting to Internet connect  on right window

# In[ ]:


#from keras.applications.vgg16 import VGG16 as PTModel, preprocess_input
#from keras.applications.densenet import DenseNet169 as PTModel, preprocess_input
from keras.applications.resnet50 import ResNet50 as ResModel
#from keras.applications.vgg16 import VGG16 as VGG16Model
img_width, img_height = 256, 256
model = ResModel(weights = 'imagenet', include_top=False, input_shape = (img_width, img_height, 3))


# ## Add fully connect layer
# * Freeze convolution layer and add fully connect layer
# * On this case, we only need predict 2 category (1. have ship, 2. no ship)
# * For transfer learning, we only need to train parametric on fully connect layer

# In[ ]:


from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
from keras.models import Sequential, Model 
for layer in model.layers:
    layer.trainable = False

x = model.output
x = Flatten()(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(1024, activation="relu")(x)
predictions = Dense(2, activation="softmax")(x)

# creating the final model 
model_final = Model(input = model.input, output = predictions)


# ##  Set Hyperparameter and Start training 
# * SGD optimizer
# * Using categorical_crossentropy to be loss function
# * lrate set to 0.001 (Maybe we have better value, In here, I have no experence on this)

# In[ ]:


from keras import optimizers
epochs = 10
lrate = 0.001
decay = lrate/epochs
#adam = optimizers.Adam(lr=lrate,beta_1=0.9, beta_2=0.999, decay=decay)
sgd = optimizers.SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model_final.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
model_final.summary()


# In[ ]:


model_final.fit_generator(img_gen.flow(x_train, y_train, batch_size = 16),steps_per_epoch = len(x_train)/16, validation_data = (x_val,y_val), epochs = epochs )
model_final.save('ResNet_transfer_ship.h5')


# In[ ]:


gc.collect()


# ## Predict accuracy by random read training data

# * Get random 2000 data from training set

# In[ ]:


train_predict_sample = train_gp.sample(2000)
print(train_predict_sample['exist_ship'].value_counts())


# * Load predict data 

# In[ ]:


get_ipython().run_cell_magic('time', '', "from PIL import Image\ndata_predict = np.empty((len(train_predict_sample['ImageId']),256, 256,3), dtype=np.uint8)\ndata_target_predict = np.empty((len(train_predict_sample['ImageId'])), dtype=np.uint8)\nimage_name_list = os.listdir(Train_path)\nindex = 0\nfor image_name in image_name_list:\n    if image_name in list(train_predict_sample['ImageId']):\n        imageA = Image.open(Train_path+image_name).resize((256,256)).convert('RGB')\n        data_predict[index]=imageA\n        data_target_predict[index]=train_predict_sample[train_gp['ImageId'].str.contains(image_name)]['exist_ship'].iloc[0]\n        index+=1\n        \nprint(data_predict.shape)\nprint(data_target_predict.shape)")


# * Do one hot for predict target

# In[ ]:


from sklearn.preprocessing import OneHotEncoder
targets_predict =data_target_predict.reshape(len(data_target_predict),-1)
enc = OneHotEncoder()
enc.fit(targets_predict)
targets_predict = enc.transform(targets_predict).toarray()
print(targets_predict.shape)


# * Evaluate predict

# In[ ]:


predict_ship = model_final.evaluate(data_predict,targets_predict)


# * Result

# In[ ]:


print ('Accuracy of random data = '+ str(round(predict_ship[1]*100)) + "%")


# In[ ]:


image_test_name_list = os.listdir(Test_path)
data_test = np.empty((len(image_test_name_list),256, 256,3), dtype=np.uint8)
test_name = []
index = 0
for image_name in image_test_name_list:
    imageA = Image.open(Test_path+image_name).resize((256,256)).convert('RGB')
    test_name.append(image_name)
    data_test[index]=imageA
    index+=1
print (data_test.shape)


# In[ ]:


result = model_final.predict(data_test)


# In[ ]:


result_list={
    "ImageId": test_name,
    "Have_ship":np.argmax(result,axis=1)
}
result_pd = pd.DataFrame(result_list)
result_pd.to_csv('Have_ship_or_not.csv',index = False)


# ## Conclution
# *  We can use tranfer learning to detect ship or not , and get higher accuracy on it 
# *  If we get 95% accuracy up, we can merge it with Unet model to produce a final submission
# *  Like Iafoss kernel: https://www.kaggle.com/iafoss/fine-tuning-resnet34-on-ship-detection/notebook
