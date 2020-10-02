#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# This my notebook/Kernel that is  derived from the **[Kaggle Machine Learning module](https://www.kaggle.com/learn/machine-learning)**. This was to help me get familiar with a Kaggle competition and creating/submitting predictions for a competition. 
# 
# I want to get familar with this since I believe machine learning competitions are a way to improve my data science skills and measure my progress. 
# 
# With that being said, this Kernel looks at a dataset with housing attributes and is mainly concerned with trying to predict housing prices. 
# 
# If you do end up gleaming anything useful from this Kernel, please upvote (Kaggle's version of like?) and also feel free to give feedback. If you end up using some of this code, please do not forget to reference this Kernel and me. (Also, a comment with a link to your Kernel would be cool too.)
# 
# Anyway, there is no salad in this Kernel if you were expecting some free salad. I apologize, but lettuce turnip the beet and get on to the rest of Kernel!
# 

# ## Data
# 
# As mentioned before, the data is mainly concerned with housing attributes for some houses in Iowa. 
# 
# This section loads in the data and the appropiate libraries and functions.
# 
# As a first step, we are just going to use attributes/features that are numerical and then use imputing to fill in any missing/na values.

# In[ ]:


# Import Desired Libraries 
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble.partial_dependence import partial_dependence, plot_partial_dependence
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.metrics import mean_absolute_error

# Read file/path for training data
iowa_file_path = '../input/train.csv'
home_data = pd.read_csv(iowa_file_path)
# Read file/path for predictions
test_data_path = '../input/test.csv'
test_data = pd.read_csv(test_data_path)

# Create target object and call it y
y = home_data.SalePrice

# Create X Data (only select numeric data for now)
X = home_data.drop('SalePrice', axis=1)
test_X = test_data

#Save off Orig X's before changing them
X_orig = X
test_X_orig = test_X

# TODO: Look into moving get dummies and col with missing into pipeline
X= pd.get_dummies(X) 
test_X = pd.get_dummies(test_X)

# Create new columns indicating which rows/cols are going to be imputed
cols_with_missing = [col for col in X.columns if X[col].isnull().any()]
impute_X = X.copy()
impute_test_X = test_X.copy()
for col in cols_with_missing:
    impute_X[col+'_was_missing']= impute_X[col].isnull()
    impute_test_X[col+'_was_missing']= impute_test_X[col].isnull()
X = impute_X
test_X = impute_test_X

# Create Dataframe to store model CV results
cvResultsdf = pd.DataFrame(columns=['Model Name','CV Mean Score','Model'])

# Define constants/variables to use
seed_Num = 8 # aka Random State
scoring_type = 'neg_mean_absolute_error'
cv_folds = 3


# ## Models 
# This section will go over the models selected. Each model will be a pipeline of a simple imputer and then the model itself. We will also use the mean score from a 5-fold cross validation of mean absolute error to compare the models.

# In[ ]:


# Tuned Decision Tree
estimators = [('Imputer', SimpleImputer()), ('model', DecisionTreeRegressor(random_state=seed_Num))]
pipe = Pipeline(estimators)
# Set Parameters for tuning
parameters = {'model__max_depth':[5, 10, 50], 
              'model__max_leaf_nodes':[10, 100, 300]}
# Create Grid CV to test out parameters with CV
decTrReg = GridSearchCV(pipe, cv = cv_folds,n_jobs = -1,
                   param_grid = parameters, 
                   scoring= scoring_type)
decTrReg.fit(X,y)
best_score = -decTrReg.best_score_
cvResultsdf.loc[len(cvResultsdf)] = ['Tuned Decision Tree', best_score, decTrReg]
print("CV Mean MAE for Tuned Decision Tree: {:,.0f}".format(best_score))


# In[ ]:


# Tuned Random Forest
estimators = [('Imputer', SimpleImputer()), ('model', RandomForestRegressor(random_state=seed_Num))]
pipe = Pipeline(estimators)
# Set Parameters for tuning
parameters = {'model__n_estimators':[10, 100], 
              'model__max_leaf_nodes':[10, 100]}
# Create Grid CV to test out parameters with CV
randForestReg = GridSearchCV(pipe, cv = 4, n_jobs = -1,
                   param_grid=parameters, 
                   scoring= scoring_type)
randForestReg.fit(X,y)
best_score = -randForestReg.best_score_
cvResultsdf.loc[len(cvResultsdf)] = ['Random Forest', best_score, randForestReg]
print("CV Mean MAE for Tuned Random Forest Model: {:,.0f}".format(best_score))


# In[ ]:


# Out of Box XGBR Model
estimators = [('Imputer', SimpleImputer()), ('model', XGBRegressor(random_state=seed_Num))]
pipe = Pipeline(estimators)
pipe.fit(X,y)
scores = -cross_val_score(pipe, X, y, cv=cv_folds, scoring=scoring_type)
score = scores.mean()
cvResultsdf.loc[len(cvResultsdf)] = ['Out of Box XGBR Model', score, pipe]
print("CV Mean MAE for Out of Box XGBRegressor Model: {:,.0f}".format(score))


# In[ ]:


# Tuned XGboost
estimators = [('Imputer', SimpleImputer()), ('model', XGBRegressor(random_state=seed_Num))]
pipe = Pipeline(estimators)
# Set Parameters for tuning
parameters = {'model__max_depth':range(2,10), 
                'model__min_child_weight':range(1,6)}
# Create Grid CV to test out parameters with CV
xgbReg = GridSearchCV(pipe, cv = 4,n_jobs = -1,
                   param_grid=parameters, 
                   scoring= scoring_type)
xgbReg.fit(X,y)
best_score = -xgbReg.best_score_
cvResultsdf.loc[len(cvResultsdf)] = ['Tuned XGBR Model', best_score, xgbReg]
print("CV Mean MAE for Tuned XGBRegressor Model: {:,.0f}".format(best_score))


# # Compare Models and Select a Model
# Here, we will compare the error of the models (lower error = better).

# In[ ]:


cvResultsdf.sort_values(by=['CV Mean Score'], inplace=True)
print(cvResultsdf[['Model Name','CV Mean Score']])
# Get Model with lowest CV Mean Score
selected_model = cvResultsdf.loc[cvResultsdf['CV Mean Score'].idxmin()].Model


# Here, we see that the Tuned XGBRegressor Model had the lower CV Mean Score. This will be our selected model.
# 

# In[ ]:


# Check out permutation importance
#perm = PermutationImportance(selected_model, random_state=8).fit(X, y)
#eli5.show_weights(perm, feature_names = X.columns.tolist())


# # Make Predictions
# Now, we wll fit the selected model to all of the data. Then we will apply the fitted model to make predictions based on the test data. This will be our submission and viola! We are done.

# In[ ]:


# Make predictions
_, final_test_X = X.align(test_X,join='left',axis=1)
test_preds = selected_model.predict(final_test_X)

# The lines below shows you how to save your data in the format needed to score it in the competition
output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_preds})

output.to_csv('submission.csv', index=False)


# Even though it might not be a 'home' run Kernel, I hope you enjoyed my Kernel! It is slowly evolving as I experiment and tinker with it, but I also want to keep it somewhat short a simple. 
# 
# If you enjoyed the Kernel, please like it (aka Upvote). Also, let me know if you have any comments, concerns, feedback, or questions.
# 
# ## Sources:
# [1] I have mainly used the Kaggle Learn **[Machine Learning Modules](https://www.kaggle.com/learn/machine-learning)** to help with starting this Kernel. 
# 
# [2] Of course, **[Google](https://www.google.com/)** has been indispensable as a search engine for my various bugs/concerns/questions. It has led me to sites like **[Stack Overflow](https://stackoverflow.com/)**
# 
# [3] **[Sklearn Site](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html#sklearn.model_selection.GridSearchCV)** is also helpful with the various sklearn details and nuances, like GridSearchCV
# 
# [4] For some preprocessing, I have also looked at **[Vijay Narayanan's Kernel](https://www.kaggle.com/pnvijay/exercise-machine-learning-competitions)** from this competition.
# 
