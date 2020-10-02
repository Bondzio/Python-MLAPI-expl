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




import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from sklearn.model_selection import (KFold, StratifiedKFold,
                                     cross_val_predict, cross_val_score,
                                     train_test_split)

from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB

from sklearn.tree import DecisionTreeClassifier


# In[ ]:


df = pd.read_csv("../input/banknote-authentication-uci/BankNoteAuthentication.csv")
df.head()


# In[ ]:


df.describe()


# In[ ]:




# Count the number of observations of each class
print('Observations per class: \n', df['class'].value_counts())


# In[ ]:


# Import seaborn
import seaborn as sns
#import matplotlib
import matplotlib.pyplot as plt
# Use pairplot and set the hue to be our class
sns.pairplot(df, hue='class') 

# Show the plot
plt.show()


# In[ ]:


df.isin([0]).any()


# In[ ]:


X = df.drop('class', axis=1)   # input feature vector
y = df['class']                # labelled target vector


# In[ ]:


X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.20, random_state=10, stratify=y)
X_train.head()


# In[ ]:


kfold = KFold(n_splits=4, random_state=100)


# ### Gini

# In[ ]:


clf_g = DecisionTreeClassifier(criterion="gini",random_state = 10)

clf_g.fit(X_train, y_train)


# In[ ]:


scores = cross_val_score(clf_g, X_train, y_train, cv=kfold)
scores.mean()


# In[ ]:


y_pred = clf_g.predict(X_valid)
y_pred


# In[ ]:


cfm = confusion_matrix(y_pred, y_valid)
cfm


# In[ ]:


# accuracy score
print('accuracy using gini index: ',accuracy_score(y_pred,y_valid))


# ### entropy

# In[ ]:


clf_e = DecisionTreeClassifier(criterion="entropy",random_state = 10)
clf_e.fit(X_train,y_train)


# In[ ]:


scores = cross_val_score(clf_e, X_train, y_train, cv=kfold)
scores.mean()


# In[ ]:


y_pred_e = clf_g.predict(X_valid)
y_pred_e


# In[ ]:


cfm_e = confusion_matrix(y_pred_e, y_valid)
cfm_e


# In[ ]:


# accuracy score
print('accuracy using entropy: ',accuracy_score(y_pred_e,y_valid))


# In[ ]:


# generate the tree

from sklearn import tree
tree.export_graphviz(clf_g, out_file="tree_gini.dot")


# In[ ]:


# display the tree 

from graphviz import Source
Source.from_file('tree_gini.dot') 


# Decision Tree classifier performed very well on bank note authentication classification problem using gini index and entropy parameters.
