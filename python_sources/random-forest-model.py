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

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


ad_df = pd.read_csv('../input/add.csv', index_col=0,low_memory=False)


# In[ ]:


ad_df.head(15)


# some fields contain invalid data, which has to be removed before we train our model

# In[ ]:


ad_df2 = ad_df.applymap(lambda val: np.nan if str(val).strip() == '?' else val)
ad_df2 = ad_df2.dropna()


# We will now use the label encorder to convert the y values to numeric

# In[ ]:


from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()
y = lb.fit_transform(ad_df2.iloc[:, -1])


# In[ ]:


y[0:5]


# In[ ]:


X = ad_df2.iloc[:,:-1]


# In[ ]:


X.head(5)


# Using standard scaler we will now normalize the X values

# In[ ]:


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)


# In[ ]:


X[0:5,:]


# Now we will split the data into two sets

# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# Training the model - Random Forest classifier

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=60)
rf.fit(X_train, y_train)


# Now we will predict * y_test*

# In[ ]:


pred = rf.predict(X_test)


# Checking the accuracy of the model

# In[ ]:


from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))


# Visualizing data

# In[ ]:


from sklearn.decomposition import PCA


# In[ ]:


pca = PCA(n_components=2)
pca.fit(X_train)


# In[ ]:


pca.explained_variance_


# In[ ]:


X_train_PCA = pca.transform(X_train)
X_test_PCA = pca.transform(X_test)


# In[ ]:


rf2 = RandomForestClassifier(n_estimators=60)
rf2.fit(X_train_PCA, y_train)


# In[ ]:


pred2 = rf2.predict(X_test_PCA)


# In[ ]:


print(confusion_matrix(y_test, pred2))
print(classification_report(y_test, pred2))


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


for i in range(0, X_test_PCA.shape[0]):
    if y_test[i] == 0:
        c1 = plt.scatter(X_test_PCA[i,0],X_test_PCA[i,1],c='r',marker='+')
    elif y_test[i] == 1:
        c2 = plt.scatter(X_test_PCA[i,0],X_test_PCA[i,1],c='g',marker='o')
plt.legend([c1, c2], ['Ad', 'No-Ad'])
plt.title('PCA vs AD Actual')


# In[ ]:


for i in range(0, X_test_PCA.shape[0]):
    if pred[i] == 0:
        c1 = plt.scatter(X_test_PCA[i,0],X_test_PCA[i,1],c='r',marker='+')
    elif pred[i] == 1:
        c2 = plt.scatter(X_test_PCA[i,0],X_test_PCA[i,1],c='g',marker='o')
plt.legend([c1, c2], ['Ad', 'No-Ad'])
plt.title('PCA vs AD Predicted without PCA')


# In[ ]:


for i in range(0, X_test_PCA.shape[0]):
    if pred2[i] == 0:
        c1 = plt.scatter(X_test_PCA[i,0],X_test_PCA[i,1],c='r',marker='+')
    elif pred2[i] == 1:
        c2 = plt.scatter(X_test_PCA[i,0],X_test_PCA[i,1],c='g',marker='o')
plt.legend([c1, c2], ['Ad', 'No-Ad'])
plt.title('PCA vs AD Predicted with PCA')


# In[ ]:




