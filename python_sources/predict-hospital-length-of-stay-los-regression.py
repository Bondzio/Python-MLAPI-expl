#!/usr/bin/env python
# coding: utf-8

# * The original data is from MIMIC2 - Multiparameter Intelligent Monitoring in Intensive Care (deidentified DB) available freely from 
# https://mimic.physionet.org/
# * Each instance in the mldata.csv attached is one admission
# * Testing a theory I have, that one can predict LOS just by the number of interactions betweeen patient and hospital per day, I've used the following features for the LOS prediction as a REGRESSION problem:
# * Age, Gender, Ethnicity, Insurance, Admission Type, Admission Source, etc.
# * Number of Diagnosis on Admission, Procedures on Admission
# * Daily average number of: Labs, Micro labs, IV meds, Non-IV meds, Imaging Reports, Notes, Orders, Caregivers, Careunits
# 
# The label is LOS in days
# 
# I've compared initially 12 REGRESSOR models.  
# 
# 
# Let me know *your* results on this (overly simplified) dataset

# In[ ]:


# IMPORT MODULES
# TURN ON the GPU !

import os
from operator import itemgetter    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
get_ipython().magic(u'matplotlib inline')
plt.style.use('ggplot')

from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn import preprocessing
from sklearn.preprocessing import Imputer
from pandas.tools.plotting import scatter_matrix
from sklearn.preprocessing import RobustScaler, StandardScaler, LabelEncoder, MinMaxScaler, OneHotEncoder, LabelBinarizer
from sklearn.metrics import mean_squared_error, accuracy_score, mean_absolute_error
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV, KFold, cross_val_predict, StratifiedKFold, train_test_split, learning_curve, ShuffleSplit
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, SGDRegressor, BayesianRidge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor, BaggingRegressor
from sklearn.svm import SVR, LinearSVR
from sklearn.kernel_ridge import KernelRidge
from xgboost import XGBRegressor

import tensorflow as tf

from keras import models, regularizers, layers, optimizers, losses, metrics
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils

print(os.getcwd())
print("Modules imported \n")
import os
print(os.listdir("../input"))


# In[ ]:


# Load MIMIC2 data 

data = pd.read_csv('../input/mimic3a.csv')
print("With id", data.shape)
data_full = data.drop('hadm_id', 1)
print("No id",data_full.shape)


# In[ ]:


print(data_full.shape)
data_full.info()
data_full.describe()


# In[ ]:


data_full.head(10)


# In[ ]:


# Label = LOS
y = data_full['LOSdays']
X = data_full.drop('LOSdays', 1)
X = X.drop('ExpiredHospital', 1)
X = X.drop('AdmitDiagnosis', 1)
X = X.drop('AdmitProcedure', 1)
X = X.drop('marital_status', 1)
X = X.drop('ethnicity', 1)
X = X.drop('religion', 1)
X = X.drop('insurance', 1)

print("y - Labels", y.shape)
print("X - No Label No id ", X.shape)
print(X.columns)


# In[ ]:


data_full.hist(bins=30, figsize=(20,15))
plt.show()


# In[ ]:


age_histogram = data_full.hist(column='age', bins=20, range=[0, 100])
for ax in age_histogram.flatten():
    ax.set_xlabel("Age")
    ax.set_ylabel("Num. of Patients")
    
age_LOS = data_full.hist(column='LOSdays', bins=20, range=[0, 100])
for ax in age_LOS.flatten():
    ax.set_xlabel("LOS")
    ax.set_ylabel("Num. of Patients")


# data_full.groupby('insurance').size().plot.bar()
# plt.show()
# data_full.groupby('admit_type').size().plot.bar()
# plt.show()
# data_full.groupby('admit_location').size().plot.bar()
# plt.show()

# In[ ]:


# Pearson linear correlation

corr_matrix = data_full.corr()
corr_matrix["LOSdays"].sort_values(ascending=False)


# # IMPUTE missing values
# 
# X.fillna(value='unknown', axis=1, inplace=True)

# In[ ]:


# Check that all X columns have no missing values
X.info()
X.describe()


# In[ ]:


#data_full.plot(kind="scatter", x="sofa_max", xlim=(0,25), y="LOS", alpha=0.1, ylim=(0,50))
data_full.plot(kind="scatter", x="age", xlim=(0,100), y="LOSdays", alpha=0.1, ylim=(0,50))
data_full.plot(kind="scatter", x="TotalNumInteract", xlim=(0,300), y="LOSdays", alpha=0.1, ylim=(0,50))


# In[ ]:


# MAP Text to Numerical Data
# Use one-hot-encoding to convert categorical features to numerical

print(X.shape)
categorical_columns = [
                       'gender',                     
                      'admit_type',
                      'admit_location'                      
                      ]

for col in categorical_columns:
    #if the original column is present replace it with a one-hot
    if col in X.columns:
        one_hot_encoded = pd.get_dummies(X[col])
        X = X.drop(col, axis=1)
        X = X.join(one_hot_encoded, lsuffix='_left', rsuffix='_right')
        
print(X.shape)


# In[ ]:


print(X.columns)


# In[ ]:



print(data_full.shape)
print(X.shape)
#XnotNorm = np.array(X.copy())
XnotNorm = X.copy()
print('XnotNorm ', XnotNorm.shape)

yFI = data_full.LOSdays
ynotNorm = yFI.copy()
print('ynotNorm ', ynotNorm.shape)


# In[ ]:


# Normalize X

x = XnotNorm.values #returns a numpy array
scaler = preprocessing.StandardScaler()
x_scaled = scaler.fit_transform(x)
XNorm = pd.DataFrame(x_scaled, columns=XnotNorm.columns)
print(XNorm)


# In[ ]:


# Normalize y

y = ynotNorm.values #returns a numpy array
y = y.reshape(-1, 1)
y_scaled = scaler.fit_transform(y)
ynorm=pd.DataFrame(y_scaled)
print(ynorm)


# In[ ]:


# FEATURE IMPORTANCE Data NOT normalized using Lasso model - NOT the best one ...

trainFinalFI = XnotNorm
yFinalFI = ynotNorm

lasso=Lasso(alpha=0.001, copy_X=True, fit_intercept=True, max_iter=1000,
   normalize=False, positive=False, precompute=False, random_state=None,
   selection='cyclic', tol=0.0001, warm_start=False)
lasso.fit(trainFinalFI,yFinalFI)

FI_lasso = pd.DataFrame({"Feature Importance":lasso.coef_}, index=trainFinalFI.columns)

# Focus on those with 0 importance
#print(FI_lasso.sort_values("Feature Importance",ascending=False).to_string())
#print("_"*80)
FI_lasso[FI_lasso["Feature Importance"] >0.2].sort_values("Feature Importance").plot(kind="barh",figsize=(15,25))
plt.xticks(rotation=90)
FI_lasso[FI_lasso["Feature Importance"] <-0.2].sort_values("Feature Importance").plot(kind="barh",figsize=(15,25))
plt.xticks(rotation=90)
plt.show()


# In[ ]:


# CROSS VALIDATION

def rmse_cv(model,X,y):
    rmse = np.sqrt(-cross_val_score(model, X, y, scoring="neg_mean_squared_error", cv=5))
    return rmse


# # Lin reg ALL models HYPERPARAMS NOT optimized
# 
# models = [LinearRegression(),Ridge(),Lasso(),RandomForestRegressor(),GradientBoostingRegressor(),SVR(),LinearSVR(),
#           ElasticNet(),SGDRegressor(),BayesianRidge(),KernelRidge(),ExtraTreesRegressor()]
# names = ["LinearRegression", "Ridge", "Lasso", "RandomForestRegressor", "GradientBoostingRegressor", "SVR", "LinearSVR", 
#          "ElasticNet","SGDRegressor","BayesianRidge","KernelRidge","ExtraTreesRegressor"]
#          

# In[ ]:


# Lin reg ALL models HYPERPARAMS NOT optimized

models = [RandomForestRegressor(), ExtraTreesRegressor(), GradientBoostingRegressor()]
names = ["RandomForestRegressor", "ExtraTreesRegressor", "GradientBoostingRegressor"]


# In[ ]:


# Run the models and compare

ModScores = {}

for name, model in zip(names, models):
    score = rmse_cv(model, XNorm, ynorm)
    ModScores[name] = score.mean()
    print("{}: {:.2f}".format(name,score.mean()))

print("_"*100)
for key, value in sorted(ModScores.items(), key = itemgetter(1), reverse = False):
    print(key, round(value,3))


# In[ ]:


# Optimize hyper params for one model

model = RandomForestRegressor()

param_grid = [{},]

grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(XNorm, ynorm)

print(grid_search.best_estimator_)


# In[ ]:


model = RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
           max_features='auto', max_leaf_nodes=None,
           min_impurity_decrease=0.0, min_impurity_split=None,
           min_samples_leaf=1, min_samples_split=2,
           min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
           oob_score=False, random_state=None, verbose=0, warm_start=False)


# In[ ]:


# FEATURE IMPORTANCE - NORMALIZED - last model

trainFinalFI = XNorm
yFinalFI = ynorm

model.fit(trainFinalFI,yFinalFI)

FI_model = pd.DataFrame({"Feature Importance":model.feature_importances_,}, index=trainFinalFI.columns)
FI_model[FI_model["Feature Importance"] > 0.007].sort_values("Feature Importance").plot(kind="barh",figsize=(15,25))
plt.xticks(rotation=90)
plt.xticks(rotation=90)
plt.show()


# In[ ]:


# List of important features for model
FI_model = pd.DataFrame({"Feature Importance":model.feature_importances_,}, index=trainFinalFI.columns)
FI_model=FI_model.sort_values('Feature Importance', ascending = False)
print(FI_model[FI_model["Feature Importance"] > 0.001])


# In[ ]:


def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Error")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = 1-np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = 1-np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt


# In[ ]:


# LEARNING CURVES Train / Validation

title = "Learning Curves "
cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=42)
plot_learning_curve(model, title, XNorm, ynorm, cv=cv, n_jobs=5)
#plot_learning_curve(model, title, XNorm, y, ylim=(0.01, 0.99), cv=cv, n_jobs=4)


# In[ ]:


# Split into Train & Test

X_train, X_test, y_train, y_test = train_test_split(XNorm, ynorm, test_size=0.2, random_state=42)
print ('X_train: ', X_train.shape)
print ('X_test: ', X_test.shape)
print ('y_train: ', y_train.shape)
print ('y_test: ', y_test.shape)

# Model FINAL fit and evaluation on test

model.fit(X_train, y_train)

final_predictions = model.predict(X_test)
final_mse = mean_squared_error(y_test, final_predictions)
final_rmse = np.sqrt(final_mse) 
print("NORM rmse on test ", round(final_rmse, 4))

final_mae = mean_absolute_error(y_test, final_predictions)
print("NORM mae on test ", round(final_mae, 4))


# In[ ]:


# Split into Train & Test

#   NOTE - For ed purposes - MAE - ynotNorm was USED !!!

X_train, X_test, y_train, y_test = train_test_split(XNorm, ynotNorm, test_size=0.2, random_state=42)
print ('X_train: ', X_train.shape)
print ('X_test: ', X_test.shape)
print ('y_train: ', y_train.shape)
print ('y_test: ', y_test.shape)


# In[ ]:


# Model FINAL fit and evaluation on test

model.fit(X_train, y_train)

final_predictions = model.predict(X_test)
final_mse = mean_squared_error(y_test, final_predictions)
final_rmse = np.sqrt(final_mse) 
print("rmse on test ", round(final_rmse, 4))

final_mae = mean_absolute_error(y_test, final_predictions)
print("mae on test ", round(final_mae, 4))


# In[ ]:


# PLOT True vs Predicted

xChart = [np.array(y_test)]
yChart = [np.array(final_predictions)]

plt.scatter(xChart,yChart, alpha=0.2)
plt.xlim(0,30)
plt.ylim(0,30)
plt.plot( [0,30],[0,30], 'b')
plt.show()


# **NN model**  

# In[ ]:


# Split into Train & Test

X_train, X_test, y_train, y_test = train_test_split(XNorm, ynorm, test_size=0.2, random_state=42)
print ('X_train: ', X_train.shape)
print ('X_test: ', X_test.shape)
print ('y_train: ', y_train.shape)
print ('y_test: ', y_test.shape)


# In[ ]:


# Transfer data to NN format

x_val = X_test
partial_x_train = X_train
y_val = y_test
partial_y_train = y_train

print("partial_x_train ", partial_x_train.shape)
print("partial_y_train ", partial_y_train.shape)

print("x_val ", x_val.shape)
print("y_val ", y_val.shape)


# In[ ]:


# NN MODEL
from keras import models
model = models.Sequential()
model.add(layers.Dense(2048, activation='relu', kernel_regularizer=regularizers.l2(0.001),
                       input_shape=(partial_x_train.shape[1],)))
#model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(2048, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(2048, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(2048, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1))
model.summary()

model.compile(optimizer=optimizers.Adam(lr=1e-4), loss='mse', metrics=['mae'])
print("model compiled")


# In[ ]:


history = model.fit(partial_x_train, partial_y_train,
                    validation_data=(x_val, y_val), 
                    verbose=1,
                   epochs=100)


# In[ ]:


acc = history.history['mean_absolute_error']
val_acc = history.history['val_mean_absolute_error']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, acc, 'bo', label='Training error')
plt.plot(epochs, val_acc, 'r', label='Validation error')
plt.title('Training and validation ERROR')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation LOSS')
plt.legend()
plt.show()


# In[ ]:


# Model evaluation on test

test_mse_score, test_mae_score = model.evaluate(x_val, y_val)
final_rmse = np.sqrt(test_mse_score) 
print("rmse on test ", round(final_rmse, 4))

print("mae on test ", round(test_mae_score, 4))

