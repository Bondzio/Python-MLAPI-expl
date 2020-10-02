#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# importing the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[ ]:


# Input data files are available in the "../input/" directory
# print all the file/directories present at the path
import os
print(os.listdir("../input/"))


# In[ ]:


# importing the dataset
dataset = pd.read_csv('../input/50_Startups.csv')


# In[ ]:


dataset.head()


# In[ ]:


dataset.info()


# In[ ]:


dataset.isnull().sum()


# In[ ]:


# State is a categorical variable with 3 different values possible.
# California is with top frequenecy of 17
dataset.iloc[:,3].describe()


# In[ ]:


# matrix of features as X and dep variable as Y (convert dataframe to numpy array)
X = dataset.iloc[:,:-1].values          #R&D spend, Administration, Marketing Spend, State
Y = dataset.iloc[:,-1].values           #Profit


# In[ ]:


# Encoding Categorical variable
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
en = LabelEncoder()
X[:,3] = en.fit_transform(X[:,3])
oh = OneHotEncoder(categorical_features=[3])
X = oh.fit_transform(X)                                   #type(X)==sparse matrix


# In[ ]:


# converting from matrix to array
X = X.toarray()


# In[ ]:


# Dummy variable trap ---- Removing one dummy variable 
X = X[:,1:]


# In[ ]:


# R&D Spend vs Profit
from matplotlib import pyplot
pyplot.scatter(dataset.iloc[:,0:1].values,dataset.iloc[:,4:5])
pyplot.title('R&D Spend vs Profit')


# In[ ]:


# Administration vs Profit
from matplotlib import pyplot
pyplot.scatter(dataset.iloc[:,1:2].values,dataset.iloc[:,4:5])
pyplot.title('Administration vs Profit')


# In[ ]:


# Marketing spend vs Profit
from matplotlib import pyplot
pyplot.scatter(dataset.iloc[:,2:3].values,dataset.iloc[:,4:5])
pyplot.title('Marketing spend vs Profit')


# In[ ]:


# splitting the dataset into test & train set 
# test set == 20% of the complete dataset size
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=0)


# In[ ]:


from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg = reg.fit(X_train,Y_train)


# In[ ]:


# Visualization of ---- Actual (in red) and predicted (in blue) values of profit against R&D spend
plt.scatter(X_test[:,2],Y_test,color='red')
plt.scatter(X_test[:,2],reg.predict(X_test),color='blue')

