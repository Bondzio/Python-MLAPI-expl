#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# !pip install --upgrade tornado nb_black dataprep
get_ipython().run_line_magic('load_ext', 'nb_black')


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import lightgbm as lgb

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

for dirname, _, filenames in os.walk("/kaggle/input"):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


df = pd.read_csv(
    "/kaggle/input/health-care-data-set-on-heart-attack-possibility/heart.csv"
)
df.head()


# In[ ]:


y = df["target"]
X = df.drop("target", axis=1)


# In[ ]:


X.isnull().sum()


# In[ ]:


len(X)


# In[ ]:


drop = ["fbs", "exang", "slope", "trestbps"]
X = X.drop(drop, axis=1)


# In[ ]:


train_data = lgb.Dataset(X, y)


# In[ ]:


params = {"objective": "binary"}
cv = lgb.cv(params, train_data, early_stopping_rounds=5, verbose_eval=False)
best_score = cv["binary_logloss-mean"][-1]
best_round = np.argmin(cv["binary_logloss-mean"]) + 1
print(f"Round {best_round}: {int(best_score * 1e3)}")


# In[ ]:


bst = lgb.train(params, train_data, best_round)


# In[ ]:


lgb.plot_importance(bst, grid=False, dpi=144)


# In[ ]:


import shap


# In[ ]:


explainer = shap.TreeExplainer(bst)
shap_values = explainer.shap_values(X)[1]


# In[ ]:


shap.summary_plot(shap_values, X)


# In[ ]:


for col in X:
    shap.dependence_plot(col, shap_values, X)


# In[ ]:




