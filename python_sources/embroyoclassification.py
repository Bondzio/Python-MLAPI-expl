#!/usr/bin/env python
# coding: utf-8

# In[69]:


import numpy as np
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense, Flatten, Dropout
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import *
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from IPython.display import display
from sklearn.preprocessing import LabelEncoder
#from PIL import Image
import itertools
get_ipython().run_line_magic('matplotlib', 'inline')


# In[70]:


train_path = '../input/embryosdataset/embryosdataset/train'
test_path = '../input/embryosdataset/embryosdataset/test'


# In[71]:


train_batches = ImageDataGenerator().flow_from_directory(train_path, target_size=(224,224), classes=['control', 'mutant'], batch_size=31)
test_batches = ImageDataGenerator().flow_from_directory(test_path, target_size=(224,224), classes=['control', 'mutant'], batch_size=17)


# In[72]:


def plots(ims, figsize=(12,6), rows=1, interp=False, titles=None):
    if type(ims[0]) is np.ndarray:
        ims = np.array(ims).astype(np.uint8)
        if (ims.shape[-1] != 3):
            ims = ims.transpose((0,2,3,1))
    f = plt.figure(figsize=figsize)
    cols = len(ims)//rows if len(ims) % 2 == 0 else len(ims)//rows + 1
    for i in range(len(ims)):
        sp = f.add_subplot(rows, cols, i+1)
        sp.axis('Off')
        if titles is not None:
            sp.set_title(titles[i], fontsize=16)
        plt.imshow(ims[i], interpolation=None if interp else 'none')


# In[73]:


import sys
from PIL import Image
sys.modules['Image'] = Image 
print(Image.__file__)
import Image
print(Image.__file__)

test_imgs, test_lables = next(train_batches)
plots(test_imgs, titles=test_lables, rows=2)


# In[75]:


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# In[76]:


vgg16_model = keras.applications.vgg16.VGG16()
vgg16_model.summary()


# In[77]:


model = Sequential()
for i in range(0, len(vgg16_model.layers)-1):
    layer = vgg16_model.layers[i]
    model.add(layer)
model.summary()


# In[78]:


len(model.layers)


# In[79]:


for i in range(0, len(model.layers)):
    print(i)
    layer = model.layers[i]
    print(layer)
    layer.trainable = False
# model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))


# In[80]:


model.summary()


# In[81]:


model.compile(Adam(lr=0.0001), loss='binary_crossentropy', metrics=['accuracy'])


# In[82]:


model.fit_generator(train_batches, steps_per_epoch = 6,
                   validation_steps = 5, epochs = 25, verbose = 1)


# In[83]:


test_imgs, test_lables = next(test_batches)
plots(test_imgs, titles=test_lables)


# In[84]:


test_lables = test_lables[:,0]
test_lables


# In[85]:


predictions = model.predict_generator(test_batches, steps=1, verbose=2)
predictions


# In[86]:


cm = confusion_matrix(test_lables, np.round(predictions[:,0]))
cm_plot_labels = ['control', 'mutant']
plot_confusion_matrix(cm, cm_plot_labels, title='Confusion Matrix')


# In[ ]:




