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


# **Read the data**

# In[ ]:


train = pd.read_csv('/kaggle/input/digit-recognizer/train.csv')
test = pd.read_csv('/kaggle/input/digit-recognizer/test.csv')
#combined = pd.concat((train,test), sort=False).reset_index(drop = True) # Imputations will be done on combined dataset
train.head()


# In[ ]:


y = train['label']
X = train.drop("label", axis=1)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = .25, random_state=0)


# **Random Forest Classifier**

# In[ ]:


get_ipython().run_cell_magic('time', '', 'from sklearn.ensemble import RandomForestClassifier\nclf = RandomForestClassifier(n_estimators=784)\nclf.fit(X_train, y_train)')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'from sklearn.model_selection import cross_val_predict\ny_train_cross_val_est = cross_val_predict(clf, X_train, y_train)')


# In[ ]:


from sklearn.metrics import f1_score
print('F1 score for random forest classifier - Train: {}'.format(round(f1_score(y_train, y_train_cross_val_est, average="macro"), 4)))


# In[ ]:


get_ipython().run_cell_magic('time', '', 'y_test_cross_val_est = cross_val_predict(clf, X_test, y_test)\nprint(\'F1 score for random forest classifier - Test: {}\'.format(round(f1_score(y_test, y_test_cross_val_est, average="macro"), 4)))')


# **PCA - Dimensionality Reduction**

# In[ ]:


get_ipython().run_cell_magic('time', '', 'from sklearn.decomposition import PCA\npca = PCA()\npca.fit(train)\ncumsum = np.cumsum(pca.explained_variance_ratio_)\ndimensions = np.argmax(cumsum >= 0.95) + 1\ndimensions')


# **Random Forest Classifier after PCA Dimensionality Reduction**

# In[ ]:


get_ipython().run_cell_magic('time', '', 'pca = PCA(n_components = 154)\nX_after_pca = pca.fit_transform(X_train)\nX_test_after_pca = pca.fit_transform(X_test)')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'clf_after_pca = RandomForestClassifier(n_estimators=154)\nclf_after_pca.fit(X_after_pca, y_train)')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'y_train_cross_val_est_after_pca = cross_val_predict(clf_after_pca, X_after_pca, y_train)\nprint(\'F1 score for random forest classifier after PCA - Train: {}\'.format(round(f1_score(y_train, y_train_cross_val_est_after_pca, average="macro"), 4)))')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'y_test_cross_val_est_after_pca = cross_val_predict(clf_after_pca, X_test_after_pca, y_test)\nprint(\'F1 score for random forest classifier - Test: {}\'.format(round(f1_score(y_test, y_test_cross_val_est_after_pca, average="macro"), 4)))')


# In[ ]:


results = clf_after_pca.predict(X_test_after_pca)

np.savetxt('results.csv', 
           np.c_[range(1,len(X_test_after_pca)+1),results], 
           delimiter=',', 
           header = 'ImageId,Label', 
           comments = '', 
           fmt='%d')

