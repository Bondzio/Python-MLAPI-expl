#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_absolute_error, mean_squared_error,r2_score


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


insdf=pd.read_csv("../input/insurance.csv")
insdf1=insdf.copy()
insdf.head()


# In[ ]:


#To find no.of rows and columns
insdf1.shape


# In[ ]:


#Listing the columns of dataset
insdf1.columns


# In[ ]:


#Dataframe.Info() This method prints information about a DataFrame including the
# index dtype and column dtypes, non-null values and memory usage
insdf1.info()


# In[ ]:


#To detect any missing values
insdf1.isna().sum()


# In[ ]:


#Check the duplicated records
insdf1.duplicated().sum()


# In[ ]:


#To return the duplicated rows
dfRowsDuplicated=insdf1[insdf1.duplicated()]
dfRowsDuplicated


# In[ ]:


#Check the count of duplicate records and remove duplicate records
insdf1.duplicated().sum()
insdf1.drop_duplicates(inplace = True)


# In[ ]:


#To check whether duplicated rows are removed
insdf1.duplicated().sum()


# In[ ]:


num_col=insdf1.select_dtypes(include=np.number).columns
num_col


# In[ ]:


cat_col=insdf1.select_dtypes(exclude=np.number).columns
cat_col


# In[ ]:


#one hot encoding for category column
encoded_cat_col=pd.get_dummies(insdf1[cat_col])
encoded_cat_col.head()


# In[ ]:


#Concat Category column & numerical column
insdf1_ready_model=pd.concat([insdf1[num_col],encoded_cat_col], axis = 1)
insdf1_ready_model.head()


# In[ ]:


#performing Label encoding so that dataframe gets updated
le = LabelEncoder()
for i in cat_col:
    insdf1[i] = le.fit_transform(insdf1[i])
insdf1.head()


# Deriving the statistical measure for each column. Comparing the mean and median.
# Age - slight variation between mean and median
# BMI - slight variation between mean and median
# Expenses - High variation between mean and median

# In[ ]:


insdf1.describe().T


# Getting the  Outliers for Age, BMI, Expenses
# **Observation**:
# Age -> No outliers in Age
# BMI - Outlier in BMI above 47
# Expenses - Has outliers in expenses above 35000

# In[ ]:


#Boxplot for Age
ax=sns.boxplot(insdf1['age'])
ax.set_title('Dispersion of Age')
plt.show(ax)


# In[ ]:


#Boxplot for BMI
ax=sns.boxplot(insdf1['bmi'])
ax.set_title('Dispersion of BMI')
plt.show(ax)


# In[ ]:


#Boxplot for Expenses
ax=sns.boxplot(insdf1['expenses'])
ax.set_title('Dispersion of Expenses')
plt.show(ax)


# **Scatterplot for :**
# Age vs BMI
# Age vs Expenses
# BMI vs Expenses
# 

# In[ ]:



ax=sns.scatterplot(x='bmi',y='expenses',data=insdf1)
ax.set_title('BMI vs Expenses')
plt.show(ax)


# In[ ]:


ax=sns.scatterplot(x='age',y='expenses',data=insdf1)
ax.set_title('Age vs Expenses')
plt.show(ax)


# To understand the relationship between the Age and expenses with respect to bmi.

# In[ ]:


plt.figure(figsize=(15,10))
ax=sns.scatterplot(x='age',y='expenses',hue='bmi',size='bmi',data=insdf1)
ax.set_title('Age vs Expenses by BMI')
plt.xlabel('Age')
plt.ylabel('Expenses')
plt.show(ax)


# In[ ]:


#As you see Age with sex is not influencing the expenses
plt.figure(figsize=(10,5))
ax = sns.scatterplot(x='age',y='expenses', hue='sex',style = 'sex',data=insdf1)
ax.set_title("Age vs Expenses by Sex")
plt.show(ax)


# In[ ]:


#Both age and smoker are higgly influencing the expenses
plt.figure(figsize=(10,7))
ax=sns.scatterplot(x='age',y='expenses',hue=insdf1['smoker'],style=insdf1['smoker'],
                   size=insdf1['smoker'],data=insdf1)
ax.set_title('Age vs Expenses by Smoker')
plt.xlabel('Smoker(Yes-1 No-0)')
plt.ylabel("Expenses")
plt.show(ax)


# #We need to find Correlation to understand the relationship of each independent variable with
# #dependent variable
# 
# #Age has positive side (30%) relationship against expenses
# #bmi has positive side (20%) relationship against expenses
# #Children has almost no relationship against expenses
# #Smoker has strong positive relationship (78%) against expenses

# In[ ]:


#Finding correlation
insdf1.corr()


# In[ ]:


#Swarm plot shows how smoker feature is influencing the expeneses compare with smoker and non-smoker
ax=sns.swarmplot(x='smoker',y='expenses',data=insdf1)
ax.set_title("Smoker vs Expenses")
plt.xlabel("Smoker (Yes - 1, No - 0)")
plt.ylabel("Expenses")
plt.show(ax)


# In[ ]:


#Loading y with dependant variable
y=insdf1["expenses"]


# In[ ]:


#Filtering the dependant variable and loading X with Independant variable
X=insdf1.drop(columns="expenses")
X.head()


# In[ ]:


train_X,test_X,train_y,test_y=train_test_split(X,y,test_size=0.3,random_state=1)


# In[ ]:


print("Train X :", train_X.shape)
print("Test X :",test_X.shape)
print("Train y :",train_y.shape)
print("Test y :",test_y.shape)


# In[ ]:


model=LinearRegression()
model.fit(train_X,train_y)


# In[ ]:


print("Coefficient value:",model.coef_)
print("Intercept value:", model.intercept_)


# In[ ]:


#Predicting the Y value from the train set and test set
train_y_predict=model.predict(train_X)
train_y_predict[0:5]

test_y_predict=model.predict(test_X)


# In[ ]:


#Plot to see the actual expenses and predicted expenses 
ax=sns.scatterplot(train_y,train_y_predict)
ax.set_title("Actual Expenses vs Predicted Expenses")
plt.xlabel("Actual Expenses")
plt.ylabel("Predicted Expenses")
plt.show(ax)


# In[ ]:


#MAE
print("Mean Absolute Error Train: ",mean_absolute_error(train_y_predict,train_y))
print("Mean Absolute Error Test: ",mean_absolute_error(test_y_predict,test_y))


# In[ ]:


#MSE
print("mean_squared_error Train: ", mean_squared_error(train_y_predict,train_y))
print("mean_squared_error Test: ", mean_squared_error(test_y_predict,test_y))


# In[ ]:


#MSE
print("mean_squared_error Train: ", mean_squared_error(train_y,train_y_predict))
print("mean_squared_error Test: ", mean_squared_error(test_y,test_y_predict))


# In[ ]:


#RMSE
print(np.sqrt(mean_squared_error(train_y_predict,train_y)))
print(np.sqrt(mean_squared_error(test_y_predict,test_y)))


# In[ ]:


print("R-Squared Train value: ",r2_score(train_y_predict,train_y))
print("R-Squared Test value: ",r2_score(test_y_predict,test_y))

