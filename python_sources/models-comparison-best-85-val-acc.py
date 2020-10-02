#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/HinePo/Heart-disease-classification-and-Hyper-Parameter-tuning/blob/master/Heart_Disease_Classification.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Classification and Hyper-Parameter Optimization

# In this kernel I will try to find the best model to predict heart disease. It is a classification problem (person has heart disease? yes or no), and I will do some tests and analysis on the models and hyper parameters.
# 
# Dataset:
# https://www.kaggle.com/ronitf/heart-disease-uci

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use("bmh")

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn import metrics


# # Loading the data

# In[ ]:


df = pd.read_csv('../input/heart-disease-uci/heart.csv')


# In[ ]:


df.head()


# # Overview and Exploration

# In[ ]:


df.describe()


# In[ ]:


# there are no missing values on the dataset
df.isnull().values.any()


# In[ ]:


df.shape


# In[ ]:


df.dtypes


# In[ ]:


# unique values on column 'cp'
set(df.cp)


# In[ ]:


# group by 'cp'
df.groupby('cp').count()


# In[ ]:


df.groupby('target').count()


# In[ ]:


corr = df.corr()
plt.figure(figsize=(14,14))
sns.heatmap(corr, annot = True, vmin=-1, vmax=1, center= 0, cmap= 'coolwarm')


# Color control: https://python-graph-gallery.com/92-control-color-in-seaborn-heatmaps/

# In[ ]:


sns.heatmap(corr, vmin = -1, vmax = 1, cmap = 'Greens')


# Dataset: https://www.kaggle.com/ronitf/heart-disease-uci
# 
# "Experiments with the Cleveland database have concentrated on simply attempting to distinguish presence (values 1,2,3,4) from absence (value 0). See if you can find any other trends in heart data to predict certain cardiovascular events or find any clear indications of heart health."
# 
# So, we will use 'target' column as our predicted variable.

# # Features and target

# In[ ]:


# use the dataframe variable to create an array with the columns names 
all_vars = np.array(df.columns)
all_vars


# In[ ]:


# define features
features = np.array(all_vars[0:13])
features


# In[ ]:


# define target
target = np.array(all_vars[13])
target


# # Splitting

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size = 0.2,
                                                      stratify = df[target], random_state = 0)


# # Models

# In[ ]:


# defining variable to store the results
all_models = []
all_scores = []


# ## Support Vector Machine

# Link for documentation:
# https://scikit-learn.org/stable/modules/svm.html

# In[ ]:


from sklearn.svm import LinearSVC


# In[ ]:


def svm_test(X_train, y_train, cv = 10):
  np.random.seed(0)
  svc = LinearSVC(random_state=0)
  cv_scores = cross_val_score(svc, X_train, y_train, scoring = 'accuracy', cv = cv, n_jobs = -1)
  print('Average of', cv, 'tests: ', cv_scores.mean())
  return cv_scores.mean()


# In[ ]:


res = svm_test(X_train, y_train)


# In[ ]:


# updating results 
all_models = np.append(all_models, "SVC")
all_scores = np.append(all_scores, round(res, 4))


# In[ ]:


all_models, all_scores


# ## Random Forest

# Link for documentation: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

# In[ ]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


def rfc_test(X_train, y_train, n_estimators = 100, cv = 10):
  np.random.seed(0)
  rfc = RandomForestClassifier(n_estimators = n_estimators, random_state = 0, n_jobs = -1)
  cv_scores = cross_val_score(rfc, X_train, y_train, scoring = 'accuracy', cv = cv, n_jobs = -1)
  print('Average of', cv, 'tests: ', cv_scores.mean())
  return cv_scores.mean()


# In[ ]:


res = rfc_test(X_train, y_train)


# In[ ]:


# updating results 
all_models = np.append(all_models, "RFC")
all_scores = np.append(all_scores, round(res, 4))


# ## XGBClassifier

# Link for documentation: https://xgboost.readthedocs.io/en/latest/python/python_api.html#module-xgboost.sklearn

# In[ ]:


from xgboost import XGBClassifier


# In[ ]:


def xgb_test(X_train, y_train, n_estimators = 100, cv = 10):
  np.random.seed(0)
  xgb = XGBClassifier(n_estimators = n_estimators, random_state = 0, n_jobs = -1)
  cv_scores = cross_val_score(xgb, X_train, y_train, scoring = 'accuracy', cv = cv, n_jobs = -1)
  print('Average of', cv, 'tests: ', cv_scores.mean())
  return cv_scores.mean()


# In[ ]:


res = xgb_test(X_train, y_train)


# In[ ]:


# updating results 
all_models = np.append(all_models, "XGB")
all_scores = np.append(all_scores, round(res, 4))


# ## Multi-Layer Perceptron

# Link for documentation: https://scikit-learn.org/stable/modules/neural_networks_supervised.html

# In[ ]:


from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# In[ ]:


def mlp_test(X_train, y_train, cv = 10):
  np.random.seed(0)

  mlp = MLPClassifier(random_state=0)
  scaler = StandardScaler()
  pipe = Pipeline([('scaler', scaler), ('mlp', mlp)])

  cv_scores = cross_val_score(pipe, X_train, y_train, scoring = 'accuracy', cv = cv, n_jobs = -1)
  print('Average of', cv,  'tests: ', cv_scores.mean())
  return cv_scores.mean()


# In[ ]:


res = mlp_test(X_train, y_train)


# In[ ]:


# updating results 
all_models = np.append(all_models, "MLP")
all_scores = np.append(all_scores, round(res, 4))


# # Fit model

# ## Random Forest

# In[ ]:


# fitting/training only for all the features case, since it has proven to show better results
model = RandomForestClassifier(random_state = 0, n_jobs = -1)
model.fit(X_train, y_train)


# In[ ]:


predictions = model.predict(X_test)
score = metrics.accuracy_score(y_test, predictions)
print("Results for test data: Random Forest trained", round(score, 4))


# In[ ]:


# updating results 
all_models = np.append(all_models, "RFC trained")
all_scores = np.append(all_scores, score)


# In[ ]:


cm_rfc = confusion_matrix(predictions, y_test)
cm_rfc


# ## XGB

# In[ ]:


model2 = XGBClassifier(random_state = 0, n_jobs = -1)
model2.fit(X_train, y_train)


# In[ ]:


predictions = model2.predict(X_test)
score = metrics.accuracy_score(y_test, predictions)
print("Results for test data: XGB trained", score)


# In[ ]:


# updating results 
all_models = np.append(all_models, "XGB trained")
all_scores = np.append(all_scores, round(score, 4))


# # Hyper Parameter Optimization

# In[ ]:


from sklearn.model_selection import RandomizedSearchCV


# ## Define parameter dictionary and distribution

# Link for RandomizedSearchCV documentation
# 
# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html

# As an example, we will experiment optmizing the RandomForestClassifier model with two models: RandomForestClassifier and XGBClassifier.

# In[ ]:


# parameters dictionary for RFC
# check documentation for RFC

params_rfc = {
 "n_estimators"             : [50, 100, 150, 200],
 "min_samples_leaf"         : [1, 2, 3, 4, 5],
 "min_weight_fraction_leaf" : [0.00, 0.05, 0.10, 0.15, 0.20],
 "random_state"             : [0],
 "n_jobs"                   : [-1]
}


# In[ ]:


# parameters dictionary for XGB
# check documentation for XGB

params_xgb = {
 "n_estimators"     : [100, 150, 200, 250],
 "learning_rate"    : [0.50, 0.6, 0.7, 0.8, 0.9],
 "max_depth"        : [3, 5, 8, 10, 12],
 "gamma"            : [0.5, 0.7, 0.8, 0.9],
 "colsample_bytree" : [0.3, 0.5, 0.60, 0.80, 0.90, 0.95],
 "random_state"     : [0],
 "n_jobs"           : [-1]
}


# ## Optimizing RFC

# In[ ]:


# optimizing rfc (Random Forest Classifier)
random_search_rfc = RandomizedSearchCV(RandomForestClassifier(),
                                       param_distributions = params_rfc,
                                       scoring = 'accuracy',
                                       n_jobs = -1,
                                       random_state = 0,
                                       cv=10)

random_search_rfc.fit(X_train, y_train)


# In[ ]:


# Random Search score for the training data
random_search_rfc.score(X_train,y_train)


# In[ ]:


# optimized RFC model
random_search_rfc.best_estimator_


# In[ ]:


# optimized RFC parameters
random_search_rfc.best_params_


# In[ ]:


# average score of 3 folds for the best estimator
random_search_rfc.best_score_


# In[ ]:


# cv score for the optimized RFC model
opt_rfc = random_search_rfc.best_estimator_

score = cross_val_score(opt_rfc, X_train, y_train, cv = 10)
print("Cross Validation score for Optimized Random Forest", score.mean())


# In[ ]:


# updating results 
all_models = np.append(all_models, "RFC opt")
all_scores = np.append(all_scores, round(score.mean(), 4))


# In[ ]:


# predict on test data
predictions = opt_rfc.predict(X_test)

# evaluate results
score = metrics.accuracy_score(y_test, predictions)
print("Results for test data: Random Forest Optimized and trained", score)


# In[ ]:


# updating results 
all_models = np.append(all_models, "RFC opt (val acc)")
all_scores = np.append(all_scores, round(score, 4))


# In[ ]:


cm_rfc_opt = confusion_matrix(predictions, y_test)
cm_rfc_opt


# ## Optimizing XGBClassifier

# In[ ]:


# optimizing xgb (XGB Classifier)
random_search_xgb = RandomizedSearchCV(XGBClassifier(),
                                       param_distributions = params_xgb,
                                       scoring = 'accuracy',
                                       n_jobs = -1,
                                       random_state = 0,
                                       cv=10)

random_search_xgb.fit(X_train, y_train)


# In[ ]:


# Random Search score for the training data
random_search_xgb.score(X_train, y_train)


# In[ ]:


# optimized XGB model
random_search_xgb.best_estimator_


# In[ ]:


# optimized XGB parameters
random_search_xgb.best_params_


# In[ ]:


# average score of 3 folds for the best estimator
random_search_xgb.best_score_


# In[ ]:


# cv score for the optimized RFC model
opt_xgb = random_search_xgb.best_estimator_

score = cross_val_score(opt_xgb, X_train, y_train, cv = 10)
print("Cross Validation score for Optimized XGB", score.mean())


# In[ ]:


# updating results 
all_models = np.append(all_models, "XGB opt")
all_scores = np.append(all_scores, round(score.mean(), 4))


# In[ ]:


# predict on test data
predictions = opt_xgb.predict(X_test)

# evaluate results
score = metrics.accuracy_score(y_test, predictions)
print("Results for test data: XGB Optimized and trained", score)


# In[ ]:


# updating results 
all_models = np.append(all_models, "XGB opt (val acc)")
all_scores = np.append(all_scores, round(score, 4))


# In[ ]:


cm_xgb_opt = confusion_matrix(predictions, y_test)
cm_xgb_opt


# # Results

# In[ ]:


all_models, all_scores


# In[ ]:


argsort = np.argsort(all_scores)
all_scores_sorted = all_scores[argsort]

all_models_names = all_models
all_models_sorted = all_models_names[argsort]

plt.figure(figsize=(10,6))
fig, ax = plt.subplots()
ax.barh(all_models_sorted, all_scores_sorted)
plt.xlim(0, 1)
plt.title("Heart disease prediction: Model vs Accuracy")
for index, value in enumerate(all_scores_sorted):
    plt.text(value, index, str(round(value, 4)), fontsize = 12)


# # Conclusions

# For this heart disease prediction problem it's possible to achieve accuracies above 85 % when predicting in new data.
