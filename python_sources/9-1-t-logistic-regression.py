#!/usr/bin/env python
# coding: utf-8

# In this example we have to rightly predict whether a native PIMA indian person has diabetes or not based on features shared

# # 1). Import necessary libraries and dataset

# In[ ]:


# To enable plotting graphs in Jupyter notebook
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import pandas as pd
from sklearn.linear_model import LogisticRegression

# importing ploting libraries
import matplotlib.pyplot as plt   

#importing seaborn for statistical plots
import seaborn as sns

#Let us break the X and y dataframes into training set and test set. For this we will use
#Sklearn package's data splitting function which is based on random function

from sklearn.model_selection import train_test_split

import numpy as np


# calculate accuracy measures and confusion matrix
from sklearn import metrics


# In[ ]:


# Since it is a data file with no header, we will supply the column names which have been obtained from the above URL 
# Create a python list of column names called "names"

#Load the file from local directory using pd.read_csv which is a special form of read_table

pima_df = pd.read_csv("../input/pima-indians-diabetes-database/diabetes.csv")


# # 2). Analyse the dataset

# In[ ]:


pima_df.head()


# In[ ]:


# Let us check whether any of the columns has any value other than numeric i.e. data is not corrupted such as a "?" instead of 
# a number.

# we use np.isreal a numpy function which checks each column for each row and returns a bool array, 
# where True if input element is real.
# applymap is pandas dataframe function that applies the np.isreal function columnwise
# Following line selects those rows which have some non-numeric value in any of the columns hence the  ~ symbol

pima_df[~pima_df.applymap(np.isreal).all(1)]


# In[ ]:


# replace the missing values in pima_df with median value :Note, we do not need to specify the column names
# every column's missing value is replaced with that column's median respectively
#pima_df = pima_df.fillna(pima_df.median())
#pima_df


# In[ ]:


#Lets analysze the distribution of the various attributes
pima_df.describe()


# In[ ]:


# Let us look at the target column which is 'class' to understand how the data is distributed amongst the various values
pima_df.groupby(["Outcome"]).count()

# Most are not diabetic. The ratio is almost 1:2 in favor or class 0.  The model's ability to predict class 0 will 
# be better than predicting class 1. 


# In[ ]:


# Let us do a correlation analysis among the different dimensions and also each dimension with the dependent dimension
# This is done using scatter matrix function which creates a dashboard reflecting useful information about the dimensions
# The result can be stored as a .png file and opened in say, paint to get a larger view 

#pima_df_attr = pima_df.iloc[:,0:9]

#axes = pd.plotting.scatter_matrix(pima_df_attr)
#plt.tight_layout()
#plt.savefig('d:\greatlakes\pima_pairpanel.png')


# In[ ]:


# Pairplot using sns

#sns.pairplot(pima_df)


# In[ ]:


#data for all the attributes are skewed, especially for the variable "Insulin"

#The mean for Insulin is 80(rounded) while the median is 30.5 which clearly indicates an extreme long tail on the right


# In[ ]:


# Attributes which look normally distributed (plas, pres, skin, and mass).
# Some of the attributes look like they may have an exponential distribution (preg, insulin, pedi, age).
# Age should probably have a normal distribution, the constraints on the data collection may have skewed the distribution.

# There is no obvious relationship between age and onset of diabetes.
# There is no obvious relationship between pedi function and onset of diabetes.


# # 3). Model the dataset

# In[ ]:


array = pima_df.values
X = pima_df.iloc[:,0:8]
y = pima_df.iloc[:,8]
#X = array[:,0:8] # select all rows and first 8 columns which are the attributes
#Y = array[:,8]   # select all rows and the 8th column which is the classification "Yes", "No" for diabeties
test_size = 0.30 # taking 70:30 training and test set
seed =1 # Random numbmer seeding for reapeatability of the code
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)


# In[ ]:


# Fit the model on 30%
model = LogisticRegression()
model.fit(X_train, y_train)
y_predict = model.predict(X_test)

coeff_df = pd.DataFrame(model.coef_)
coeff_df['intercept'] = model.intercept_
print(coeff_df)


# Model score will help us determine accuracy of model

# In[ ]:


model_score = model.score(X_test, y_test)
print(model_score)
print(metrics.confusion_matrix(y_test, y_predict))


# # 4). Further improve this model

# In[ ]:


# Improve the model -----------------------------Iteration 2 -----------------------------------------------


# In[ ]:


# To scale the dimensions we need scale function which is part of scikit preprocessing libraries

from sklearn import preprocessing

# scale all the columns of the mpg_df. This will produce a numpy array
#pima_df_scaled = preprocessing.scale(pima_df[0:7])
X_train_scaled = preprocessing.scale(X_train)
X_test_scaled = preprocessing.scale(X_test)


# In[ ]:


# Fit the model on 30%
model = LogisticRegression()
model.fit(X_train_scaled, y_train)
y_predict = model.predict(X_test_scaled)
model_score = model.score(X_test_scaled, y_test)
print(model_score)


# IMPORTANT: first argument is true values, second argument is predicted values
# this produces a 2x2 numpy array (matrix)
print(metrics.confusion_matrix(y_test, y_predict))


#     Analyzing the confusion matrix
# 
# True Positives (TP): we correctly predicted that they do have diabetes 132
# 
# True Negatives (TN): we correctly predicted that they don't have diabetes 48
# 
# False Positives (FP): we incorrectly predicted that they do have diabetes (a "Type I error") 37
# Falsely predict positive Type I error
# 
# 
# False Negatives (FN): we incorrectly predicted that they don't have diabetes (a "Type II error") 14
# Falsely predict negative Type II error
