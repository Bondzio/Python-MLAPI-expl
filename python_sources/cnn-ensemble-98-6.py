#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Import packages

import seaborn as sns 
sns.set(font_scale=1.5)
import pandas as pd
import os 
import keras
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import model_from_json
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense,Conv2D,Flatten,MaxPool2D,Dropout,BatchNormalization
from keras.callbacks import LearningRateScheduler
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.interpolation import map_coordinates
import matplotlib.pyplot as plt
import os

# Any results you write to the current directory are saved as output.


# # **CNN Ensemble!**
# 
# **Purpose**
# 
# The purpose of this notebook is to share an ensemble method consisting of three convolutional neural networks for the Kannada Mnist challenge. Running this workbook as is achieves 98.60% accuracy on the leaderboard, and increasing the number of unique CNNs in the ensemble can achieve a score of 98.90%. 
# 
# This is my first noteback and I'm looking to learn like everyone else so any and all feedback is welcomed! Also a quick shoutout to this great kernal https://www.kaggle.com/cdeotte/25-million-images-0-99757-mnist that inspired both the ensembling and architecture! 
# 
# Along the way we will see
# 1. A brief history of the original MNIST dataset
# 2. Check out the Kannada dataset
# 3. Data augmentations including elastic distortions
# 4. A set of three convolutional neural networks 
# 5. Submit some predictions and hear how to improve accuracy

# **A brief history of digit classifcation**
# Thankfully for us this competition is very similar to the original MNIST competition, meaning we have all the key learnings of that competition at our finger tips. A great survey of MNIST progress is provided here https://www.researchgate.net/publication/334957576_A_Survey_of_Handwritten_Character_Recognition_with_MNIST_and_EMNIST. Below we plot a key table from the report which shows the error rates for a range of very competitive methods. Not surprising we see the much loved CNN with data augmentation taking out all the top spots for lowest error rates, and that's what we'll focus on below!

# In[ ]:


summaryResults = pd.read_csv('/kaggle/input/summarypaper/SummaryPaper.csv').sort_values(by = ['ErrorRate'])
plt.figure(figsize=(18, 17))
ax = sns.barplot(x="ErrorRate", y='Method',hue = 'Category', data=summaryResults, dodge = False)
plt.legend(loc='upper right')
plt.setp(ax.get_legend().get_texts(), fontsize='22') # for legend text
plt.setp(ax.get_legend().get_title(), fontsize='32') # for legend title
plt.xlabel("Error rate")


# **The Kannada Data Set**
# Let's get started and take a look at these images! Like the Mnist dataset we have 28x28 pixel images, all stored as a vector of length 784. Below we read them all in, reshape them and change the scale from 0 to 255 to be -0.5 to 0.5 and then look at a few samples!

# In[ ]:


train_path = "../input/Kannada-MNIST/train.csv"
test_path = "../input/Kannada-MNIST/test.csv"
train = pd.read_csv(train_path)
test = pd.read_csv(test_path)


# In[ ]:


#Split the data up into labels and images, and also scale the images to be between -0.5 and 0.5.
train_images = train.iloc[:,1:]/255 - 0.5
train_labels = train.iloc[:,0]
test_images = test.iloc[:,1:]/255 - 0.5
test_id = test.iloc[:,0]

#Since we're using CNNs we need everything shaped as an image - i.e a 28*28*1 matrix. 
#This represents pixel height, width and "channel". For greyscale images channel =1, for RGB channel =3. 
X_train=train_images.values.reshape(-1,28,28,1)
X_test=test_images.values.reshape(-1,28,28,1)
Y_train=to_categorical(train_labels)

##Let's plot a few sample images
fig=plt.figure(figsize=(16, 16))
for i in range(1, 5):
    img = X_train[i].squeeze()
    fig.add_subplot(1, 5, i)
    plt.imshow(img,cmap=plt.cm.binary)
    plt.axis('off')
plt.show()


# **Image Augmentation** The image augmentation used is typical to many other kernals with affine transforms, that is shifts and rotations. An elastic deformation as described by Simard, Steinkraus, and Plattin (2003) in "Best Practices for Convolutional Neural Networks Applied to Visual Document Analysis" is also included using code and suggested parameters from https://www.kaggle.com/babbler/mnist-data-augmentation-with-elastic-distortion as it sounded like an interesting addition! After running with/without the elastic deformation it seemed a higher score is achieved without, so in the actual image gen I comment out the call to it. 

# Elastic deformation code:

# In[ ]:


def elastic_transform(image, alpha_range, sigma, random_state=None):
    """Elastic deformation of images as described in [Simard2003]_.
    .. [Simard2003] Simard, Steinkraus and Platt, "Best Practices for
       Convolutional Neural Networks applied to Visual Document Analysis", in
       Proc. of the International Conference on Document Analysis and
       Recognition, 2003.
       
   # Arguments
       image: Numpy array with shape (height, width, channels). 
       alpha_range: Float for fixed value or [lower, upper] for random value from uniform distribution.
           Controls intensity of deformation.
       sigma: Float, sigma of gaussian filter that smooths the displacement fields.
       random_state: `numpy.random.RandomState` object for generating displacement fields.
    """
    import numpy as np
    from scipy.ndimage.filters import gaussian_filter
    from scipy.ndimage.interpolation import map_coordinates

    if random_state is None:
        random_state = np.random.RandomState(None)
        
    if np.isscalar(alpha_range):
        alpha = alpha_range
    else:
        alpha = np.random.uniform(low=alpha_range[0], high=alpha_range[1])

    shape = image.shape
    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha

    x, y, z = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), np.arange(shape[2]), indexing='ij')
    indices = np.reshape(x+dx, (-1, 1)), np.reshape(y+dy, (-1, 1)), np.reshape(z, (-1, 1))

    return map_coordinates(image, indices, order=1, mode='reflect').reshape(shape)


# Image augmentation set up:

# In[ ]:


datagen = ImageDataGenerator(
        rotation_range=10,  #This randomly rotates images
        zoom_range = 0.10,  #This randomly zooms images
        width_shift_range=0.1, #This randomly shifts images vertically
        height_shift_range=0.1 #This randomly shifts images horizontally 
        #preprocessing_function=lambda x: elastic_transform(x, alpha_range=[8,10], sigma=3) #Defined above
)


# **Build the three models!** 
# The architecture of the models and the ensembling process is taken from https://www.kaggle.com/cdeotte/25-million-images-0-99757-mnist exactly as is. Not very creative I know, but it looks like a lot of research was done in choosing this structure here so why mess with a good thing. 

# In[ ]:


nets=3
model = [0] * nets
for j in range(nets):
    model[j] = Sequential()

    model[j].add(Conv2D(32, kernel_size = 3, activation='relu', input_shape = (28, 28, 1)))
    model[j].add(BatchNormalization())
    model[j].add(Conv2D(32, kernel_size = 3, activation='relu'))
    model[j].add(BatchNormalization())
    model[j].add(Conv2D(32, kernel_size = 5, strides=2, padding='same', activation='relu'))
    model[j].add(BatchNormalization())
    model[j].add(Dropout(0.1))

    model[j].add(Conv2D(64, kernel_size = 3, activation='relu'))
    model[j].add(BatchNormalization())
    model[j].add(Conv2D(64, kernel_size = 3, activation='relu'))
    model[j].add(BatchNormalization())
    model[j].add(Conv2D(64, kernel_size = 5, strides=2, padding='same', activation='relu'))
    model[j].add(BatchNormalization())
    model[j].add(Dropout(0.15))

    model[j].add(Conv2D(128, kernel_size = 4, activation='relu'))
    model[j].add(BatchNormalization())
    model[j].add(Flatten())
    model[j].add(Dropout(0.2))
    model[j].add(Dense(10, activation='softmax'))

    #Compile all the pieces of our model together
    model[j].compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

model[0].summary()


# The models are trained using a decaying learning rate. The number of epochs was set to 30 in the interest of having time to build 3 nets in the competitions runtime. Better results can be achieved by increasing this number. There is also room to experiment with early stopping. 

# In[ ]:


decay = LearningRateScheduler(lambda x: 1e-3 * 0.95 ** x)
epochs = 30
batch_size = 64

history = [0] * nets
for j in range(nets):
    
    ##Train the models using different subsets of the training data
    X_train2, X_val2, Y_train2, Y_val2 = train_test_split(X_train, Y_train, test_size = 0.1)
    history[j] = model[j].fit_generator(datagen.flow(X_train2, Y_train2, batch_size=batch_size),                                        epochs = epochs,steps_per_epoch = X_train2.shape[0]//64,                                        validation_data = (X_val2,Y_val2),callbacks = [decay], verbose = True)
    ##Save the model output incase we want to reuse it later
    model_json = model[j].to_json()
    with open("model"+str(j)+".json", "w") as json_file:
        json_file.write(model_json)
        # serialize weights to HDF5
    model[j].save_weights("modelw"+str(j)+".h5")
    print("Saved model to disk")


# **Let's make some predictions!** 
# This is the easy bit - now we just let each of the models make it's predction and add them all together. We choose the highest score from the result as our final prediction. 

# In[ ]:


##Initialise a matrix with rows = number of test images and columns = number of classifications (10)
predictions = np.zeros( (X_test.shape[0],10) ) 

##Loop through the different Neural networks to add together the predictions
for j in range(nets):
    predictions = predictions + model[j].predict(X_test)
    
test_labels = np.argmax(predictions, axis=1)

submission = pd.DataFrame(test_labels)
submission.index = test_id
submission.columns = ["label"]
submission.to_csv("submission.csv")


# **Results** 
# 
# Running this piece as it is resulted in a score of 98.6%. Like mentioned previously I've since used essentially the same code with an increase in both epochs and models and that has provided an accuracy of 98.9%. 
# 
# Note that since the competition only allows a certain amount of compute time for more complicated models I've found running multiple commits and saving the models as outputs works best. Then the models can be read back in for the final run. This process is outlined here https://jovianlin.io/saving-loading-keras-models/. 
# 
# Ideas for the future: 
# * Changing the model architecture and transformation parameters. This architecture was chosen as it performed well on the original MNIST set, but might not be the best choice for this set. 
# 
# Let me know your thoughts and suggestions! 
