#!/usr/bin/env python
# coding: utf-8

# ### This notebook tries to establish predictions using a simple algorithm Logistic with ANN classifier.

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


# # Data

# In[ ]:


data = pd.read_csv('/kaggle/input/telco-customer-churn/WA_Fn-UseC_-Telco-Customer-Churn.csv')
data.head()


# In[ ]:


data.drop('customerID', axis =1, inplace = True)


# In[ ]:


data.info()


# # Data Preprocessing

# In[ ]:


data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors = 'coerce')


# In[ ]:


data.info()


# In[ ]:


X = data.iloc[:,:-2].values
y = data.loc[:,'Churn'].values


# In[ ]:


from sklearn.preprocessing import LabelEncoder,OneHotEncoder


# In[ ]:


cols = [0,2,3,5,6,7,8,9,10,11,12,13,14,15,16]
for col in cols:
    label_encoder = LabelEncoder()
    X[:,col] = label_encoder.fit_transform(X[:,col])

X


# In[ ]:


X_1 = X[:,[4,-2,-1]]
X = X[:,[0,1,2,3,5,6,7,8,9,10,11,12,13,14,15,16]]


# In[ ]:


onehotencoders = OneHotEncoder(categories='auto', drop = 'first')
X = onehotencoders.fit_transform(X).toarray()
X


# In[ ]:


X = np.concatenate((X,X_1),axis = 1)
X = np.asarray(X)


# In[ ]:


y


# In[ ]:


labelencoder = LabelEncoder()
y = labelencoder.fit_transform(y)
y


# # Data Preparation

# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test, y_train,y_test = train_test_split(X,y,test_size = 0.2, random_state = 42)


# In[ ]:


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# In[ ]:


len(X_test)


# # Model testing

# ## Logistic Regression

# In[ ]:


from sklearn.linear_model import LogisticRegression


# In[ ]:


logclf = LogisticRegression(penalty = 'l1')
logclf.fit(X_train,y_train)


# In[ ]:


logclf.predict(X_test)
log_acc= logclf.score(X_test, y_test)
print(log_acc)


# ## AdaBoost

# In[ ]:


from sklearn.ensemble import AdaBoostClassifier


# In[ ]:


ada_clf = AdaBoostClassifier(random_state = 14)
ada_clf.fit(X_train,y_train)
ada_acc= ada_clf.score(X_test,y_test)
ada_acc


# ### Decision Tree

# In[ ]:


from sklearn import tree


# In[ ]:


dec_clf = tree.DecisionTreeClassifier(criterion ='entropy', splitter='random', random_state= 53, max_features=8, max_leaf_nodes=20)
dec_clf.fit(X_train,y_train)
dec_acc = dec_clf.score(X_test,y_test)
dec_acc


# ## ANN model

# In[ ]:


import keras
from keras.models import Sequential
from keras.layers import Dense

classifier = Sequential()
classifier.add(Dense(output_dim = 30, init='uniform', activation='relu', input_dim = 30))
classifier.add(Dense(output_dim = 50, init='uniform', activation='relu'))
classifier.add(Dense(output_dim = 30, init='uniform', activation='relu'))
classifier.add(Dense(output_dim = 1, init='uniform', activation='sigmoid'))


# In[ ]:


classifier.compile(optimizer = 'adam', loss='binary_crossentropy',metrics = ['accuracy'])
classifier.fit(X_train,y_train, batch_size = 10, nb_epoch=100)


# In[ ]:


y_pred = classifier.predict(X_test)
y_pred = (y_pred>0.5)
y_pred


# In[ ]:


cm = confusion_matrix(y_test,y_pred)
cm


# In[ ]:


ann_acc = classifier.evaluate(X_test, y_test)[1]


# # Model Comparison

# In[ ]:


print("Logistic Accuracy Score: {}\nAdaBOOST Accuracy Score: {}\nDecision Tree Accuracy Score: {}\nANN Classifier Accuracy Score: {}".format(log_acc,ada_acc,dec_acc,ann_acc))


# ## The simple logistic regression model produces a higher accuracy score as compared to ANN classifier
