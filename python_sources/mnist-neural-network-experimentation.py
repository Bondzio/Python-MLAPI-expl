#!/usr/bin/env python
# coding: utf-8

# # MNIST - Neural Network Experimentation
# 
# Greetings! In this notebook, we experiment with various neural network configurations applied to the task of classifying MNIST digits. 
# 
# We start with a dense (fully connected) network and play with using different amounts of dropout to promote model generalization. Then we implement a LeNet-5-inspired convolutional neural network and experiment with additional conv blocks and a new activation function called Mish.
# 
# Thanks for reading and please leave a comment below if this helped you in your digit classification :)

# ### Load the Good Stuff

# In[ ]:


import pandas as pd
import numpy as np
import os, datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import keras
import tensorflow
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.optimizers import SGD
from keras.layers.normalization import BatchNormalization

# Load TensorBoard
from keras.callbacks import TensorBoard
get_ipython().run_line_magic('load_ext', 'tensorboard')

# Set plotting defaults
params = {'legend.fontsize': 'large',
          'figure.figsize': (10, 8),
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)
sns.set(style="white")

# Prevent Pandas from truncating displayed dataframes
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Seed randomness for reproducibility
from numpy.random import seed
SEED = 42
seed(SEED)
tensorflow.random.set_seed(SEED)


# ### Load the Data

# In[ ]:


# 10 digits
num_classes = 10

# Load master copies of data - these remain pristine
train_ = pd.read_csv("../input/digit-recognizer/train.csv")
test_ = pd.read_csv("../input/digit-recognizer/test.csv")
sample_submission = pd.read_csv("../input/digit-recognizer/sample_submission.csv")

# Take copies of the master dataframes
train = train_.copy()
test = test_.copy()

# Separate the target variable from the digits
y = train.pop("label")

# Scale the data to [0-1]
train = train / np.max(np.max(train))
test = test / np.max(np.max(test))


# ### Data Preprocessing

# In[ ]:


X_train, X_valid, y_train, y_valid = train_test_split(train, y, test_size=0.2, random_state=SEED)
y_train = keras.utils.to_categorical(y_train, num_classes=num_classes)
y_valid = keras.utils.to_categorical(y_valid, num_classes=num_classes)

y = keras.utils.to_categorical(y, num_classes=num_classes)

# For CNNs - reshape vector into 2D matrix
X_train_2D = X_train.values.reshape(-1,28,28,1) # Keras requires an extra dimension representing the image channel
X_valid_2D = X_valid.values.reshape(-1,28,28,1)
train_2D = train.values.reshape(-1,28,28,1)
test_2D = test.values.reshape(-1,28,28,1)


# ### Helper Functions

# In[ ]:


class NeuralNetwork():
    """Wrap neural network functions into a handy class."""
    
    def __init__(self, name, batch_size, epochs, optimizer, verbose):
        self.name = name
        self.batch_size = batch_size
        self.epochs = epochs
        self.verbose = verbose
        self.model = Sequential()
        self.optimizer = optimizer
        
    def add_(self, layer):
        self.model.add(layer)

    def compile_and_fit(self):
        self.model.compile(loss="categorical_crossentropy", optimizer=self.optimizer, metrics=["accuracy"])
        self.history = self.model.fit(x=X_train,
                                      y=y_train,
                                      batch_size=self.batch_size,
                                      epochs=self.epochs,
                                      verbose=self.verbose,
                                      validation_data=(X_valid, y_valid))
        self.val_loss = self.history.history["val_loss"]
        self.val_accuracy = self.history.history["val_accuracy"]
    
    def plot_learning_curves(self):
        fig, ax = plt.subplots(1, 2, figsize=(15, 5))
        
        sns.lineplot(x=range(0,len(self.val_accuracy)), y=self.val_accuracy, ax=ax[0], label="Validation Accuracy")
        sns.lineplot(x=range(0,len(self.val_loss)), y=self.val_loss, ax=ax[1], label="Validation Loss")

        ax[0].set_xlabel("# of Epochs")
        ax[1].set_xlabel("# of Epochs")

        plt.suptitle("Learning Curves: {}".format(self.name))
        plt.show()

    def evaluate_(self):
        return self.model.evaluate(x=X_valid, y=y_valid, batch_size=self.batch_size)
    
    def save(self, filename):
        self.model.save("working/"+filename+".hd5")
        
    def predict_(self, test):
        return self.model.predict(test, batch_size=self.batch_size).argmax(axis=1)
        
    def summary_(self):
        return self.model.summary()


# In[ ]:


def generate_output(model, test_data, filename, save=False):
    """Generate output dataframe (and .csv file) of predictions for Kaggle submission."""
    
    try:
        predictions = model.predict_(test_data)
    except:
        predictions = model.predict(test_data).argmax(axis=1)
    
    output = sample_submission.copy()
    output["Label"] = predictions

    if save:
        output.to_csv(filename + ".csv", index=False)
    return output


# ### Intermediate Net
# 
# First, let's create a fully connected network comprised of only dense layers. Using such a configuration achieves a score of `0.97` on the Kaggle leaderboard.

# In[ ]:


batch_size = 128
n_epochs = 20
learning_rate = 0.1
verbose = 0 # set this = 1 to see training progress
optimizer = "adam"

model = NeuralNetwork("3 Relu Hidden Layers + Batch Norm + Dropout (Adam Optimizer)", batch_size, n_epochs, optimizer, verbose)
model.add_(Dense(64, activation="relu", input_shape=(784,)))
model.add_(BatchNormalization())

model.add_(Dense(64, activation="relu"))
model.add_(BatchNormalization())

model.add_(Dense(64, activation="relu"))
model.add_(BatchNormalization())
model.add_(Dropout(0.2))

model.add_(Dense(10, activation="softmax"))

model.summary_()
model.compile_and_fit()
model.plot_learning_curves()


# In[ ]:


results = model.evaluate_()
results


# In[ ]:


predictions = model.predict_(test)
predictions[0:10]


# We can preview individual digits in the test set and observe whether any of the model predictions are correct.

# In[ ]:


preview_index = 4 # The index of the digit in the training set to preview

fig, ax = plt.subplots(figsize=(5,5))
image = test.iloc[preview_index].values.reshape((28,28))
plt.imshow(image, cmap="Greys")
plt.axis("off")

plt.suptitle("Previewing Digit #{}".format(preview_index + 1), y=0.9)
plt.show()


# ### Compare Varying Amounts of Dropout
# 
# Dropout is a powerful technique for preventing overfitting. Often trial and error is the best way to determine how many rounds of dropout to incorporate into a network. 
# 
# For example, below are three networks: one with one round of dropout, one with two rounds of dropout and one with three rounds of dropout. Based on validation metrics, we can see that having two rounds of dropout yields optimal accuracy. Similarly, you could analyze configurations with more or less dropout per layer (i.e. adjust the 20% parameter).

# In[ ]:


batch_size = 128
n_epochs = 50
verbose = 0
optimizer = "adam"

# 1 round of dropout
model_1d = NeuralNetwork("3 Relu Hidden Layers + Batch Norm + 1 x Dropout (Adam Optimizer)", batch_size, n_epochs, optimizer, verbose)
model_1d.add_(Dense(64, activation="relu", input_shape=(784,)))
model_1d.add_(BatchNormalization())

model_1d.add_(Dense(64, activation="relu"))
model_1d.add_(BatchNormalization())

model_1d.add_(Dense(64, activation="relu"))
model_1d.add_(BatchNormalization())
model_1d.add_(Dropout(0.2))

model_1d.add_(Dense(10, activation="softmax"))

model_1d.compile_and_fit()
model_1d.plot_learning_curves()

# 2 rounds of dropout
model_2d = NeuralNetwork("3 Relu Hidden Layers + Batch Norm + 2 x Dropout (Adam Optimizer)", batch_size, n_epochs, optimizer, verbose)
model_2d.add_(Dense(64, activation="relu", input_shape=(784,)))
model_2d.add_(BatchNormalization())

model_2d.add_(Dense(64, activation="relu"))
model_2d.add_(BatchNormalization())
model_2d.add_(Dropout(0.2))

model_2d.add_(Dense(64, activation="relu"))
model_2d.add_(BatchNormalization())
model_2d.add_(Dropout(0.2))

model_2d.add_(Dense(10, activation="softmax"))

model_2d.compile_and_fit()
model_2d.plot_learning_curves()

# 3 rounds of dropout
model_3d = NeuralNetwork("3 Relu Hidden Layers + Batch Norm + 3 x Dropout (Adam Optimizer)", batch_size, n_epochs, optimizer, verbose)
model_3d.add_(Dense(64, activation="relu", input_shape=(784,)))
model_3d.add_(BatchNormalization())
model_3d.add_(Dropout(0.2))

model_3d.add_(Dense(64, activation="relu"))
model_3d.add_(BatchNormalization())
model_3d.add_(Dropout(0.2))

model_3d.add_(Dense(64, activation="relu"))
model_3d.add_(BatchNormalization())
model_3d.add_(Dropout(0.2))

model_3d.add_(Dense(10, activation="softmax"))

model_3d.compile_and_fit()
model_3d.plot_learning_curves()


# In[ ]:


model_1d.evaluate_()


# In[ ]:


model_2d.evaluate_()


# In[ ]:


model_3d.evaluate_()


# In[ ]:


plt.plot(model_1d.history.history["val_accuracy"], label="1 x Dropout")
plt.plot(model_2d.history.history["val_accuracy"], label="2 x Dropout")
plt.plot(model_3d.history.history["val_accuracy"], label="3 x Dropout")
plt.legend()
plt.title("Impact of Dropout on Neural Network Learning")
plt.ylabel("Validation Accuracy")
plt.xlabel("Epoch")
plt.show()


# ### CNN v1
# 
# Convolutional neural networks are uniquely adept at extracting spatial information. Below is a simple CNN with two convolutional layers (inspired by LeNet-5 architecture).

# In[ ]:


batch_size = 128
n_epochs = 10
verbose = 1
optimizer = "adam"

# cnn = NeuralNetwork("CNN", batch_size, n_epochs, optimizer, verbose)
cnn = Sequential()

# 1st convolutional layer
cnn.add(Conv2D(32, kernel_size=(3,3), activation="relu", input_shape=(28,28,1)))

# 2nd convolutional layer
cnn.add(Conv2D(64, kernel_size=(3,3), activation="relu"))

# reduce computational complexity
cnn.add(MaxPooling2D(pool_size=(2,2)))

# dropout
cnn.add(Dropout(0.25))

# dimensionality reduction
cnn.add(Flatten())

# dense layer
cnn.add(Dense(128, activation="relu"))
        
# dropout
cnn.add(Dropout(0.5))

# output
cnn.add(Dense(10, activation="softmax"))

cnn.summary()


# In[ ]:


cnn.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

cnn_history = cnn.fit(x=X_train_2D,
                      y=y_train,
                      batch_size=batch_size,
                      epochs=n_epochs,
                      verbose=verbose,
                      validation_data=(X_valid_2D, y_valid))


# In[ ]:


plt.plot(cnn_history.history["val_accuracy"], label="CNN")
plt.legend()
plt.title("CNN Learning")
plt.ylabel("Validation Accuracy")
plt.xlabel("Epoch")
plt.show()


# ### CNN v2: Adding More Conv Blocks
# 
# To extract even more complex spatial information from an image, we can increase the number of convolutional blocks (composed of convolutional layers, max pooling layers and dropout layers). This configuration earns around a `0.992` on the leaderboard.

# In[ ]:


# https://www.kaggle.com/yassineghouzam/introduction-to-cnn-keras-0-997-top-6

batch_size = 128
n_epochs = 10
verbose = 1
optimizer = "adam"

cnn = Sequential()

cnn.add(Conv2D(32, kernel_size=(3,3), activation="relu", input_shape=(28,28,1)))
cnn.add(Conv2D(32, kernel_size=(3,3), activation="relu"))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Dropout(0.25))

cnn.add(Conv2D(64, kernel_size=(3,3), activation="relu"))
cnn.add(Conv2D(64, kernel_size=(3,3), activation="relu"))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Dropout(0.25))

cnn.add(Flatten())
cnn.add(Dense(256, activation="relu"))
cnn.add(Dropout(0.5))

cnn.add(Dense(10, activation="softmax"))

cnn.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
cnn_history = cnn.fit(x=X_train_2D,
                      y=y_train,
                      batch_size=batch_size,
                      epochs=n_epochs,
                      verbose=1,
                      validation_data=(X_valid_2D, y_valid))


# ### CNN v3: Increase L1/L2 Filter Size & Use Same Padding
# 
# Further adjustments can be made to the network above, including: increasing the filter size in the first conv block and setting `padding="Same"`.

# In[ ]:


batch_size = 128
n_epochs = 10
verbose = 1
optimizer = "adam"

cnn = Sequential()

cnn.add(Conv2D(32, kernel_size=(5,5), activation="relu", padding="Same", input_shape=(28,28,1)))
cnn.add(Conv2D(32, kernel_size=(5,5), activation="relu", padding="Same"))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Dropout(0.25))

cnn.add(Conv2D(64, kernel_size=(3,3), activation="relu", padding="Same"))
cnn.add(Conv2D(64, kernel_size=(3,3), activation="relu", padding="Same"))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Dropout(0.25))

cnn.add(Flatten())
cnn.add(Dense(256, activation="relu"))
cnn.add(Dropout(0.5))

cnn.add(Dense(10, activation="softmax"))

cnn.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"])

cnn_history = cnn.fit(x=X_train_2D,
                      y=y_train,
                      batch_size=batch_size,
                      epochs=n_epochs,
                      verbose=1,
                      validation_data=(X_valid_2D, y_valid))


# ### CNN v4: Experiment with a New Activation Function (Mish)
# 
# Someone on Twitter tipped me off to two new activation functions that are gaining popularity: Swish and Mish. I decided to try Mish, however didn't see any performance gains relative to our `relu`-based network.

# In[ ]:


# Keras Implementation of Mish Activation Function.
# Author: https://github.com/digantamisra98/Mish

# Import Necessary Modules.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from keras.engine.base_layer import Layer
from keras import backend as K

class Mish(Layer):
    '''
    Mish Activation Function.
    .. math::
        mish(x) = x * tanh(softplus(x)) = x * tanh(ln(1 + e^{x}))
    Shape:
        - Input: Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.
        - Output: Same shape as the input.
    Examples:
        >>> X_input = Input(input_shape)
        >>> X = Mish()(X_input)
    '''

    def __init__(self, **kwargs):
        super(Mish, self).__init__(**kwargs)
        self.supports_masking = True

    def call(self, inputs):
        return inputs * K.tanh(K.softplus(inputs))

    def get_config(self):
        base_config = super(Mish, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def compute_output_shape(self, input_shape):
        return input_shape


# In[ ]:


batch_size = 128
n_epochs = 10
verbose = 1
optimizer = "adam"

cnn = Sequential()

cnn.add(Conv2D(32, kernel_size=(5,5), activation=Mish(), padding="Same", input_shape=(28,28,1)))
cnn.add(Conv2D(32, kernel_size=(5,5), activation=Mish(), padding="Same"))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Dropout(0.25))

cnn.add(Conv2D(64, kernel_size=(3,3), activation=Mish(), padding="Same"))
cnn.add(Conv2D(64, kernel_size=(3,3), activation=Mish(), padding="Same"))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Dropout(0.25))

cnn.add(Flatten())
cnn.add(Dense(256, activation=Mish()))
cnn.add(Dropout(0.5))

cnn.add(Dense(10, activation="softmax"))

cnn.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"])

cnn_history = cnn.fit(x=X_train_2D,
                      y=y_train,
                      batch_size=batch_size,
                      epochs=n_epochs,
                      verbose=1,
                      validation_data=(X_valid_2D, y_valid))


# ### Training on All Training Data
# 
# Based on validation performance, I decided to submit CNN v3 as my final model, training on the entire training dataset to eke out as much performance as possible.
# 
# The model below earned a public score of around `0.993`. Not bad for minimal architectural trial and error!

# In[ ]:


batch_size = 128
n_epochs = 10
verbose = 0
optimizer = "adam"

cnn = Sequential()

cnn.add(Conv2D(32, kernel_size=(5,5), activation="relu", padding="Same", input_shape=(28,28,1)))
cnn.add(Conv2D(32, kernel_size=(5,5), activation="relu", padding="Same"))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Dropout(0.25))

cnn.add(Conv2D(64, kernel_size=(3,3), activation="relu", padding="Same"))
cnn.add(Conv2D(64, kernel_size=(3,3), activation="relu", padding="Same"))
cnn.add(MaxPooling2D(pool_size=(2,2)))
cnn.add(Dropout(0.25))

cnn.add(Flatten())
cnn.add(Dense(256, activation="relu"))
cnn.add(Dropout(0.5))

cnn.add(Dense(10, activation="softmax"))

cnn.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

cnn_history = cnn.fit(x=train_2D,
                      y=y,
                      batch_size=batch_size,
                      epochs=n_epochs,
                      verbose=verbose)


# In[ ]:


output = generate_output(cnn, test_2D, "cnn", save=True)
output.head()


# Thanks for reading and, until next time, happy coding :)
