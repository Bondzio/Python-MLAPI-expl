#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('wget "https://raw.githubusercontent.com/udacity/deep-learning-v2-pytorch/master/convolutional-neural-networks/conv-visualization/data/udacity_sdc.png"')


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.image as mpimg

import cv2
import numpy as np
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import torch
import torch.nn.functional as F
import torch.nn as nn

# Any results you write to the current directory are saved as output.


# CNNs bases their principles in Image feature extraction using Convolutional kernels let's see how this kernels works on and Image and then we will see how to contruct a CNN network using Pytorch

# In[ ]:



from torchvision import datasets
import torchvision.transforms as transforms
from torch.utils.data.sampler import SubsetRandomSampler

# number of subprocesses to use for data loading
num_workers = 3 # lets try to parallelize the data loading
# how many samples per batch to load
batch_size = 20
# percentage of training set to use as validation
valid_size = 0.2

# convert data to a normalized torch.FloatTensor
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

# choose the training and test datasets
train_data = datasets.CIFAR10('input/CIFAR', train=True,
                              download=True, transform=transform)
test_data = datasets.CIFAR10('input/CIFAR', train=False,
                             download=True, transform=transform)

# obtain training indices that will be used for validation
num_train = len(train_data)
indices = list(range(num_train))
np.random.shuffle(indices)
split = int(np.floor(valid_size * num_train))
train_idx, valid_idx = indices[split:], indices[:split]

# define samplers for obtaining training and validation batches
train_sampler = SubsetRandomSampler(train_idx)
valid_sampler = SubsetRandomSampler(valid_idx)

# prepare data loaders (combine dataset and sampler)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size,
    sampler=train_sampler, num_workers=num_workers)
valid_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, 
    sampler=valid_sampler, num_workers=num_workers)
test_loader = torch.utils.data.DataLoader(test_data, batch_size=batch_size, 
    num_workers=num_workers)
# specify the image classes
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck']


# In[ ]:


import matplotlib.pyplot as plt
# helper function to un-normalize and display an image
def imshow(img,label=None):
    img = img / 2 + 0.5  # unnormalize
    if label:
        plt.title(classes[label])
    plt.imshow(np.transpose(img, (1, 2, 0)))  # convert from Tensor image


# ## Visualizing Kernel effects
# let's se how convolutions affects our Images 

# In[ ]:


dataiter = iter(train_loader)
images, labels = dataiter.next()


# In[ ]:


imshow(images[0],labels[0])


# In the following cell you can be able to see how applying a particular filter (Convolutional kernel) will affect an image filtering out unrelevant features or emphasizing particular ones, in this case applying the sobel_y filter will emphasize horizontal lines and filtersout other features.
# 
# for edge detection it's important that all te elements of the kernel sum 0 in order to don't alterate the original brightness of the image, since we just want to detect the edges (high frequency regions in image (high-pass filter))
# 
# - 0 no change
# - positive - more brighter
# - negative - less brighter

# In[ ]:


# 3x3 array for edge detection
sobel_y = np.array([[ -1, -2, -1], 
                   [ 0, 0, 0], 
                   [ 1, 2, 1]])
# Filter the image using filter2D, which has inputs: (grayscale image, bit-depth, kernel)  
filtered_image = cv2.filter2D(images[0].numpy()[0], -1, sobel_y)
plt.imshow(filtered_image, cmap='gray')


# To see it clear let's actually write a convolutional layer to see the outputs it's produce and also how the activation function affect the results
# 
# So let's say we have the following images and filters gray scale image

# In[ ]:


bgr_img = cv2.imread("udacity_sdc.png") # we normalize the image to ly into 0-1 range so tat our filters and sGD will work better
gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY).astype("float32")/255
plt.imshow(gray_img,cmap='gray')
gray_img_tensor = torch.from_numpy(gray_img).unsqueeze(0).unsqueeze(1).float()


# Then we have 4 filters one for left vertical lines, other for right vertical lines and others 2 for horizontal lines

# In[ ]:


right_V = np.array([[-1, -1, 1, 1],
                    [-1, -1, 1, 1],
                    [-1, -1, 1, 1],
                    [-1, -1, 1, 1]])
left_V = -right_V
down_H = right_V.T
up_H = -down_H
filters = np.array([right_V, left_V, down_H, up_H])


# In[ ]:


"""
Cite: taken from udacity/deep-learning-v2-pytorch
"""
def viz_filters(filters):
    fig = plt.figure(figsize=(10, 5))
    fig.subplots_adjust(left=0, right=1.5, bottom=0.8, top=1, hspace=0.05, wspace=0.05)
    for i in range(4):
        ax = fig.add_subplot(1, 4, i+1, xticks=[], yticks=[])
        ax.imshow(filters[i], cmap='gray')
        ax.set_title('Filter %s' % str(i+1))
        width, height = filters[i].shape
        for x in range(width):
            for y in range(height):
                ax.annotate(str(filters[i][x][y]), xy=(y,x),
                            horizontalalignment='center',
                            verticalalignment='center',
                            color='white' if filters[i][x][y]<0 else 'black')
viz_filters(filters)


# then we will create a conv layer that uses this filters as conv kernels

# In[ ]:


import torch.nn.functional as F

class convtest(torch.nn.Module):
    def __init__(self,weights):
        super().__init__()
        kernel_height,kernels_width=weights.shape[-2:] #the last two are the rows and columns of the kernels
        #we input 1 "feature map(image) 1 dimension", we have 4 filters so we output 4 feature maps
        self.convLayer1=nn.Conv2d(1, 4, kernel_size=(kernel_height, kernels_width), bias=False)
        #we replace the weights with custom filters
        self.convLayer1.weight = torch.nn.Parameter(weights)
        # define a pooling layer
        self.maxPool = nn.MaxPool2d(2, 2)#maxpooling with stride 2 and window of size 2x2 we speact to have the a half of the size o the input
        self.averagePool=nn.AvgPool2d(2,2)#Avgpooling with stride 2 and window of size 2x2 we speact to have the a half of the size o the input
    def forward(self,inputs):
        convolved=self.convLayer1(inputs)
        withActivation=F.relu(convolved)
        maxPooled=self.maxPool(withActivation)
        avgPooled=self.averagePool(withActivation)
        return convolved,withActivation,maxPooled,avgPooled


# we will create the layers, cast our filters to 

# In[ ]:


weights = torch.from_numpy(filters).unsqueeze(1).type(torch.FloatTensor)
model = convtest(weights)
model


# In[ ]:


# helper function for visualizing the output of a given layer
# default number of filters is 4
def viz_layer(layer, n_filters= 4,title=''):
    fig = plt.figure(figsize=(20, 20))
    fig.suptitle(title,y=0.6)
    for i in range(n_filters):
        ax = fig.add_subplot(1, n_filters, i+1, xticks=[], yticks=[])
        # grab layer outputs
        ax.imshow(np.squeeze(layer[0,i].data.numpy()), cmap='gray')
        ax.set_title(f"Output {i+1}")


# In[ ]:


# plot original image
plt.imshow(gray_img, cmap='gray')

viz_filters(model.convLayer1.weight.squeeze(1).detach().int().numpy())
gray_img_tensor = torch.from_numpy(gray_img).unsqueeze(0).unsqueeze(1)
# get the convolutional layer (pre and post activation)
conv_layer, activated_layer,maxPooled,avgPooled = model(gray_img_tensor)
# visualize the output of a conv layer
viz_layer(conv_layer,title='Conv Layer No Activation Function')
viz_layer(activated_layer,title='Conv Layer with Activation Function')
viz_layer(maxPooled,title='Max Pooling results')
viz_layer(avgPooled,title='Avg Pooling results')
print(f"Conv Layer Output Shape: {str(conv_layer.shape):>40}")
print(f"Activated Conv Output Shape: {str(activated_layer.shape):>36}")
print(f"MaxPooling Output Shape: {str(maxPooled.shape):>40}")
print(f"AveragePooling Output Shape: {str(avgPooled.shape):>36}")


# ## Building a CNN for the CIFAR dataset
# Now let's build a network to classify the images in the CIFAR dataset and see the kernels that our network will learn
# 
# For image classification tasks we usually want to increase the depth of our features but to decrease its size to create a bootleneck for compressing information obtaining a hicherical structure of the features going from general to particular
# 
# - In our case we are going to **increase** by the double the number of kernels to get more feature maps trought each convLayer **16 features--> 32 features--> 64 features** 
# - then we will **downsample** the features **HxW** by a half each layer using MaxPooling to extract the most important features for classification **size(32x32) --> size (16x16) --> size (8x8) --> size (4x4)**
# - At the end we will perfom the classification flattening our output feature maps and passing it throught a fully connected network so the input of the fc network will be 
# $$n_{features} = depth*height*width$$
# 
#     where depth is the number of feature maps coming and usually height and weight are the same value and could be calculated as
#    $$(height  | width)=\frac{input_{(height|width)}}{P_{1}.stride*P_{2}.stride....*P_{n}.stride}$$
#   
#   **only when you mantain the same input-output size in each conv layer**
#   where P refers to the pooling layers applied until the desired output sequencially , remember pooling layers each time their are applied downsample our height|weight by a factor of the stride size (2 a half,1 maintain the same size, etc...)
#     

# In[ ]:


from tqdm.auto import tqdm,trange
class metrics():
    def __init__(self):
        self.loss=[]
        self.accuracy=[]
    def append(self,loss,accuracy):
        self.loss.append(loss)
        self.accuracy.append(accuracy)

class CIFARNET(torch.nn.Module):
    def __init__(self,input_d,size):#size assuming H and W are the same (32x32)
        super().__init__()
        """
        the First Layer will have 16 kernels with size 3 
        an stride of 1 to preserve te size and a padding of 1 to complete the missing pixels of the 3x3 kernels
        """
        self.conv1=nn.Conv2d(input_d,16,kernel_size=3,stride=1,padding=1)#sees (32x32)x3 
        self.conv2=nn.Conv2d(self.conv1.out_channels,32,kernel_size=3,stride=1,padding=1)#sees (16x16)x16 image tensor we've downsample the HxW with maxpooling a half
        self.conv3=nn.Conv2d(self.conv2.out_channels,64,kernel_size=3,stride=1,padding=1)#sees (8x8)x32 image tensor  we've downsample the HxW with maxpooling a half
        self.maxPooling=nn.MaxPool2d(2,2)#window size 2,stride 2 downsample the features height and weight to a half of their size
        """The fc network recieves a flatten tensor of size 64(feature maps)*height*width 
        where this H and w has been downsample by a factor of 2 each time we applied MaxPooling with stride 2
        so the input image has a size of 32x32 pixels then the feature smaps of conv1 16x16, then 8x8 and finaly 4*4
        """
        fc_input_f=self.conv3.out_channels*((size//(self.maxPooling.stride**3))**2)
        self.fc=nn.Sequential(#sees (4x4)x64 image tensor we've downsample the HxW with maxpooling a half
                      nn.Linear(fc_input_f,512),
                      nn.ReLU(),
                      nn.Dropout(0.25),
                      nn.Linear(512,10),
                      nn.LogSoftmax(dim=1)
                      )
        """ we can also don't use activation an use crossentropy loss 
        but cross entropy loss applies logsoftmax and Nlloss so is more efficient to use Logsofmax 
        and NLLoss, and then just use torch.exp to get the actual probabilities"""
    
    def forward(self,inputs):
        h_1=self.maxPooling(F.relu(self.conv1(inputs)))#feature maps by the conv1 max pooled (16x16)x16  
        h_2=self.maxPooling(F.relu(self.conv2(h_1))) #feature maps by the conv2 max pooled (8x8)x32
        h_3=self.maxPooling(F.relu(self.conv3(h_2))) #feature maps by the conv3 max pooled (4x4)x64  
        h_3_flatten=h_3.view(-1,self.fc._modules['0'].in_features)# conv3 feature maps flattened (64 * 4 * 4) , we have already calculated in is the in-features of fc layer
        return self.fc(h_3_flatten) #log probabilities for each class (we must use exp to get the actual probabilities
    
    
    def fit(self,train_generator,val_generator,criterion,Optimizer,faccuracy,Epochs=10,device='cuda'):
        self.to(device)
        train_batches=len(train_generator)
        val_batches=len(val_generator)
        val_metrics,train_metrics = metrics(),metrics()
        for epoch in trange(Epochs,desc='Epochs:'):
            #Train steps
            self.train()
            train_accuracy,train_loss=0,0
            for images,labels in tqdm(train_generator,desc='Train Steps:',leave=False):
                images,labels=images.to(device),labels.to(device)
                Optimizer.zero_grad()#clean the gradients of optimizer
                logProbs=self.forward(images)#calculate logProbabilities 
                loss=criterion(logProbs,labels)#calculating loss
                loss.backward()#Calculating loss gradient with respect the parameters
                Optimizer.step()#Optimization step (backpropagation)
                train_loss+=loss.item()
                train_accuracy+=faccuracy(torch.exp(logProbs),labels).item()
            train_metrics.append(train_loss/train_batches,train_accuracy/train_batches)
            #Validation steps
            self.eval()#turns off dropout 
            val_accuracy,val_loss=0,0
            for images,labels in tqdm(val_generator,desc='Val Steps:',leave=False):
                with torch.no_grad():
                    images,labels=images.to(device),labels.to(device)
                    logProbs=self.forward(images)
                    val_loss+=criterion(logProbs,labels).item()
                    val_accuracy+=faccuracy(torch.exp(logProbs),labels).item()
            val_metrics.append(val_loss/val_batches,val_accuracy/val_batches)
            print(f"EPOCH: {epoch}"
                  f"\nTrain loss: {train_metrics.loss[-1]:.4f} Train accuracy: {train_metrics.accuracy[-1]:.4f}"
                  f"\nVal loss: {val_metrics.loss[-1]:.4f} Val accuracy: {val_metrics.accuracy[-1]:.4f}")
        return train_metrics,val_metrics


# In[ ]:


images.shape


# In[ ]:


model=CIFARNET(images.shape[1],images.shape[2])
print("Model Description: ",model,"\nTest model\n",torch.sum(torch.exp(model(images)),dim=1))


# Let's train and test our mode

# In[ ]:


import matplotlib.pyplot as plt
def plot_train_history(train_metrics,val_metrics):
    train_loss,train_accuracy = train_metrics.loss,train_metrics.accuracy
    val_loss,val_accuracy = val_metrics.loss,val_metrics.accuracy
    plt.plot(train_loss, label='Training loss')
    plt.plot(val_loss, label='Validation loss')
    plt.legend(frameon=False)
    plt.show()
    plt.plot(train_accuracy, label='Training accuracy')
    plt.plot(val_accuracy, label='Validation accuracy')
    plt.legend(frameon=False)
    plt.show()


# In[ ]:


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def f_accuracy(predictions,labels):
    top_p, top_class = predictions.topk(1, dim=1)
    equals = top_class == labels.view(*top_class.shape)
    return torch.mean(equals.type(torch.FloatTensor))
criterion=nn.NLLLoss()
Optimizer=torch.optim.SGD(model.parameters(), lr=0.01)


# In[ ]:


train_metrics,val_metrics=model.fit(train_loader,valid_loader,criterion,Optimizer,f_accuracy)


# In[ ]:


plot_train_history(train_metrics,val_metrics)


# ## Data Augmentation  
# We have several problems in this model the first one is that our maximum accuracy archieved whitout overfitting the model is around 70% that is not too god for this data set so there are several problems that could be happening in our. 
# 
# First we know that convNets have some properties by themselves for example they provide translation invariance (in a some way by the kernels working)  so they can found a pattern in an image (matrix) wherever they are but there are a lack of propierties that we need to correctly perfom our task (detect a kind of object and classify it) such as
# 
# - Rotation Invariance (recognizes patterns no matter it rotation in the image)
# - Scale Invariance (recognizes patterns no metter it's size in the image)
# 
# So in order to produce better results and give our model rotation,scale and translation invariences propierties we can do several things one of the simplest way is just adding images that train our model to detect this patter in dificult situations so basically we perfom a preprocessing in our training set such as:
# - Image rotations: to give examples with diferent rotation
# - Shift images: to give examples where the object is not in a typical location
# - Scale the image: to give our image examples where the patterns appear in different scale(this is more harder so there is other ways to perfom this than Data Augmentation )
# 
# Data augmentation is considered a resampling techinique which helps to deal a lot of problems in ML algorithms in this case give our images better examples for classfication creating sintetic data.
# 
# **we only apply data augmentation in our training set we didn't modify our test set cause we want ur test data to be the more similar to our real cases**
# 

# In[ ]:


from torchvision import datasets
import torchvision.transforms as transforms
from torch.utils.data.sampler import SubsetRandomSampler

# number of subprocesses to use for data loading
num_workers = 3 # lets try to parallelize the data loading
# how many samples per batch to load
batch_size = 20
# percentage of training set to use as validation
valid_size = 0.2

# let's perom data augmentation (sintetized samples)
transform_Augmented = transforms.Compose([
    transforms.RandomRotation(10),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

# choose the training and test datasets
train_data = datasets.CIFAR10('input/CIFAR', train=True,
                              download=True, transform=transform_Augmented) 
#we only apply data augmentation in our training set we didn't modify our test set cause we want ur test data to be the more similar to our real cases
test_data = datasets.CIFAR10('input/CIFAR', train=False,
                             download=True, transform=transform)

# obtain training indices that will be used for validation
num_train = len(train_data)
indices = list(range(num_train))
np.random.shuffle(indices)
split = int(np.floor(valid_size * num_train))
train_idx, valid_idx = indices[split:], indices[:split]

# define samplers for obtaining training and validation batches
train_sampler = SubsetRandomSampler(train_idx)
valid_sampler = SubsetRandomSampler(valid_idx)

# prepare data loaders (combine dataset and sampler)
train_loader_aug = torch.utils.data.DataLoader(train_data, batch_size=batch_size,
    sampler=train_sampler, num_workers=num_workers)
valid_loader_aug = torch.utils.data.DataLoader(train_data, batch_size=batch_size, 
    sampler=valid_sampler, num_workers=num_workers)
test_loader_aug = torch.utils.data.DataLoader(test_data, batch_size=batch_size, 
    num_workers=num_workers)


# Then this is how our data looks now

# In[ ]:


classes = ['airplane', 'automobile', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck']


# In[ ]:


dataiter = iter(train_loader_aug)
images, labels = dataiter.next()

# plot the images in the batch, along with the corresponding labels
fig = plt.figure(figsize=(25, 4))
# display 20 images
for idx in np.arange(20):
    ax = fig.add_subplot(2, 20/2, idx+1, xticks=[], yticks=[])
    imshow(images[idx])
    ax.set_title(classes[labels[idx]])


# then let's see if our model valid loss and accuracy could be improved by using this resample technique

# In[ ]:


model_aug=CIFARNET(images.shape[1],images.shape[2])
Optimizer=torch.optim.SGD(model_aug.parameters(), lr=0.01)
train_metrics_aug,val_metrics_aug=model_aug.fit(train_loader_aug,valid_loader_aug,criterion,Optimizer,f_accuracy,Epochs=28)


# In[ ]:


plot_train_history(train_metrics_aug,val_metrics_aug)


# In[ ]:





# In[ ]:




