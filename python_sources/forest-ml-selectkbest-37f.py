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


# Import training data - review shape and columns
import pandas as pd
train = pd.read_csv('/kaggle/input/learn-together/train.csv', index_col='Id')
#print(train.info())


# # Univariate Feature Selection
# ## 1. Select KBest
# In SelectKBest, we derive statistically the metrics to calculate feature importance for a classification problem. It does so by evaluating one feature at a time in regards to its ability to influence the target class. We then rank the features based on the metric to pick only K best features for machine learning tasks.
# 
# For classification problems, there are 2 metrics that are used:
# 1. chi2 - this is used to validate that occurance of a categorical feature influences occurance of a categorical outcome. So this is used when we are trying to evaluate feature importance for categorical features only.
# 2. f_classif - this is used to evaluate the importance of numerical as well as categorical features for a categorical outcome, using a F-test. So we can check the numerical features as well as the categorical features we earlier evaluated with chi2. Typically both metrics give similar feature importance scores.
# 
# Before we apply SelectKBest, we need to split the features into numerical and categorical features for reasons stated above and then apply the feature selection in 2 steps.
# 
# 1. Using Chi2 as the metric - we select only the categorical features - 4 Wild Areas and 36 Soil Types (remember we removed the 4 Soil type features earlier)
# 2. Using f_classif as the metric - we select only the 10 numerical features - first 10 columns of our dataset.
# 
# 
# 

# In[ ]:


# Make a copy of train df for ML experiments
train_2 = train.copy()
train_2.drop(['Soil_Type7','Soil_Type15', 'Soil_Type8','Soil_Type25'], axis = 1, inplace=True)
train_2.columns

print(train_2.columns)
print(train_2.columns.get_loc('Wilderness_Area1'))
print(train_2.columns.get_loc('Soil_Type40'))


# #### Get Numerical and Categorical Features separately for SelectKBest

# In[ ]:


numerical_df = train_2.iloc[:,[0,1,2,3,4,5,6,7,8,9,50]] # Include Cover Type as well along with numerical features
X_num = numerical_df.drop('Cover_Type', axis=1)
y_num = numerical_df.Cover_Type
print(X_num.columns)
print(y_num[:5])
cat_df = train_2.iloc[:,10:51] # Include Cover Type along with categorical features
X_cat = cat_df.drop('Cover_Type', axis= 1)
y_cat = cat_df.Cover_Type
print(X_cat.columns)
print(y_cat[:5])


# ### Apply SelectKBest to numerical features with score_func as f_classif
# We will set K = Total number of features under consideration so that we can get a view of ranking for all features. This will be 10 for numerical features and 40 for categorical features (Wilderness Areas and Soil Types (excluding the 4 Soil Types we already removed)
# 
# Lets rank all numerical features and get top 7/10 numerical features

# In[ ]:


from sklearn.feature_selection import SelectKBest, f_classif,chi2
selector_num = SelectKBest(score_func=f_classif,k=10)
selector_num.fit(X_num,y_num)
#print("scores_:",selector_num.scores_)
#print("pvalues_:",selector_num.pvalues_)
#print(pd.DataFrame(list(zip([list(X_num.columns)],selector_num.scores_,selector_num.pvalues_))))
df_num_kbest = pd.DataFrame(list(zip(list(X_num.columns),selector_num.scores_,selector_num.pvalues_)), columns=['Feature','Score','P-value'])
df_num_kbest.sort_values('Score', ascending=False)
X_num_top7 = list(df_num_kbest.sort_values('Score', ascending=False).Feature[:7])
print('Top 7 Numerical Features: ',X_num_top7)


# We see that Aspect, Vertical Distance to Hydrology are at the bottom of the stack. Vertical distance to hydrology has strong correlation with Horizontal distance to hydrology. so probably this is fine.

# ### Apply SelectKBest to categorical features with score_func as chi2

# In[ ]:


from sklearn.feature_selection import SelectKBest, f_classif,chi2
selector_cat = SelectKBest(score_func=chi2,k=40)
selector_cat.fit(X_cat,y_cat)
#print("scores_:",selector_cat.scores_)
#print("pvalues_:",selector_cat.pvalues_)
#print(pd.DataFrame(list(zip([list(X_num.columns)],selector_num.scores_,selector_num.pvalues_))))
df_kbest = pd.DataFrame(list(zip(list(X_cat.columns),selector_cat.scores_,selector_cat.pvalues_)), columns=['Feature','Score','P-value'])
df_kbest.sort_values('Score', ascending=False)


# ### Apply SelectKBest to categorical features with score_func as f_classif - Get Top 30 features

# In[ ]:


from sklearn.feature_selection import SelectKBest, f_classif,chi2
selector_cat = SelectKBest(score_func=f_classif,k=40)
selector_cat.fit(X_cat,y_cat)
#print("scores_:",selector_cat.scores_)
#print("pvalues_:",selector_cat.pvalues_)
#print(pd.DataFrame(list(zip([list(X_num.columns)],selector_num.scores_,selector_num.pvalues_))))
df_cat_kbest = pd.DataFrame(list(zip(list(X_cat.columns),selector_cat.scores_,selector_cat.pvalues_)), columns=['Feature','Score','P-value'])
print(df_cat_kbest.sort_values('Score', ascending=False))


# Looks like bothf_classif as well as chi2 give similar ranking for categorical features. So we can just use f_classif rankings itself.

# #### Get Top 30/40 categorical features

# In[ ]:


X_cat_top30 = list(df_cat_kbest.sort_values('Score', ascending=False).Feature[:30])
print('Top 30 Categorical Features: ',X_cat_top30)


# In[ ]:


# Combine Top 7 numerical features and Top 30 categorical features
top_37_features = X_num_top7 + X_cat_top30
top_37_features


# ### Conclusion from SelectKBest
# 
# We can either select the top 40 features from the overall list that as numerical as well as categorical features. Or we can take top 7 features from numerical and the top 30 categorical features. Lets take the latter approach and get the final list of features to be considered. We will then redetermine the feature and target arrays from this and proceed with machine learning tasks.
# 
# The final 37 features in our first feature selection model are :
# 

# In[ ]:


top_37_features


# In[ ]:


X_FE1 = train_2[top_37_features]
X_FE1.shape
y_FE1 = train_2.Cover_Type
y_FE1[:5]

# Split X and y into Train and Validation sets
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X_FE1,y_FE1,test_size = 0.2,random_state = 99)


# ## Run RF, Extra trees and LGBM with new reduced data set

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

# Function to execute random forest
def rf_grid(X_train,y_train, param_grid, cv=5):
    rf = RandomForestClassifier(random_state=99)
    rf_grid = GridSearchCV(rf,param_grid, cv=5)
    rf_grid.fit(X_train,y_train)
    y_pred = rf_grid.predict(X_val)
    print(pd.DataFrame(rf_grid.cv_results_)[['params','mean_test_score']])
    print('Random Forest Best Parameters: ',rf_grid.best_params_)
    print('Random Forest Best Training Score: ',rf_grid.best_score_)
    print('Random Forest Validation Accuracy is: ', accuracy_score(y_val,y_pred))

param_grid_rf = {'n_estimators': [700,800,1000,1200,1400,1600,1800]}

# Execute Random Forest
rf_grid(X_train,y_train,param_grid_rf)


# In[ ]:


from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

# Function to execute Extremely Randomized Trees
def extra_trees_grid(X_train,y_train, param_grid, cv=5):
    extra_trees = ExtraTreesClassifier(random_state=99)
    extra_trees_grid = GridSearchCV(extra_trees,param_grid, cv=5)
    extra_trees_grid.fit(X_train,y_train)
    y_pred = extra_trees_grid.predict(X_val)
    print(pd.DataFrame(extra_trees_grid.cv_results_)[['params','mean_test_score']])
    print('Extra Trees Best Parameters: ',extra_trees_grid.best_params_)
    print('Extra Trees Best Training Score: ',extra_trees_grid.best_score_)
    print('Extra Trees Validation Accuracy is: ', accuracy_score(y_val,y_pred))
    
param_grid_extra = {'n_estimators': [700,1000,1400,1700,2000,2200,2400]}

# Execute Extremely Randomized Trees
extra_trees_grid(X_train,y_train,param_grid_extra)


# In[ ]:


from lightgbm import LGBMClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

# Function to execute lightGBM classifier
def lgbm_grid(X_train,y_train, param_grid, cv=5):
    lgbm = LGBMClassifier(random_state=99)
    lgbm_grid = GridSearchCV(lgbm,param_grid, cv=5)
    lgbm_grid.fit(X_train,y_train)
    y_pred = lgbm_grid.predict(X_val)
    print(pd.DataFrame(lgbm_grid.cv_results_)[['params','mean_test_score']])
    print('LightGBM Best Parameters: ',lgbm_grid.best_params_)
    print('LightGBM Best Training Score: ',lgbm_grid.best_score_)
    print('LightGBM Validation Accuracy is: ', accuracy_score(y_val,y_pred))

param_grid_lgbm = {'n_estimators': [1000,1200,1400,1600,1800]}

# Execute LightGBM classifier
lgbm_grid(X_train,y_train,param_grid_lgbm)

