#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys
import pickle
from random import randint,seed
import numpy as np
import pandas as pd
from PIL import Image, ImageFilter
import seaborn as sns
sns.set(style='white')
from ipywidgets import IntSlider
from tqdm import tqdm_notebook
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error, log_loss, confusion_matrix
import matplotlib.pyplot as plt
np.seterr(all='ignore')
# np.random.seed(100)
# threshold=50
BCH=2  #batch size for visualisation
LEVEL = 'level_3'


# In[ ]:


class SigmoidNeuron:
  
  def __init__(self):
    self.w = None
    self.b = None
    
  def perceptron(self, x):
    return np.dot(x, self.w.T) + self.b
  
  def sigmoid(self, x):
    return 1.0/(1.0 + np.exp(-x))
  
  def grad_w_mse(self, x, y):
    y_pred = self.sigmoid(self.perceptron(x))
    return (y_pred - y) * y_pred * (1 - y_pred) * x
  
  def grad_b_mse(self, x, y):
    y_pred = self.sigmoid(self.perceptron(x))
    return (y_pred - y) * y_pred * (1 - y_pred)
  
  def grad_w_ce(self, x, y):
    y_pred = self.sigmoid(self.perceptron(x))
    if y == 0:
      return y_pred * x
    elif y == 1:
      return -1 * (1 - y_pred) * x
    else:
      raise ValueError("y should be 0 or 1")
    
  def grad_b_ce(self, x, y):
    y_pred = self.sigmoid(self.perceptron(x))
    if y == 0:
      return y_pred 
    elif y == 1:
      return -1 * (1 - y_pred)
    else:
      raise ValueError("y should be 0 or 1")
  
  def fit(self, X, Y, epochs=1, learning_rate=1, initialise=True, loss_fn="mse", display_loss=False):
    
    # initialise w, b
    if initialise:
      self.w = np.random.randn(1, X.shape[1])
      self.b = 0
      
    if display_loss:
      loss = {}
    
    for i in tqdm_notebook(range(epochs), total=epochs, unit="epoch"):
      dw = 0
      db = 0
      for x, y in zip(X, Y):
        if loss_fn == "mse":
          dw += self.grad_w_mse(x, y)
          db += self.grad_b_mse(x, y) 
        elif loss_fn == "ce":
          dw += self.grad_w_ce(x, y)
          db += self.grad_b_ce(x, y)
      self.w -= learning_rate * dw
      self.b -= learning_rate * db
      
      if display_loss:
        Y_pred = self.sigmoid(self.perceptron(X))
        if loss_fn == "mse":
          loss[i] = mean_squared_error(Y, Y_pred)
        elif loss_fn == "ce":
          loss[i] = log_loss(Y, Y_pred)
    
    if display_loss:
      plt.plot(loss.values())
      plt.xlabel('Epochs')
      if loss_fn == "mse":
        plt.ylabel('Mean Squared Error')
      elif loss_fn == "ce":
        plt.ylabel('Log Loss')
      plt.show()
      
  def predict(self, X):
    Y_pred = []
    for x in X:
      y_pred = self.sigmoid(self.perceptron(x))
      Y_pred.append(y_pred)
    return np.array(Y_pred)


# # Some Image Processing Steps:

# Choosing a set of random image and plotting them. First row would be `greyscaled image`, followed by the `transformed image` for every folder. 2 such batches are created. 

# In[ ]:


seed(10)
for i in range(BCH):
    image_folder = ['background','hi', 'ta', 'en']
    path= '../input/level_3_train/level_3/'
    def path_fun(folder_name):
        full_path= path+folder_name+'/'
        image_name_list=os.listdir(full_path)
        return full_path+image_name_list[randint(0,len(image_name_list))]
    fig,ax= plt.subplots(8,18,figsize=(15,10))
    c=0
    # import pdb; pdb.set_trace()
    for level in range(0,8,2):

        for col in range(18):
    #         if level==2 and col==4:
    #             print(path_fun(image_folder[c]))
            ax[level,col].set_yticklabels([])
            ax[level,col].set_xticklabels([])
            nis=Image.open(path_fun(image_folder[c])).convert('L')
            ax[level,col].imshow(nis)

    #         nis=nis.filter(ImageFilter.UnsharpMask(2,10,10))  
    
            my_data= np.array(nis)
            my_data=np.where(my_data>10,255,my_data)  
            
            #Since most of the images have 
            #dark texts,thus selecting all those pixels that are greater than 10 intensity and 
            #replacing them with white does filter most of the background noise. However, this 
            #would also filter out many blurred texts. Also, many such images where black pixels
            #are randomly spread will still stay.
            
            filtered_image=Image.fromarray(my_data)
            ax[1+level,col].set_yticklabels([])
            ax[1+level,col].set_xticklabels([])
            ax[1+level,col].imshow(filtered_image)
        c+=1


# In[ ]:


def read_all(folder_path, key_prefix=""):
    '''
    It returns a dictionary with 'file names' as keys and 'flattened image arrays' as values.
    '''
    print("Reading:")
    images = {}
    files = os.listdir(folder_path)
    for i, file_name in tqdm_notebook(enumerate(files), total=len(files)):
        file_path = os.path.join(folder_path, file_name)
        image_index = key_prefix + file_name[:-4]
        image = Image.open(file_path)
        image = image.convert("L")
        

#         image=image.filter(ImageFilter.UnsharpMask(2,10,10))
 

        my_data= np.array(image)
        my_data=np.where(my_data>10,255,my_data)
        image = Image.fromarray(my_data)
        
        images[image_index] = np.array(image.copy()).flatten()
        image.close()
    return images


# In[ ]:



# nis0=Image.open('../input/level_2_train/level_2/background/100_d2.jpg').convert('L')

# nis1=Image.open('../input/level_2_train/level_2/hi/c0_84.jpg').convert('L')

# # nis1=nis1.filter(ImageFilter.UnsharpMask(2,10,10))

# # my_data= np.array(nis0)
    
# # my_data=np.where(my_data>45,255,my_data)

# # Image.fromarray(my_data)
# plt.imshow(nis1)


# In[ ]:





# In[ ]:


languages = ['ta', 'hi', 'en']

images_train = read_all("../input/level_3_train/"+LEVEL+"/"+"background", key_prefix='bgr_') # change the path
for language in languages:
    images_train.update(read_all("../input/level_3_train/"+LEVEL+"/"+language, key_prefix=language+"_" ))
print(len(images_train))

images_test = read_all("../input/level_3_test/kaggle_"+LEVEL, key_prefix='') # change the path
print(len(images_test))


# In[ ]:


list(images_test.keys())[:5]


# In[ ]:


X_train = []
Y_train = []
for key, value in images_train.items():
    X_train.append(value)
    if key[:4] == "bgr_":
        Y_train.append(0)
    else:
        Y_train.append(1)

ID_test = []
X_test = []
for key, value in images_test.items():
  ID_test.append(int(key))
  X_test.append(value)
  
        
X_train = np.array(X_train)
Y_train = np.array(Y_train)
X_test = np.array(X_test)

print(X_train.shape, Y_train.shape)
print(X_test.shape)


# In[ ]:


scaler = StandardScaler()
X_scaled_train = scaler.fit_transform(X_train)
X_scaled_test = scaler.transform(X_test)


# In[ ]:


# sn_mse = SigmoidNeuron()
# sn_mse.fit(X_scaled_train, Y_train, epochs=500, learning_rate=0.0015, loss_fn="mse", display_loss=True)


# In[ ]:


sn_ce = SigmoidNeuron()
sn_ce.fit(X_scaled_train, Y_train, epochs=300, learning_rate=0.07, loss_fn="ce", display_loss=True)


# In[ ]:


def print_accuracy(sn):
  Y_pred_train = sn.predict(X_scaled_train)
  Y_pred_binarised_train = (Y_pred_train >= 0.5).astype("int").ravel()
  accuracy_train = accuracy_score(Y_pred_binarised_train, Y_train)
  sns.heatmap(confusion_matrix(Y_pred_binarised_train,Y_train),annot=True)
  print("Train Accuracy : ", accuracy_train)
  print("-"*50)


# In[ ]:


# print_accuracy(sn_mse)
print_accuracy(sn_ce)


# 

# ## Sample Submission

# In[ ]:


Y_pred_test = sn_ce.predict(X_scaled_test)
Y_pred_binarised_test = (Y_pred_test >= 0.5).astype("int").ravel()

submission = {}
submission['ImageId'] = ID_test
submission['Class'] = Y_pred_binarised_test

submission = pd.DataFrame(submission)
submission = submission[['ImageId', 'Class']]
submission = submission.sort_values(['ImageId'])
submission.to_csv("submisision.csv", index=False)


# In[ ]:




