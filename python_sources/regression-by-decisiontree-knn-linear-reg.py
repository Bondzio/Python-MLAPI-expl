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


# In[ ]:


df=pd.read_csv('../input/Admission_Predict_Ver1.1.csv')
df1=pd.read_csv('../input/Admission_Predict.csv')


# In[ ]:


df.shape


# In[ ]:


df1.shape


# In[ ]:


final_df=pd.concat([df,df1],axis=0)
final_df.shape


# In[ ]:


final_df.isnull().sum()


# In[ ]:


final_df.describe()


# In[ ]:


import seaborn as sns
import pandas as pd


# In[ ]:


sns.pairplot(final_df,diag_kind='kde')


# In[ ]:


from scipy.stats import zscore
z = np.abs(zscore(final_df))
threshold=3
print(np.where(z>33))
outlier = final_df[(z <3).all(axis=1)]
outlier.shape


# In[ ]:


Q1=final_df.quantile(0.25)
Q3=final_df.quantile(0.75)
IQR=Q3-Q1
outliers = final_df[~((final_df < (Q1 - 1.5 * IQR)) |(final_df > (Q3 + 1.5 * IQR))).any(axis=1)]
outliers


# In[ ]:


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
final_df.columns


# In[ ]:


final_df.columns
X=final_df.drop('Chance of Admit ',axis=1)
y=final_df['Chance of Admit ']


# In[ ]:


X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=42,test_size=0.3)


# In[ ]:


Model1=LinearRegression()
Model1=Model1.fit(X_train,y_train)
pred=Model1.predict(X_test)


# In[ ]:


from sklearn import metrics


# In[ ]:


rmse=np.sqrt(metrics.mean_squared_error(y_test,pred))
rmse


# In[ ]:


rmse=[]
from sklearn.model_selection import KFold,cross_val_score
kfold =KFold(n_splits=5,random_state=2)
cv_results = cross_val_score(Model1, X, y, cv=kfold)
rmse.append(cv_results)
msg =cv_results.mean()
print(msg)
print(np.std(rmse))
rmse


# In[ ]:


variance=np.sum((rmse-np.mean(rmse))**2)


# In[ ]:


from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
Model2=DecisionTreeRegressor()
Model3=KNeighborsRegressor(n_neighbors=30)


# In[ ]:


models=[]
models.append(('LinearRegression',Model1))
models.append(('DecisionTree',Model2))
models.append(('KNN',Model3))


# In[ ]:


results=[]
names=[]
for name,model in models:
    kfold=KFold(n_splits=5,random_state=2)
    cv_results=cross_val_score(model,X,y,cv=kfold)
    names.append(name)
    results.append(cv_results)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

    


# #Decision Tree is showing both high variance erroe and high bias error.
# #Linear Regression is also showing high bias error.

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




