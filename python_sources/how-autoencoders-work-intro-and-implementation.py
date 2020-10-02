#!/usr/bin/env python
# coding: utf-8

# ## Simple Tutorial to Understand How Autoencoders work
# 
# Autoencoders are a special type of neural network architectures in which the output is same as the input. Autoencoders are trained in an unsupervised manner in order to learn the exteremely low level repersentations of the input data. These low level features are then deformed back to project the actual data. An autoencoder is a regression task where the network is asked to predict its input (in other words, model the identity function). These networks has a tight bottleneck of a few neurons in the middle, forcing them to create effective representations that compress the input into a low-dimensional code that can be used by the decoder to reproduce the original input.
# 
# A typical autoencoder architecture comprises of three main components: 
# 
# - **Encoding Architecture :** The encoder architecture comprises of series of layers with decreasing number of nodes and ultimately reduces to a latent view repersentation.  
# - **Latent View Repersentation :** Latent view repersents the lowest level space in which the inputs are reduced and information is preserved.  
# - **Decoding Architecture :** The decoding architecture is the mirro image of the encoding architecture but in which number of nodes in every layer increases and ultimately outputs the similar (almost) input.  
# 
# ![](**https://i.imgur.com/Rrmaise.png**)
# 
# A highly fine tuned autoencoder model should be able to reconstruct the same input which was passed in the first layer. In this kernel, I will walk you through the working of autoencoders and their implementation.  Autoencoders are widly used with the image data and some of their use cases are: 
# 
# - Dimentionality Reduction   
# - Image Compression   
# - Image Denoising   
# - Image Generation    
# 
# 
# 
# ## How Autoencoders work 
# 
# The main idea behind autoencoders is to learn a low level repersenation of a high level dimentional data. Lets try to understand the encoding process with an example.  Consider a data repersentation space (N dimentional space which is used to repersent the data) and consider the data points repersented by two variables : x1 and x2. Data Manifold is the space inside the data repersentation space in which the true data resides. 

# In[ ]:


from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import numpy as np
init_notebook_mode(connected=True)

## generate random data
N = 50
random_x = np.linspace(2, 10, N)
random_y1 = np.linspace(2, 10, N)
random_y2 = np.linspace(2, 10, N)

trace1 = go.Scatter(x = random_x, y = random_y1, mode="markers", name="Actual Data")
trace2 = go.Scatter(x = random_x, y = random_y2, mode="lines", name="Model")
layout = go.Layout(title="2D Data Repersentation Space", xaxis=dict(title="x2", range=(0,12)), 
                   yaxis=dict(title="x1", range=(0,12)), height=400, 
                   annotations=[dict(x=5, y=5, xref='x', yref='y', text='This 1D line is the Data Manifold (where data resides)',
                   showarrow=True, align='center', arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#636363',
                   ax=-120, ay=-30, bordercolor='#c7c7c7', borderwidth=2, borderpad=4, bgcolor='orange', opacity=0.8)])
figure = go.Figure(data = [trace1], layout = layout)
iplot(figure)


# To repersent this data, we are currently using 2 dimensions - X and Y. But it is possible to reduce the dimensions of this space into lower dimensions ie. 1D. If we can define following : 
# 
# - Reference Point on the line : A  
# - Angle L with a horizontal axis  
# 
# then any other point, say B, on line A can be repersented in terms of Distance "d" from A and angle L.  

# In[ ]:


random_y3 = [2 for i in range(100)]
random_y4 = random_y2 + 1
trace4 = go.Scatter(x = random_x[4:24], y = random_y4[4:300], mode="lines")
trace3 = go.Scatter(x = random_x, y = random_y3, mode="lines")
trace1 = go.Scatter(x = random_x, y = random_y1, mode="markers")
trace2 = go.Scatter(x = random_x, y = random_y2, mode="lines")
layout = go.Layout(xaxis=dict(title="x1", range=(0,12)), yaxis=dict(title="x2", range=(0,12)), height=400,
                   annotations=[dict(x=2, y=2, xref='x', yref='y', text='A', showarrow=True, align='center', arrowhead=2, arrowsize=1, arrowwidth=2, 
                                     arrowcolor='#636363', ax=20, ay=-30, bordercolor='#c7c7c7', borderwidth=2, borderpad=4, bgcolor='orange', opacity=0.8), 
                                dict(x=6, y=6, xref='x', yref='y', text='B', showarrow=True, align='center', arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#636363',
                                     ax=20, ay=-30, bordercolor='#c7c7c7', borderwidth=2, borderpad=4, bgcolor='yellow', opacity=0.8), dict(
                                     x=4, y=5, xref='x', yref='y',text='d', ay=-40), 
                                dict(x=2, y=2, xref='x', yref='y', text='angle L', ax=80, ay=-10)], title="2D Data Repersentation Space", showlegend=False)
data = [trace1, trace2, trace3, trace4]
figure = go.Figure(data = data, layout = layout)
iplot(figure)



#################

random_y3 = [2 for i in range(100)]
random_y4 = random_y2 + 1
trace4 = go.Scatter(x = random_x[4:24], y = random_y4[4:300], mode="lines")
trace3 = go.Scatter(x = random_x, y = random_y3, mode="lines")
trace1 = go.Scatter(x = random_x, y = random_y1, mode="markers")
trace2 = go.Scatter(x = random_x, y = random_y2, mode="lines")
layout = go.Layout(xaxis=dict(title="u1", range=(1.5,12)), yaxis=dict(title="u2", range=(1.5,12)), height=400,
                   annotations=[dict(x=2, y=2, xref='x', yref='y', text='A', showarrow=True, align='center', arrowhead=2, arrowsize=1, arrowwidth=2, 
                                     arrowcolor='#636363', ax=20, ay=-30, bordercolor='#c7c7c7', borderwidth=2, borderpad=4, bgcolor='orange', opacity=0.8), 
                                dict(x=6, y=6, xref='x', yref='y', text='B', showarrow=True, align='center', arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#636363',
                                     ax=20, ay=-30, bordercolor='#c7c7c7', borderwidth=2, borderpad=4, bgcolor='yellow', opacity=0.8), dict(
                                     x=4, y=5, xref='x', yref='y',text='d', ay=-40), 
                                dict(x=2, y=2, xref='x', yref='y', text='angle L', ax=80, ay=-10)], title="Latent Distance View Space", showlegend=False)
data = [trace1, trace2, trace3, trace4]
figure = go.Figure(data = data, layout = layout)
iplot(figure)


# But the key question here is with what logic or rule, point B can be represented in terms of A and angle L. Or in other terms, what is the equation among B, A and L. The answer is straigtforward, there is no fixed equation but a best possible equation is obtained by the unsupervised learning process. In simple terms, the learning process can be defined as a rule / equation which converts B in the form of A and L. Lets understand this process from a autoencoder perspective. 
# 
# Consider the autoencoder with no hidden layers, the inputs x1 and x2 are encoded to lower repersentation d which is then further projected into x1 and x2. 
# 
# ![](https://i.imgur.com/lfq4eEy.png)
# 
# <br>
# **Step1 : Repersent the points in Latent View Space**   
# 
# If the coordinates of point A and B in the data representation space are: 
# 
# - Point A : (x1A, x2A)  
# - Point B : (x1B, x2B)   
# 
# then their coordinates in the latent view space will be:  
# 
# - Point A : (0, 0)  
# - Point B : (u1B, u2B)  
# 
# u1B = x1B - x1A
# u2B = x2B - x2A
# 
# **Step2 : Represent the points with distance d and angle L **    
# 
# Now, u1B and u2B can represented as a combination of distance d and angle L. And if we rotate this by angle L, towards the horizontal axis, L will become 0. ie.  
# 
# **=> (d, L)**     
# **=> (d, 0)**   (after rotation)   
# 
# This is the output of the encoding process and repersents our data in low dimensions.  If we recall the fundamental equation of a neural network with weights and bias of every layer, then 
# 
# **=> (d, 0) = W. (u1B, u2B)**    
# ==> (encoding)    
# 
# where W is the weight matrix of hidden layer.  Since, we know that the decoding process is the mirror image of the encoding process. 
# 
# **=> (u1B, u2B) = Inverse (W) . (d, 0)**    
# ==> (decoding)  
# 
# The reduced form of data (x1, x2) is (d, 0) in the latent view space which is obtained from the encoding architecture. Similarly, the decoding architecture converts back this representation to original form (u1B, u2B) and then (x1, x2). An important point is that Rules / Learning function / encoding-decoding equation will be different for different types of data. For example, consider the following data in 2dimentional space.  
# 
# 
# ## Different Rules for Different data
# 
# Same rules cannot be applied to all types of data. For example, in the previous example, we projected a linear data manifold in one dimention and eliminated the angle L. But what if the data manifold cannot be projected properly. For example consider the following data manifold view. 

# In[ ]:


import matplotlib.pyplot as plt 
import numpy as np
fs = 100 # sample rate 
f = 2 # the frequency of the signal
x = np.arange(fs) # the points on the x axis for plotting
y = [ np.sin(2*np.pi*f * (i/fs)) for i in x]

get_ipython().run_line_magic('matplotlib', 'inline')
plt.figure(figsize=(15,4))
plt.stem(x,y, 'r', );
plt.plot(x,y);


# In this type of data, the key problem will be to obtain the projection of data in single dimention without loosing information. When this type of data is projected in latent space, a lot of information is lost and it is almost impossible to deform and project it to the original shape. No matter how much shifts and rotation are applied, original data cannot be recovered. 
# 
# So how does neural networks solves this problem ? The intution is, In the manifold space, deep neural networks has the property to bend the space in order to obtain a linear data fold view. Autoencoder architectures applies this property in their hidden layers which allows them to learn low level representations in the latent view space. 
# 
# The following image describes this property: 
# 
# ![](https://i.imgur.com/gKCOdiL.png)
# 
# Lets implement an autoencoder using keras that first learns the features from an image, and then tries to project the same image as the output.  
# 
# ### 1. Load the required libraries
# 

# In[ ]:


## load the libraries 
from keras.layers import Dense, Input, Conv2D, MaxPool2D, UpSampling2D
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from keras.models import Model
from imgaug import augmenters
import pandas as pd
import numpy as np


# ### 2. Dataset Prepration 
# 
# Load the dataset, separate predictors and target, normalize the inputs.

# In[ ]:


### read dataset 
train = pd.read_csv("../input/fashion-mnist_train.csv")
train_x = train[list(train.columns)[1:]].values
train_y = train['label'].values

## normalize and reshape the predictors  
train_x = train_x / 255

## create train and validation datasets
train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size=0.2)

## reshape the inputs
train_x = train_x.reshape(-1, 784)
val_x = val_x.reshape(-1, 784)


# ### 3. Create Autoencoder architecture
# 
# In this section, lets create an autoencoder architecture. The encoding part comprises of three layers with 2000, 1200, and 500 nodes. Encoding architecture is connected to latent view space comprising of 10 nodes which is then connected to decoding architecture with 500, 1200, and 2000 nodes. The final layer comprises of exact number of nodes as the input layer.

# In[ ]:


## input layer
input_layer = Input(shape=(784,))

## encoding architecture
encode_layer1 = Dense(1500, activation='relu')(input_layer)
encode_layer2 = Dense(1000, activation='relu')(encode_layer1)
encode_layer3 = Dense(500, activation='relu')(encode_layer2)

## latent view
latent_view   = Dense(10, activation='sigmoid')(encode_layer3)

## decoding architecture
decode_layer1 = Dense(500, activation='relu')(latent_view)
decode_layer2 = Dense(1000, activation='relu')(decode_layer1)
decode_layer3 = Dense(1500, activation='relu')(decode_layer2)

## output layer
output_layer  = Dense(784)(decode_layer3)

model = Model(input_layer, output_layer)


# Here is the summary of our autoencoder architecture.

# In[ ]:


model.summary()


# Next, we will train the model with early stopping callback.

# In[ ]:


model.compile(optimizer='adam', loss='mse')
early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1, mode='auto')
model.fit(train_x, train_x, epochs=20, batch_size=2048, validation_data=(val_x, val_x), callbacks=[early_stopping])


# Generate the predictions on validation data. 

# In[ ]:


preds = model.predict(val_x)


# Lets plot the original and predicted image
# 
# **Inputs: Actual Images**

# In[ ]:


from PIL import Image 
f, ax = plt.subplots(1,5)
f.set_size_inches(80, 40)
for i in range(5):
    ax[i].imshow(val_x[i].reshape(28, 28))
plt.show()


# **Predicted : Autoencoder Output**

# In[ ]:


f, ax = plt.subplots(1,5)
f.set_size_inches(80, 40)
for i in range(5):
    ax[i].imshow(preds[i].reshape(28, 28))
plt.show()


# So we can see that an autoencoder trained with 20 epoochs is able to reconstruct the input images very well. 
# 
# ## Image Denoising
# 
# Autoencoders are pretty useful, lets look at another application of autoencoders - Image denoising. Many a times input images contain noise in the data, autoencoders can be used to get rid of those images. Lets see it in action. First prepare the train_x and val_x data contianing the image pixels. 
# 
# ![](https://www.learnopencv.com/wp-content/uploads/2017/11/denoising-autoencoder-600x299.jpg)

# In[ ]:


## recreate the train_x array and val_x array
train_x = train[list(train.columns)[1:]].values
train_x, val_x = train_test_split(train_x, test_size=0.2)

## normalize and reshape
train_x = train_x/255.
val_x = val_x/255.


# In this autoencoder network, we will add convolutional layers because convolutional networks works really well with the image inputs. To apply convolutions on image data, we will reshape our inputs in the form of 28 * 28 matrix. For more information related to CNN,  refer to my previous [kernel](https://www.kaggle.com/shivamb/a-very-comprehensive-tutorial-nn-cnn). 

# In[ ]:


train_x = train_x.reshape(-1, 28, 28, 1)
val_x = val_x.reshape(-1, 28, 28, 1)


# ### Noisy Images 
# 
# We can intentionally introduce the noise in an image. I am using imaug package which can be used to augment the images with different variations. One such variation can be introduction of noise. Different types of noises can be added to the images. For example: 
# 
# - Salt and Pepper Noise  
# - Gaussian Noise  
# - Periodic Noise  
# - Speckle Noise  
# 
# Lets introduce salt and pepper noise to our data which is also known as impulse noise. This noise introduces sharp and sudden disturbances in the image signal. It presents itself as sparsely occurring white and black pixels

# In[ ]:


# Lets add sample noise - Salt and Pepper
noise = augmenters.SaltAndPepper(0.1)
seq_object = augmenters.Sequential([noise])

train_x_n = seq_object.augment_images(train_x)
val_x_n = seq_object.augment_images(val_x)


# Before adding noise

# In[ ]:


f, ax = plt.subplots(1,5)
f.set_size_inches(80, 40)
for i in range(5,10):
    ax[i-5].imshow(train_x[i].reshape(28, 28))
plt.show()


# After adding noise

# In[ ]:


f, ax = plt.subplots(1,5)
f.set_size_inches(80, 40)
for i in range(5,10):
    ax[i-5].imshow(train_x_n[i].reshape(28, 28))
plt.show()


# Lets now create the model architecture for the autoencoder. 

# In[ ]:


# input layer
input_layer = Input(shape=(28, 28, 1))

# encoding architecture
encoded_layer1 = Conv2D(64, (3, 3), activation='relu', padding='same')(input_layer)
encoded_layer1 = MaxPool2D((2, 2), padding='same')(encoded_layer1)
encoded_layer2 = Conv2D(32, (3, 3), activation='relu', padding='same')(encoded_layer1)
encoded_layer2 = MaxPool2D((2, 2), padding='same')(encoded_layer2)
encoded_layer3 = Conv2D(16, (3, 3), activation='relu', padding='same')(encoded_layer2)
latent_view    = MaxPool2D((2, 2), padding='same')(encoded_layer3)

# decoding architecture
decoded_layer1 = Conv2D(16, (3, 3), activation='relu', padding='same')(latent_view)
decoded_layer1 = UpSampling2D((2, 2))(decoded_layer1)
decoded_layer2 = Conv2D(32, (3, 3), activation='relu', padding='same')(decoded_layer1)
decoded_layer2 = UpSampling2D((2, 2))(decoded_layer2)
decoded_layer3 = Conv2D(64, (3, 3), activation='relu')(decoded_layer2)
decoded_layer3 = UpSampling2D((2, 2))(decoded_layer3)
output_layer   = Conv2D(1, (3, 3), padding='same')(decoded_layer3)

# compile the model
autoencoder = Model(input_layer, output_layer)
autoencoder.compile(optimizer='adam', loss='mse')


# Here is the model summary

# In[ ]:


autoencoder.summary()


# Train the model with early stopping callback. Increase the number of epochs to a higher number for better results. 

# In[ ]:


early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=5, mode='auto')
train_history = autoencoder.fit(train_x_n, train_x, epochs=10, batch_size=2048, validation_data=(val_x_n, val_x), callbacks=[early_stopping])


# In this implementation, I have not traiened this network for longer epoochs, but for better predictions, you can train the network for larger number of epoochs say somewhere in the range of 500 - 1000. 
# 
# ### Excellent References
# 
# 1. https://www.analyticsvidhya.com/blog/2018/06/unsupervised-deep-learning-computer-vision/
# 2. https://towardsdatascience.com/applied-deep-learning-part-3-autoencoders-1c083af4d798
# 3. https://blog.keras.io/building-autoencoders-in-keras.html
# 4. https://cs.stanford.edu/people/karpathy/convnetjs/demo/autoencoder.html
# 
# 
# Thanks for viewing the kernel, please upvote if you liked it. 
