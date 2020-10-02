#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# importing libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


ds = pd.read_csv('/kaggle/input/cartier-jewelry-catalog/cartier_catalog.csv')
ds.head()


# In[ ]:


ds.info()


# In[ ]:


ds.isnull().sum()


# In[ ]:


# dropping unnecessary columns
ds.drop(['ref','description','image'], axis = 1, inplace=True)
ds


# In[ ]:


# Converting strings columns into integar

from sklearn.preprocessing import LabelEncoder

categorie = LabelEncoder()
title = LabelEncoder()
tags = LabelEncoder()

ds['categorie_n'] = categorie.fit_transform(ds['categorie'])
ds['title_n'] = title.fit_transform(ds['title'])
ds['tags_n'] = tags.fit_transform(ds['tags'])

ds


# In[ ]:


# dropping unnecessary columns
ds.drop(['categorie','title','tags'],axis=1, inplace=True)
ds


# ## Visualizing the values of Target labels

# In[ ]:


value_bar = ds['categorie_n'].value_counts()
value_bar


# In[ ]:


plt.figure(figsize=(5,3))
plt.bar(x = [' Label 3','Label 0','Label 2','Label 1'], height = value_bar, color = 'orange')


# ## splitting the data into train & test

# In[ ]:


x = ds.drop('categorie_n', axis = 1)
y = ds['categorie_n']


# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2)

x_train.shape , x_test.shape


# # Standardizing data

# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)


# # Machine Learning Classifiers

# In[ ]:


from sklearn.tree import DecisionTreeClassifier 
from xgboost import XGBClassifier


# In[ ]:


dt = DecisionTreeClassifier()
dt.fit(x_train,y_train)
dt.score(x_test,y_test)


# In[ ]:


xg = XGBClassifier()
xg.fit(x_train,y_train)
xg.score(x_test,y_test)


# # Confusion matrix

# In[ ]:


from sklearn.metrics import confusion_matrix, classification_report

y_pred = xg.predict(x_test)

cm = confusion_matrix(y_test, y_pred)
print('Confusion Matrix\n',cm)


# In[ ]:


plt.figure(figsize=(7,5))
sns.heatmap(cm,annot=True)
plt.xlabel('Predicted')
plt.ylabel('truth')


# # Classification Report

# In[ ]:


print(classification_report(y_test, y_pred, target_names=['class 0','class 1','class 2','class 3']))

