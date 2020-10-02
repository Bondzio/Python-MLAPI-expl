#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import Sequential


# In[ ]:


model = Sequential()


# In[ ]:


#inputlayer : apply filters
model.add(Convolution2D(filters=32, 
                        kernel_size=(3,3), 
                        activation='relu',
                   input_shape=(64, 64, 3)
                       ))


# In[ ]:


# pooling layer where we are doing maxpooling
model.add(MaxPooling2D(pool_size=(2, 2)))


# In[ ]:


#modification for increasing accuracy
model.add(Convolution2D(filters=32, 
                        kernel_size=(3,3), 
                        activation='relu',
                       ))


# In[ ]:


#modification for increasing accuracy
model.add(MaxPooling2D(pool_size=(2, 2)))


# In[ ]:


#layer inwhich we areconverting 2d/3d image to 1d image i.e flattening
model.add(Flatten())


# In[ ]:


# layer: appling relu to give positive output
# from here our hidden layerrs starts
model.add(Dense(units=128, activation='relu'))


# In[ ]:


#output layer : to provide binary output using sigmoid function
model.add(Dense(units=6, activation='softmax'))


# In[ ]:


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# In[ ]:


from keras_preprocessing.image import ImageDataGenerator


# In[ ]:





# In[ ]:


#image augmentation
#url : https://keras.io/api/preprocessing/image/ 
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)
training_set = train_datagen.flow_from_directory(
        '../input/intel-image-classification/seg_train/seg_train/',
        target_size=(64,64),
        batch_size=32,
        class_mode='categorical')
test_set = test_datagen.flow_from_directory(
        '../input/intel-image-classification/seg_test/seg_test/',
        target_size=(64,64),
        batch_size=32,
        class_mode='categorical')


# In[ ]:


training_set.class_indices # to see classes of our dataset


# In[ ]:


model.fit(
        training_set,
        steps_per_epoch=2300,
        epochs=10,
        validation_data=test_set,
        validation_steps=12000)


# In[ ]:


import matplotlib.pyplot as plt 


# In[ ]:


def plot_accuracy_loss(history):
    """
        Plot the accuracy and the loss during the training of the nn.
    """
    fig = plt.figure(figsize=(10,5))

    # Plot accuracy
    plt.subplot(221)
    plt.plot(history.history['acc'],'bo--', label = "acc")
    plt.plot(history.history['val_acc'], 'ro--', label = "val_acc")
    plt.title("train_acc vs val_acc")
    plt.ylabel("accuracy")
    plt.xlabel("epochs")
    plt.legend()

    # Plot loss function
    plt.subplot(222)
    plt.plot(history.history['loss'],'bo--', label = "loss")
    plt.plot(history.history['val_loss'], 'ro--', label = "val_loss")
    plt.title("train_loss vs val_loss")
    plt.ylabel("loss")
    plt.xlabel("epochs")

    plt.legend()
    plt.show()


# In[ ]:


plot_accuracy_loss(history)


# In[ ]:


#model.save("new-cnn-placeimage_model.h5")   #save model


# In[ ]:


#from keras.models import load_model
#model=load_model("cnn-intel-image-model.h5")  #load model  <- this has run on 3 epochs with ~85% accuracy


# In[ ]:


#from keras.preprocessing import image


# In[ ]:


#test_image = image.load_img("'../input/intel-image-classification/seg_pred/seg_pred/14.jpg",target_size=(64,64))


# In[ ]:


#test_image #since this format is PIL or pillow so it can be printed


# In[ ]:


#test_image = image.img_to_array(test_image)  #convert PIL image to numpy array


# In[ ]:


#import numpy as np


# In[ ]:


#test_image = np.expand_dims(test_image,axis=0)
#since keras uses tensor flow and for tensorflow it needs 4d image so we converted 3d image to 4d image using above


# In[ ]:


#result = model.predict(test_image)


# In[ ]:


#result


# In[ ]:


"""if result[0][0]==1:
    print("Buildings")
elif result[0][1]==1:
    print("Forest")
elif result[0][2]==1:
    print("Glacier")
elif result[0][3]==1:
    print("Mountain")
elif result[0][4]==1:
    print("Sea")
else:
    print("Street")
    """


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




