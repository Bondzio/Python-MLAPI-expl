#!/usr/bin/env python
# coding: utf-8

# >In this kernel I build a machine learning model to use tumor information to predict whether or not a tumor is malignant or benign.

# In[ ]:


import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

import sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
#importing the library to be able to print multiple lines in one cell
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import pprint


# In[ ]:


#load dataset
data = load_breast_cancer()


# >Exploratory Data Analysis

# In[ ]:


#discover the dataset type
type(data)
#discover the dataset labels and the number of samples and features
data.keys()
data['target'].shape
data.target_names
data['data'].shape
type(data.target)


# In[ ]:


#Organize the data
X = data.data
X_labels = data['feature_names']
Y = data.target
Y_labels = data['target_names']


# In[ ]:


#discover feature values for the first sample, feature names, the class labels, first data sample's label
X[0]
X_labels
Y[0]
Y_labels[0]


# In[ ]:


#Spliting the data into training and test sets by as well spliting the labels as they are in the original dataset

train, test, train_labels, test_labels = train_test_split(X, Y, train_size=0.7, test_size=0.3, random_state=42, stratify=Y)


# >Building the Naive Bayes Model

# In[ ]:


#Initialize the classifier
gnb = GaussianNB()
#Fit the classifier
model = gnb.fit(train, train_labels)


# In[ ]:


#Predict on unlabeled data
prediction = gnb.predict(test)
print('Prediction{}'.format(prediction))


# >Evaluating the Model's Accuracy

# In[ ]:


accuracy_score(test_labels, prediction)
confusion_matrix(test_labels, prediction)
pprint.pprint(classification_report(test_labels, prediction))

