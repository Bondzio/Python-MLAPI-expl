#!/usr/bin/env python
# coding: utf-8

# ## Import libraries

# In[ ]:


import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import time


# ## Load train & test data

# In[ ]:


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')

train_image = train.iloc[:,1:]
train_label = train.iloc[:,0]


# In[ ]:


train_image = train_image.values / 255.0
test_image = test.values / 255.0


# In[ ]:


train_label = train_label.values


# In[ ]:


print('the shape of train_image: {}, train_label: {}'.format(train_image.shape, train_label.shape))
print('the shape of test_image: {}'.format(test_image.shape))


# ## Splitting the training set using train_test_split

# In[ ]:


X_train, X_val, y_train, y_val = train_test_split(train_image,train_label, train_size = 0.8,random_state = 0)


# In[ ]:


print(X_train.shape)
print(X_val.shape)


# ## Finding accuracy using PCA with n_components

# In[ ]:


# 
def n_component_analysis(n, X_train, y_train, X_val, y_val):
    start = time.time()
    pca = PCA(n_components=n)
    print("PCA begin with n_components: {}".format(n));
    pca.fit(X_train)
    
    X_train_pca = pca.transform(X_train)
    X_val_pca = pca.transform(X_val)

    print('SVC begin')
    clf1 = svm.SVC()
    clf1.fit(X_train_pca, y_train)
    #accuracy
    accuracy = clf1.score(X_val_pca, y_val)
    end = time.time()
    print("accuracy: {}, time elaps:{}".format(accuracy, int(end-start)))
    return accuracy


# In[ ]:


n_s = np.linspace(0.70, 0.85, num=15)
accuracy = []
for n in n_s:
    tmp = n_component_analysis(n, X_train, y_train, X_val, y_val)
    accuracy.append(tmp)


# ## Visualizing n_components Vs Accuracy

# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.plot(n_s, np.array(accuracy), 'b-')


# In[ ]:


pca = PCA(n_components=0.75)
pca.fit(X_train)


# In[ ]:


pca.n_components_


# In[ ]:


pca.explained_variance_ratio_


# In[ ]:


X_train_pca = pca.transform(X_train)
X_val_pca = pca.transform(X_val)


# In[ ]:


print(X_train_pca.shape)
print(X_val_pca.shape)


# ## Applying SVM and finding Accuracy

# In[ ]:


clf1 = svm.SVC()
clf1.fit(X_train_pca, y_train)
clf1.score(X_val_pca, y_val)

