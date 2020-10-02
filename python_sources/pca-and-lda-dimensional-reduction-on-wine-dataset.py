#!/usr/bin/env python
# coding: utf-8

# ## - Introduction
# ### 1- Import and Meet Dataset
# ### 2- Plain Logistic Regression Application
# ### 3- With PCA Logistic Regression Application
# ### 4- With LDA Logistic Regression Application

# -------------------------------------------------------------------------------------------------------------------------------

# ## 1 - Import and Meet Dataset

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


df = pd.read_csv("../input/Wine.csv")
df.sample(7)


# In[ ]:


df.columns


# In[ ]:


df.info()


# In[ ]:


df.describe()


# In[ ]:


X = df.iloc[:,0:13].values
y = df.iloc[:,13].values


# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X,y,test_size = 0.2, random_state=0)


# In[ ]:


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(x_train)
X_test = sc.fit_transform(x_test)


# ### 2- Plain Logistic Regression Application

# In[ ]:


from sklearn.linear_model import LogisticRegression
model = LogisticRegression(random_state = 0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)
print("This confusion matrix without PCA or LDA. ")
print(cm)


# ### 3- With PCA Logistic Regression Application

# In[ ]:


from sklearn.decomposition import PCA
pca = PCA(n_components = 2) # we are reducing, but to how many components? 2.
X_trainPCA = pca.fit_transform(X_train)
X_testPCA = pca.transform(X_test)


# In[ ]:


model = LogisticRegression(random_state = 0)
model.fit(X_trainPCA, y_train)
y_predPCA = model.predict(X_testPCA)


# In[ ]:


cmPCA = confusion_matrix(y_test,y_predPCA)
print("This confusion matrix with PCA.")
print(cmPCA)


# ### 4- With LDA Logistic Regression Application

# In[ ]:


from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
lda = LDA(n_components = 2) # Again choosed 2 component.
X_train_LDA = lda.fit_transform(X_train, y_train)
X_test_LDA = lda.transform(X_test)


# In[ ]:


modelLDA = LogisticRegression(random_state = 0)
modelLDA.fit(X_train_LDA, y_train)
y_predLDA = modelLDA.predict(X_test_LDA)
cmLDA = confusion_matrix(y_test, y_predLDA)
print("This confusion matrix with LDA.")
print(cmLDA)

