#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import warnings                       # to hide warnings if any
warnings.filterwarnings('ignore')

import os
print(os.listdir("../input"))


# In[ ]:


#loading libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#reading data set
df = pd.read_csv('../input/data.csv')
df.head()


# In[ ]:


#removing unnecessary columns
df = df.drop(['id', 'Unnamed: 32'], axis = 1)


# In[ ]:


df.head()


# In[ ]:


df.shape


# In[ ]:


df.dtypes


# In[ ]:


#check wheter any of the columns contain null values
df.isnull().sum()


# Converting the diagnosis value of M and B  to a numerical value <br/>
# M (Malignant) = 1<br/>
# B (Benign) = 0

# In[ ]:


def diagnosis_value(diagnosis):
    if diagnosis == 'M':
        return 1
    else:
        return 0

df['diagnosis'] = df['diagnosis'].apply(diagnosis_value)


# In[ ]:


sns.lmplot(x = 'radius_mean', y= 'texture_mean', hue = 'diagnosis',data = df)


# In[ ]:


sns.lmplot(x='smoothness_mean', y = 'compactness_mean', data = df, hue = 'diagnosis')


# In[ ]:


#loading libraries

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


# In[ ]:


X = np.array(df.iloc[:,1:])
y = np.array(df['diagnosis'])


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.33, random_state = 42)


# In[ ]:


knn = KNeighborsClassifier(n_neighbors = 13)
knn.fit(X_train,y_train)


# In[ ]:


knn.score(X_test,y_test)


# In[ ]:


#Performing cross validation
neighbors = []
cv_scores = []
from sklearn.model_selection import cross_val_score
#perform 10 fold cross validation
for k in range(1,51,2):
    neighbors.append(k)
    knn = KNeighborsClassifier(n_neighbors = k)
    scores = cross_val_score(knn,X_train,y_train,cv=10, scoring = 'accuracy')
    cv_scores.append(scores.mean())
    


# In[ ]:


#Misclassification error versus k
MSE = [1-x for x in cv_scores]

#determining the best k
optimal_k = neighbors[MSE.index(min(MSE))]
print('The optimal number of neighbors is %d ' %optimal_k)

#plot misclassification error versus k

plt.figure(figsize = (10,6))
plt.plot(neighbors, MSE)
plt.xlabel('Number of neighbors')
plt.ylabel('Misclassification Error')
plt.show()

