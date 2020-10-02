#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # Importing Essential Libraries

# In[ ]:


import pandas as pd #Library Used for Data Frames
import numpy as np # linear algebra
from sklearn.linear_model import LinearRegression #Importing Linear reg from in built Lib
from sklearn.model_selection import train_test_split #used for training the model
from sklearn.metrics import accuracy_score, r2_score #for predicting accuracy score
from  ipywidgets import interact #Used for Slider bar


# # **Reading a Dataset**

# In[ ]:


df=pd.read_csv("../input/real-estate-price-prediction/Real estate.csv") #Importing a csv file
df.head() #this will print first 5 elements from the data


# *Removing Null Values(if any)*

# In[ ]:


df1=df.dropna() #It allows to neglect the null values in the data set
df1.shape #Gives number of rows & coloumns


# df1 is a variable name dataframe1 which stores non-null values of the data

# # Slicing Values

# In[ ]:


x = df1.iloc[:,0:4].values #InDependent Variables
y = df1.iloc[:,-1].values #Dependent 


# X is a independent variable which consits of independent entites such as transaction date,house age,dist to nearest MRT station etc.
# 
# 

# Y is an dependent data that is house price of unit area which is dependent on all the independent factors.

# We are going to predict Y dependent on X(x1-x4) using Multiple Linear Regression. 

# * Note:Latitute & longitude(x5 &x6) are not considered in this code.

# Any machine learning model requires training before testing.

# # **Training Of Model**

# In[ ]:


xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.3, random_state = 16) 


# Here,test data is considered as 30% & train data is taken as 70%.

# Random state is used to shuffle the data each time when it is executed.

# # Imporing LinearRegression

# In[ ]:


model = LinearRegression()
model.fit(xtrain,ytrain) #fitting the data with linearRegression 


# General formula of multi-linear reg is:y=m1x1+m2x2+...+mnxn. where,m=slope,c=intercept

# # *  Loading Slope & Intercept

# In[ ]:


m = model.coef_
c = model.intercept_


# Consider some random values of x1,x2,x3,x4 and predict y for those values.

# In[ ]:


x = [100,2013,32,500]
y_predict = sum(m*x) + c
y_predict


# # Prediction

# In[ ]:


y_predict = model.predict([x])
ytest_predict = model.predict(xtest) 
y_predict


# > creating a function

# In[ ]:


def RealEstatePricePredict(transaction_date,hous_age,distance,stores):
    y_predict = model.predict([[transaction_date,hous_age,distance,stores]])
    print("Predicted House Price is:", y_predict[0])


# **The Predicted Price is:**

# In[ ]:


RealEstatePricePredict(99,2014,33,561)


# # Code For Slider

# Instances for min & max values

# In[ ]:


trans_min=df1.iloc[:,0].min()
trans_max=df1.iloc[:,0].max()
age_min=df1.iloc[:,1].min()
age_max=df1.iloc[:,1].max()
dist_min=df1.iloc[:,2].min()
dist_max=df1.iloc[:,2].max()
store_min=df1.iloc[:,3].min()
store_max=df1.iloc[:,3].max()


# In[ ]:


interact(RealEstatePricePredict,transaction_date=(trans_min,trans_max),
        hous_age=(age_min,age_max),distance=(dist_min,dist_max),stores=(store_min,store_max))


# In[ ]:




