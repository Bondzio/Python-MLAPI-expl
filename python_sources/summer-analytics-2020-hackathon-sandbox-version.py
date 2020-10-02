#!/usr/bin/env python
# coding: utf-8

# # ***Importing basic libraries***
# We shall import more as and when necessary.

# In[ ]:


import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import decomposition
get_ipython().run_line_magic('matplotlib', 'inline')

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


train = pd.read_csv("/kaggle/input/train.csv")
test = pd.read_csv("/kaggle/input/test.csv")


# Now to actually see what the dataset columns look like. We shall also look for missing values, if any, and take necessary steps to fix that issue.

# In[ ]:


pd.set_option('max_columns', None)
train.describe(include = 'all')


# There seem to be no missing values in any of the columns, which is a good sign. A couple of columns are useless from the outset, like 'Id' and 'Behaviour', but we'll take care of those later.
# 
# For now, we'll look at categorical variables.

# In[ ]:


cat_train = train.select_dtypes(include = 'object')
count = 0
for i in (cat_train.columns):
    print(cat_train.columns[count], ': ', cat_train[i].unique())
    print('\n--------------------------\n')
    count += 1


# # ***Encoding categorical variables***

# In[ ]:


cat_replace = {'OverTime': {'No': 0, 'Yes': 1}}
train.replace(cat_replace, inplace = True)


# In[ ]:


obj = train.dtypes == 'object'
obj_cols = list(obj[obj].index)
# train_ohe_cols = pd.DataFrame(one_hot.fit_transform(train[obj_cols])) 

encoded = pd.DataFrame()
temp = pd.DataFrame()
for col in obj_cols:
    temp = pd.get_dummies(train[col], prefix = col)
    encoded[temp.columns] = temp

# train_ohe_cols.index = train.index
train_ohe = pd.concat([train, encoded], axis = 1)
train_encoded = train_ohe.drop(obj_cols, axis = 1)
train_encoded.head()


# # ***Finding correlation of features***

# In[ ]:


cm = train_encoded.drop(['Id', 'Behaviour'], axis = 1).corr()

plt.figure(figsize = (20, 20))
sns.heatmap(cm, square = True, xticklabels = True, yticklabels = True, cmap = 'inferno')

correlated = []
for i in range(len(cm.index)):
    for j in range(len(cm.columns)):
        if np.abs((cm.iloc[i, j])) >= 0.5 and i != j:
            correlated.append((cm.index[i], cm.columns[j], cm.iloc[i, j]))
            
len(correlated)


# # ***Applying PCA for dimensionality reduction***
# 
# We see that a bunch of columns are related (either positively or negatively). Using PCA (with 99% variance retention) should automatically solve this issue, without us having to bother about individual correlations. 
# However, this will not give us a proper idea of which features are more important than the others to the prediction. 

# In[ ]:


train_encoded.drop(['Id', 'Behaviour'], axis = 1, inplace = True)


# In[ ]:


# selecting features to scale. This includes all numerical features that aren't ordinal in nature:
features = ['Age', 'EmployeeNumber','DistanceFromHome', 'MonthlyIncome', 'NumCompaniesWorked', 'PercentSalaryHike', 
                    'TotalWorkingYears', 'YearsAtCompany','YearsInCurrentRole', 
                    'YearsSinceLastPromotion','YearsWithCurrManager', 'TrainingTimesLastYear']

from sklearn.preprocessing import StandardScaler

# scaling the entire training dataset now:
ss_final = StandardScaler()

train_std = train_encoded[features]
train_std = pd.DataFrame(ss_final.fit_transform(train_std))
train_std_full = pd.concat([train_std, train_encoded.drop(features, axis = 1)], axis = 1)

from sklearn.decomposition import PCA

pca_check = PCA(whiten = True)
pca_check.n_components = 46
pca_check.fit_transform(train_std_full.drop('Attrition', axis = 1))
var_retention = pca_check.explained_variance_ratio_.cumsum()
print("var_retention: ", var_retention, "\n ---------------------------------------------------------------------------------------------")

# pulling least value of k for which variance retention is 99% or close
for i in range(len(var_retention)):
    if var_retention[i] >= 0.98:
        print(i, ", ", var_retention[i])

full_tgt = train_std_full.Attrition
train_std_full.drop('Attrition', axis = 1, inplace = True)


# In[ ]:


# therefore, best value of n_components would be 33
pca = PCA(n_components = 33) # could try whiten = True later.
train_pca = pd.DataFrame(pca.fit_transform(train_std_full))


# # ***Recap (preprocessing on test set)***
# 
# Let us repeat the same operations on the test set that we done on the training set.
# This cell shall act as a summary for the entirety of operations done on the dataset, and I might use it to develop a pipeline later on
# 

# In[ ]:


# dropping unnecessary columns
test.drop(['Id', 'Behaviour'], axis = 1, inplace = True)


# separating categorical columns, and label/one-hot encoding them
cat_replace = {'OverTime': {'No': 0, 'Yes': 1}}
test.replace(cat_replace, inplace = True)

# replaced OneHotEncoder with pd.get_dummies() for legibility of dataframe before scaling and PCA.

encoded_test = pd.DataFrame()
temp_test = pd.DataFrame()
for col in obj_cols:
    temp_test = pd.get_dummies(test[col], prefix = col)
    encoded_test[temp_test.columns] = temp_test
    
test_encoded = pd.concat([test, encoded_test], axis = 1)
test_encoded.drop(obj_cols, axis = 1, inplace = True)

# Scaling of test set according to insights from training set:
test_std = test_encoded[features]
test_std = pd.DataFrame(ss_final.transform(test_std))
test_std_full = pd.concat([test_std, test_encoded.drop(features, axis = 1)], axis = 1)

# transforming test set via PCA:
test_pca = pd.DataFrame(pca.transform(test_std_full))


# # ***Finding the best XGBoost model***
# 
# The lines containing the GridSearchCV objects have been commented for ease of running the notebook. They can be uncommented and analyses can be run on different configurations of ***param_grid_xgb***.
# 
# **WARNING: this may take considerable time and processing power. Thus, keep** ***n_jobs = -1*** **for using all cores of your processor, to make it as speedy as possible.**

# In[ ]:


# checking for best RFC parameters:
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier

# param_grid_xgb = {
#     'n_estimators': range[100000],
#     'early_stopping rounds': [10, 20],
#     'learning_rate': [0.0005, 0.0001],
#     'max_depth': [7],
#     'verbosity': [1]
# }

# xgb_final = XGBClassifier()
# grid_search_xgb = GridSearchCV(estimator = xgb_final, param_grid = param_grid_xgb, cv = 6, n_jobs = -1)
# grid_search_xgb.fit(train_pca, full_tgt)
# grid_search_xgb.best_params_


# # ***Making the model***
# 
# Utilising the best possible values from above, suitable values of the hyperparameters can be chosen and the model can be made.

# In[ ]:


# fitting an XGBC model
xgbc_final = XGBClassifier(n_estimators = 125000, learning_rate = 0.0005,
                           max_depth = 7, n_jobs = -1, verbosity = 1)
xgbc_final.fit(train_pca, full_tgt)
pred_xgbc = xgbc_final.predict(test_pca)


# In[ ]:


test_atts = xgbc_final.predict_proba(test_pca)
prob_att = pd.Series(test_atts[:, 1])
prob_att.rename('Attrition', inplace = True)


# In[ ]:


test_orig = pd.read_csv("/kaggle/input/test.csv")

submission = pd.concat([test_orig.Id, prob_att], axis = 1)
submission.to_csv("submission.csv", index=False)
submission

