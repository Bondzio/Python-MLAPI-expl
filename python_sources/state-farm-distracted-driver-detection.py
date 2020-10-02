#!/usr/bin/env python
# coding: utf-8

# <H1>State Farm Distracted Driver Detection</H1>
# <h2>Importing Libraries</h2>

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import cv2 #opencv library
import glob
import matplotlib.pyplot as plt  #plotting library
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
import tensorflow
import random
from keras.callbacks import EarlyStopping
from PIL import Image
import h5py
import os
print(os.listdir("../input"))


# In[ ]:


directory = '../input/state-farm-distracted-driver-detection/train'
test_directory = '../input/state-farm-distracted-driver-detection/test/'
random_test = '../input/driver/'
classes = ['c0','c1','c2','c3','c4','c5','c6','c7','c8','c9']


# <h2>Loading the Training dataset</h2>

# In[ ]:


training_data = []
testing_data = []


# In[ ]:


# creating a training dataset.
#training_data = []
def create_training_data():
    for category in classes:
        path = os.path.join(directory,category)
        class_num = classes.index(category)
        
        for img in os.listdir(path):
            img_array = cv2.imread(os.path.join(path,img),cv2.IMREAD_GRAYSCALE)
            new_img = cv2.resize(img_array,(240,240))
            training_data.append([
                new_img,class_num])


# <h2> Loading Test dataset </h2>

# In[ ]:


# Creating a test dataset.
#testing_data = []
def create_testing_data():        
    for img in os.listdir(test_directory):
        img_array = cv2.imread(os.path.join(test_directory,img),cv2.IMREAD_GRAYSCALE)
        new_img = cv2.resize(img_array,(240,240))
        testing_data.append([img,
            new_img])


# In[ ]:


create_training_data()
create_testing_data()


# <h2> Count the number of images in each subdirectory </h2>

# In[ ]:


#Count the number of files in each subdirectory
def listDirectoryCounts(path):
    d = []
    for subdir, dirs, files in os.walk(path,topdown=False):
        filecount = len(files)
        dirname = subdir
        d.append((dirname,filecount))
    return d 

def SplitCat(df):
    for index, row in df.iterrows():
        directory=row['Category'].split('/')
        if directory[4]!='':
            directory=directory[4]
            df.at[index,'Category']=directory
        else:
            df.drop(index, inplace=True)
    return


#Get image count per category
dirCount=listDirectoryCounts("../input/state-farm-distracted-driver-detection/train/")
categoryInfo = pd.DataFrame(dirCount, columns=['Category','Count'])
SplitCat(categoryInfo)
categoryInfo=categoryInfo.sort_values(by=['Category'])
print(categoryInfo.to_string(index=False))


# In[ ]:


#Plotting class distribution
img_list = pd.read_csv('../input/state-farm-distracted-driver-detection/driver_imgs_list.csv')
img_list['class_type'] = img_list['classname'].str.extract('(\d)',expand=False).astype(np.float)
plt.figure()
img_list.hist('class_type',alpha=0.5,layout=(1,1),bins=9)
plt.title('class distribution')
plt.draw()


# <h2> Creating features and labels</h2>

# In[ ]:


random.shuffle(training_data)
x = []
y = []
for features, label in training_data:
    x.append(features)
    y.append(label)


# In[ ]:


x[0].shape


# <h3> Display training image </h3>

# In[ ]:


for i in classes:
    path = os.path.join(directory,i)
    for img in os.listdir(path):
        img_array = cv2.imread(os.path.join(path,img),cv2.IMREAD_COLOR)
        plt.imshow(img_array, cmap='gray')
        plt.show()
        break
    break


# In[ ]:



# load the image and show it
#image = cv2.imread('../input/train/c0/img_2380.jpg',cv2.IMREAD_COLOR)
image = mpimg.imread('../input/state-farm-distracted-driver-detection/train/c6/img_212.jpg',cv2.IMREAD_COLOR)
imgplot = plt.imshow(image)
plt.show()


# <h3> Label Encoding </h3>

# In[ ]:


y[0:20]


# In[ ]:


from keras.utils import np_utils
y_cat = np_utils.to_categorical(y,num_classes=10)


# In[ ]:


y_cat[0:10]


# In[ ]:


X = np.array(x).reshape(-1,240,240,1)
X[0].shape


# In[ ]:


X.shape


# <h3> Train/Test Split </h3>

# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y_cat,test_size=0.3,random_state=50)


# In[ ]:


print("Shape of train images is:", X_train.shape)
print("Shape of validation images is:", X_test.shape)
print("Shape of labels is:", y_train.shape)
print("Shape of labels is:", y_test.shape)


# <h2> Creating Model </h2>

# In[ ]:


batch_size = 32
from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array, load_img
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout,BatchNormalization


# model = models.Sequential()
# model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(240,240,1)))
# model.add(BatchNormalization())
# 
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(BatchNormalization())
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.5))
# 
# model.add(Conv2D(128, (5, 5), activation='relu'))
# model.add(BatchNormalization())
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.5))
# 
# #Dense
# model.add(Flatten())
# model.add(Dense(128, activation='relu'))
# model.add(BatchNormalization())
# model.add(Dropout(0.5))
# model.add(Dense(64, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(10, activation='softmax'))

# In[ ]:


model = models.Sequential()

## CNN 1
model.add(Conv2D(32,(3,3),activation='relu',input_shape=(240,240,1)))
model.add(BatchNormalization())
model.add(Conv2D(32,(3,3),activation='relu',padding='same'))
model.add(BatchNormalization(axis = 3))
model.add(MaxPooling2D(pool_size=(2,2),padding='same'))
model.add(Dropout(0.2))

## CNN 2
model.add(Conv2D(64,(3,3),activation='relu',padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(64,(3,3),activation='relu',padding='same'))
model.add(BatchNormalization(axis = 3))
model.add(MaxPooling2D(pool_size=(2,2),padding='same'))
model.add(Dropout(0.3))

## CNN 3
model.add(Conv2D(128,(3,3),activation='relu',padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(128,(3,3),activation='relu',padding='same'))
model.add(BatchNormalization(axis = 3))
model.add(MaxPooling2D(pool_size=(2,2),padding='same'))
model.add(Dropout(0.5))

## CNN 3
model.add(Conv2D(256,(5,5),activation='relu',padding='same'))
model.add(BatchNormalization(axis = 3))
model.add(MaxPooling2D(pool_size=(2,2),padding='same'))
model.add(Dropout(0.5))

## Dense & Output
model.add(Flatten())
model.add(Dense(units = 512,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(units = 128,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10,activation='softmax'))


# In[ ]:


model.summary()


# In[ ]:


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[ ]:


callbacks = [EarlyStopping(monitor='val_acc',patience=5)]


# <h3> Fit Model</h3>

# In[ ]:


results = model.fit(X_train,y_train,batch_size=batch_size,epochs=12,verbose=1,validation_data=(X_test,y_test),callbacks=callbacks)


# In[ ]:


model.save('C:\\Users\\sidsu\\Desktop\\Algorithms\\Project1.h5')


# In[ ]:


model.save('Project13.h5')


# In[ ]:


model_json = model.to_json()
with open("C:\\Users\\sidsu\\Desktop\\Algorithms\\model.json", "w") as json_file:
    json_file.write(model_json)


# <b><h2>Transfer Learning</h2></b>

# In[ ]:


#from keras.applications.resnet50 import ResNet50, preprocess_input
#from keras.preprocessing.image import ImageDataGenerator


# In[ ]:


#Loading the ResNet50 model with pre-trained ImageNet weights
#model = ResNet50(weights='imagenet', include_top=False, input_shape=(200, 200, 3))


# In[ ]:





# <H2> Data Augumentation </h2>

# In[ ]:


#First Augument
#train_datagen = ImageDataGenerator(rescale=1./255,   #Scale the image between 0 and 1
#                                    rotation_range=40,
#                                    width_shift_range=0.2,
#                                    height_shift_range=0.2,
#                                    shear_range=0.2,
#                                    zoom_range=0.2,
#                                    horizontal_flip=True,)
#
#val_datagen = ImageDataGenerator(rescale=1./255)


# In[ ]:


#train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size)
#val_generator = val_datagen.flow(X_val, y_val, batch_size=batch_size)


# #get the length of the train and validation data
# ntrain = len(X_train)
# print(ntrain)
# nval = len(X_test)
# nval

# In[ ]:


#FIRST MODEL
#history = model.fit_generator(train_generator,
#                              steps_per_epoch=ntrain // batch_size,
#                              epochs=4,
#                              validation_data=val_generator,
#                              validation_steps=nval // batch_size)


# In[ ]:


model.evaluate(X_test,y_test)


# In[ ]:


# Plot training & validation accuracy values
plt.plot(results.history['acc'])
plt.plot(results.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(results.history['loss'])
plt.plot(results.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()


# In[ ]:


preds = model.predict(np.array(testing_data[0][1]).reshape(-1,240,240,1))
preds


# In[ ]:


class_idx = np.argmax(preds)
class_idx


# In[ ]:


#class_output = model.output[:, class_idx]
#class_output


# In[ ]:


print('Predicted: {}'.format(np.argmax(preds)))
new_img = cv2.resize(testing_data[0][1],(240,240))
plt.imshow(new_img,cmap='gray')
plt.show()


# <H2>Model Interpretability </h2>

# image = mpimg.imread('../input/state-farm-distracted-driver-detection/test/img_8009.jpg',cv2.IMREAD_COLOR)
# imgplot = plt.imshow(image)
# plt.show()

# from keras.preprocessing import image
# import numpy as np
# 
# img_path = '../input/state-farm-distracted-driver-detection/test/img_8009.jpg'
# img_tensor = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
# new_img1 = cv2.resize(img_tensor,(240,240))
# x1 = np.array(new_img1).reshape(-1,240,240,1)
# print(x1.shape)

# img_tensor.shape

# from keras import models
# 
# # Extracts the outputs of the top 8 layers:
# layer_outputs = [layer.output for layer in model.layers[:7]]
# # Creates a model that will return these outputs, given the model input:
# activation_model = models.Model(inputs=model.input, outputs=layer_outputs)

# # This will return a list of 5 Numpy arrays:
# # one array per layer activation
# activations = activation_model.predict(x1)

# first_layer_activation = activations[0]
# print(first_layer_activation.shape)

# 
# import matplotlib.pyplot as plt
# 
# plt.matshow(first_layer_activation[0, :, :, 2], cmap='viridis')
# plt.show()

# In[ ]:


plt.matshow(first_layer_activation[0, :, :, 30], cmap='viridis')
plt.show()


# plt.matshow(first_layer_activation[0, :, :, 30], cmap='viridis')
# plt.show()

# plt.matshow(first_layer_activation[0, :, :, 30], cmap='viridis')
# plt.show()

# In[ ]:


#!pip install keras-vis


# In[ ]:


# import specific functions from keras-vis package
#from vis.utils import utils
#from vis.visualization import visualize_cam, overlay


# conv_layer

# import keras
# 
# # These are the names of the layers, so can have them as part of our plot
# layer_names = []
# for layer in model.layers[:15]:
#     layer_names.append(layer.name)
# 
# images_per_row = 16
# 
# # Now let's display our feature maps
# for layer_name, layer_activation in zip(layer_names, activations):
#     # This is the number of features in the feature map
#     n_features = layer_activation.shape[-1]
# 
#     # The feature map has shape (1, size, size, n_features)
#     size = layer_activation.shape[1]
# 
#     # We will tile the activation channels in this matrix
#     n_cols = n_features // images_per_row
#     display_grid = np.zeros((size * n_cols, images_per_row * size))
# 
#     # We'll tile each filter into this big horizontal grid
#     for col in range(n_cols):
#         for row in range(images_per_row):
#             channel_image = layer_activation[0,
#                                              :, :,
#                                              col * images_per_row + row]
#             # Post-process the feature to make it visually palatable
#             channel_image -= channel_image.mean()
#             channel_image /= channel_image.std()
#             channel_image *= 64
#             channel_image += 128
#             channel_image = np.clip(channel_image, 0, 255).astype('uint8')
#             display_grid[col * size : (col + 1) * size,
#                          row * size : (row + 1) * size] = channel_image
# 
#     # Display the grid
#     scale = 1. / size
#     plt.figure(figsize=(scale * display_grid.shape[1],
#                         scale * display_grid.shape[0]))
#     plt.title(layer_name)
#     plt.grid(False)
#     plt.imshow(display_grid, aspect='auto', cmap='viridis')
#     plt.savefig(layer_name)
#     
# plt.show()

# !pip install https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.2/imageai-2.0.2-py3-none-any.whl

# <H1>Object detection</H1>

# from imageai.Detection import ObjectDetection
# import os
# 
# execution_path = os.getcwd()
# print(execution_path)
# detector = ObjectDetection()
# detector.setModelTypeAsRetinaNet()
# detector.setModelPath( os.path.join('../input/resnet/', "resnet50_coco_best_v2.0.1.h5"))
# detector.loadModel()
# #detections = detector.detectObjectsFromImage(input_image=os.path.join('../input/state-farm-distracted-driver-detection/train/c0/' , "img_195.jpg"), output_image_path='D:/Springboard/state-farm-distracted-driver-detection/imgs/imagenew.jpg')
# returned_image,detections = detector.detectObjectsFromImage(input_image=os.path.join('../input/state-farm-distracted-driver-detection/train/c6/' , "img_212.jpg"), output_type = 'array')
# #print(returned_image)
# 
# for eachObject in detections:
#    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )

# from imageai.Detection import ObjectDetection
# import os
# 
# execution_path = os.getcwd()
# print(execution_path)
# detector = ObjectDetection()
# detector.setModelTypeAsRetinaNet()
# detector.setModelPath( os.path.join('../input/resnet/', "resnet50_coco_best_v2.0.1.h5"))
# detector.loadModel()
# #detections = detector.detectObjectsFromImage(input_image=os.path.join('../input/state-farm-distracted-driver-detection/train/c0/' , "img_195.jpg"), output_image_path='D:/Springboard/state-farm-distracted-driver-detection/imgs/imagenew.jpg')
# returned_image,detections = detector.detectObjectsFromImage(input_image=os.path.join('../input/state-farm-distracted-driver-detection/train/c6/' , "img_212.jpg"), output_type = 'array')
# #print(returned_image)
# 
# for eachObject in detections:
#    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
