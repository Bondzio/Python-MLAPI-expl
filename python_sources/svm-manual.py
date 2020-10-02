#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
sns.set()

from audioClassification import feature_extraction

from jupyterthemes import jtplot
jtplot.style(theme='grade3', grid=False, fscale=1.3)


# In[ ]:


features, labels = feature_extraction("dataset/data/")


# In[ ]:


print(features.shape)


# In[ ]:


from sklearn.model_selection import train_test_split 


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(features,labels,test_size=0.2, random_state=42) # 80% training 20% testing


# In[ ]:


from sklearn.svm import SVC


# In[ ]:


clf = SVC(kernel='rbf',C=21, decision_function_shape='ovr', gamma=0.00009, verbose=False, probability=True)


# In[ ]:


model = clf.fit(X_train,y_train)


# In[ ]:


from sklearn.externals import joblib
import pickle


# In[ ]:


# with open('svm_model','wb') as f:
#     pickle.dump(model,f)


# In[ ]:


y_pred = clf.predict(X_test)


# In[ ]:


clf.score(X_test,y_test)


# In[ ]:


from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, plot_confusion_matrix


# In[ ]:


plot_confusion_matrix(clf,X_test,y_test, cmap='Blues')


# In[ ]:


print(classification_report(y_test,y_pred))


# In[ ]:


from scikitplot.metrics import plot_roc, plot_precision_recall


# In[ ]:


y_proba = clf.predict_proba(X_test)


# In[ ]:


plot_roc(y_test,y_proba, figsize=(15,5))


# In[ ]:


plot_precision_recall(y_test,y_proba, figsize=(13,5))


# In[ ]:


from scikitplot.estimators import plot_learning_curve


# In[ ]:


plot_learning_curve(clf,X_train,y_train, figsize=(5,3))


# In[ ]:


from sklearn.model_selection import learning_curve,ShuffleSplit


# In[ ]:





# In[ ]:




