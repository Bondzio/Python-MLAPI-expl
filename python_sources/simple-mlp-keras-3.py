#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import os
print(os.listdir("../input"))


# ### Load data

# In[ ]:


def load_train_data():
    return pd.read_csv('../input/quickdraw_train.csv', index_col='id')

def load_test_data():
    return pd.read_csv('../input/quickdraw_test_x.csv', index_col='id')


# In[ ]:


df_train = load_train_data()
df_train.shape


# In[ ]:


df_test = load_test_data()
df_test.shape


# #### Insight into data
# As you can see, there are 2 categories. These categories are not used as labels not are they in the test set. Is there a way to use them? Who knows, feel free to find out for yourself!

# In[ ]:


df_train['category'].unique()


# There are 42 different classes for the images, these are the labels that we aim to predict. In the training set there are 1000 images per class. The test set contains 500 images per class, 50% will be used for the public leaderboard, 50% will be used for the final score in the private leaderboard. Be aware that your score can thus change after the submission deadline.

# In[ ]:


df_train['subcategory'].unique()


# In[ ]:


df_train['subcategory'].value_counts().head()


# In[ ]:


def show_sample(df):
    fig = plt.figure(figsize=(28, 28)) 
    unique_samples = df.sample(df.shape[0]).drop_duplicates('subcategory').sort_values('subcategory').reset_index(drop=True)
    images_per_row = 8
    rows = int(np.ceil(unique_samples.shape[0] / images_per_row))
    for i, row in unique_samples.iterrows():
        plt.subplot(rows, images_per_row, i+1)
        im = row[:-2].astype(float).values 
        plt.title(f"{row[-1]} ({row[-2]})")
        plt.imshow(im.reshape([28,28]), cmap='gray', vmin=0, vmax=255, )
        frame1 = plt.gca()
        frame1.axes.get_xaxis().set_visible(False)
        frame1.axes.get_yaxis().set_visible(False)
        
def show_drawing(data):
    """
    Show a drawing from either a dataframe or a numpy array
    """
    if type(data) == type(pd.Series()):
        im = data[[f"pix{x}" for x in range(28*28)]].values.reshape((28,28)).astype(float)
        title = ''
        if 'subcategory' in data.index:
            title = f"{data['subcategory']} ({data['category']})"
    elif type(data) == type(np.zeros(1)): 
        im = data.reshape((28,28)).astype(float)
        title = ''
    else:
        print('ERROR: data not suitable: dataframe or numpy array supported')
        return

    plt.imshow(im, cmap='gray', vmin=0, vmax=255)
    plt.xticks([])
    plt.yticks([])
    plt.title(title)
    plt.show()
    


# In[ ]:


show_sample(df_train)


# ### to show that the images in the test set are similar

# In[ ]:


show_drawing(df_test.iloc[1])


# ## Example code for benchmark submission
# ## Simple Keras MLP from MNIST example 
# (https://github.com/keras-team/keras/blob/master/examples/mnist_mlp.py)

# In[ ]:


df_train.head()


# In[ ]:


import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, MaxPooling2D, Conv2D, Activation, Flatten
from keras.optimizers import RMSprop, Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.callbacks import EarlyStopping

from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense

batch_size = 128
num_classes = 42
epochs = 60


# ## Processing data

# In[ ]:


df_x = df_train.drop(['category', 'subcategory'], axis=1)
df_y = df_train[['subcategory']]


# ## Drop bad training data

# In[ ]:


tmp = df_x.copy() > 0
tmp = tmp.apply(lambda x: sum(x), axis = 1)


# In[ ]:


import seaborn as sns
sns.distplot(tmp)


# In[ ]:


good_train_data = tmp[(tmp >= 100) | tmp <= 400].keys()


# In[ ]:


df_x = df_x.loc[good_train_data]
df_y = df_y.loc[good_train_data]


# ### More cleaning data

# In[ ]:


# the data, split between train and test sets
x_train, x_test, y_train, y_test = train_test_split(df_x.values, df_y.values, test_size=0.1)

# floats!
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

#don't forget to normalize your data!
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
print('x_train shape:', x_train.shape)
print('x_test shape: ', x_test.shape)

# convert class vectors to binary class matrices
le = LabelEncoder()
y_train = le.fit_transform(y_train.flatten())
y_test  = le.transform(y_test.flatten())
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

print('y_train shape:', y_train.shape)
print('y_test shape: ', y_test.shape)


# ## Data augmentation
# 
# - flipping (horizontal)
# - zooming
# 
# https://medium.com/nybles/create-your-first-image-recognition-classifier-using-cnn-keras-and-tensorflow-backend-6eaab98d14dd
# 
# More on imager data generator of keras
# https://medium.com/@arindambaidya168/https-medium-com-arindambaidya168-using-keras-imagedatagenerator-b94a87cdefad
# 

# In[ ]:


def reshape_rgb_image(array):
    """
    From 768 to 28x28x1 
    
    samples * height * width * channels
    """
    array = np.reshape(np.copy(array), (-1, 28, 28))

    return array[:, :, :, np.newaxis]


reshape_rgb_image(x_test).shape


# In[ ]:


from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    #featurewise_center=True,
    #featurewise_std_normalization=True,
    #rotation_range=30,
    #width_shift_range=0.3,
    #height_shift_range=0.3,
    horizontal_flip=True
    )

train_datagen = train_datagen.flow(x = reshape_rgb_image(x_train), 
                                   y = y_train, batch_size = 64, seed = 42)

test_datagen = ImageDataGenerator()
test_datagen = test_datagen.flow(x = reshape_rgb_image(x_test), 
                                   y = y_test, 
                                   batch_size = 64, seed = 42)

#test_datagen = train_datagen.flow(reshape_rgb_image(x_test))
#train_datagen = train_datagen.flow(reshape_rgb_image(x_train), batch_size = 32)


# ### Specify the model architecture
# It contains two dense (feed-forward) neural network layers of each 512 hidden nodes, followed by a relu activation.

# In[ ]:


model = Sequential()

# first CONV => RELU => CONV => RELU => POOL layer set
model.add(Conv2D(32, (3, 3), padding="same",
    input_shape=(28,28,1)))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=-1))
model.add(Conv2D(32, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=-1))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

# second CONV => RELU => CONV => RELU => POOL layer set
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=-1))
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=-1))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

# first (and only) set of FC => RELU layers
model.add(Flatten())
model.add(Dense(512))
model.add(Activation("relu"))
model.add(BatchNormalization())
model.add(Dropout(0.3))

model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(Dropout(0.25))


# softmax classifier
model.add(Dense(num_classes))
model.add(Activation("softmax"))

# model.add(Conv2D(128, (3, 3), padding='same',
#                  input_shape=(28,28,1), activation = 'relu'))

# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

# model.add(Conv2D(64, (3, 3), activation = 'relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

# model.add(Conv2D(32, (3, 3), activation='relu'))
# model.add(Dropout(0.25))

# model.add(Flatten())
# model.add(Dense(128))
# model.add(Activation('relu'))

# model.add(Dropout(0.3))
# model.add(Dense(num_classes, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999 ),
              metrics=['accuracy'])

es = EarlyStopping(monitor='val_acc', mode='max', verbose=1, patience=0)

history = model.fit_generator(train_datagen,
                    epochs = epochs,
                    verbose=1,
                    steps_per_epoch = train_datagen.n // train_datagen.batch_size,
                    validation_data = test_datagen,
                    validation_steps = test_datagen.n // test_datagen.batch_size,
                    callbacks = [es]
                    )


# In[ ]:


score = model.evaluate(reshape_rgb_image(x_train), y_train, verbose=0)
print('Val loss:', score[0])
print('Val accuracy:', score[1])


# In[ ]:


score = model.evaluate(reshape_rgb_image(x_test), y_test, verbose=0)
print('Val loss:', score[0])
print('Val accuracy:', score[1])


# ### Now predict on the test set
# 1. Create a prediction
# 2. Save the prediction as submission file using the `create_submissiong()` method.
# 3. Upload on kaggle
# 4. Check your score and win!

# In[ ]:


clean_df_test = df_test.copy()
clean_df_test = clean_df_test.values 
clean_df_test = clean_df_test.astype('float32')
clean_df_test /= 255


# In[ ]:


predictions = model.predict(reshape_rgb_image(clean_df_test))
predictions = le.inverse_transform(np.argmax(predictions, axis=1))
np.unique(predictions, return_counts=True)


# In[ ]:


df_submission = df_test.copy()
df_submission['subcategory'] = predictions
df_submission = df_submission[['subcategory']]


# In[ ]:


def make_submission_file(df, filename='submission.csv'):
    assert 'subcategory' in df.columns, 'subcategory columns is missing'
    assert df.shape[0] == 21000, 'you should have 21000 rows in your submission file'
    df.to_csv(filename)


# In[ ]:


make_submission_file(df_submission, 'mlp_kernel_submission_3.csv')


# In[ ]:




