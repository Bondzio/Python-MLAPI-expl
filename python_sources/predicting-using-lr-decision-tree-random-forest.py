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


# In[ ]:


import numpy as np
import pandas as pd

data=pd.read_csv('/kaggle/input/graduate-admissions/Admission_Predict.csv')


# In[ ]:


data.head()


# In[ ]:


data.shape


# # 1. Droping Unwanted Columns 

# In[ ]:


data.drop('Serial No.',axis=1,inplace=True)


# In[ ]:


data.shape


# # Checking for null values

# In[ ]:


data.isnull().sum()


# # Normalizing the values

# from sklearn.preprocessing import StandardScaler
# sc=StandardScaler()
# data=sc.fit_transform(data)

# In[ ]:


x=data.iloc[:,:-1]
y=data.iloc[:,-1]


# # Plotting between Dependent and independent variables

# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
i=331;
for z in x:
    plt.subplot(i)
    i=i+1
    plt.scatter(x[z],y)


# # Checking outliers

# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
i=331;
for z in x:
    plt.subplot(i)
    i=i+1
    plt.boxplot(x[z])
    plt.title(z)


# In[ ]:


x.corr()


# #  Using PCA

# from sklearn.decomposition import PCA
# cols=data.columns
# pca=PCA(n_components=6)
# x=pca.fit_transform(x)

# In[ ]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=1)


# In[ ]:


x_train.shape


# In[ ]:


x_test.shape


# #     USING LINEAR REGRESSION

# In[ ]:


from sklearn.linear_model import LinearRegression

M1=LinearRegression()
M1.fit(x_train,y_train)


# In[ ]:



y_pred= M1.predict(x_test)


# In[ ]:


from sklearn import metrics
def errors(y_test,y_pred):
    print('MAE is',metrics.mean_absolute_error(y_test,y_pred))
    print('MSE is',metrics.mean_squared_error(y_test,y_pred))
    print('RMSE is',np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
    print('R2 score is',metrics.r2_score(y_test,y_pred))


# In[ ]:


print("LINEAR REGRESSION")
errors(y_test,y_pred)


# In[ ]:





# # USING DECISION TREE

# In[ ]:


from sklearn import tree

m2=tree.DecisionTreeRegressor(criterion='mse',max_depth=4,random_state=1)
m2.fit(x_train,y_train)


# In[ ]:


y_pred= m2.predict(x_test)


# In[ ]:


print("DECISION TREE")

errors(y_test,y_pred)


# # USING RANDOM FOREST

# In[ ]:


from sklearn.ensemble import RandomForestRegressor

m3=RandomForestRegressor(max_depth=8,n_estimators=300,random_state=1)
m3.fit(x_train,y_train)


# In[ ]:


y_pred= m2.predict(x_test)


# In[ ]:


print("RANDOM FOREST REGRESSOR")
errors(y_test,y_pred)


# In[ ]:


m3.feature_importances_


# In[ ]:


data.isnull().sum()


# In[ ]:


y.mean()


# In[ ]:




