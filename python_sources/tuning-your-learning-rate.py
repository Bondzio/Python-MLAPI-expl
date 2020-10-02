#!/usr/bin/env python
# coding: utf-8

# # Tuning your learning rate
# 
# ## Background
# 
# The **learning rate** is one of those first and most important parameters of a model, and one that you need to start thinking about pretty much immediately upon starting to build a model. It controls how big the jumps your model makes, and from there, how quickly it learns.
# 
# Neural networks learn by performing gradient descent on your data across a network of nodes, arriving at a sequence of nodal weights that are (hopefully), when combined, predictive of the values in your target. You can think of the objective of the gradient descent algorithm you use to learn with your neural network as being the 
# 
# If you choose a learning rate that is too small, your neural network will take a long time to converge. If you choose a learning rate that is too big, you will get a different and more interesting problem. For most purposes it's useful to imagine gradient descent as moving around on an uneven, highly bumpy, and potentially non-convex cost surface. A cross section of this surface can be anything really, but in practice a multidimensional bowl or sinkhole is a good approximation. If you're on one side of the bowl, and your learning rate is too high, instead of sinking towards and settling into the center of the bowl, your learner will overshoot the bottom and end up on the other side. The next gradient step it will reverse course, overshoot again, and end up on the opposite side of the bowl, back near where you first started. If your learning rate is chosen badly enough, you can even end up getting *worse* performance over time, instead of better&mdash;divergent behavior. This effect is well-illustrated in this graphic from [the following article](https://www.jeremyjordan.me/nn-learning-rate/), which much of this notebook is based off of:
# 
# ![](https://i.imgur.com/1ZPQw1l.png)
# 
# ## Picking a learning rate
# 
# So how do you determine the right learning rate for your learner? In the last notebook, ["Full batch, mini-batch, and online learning"](https://www.kaggle.com/residentmario/full-batch-mini-batch-and-online-learning), I talked about best practices on setting another immediately relevant neural network parameter, the batch size. That notebook also covered the interplay between batch size and the learning rate. To recap, in general, larger batch sizes work with larger gradients and update less often but more reliably, whilst smaller batches work with smaller gradients and update more often but less reliably. I also mentioned that the batch size is something you can set early in the training process, at the toy model phase, and rely on until you get pretty far into the training optimization.
# 
# Once you have picked a batch size, it's time to pick a learning rate that works best with that value. This is a one-dimensional parameter search (an optimization problem in an optimization problem!), and a relatively expensive one, as every learning rate adjustment requires retraining the entire network once more.
# 
# If you pick a specific batch size and then chart out the overall loss your model gets once fully trained with a selection of learning rates, here's the curve you get (again copied from the same article):
# 
# ![](https://i.imgur.com/u3FDTzU.png)
# 
# This curve consists of three distinct parts: learning rates that don't learn fast enough, and don't take the model anywhere; an area of steepest descent, eventually leading into an optimal or near-optimal learning rate. Past the edge of that curve you get noise, and eventually divergence (this is where the learning rate is *too* large). In the previous notebook I mentioned the `fast.ai` automatic learning rate setter utility. All that utility *really* does is determine the rough boundaries of these three areas. That's something you can do yourself too.
# 
# ## Learning rate annealing
# 
# Even if you preprocess your data, and especially if you don't the cost surfaces that your model will have are liable to be highly skewed. In other words, one bowl-slice of the loss surface might be relatively wide, whilst another slice might be super narrow. It's hard to pick a learning rate that works well with both of these shapes. A small learning rate that works well on the narrow part of the curve will be too slow for the wide part of the curve, and if you pick a big learning rate expect to see good convergence characteristics on the wide bowl but possibly divergence on the small bowl.
# 
# Additionally, if we keep a constant learning rate, we will always overshoot the absolute minima of the bowl by at most the value of the learning rate. We will step past the minimal point in one direction, then past it again in other direction, and so on.
# 
# These two observations (and others) imply that to "settle" our neural network, it is probably helpful to adaptively downtune our learning rate over the course of the training. This is known as **learning rate annealing**. 
# 
# The most common learning rate annealing technique is multiplicative backoff: we pick some number of batches, and each time we've hit that many batches we multiply the learning rate by some fractional number. Multiplicative backoff will deal with both of these problems in one fell swoop. This is not a panacea; if we are not converging fast enough, learning rate annealing might prevent us from converging on the true solution. We want to downtune learning rates only after the model has converged on a rough model picture, so there's still tuning to do. But all other things being equal, learning rate annealing seems to be a pretty reliable way of squeezing a little more predictive value from our model.
# 
# Another interesting and more complicated idea when it comes to learning rate annealing is to actually turn the learning rate down, and then back *up*. A couple of ways of doing this that have been studied are a triangular sawtooth learning rate schedule (cyclic learning rate, which first appeared in [this paper](https://arxiv.org/abs/1506.01186)), and "stochastic gradient descent with warm restarts" (basically copy pasting half cosine curves, with a reset to the full rate coming after the minima).
# 
# Increasing the learning rate after a downturn, assuming that the model has already converged on the rough model picture, is going to have a negative effect on convergence in the short term, up to and including divergence. However, it may improve the learning in the long term. The basic premise is that it allows the model to escape sharp minima, that is minimal points with steep slopes, and explore afield for flat minima, minima with less steep slopes. It's generally accepted that flat minima have better generalization characteristics to new data, for reasons that are fairly intuitive: if our test data cost surface diverges slightly (or is not strongly representative enough, by a small amount) from the true data cost surface, the nearby point will be relatively close in a shallow hole, and relatively far away in a steep hole.
# 
# The other effect is that it enhances the ability of the learner to more easily escape saddle points on the surface: places where the gradients are relatively flat in all directions, and so the learning rate is painfully slow. I think this is less important because there are better techniques for approaching this problem, like using momentum.
# 
# ## Learning rates in practice
#  
# The batch size you choose is most heavily affected by the characteristics of the data that you are training on. You need to pick a batch size large enough to capture a relatively representative sample of the dataset on a per-batch basis. It's not *that* significantly impacted by other decisions you make as part of the network definition process. It's also very easy to retune, if you want to get to tuning it again later on. So, since data is a constant, you can pick a batch size early in the training process and use that one for a while.
# 
# The optimal learning rate, on the other hand, *does* change quite a lot, depending on the learner that you use, the network configuration, the preprocessing you perform on the dataset, and all the other things you do. It's worth adjusting it pretty often. You'll definitely have to tweak it every time you adjust the optimizer, for instance.

# ## Implementations
# 
# There is no "learning rate schedule" global parameter at the model level. To tamper with the learning rate on the fly, we need to update parameters of the Keras model throughout the training process. This requires using a feature of Keras known as callbacks, which allow us to arbitrarily modify the model in the midst of fitting it. For slightly more details on callbacks see ["Keras callbacks and config files"](https://www.kaggle.com/residentmario/keras-callbacks-and-config-files/edit).
# 
# For links to repositories with recipes the more complicated learning rate adjustments, check out [the blog post this kernel is based on](https://www.jeremyjordan.me/nn-learning-rate/). A good way to implement these adjustments is to make use of the `LearningRateScheduler` available as a Keras builtin. For example, here's a build for the stepped backoff learning rate schedule:

# In[ ]:


##############################
# MODEL BUILDING BOILERPLATE #
##############################

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD

# Generate dummy data
import numpy as np
import pandas as pd

X_train = np.random.random((1000, 3))
y_train = pd.get_dummies(np.argmax(X_train[:, :3], axis=1)).values
X_test = np.random.random((100, 3))
y_test = pd.get_dummies(np.argmax(X_test[:, :3], axis=1)).values


# In[ ]:


import numpy as np
from keras.callbacks import LearningRateScheduler

###########################################
# DEFINE A STEPPED LEARNING RATE SCHEDULE #
###########################################

lr_sched = LearningRateScheduler(lambda epoch: 1e-4 * (0.75 ** np.floor(epoch / 2)))

# Build the model.
clf = Sequential()
clf.add(Dense(9, activation='relu', input_dim=3))
clf.add(Dense(9, activation='relu'))
clf.add(Dense(3, activation='softmax'))
clf.compile(loss='categorical_crossentropy', optimizer=SGD())

# Perform training.
clf.fit(X_train, y_train, epochs=10, batch_size=500, callbacks=[lr_sched])

