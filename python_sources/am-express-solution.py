#!/usr/bin/env python
# coding: utf-8

# > **American Express Artificial Intelligence Hackerearth Problem 2 Soution**
# 
# Recently i participated in Hackerearth challenge which lasted 16 days based on Big Data and classification modelling. The accuracy of problem was evaluated by LUAC and AUC as prediction values are probabilities.

# > **Importing dataset and needed libraries**

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import matplotlib.pyplot as plt #Plotting
import seaborn as sns
# Scaling preprocessing library
from sklearn.preprocessing import StandardScaler
import sklearn.preprocessing
from sklearn.preprocessing import Imputer
# Math Library
from math import ceil
from functools import reduce
# Boosting Libraries
from xgboost import XGBRegressor
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor
from keras.models import Sequential
from keras.layers import Dense , Dropout , Lambda, Flatten
from keras.optimizers import Adam ,RMSprop
from sklearn.model_selection import train_test_split
from keras import  backend as K
import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# 1. *Importing of Train data as i've already added the headers inside the csv files.*

# In[ ]:


# Importing the dataset
train = pd.read_csv('../input/train.csv',low_memory=False)
train.head()


# In[ ]:


# Importing the dataset
test = pd.read_csv('../input/test.csv',low_memory=False)
test.head()


# * **Handling the Missing Values**
# 
# 
# I've used 0 as mean or median handling would be a hectic work to do, moreover there are no missing values.

# In[ ]:


#Filling for NaN values
train = train.fillna(0)
test = test.fillna(0)
train.head()


# In[ ]:


#Removal of first row
train= train[1:]


# In[ ]:


#Removal of first row
test= test[1:]


# In[ ]:


#Feature Selection
x_train = train.loc[:, train.columns != 'label'].values.astype(int)
y_train = train.iloc[:, -1].values.astype(int)


# In[ ]:


x_train


# In[ ]:


y_train.astype(float)


# In[ ]:


x_test =test.iloc[:, test.columns != 'label'] .values.astype(int)


# In[ ]:


x_test


# In[ ]:


# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)


# > **Generation of Covariance Matrix through mean vector**

# In[ ]:


mean_vec = np.mean(X_train, axis=0)
cov_mat = (X_train - mean_vec).T.dot((X_train - mean_vec)) / (X_train.shape[0]-1)
print('Covariance matrix \n%s' %cov_mat)


# In[ ]:


mean_vec = np.mean(X_test, axis=0)
cov_mat1 = (X_test - mean_vec).T.dot((X_test - mean_vec)) / (X_test.shape[0]-1)
print('Covariance matrix \n%s' %cov_mat1)


# In[ ]:


print('NumPy covariance matrix: \n%s' %np.cov(X_train.T))


# In[ ]:


print('NumPy covariance matrix: \n%s' %np.cov(X_test.T))


# In[ ]:


#Plotting of covariance matrix
plt.figure(figsize=(20,20))
sns.heatmap(cov_mat, vmax=1, square=True,annot=True,cmap='cubehelix')

plt.title('Correlation between different features')


# In[ ]:


#Generation of Eigenvectors and Eigenvalues from train covariance matrix
eig_vals, eig_vecs = np.linalg.eig(cov_mat)

print('Eigenvectors \n%s' %eig_vecs)
print('\nEigenvalues \n%s' %eig_vals)


# In[ ]:


#Generation of Eigenvalues and Eigenvectors from test covariance matrix
eig_vals1, eig_vecs1 = np.linalg.eig(cov_mat1)

print('Eigenvectors \n%s' %eig_vecs1)
print('\nEigenvalues \n%s' %eig_vals1)


# In[ ]:


# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs.sort(key=lambda x: x[0], reverse=True)

# Visually confirm that the list is correctly sorted by decreasing eigenvalues
print('Eigenvalues in descending order:')
for i in eig_pairs:
    print(i[0])


# In[ ]:


# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs1 = [(np.abs(eig_vals1[i]), eig_vecs1[:,i]) for i in range(len(eig_vals1))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs1.sort(key=lambda x: x[0], reverse=True)

# Visually confirm that the list is correctly sorted by decreasing eigenvalues
print('Eigenvalues in descending order:')
for i in eig_pairs1:
    print(i[0])


# In[ ]:


#Reshaping of Eigenpairs Matrix
matrix_w = np.hstack((eig_pairs[0][1].reshape(55,1), 
                      eig_pairs[1][1].reshape(55,1)
                    ))
print('Matrix W:\n', matrix_w)


# In[ ]:


#Reshaping Test eigenpairs Matrix
matrix_w1 = np.hstack((eig_pairs1[0][1].reshape(55,1), 
                      eig_pairs1[1][1].reshape(55,1)
                    ))
print('Matrix W:\n', matrix_w1)


# In[ ]:


Y = X_train.dot(matrix_w)
Y


# In[ ]:


Y1 = X_test.dot(matrix_w1)
Y1


# In[ ]:


#Principal component analysis for feature column dropping
from sklearn.decomposition import PCA
pca = PCA().fit(X_train)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlim(0,55,1)
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance')


# In[ ]:


from sklearn.decomposition import PCA
pca = PCA().fit(X_test)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlim(0,55,1)
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance')


# In[ ]:


#Dropping of columns from where covariance is almost 1.0
from sklearn.decomposition import PCA 
sklearn_pca = PCA(n_components=50)
X_pca_train = sklearn_pca.fit_transform(X_train)


# In[ ]:


from sklearn.decomposition import PCA 
sklearn_pca = PCA(n_components=50)
X_pca_test = sklearn_pca.fit_transform(X_test)


# In[ ]:


print(X_pca_train)


# In[ ]:


print(X_pca_test)


# In[ ]:


X_pca_train.shape


# In[ ]:


#Splitting the train set into training data and validation data
trainX, valX, trainY, valY = train_test_split(X_pca_train, y_train, test_size=0.2, random_state=42)


# > **Modelling of training data and prediciton of scores**
# 
# Through Random Forrest classifier

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


clf = RandomForestClassifier(random_state=1)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_train)
accuracy_score(y_train,y_pred)


# In[ ]:


score =clf.predict_proba(X_test)


# > **Neural Network Approach **
# 
# I have used a simple neural network to find the accuracy and the prediction score, this model gives pretty low compare to random forrest but hypertuning of parameters will give the better results.

# In[ ]:


def getModel(arr):
    model=Sequential()
    for i in range(len(arr)):
        if i!=0 and i!=len(arr)-1:
            if i==1:
                model.add(Dense(arr[i],input_dim=arr[0],kernel_initializer='normal', activation='relu'))
            else:
                model.add(Dense(arr[i],activation='relu'))
    model.add(Dense(arr[-1],kernel_initializer='normal',activation="sigmoid"))
    model.compile(loss="binary_crossentropy",optimizer='rmsprop',metrics=['accuracy'])
    return model


# In[ ]:


#Define a model of 5 dense layers
Model=getModel([50,50,70,40,1])


# In[ ]:


import keras
import matplotlib.pyplot as plt
from IPython.display import clear_output
class PlotLosses(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        
        self.fig = plt.figure()
        
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.i += 1
        
        clear_output(wait=True)
        plt.plot(self.x, self.losses, label="loss")
        plt.legend()
        plt.show();
        
plot_losses = PlotLosses()


# In[ ]:


#Fitting the Model
Model.fit(np.array(trainX),np.array(trainY),epochs=6,callbacks=[plot_losses])


# In[ ]:


#Accuracy Score
scores=Model.evaluate(np.array(valX),np.array(valY))


# In[ ]:


print(scores)


# In[ ]:


#Probability Prediction
predY=Model.predict_proba(np.array(X_pca_test))


# > **Best Result came from GridSearchCV**
# 
# 
# (Hypertuning of Random Forrest ) With best parameters selection in the random forrest GridSearchCV the best accuracy i've got was 0.96623

# In[ ]:


# Uncomment the whole section and run it 
#param_grid = { 
 #   'n_estimators': [200, 500],
  #  'max_features': ['auto', 'sqrt', 'log2'],
   # 'max_depth' : [4,5,6,7,8],
    #'criterion' :['gini', 'entropy']
#} 


# In[ ]:


#CV_rfc = GridSearchCV(estimator=clf, param_grid=param_grid, cv= 5)
#CV_rfc.fit(x_pca_train, y_train)


# In[ ]:


#CV_rfc.best_params_
#rfc1=RandomForestClassifier(random_state=42, max_features='auto', n_estimators= 200, max_depth=8, criterion='gini')


# In[ ]:


#rfc1.fit(x_pca_train, y_train)


# In[ ]:


#pred=rfc1.predict_proba(x_pca_test)


# 

# 
