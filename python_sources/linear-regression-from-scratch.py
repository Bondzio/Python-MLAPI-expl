#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 


# In[ ]:


df = pd.read_csv('../input/winequality-red.csv')
df.head()


# In[ ]:


X = df.iloc[:,:-1].values
X[0:3]
#First 3 Rows


# In[ ]:


y = df.iloc[:,-1].values
y[0:3]
#First 3 values


# In[ ]:


#Splitting into train and test sets
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)


# In[ ]:


#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# In[ ]:


entries = len(y_train)
entries


# In[ ]:


y_pred = []
len_x = len(X_train[0])
w = []
b = 0
print(len_x)


# In[ ]:


for weights in range(len_x):
    w.append(0)
w


# In[ ]:


def predict(inputs):
    predicted = np.dot(w,inputs)+b
    return predicted


# In[ ]:


def loss_func(y,a):
    J = (y-a)**2
    return J


# In[ ]:


dw = []
db = 0
J = 0
alpha = 0.05
for x in range(len_x):
    dw.append(0)


# In[ ]:


#Repeating the Gradient Descent Process 100 times
for iterations in range(100):
    for i in range(entries):
        localx = X_train[i]
        a = predict(localx)   
        dz = a - y_train[i]
        J += loss_func(y_train[i],a)
        for j in range(len_x):
            dw[j] = dw[j]+(localx[j]*dz)
        db += dz
    J = J/entries
    db = db/entries
    for x in range(len_x):
        dw[x]=dw[x]/entries
    for x in range(len_x):
        w[x] = w[x]-(alpha*dw[x])
    b = b-(alpha*db)   
    J=0
    


# In[ ]:


#Coefficients
print(w)


# In[ ]:


#Intercept (Bias)
print(b)


# In[ ]:


for x in range(len(y_test)):
    y_pred.append(predict(X_test[x]))


# In[ ]:


#Actual Vs Predicted
for x in range(len(y_pred)):
    print('Actual ',y_test[x],' Predicted ',y_pred[x])
    y_pred[x] = round(y_pred[x])

