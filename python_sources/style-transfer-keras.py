#!/usr/bin/env python
# coding: utf-8

# # Neural style transfer

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.
from keras import backend as K
from keras.preprocessing.image import load_img, save_img, img_to_array
from keras.applications import vgg19
from keras.models import Model
import tensorflow as tf

import matplotlib.pyplot as plt
from PIL import Image
import time
from scipy.optimize import fmin_l_bfgs_b


# ## Load Images

# In[ ]:


style_path = "../input/best-artworks-of-all-time/images/images/"
content_path = "../input/image-classification/validation/validation/travel and adventure/"


# In[ ]:


content_image_name = "13.jpg"
base_image_path = content_path + content_image_name
style_image_name = "Pablo_Picasso/Pablo_Picasso_92.jpg"
# style_image_name = "Vincent_van_Gogh/Vincent_van_Gogh_875.jpg"
style_image_path = style_path + style_image_name


# In[ ]:


plt.figure()
plt.title("Base Image", fontsize=20)
# print(base_image_path)
img_base = load_img(base_image_path)
plt.imshow(img_base)

plt.figure()
plt.title("Style Image", fontsize=20)
# print(style_image_path)
img_style = load_img(style_image_path)
plt.imshow(img_style)

width, height = load_img(base_image_path).size
img_nrows = 400
img_ncols = int(width * img_nrows / height)


# ## Preprocessing Image
# * we convert these images into a form suitable for numercial processing by adding another dimension (beyond the classic height x width x 3 dimensions) so that we can later concatenate the representations of these two images into a common data structure.
# * we need to match imput data into vgg network model

# In[ ]:


def preprocess_img(image_path):
    img = load_img(image_path, target_size=(img_nrows, img_ncols))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = vgg19.preprocess_input(img)
    return img


# In[ ]:


# create base & style image tf variable
base_image = K.variable(preprocess_img(base_image_path))
style_image = K.variable(preprocess_img(style_image_path))
K.image_data_format()

# a placeholder to contain generated image
if K.image_data_format() == 'channels_first':
    combination_image = K.placeholder((1,3,img_nrows, img_ncols))
else:
    combination_image = K.placeholder((1, img_nrows, img_ncols, 3))

# combine the 3 images into a single Keras tensor which is suitable for processing by vgg19 model
input_tensor = K.concatenate([base_image, style_image, combination_image], axis=0)


# ## The Pre-trained VGG Model
# * The idea introduced by the paper is that convolutional neural networks (CNNs) pre-trained for image classification already know how to encode perceptual and semantic information about images.
# * Since we are not interested in the classification problem, we do not need the fully connected layers or the final softmax classifier.
# * Setting include_top=False in the code below means that we do not include any of the fully connected layers.

# In[ ]:


# building VGG19 model
vgg19_weights = "../input/vgg19/vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5"
model = vgg19.VGG19(input_tensor=input_tensor, include_top=False, weights=vgg19_weights)
print("Model loaded.")


# In[ ]:


layers = dict([(layer.name, layer.output) for layer in model.layers])
layers


# ## The Optimisation Problem
# * The loss function we want to minimise can be decomposed into three distinct parts: the content loss, the style loss, and the total variation loss.
# ## The content loss
# * Draw the content features from block4_conv2
# * Content loss is defined as the Mean Squared Error between the feature map F of out content image C and the feature map P of our generated image Y, in other words, (scaled, squared) Eucildean distance between feature representations of the content and combination images.
# ## The style loss
# * Define Gram matrix: The terms of this matrix are proportional to the covariances of corresponding sets of features, and thus captures information about which features tend to activate together. By only capturing these aggregate statistics across the image, they are blind to the specific arrangement of objects inside the image. This is what allows them to capture information about style independent of content.
# * Compute Gram matrix: The Gram matrix can be computed efficiently by reshaping the feature spaces suitably and taking an outer product.
# * The style loss: is (scaled, squared) Frobenius norm of the difference between the Gram matices of the style and combination images.
# ## The total variation loss
# * If you were to solve the optimisation problem with only the two loss terms we've introduced so far (style and content), you'll find that the output is quite noisy. We thus add another term, called the total variation loss (a regularisation term) that encourages spatial smoothness.

# In[ ]:


# the relative importance of content loss, style loss and total variation
content_weight = 0.025
style_weight = 1.0
total_variation_weight = 1.0


# In[ ]:


# compute content loss
def get_content_loss(base_content, combination):
    return K.sum(K.square(combination - base_content))


# In[ ]:


# compute style loss
def gram_matrix(input_tensor):
    features = K.batch_flatten(K.permute_dimensions(input_tensor, (2, 0, 1)))
    gram = K.dot(features, K.transpose(features))
    return gram

    
def get_style_loss(style, combination):
    style_gram = gram_matrix(style)
    combine_gram = gram_matrix(combination)
    channels = 3
    size = img_nrows * img_ncols
    return K.sum(K.square(style_gram - combine_gram)) / (4. * (channels ** 2) * (size ** 2))


# In[ ]:


# compute total variation loss:
def total_variation_loss(x):
    a = K.square(x[:, :img_nrows-1, :img_ncols-1, :] - x[:, 1:, :img_ncols-1, :])
    b = K.square(x[:, :img_nrows-1, :img_ncols-1, :] - x[:, :img_nrows-1, 1:, :])
    return K.sum(K.pow(a + b, 1.25))


# In[ ]:


# initialise the total loss to 0 and adding to it in stages
loss = K.variable(0.)

content_features = layers['block4_conv2']
content_image_features = content_features[0, :, :, :]
content_combination_features = content_features[2, :, :, :]
loss += content_weight * get_content_loss(content_image_features, content_combination_features)

style_layers = ['block1_conv1', 
                'block2_conv1',
                'block3_conv1',
                'block4_conv1',
                'block5_conv1']
for layer_name in style_layers:
    style_features = layers[layer_name]
    style_image_features = style_features[1, :, :, :]
    style_combination_features = style_features[2, :, :, :]
    style_loss = get_style_loss(style_image_features, style_combination_features)
    loss += (style_weight / len(style_layers)) * style_loss
    
loss += total_variation_weight * total_variation_loss(combination_image)


# ## Define Gradients and Solve the Optimisation Problem
# * Define gradients of the total loss relative to the combination image, and use these gradients to iteratively improve upon our combination image to minise the loss.
# * Evaluator: computes loss and gradients in one pass while retrieving them via two separate functions, loss and grads. Because scipy.optimize requires separate functions for loss and gradients, but computing them separately would be inefficient.
# * Use L-BFGS algorithm (a quasi-Newton algorithm that's significantly quicker to converge than standard gradient descent) to iteratively imporve upon it.

# In[ ]:


# define gradients
grads = K.gradients(loss, combination_image)

outputs = [loss]
outputs += grads
f_outputs = K.function([combination_image], outputs)

def eval_loss_and_grads(x):
    x = x.reshape((1, img_nrows, img_ncols, 3))
    outs = f_outputs([x])
    loss_value = outs[0]
    grad_values = outs[1].flatten().astype('float64')
    return loss_value, grad_values

class Evaluator(object):
    
    def __init__(self):
        self.loss_value = None
        self.grad_values = None
    
    def loss(self, x):
        assert self.loss_value is None
        loss_value, grad_values = eval_loss_and_grads(x)
        self.loss_value = loss_value
        self.grad_values = grad_values
        return self.loss_value
    
    def grads(self, x):
        assert self.loss_value is not None
        grad_values = np.copy(self.grad_values)
        self.loss_value = None
        self.grad_values = None
        return grad_values

evaluator = Evaluator()


# In[ ]:


# 10 iterations of L-BFGS
# start with random collections of pixels
x = np.random.uniform(0, 255, (1, img_nrows, img_ncols, 3)) - 128

iterations = 20

for i in range(iterations):
    print('Start iteration', i)
    start_time = time.time()
    x, min_val, info = fmin_l_bfgs_b(evaluator.loss, x.flatten(),
                                     fprime=evaluator.grads, maxfun=20)
    print('Current loss value:', min_val)
    end_time = time.time()
    print('Iteration %d completed in %ds' % (i, end_time-start_time))
    


# In[ ]:


# get result image
x = x.reshape((img_nrows, img_ncols, 3))
x = x[:, :, ::-1]
x[:, :, 0] += 103.939
x[:, :, 1] += 116.779
x[:, :, 2] += 123.68
img_result = np.clip(x, 0, 255).astype('uint8')


# In[ ]:


# show content image
plt.figure()
plt.title("Base Image", fontsize=20)
# print(base_image_path)
img_base = load_img(base_image_path)
plt.imshow(img_base)

# show style image
plt.figure()
plt.title("Style Image", fontsize=20)
# print(style_image_path)
img_style = load_img(style_image_path)
plt.imshow(img_style)

# show results
plt.figure()
plt.title("Combined Image", fontsize=20)
plt.imshow(img_result)


# In[ ]:




