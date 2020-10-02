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

data=pd.read_csv('/kaggle/input/datasets_35901_52633_winequalityN.csv')


# In[ ]:


data.head()


# In[ ]:


data.shape


# In[ ]:


data.describe()


# data=data[~((data['fixed acidity'] < 5) | (data['fixed acidity']>8))]
# data=data[~((data['residual sugar'] < 1) | (data['residual sugar']>10))]
# data=data[~(data['volatile acidity']>0.45)]
# data=data[~((data['citric acid'] < 0.2) | (data['citric acid']>0.46))]
# data=data[~((data['chlorides'] < 0.02) | (data['chlorides']>0.065))]
# data=data[~((data['free sulfur dioxide'] < 16) | (data['free sulfur dioxide']>45))]
# data=data[~((data['total sulfur dioxide'] < 60) | (data['total sulfur dioxide']>170))]
# data=data[~(data['density']>1.01)]
# data=data[~((data['pH'] < 2.9) | (data['pH']>3.5))]
# data=data[~(data['sulphates']>0.7)]
# 

# In[ ]:


data.isnull().sum()


# In[ ]:


x=data.iloc[:,:-1]
y=data.iloc[:,-1]


# In[ ]:


x.shape


# In[ ]:


x['type'].value_counts()


# In[ ]:


from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
x['type']=le.fit_transform(x['type'])


# In[ ]:


x['type'].value_counts()


# In[ ]:


null_values=x.isnull().sum()
null_values


# In[ ]:


for z in x:
 if(null_values[z]>0) : 
     x.loc[(x[z].isnull()),z]=x[z].mean()


# In[ ]:


x.isnull().sum()


# In[ ]:


x.corr()


# In[ ]:


x.describe()


# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
i=1;
for z in x:
    plt.subplot(4,4,i)
    i=i+1
    plt.scatter(x[z],y)


# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
i=1;
for z in x:
    plt.subplot(4,4,i)
    i=i+1
    plt.boxplot(x[z])
    plt.title(z)


# In[ ]:


from sklearn.preprocessing import StandardScaler
sc=StandardScaler() 
x=sc.fit_transform(x)


# In[ ]:


type(y)


# In[ ]:


y=pd.DataFrame(y,columns=['quality'])


# In[ ]:


y.head()


# In[ ]:


y.loc[(y['quality'] <= 5),'quality']=0
y.loc[(y['quality'] <= 7) & (y['quality'] >5),'quality']=1
y.loc[(y['quality'] >7 ) ,'quality']=2


# In[ ]:


y['quality'].value_counts()


# In[ ]:


import seaborn as sns
plt.figure(figsize=(8,4))
sns.countplot(y["quality"],palette="muted")


# In[ ]:


from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=1)


# In[ ]:


x_train.shape


# In[ ]:


y_train.shape
y_train['quality'].value_counts()


# In[ ]:


x_test.shape


# In[ ]:


from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
nb=GaussianNB()

#training the model
nb.fit(x_train,y_train.values.ravel())
y_pred=nb.predict(x_test)
metrics.accuracy_score(y_test,y_pred)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rf=RandomForestClassifier(max_depth=32,n_estimators=120,criterion='entropy')
rf.fit(x_train,y_train.values.ravel())
y_pred=rf.predict(x_test)
metrics.accuracy_score(y_test,y_pred)


# In[ ]:


rf.predict([[1,7.0,0.270,0.36,20.7,0.045,45.0,170.0,1.00100,3.00,0.450000,8.8]])


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
dt=DecisionTreeClassifier(criterion='entropy')
dt.fit(x_train,y_train)
y_pred=dt.predict(x_test)
metrics.accuracy_score(y_test,y_pred)


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier  
classifier= KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2 )  
classifier.fit(x_train, y_train.values.ravel()) 
y_pred= classifier.predict(x_test) 
metrics.accuracy_score(y_test,y_pred)


# In[ ]:


from imblearn.over_sampling import RandomOverSampler
ros = RandomOverSampler(random_state=0)
x_r, y_r = ros.fit_resample(x, y)


# In[ ]:


from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x_r,y_r,test_size=0.2,random_state=1)


# In[ ]:


y_train['quality'].value_counts()


# In[ ]:


from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
nb=GaussianNB()

#training the model
nb.fit(x_train,y_train.values.ravel())
y_pred=nb.predict(x_test)
metrics.accuracy_score(y_test,y_pred)


# In[ ]:


rf=RandomForestClassifier(max_depth=32,n_estimators=120,criterion='entropy')
rf.fit(x_train,y_train.values.ravel())
y_pred=rf.predict(x_test)
metrics.accuracy_score(y_test,y_pred)


# In[ ]:


dt=DecisionTreeClassifier(criterion='entropy')
dt.fit(x_train,y_train)
y_pred=dt.predict(x_test)
metrics.accuracy_score(y_test,y_pred)


# In[ ]:


classifier= KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2 )  
classifier.fit(x_train, y_train.values.ravel()) 
y_pred= classifier.predict(x_test) 
metrics.accuracy_score(y_test,y_pred)

