#!/usr/bin/env python
# coding: utf-8

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

# Any results you write to the current directory are saved as output.


# #******************  Importing Libraries     **************************

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns


# Reading the Dataset

# In[ ]:


df_grad = pd.read_csv("../input/Admission_Predict.csv")


# Visualising the dataset

# In[ ]:


df_grad.info()


# In[ ]:


plt.hist(df_grad['GRE Score'])


# In[ ]:


plt.hist(df_grad['TOEFL Score'])


# In[ ]:


plt.hist(df_grad['CGPA'])


# ********** Lets Drop the Serial No. Field - Not Significant *********

# In[ ]:


df_grad = df_grad.drop(['Serial No.'],axis =1)


# ***** Let see the corr of the field to the Chance of Admission *** 

# In[ ]:


plt.figure(figsize = [10,10])
sns.heatmap(df_grad.corr(),annot=True)


# *** As seen above GRE Score, TOEFL, CGPA and Univ Rating are the determinants to Change to admission **

# *** Lets prep our variables for processing ***

# In[ ]:


X = df_grad.drop(['Chance of Admit '],axis =1)
y = df_grad['Chance of Admit ']


# *** Lets Feature scale the variables *** 

# In[ ]:


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)


# ** Lets Split the dataset into training and test sets **

# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=0)


# ** Applying Logistic regression - Regression problem (Continuous dependent variable) **

# In[ ]:


from sklearn.linear_model import LinearRegression
lin_regressor = LinearRegression()
lin_regressor.fit(X_train,y_train)
from sklearn.metrics import mean_squared_error
y_predict = lin_regressor.predict(X_test)


# In[ ]:


print("Accuracy Level : ",lin_regressor.score(X_test, y_test)*100,' %')
print("Mean Squared Error is : ",np.sqrt(mean_squared_error(y_test,y_predict)))


# ** Lets plot the graph of test and predicted values

# In[ ]:


plt.plot(range(len(y_test)),y_test)
plt.plot(range(len(y_predict)),y_predict)


# ** Lets now try RandomForest algorithm **

# In[ ]:


from sklearn.ensemble import RandomForestRegressor
random_regressor = RandomForestRegressor(n_estimators = 200)
random_regressor.fit(X_train,y_train)
y_predict = random_regressor.predict(X_test)


# In[ ]:


print("Accuracy Level : ",random_regressor.score(X_test, y_test)*100,' %')
print("Mean Squared Error is : ",np.sqrt(mean_squared_error(y_test,y_predict)))


# ** Accuracy level decreased and MSE also increased indicating Linear model was better

# ** Lets Try to run all the regression models and compare the accuracies and MSE **

# In[ ]:


from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.linear_model import Lasso,Ridge,BayesianRidge,ElasticNet,HuberRegressor,LinearRegression,LogisticRegression,SGDRegressor
from sklearn.metrics import mean_squared_error

models = [['DecisionTree :',DecisionTreeRegressor()],
           ['Linear Regression :', LinearRegression()],
           ['RandomForest :',RandomForestRegressor(n_estimators = 200)],
           ['KNeighbours :', KNeighborsRegressor(n_neighbors = 2)],
           ['SVM :', SVR()],
           ['AdaBoostClassifier :', AdaBoostRegressor()],
           ['GradientBoostingClassifier: ', GradientBoostingRegressor()],
           ['Xgboost: ', XGBRegressor(max_depth = 6)],
           ['CatBoost: ', CatBoostRegressor(logging_level='Silent')],
           ['Lasso: ', Lasso()],
           ['Ridge: ', Ridge()],
           ['BayesianRidge: ', BayesianRidge()],
           ['ElasticNet: ', ElasticNet()],
           ['HuberRegressor: ', HuberRegressor()]]


# In[ ]:


RMS_score_model = {}
ACC_score_model = {}
for name_of_model,model_parms in models:
    curr_model = model_parms
    curr_model.fit(X_train, y_train)
    curr_predict = curr_model.predict(X_test)
    RMS_score_model[name_of_model] = np.sqrt(mean_squared_error(y_test, curr_predict))
    ACC_score_model[name_of_model] = curr_model.score(X_test, y_test)*100


# **** Lets sort the RMS and Accuracies to print them in order ***

# In[ ]:


from collections import OrderedDict
RMS_sorted_scores_value = OrderedDict(sorted(RMS_score_model.items(), key=lambda x: x[1]))
ACC_sorted_scores_value = OrderedDict(sorted(ACC_score_model.items(), key=lambda x: x[1],reverse = True))


# In[ ]:


print('RMS Scores for the models are as follows :')
RMS_sorted_scores_value


# In[ ]:


print('Accuracy Levels % for the models are as follows :')
ACC_sorted_scores_value


# *** We can go with Linear regression which give good results as seen from stats above ***

# **** Lets run Linear model again to summarize ****

# In[ ]:


from sklearn.linear_model import LinearRegression
lin_regressor = LinearRegression()
lin_regressor.fit(X_train,y_train)
from sklearn.metrics import mean_squared_error
y_predict = lin_regressor.predict(X_test)
plt.plot(range(len(y_test)),y_test)
plt.plot(range(len(y_predict)),y_predict)
print("Accuracy Level : ",lin_regressor.score(X_test, y_test)*100,' %')
print("Mean Squared Error is : ",np.sqrt(mean_squared_error(y_test,y_predict)))


# *** Let me know your views and any inputs please.....

# In[ ]:




