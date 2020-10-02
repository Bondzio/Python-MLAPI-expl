#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 
import os
import seaborn as sns
print(os.listdir("../input"))


# In[ ]:


dataset = pd.read_csv('../input/Iris.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, [-1]].values


# In[ ]:


dataset.head()


# In[ ]:


i=sns.swarmplot(data=dataset,x='Species',y='SepalLengthCm')


# In[ ]:


p=sns.stripplot(x="Species", y="PetalLengthCm",data=dataset)


# In[ ]:


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 0)


# In[ ]:


# Encoding categorical data
# Encoding the Independent Variable
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()

X[:, 0] = labelencoder_X.fit_transform(X[:, 0])
onehotencoder = OneHotEncoder(categorical_features = [0])
X = onehotencoder.fit_transform(X).toarray()

# Encoding the Dependent Variable
labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)


# In[ ]:


# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# In[ ]:


# Fitting SVM to the Training set
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, y_train)


# In[ ]:


# Predicting the Test set results
y_pred = classifier.predict(X_test)


# In[ ]:


# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)


# In[ ]:


cm

