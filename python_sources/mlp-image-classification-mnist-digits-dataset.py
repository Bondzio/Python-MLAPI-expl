#!/usr/bin/env python
# coding: utf-8

# ## Image Recognition using MLP for the MNIST digits dataset
# 
# ### by Ayrton Casella 

# In[13]:


# Import the Libraries
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import matplotlib.pyplot as plt
import numpy as np
from pandas import read_csv

from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import confusion_matrix

import tensorflow as tf                                    # Tensorflow also can perform ANN
import keras
from keras.models import Sequential, load_model            # ANN from keras
from keras.layers import Dense, Flatten

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Function to unflatten the images, in other words, to transform a lot of vectors (LxM*N) into a matrix (LxMxN)
def unflatten_images(matriz):
    L, C = matriz.shape
    images = np.zeros([L, 28, 28])
    for n in range(0, L):
        images[n, :, :] = matriz[n, :].reshape(28, 28)
    return images


# In[11]:


"""
Function to one_hot_encode the labels which are in a decimal format, in other words, 
to transform a number from (0 to 10) into a binary array (1x10) 

e.g.:

5 => [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

"""
def one_hot_labels(labels):
    labels = np.array([list(labels)]).T
    ohc = OneHotEncoder(categorical_features = [0])
    labels = ohc.fit_transform(labels).toarray()
    return labels


# In[12]:


# Reading Train and Test data from csv files 

dataTrain = read_csv('../input/Train.csv').values
dataTest = read_csv('../input/Test.csv').values


# Spliting data and classes, and one_hot_encoding the Train and Test labels

imTrain = dataTrain[:, :-1] # Getting the data
train_labels = dataTrain[:, -1] # Getting the classes
labelTrain = one_hot_labels(train_labels) # One hot encode to the classes

imTest = dataTest[:, :-1] # Getting the data
test_labels = dataTest[:, -1] # Getting the classes
labelTest = one_hot_labels(test_labels) # One hot encode to the classes

L, N = imTrain.shape


# OK, so now we've got the following variables:
# 
# - train_labels: Vector (60000x1) with each label image in its indexes. 
# - test_labels: Vector (10000x1) with each label image in its indexes. 
# - imTrain: Matrix (60000x784) with each train image in its rows.
# - labelTrain: Matrix (60000x10) with each label image in its rows.
# - imTest: Matrix (10000x784) with each test image in its rows.
# - labelTest: Matrix (60000x10) with each test label in its rows.

# Here's the deal, we will build this neural network using the Keras framework:

# ### Let's begin by building the model
# 
# We define a sequential model for our Multi Layer Perceptron. Then we add a hidden layer with 100 neurons (100 is kind of random) and we specify "relu" activation function, following by the output layer with 10 neurons and the "softmax" activation function. Both layers have their weigths initialized with random numbers from a uniform distribution.

# In[ ]:


# Build the model
classificador = Sequential()
classificador.add(Dense(units=100, kernel_initializer='uniform', activation='relu', input_dim=N))
classificador.add(Dense(units=10, kernel_initializer='uniform', activation='softmax'))

# Compile and fit the model
classificador.compile(optimizer='adam', loss = 'binary_crossentropy', metrics=['accuracy'])
classificador.fit(imTrain[:60000, :], labelTrain[:60000, :], validation_split=0.1, epochs=50, batch_size=200, verbose=1)

# Evaluate if the model is making good predictions or not
scores = classificador.evaluate(imTest, labelTest)
print('{}: {:.2f}%'.format(classificador.metrics_names[1], scores[1]*100))


# ### Now, we're gonna inspect  the results that were given

# In[ ]:


# Function to plot more than one image at a time
def plot_images(images):
    "Plot a list of MNIST images."
    fig, axes = plt.subplots(nrows=1, ncols=images.shape[0])
    for j, ax in enumerate(axes):
        img1 = images[j, :, :]
        ax.matshow(img1.reshape(28,28), cmap = plt.cm.binary)
        ax.set_xticks([])
        ax.set_yticks([])
    plt.show()


# In[ ]:


# Inspecting if the predictions are good
indexes = (33, 499, 2902, 7238, 1348, 8999, 9200, 3430, 9501, 6788)
resultados = classificador.predict(imTest[indexes, :])
final = []
corretos = []
for cont, n in enumerate(resultados):
    final.append(np.argmax(n))
    corretos.append(test_labels[indexes[cont]])
print('Predicted Results: {}'.format(final))
print('Correct Results:   {}'.format(corretos))

check_images = unflatten_images(imTest[indexes, :])

plot_images(check_images)


# ### We can plot the confusion matrix to see the whole accuracy of our model

# In[ ]:


# Function to plot the confusion matrix
def plot_confusion_matrix(Mconf, classes, title=None, normalize=False, cmap=plt.cm.Blues):
    """
    This function plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    plt.imshow(Mconf, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes, rotation=45)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = Mconf.max() / 2.
    for i in range(Mconf.shape[0]):
        for j in range(Mconf.shape[1]):
            plt.text(j, i, format(Mconf[i, j], fmt),
                    ha="center", va="center",
                    color="white" if Mconf[i, j] > thresh else "black")
    plt.tight_layout()


# In[ ]:


# Plotting the confusion matrix
resultados = classificador.predict_classes(imTest)
Mconf = confusion_matrix(test_labels, resultados)
classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
plot_confusion_matrix(Mconf, classes)


# ### Finally, we can save our model to use this configuration later

# In[ ]:


# Saving current model
classificador.save('mnist.h5')


# In[ ]:


# Loading previous trained model saved
new_model = load_model('mnist.h5')


# In[ ]:


# Summary of the trained model
new_model.summary()

