#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import os
import pandas as pd
#import tensorflow as tf

# To plot pretty figures
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


# ### Exploring the data

# In[ ]:


from IPython.display import display, Image


# In[ ]:


train_df = pd.read_csv('../input/train.csv')
submission_df = pd.read_csv('../input/sample_submission.csv')


# In[ ]:


train_df.head()


# In[ ]:


train_df.info()


# In[ ]:


train_df.describe()


# In[ ]:


train_df['has_cactus'].value_counts()


# In[ ]:


train_df.hist()


# In[ ]:


print("Number of rows in submission/test set: %d"%(len(submission_df)))


# In[ ]:


train_dir = "../input/train/train/"


# In[ ]:


im = Image(os.path.join(train_dir,train_df.iloc[0,0]), height=200, width=200)
display(im)


# In[ ]:


image = plt.imread(os.path.join(train_dir,train_df.iloc[0,0]))
image.shape


# In[ ]:


def grid_display(list_of_images, list_of_titles=[], no_of_columns=2, figsize=(10,10)):

    fig = plt.figure(figsize=figsize)
    column = 0
    for i in range(len(list_of_images)):
        column += 1
        #  check for end of column and create a new figure
        if column == no_of_columns+1:
            fig = plt.figure(figsize=figsize)
            column = 1
        fig.add_subplot(1, no_of_columns, column)
        plt.imshow(list_of_images[i])
        plt.axis('off')
        if len(list_of_titles) >= len(list_of_images):
            plt.title(list_of_titles[i])


# In[ ]:


list_of_images = []
list_of_titles = []

for i in range(21):
    list_of_images.append(plt.imread(os.path.join(train_dir,train_df.iloc[i,0])))
    list_of_titles.append('is a cactus: {}'.format(train_df.iloc[i,1]))

grid_display(list_of_images, list_of_titles, no_of_columns= 7, figsize = (15,15))


# ### Generating train and validation sets

# In[ ]:


from keras.preprocessing.image import ImageDataGenerator


# In[ ]:


datagen = ImageDataGenerator(rescale=1./255,validation_split=0.2,shear_range=0.2,
                             zoom_range=0.2,horizontal_flip=True)


# In[ ]:


print('size train: {}, size validation: {}'.format(17500*0.8, 17500*0.2))


# In[ ]:


train_df.has_cactus=train_df.has_cactus.astype(str)


# In[ ]:


train_generator = datagen.flow_from_dataframe(dataframe=train_df, directory=train_dir, subset='training', 
                                              x_col='id', y_col='has_cactus', class_mode='binary', 
                                              batch_size= 140, target_size=(32,32))


validation_generator = datagen.flow_from_dataframe(dataframe=train_df, directory=train_dir, subset='validation', 
                                                   x_col='id', y_col='has_cactus', class_mode='binary', 
                                                   batch_size= 35, target_size=(32,32))


# ### CNN model

# In[ ]:


from keras.models import Sequential
from keras.layers import Convolution2D,Dense,Flatten,Dropout,MaxPool2D


# In[ ]:


model = Sequential()


# In[ ]:


model.add(Convolution2D(32, (3,3), activation='relu', input_shape=(32,32,3)))
model.add(Convolution2D(32, (3,3), activation='relu'))
model.add(MaxPool2D(2,2))
model.add(Convolution2D(64, (3,3), activation='relu'))
model.add(Convolution2D(64, (3,3), activation='relu'))
model.add(MaxPool2D(2,2))
model.add(Convolution2D(128, (3,3), activation='relu'))
model.add(MaxPool2D(2,2))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))


# In[ ]:


model.summary()


# In[ ]:


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


# In[ ]:


history = model.fit_generator(train_generator, steps_per_epoch=400, epochs=10, 
                              validation_data=validation_generator, validation_steps=100)


# ### Learning Curves

# In[ ]:


def plot_LC(history):
    loss=history.history['loss']    ##getting  loss of each epochs
    n_epochs = len(loss)
    epochs_=range(0,n_epochs)
    plt.plot(epochs_,loss,label='training loss')
    plt.xlabel('No of epochs')
    plt.ylabel('loss')

    acc_val=history.history['val_loss']  ## getting validation loss of each epochs
    plt.scatter(epochs_,acc_val,label="validation loss")
    plt.title('No of epochs vs loss')
    plt.legend()
    plt.show()


# In[ ]:


def plot_acc(history):
    acc=history.history['acc']  ##getting  accuracy of each epochs
    n_epochs = len(acc)
    epochs_=range(0,n_epochs)    
    plt.plot(epochs_,acc,label='training accuracy')
    plt.xlabel('No of epochs')
    plt.ylabel('accuracy')

    acc_val=history.history['val_acc']  ##getting validation accuracy of each epochs
    plt.scatter(epochs_,acc_val,label="validation accuracy")
    plt.title("No of epochs vs accuracy")
    plt.legend()
    plt.show()


# In[ ]:


plot_LC(history)


# In[ ]:


plot_acc(history)


# ### Predictions and submission

# In[ ]:


from tqdm import tqdm

test_path = "../input/test/test/"
test_images_names = []

for filename in os.listdir(test_path):
    test_images_names.append(filename)

test_images_names.sort()

images_test = []

for image_id in tqdm(test_images_names):
    images_test.append(np.array(plt.imread(test_path + image_id)))
    
images_test = np.asarray(images_test)
images_test = images_test.astype('float32')
images_test /= 255


# In[ ]:


predict_proba = model.predict(images_test).reshape(-1)


# In[ ]:


predict_proba[:5]


# In[ ]:


predict = (predict_proba >= 0.5)*1


# In[ ]:


predict[:5]


# In[ ]:


submission_df['has_cactus'] = predict_proba
submission_df.to_csv('submission_cnn_04.csv',index = False)


# In[ ]:




