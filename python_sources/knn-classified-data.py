#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#Import the file

df=pd.read_csv('../input/Classified Data.csv', index_col=0)


# In[ ]:


df.head()


# In[ ]:


#Make the data in Scaler form
from sklearn.preprocessing import StandardScaler


# In[ ]:


scaler = StandardScaler()


# In[ ]:


scaler.fit(df.drop(['TARGET CLASS'], axis=1))


# In[ ]:


scaled_features = scaler.transform(df.drop(['TARGET CLASS'], axis=1))


# In[ ]:


df_feat = pd.DataFrame(scaled_features, columns=df.columns[:-1])
df_feat.head()


# In[ ]:


#Splitting the data

from sklearn.model_selection import train_test_split


# In[ ]:


X = df_feat
y = df['TARGET CLASS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


# In[ ]:


#KNN Model selection

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=1)


# In[ ]:


#Training the Model

knn.fit(X_train, y_train)


# In[ ]:


#Predictions from the model
pred = knn.predict(X_test)


# In[ ]:


#Determination od Accuracy from the model

from sklearn.metrics import confusion_matrix, classification_report

print (confusion_matrix(y_test, pred))
print('\n')
print (classification_report(y_test, pred))


# In[ ]:


#Choosing K value with Elbow method

error_rate= []

for i in range(1, 40):
    
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit (X_train, y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i!=y_test))


# In[ ]:


plt.figure(figsize= (12,8))
plt.plot(range(1,40), error_rate, linestyle = 'dashed', color = 'green', marker = 'o', markerfacecolor='red')


# In[ ]:


#For K=30, the error rate is minimum

knn = KNeighborsClassifier(n_neighbors=30)
knn.fit (X_train, y_train)
pred = knn.predict(X_test)

print ('With K=30')
print ('\n')
print (confusion_matrix(y_test, pred))
print ('\n')
print (classification_report(y_test, pred))


# In[ ]:


#Accuracy of the model is 95%

