#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[ ]:


# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

# data visualisation and manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
 
#configure
# sets matplotlib to inline and displays graphs below the corressponding cell.
get_ipython().run_line_magic('matplotlib', 'inline')
style.use('fivethirtyeight')
sns.set(style='whitegrid',color_codes=True)

#model selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix,roc_curve,roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder

#preprocess.
from keras.preprocessing.image import ImageDataGenerator

#dl libraraies
from keras import backend as K
from keras import regularizers
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
from keras.optimizers import Adam,SGD,Adagrad,Adadelta,RMSprop
from keras.utils import to_categorical
from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import ModelCheckpoint

# specifically for cnn
from keras.layers import Dropout, Flatten,Activation
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.layers import InputLayer
 
import tensorflow as tf
import random as rn

# specifically for manipulating zipped images and getting numpy arrays of pixel values of images.
import cv2                  
import numpy as np  
from tqdm import tqdm
import os                   
from random import shuffle  
from zipfile import ZipFile
from PIL import Image

#TL pecific modules
#from keras.applications.resnet50 import ResNet50
#from keras.applications.vgg16 import VGG16
get_ipython().system('pip install keras_vggface')
from keras_vggface.vggface import VGGFace


# In[ ]:


os.listdir('../input/humain/dataset')


# In[ ]:


def assign_label(img,label):
    return label


# In[ ]:


def make_train_data(label,DIR):
    for img in tqdm(os.listdir(DIR)):
        path = os.path.join(DIR,img)
        img = cv2.imread(path,cv2.IMREAD_COLOR)
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
        
        X.append(np.array(img))
        Z.append(str(label))


# ### **Importing Pre-trained Model VGG Face for Transfer Learning**

# In[ ]:


base_model=VGGFace(include_top=False, weights=None,input_shape=(150,150,3), pooling='avg')

weights_path='../input/humain/dataset/vgg_face_weights.h5' # 16 to 13 layers
base_model.load_weights(weights_path,by_name='True') 


# ## Ethnicity Model
# 
# There will be 4 seperate models trained to predict age, gender, ethnicity and emotion.
# 
# Training Approach : Transfer learning on a pre-trained vggface convolutional neural network.

# In[ ]:


X=[]
Z=[]
IMG_SIZE=150
ETHNICITY_ARAB_DIR='../input/humain/dataset/ethnicity/E_Arab'
ETHNICITY_ASIAN_DIR='../input/humain/dataset/ethnicity/E_Asian'
ETHNICITY_BLACK_DIR='../input/humain/dataset/ethnicity/E_Black'
ETHNICITY_HISPANIC_DIR='../input/humain/dataset/ethnicity/E_Hispanic'
ETHNICITY_INDIAN_DIR='../input/humain/dataset/ethnicity/E_Indian'
ETHNICITY_WHITE_DIR='../input/humain/dataset/ethnicity/E_White'

make_train_data('Arab',ETHNICITY_ARAB_DIR)
make_train_data('Asian',ETHNICITY_ASIAN_DIR)
make_train_data('Black',ETHNICITY_BLACK_DIR)
make_train_data('Hispanic',ETHNICITY_HISPANIC_DIR)
make_train_data('Indian',ETHNICITY_INDIAN_DIR)
make_train_data('White',ETHNICITY_WHITE_DIR)


# In[ ]:


fig,ax=plt.subplots(2,5)
plt.subplots_adjust(bottom=0.3, top=0.7, hspace=0)
fig.set_size_inches(10,10)

for i in range(2):
    for j in range (5):
        l=rn.randint(0,len(Z))
        ax[i,j].imshow(X[l][:,:,::-1])
        ax[i,j].set_title(Z[l])
        ax[i,j].set_aspect('equal')


# In[ ]:


le=LabelEncoder()
Y=le.fit_transform(Z)
Y=to_categorical(Y,6)
X=np.array(X)
X=X/255

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25,random_state=1337)

np.random.seed(42)
rn.seed(42)
tf.set_random_seed(42)


# In[ ]:


ethnicitymodel=Sequential()
ethnicitymodel.add(base_model)
#ethnicitymodel.add(Dropout(0.3))
ethnicitymodel.add(Dense(512,activation='relu'))
# ethnicitymodel.add(Dropout(0.25))
ethnicitymodel.add(Dense(256,activation='relu'))
# ethnicitymodel.add(Dropout(0.20))
ethnicitymodel.add(Dense(128,activation='relu'))#, kernel_regularizer=regularizers.l2(0.001), activity_regularizer=regularizers.l1(0.001)))
# ethnicitymodel.add(Dropout(0.15))
ethnicitymodel.add(Dense(64,activation='relu'))
ethnicitymodel.add(Dense(6,activation='softmax'))


# ### **Data Augmentation **

# In[ ]:


datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=10,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range = 0.1, # Randomly zoom image 
        width_shift_range=0.2,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.2,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images


datagen.fit(x_train)


# ### Model Architechture

# In[ ]:


epochs=200
batch_size=32
#red_lr=ReduceLROnPlateau(monitor='val_acc', factor=0.9, min_delta=0.001, patience=5,min_lr=1e-10, verbose=1)

base_model.trainable=True # setting the VGG model to be trainable.
ethnicitymodel.summary()


# ### Training Model

# In[ ]:


checkpoint = ModelCheckpoint('../working/ethnicity_model.h5', monitor='val_accuracy', verbose=1, save_best_only=True, mode='min')

callbacks_list = [checkpoint] #,red_lr]

ethnicitymodel.compile(optimizer=Adam(lr=1e-3),loss='categorical_crossentropy',metrics=['accuracy'])

History = ethnicitymodel.fit_generator(datagen.flow(x_train,y_train, batch_size=batch_size),
                              epochs = epochs, validation_data = (x_test,y_test),
                              verbose = 1, steps_per_epoch=x_train.shape[0] // batch_size,callbacks=callbacks_list)

ethnicitymodel.save('../working/ethnicitymodel.h5')


# In[ ]:


plt.plot(History.history['acc'])
plt.plot(History.history['val_acc'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend(['train', 'test'])
plt.show()


# In[ ]:


plt.plot(History.history['loss'])
plt.plot(History.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend(['train', 'test'])
plt.show()


# In[ ]:




