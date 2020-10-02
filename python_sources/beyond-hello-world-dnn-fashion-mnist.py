#!/usr/bin/env python
# coding: utf-8

# # Beyond Hello World, A Computer Vision Example
# You saw how to create a neural network that figured out the problem you were trying to solve in [Hello World of Deep Learning with Neural Networks](https://www.kaggle.com/anmspro/hello-world-of-deep-learning-with-neural-networks). This gave an explicit example of learned behavior. Of course, in that instance, it was a bit of overkill because it would have been easier to write the function Y=2x-1 directly, instead of bothering with using Machine Learning to learn the relationship between X and Y for a fixed set of values, and extending that for all values.
# 
# But what about a scenario where writing rules like that is much more difficult -- for example a computer vision problem? Let's take a look at a scenario where we can recognize different items of clothing, trained from a dataset containing 10 different types.

# ## Start Coding
# 
# Let's start with our import of TensorFlow

# In[ ]:


import tensorflow as tf
print(tf.__version__)


# The Fashion MNIST data is available directly in the tf.keras datasets API. You load it like this:

# In[ ]:


mnist = tf.keras.datasets.fashion_mnist


# Calling load_data on this object will give you two sets of two lists, these will be the training and testing values for the graphics that contain the clothing items and their labels.
# 

# In[ ]:


(training_images, training_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data(path='mnist.npz')


# What does these values look like? Let's print a training image, and a training label to see...Experiment with different indices in the array. For example, also take a look at index 42...that's a a different boot than the one at index 0
# 

# In[ ]:


import numpy as np
np.set_printoptions(linewidth=200)

import matplotlib.pyplot as plt

plt.imshow(training_images[0])

print(training_labels[0])
print(training_images[0])


# You'll notice that all of the values in the number are between 0 and 255. If we are training a neural network, for various reasons it's easier if we treat all values as between 0 and 1, a process called '**normalizing**'...and fortunately in Python it's easy to normalize a list like this without looping. You do it like this:

# In[ ]:


training_images  = training_images / 255.0
test_images = test_images / 255.0


# Now you might be wondering why there are 2 sets...training and testing -- remember we spoke about this in the intro? The idea is to have 1 set of data for training, and then another set of data...that the model hasn't yet seen...to see how good it would be at classifying values. After all, when you're done, you're going to want to try it out with data that it hadn't previously seen!

# Let's now design the model. There's quite a few new concepts here, but don't worry, you'll get the hang of them. 

# In[ ]:


model = tf.keras.models.Sequential([tf.keras.layers.Flatten(), 
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu), 
                                    tf.keras.layers.Dense(10, activation=tf.nn.softmax)])


# **Sequential**: That defines a SEQUENCE of layers in the neural network
# 
# **Flatten**: Remember earlier where our images were a square, when you printed them out? Flatten just takes that square and turns it into a 1 dimensional set.
# 
# **Dense**: Adds a layer of neurons
# 
# Each layer of neurons need an **activation function** to tell them what to do. There's lots of options, but just use these for now. 
# 
# **Relu** effectively means "If X>0 return X, else return 0" -- so what it does it it only passes values 0 or greater to the next layer in the network.
# 
# **Softmax** takes a set of values, and effectively picks the biggest one, so, for example, if the output of the last layer looks like [0.1, 0.1, 0.05, 0.1, 9.5, 0.1, 0.05, 0.05, 0.05], it saves you from fishing through it looking for the biggest value, and turns it into [0,0,0,0,1,0,0,0,0] -- The goal is to save a lot of coding!
# 

# The next thing to do, now the model is defined, is to actually build it. You do this by compiling it with an optimizer and loss function as before -- and then you train it by calling **model.fit ** asking it to fit your training data to your training labels -- i.e. have it figure out the relationship between the training data and its actual labels, so in future if you have data that looks like the training data, then it can make a prediction for what that data would look like. 

# In[ ]:


model.compile(optimizer = tf.optimizers.Adam(),
              loss = 'sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(training_images, training_labels, epochs=5)


# Once it's done training -- you should see an accuracy value at the end of the final epoch. It might look something like 0.9098. This tells you that your neural network is about 91% accurate in classifying the training data. I.E., it figured out a pattern match between the image and the labels that worked 91% of the time. Not great, but not bad considering it was only trained for 5 epochs and done quite quickly.
# 
# But how would it work with unseen data? That's why we have the test images. We can call model.evaluate, and pass in the two sets, and it will report back the loss for each. Let's give it a try:

# In[ ]:


model.evaluate(test_images, test_labels)


# For me, that returned a accuracy of about .8838, which means it was about 88% accurate. As expected it probably would not do as well with *unseen* data as it did with data it was trained on!
# 
# 

# In[ ]:




