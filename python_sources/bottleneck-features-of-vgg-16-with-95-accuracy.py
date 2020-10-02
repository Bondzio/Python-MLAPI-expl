#!/usr/bin/env python
# coding: utf-8

# In this kernel, I am going to build a model using VGG-16 bottleneck features.  When we say that we are going to use bottleneck features of a pre-trained model like VGG-16, we mean that we are going to remove the final layers of the VGG-16 model i.e. we are going to remove the high level classification layers(specific to the VGG 16 model labels). We will then pass our training and validation data through this model once and record the output into two arrays (one for training set and one for validation set) which are the bottleneck features for training and validation data. It is basically extracting patterns out of our dataset using the VGG-16 architecture. Then, we train a small fully connected model on top of these features. Let's get started !
# 
# In this dataset, we have a total of 55244 images which are divided into two folders - training set of 41322 images and testing set of 13877 images. The size of the given images is 100 * 100. We have 81 classes of fruits. Let's get started!
# 

# In[ ]:


import numpy as np  
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img  
from keras.models import Sequential  
from keras.layers import GlobalAveragePooling2D, Dense
from keras import applications  
from keras.utils.np_utils import to_categorical  
import matplotlib.pyplot as plt  
import math 


# In[ ]:


# dimensions of our image  
img_width, img_height = 100, 100  
   
top_model_weights_path = 'bottleneck_fruits_model.h5'  
train_data_dir = '../input/fruits-360_dataset/fruits-360/Training'  
validation_data_dir = '../input/fruits-360_dataset/fruits-360/Test'  
    
epochs = 20  # number of epochs to train top model 
batch_size = 16  


# In[ ]:


# save bottleneck features
model = applications.VGG16(include_top=False, weights='imagenet')  
    
datagen = ImageDataGenerator(rescale=1. / 255) 
    
generator = datagen.flow_from_directory(  
     train_data_dir,  
     target_size=(img_width, img_height),  
     batch_size=batch_size,  
     class_mode=None,  
     shuffle=False)  
    
nb_train_samples = len(generator.filenames)  
    
predict_size_train = int(math.ceil(nb_train_samples / batch_size)) 
    
bottleneck_features_train = model.predict_generator(  
     generator, predict_size_train) 
    
print(bottleneck_features_train.shape)
    
np.save('bottleneck_features_train.npy', bottleneck_features_train) 
    
    
    
generator = datagen.flow_from_directory(  
     validation_data_dir,  
     target_size=(img_width, img_height),  
     batch_size=batch_size,  
     class_mode=None,  
     shuffle=False)  
    
nb_validation_samples = len(generator.filenames)  
predict_size_validation = int(math.ceil(nb_validation_samples / batch_size))  
    
bottleneck_features_validation = model.predict_generator(  
    generator, predict_size_validation)  

print(bottleneck_features_validation.shape)
    
np.save('bottleneck_features_validation.npy', bottleneck_features_validation)


# In[ ]:


#extract bottleneck features for training
from keras.callbacks import ModelCheckpoint

datagen_top = ImageDataGenerator(rescale=1./255) 
    
generator_top = datagen_top.flow_from_directory(  
         train_data_dir,  
         target_size=(img_width, img_height),  
         batch_size=batch_size,  
         class_mode='categorical',  
         shuffle=False)  
    
    
nb_train_samples = len(generator_top.filenames)  
num_classes = len(generator_top.class_indices)  
    
# load the bottleneck features saved earlier  
train_data = np.load('bottleneck_features_train.npy')  
    
# get the class labels for the training data, in the original order  
train_labels = generator_top.classes
    
# convert the training labels to categorical vectors  
train_labels = to_categorical(train_labels, num_classes=num_classes)  
train_labels[0] # array of 81 elements


# In[ ]:


#extract bottleneck features for validation
generator_top = datagen_top.flow_from_directory(  
         validation_data_dir,  
         target_size=(img_width, img_height),  
         batch_size=batch_size,  
         class_mode=None,  
         shuffle=False)  
nb_validation_samples = len(generator_top.filenames)  
validation_data = np.load('bottleneck_features_validation.npy')  
    
validation_labels = generator_top.classes  
validation_labels = to_categorical(validation_labels, num_classes=num_classes) 
validation_labels.shape
validation_labels[0] # array of 81 elements


# In[ ]:


#build the top model and start training

checkpointer = ModelCheckpoint('best_model.hdf5',save_best_only = True,verbose = 1)
    
model = Sequential()  
# NOTE the shape given is the shape of the train_data saved in bottleneck features
model.add(GlobalAveragePooling2D(input_shape=train_data.shape[1:]))
model.add(Dense(81, activation='softmax'))
model.summary()
    
model.compile(optimizer='rmsprop',  
              loss='categorical_crossentropy', metrics=['accuracy']) 
    
history = model.fit(train_data, train_labels,  
          epochs=epochs,  
          batch_size=batch_size,  
          validation_data=(validation_data, validation_labels),
          callbacks = [checkpointer])  
    
model.load_weights('best_model.hdf5')
    
(eval_loss, eval_accuracy) = model.evaluate(  
     validation_data, validation_labels, batch_size=batch_size, verbose=1)

print("[INFO] accuracy: {:.2f}%".format(eval_accuracy * 100))  
print("[INFO] Loss: {}".format(eval_loss))


# We have got validation accuracy of ~95% in just 20 epochs using VGG-16 bottleneck features. We can visualize the loss and accuracy wrt epochs with graph below.

# In[ ]:


import matplotlib.pyplot as plt 
plt.figure(1)  
   
 # summarize history for accuracy  
   
plt.subplot(211)  
plt.plot(history.history['acc'])  
plt.plot(history.history['val_acc'])  
plt.title('model accuracy')  
plt.ylabel('accuracy')  
plt.xlabel('epoch')  
plt.legend(['train', 'test'], loc='upper left')  
   
 # summarize history for loss  
   
plt.subplot(212)  
plt.plot(history.history['loss'])  
plt.plot(history.history['val_loss'])  
plt.title('model loss')  
plt.ylabel('loss')  
plt.xlabel('epoch')  
plt.legend(['train', 'test'], loc='upper left')  
plt.show()

