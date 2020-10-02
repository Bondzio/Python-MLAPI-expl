#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install --upgrade pip
get_ipython().system('pip install fastai==0.7.0 ## Based on Fast.ai ML course')

get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import numpy as np 
import pandas as pd
from IPython.display import display
from fastai.imports import *
from fastai.structured import *
from pandas_summary import DataFrameSummary
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
import os
from pandas_summary import DataFrameSummary
from matplotlib import pyplot as plt
import math

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
import re

import shap
import eli5
from eli5.sklearn import PermutationImportance
from pdpbox import pdp, get_dataset, info_plots

import IPython
from IPython.display import display
print(os.listdir("../input/"))


# In[ ]:


train_df = pd.read_csv("../input/train.csv")
test_df = pd.read_csv("../input/test.csv")
train_df.head()


# The evaluation criteria is RMSE of log of Sales Price. So first, let's change the target variable to log

# In[ ]:


train_df['SalePrice'] = np.log(train_df['SalePrice'])


# We'll just use a Random Forest Regressor. For that, we need to convert all columns to numeric type. But there are some categorical variables too.

# In[ ]:


train_cats(train_df)
apply_cats(test_df, train_df)


# We'll replace categories with their numeric codes, handle missing continuous values, and split the dependent variable into a separate variable. Fastai to the rescue again !!

# In[ ]:


df_trn, y_trn, nas = proc_df(train_df, 'SalePrice')
df_test, _, _ = proc_df(test_df, na_dict=nas)
df_trn.head()


# In[ ]:


df_test.head()


# In[ ]:


df_test.drop(['LotFrontage_na', 'MasVnrArea_na', 'BsmtFinSF1_na', 'BsmtFinSF2_na', 'BsmtUnfSF_na', 
              'TotalBsmtSF_na', 'BsmtFullBath_na', 'BsmtHalfBath_na', 'GarageYrBlt_na', 'GarageCars_na',
              'GarageArea_na'], axis =1, inplace = True)
df_trn.drop(['LotFrontage_na', 'MasVnrArea_na', 'GarageYrBlt_na'], axis = 1, inplace = True)


# ### Defining function to calculate the evaluation metric

# In[ ]:


def rmse(x,y): return math.sqrt(((x-y)**2).mean())

def print_score(m):
    res = [rmse(m.predict(train_X), train_y), rmse(m.predict(val_X), val_y),     ## RMSE of log of prices
                m.score(train_X, train_y), m.score(val_X, val_y)]
    if hasattr(m, 'oob_score_'): res.append(m.oob_score_)
    print(res)


# ### Split the data into training and validation sets

# In[ ]:


train_X, val_X, train_y, val_y = train_test_split(df_trn, y_trn, test_size=0.33, random_state=42)


# We can now pass this processed data frame to Random Forest Regressor

# Initially, let's just fit a single decision tree to visualize it properly

# In[ ]:


get_ipython().run_line_magic('time', '')
m = RandomForestRegressor(n_estimators=1, min_samples_leaf=3, n_jobs=-1, max_depth = 3, oob_score=True) ## Use all CPUs available
m.fit(train_X, train_y)

print_score(m)


# In[ ]:


draw_tree(m.estimators_[0], train_X, precision=3)


# A single decision tree did not perform so badly. Now, let's bag a collection of trees to create a random forest.

# In[ ]:


get_ipython().run_line_magic('time', '')
m = RandomForestRegressor(n_estimators=20, min_samples_leaf=3, max_features=0.5, n_jobs=-1, oob_score=True) ## Use all CPUs available
m.fit(train_X, train_y)

print_score(m)


# ## Permuation importance of features

# In[ ]:


perm = PermutationImportance(m, random_state=1).fit(val_X, val_y)
eli5.show_weights(perm, feature_names = val_X.columns.tolist())


# ## Partial Dependence Plots

# In[ ]:


for feat_name in val_X.columns:
#for feat_name in base_features:
    #pdp_dist = pdp.pdp_isolate(model=m, dataset=val_X, model_features=base_features, feature=feat_name)
    pdp_dist = pdp.pdp_isolate(model = m, dataset=val_X, model_features=val_X.columns, feature=feat_name)

    pdp.pdp_plot(pdp_dist, feat_name)

    plt.show()


# ## SHAP values for selected rows

# In[ ]:


explainer = shap.TreeExplainer(m)
shap_values = explainer.shap_values(val_X)

# visualize the first prediction's explanation (use matplotlib=True to avoid Javascript)
shap.force_plot(explainer.expected_value, shap_values[1,:], val_X.iloc[1,:], matplotlib=True) ## change shap and val_X


# In[ ]:


shap.summary_plot(shap_values, val_X)


# In[ ]:


shap.summary_plot(shap_values, val_X, plot_type="bar")


# ## Submitting Predictions

# In[ ]:


pred = m.predict(df_test)
submission = pd.read_csv('../input/sample_submission.csv')
submission.head()


# In[ ]:


submission['SalePrice'] = np.exp(pred)   ## Convert log back 
submission.to_csv('rf_submission_v1.csv', index=False)

