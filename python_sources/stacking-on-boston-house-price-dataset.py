#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_boston
import warnings
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor, BaggingRegressor, RandomForestRegressor, StackingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor


# In[ ]:


# Function Approach to do the same
def _df(load):
  # Creating Dataframe
  df = pd.DataFrame(data = load.data, columns = load.feature_names)
  # Adding Output to the DF
  df["label"] = load.target
  # Return df
  return(df)


# In[ ]:


df = _df(load_boston()) # Running Function Created Above


# In[ ]:


df.columns


# In[ ]:


# Data Dictionary
print(load_boston().DESCR)


# In[ ]:


# Splitting the Data in Train and Test
from sklearn.model_selection import train_test_split

# Getting X and Ys
X = df.drop("label", axis = 1)
y = df.label

# Creating Train and Test
xtrain,xtest,ytrain,ytest = train_test_split(X, y, test_size = 0.33, random_state = None)


# In[ ]:


# Apply Linear Regression Model as Base Model
lr = LinearRegression()
pred_lr = lr.fit(xtrain, ytrain).predict(xtest)

# Checking Model Metrics
from sklearn.metrics import r2_score, mean_squared_error
print("R2 Score: ", r2_score(ytest, pred_lr))
print("RMSE: ", np.sqrt(mean_squared_error(ytest, pred_lr)))


# # Base Model: Linear Regression
# 
# The Base Model reports R Sqaured Value: 0.67 and RMSE: 5.6.
# Now, we will use Stacking to Improve the Performance of the Model(s).
# 
# Stacking generally uses lots of models and finds the best predicted values from each model and creates a meta learner to learn from the training set + predicted values to generate a Super Model that improves the overall performance.

# In[ ]:


# Checking Sklearn Version
import sklearn
sklearn.__version__


# In[ ]:


# Get a List of Models as Base Models
def base_models():
  models = dict()
  models['lr'] = LinearRegression()
  models["Ridge"] = Ridge()
  models["Lasso"] = Lasso()
  models["Tree"] = DecisionTreeRegressor()
  models["Random Forest"] = RandomForestRegressor()
  models["Bagging"] = BaggingRegressor()
  models["GBM"] = GradientBoostingRegressor()
  return models


# In[ ]:


# Now we will apply K Fold Cross Validation. We will now create a evaluate function with Repeated Stratified K Fold
# And Capture the Cross Val Score
from sklearn.model_selection import RepeatedKFold
from matplotlib import pyplot

# Function to evaluate the list of models
def eval_models(model):
  cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
  scores = -cross_val_score(model, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1, 
                            error_score='raise')
  return scores


# In[ ]:


# Lets Apply and Calculate the Scores
# Getting X and Ys
X = df.drop("label", axis = 1)
y = df.label

# get the models to evaluate
models = base_models()
# evaluate the models and store results
results, names = list(), list() 

for name, model in models.items():
  scores = eval_models(model)
  results.append(scores)
  names.append(name)
  print('>%s %.3f (%.3f)' % (name, scores.mean(), scores.std()))


# In[ ]:


# plot model performance for comparison
pyplot.boxplot(results, labels=names, showmeans=True)
pyplot.xticks(rotation = 90)
pyplot.ylabel("MSE")
pyplot.title("Model Performance")
pyplot.show()


# In[ ]:


# get a stacking ensemble of models
def get_stacking():
	# define the base models
  level0 = list()
  level0.append(('Tree', DecisionTreeRegressor()))
  level0.append(('RF', RandomForestRegressor()))
  level0.append(('XGB', XGBRegressor()))
  level0.append(('Bagging', BaggingRegressor()))
	# define meta learner model
  level1 = LGBMRegressor()
	# define the stacking ensemble
  model = StackingRegressor(estimators=level0, final_estimator=level1, cv=5)
  return model


# In[ ]:


def base_models():
  models = dict()
  models["Tree"] = DecisionTreeRegressor()
  models["Random Forest"] = RandomForestRegressor()
  models["Bagging"] = BaggingRegressor()
  models["XGB"] = XGBRegressor()
  models["Stacked Model"] = get_stacking()
  return models


# In[ ]:


# Function to evaluate the list of models
def eval_models(model):
  cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
  scores = -cross_val_score(model, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1, 
                            error_score='raise')
  return scores


# get the models to evaluate
models = base_models()
# evaluate the models and store results
results, names = list(), list() 

for name, model in models.items():
  scores = eval_models(model)
  results.append(scores)
  names.append(name)
  print('>%s %.3f (%.3f)' % (name, scores.mean(), scores.std()))


# plot model performance for comparison
pyplot.boxplot(results, labels=names, showmeans=True)
pyplot.xticks(rotation = 90)
pyplot.ylabel("MSE")
pyplot.title("Model Performance")
pyplot.show()


# In[ ]:


# Lets apply on Train and Test Split
level0 = list()
level0.append(('Tree', DecisionTreeRegressor()))
level0.append(('RF', RandomForestRegressor()))
level0.append(('GBM', GradientBoostingRegressor()))
level0.append(('Bagging', BaggingRegressor()))
level0.append(("XGB", XGBRegressor()))


# In[ ]:


level1 = LGBMRegressor()
model = StackingRegressor(estimators=level0, final_estimator=level1, cv=10)


# In[ ]:


# Making Predictions on Train & Test
stacked_pred = model.fit(xtrain, ytrain).predict(xtest)


# In[ ]:


# Checking Model Metrics
print(r2_score(ytest, stacked_pred))
print(np.sqrt(mean_squared_error(ytest, stacked_pred)))


# ## Conclusion
# 
# Hence, it is clear that LightGBM is a better stacked model as it has increased the R2 Score to 0.82 & RMSE has been reduced to 3.78.
