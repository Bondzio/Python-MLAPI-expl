#!/usr/bin/env python
# coding: utf-8

# # Pokemon-VQVAE
# * Encoding and Recreating Images using Vector Quantized Variational AutoEncoders
# * `64x64x3` images are encoded into `12x12x32`==`64x24x3` latent space and transformed back into `64x64x3` images
# * The Vector Quantized representation is `37.5%` the size of the original image
# 
# # Work Based on
# * [Neural Discrete Representation Learning](https://arxiv.org/abs/1711.00937)
# * [VQ-VAE Keras Implementation](https://github.com/HenningBuhl/VQ-VAE_Keras_Implementation)
# * [Kaggle Dataset](https://www.kaggle.com/brilja/pokemon-mugshots-from-super-mystery-dungeon)
# 

# In[ ]:


# Imports
import numpy as np
from matplotlib import pyplot as plt

import tensorflow as tf
import keras

from keras.models import Model
from keras.layers import Input, Layer, Activation, Dense, Flatten, Dropout, Lambda, Conv2D, MaxPooling2D, UpSampling2D, Conv2DTranspose, SpatialDropout2D
from keras.layers.normalization import BatchNormalization
from keras import losses
from keras import backend as K
from sklearn.model_selection import train_test_split

import os
from PIL import Image
from matplotlib.pyplot import imshow
from random import randrange


# In[ ]:


os.listdir('../input/pokemon-mugshots-from-super-mystery-dungeon')


# # Data Preprocessing
# The images are all pngs so I am using `x = x[...,:3]` to get rid of the alpha channel

# In[ ]:


# Load data.
data = []
paths = []
for r, d, f in os.walk(r'../input/pokemon-mugshots-from-super-mystery-dungeon/smd/'):
    for file in f:
        if '.png' in file:
            paths.append(os.path.join(r, file))
            
for path in paths:
    img = Image.open(path)
    x = np.array(img)
    x = x[...,:3]
    if(x.shape == (64,64,3)):
        data.append(x)

src = np.array(data)
src = src.reshape(len(data),64,64,3)


#splitting data into train and test sets
x_train,x_test,y_train,y_test = train_test_split(src, src, test_size=0.2, shuffle=True, random_state=69)

# Normalize data.
x_test = x_test / np.max(x_train)
x_train = x_train / np.max(x_train)


# # Custom VQVAE Keras Layer
# Very nicely written custom layer provided by Github user [HenningBuhl](https://github.com/HenningBuhl/VQ-VAE_Keras_Implementation/blob/master/VQ_VAE_Keras_MNIST_Example.ipynb)

# In[ ]:


# VQ layer.
class VQVAELayer(Layer):
    def __init__(self, embedding_dim, num_embeddings, commitment_cost,
                 initializer='uniform', epsilon=1e-10, **kwargs):
        self.embedding_dim = embedding_dim
        self.num_embeddings = num_embeddings
        self.commitment_cost = commitment_cost
        self.initializer = initializer
        super(VQVAELayer, self).__init__(**kwargs)

    def build(self, input_shape):
        # Add embedding weights.
        self.w = self.add_weight(name='embedding',
                                  shape=(self.embedding_dim, self.num_embeddings),
                                  initializer=self.initializer,
                                  trainable=True)

        # Finalize building.
        super(VQVAELayer, self).build(input_shape)

    def call(self, x):
        # Flatten input except for last dimension.
        flat_inputs = K.reshape(x, (-1, self.embedding_dim))

        # Calculate distances of input to embedding vectors.
        distances = (K.sum(flat_inputs**2, axis=1, keepdims=True)
                     - 2 * K.dot(flat_inputs, self.w)
                     + K.sum(self.w ** 2, axis=0, keepdims=True))

        # Retrieve encoding indices.
        encoding_indices = K.argmax(-distances, axis=1)
        encodings = K.one_hot(encoding_indices, self.num_embeddings)
        encoding_indices = K.reshape(encoding_indices, K.shape(x)[:-1])
        quantized = self.quantize(encoding_indices)

        return quantized

    @property
    def embeddings(self):
        return self.w

    def quantize(self, encoding_indices):
        w = K.transpose(self.embeddings.read_value())
        return tf.nn.embedding_lookup(w, encoding_indices, validate_indices=False)


# In[ ]:


# Calculate vq-vae loss.
def vq_vae_loss_wrapper(data_variance, commitment_cost, quantized, x_inputs):
    def vq_vae_loss(x, x_hat):
        recon_loss = losses.mse(x, x_hat) / data_variance
        
        e_latent_loss = K.mean((K.stop_gradient(quantized) - x_inputs) ** 2)
        q_latent_loss = K.mean((quantized - K.stop_gradient(x_inputs)) ** 2)
        loss = q_latent_loss + commitment_cost * e_latent_loss
        
        return recon_loss + loss #* beta
    return vq_vae_loss


# In[ ]:


# Hyper Parameters.
epochs = 2 # MAX
batch_size = 500
validation_split = 0.2

# VQ-VAE Hyper Parameters.
embedding_dim = 32 # Length of embedding vectors.
num_embeddings = 128 # Number of embedding vectors (high value = high bottleneck capacity).
commitment_cost = 0.25 # Controls the weighting of the loss terms.


# Model will take a `64x64x3` image and encode it in into a tensor of size `12x12x32`, then upsample back to `64x64x3`

# In[ ]:


# Encoder
input_img = Input(shape=(64, 64, 3))
x = Conv2D(32, (3, 3), activation='relu')(input_img)
x = Conv2D(32, (3, 3), activation='relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(64, (3, 3), activation='relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(64, (3, 3), activation='relu')(x)
# VQVAELayer.
enc = Conv2D(embedding_dim, kernel_size=(1, 1), strides=(1, 1), name="pre_vqvae")(x)
enc_inputs = enc

#uncomment these lines when you run locally
#enc = VQVAELayer(embedding_dim, num_embeddings, commitment_cost, name="vqvae")(enc)
#x = Lambda(lambda enc: enc_inputs + K.stop_gradient(enc - enc_inputs), name="encoded")(enc)

data_variance = np.var(x_train)
loss = vq_vae_loss_wrapper(data_variance, commitment_cost, enc, enc_inputs)

# Decoder.
x = Conv2DTranspose(64, (3, 3), activation='relu')(x)
x = UpSampling2D()(x)
x = Conv2DTranspose(32, (3, 3), activation='relu')(x)
x = UpSampling2D()(x)
x = Conv2DTranspose(32, (3, 3), activation='relu')(x)
x = Conv2DTranspose(3, (3, 3))(x)

# Autoencoder.
vqvae = Model(input_img, x)
vqvae.compile(loss=loss, optimizer='adam')
#vqvae.summary()
# this model maps an input to its encoded representation. Saving it as it's own model
encoder = Model(input_img, enc)
#encoder.summary()


# # Model Summary
# 
# I couldn't get the custom layer to work on a Kaggle notebook so here is the local version
# 
# ![model](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/model.JPG)

# The training is too time consuming for the online notebook. The results from training done locally are posted below

# In[ ]:


history = vqvae.fit(x_train, x_train,batch_size=batch_size, epochs=epochs,validation_data=(x_test, x_test))


# # Training
# Trained locally for 250 epochs
# ![training](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/training.JPG)

# # Results
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/label0.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/label1.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/image_2.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/image_3.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/image_4.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/image_5.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/image_6.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/image_7.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/image_8.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/image_9.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/image_0.png)
# ![r](https://raw.githubusercontent.com/vee-upatising/Pokemon-VQVAE/master/results/image_11.png)
# 
# # [View Jupyter Notebook](https://nbviewer.jupyter.org/github/vee-upatising/Pokemon-VQVAE/blob/master/VQVAE.ipynb)
# 
# 
