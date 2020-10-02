#!/usr/bin/env python
# coding: utf-8

# # If confused about which hyper-parameter should be use... follow the notebook :- 

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


# # Importing the data

# In[ ]:


df=pd.read_csv("../input/pima-indians-diabetes-database/diabetes.csv")


# In[ ]:


df.head()


# In[ ]:


df['Outcome'].value_counts() #has only zero and one


# **Checking for null values in the data**

# In[ ]:


df.isnull().sum() #has no null value


# In[ ]:


X=df.iloc[:,0:8].values
y=df.iloc[:,-1].values


# # Data preprocessing:

# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()


# In[ ]:


X=scaler.fit_transform(X)


# # Training the model :

# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
clf=DecisionTreeClassifier()


# In[ ]:


clf.fit(X_train,y_train)


# In[ ]:


y_pred=clf.predict(X_test)


# # Checking accuracy

# In[ ]:


from sklearn.metrics import accuracy_score
accuracy_score(y_test,y_pred)


# # Using GridSearchCV package to pass multiple parameter 

# In[ ]:


param_dist={
    "criterion":["gini","entropy"],
    "max_depth":[1,2,3,4,5,6,7,8,None]
}


# In[ ]:


from sklearn.model_selection import GridSearchCV
grid=GridSearchCV(clf,param_grid=param_dist, cv=10, n_jobs=-1) #n_jobes is telling the algo to use all the cores of the processor to do the job


# In[ ]:


grid.fit(X_train,y_train)


# In[ ]:


grid.best_estimator_


# In[ ]:


grid.best_score_


# # Finding out the optimal hyper-parameter values for the given data:

# In[ ]:


grid.best_params_


# In[ ]:




