#!/usr/bin/env python
# coding: utf-8

# ## Blur Detection via Classification

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
import matplotlib.pyplot as plt
import cv2
import sklearn
import seaborn as sb

from skimage.color import rgb2gray
from skimage.filters import laplace, sobel, roberts
# Any results you write to the current directory are saved as output.


# #### Features selected:
# The images losses it's edges due to defocus and so the features are selected as edges through sobel and laplacian operators

# **Sobel Edge operator**
# It is a edge detection operator based on gradient method i.e., the first order derivative method. Along x or along y or bi-directional. The edges are detected by convolving the kernel with actual image.
# The sobel operator kernel used here is bi-directional
# 
# **Roberts Edge Operator**
# It is similar to Sobel operator gives the gradient magnitude highlighting the edges
# 
# **Laplacian Edge operator**
# It is also an edge detection operator based on gradient methos but it calculated the second dervative od the data . It internally calls the sobel operator for first derivative.
# 
# **Why Derivative?**
# The edges can be deteced by finding the local maxima or minima of it's first derivative
# The edges can be deteced by finding the zero-crossing of it's second derivative 
# 

# In[ ]:


print('Sobel operator:\n',np.matrix([[1,0,-1],[2,0,-2],[1,0,-1]]))
print('Laplacian operator:\n',np.matrix([[0,-1,0],[-1,4,-1],[0,-1,0]]))


# #### Dataset:
# It is a image blur data from kaggle and it has 3 types of a same image
# 1. Sharp image 
# 2. Defocused image
# 3. Motion blurred image

# In[ ]:


s_path ='../input/blur_dataset_scaled/sharp/'
df_path='../input/blur_dataset_scaled/defocused_blurred/'
mot_path ='../input/blur_dataset_scaled/motion_blurred/'

img_paths = ['../input/blur_dataset_scaled/sharp/89_IPHONE-6S_S.jpeg','../input/blur_dataset_scaled/defocused_blurred/89_IPHONE-6S_F.jpeg','../input/blur_dataset_scaled/motion_blurred/89_IPHONE-6S_M.jpeg']
 
def show_images(path):
    plt.figure(figsize=(10,10))
    for i in range(len(path)):
        x=plt.imread(path[i])
        plt.subplot(1, 3, i+1)
        plt.imshow(x)
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout()
    plt.show()
show_images(img_paths)


# ### Laplacian feature visualization

# In[ ]:


def show_images(path):
    plt.figure(figsize=(10,10))
    for i in range(len(path)):
        x=cv2.imread(path[i],0)
        l = laplace(x)
        plt.subplot(1, 3, i+1)
        plt.imshow(l,cmap='gray')
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout()
    plt.show()
show_images(img_paths)


# ### Sobel feature visualization

# In[ ]:


def show_images(path):
    plt.figure(figsize=(10,10))
    for i in range(len(path)):
        x=cv2.imread(path[i],0)
        l = sobel(x)
        plt.subplot(1, 3, i+1)
        plt.imshow(l,cmap='gray')
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout()
    plt.show()
show_images(img_paths)


# ### Roberts feature visualization

# In[ ]:


def show_images(path):
    plt.figure(figsize=(10,10))
    for i in range(len(path)):
        x=cv2.imread(path[i],0)
        l = roberts(x)
        plt.subplot(1, 3, i+1)
        plt.imshow(l,cmap='gray')
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout()
    plt.show()
show_images(img_paths)


# In[ ]:


sharp_images = os.listdir(s_path)
defocused = os.listdir(df_path)
motion_blurred = os.listdir(mot_path)


# In[ ]:


def get_data(path,images):
    features=[]
    for img in images:
        feature=[]
        image_gray = cv2.imread(path+img,0)
        lap_feat = laplace(image_gray)
        sob_feat = sobel(image_gray)
        rob_feat = roberts(image_gray)
        feature.extend([img,lap_feat.mean(),lap_feat.var(),np.amax(lap_feat),
                        sob_feat.mean(),sob_feat.var(),np.max(sob_feat),
                        rob_feat.mean(),rob_feat.var(),np.max(rob_feat)])
        
        features.append(feature)
    return features


# ### Feature Engineering:
# The mean, variance,maximum of the edge detected feature matrix are take for each image applied on sobel and lapaclacian edge detection

# In[ ]:


sharp_features = get_data(s_path,sharp_images)
defocused_features = get_data(df_path,defocused)
motion_blur_features = get_data(mot_path,motion_blurred)


# In[ ]:


sharp_df = pd.DataFrame(sharp_features)
sharp_df.drop(0,axis=1,inplace=True)
sharp_df.head()


# In[ ]:


defocused_df = pd.DataFrame(defocused_features)
defocused_df.drop(0,axis=1,inplace=True)
defocused_df.head()


# In[ ]:


motion_df = pd.DataFrame(motion_blur_features)
motion_df.drop(0,axis=1,inplace=True)
motion_df.head()


# In[ ]:


label = ['Sharp_images','Defocused_images','Mtion_blurred_images']
no_images=[len(sharp_features),len(defocused_features),len(motion_blur_features)]


# In[ ]:


def plot_bar_x():
    # this is for plotting purpose
    index = np.arange(len(label))
    plt.bar(index, no_images)
    plt.xlabel('Image_type', fontsize=10)
    plt.ylabel('No of Images', fontsize=10)
    plt.xticks(index, label, fontsize=10, rotation=0)
    plt.title('Data Visualization')
    plt.show()
plot_bar_x()


# ### Support Vector Machine

# A Support Vector Machine (SVM) is a discriminative classifier formally defined by a separating hyperplane. In other words, given labeled training data (supervised learning), the algorithm outputs an optimal hyperplane which categorizes new examples. In two dimentional space this hyperplane is a line dividing a plane in two parts where in each class lay in either side.

# It has two types
# 1. HArd Margin - the data can be classified by a line or hyperplane but without error added to the algorithm
# 2. Soft margin -  the data can be classified by a line or hyperplane but with error added to the algorithm
# 
# If the data cannot be clssified by a line .. It maps the data to higher dimension where it can calssify using the plane/ hyperplane
# 

# **Lets try the classification between sharp and defocused**

# In[ ]:


from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score, classification_report
images=pd.DataFrame()

images = images.append(sharp_df)
images = images.append(defocused_df)
all_features = np.array(images)
y_f = np.concatenate((np.ones((sharp_df.shape[0], )), np.zeros((defocused_df.shape[0], ))), axis=0)

x_train,x_valid,y_train,y_valid = train_test_split(all_features,y_f,test_size=0.33,stratify=y_f)

svm_model = svm.SVC(C=100,kernel='linear')
svm_model.fit(x_train,y_train)
pred =svm_model.predict(x_valid)
print('Accuracy:',accuracy_score(y_valid,pred))
print('Confusion matrix:\n',confusion_matrix(y_valid,pred))
print('F1_score:',f1_score(y_valid,pred))
print('Classification_report:\n',classification_report(y_valid,pred))


# Change the kernel as one of the best non-linear kernel 'rbf'

# In[ ]:


svm_model = svm.SVC(C=100,kernel='rbf')
svm_model.fit(x_train,y_train)
pred =svm_model.predict(x_valid)
print('Accuracy:',accuracy_score(y_valid,pred))
print('Confusion matrix:\n',confusion_matrix(y_valid,pred))
print('F1_score:',f1_score(y_valid,pred))
print('Classification_report:\n',classification_report(y_valid,pred))


# **Lets try the classification between sharp and 'defocused & motion-blur'**

# In[ ]:


images=pd.DataFrame()

images = images.append(sharp_df)
images = images.append(defocused_df)
images = images.append(motion_df)
all_features = np.array(images)
y_f = np.concatenate((np.ones((sharp_df.shape[0], )), np.zeros((defocused_df.shape[0]+motion_df.shape[0], ))), axis=0)

x_train,x_valid,y_train,y_valid = train_test_split(all_features,y_f,test_size=0.33,stratify=y_f)

svm_model = svm.SVC(C=100,kernel='rbf')
svm_model.fit(x_train,y_train)
pred =svm_model.predict(x_valid)
print('Accuracy:',accuracy_score(y_valid,pred))
print('Confusion matrix:\n',confusion_matrix(y_valid,pred))
print('F1_score:',f1_score(y_valid,pred))
print('Classification_report:\n',classification_report(y_valid,pred))


# This is because the features extracted are not much of a difference between motion blurred and the sharp images

# **Lets try the classification between all the three**

# In[ ]:


from keras.utils import to_categorical
images=pd.DataFrame()

images = images.append(sharp_df)
images = images.append(defocused_df)
images = images.append(motion_df)
all_features = np.array(images)
y_f = np.concatenate((np.zeros((sharp_df.shape[0], )), np.ones((defocused_df.shape[0], )), 2*np.ones((motion_df.shape[0], ))), axis=0)

x_train,x_valid,y_train,y_valid = train_test_split(all_features,y_f,test_size=0.33,stratify=y_f)

svm_model = svm.SVC(C=100,kernel='rbf')
svm_model.fit(x_train,y_train)
pred =svm_model.predict(x_valid)
print('Accuracy:',accuracy_score(y_valid,pred))
print('Confusion matrix:\n',confusion_matrix(y_valid,pred))
y_valid_cat = to_categorical(y_valid, num_classes=3)
pred_cat = to_categorical(pred, num_classes=3)
print('F1_score:',f1_score(y_valid_cat,pred_cat, average='weighted'))
print('Classification_report:\n',classification_report(y_valid_cat,pred_cat))


# ## *If you like it, please UPVOTE*
