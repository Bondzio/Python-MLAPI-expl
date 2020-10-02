#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from lightgbm import LGBMClassifier


# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


data = pd.read_csv("/kaggle/input/titanic/train.csv", index_col=["PassengerId"])
data


# In[ ]:


for c in data.select_dtypes("O"):
    print(c)
    data[c] = data[c].astype("category")


# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

X_train, X_test, y_train, y_test = train_test_split(data.drop("Survived", axis=1), 
                                                      data.Survived, test_size=0.1, random_state=2)
X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.1, random_state=2)


# In[ ]:


learner = LGBMClassifier(n_estimators=10000, num_leaves=10)
learner.fit(X_train, y_train, early_stopping_rounds=10, eval_metric="binary_error",
            eval_set=[(X_train, y_train), (X_valid, y_valid)], verbose=1)


# In[ ]:


preds = learner.predict(X_test)
preds


# In[ ]:


(preds == y_test).mean()


# In[ ]:


pd.crosstab(preds, y_test)


# In[ ]:


import numpy as np


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(data.drop("Survived", axis=1), 
                                                      data.Survived, test_size=0.1, random_state=2)

preds = []
for _ in range(10):
    idx = X_train.sample(frac=0.8).index
    learner = LGBMClassifier(n_estimators=10000, num_leaves=10)
    learner.fit(X_train.loc[idx], y_train.loc[idx], early_stopping_rounds=10, eval_metric="binary_error",
                eval_set=[(X_train.loc[idx], y_train.loc[idx]), 
                          (X_train.drop(idx), y_train.drop(idx))], verbose=1)
    preds = pd.Series(learner.predict_proba(X_test)[:, -1], index=X_test.index)
preds = pd.concat([preds], axis=1).mean(axis=1)


# In[ ]:


preds


# In[ ]:


(y_test == (preds > 0.5)).mean()


# In[ ]:


pd.crosstab((preds > 0.5), y_test)


# In[ ]:


pd.Series(learner.feature_importances_, index=X_train.columns).sort_values().to_frame()


# In[ ]:




