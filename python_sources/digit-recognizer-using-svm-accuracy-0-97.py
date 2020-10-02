#!/usr/bin/env python
# coding: utf-8

# # HANDWRITTEN DIGITS CLASSIFICATION (MNIST DATASET)

# ## IMPORTING LIBRARIES

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC


# In[ ]:


sns.set(rc={'figure.figsize':(10.75,6.5)})
sns.set_style('whitegrid')


# ## Reading the MNIST Train Dataset

# In[ ]:


mnist_data=pd.read_csv('/kaggle/input/digit-recognizer/train.csv')


# ### COUNT PLOT OF THE DIGITS RANGING 0-9 

# In[ ]:


sns.countplot(x='label',data=mnist_data);


# ### SPLITTING THE DATASET INTO FEATURES (PIXELS) AND ACTUAL DIGITS (LABELS)

# In[ ]:


pixels_data=mnist_data.drop('label',axis=1)
labels_data = mnist_data['label']


# In[ ]:


pixels_data.shape #Total pixels=784, needs to reshape into 28x28 to view the actual image


# ### SOME SAMPLE IMAGES

# In[ ]:


fig1, ax=plt.subplots(5, 12,figsize=(18,6))
ax=ax.reshape(-1)

img_no=0
for i in range(len(ax)):
    image=pixels_data.iloc[img_no,:].to_numpy().reshape(28,28)
    ax[i].set_xticks([])
    ax[i].set_yticks([])
    ax[i].imshow(image,cmap=matplotlib.cm.binary)
    img_no=random.randint(0,len(pixels_data.index)-1)


# ## FITTING THE PIXELS INTO SVM MODEL

# In[ ]:


SVMmodel=SVC(kernel='rbf').fit(pixels_data, labels_data)


# ## Reading the MNIST Test Dataset having 784 pixels of images without any actual labels of digits

# In[ ]:


test_pixels_data=pd.read_csv('/kaggle/input/digit-recognizer/test.csv')
test_pixels_data.shape


# ## PREDICTING SOME RANDOM SAMPLE IMAGES FROM TEST DATASET

# In[ ]:


fig2,axes = plt.subplots(4,7,figsize=(35,26))
axes=axes.reshape(-1)
fig2.suptitle('THE IMAGES REPRESENTS THE HANDWRITTEN DIGITS AND THEIR TITLE INDICATES THE PREDICTED DIGIT',fontsize=40)
#plt.subplots_adjust(top=0.83)

test_img_no=0
for i in range(len(axes)):
    test_image=test_pixels_data.iloc[test_img_no,:].to_numpy().reshape(28,28)
    test_image_data=test_pixels_data.iloc[test_img_no,:].to_numpy().reshape(1,-1)
    pred_digit=SVMmodel.predict(test_image_data)
    axes[i].set_title('Predicted Digit: {}'.format(pred_digit[0]),fontsize=30)
    axes[i].set_xticks([])
    axes[i].set_yticks([])
    axes[i].imshow(test_image,cmap=matplotlib.cm.binary)
    test_img_no=random.randint(0,len(test_pixels_data.index)-1)

