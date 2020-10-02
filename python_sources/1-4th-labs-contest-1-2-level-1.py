#!/usr/bin/env python
# coding: utf-8

# # Import required Libraries.

# In[ ]:


import os
import sys
import pickle
import numpy as np
import pandas as pd
from PIL import Image, ImageFilter
from tqdm import tqdm_notebook
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, log_loss, confusion_matrix
import matplotlib.pyplot as plt
import random
import warnings

warnings.filterwarnings('ignore') # Supress Warnings.
np.random.seed(100)
LEVEL = 'level_1'


# <hr>

# # Read image files to arrays.

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
        images[image_index] = np.array(image.copy()).flatten()
        image.close()
    return images


# In[ ]:


languages = ['ta', 'hi', 'en']

images_train = read_all("../input/level_1_train/"+LEVEL+"/"+"background", key_prefix='bgr_') 
for language in languages:
 images_train.update(read_all("../input/level_1_train/"+LEVEL+"/"+language, key_prefix=language+"_" ))
print(len(images_train))

images_test = read_all("../input/level_1_test/kaggle_"+LEVEL, key_prefix='') 
print(len(images_test))


# In[ ]:


list(images_test.keys())[:5] # View first five keys for images in the test set


# # Create train and test set.

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


# # Scale the data.

# In[ ]:


scaler = StandardScaler()
X_scaled_train = scaler.fit_transform(X_train)
X_scaled_test = scaler.transform(X_test)


# <hr>

# # Create Model.

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


# # Instantiate and Fit Model.
# 1. Loss function: Mean-squared error.[](http://)

# In[ ]:


sn_mse = SigmoidNeuron()
sn_mse.fit(X_scaled_train, Y_train, epochs=100, learning_rate=0.1, loss_fn="mse", display_loss=True)


# 2. Loss function: Cross-entropy.

# In[ ]:


sn_ce = SigmoidNeuron()
sn_ce.fit(X_scaled_train, Y_train, epochs=100, learning_rate=0.1, loss_fn="ce", display_loss=True)


# In[ ]:


# Calculate accuracy
def cal_accuracy(sn, X, y, prob_thres=0.5):
  y_pred = sn.predict(X)
  y_pred_binarised = (y_pred >= prob_thres).astype("int").ravel()
  accuracy = accuracy_score(y_pred_binarised, y)
  return accuracy


# In[ ]:


print('Train Accuracy when loss function is mean squared error: ', cal_accuracy(sn_mse, X_scaled_train, Y_train))
print('Train Accuracy when loss function is cross-entropy: ', cal_accuracy(sn_ce, X_scaled_train, Y_train))


# <hr>

# # k-Fold Cross-Validation.

# In[ ]:


def cross_val(estimator, X, y, k=5, epochs=100, lr=0.1, loss_fn='ce', prob_thres=0.5, display_loss=True):

    # Split the data in k-folds
    population = range(X.shape[0]) # Number of rows in X_train
    rand_indices = random.sample(population, X.shape[0])
    k = k # k-splits.
    X_split = np.array(np.split(X[rand_indices], k)) # k random splits of X
    y_split = np.array(np.split(y[rand_indices], k)) # k random splits of y
    train_acc = np.empty((0)); test_acc = np.empty((0)) # Here we store the accuracy for different folds
    
    # Fit and predict on k different train and test folds
    for i in range(k):
        
        # Create train and test sets for different folds
        k_X_test = X_split[i]; k_y_test = y_split[i] # cross-validation test set
        train_indices = list(range(k)); train_indices.remove(i)
        k_X_train = np.empty((0, k_X_test.shape[1])); k_y_train = np.empty((0)) 
        for j in train_indices:
            k_X_train = np.vstack((k_X_train, X_split[j])); k_y_train = np.hstack((k_y_train, y_split[j])) # train set for k-fold

        # Fit data to model.
        estimator.fit(k_X_train, k_y_train, epochs=epochs, learning_rate=lr, loss_fn=loss_fn, display_loss=display_loss)
        # Calculate the train and test accuracy on validation set
        train_acc = np.hstack((train_acc, cal_accuracy(estimator, k_X_train, k_y_train, prob_thres=prob_thres)))
        test_acc = np.hstack((test_acc, cal_accuracy(estimator, k_X_test, k_y_test, prob_thres=prob_thres)))
        
    print('Mean Train Accuracy: ', np.mean(train_acc))
    print('Mean Test Accuracy: ', np.mean(test_acc))
    return([np.mean(train_acc), np.mean(test_acc)])


# In[ ]:


cross_val(SigmoidNeuron(), X_scaled_train, Y_train, epochs=200, lr=0.5, display_loss=False)


# In[ ]:


cross_val(SigmoidNeuron(), X_scaled_train, Y_train, epochs=200, lr=0.5, loss_fn='mse', display_loss=False)


# **5-fold cross validation.**
# 1.  When running 200 epochs at a learning rate of 0.5, loss funcion set to 'cross-entropy' and probability threshold set to 0.5, I am getting a mean accuracy of 100% on train set and 97 to 98% accuracy on test set when doing cross-validation.<br>
# 2. Keeping all the other parameters constant and changing only loss function to 'mean squared error' leads to a train accuracy of around 96 to 97% and test accuracy of around 95%.<br><br>
# *When observing the above metrics, it seems that for same number of epochs and learning rate cross-entropy error shows better performance than means squared error.*<br>
# *Also not that, these accuracy scores will be different every time you run `cross_val` function, because k-splits are done randomly.*

# <hr>
# # Selecting Probability Threshold.

# In[ ]:


cutoff_df = pd.DataFrame(columns=['prob', 'train_acc', 'test_acc'])
num = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
for i, prob in enumerate(num):
    acc = cross_val(SigmoidNeuron(), X_scaled_train, Y_train, epochs=200, lr=0.5, prob_thres=prob, display_loss=False) # get train and test accuracies
    cutoff_df = cutoff_df.append({'prob': prob, 'train_acc': acc[0], 'test_acc': acc[1]}, ignore_index=True)


# In[ ]:


# Different probabilites and their train and test accuracies
print(cutoff_df)
print('Row with maximum test accuracy:\n', cutoff_df.iloc[cutoff_df[['test_acc']].idxmax()])
cutoff_df.plot.line(x='prob', y=['train_acc', 'test_acc'])
plt.show()


# Maximum test accuracy is obtained at a probability threshold of 0.4. Now, we need to prepare a final model with this threshold.

# <hr>
# # Prepare Final Model.

# In[ ]:


# Do train-test split
X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(X_scaled_train, Y_train, train_size=0.7, test_size=0.3, random_state=123, stratify=Y_train)


# In[ ]:


sn = SigmoidNeuron()
sn.fit(X_train_f, y_train_f, epochs=200, learning_rate=0.5, loss_fn="ce", display_loss=True)
print('Train Accuracy: ', cal_accuracy(sn, X_train_f, y_train_f, prob_thres=0.4))
print('Test Accuracy: ', cal_accuracy(sn, X_test_f, y_test_f, prob_thres=0.4))


# <hr>
# # Make predictions on Kaggle test set.

# In[ ]:


y_pred_kgl = sn.predict(X_scaled_test) # kgl stands for kaggle here
y_pred_binarised_kgl = (y_pred_kgl >= 0.4).astype("int").ravel()

submission = {}
submission['ImageId'] = ID_test
submission['Class'] = y_pred_binarised_kgl

submission = pd.DataFrame(submission)
submission = submission[['ImageId', 'Class']]
submission = submission.sort_values(['ImageId'])
submission.to_csv("submisision.csv", index=False)

