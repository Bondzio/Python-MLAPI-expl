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


data  = pd.read_csv("../input/breast-cancer-wisconsin-data/data.csv")


# In[ ]:


data.columns
data.drop(['id','Unnamed: 32'],axis =1, inplace = True)


# In[ ]:


data.columns


# In[ ]:


data['diagnosis'].unique()
data['diagnosis'] = data['diagnosis'].map({'M':1,'B':0})


# In[ ]:


data


# In[ ]:


# standard code to check for null values in columns in data
print(data.isnull().any())
# show how many null values there.
print(data.isnull().sum())


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
my_first_model = KNeighborsClassifier(n_neighbors = 1)
#neigh.fit(samples)


# In[ ]:


print(my_first_model)


# In[ ]:


X = data.drop('diagnosis',axis =1)
y = data['diagnosis']


# In[ ]:


X


# In[ ]:


y


# In[ ]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 3)


# In[ ]:


y_test


# In[ ]:


# pass features and dependent varaible
# fit means model training
my_first_model.fit(X_train, y_train)


# In[ ]:


prediction = my_first_model.predict(X_test)
print(prediction)
print(len(prediction))


# In[ ]:


print(prediction)


# In[ ]:


X_test


# In[ ]:


from sklearn.metrics import accuracy_score, confusion_matrix , f1_score , precision_score, recall_score
# pass actual values , predicted values
# Validation accuracy
accuracy_score(y_test,prediction)


# In[ ]:


confusion_matrix(y_test,prediction)


# In[ ]:


print(f1_score(y_test,prediction))
print(precision_score(y_test,prediction))
print(recall_score(y_test,prediction))


# In[ ]:





# In[ ]:


train_prediction = my_first_model.predict(X_train)


# In[ ]:


train_prediction
# Acutal is y_test
# training accuracy
accuracy_score(y_train,train_prediction)


# In[ ]:


### Changing K value of algorithm is called Hyper parameter tuning

## Algorith Used : KNN Classifier

#Models:
##### iteration 1: 0.9322 k = 2, model 1 
##### iteration 2: 0.9298 K= 7, model 2
#### iteration 3: 0.9181 K = 4,model 3

