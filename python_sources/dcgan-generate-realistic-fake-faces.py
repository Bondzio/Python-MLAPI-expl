#!/usr/bin/env python
# coding: utf-8

# # Deep Convolutional GANs
# A GAN using convolutional layers in the generator and discriminator is called a Deep Convolutional GAN, or DCGAN for short. The DCGAN architecture was first explored in 2016 and has seen impressive results in generating new images; you can read the [original paper, here](https://arxiv.org/pdf/1511.06434.pdf).
# 
# Specifically, we'll use a series of convolutional or transpose convolutional layers in the discriminator and generator. It's also necessary to use batch normalization to get these convolutional networks to train.

# # Face Generation
# In this notebook, we will generate realistic fake faces, by defining and training a DCGAN. Our main objective is to get a generator network to generate new images of faces that look as realistic as possible!
# 
# **Get Data**
# I'll be using the CelebFaces Attributes Dataset (CelebA) to train your adversarial networks.
# 
# **Pre processed Data**
# Each of the CelebA images has been cropped to remove parts of the image that don't include a face, then resized down to 64x64x3 NumPy images. 
# 
# Source - The data has been taken from udacity's deep learning [github repository](https://github.com/udacity).
# 

# In[ ]:


# Downloading the necessary files and the dataset
from IPython.display import clear_output

get_ipython().system('wget -cq -O problem_unittests.py https://raw.githubusercontent.com/udacity/deep-learning-v2-pytorch/master/project-face-generation/problem_unittests.py')
get_ipython().system('wget -cq -O processed_celeba_small.zip https://s3.amazonaws.com/video.udacity-data.com/topher/2018/November/5be7eb6f_processed-celeba-small/processed-celeba-small.zip')
clear_output()  
print("Downloaded Successfully")


# In[ ]:


# Extractting the dataset
get_ipython().system('unzip -n processed_celeba_small.zip')
clear_output()
print("Extracted Successfully")


# In[ ]:


data_dir = 'processed_celeba_small/'

import pickle as pkl
import matplotlib.pyplot as plt
import numpy as np
import problem_unittests as tests
#import helper

get_ipython().run_line_magic('matplotlib', 'inline')


# # **Visualize the CelebA Data**
# 
# The CelebA dataset contains over 200,000 celebrity images with annotations. These are color images with 3 color channels (RGB)#RGB_Images each.
# 
# **Pre-process and Load the Data**
# 
# Each of the CelebA images has been cropped to remove parts of the image that don't include a face, then resized down to 64x64x3 NumPy images. This pre-processed dataset is a smaller subset of the very large CelebA data.
# 

# In[ ]:


# necessary imports
import torch
from torchvision import datasets
from torchvision import transforms
from torch.utils.data import DataLoader


# ## Function to create DataLoader

# In[ ]:


def get_dataloader(batch_size, image_size, data_dir='processed_celeba_small/'):
    """
    Batch the neural network data using DataLoader
    :param batch_size: The size of each batch; the number of images in a batch
    :param img_size: The square size of the image data (x, y)
    :param data_dir: Directory where image data is located
    :return: DataLoader with batched data
    """
    
    # resize and normalize the images
    transform = transforms.Compose([transforms.Resize(image_size),
                                    transforms.ToTensor()])

    # define datasets using ImageFolder
    dataset = datasets.ImageFolder(data_dir, transform)

    # create and return DataLoader
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers = 4)

    return data_loader


# ## Creating the DataLoader

# In[ ]:


# Define function hyperparameters
batch_size = 32
img_size = 32

# Call your function and get a dataloader
celeba_train_loader = get_dataloader(batch_size, img_size)


# # Visualising the pre-processed data
# Function to visualise the images present in the data.

# In[ ]:


def imshow(img):
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))

# obtain one batch of training images
dataiter = iter(celeba_train_loader)
images, _ = dataiter.next() # _ for no labels

# plot the images in the batch, along with the corresponding labels
fig = plt.figure(figsize=(20, 4))
plot_size=20
for idx in np.arange(plot_size):
    ax = fig.add_subplot(2, plot_size/2, idx+1, xticks=[], yticks=[])
    imshow(images[idx])


# ### **Scaling the data**
# 
# The output of a tanh activated generator will contain pixel values in a range from -1 to 1,so we need to rescale our training images to range -1 to 1, which was 0 to 1 now.

# In[ ]:


def scale(x, feature_range=(-1, 1)):
    ''' Scale takes in an image x and returns that image, scaled
       with a feature_range of pixel values from -1 to 1. 
       This function assumes that the input x is already scaled from 0-1.'''
    min, max = feature_range
    x = x * (max - min) + min
    
    return x


# In[ ]:


# checking scaled range
# should be close to -1 to 1
img = images[0]
scaled_img = scale(img)

print('Min: ', scaled_img.min())
print('Max: ', scaled_img.max())


# # **Define the Model**
# A GAN is comprised of two adversarial networks, a discriminator and a generator.
# 
# # **Discriminator**
# We will define the discriminator. This is a convolutional classifier. It is suggested we define this with normalization.
# 
# The inputs to the discriminator are 32x32x3 tensor images
# 
# The output is a single value that will indicate whether a given image is real or fake

# In[ ]:


import torch.nn as nn
import torch.nn.functional as F


# Helper function to create convolutional layers with batch normalization.

# In[ ]:


# helper conv function -> a convolutional layer + an optional batch norm layer
def conv(in_channels, out_channels, kernel_size=4, stride=2, padding=1, batch_norm=True):
    """Creates a convolutional layer, with optional batch normalization.
    """
    layers = []
    conv_layer = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, 
                           kernel_size=kernel_size, stride=stride, padding=padding, bias=False)
    
    #appending convolutional layer
    layers.append(conv_layer)
    
    #appending batch norm layer
    if batch_norm:
        layers.append(nn.BatchNorm2d(out_channels))
        
    return nn.Sequential(*layers)


# ## Discriminator Model

# In[ ]:


class Discriminator(nn.Module):

    def __init__(self, conv_dim):
        """
        Initialize the Discriminator Module
        :param conv_dim: The depth of the first convolutional layer
        """
        super(Discriminator, self).__init__()

        # complete init function
        self.conv_dim = conv_dim
        
        #leaky relu negative slope
        self.leaky_relu_slope = 0.2
        
        # Convolutional layers, increasing in depth
        # first layer has *no* batchnorm
        
       
        self.conv1 = conv(3, conv_dim, batch_norm=False)  
        self.conv2 = conv(conv_dim, conv_dim*2)           
        self.conv3 = conv(conv_dim*2, conv_dim*4)         
                
        
        # Classification layer -- final, fully-connected layer
        self.fc = nn.Linear(conv_dim*4*4*4, 1)
    
    
    def forward(self, x):
        """
        Forward propagation of the neural network
        :param x: The input to the neural network     
        :return: Discriminator logits; the output of the neural network
        """
        # define feedforward behavior
        
        # relu applied to all conv layers but last
        out = F.leaky_relu(self.conv1(x), self.leaky_relu_slope)
        out = F.leaky_relu(self.conv2(out), self.leaky_relu_slope)
        out = F.leaky_relu(self.conv3(out), self.leaky_relu_slope)
        
        
        out = out.view(-1, self.conv_dim*4*4*4) #flattening
        
        # last, classification layer
        out = self.fc(out) 
        
        return out


# # **Generator**
# The generator should upsample an input and generate a new image of the same size as our training data 32x32x3. This should be mostly transpose convolutional layers with normalization applied to the outputs.
# 
# 
# The inputs to the generator are vectors of some length z_size
# 
# The output is a image of shape 32x32x3.
# 

# In[ ]:


#deconv helper function, which creates a transpose convolutional layer + an optional batchnorm layer
def deconv(in_channels, out_channels, kernel_size=4, stride=2, padding=1, batch_norm=True):
    """Creates a transpose convolutional layer, with optional batch normalization.
    """
    layers = []
    
    # append transpose conv layer -- we are not using bias terms in conv layers
    layers.append(nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding, bias=False))
    
    # optional batch norm layer
    if batch_norm:
        layers.append(nn.BatchNorm2d(out_channels))
        
    return nn.Sequential(*layers)


# ## Generator Model

# In[ ]:


class Generator(nn.Module):
    
    def __init__(self, z_size, conv_dim):
        """
        Initialize the Generator Module
        :param z_size: The length of the input latent vector, z
        :param conv_dim: The depth of the inputs to the *last* transpose convolutional layer
        """
        super(Generator, self).__init__()

        # complete init function
        
        self.conv_dim = conv_dim
        
        # first, fully-connected layer
        self.fc = nn.Linear(z_size, conv_dim*4*4*4)

        
        # transpose conv layers
        self.deconv1 = deconv(conv_dim*4, conv_dim*2)
        self.deconv2 = deconv(conv_dim*2, conv_dim)
        self.deconv3 = deconv(conv_dim, 3, batch_norm=False)
        
        
        

    def forward(self, x):
        """
        Forward propagation of the neural network
        :param x: The input to the neural network     
        :return: A 32x32x3 Tensor image as output
        """
        # define feedforward behavior
        
        ## fully-connected
        x = self.fc(x)
        
        #retrieve the batch size
        batch_size = x.shape[0]
        
        #reshape
        x = x.view(-1, self.conv_dim*4, 4, 4)
        
        
        # hidden transpose conv layers + relu
        x = F.relu(self.deconv1(x))
        x = F.relu(self.deconv2(x))
       
        
        # last layer + tanh activation
        x = self.deconv3(x)
        x = torch.tanh(x)
            
        return x


# # **Initialize the weights of your networks**
# 
# To help your models converge, we should initialize the weights of the convolutional and linear layers in your model. From reading the original DCGAN paper, they say:
# 
# **All weights were initialized from a zero-centered Normal distribution with standard deviation 0.02.**
# 

# In[ ]:


def weights_init_normal(m):
    """
    Applies initial weights to certain layers in a model .
    The weights are taken from a normal distribution 
    with mean = 0, std dev = 0.02.
    :param m: A module or layer in a network    
    """
    # classname will be something like:
    # `Conv`, `BatchNorm2d`, `Linear`, etc.
    classname = m.__class__.__name__
        
    # for every Linear layer and convolutional in a model..
    if classname.find('Linear') != -1 or classname.find('Convo2d') != -1:
        
        #Fills the input Tensor with values drawn from the normal distribution
        #mean =0 and standard deviation=0.02
        torch.nn.init.normal_(m.weight.data, 0.0, 0.02)
        
        #The bias terms or set to 0
        m.bias.data.fill_(0)


# # Building the whole network
# Now we'll call all the functions and make out network

# In[ ]:


def build_network(d_conv_dim, g_conv_dim, z_size):
    # define discriminator and generator
    D = Discriminator(d_conv_dim)
    G = Generator(z_size=z_size, conv_dim=g_conv_dim)

    # initialize model weights
    D.apply(weights_init_normal)
    G.apply(weights_init_normal)

    print(D)
    print()
    print(G)
    
    return D, G


# In[ ]:


# Define model hyperparams
d_conv_dim = 32
g_conv_dim = 32
z_size = 100

D, G = build_network(d_conv_dim, g_conv_dim, z_size)


# # Training on GPU
# We'll check if GPU is available or not and train our model in GPU if it is.

# In[ ]:


import torch

# Check for a GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'
train_on_gpu = torch.cuda.is_available()
if not train_on_gpu:
    print('No GPU found. Please use a GPU to train your neural network.')
else:
    print('Training on GPU!')


# # **Discriminator and Generator Losses**
# Now we need to calculate the losses for both types of adversarial networks.
# 
# ## **Discriminator Losses**
# 
# For the discriminator, the total loss is the sum of the losses for real and fake images, d_loss = d_real_loss + d_fake_loss.
# 
# ## **Generator Loss**
# The generator loss will look similar only with flipped labels. The generator's goal is to get the discriminator to think its generated images are real.
# 

# In[ ]:


def real_loss(D_out, smooth=False):
    '''Calculates how close discriminator outputs are to being real.
       param, D_out: discriminator logits
       return: real loss'''
   
    #retrieve the batch size
    batch_size = D_out.size(0)
    
    # smooth, real labels = 0.9
   
    if smooth:
        labels = torch.ones(batch_size)*0.9
    else:
        labels = torch.ones(batch_size)    # real labels = 1
    
    # move labels to GPU if available 
    if train_on_gpu:
        labels = labels.cuda()
        
    # binary cross entropy with logits loss
    criterion = nn.BCEWithLogitsLoss()
    # calculate loss
    loss = criterion(D_out.squeeze(), labels)
    
    
    return loss

def fake_loss(D_out):
    
    '''Calculates how close discriminator outputs are to being fake.
       param, D_out: discriminator logits
       return: fake loss'''
    
    batch_size = D_out.size(0)
    
    labels = torch.zeros(batch_size) # fake labels = 0
    
    if train_on_gpu:
        labels = labels.cuda()
    
    # The losses will by binary cross entropy loss with logits, which we can get with 
    # BCEWithLogitsLoss. This combines a sigmoid activation function and and binary 
    #cross entropy loss in one function.
    criterion = nn.BCEWithLogitsLoss()
    # calculate loss
    loss = criterion(D_out.squeeze(), labels)
    
    
    return loss


# # Optimizers 
# We'll use the Adam optimizer with the right parameters.

# In[ ]:


import torch.optim as optim

lr = 0.005
beta1 = 0.3
beta2 = 0.999 # default value

# Create optimizers for the discriminator D and generator G
d_optimizer = optim.Adam(D.parameters(), lr, betas=(beta1, beta2))
g_optimizer = optim.Adam(G.parameters(), lr, betas=(beta1, beta2))


# # **Training**
# Training will involve alternating between training the discriminator and the generator. You'll use your functions real_loss and fake_loss to help you calculate the discriminator losses.
# 
# We are training the discriminator by alternating on real and fake images.
# 
# Then the generator, which tries to trick the discriminator and should have an opposing loss function.

# In[ ]:


def train(D, G, n_epochs, print_every=2500):
    '''Trains adversarial networks for some number of epochs
       param, D: the discriminator network
       param, G: the generator network
       param, n_epochs: number of epochs to train for
       param, print_every: when to print and record the models' losses
       return: D and G losses'''
    
    # move models to GPU
    if train_on_gpu:
        D.cuda()
        G.cuda()

    # keep track of loss and generated, "fake" samples
    samples = []
    losses = []

    # Get some fixed data for sampling. These are images that are held
    # constant throughout training, and allow us to inspect the model's performance
    sample_size=16
    fixed_z = np.random.uniform(-1, 1, size=(sample_size, z_size))
    fixed_z = torch.from_numpy(fixed_z).float()
    # move z to GPU if available
    if train_on_gpu:
        fixed_z = fixed_z.cuda()

    # epoch training loop
    for epoch in range(n_epochs):

        # batch training loop
        for batch_i, (real_images, _) in enumerate(celeba_train_loader):

            batch_size = real_images.size(0)
            real_images = scale(real_images)
            
            

            # ===============================================
            #               TRAIN THE NETWORKS
            # ===============================================
            
            d_optimizer.zero_grad()
            
            
            # ---------TRAIN THE DISCRIMINATOR ----------------
            
            # Train the discriminator on real and fake images
            
            # Compute the discriminator losses on real images 
            if train_on_gpu:
                real_images = real_images.cuda()
                
            D_real = D(real_images)
            d_real_loss = real_loss(D_real)
            
            
            # Train with fake images
            # Generate fake images
            z = np.random.uniform(-1, 1, size=(batch_size, z_size))
            z = torch.from_numpy(z).float()
            # move x to GPU, if available
            if train_on_gpu:
                z = z.cuda()
            fake_images = G(z)  #generate fake images from generator
            
            
            # Compute the discriminator losses on fake images
            D_fake = D(fake_images)
            d_fake_loss = fake_loss(D_fake)
            
            
            # add up loss and perform backprop
            # For the discriminator, the total loss is the sum of the losses for 
            # real and fake images, d_loss = d_real_loss + d_fake_loss.
            d_loss = d_real_loss + d_fake_loss
            d_loss.backward()
            d_optimizer.step()
            
            
            
             # ---------TRAIN THE GENERATOR ----------------
             
             # Train the generator with an adversarial loss     
             
            g_optimizer.zero_grad()
            
            # Generate fake images
            z = np.random.uniform(-1, 1, size=(batch_size, z_size))
            z = np.random.uniform(-1, 1, size=(batch_size, z_size))
            z = torch.from_numpy(z).float()
            if train_on_gpu:
                z = z.cuda()
            
            fake_images = G(z)
            
            # Compute the discriminator losses on fake images 
            # using flipped labels!
            D_fake = D(fake_images) # pass the fake images to the discriminator as input
            
            g_loss = real_loss(D_fake) # use real loss to flip labels
            
            # perform backprop and optimization steps
            g_loss.backward()
            g_optimizer.step()
            
            # Print some loss stats
            if batch_i % print_every == 0:
                # append discriminator loss and generator loss
                losses.append((d_loss.item(), g_loss.item()))
                # print discriminator and generator loss
                print('Epoch [{:5d}/{:5d}] | d_loss: {:6.4f} | g_loss: {:6.4f}'.format(
                        epoch+1, n_epochs, d_loss.item(), g_loss.item()))


        ## AFTER EACH EPOCH##    
        # generate and save sample, fake images
        G.eval() # for generating samples
        samples_z = G(fixed_z)
        samples.append(samples_z)
        G.train() # back to training mode

    # Save training generator samples
    with open('train_samples.pkl', 'wb') as f:
        pkl.dump(samples, f)
    
    # finally return losses
    return losses


# In[ ]:


# set number of epochs 
n_epochs = 25

# call training function
losses = train(D, G, n_epochs=n_epochs)


# # **Training loss**
# Plotting the training losses for the generator and discriminator, recorded after each epoch.

# In[ ]:


fig, ax = plt.subplots()
losses = np.array(losses)
plt.plot(losses.T[0], label='Discriminator', alpha=0.5)
plt.plot(losses.T[1], label='Generator', alpha=0.5)
plt.title("Training Losses")
plt.legend()


# # **Generator samples from training**
# Now the faces we wanted to see that doesn't even exist in this world and are 100% fake created by the machine.

# In[ ]:


# helper function for viewing a list of passed in sample images
def view_samples(epoch, samples):
    fig, axes = plt.subplots(figsize=(16,4), nrows=2, ncols=8, sharey=True, sharex=True)
    for ax, img in zip(axes.flatten(), samples[epoch]):
        img = img.detach().cpu().numpy()
        img = np.transpose(img, (1, 2, 0))
        img = ((img + 1)*255 / (2)).astype(np.uint8)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        im = ax.imshow(img.reshape((32,32,3)))


# In[ ]:


# Load samples from generator, taken while training
with open('train_samples.pkl', 'rb') as f:
    samples = pkl.load(f)


# In[ ]:


_ = view_samples(-1, samples)

