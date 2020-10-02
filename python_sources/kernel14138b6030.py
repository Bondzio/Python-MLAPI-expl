#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv("/kaggle/input/titanic/train.csv")


# In[ ]:


data.head()


# In[ ]:


train = data[["Survived","Pclass","Sex","Age","Fare"]]


# In[ ]:


train.head()


# In[ ]:


sex = {"female": 1, "male": 2}
train["Sex"] = train["Sex"].map(sex)


# In[ ]:


train.head()


# In[ ]:


from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score, KFold


# In[ ]:


train = train.dropna()


# In[ ]:


x = train.drop("Survived", axis=1)
y = train["Survived"]


# In[ ]:


scaler = StandardScaler()
scaler.fit(x)
x_scaled = scaler.transform(x)


# In[ ]:


tree = DecisionTreeClassifier (random_state=42)
kf = KFold(random_state=42, shuffle=True, n_splits=5)
parameters = {
    'max_depth': np.arange(3, 15),
    'max_features': np.linspace(0.3, 1, 8),
    'min_samples_leaf': np.arange(2, 50, 1)
}
cv = GridSearchCV(tree, param_grid=parameters, cv=kf, iid=True)


# In[ ]:


cv.fit(x_scaled, y)


# In[ ]:


print(cv.best_score_)
print(cv.best_params_)


# In[ ]:


score=[]
for i in range(1,50):
    knn = KNeighborsClassifier(n_neighbors=i)
    kf = KFold(random_state=42, shuffle=True, n_splits=5)
    cv = cross_val_score(knn, x_scaled, y, cv=kf)
    score.append(cv.mean())


# In[ ]:


print(max(score))
print(score.index(max(score))+1)


# In[ ]:


knn = KNeighborsClassifier(n_neighbors=4)
knn.fit(x_scaled, y)


# In[ ]:


knn.predict(x_scaled[:20])


# In[ ]:


test = [[1, 1, 26, 20.000],[1, 2, 4, 40.000],[2,1,26,10.000],[3,1,26,1.000]]
knn.predict(scaler.transform(test))


# In[ ]:




