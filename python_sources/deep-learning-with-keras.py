#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import keras
from random import randint
import matplotlib.pyplot as plt


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


train_data=pd.read_csv('../input/train.csv')
test_data=pd.read_csv('../input/test.csv')
sub_sample=pd.read_csv('../input/sample_submission.csv')


# In[ ]:


train_data.head(10)


# In[ ]:


train_data.shape


# In[ ]:


test_data.head()


# In[ ]:


test_data.shape


# In[ ]:


sub_sample.head()


# In[ ]:


Y_train = train_data["label"]
Y_train = np.array(Y_train, np.uint8)


# In[ ]:


X_train = train_data.drop(labels = ["label"],axis = 1) 
X_train = np.array(X_train)
X_test=np.array(test_data)


# In[ ]:


print(X_train.shape)
print(Y_train.shape)
print(X_test.shape)
Y_train


# In[ ]:


# free memory space
del train_data


# ## Data Visualization

# In[ ]:


#Convert train datset to (num_images, img_rows, img_cols) format 
train_images = X_train.reshape(X_train.shape[0], 28, 28)


# In[ ]:


def plot_images(images, classes):
    assert len(images) == len(classes) == 9
    
    # Create figure with 3x3 sub-plots.
    fig, axes = plt.subplots(3, 3,figsize=(28,28),sharex=True)
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
   
    for i, ax in enumerate(axes.flat):
        # Plot image.
        
        ax.imshow(images[i], cmap=plt.get_cmap('gray'))    
        xlabel = "the number is: {0}".format(classes[i])
    
        # Show the classes as the label on the x-axis.
        ax.set_xlabel(xlabel)
        ax.xaxis.label.set_size(28)
        # Remove ticks from the plot.
        ax.set_xticks([])
        ax.set_yticks([])
    
    # Ensure the plot is shown correctly with multiple plots
    # in a single Notebook cell.
    
    plt.show()


# In[ ]:


random_numbers = [randint(0, len(train_images)) for p in range(0,9)]
images_to_show = [train_images[i] for i in random_numbers]
classes_to_show = [Y_train[i] for i in random_numbers]
print("Images to show: {0}".format(len(images_to_show)))
print("Classes to show: {0}".format(len(classes_to_show)))
#plot the images
plot_images(images_to_show, classes_to_show)


# * ## One Hot encoding 
# 
# **Encode labels to one hot vectors (ex : 4 ---> [0,0,0,0,1,0,0,0,0,0]   ,    9 ---> [0,0,0,0,0,0,0,0,0,1])**

# In[ ]:


from keras.utils.np_utils import to_categorical

Y_train= to_categorical(Y_train)


# In[ ]:


Y_train


# In[ ]:


Y_train.shape


# In[ ]:


#Splitting the train_images into the Training set and validation set
from sklearn.model_selection import train_test_split

X_train, X_val, Y_train, Y_val= train_test_split(X_train, Y_train,
               test_size=0.1, random_state=42,stratify=Y_train)


# In[ ]:


print(X_train.shape)
print(Y_train.shape)
print(X_val.shape)
print(Y_val.shape)
print(X_test.shape)


# In[ ]:


X_train = X_train.astype('float32')/255
X_val=X_val.astype('float32')/255
X_test = X_test.astype('float32')/255


# ## Define Model by keras

# In[ ]:


from keras.models import Sequential
from keras.layers import Dense ,Dropout
from keras.optimizers import SGD , RMSprop,Adam
from keras import regularizers
from keras.callbacks import LearningRateScheduler,ReduceLROnPlateau,ModelCheckpoint,EarlyStopping


# In[ ]:


def lr_schedule(epoch):
    lrate = 0.001
    if epoch > 50:
        lrate = 0.0003
    if epoch > 75:
        lrate = 0.00003
    elif epoch > 100:
        lrate = 0.000003       
    return lrate


# In[ ]:


lr_scheduler=LearningRateScheduler(lr_schedule)


# In[ ]:


#we can reduce the LR by half if the accuracy is not improved after 3 epochs.using the following code
reduceOnPlateau = ReduceLROnPlateau(monitor='val_acc', 
                                            patience=5, 
                                            verbose=1, 
                                            factor=0.5, 
                                            min_lr=0.00001, mode='auto')


# In[ ]:


#Save the model after every decrease in val_loss 
checkpoint = ModelCheckpoint(filepath='bestmodel.hdf5', verbose=0,monitor='val_loss',save_best_only=True,save_weights_only=False)


# In[ ]:


#Stop training when a monitored quantity has stopped improving.
earlyStopping=EarlyStopping(monitor='val_loss', min_delta=0, patience=3, verbose=0, mode='auto')


# In[ ]:


callbacks_list = [lr_scheduler,checkpoint]


# In[ ]:


model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(784,),kernel_regularizer=regularizers.l2(0.01)))
#model.add(Dropout(0.2))
model.add(Dense(128, activation='relu',kernel_regularizer=regularizers.l2(0.01)))
#model.add(Dropout(0.2))
model.add(Dense(64, activation='relu',kernel_regularizer=regularizers.l2(0.01)))
#model.add(Dropout(0.2))
model.add(Dense(10, activation='softmax'))


# In[ ]:


model.summary()


# In[ ]:


keras.utils.plot_model(model, to_file='model.png', show_shapes=False, show_layer_names=True, rankdir='LR', expand_nested=False, dpi=96)


# In[ ]:


sgd = SGD(lr=0.000002, decay=1e-6, momentum=0.9)
rmsprop = RMSprop(lr=0.001 ,decay=1e-4)
adam= Adam(lr=0.0003 ,decay=1e-4)

model.compile(optimizer=rmsprop,
                loss='categorical_crossentropy',
                metrics=['accuracy'])


# In[ ]:


H1= model.fit(X_train, Y_train, batch_size = 256, epochs = 100,callbacks=callbacks_list, 
              validation_data = (X_val, Y_val), verbose = 1)


# In[ ]:


plt.figure(0)
plt.plot(H1.history['acc'],'r')
plt.plot(H1.history['val_acc'],'g')
plt.xticks(np.arange(0, 101, 5.0))
plt.rcParams['figure.figsize'] = (14, 8)
plt.xlabel("Num of Epochs")
plt.ylabel("Accuracy")
plt.title("Training Accuracy vs Validation Accuracy")
plt.legend(['train','validation'])


# In[ ]:


plt.figure(1)
plt.plot(H1.history['loss'],'r')
plt.plot(H1.history['val_loss'],'g')
plt.xticks(np.arange(0, 101, 5.0))
plt.rcParams['figure.figsize'] = (14, 8)
plt.xlabel("Num of Epochs")
plt.ylabel("Loss")
plt.title("Training Loss vs Validation Loss")
plt.legend(['train','validation'])


# In[ ]:


score = model.evaluate(X_val, Y_val, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


# In[ ]:


from sklearn.metrics import classification_report

preds = model.predict_classes(X_val)
y_lable = [y.argmax() for y in Y_val]
print(classification_report(y_lable,preds))
preds1 = model.predict_classes(X_train)
ytr_lable = [y.argmax() for y in Y_train]
print(classification_report(ytr_lable,preds1))


# In[ ]:


# predict results
Test_perdect = model.predict(X_test)

# select the indix with the maximum probability
Test_perdect = np.argmax(Test_perdect,axis = 1)

Test_perdect = pd.Series(Test_perdect,name="Label")

submission1 = pd.concat([pd.Series(range(1,28001),name = "ImageId"),Test_perdect],axis = 1)

submission1.to_csv("submission1.csv",index=False)


# ## Using Dropout

# In[ ]:


keras.backend.clear_session() ## clear the previous model. 


# In[ ]:


model2 = Sequential()
model2.add(Dense(256, activation='relu', input_shape=(784,)))
model2.add(Dropout(0.2))
model2.add(Dense(128, activation='relu'))
model2.add(Dropout(0.2))
model2.add(Dense(64, activation='relu'))
model2.add(Dropout(0.3))
model2.add(Dense(10, activation='softmax'))


# In[ ]:


model2.summary()


# In[ ]:


#Save the model after every decrease in val_loss 
checkpoint = ModelCheckpoint(filepath='bestmodel2.hdf5', verbose=0,monitor='val_loss',save_best_only=True,save_weights_only=False)


# In[ ]:


callbacks_list = [reduceOnPlateau,checkpoint]


# In[ ]:


adam= Adam(lr=0.001 ,decay=1e-4)
model2.compile(optimizer=adam,
                loss='categorical_crossentropy',
                metrics=['accuracy'])


# In[ ]:


H2= model2.fit(X_train, Y_train, batch_size = 256, epochs = 100, callbacks=callbacks_list, 
              validation_data = (X_val, Y_val), verbose = 1)


# In[ ]:


plt.figure(0)
plt.plot(H2.history['acc'],'r')
plt.plot(H2.history['val_acc'],'g')
plt.xticks(np.arange(0, 101, 5.0))
plt.rcParams['figure.figsize'] = (14, 8)
plt.xlabel("Num of Epochs")
plt.ylabel("Accuracy")
plt.title("Training Accuracy vs Validation Accuracy")
plt.legend(['train','validation'])


# In[ ]:


plt.figure(1)
plt.plot(H1.history['loss'],'r')
plt.plot(H1.history['val_loss'],'g')
plt.xticks(np.arange(0, 101, 5.0))
plt.rcParams['figure.figsize'] = (14, 8)
plt.xlabel("Num of Epochs")
plt.ylabel("Loss")
plt.title("Training Loss vs Validation Loss")
plt.legend(['train','validation'])


# In[ ]:


score = model2.evaluate(X_val, Y_val, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


# In[ ]:


preds = model2.predict_classes(X_val)
y_lable = [y.argmax() for y in Y_val]
print(classification_report(y_lable,preds))
preds1 = model2.predict_classes(X_train)
ytr_lable = [y.argmax() for y in Y_train]
print(classification_report(ytr_lable,preds1))


# In[ ]:


# predict results
Test_perd = model2.predict(X_test)

# select the indix with the maximum probability
Test_perd = np.argmax(Test_perd,axis = 1)

Test_perd = pd.Series(Test_perd,name="Label")

submission2 = pd.concat([pd.Series(range(1,28001),name = "ImageId"),Test_perd],axis = 1)

submission2.to_csv("submission2.csv",index=False)


# In[ ]:




