#!/usr/bin/env python
# coding: utf-8

# Started on 8 July 2019
# 
# **Reference:**
# 1. https://machinelearningmastery.com/how-to-develop-a-generative-adversarial-network-for-a-cifar-10-small-object-photographs-from-scratch/
# 2. https://www.kaggle.com/xhlulu/simple-load-data-function-for-keras
# 3. https://www.kaggle.com/rhodiumbeng/generating-handwritten-digits-gan/output

# # Introduction

# I'm using the tutorial in [Reference 1][1] on GAN to generate particular CIFAR10 images.
# 
# [1]: https://machinelearningmastery.com/how-to-develop-a-generative-adversarial-network-for-a-cifar-10-small-object-photographs-from-scratch/

# In[ ]:


import numpy as np
from numpy import random
from numpy import vstack
import pandas as pd
import os
print(os.listdir("../input"))
import matplotlib.pyplot as plt
from PIL import Image
import zipfile


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Reshape
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import Conv2DTranspose
from keras.layers import LeakyReLU
from keras.layers import Dropout
from keras.optimizers import Adam
from keras.utils.vis_utils import plot_model
from keras.models import load_model


# # Load & prepare CIFAR10 dataset

# In[ ]:


get_ipython().system('tar xzvf ../input/cifar-10-python.tar.gz')


# The function 'load_data()' is taken from [Reference 2.][1]
# 
# [1]: https://www.kaggle.com/xhlulu/simple-load-data-function-for-keras

# In[ ]:


def load_data():
    """
    Loads CIFAR10 dataset and returns tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """
    import os
    import sys
    from six.moves import cPickle
    import numpy as np
    
    def load_batch(fpath):
        with open(fpath, 'rb') as f:
            d = cPickle.load(f, encoding='bytes')  
        data = d[b'data']
        labels = d[b'labels']
        data = data.reshape(data.shape[0], 3, 32, 32)
        return data, labels
    
    path = 'cifar-10-batches-py'
    num_train_samples = 50000
    x_train = np.empty((num_train_samples, 3, 32, 32), dtype='uint8')
    y_train = np.empty((num_train_samples,), dtype='uint8')
    for i in range(1, 6):
        fpath = os.path.join(path, 'data_batch_' + str(i))
        (x_train[(i - 1) * 10000:i * 10000, :, :, :],
         y_train[(i - 1) * 10000:i * 10000]) = load_batch(fpath)
    x_test, y_test = load_batch(os.path.join(path, 'test_batch'))
    y_train = np.reshape(y_train, (len(y_train), 1))
    y_test = np.reshape(y_test, (len(y_test), 1))
    x_train = x_train.transpose(0, 2, 3, 1)
    x_test = x_test.transpose(0, 2, 3, 1)
    return (x_train, y_train), (x_test, y_test)


# In[ ]:


(X_train, Y_train), (X_test, Y_test) = load_data()
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)


# In[ ]:


n_x = 32     # size of image n_x by n_x
n_c = 3      # number of channels
X = np.concatenate((X_train, X_test))     # combine X_train and X_test
Y = np.concatenate((Y_train, Y_test))     # combine Y_train and Y_test
print(X.shape, Y.shape)


# In[ ]:


apl_indices = np.array(np.where(Y[:,0] == 0))
print(apl_indices.shape)
print(apl_indices)


# In[ ]:


# pick out all airplane images
apls = X[apl_indices[0,:]]
print(apls.shape)


# In[ ]:


# pick some apl images and look at these
plt.figure(figsize=(10,10))
n_images = 64
for i in range(n_images):  
    plt.subplot(8, 8, i+1)
    plt.imshow(apls[i])
    plt.axis('off')
plt.subplots_adjust(wspace=0.3, hspace=-0.1)
plt.show()


# **Best Practice:** To scale the pixel values from the range of unsigned integers in [0,255] to the normalized range of [-1,1]. The generator model will generate images with pixel values in the range [-1,1] as it will use the tanh activation function, a best practice. Hence, the real images are to be scaled to the same range.

# In[ ]:


# scale from [0,255] to [-1,1]
apls = (apls - 127.5)/127.5


# # The Discriminator

# The discriminator takes a sample "image" from our dataset and says whether it is real or fake.
# 
# **Inputs:** "image" 32x32 pixels in size; three channels (RGB).
# 
# **Outputs:** binary classification, likelihood the sample is real.

# ### Define the Discriminator

# In[ ]:


def define_discriminator(in_shape=(n_x,n_x,n_c)):
    """
    Define the conv net for the discriminator
    """
    model = Sequential()
    model.add(Conv2D(64,kernel_size=3,padding='same',input_shape=in_shape))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Conv2D(128,kernel_size=3,strides=2,padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Conv2D(128,kernel_size=3,strides=2,padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Conv2D(256,kernel_size=3,strides=2,padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Flatten())
    model.add(Dropout(rate=0.4))
    model.add(Dense(1,activation='sigmoid'))
    opt = Adam(lr=0.0002,beta_1=0.5) # define optimizer
    model.compile(loss='binary_crossentropy',optimizer=opt,metrics=['accuracy'])
    return model


# In[ ]:


discriminator = define_discriminator()
discriminator.summary()


# ### Training of the Discriminator

# All CIFAR10 image samples will be labelled '1' (real). Need to create fake samples labelled as '0'. The fake samples will be created by the Generator. The real and fake samples will be fed into the Discriminator by batches.

# In[ ]:


def generate_real_samples(data, n_samples):
    """
    Pick 'n_samples' randomly from 'data'
    """
    idx = random.randint(low=0,high=data.shape[0],size=n_samples)
    X = data[idx]
    Y = np.ones((n_samples,1))
    return X, Y


# # The Generator

# The Generator creates new, fake but plausible images. It works by taking a point from a latent space as input and output an image.
# 
# **Inputs:** Point in latent space, e.g. a 100-element vector of Gaussian random numbers.
# 
# **Outputs:** 2D color image (3 channels; RGB) of 32x32 pixels with pixel values in [-1,1].

# In[ ]:


def define_generator(latent_dim):
    """
    Define the conv net for the generator
    """
    n_nodes = 256*4*4
    model = Sequential()
    model.add(Dense(n_nodes,input_dim=latent_dim)) # foundation for 4*4 image
    model.add(LeakyReLU(alpha=0.2))
    model.add(Reshape((4,4,256)))
    model.add(Conv2DTranspose(128,kernel_size=4,strides=2,padding='same')) # up-sample to 8*8 image
    model.add(LeakyReLU(alpha=0.2))
    model.add(Conv2DTranspose(128,kernel_size=4,strides=2,padding='same')) # up-sample to 16*16 image
    model.add(LeakyReLU(alpha=0.2))
    model.add(Conv2DTranspose(128,kernel_size=4,strides=2,padding='same')) # up-sample to 32*32 image
    model.add(LeakyReLU(alpha=0.2))
    model.add(Conv2D(3,kernel_size=3,activation='tanh',padding='same'))
    return model


# In[ ]:


latent_dim = 100 # define size of latent space
generator = define_generator(latent_dim)
generator.summary()


# In[ ]:


def generate_latent_points(latent_dim, n_samples):
    """
    This generates points in the latent space as input for the generator
    """
    x_input = random.randn(latent_dim * n_samples)
    x_input = x_input.reshape(n_samples, latent_dim)     # reshape into a batch of inputs for the network
    return x_input


# In[ ]:


def generate_fake_samples(g_model, latent_dim, n_samples):
    """
    Generate 'n_samples' of fake samples from the generator
    """
    X_input = generate_latent_points(latent_dim, n_samples)
    X = g_model.predict(X_input)    # generator predicts output
    Y = np.zeros((n_samples,1))     # create class labels '0' for fake sample
    return X, Y


# # Combining the Discriminator & Generator as a GAN

# In[ ]:


def define_gan(g_model, d_model):
    """
    This takes as arguments the generator and discriminator and creates the GAN subsuming these two models. 
    The weights in the discriminator are marked as not trainable, 
    which only affects the weights as seen by the GAN and not the standalone discriminator model.
    """
    d_model.trainable = False     # make weights in the discriminator not trainable
    model = Sequential()
    model.add(g_model)
    model.add(d_model)
    opt = Adam(lr=0.0002, beta_1=0.5)
    model.compile(loss='binary_crossentropy', optimizer=opt)
    return model


# In[ ]:


gan = define_gan(generator, discriminator)
gan.summary()


# # Functions to evaluate performance of GAN

# In[ ]:


def save_plot(examples, epoch, n=10):
    """
    This creates and save a plot of generated images
    """
    examples = (examples+1)/2.0
    for i in range(n * n):
        plt.subplot(n, n, 1 + i)
        plt.axis('off')
        plt.imshow(examples[i])
    filename = 'generated_plot_e%03d.png' % (epoch+1)
    plt.savefig(filename)
    plt.close()


# In[ ]:


# evaluate the discriminator, plot generated images, save generator model
def summarize_performance(epoch, g_model, d_model, data, latent_dim, n_samples=150):
    """
    This evaluates the discriminator, plot generated images, save generator model
    """
    X_real, Y_real = generate_real_samples(data, n_samples)
    _, acc_real = d_model.evaluate(X_real, Y_real, verbose=0)   # evaluate discriminator on real samples
    X_fake, Y_fake = generate_fake_samples(g_model, latent_dim, n_samples)
    _, acc_fake = d_model.evaluate(X_fake, Y_fake, verbose=0)   # evaluate discriminator on fake samples
    print('>Accuracy real: %.0f%%, fake: %.0f%%' % (acc_real*100, acc_fake*100))    # summarize discriminator performance
    save_plot(X_fake, epoch)
    filename = 'generator_model_%03d.h5' % (epoch + 1)
    g_model.save(filename)


# # Train the GAN

# In[ ]:


def train(g_model, d_model, gan_model, data, latent_dim, n_epochs=900, batch_size=128):
    """
    This trains the combined generator and discriminator models in the GAN
    """
    batch_per_epoch = data.shape[0] // batch_size
    half_batch = batch_size // 2
    for i in range(n_epochs):
        for j in range(batch_per_epoch):
            X_real, Y_real = generate_real_samples(data, half_batch)   # randomly select real samples
            d_loss1, _ = d_model.train_on_batch(X_real, Y_real)   # update discriminator model weights
            X_fake, Y_fake = generate_fake_samples(g_model, latent_dim, half_batch)   # generate fake samples
            d_loss2, _ = d_model.train_on_batch(X_fake, Y_fake)   # update discriminator model weights
            X_gan = generate_latent_points(latent_dim, batch_size)   # as input for generator
            Y_gan = np.ones((batch_size, 1))
            g_loss = gan_model.train_on_batch(X_gan, Y_gan)   # update generator via the discriminator's error
            # print('>%d, %d/%d, d1=%.3f, d2=%.3f, g=%.3f' % (i+1, j+1, batch_per_epoch, d_loss1, d_loss2, g_loss)) # summarize loss for batch
        # evaluate the model performance, sometimes
        if (i+1) % 100 == 0: 
            summarize_performance(i, g_model, d_model, data, latent_dim)


# In[ ]:


latent_dim = 100
d_model = define_discriminator()
g_model = define_generator(latent_dim)
gan_model = define_gan(g_model, d_model)
data = apls
train(g_model, d_model, gan_model, data, latent_dim)


# In[ ]:


image = Image.open('generated_plot_e900.png')
plt.figure(figsize=(15,15))
plt.axis('off')
plt.imshow(image)


# # Using the final Generator model to generate images

# The generation of each image requires a point in the latent space as input.

# In[ ]:


def show_plot(examples, n):
    """
    This shows the plots from the GAN
    """
    plt.figure(figsize=(10,10))
    for i in range(n * n):
        plt.subplot(n, n, 1 + i)
        plt.axis('off')
        plt.imshow(examples[i,:,:])
    plt.subplots_adjust(wspace=0.3, hspace=-0.1)
    plt.show()


# In[ ]:


latent_points = generate_latent_points(100, 10000)
new_images = g_model.predict(latent_points)
new_images = (new_images+1)/2.0
show_plot(new_images, 8)


# # Create zip file to save generated images

# In[ ]:


z = zipfile.PyZipFile('images.zip', mode='w')
for d in range(10000):
    apl_image = Image.fromarray((255*new_images[d]).astype('uint8').reshape((32,32,3)))
    f = str(d)+'.png'
    apl_image.save(f,'PNG')
    z.write(f)
    os.remove(f)
z.close()

