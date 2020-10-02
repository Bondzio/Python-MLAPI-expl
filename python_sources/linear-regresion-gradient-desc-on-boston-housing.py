#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[2]:


import numpy as np
import pandas as pd
import seaborn as sns
# Load the Boston housing dataset

df = pd.read_csv('../input/housing.csv',sep=",")


# # Exploratory Data Analysis(EDA)

# In this first section of this project, we will make a cursory investigation about the Boston housing data and provide our observations. Familiarizing ourself with the data through an explorative process is a fundamental practice to help us better understand and justify our results.
# 

# In[3]:


df.head()


# # Checking if any column have null data

# In[4]:


sns.heatmap(df.isnull(),yticklabels=False,cbar=False,cmap = 'viridis')


# In[5]:


#it state that any column doesnt have any null value.


# # Describing housing_data for statistic metrics

# In[6]:


df.describe()


# # Visualization of data

# In[7]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[8]:


sns.pairplot(df,size=2);


# 
# **Feature Observation**:
#            As a reminder, we are using three features from the Boston housing dataset: 'RM', 'LSTAT', and 'PTRATIO'. For each data point (neighborhood):
# 
# **'RM'** is the average number of rooms among homes in the neighborhood.
# **'LSTAT'** is the percentage of homeowners in the neighborhood considered "lower class" (working poor).
# **'PTRATIO'** is the ratio of students to teachers in primary and secondary schools in the neighborhood

# # Correlation Analysis for Feature Selection

# In[9]:


df.corr()  #for finding best feature


# In[10]:


plt.figure(figsize=(16,10))
sns.heatmap(df.corr(),annot=True);


# 
# In this first section of this project, we will make a cursory investigation about the Boston housing data and provide our observations. Familiarizing ourself with the data through an explorative process is a fundamental practice to help us better understand and justify our results.
# 
# Since the main goal of this project is to construct a working model which has the capability of predicting the value of houses, we will need to separate the dataset into **features and the target variable.** The features, **'RM', 'LSTAT','PTRATIO'**, give us quantitative information about each data point,they are stored in **'y'** variable. The target variable, **'MEDV'**, will be the variable we seek to predict. These are stored in **'X'** variable.
# 
# 

# In[11]:


X = df[['MEDV','RM','PTRATIO']] #select feature
y = df[['LSTAT']].values   #select target var
y = y.reshape(-1,1)


# # Applying Scikit learn Linear Regression based on 3 independent columns 'RM','LSAT','PTRATIO' to predict value of dependent variable 'MEDV'
# 

# In[12]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# In[13]:


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.3,random_state=42)


# In[14]:


#create linear regression object
lm = LinearRegression()  


# In[15]:


#train the model using training set
lm.fit(X_train,y_train)


# In[16]:


#make prediction using the training set first
y_train_pred = lm.predict(X_train)
y_test_pred = lm.predict(X_test)


# In[17]:


from sklearn.metrics import mean_absolute_error, mean_squared_error

#the mean squared error,lower the value better, if it is a .0 means perfect prediction
s = mean_squared_error(y_train,y_train_pred)
print("Mean Squared error of training set :%2f"%s)


# In[18]:



#the mean squared error,lower the value better it is .0 means perfect prediction
s = mean_squared_error(y_test,y_test_pred)
print("Mean squared error of testing set: %.2f"%s)


# In[ ]:


from sklearn.metrics import r2_score

# Explained variance score: 1 is perfect prediction
s = r2_score(y_train, y_train_pred)
print('R2 variance score of training set: %.2f' %s )


# In[ ]:



#explained the variance score :1 is perfect prediction
s = r2_score(y_test,y_test_pred)
print("R2 variance score of testing set: %2f"%s)


# In[ ]:


#calculating adjusted r2
N = y_test.size
p = X_train.shape[1]
adjr2score = 1 - ((1-r2_score(y_test, y_test_pred))*(N - 1))/ (N - p - 1)
print("Adjusted R^2 Score %.2f" % adjr2score)


# # Polynomial Regression

# In[ ]:


#import polynomial package
from sklearn.preprocessing import PolynomialFeatures


# In[ ]:


#creat a polynomial regression model for the given degree=2
poly_reg = PolynomialFeatures(degree = 2)


# In[ ]:


#transform the existing feature to high degree features.
X_train_poly = poly_reg.fit_transform(X_train)
X_test_poly = poly_reg.fit_transform(X_test)


# In[ ]:


#fit the transform features to linear regression
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_train_poly,y_train)


# In[ ]:


#predicting on training data set 
y_train_predict = lin_reg_2.predict(X_train_poly)
#predicting on testing data set
y_test_predict = lin_reg_2.predict(X_test_poly)


# In[ ]:


#ealuating the model on train dataset
rmse_train = np.sqrt(mean_squared_error(y_train,y_train_predict))
r2_train = r2_score(y_train,y_train_predict)
print("The model performance of training set")
print("---------------------------------------------")
print("RMSE of training set is{}".format(rmse_train))
print("R2 score of training set is{}".format(r2_train))


# In[ ]:


#evaluating model on test dataset
rmse_test = np.sqrt(mean_squared_error(y_test,y_test_predict))
r2_test = r2_score(y_test,y_test_predict)

print("The model performance of training set")
print("-----------------------------------------------")
print("RMSE of testing set is{}".format(rmse_test))
print("R2 score of testing set is{}".format(r2_test))


# # Quadratic 

# In[ ]:


#import polynomial package
from sklearn.preprocessing import PolynomialFeatures


# In[ ]:


#creat a polynomial regression model for the given degree=3
poly_reg = PolynomialFeatures(degree = 3)


# In[ ]:


#transform the existing feature to high degree features.
X_train_poly = poly_reg.fit_transform(X_train)
X_test_poly = poly_reg.fit_transform(X_test)


# In[ ]:


#fit the transform features to linear regression
lin_reg_3 = LinearRegression()
lin_reg_3.fit(X_train_poly,y_train)


# In[ ]:


#predicting on training data set 
y_train_predict = lin_reg_3.predict(X_train_poly)
#predicting on testing data set
y_test_predict = lin_reg_3.predict(X_test_poly)


# In[ ]:


#ealuating the model on train dataset
rmse_train = np.sqrt(mean_squared_error(y_train,y_train_predict))
r2_train = r2_score(y_train,y_train_predict)
print("The model performance of training set")
print("----------------------------------------------")
print("RMSE of training set is{}".format(rmse_train))
print("R2 score of training set is{}".format(r2_train))


# In[ ]:


#evaluating model on test dataset
rmse_test = np.sqrt(mean_squared_error(y_test,y_test_predict))
r2_test = r2_score(y_test,y_test_predict)

print("The model performance of testing set")
print("--------------------------------------------")
print("RMSE of testing set is{}".format(rmse_test))
print("R2 score of testing set is{}".format(r2_test))


# # Applying Gradient Descent

# In[ ]:


from sklearn.preprocessing import StandardScaler
sc_x = StandardScaler()
sc_y = StandardScaler()
X_std = sc_x.fit_transform(X)
y_std = sc_y.fit_transform(y.reshape(-1,1)).flatten()


# In[ ]:


X_std.shape


# In[ ]:


import numpy as np
alpha = 0.0001    #learning rate
w_ = np.zeros(1 + X_std.shape[1])    
cost_ = [] 
n_ = 100
 
for i in range(n_):
    y_pred = np.dot(X_std,w_[1:] + w_[0])
    errors  = (y_std - y_pred)
    
    w_[1:] +=alpha * X_std.T.dot(errors)   #theta1
    w_[0] +=alpha *errors.sum()        #theta0
    
    cost = (errors**2).sum() / 2.0
    cost_.append(cost)


# In[ ]:


plt.figure(figsize=(10,8))  #plot the figure
plt.plot(range(1,n_ + 1),cost_);
plt.ylabel('SSE');
plt.xlabel('Epoch');


# In[ ]:


w_   #gradient function (intercept and coeficient) 


# In[ ]:


#accuracy of gradient function
print("Accuracy: %0.2f (+/- %0.2f)" % (w_.mean(), w_.std() * 2))


# # Applying Support Vector Machin(SVM)

# In[ ]:


from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error,r2_score


# In[ ]:


df.head()


# In[ ]:


svr = SVR(kernel='linear')
svr.fit(X_train, y_train)


# In[ ]:


y_train_pred = svr.predict(X_train)


# In[ ]:


y_test_pred = svr.predict(X_test)


# In[ ]:


print("MSE train: {0:.4f},test: {1:.4f}".     format(mean_squared_error(y_train,y_train_pred),
           mean_squared_error(y_test,y_test_pred)))


# In[ ]:


print("R^2 train: {0:.4f}, test: {1:.4f}".      format(r2_score(y_train, y_train_pred),
             r2_score(y_test, y_test_pred)))


# #Polynomial

# In[ ]:


svr = SVR(kernel='poly', C=1e3, degree=2)
svr.fit(X_train, y_train)


# In[ ]:




