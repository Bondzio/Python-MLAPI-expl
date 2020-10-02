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


train = pd.read_csv('/kaggle/input/adirw2019/train.csv')
test = pd.read_csv('/kaggle/input/adirw2019/test.csv')


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns

f,ax = plt.subplots(figsize=(10, 8))
sns.heatmap(train.corr(), annot=True, linewidths=0.5, fmt='.2f',ax=ax)


# In[ ]:


numeric_columns = ['SeniorCitizen', 'tenure', 'MonthlyCharges']
numeric_data = train[numeric_columns]

labels = train['Churn']


# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(numeric_data, labels, test_size=0.33, random_state=42)

rfc = RandomForestClassifier(n_estimators=200, max_depth=8, min_samples_split=2, min_samples_leaf=1, 
                             min_weight_fraction_leaf=0.0, random_state=20)
rfc.fit(X_train, y_train)
X_train_preds_rfc = rfc.predict(X_train)
X_test_preds_rfc = rfc.predict(X_test)


# In[ ]:


print(roc_auc_score(y_train, X_train_preds_rfc))
print(roc_auc_score(y_test, X_test_preds_rfc))


# In[ ]:


sample_submission = pd.read_csv('/kaggle/input/adirw2019/sample_submission.csv')

sample_submission["Churn"] = rfc.predict(test[numeric_columns])

sample_submission.to_csv('benchmark_submission.csv', index=False)


# ## Report
# 
# ### Data preprocessing
# I left only numerical columns so I'm able to feed data to the learning algorithms
# 
# ### Data investigation
# I found that MonthlyCharges is correlated with Churn, as expected
# 
# ### Features engineering
# I didn't do any FE because I don't have time
# 
# ### Validation
# I split training data into 2 sets: train (67%) and eval (33%). It's ok because 33% is a lot of data to test on
# 
# ### Modeling
# I used one model - RandomForest. I used the hyperparameters from classes. If we were using it during classes it is probably good.
# 
# ### Other
# I think my code is fine because each cell is doing one thing
# 
# ### What I like
# 
# ### What unique I think I've done
# I prepared the first benchmark and Kaggle competition

# In[ ]:




