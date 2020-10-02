"""
Beating the Benchmark 
Caterpillar @ Kaggle

__author__ : Abhishek

"""

import pandas as pd
import numpy as np
from sklearn import ensemble, preprocessing, grid_search, cross_validation

# load training and test datasets
train = pd.read_csv('../input/train_set.csv', parse_dates=[2,])
test = pd.read_csv('../input/test_set.csv', parse_dates=[3,])

# create some new features
train['year'] = train.quote_date.dt.year
train['month'] = train.quote_date.dt.month
train['dayofyear'] = train.quote_date.dt.dayofyear
train['dayofweek'] = train.quote_date.dt.dayofweek
train['day'] = train.quote_date.dt.day

test['year'] = test.quote_date.dt.year
test['month'] = test.quote_date.dt.month
test['dayofyear'] = test.quote_date.dt.dayofyear
test['dayofweek'] = test.quote_date.dt.dayofweek
test['day'] = test.quote_date.dt.day


# drop useless columns and create labels
idx = test.id.values.astype(int)
test = test.drop(['id', 'quote_date'], axis = 1)
labels = train.cost.values
train = train.drop(['quote_date', 'cost'], axis = 1)


# convert data to numpy array
train = np.array(train)
test = np.array(test)

# label encode the categorical variables
for i in range(train.shape[1]):
    if i in [0,1,4]:
        lbl = preprocessing.LabelEncoder()
        lbl.fit(list(train[:,i]) + list(test[:,i]))
        train[:,i] = lbl.transform(train[:,i])
        test[:,i] = lbl.transform(test[:,i])


# object array to float
train = train.astype(float)
test = test.astype(float)

# i like to train on log(1+x) for RMSLE ;) 
# The choice is yours :)
label_log = np.log1p(labels)

# fit a gbm model
gbm = ensemble.GradientBoostingRegressor(random_state=42)
rf = ensemble.RandomForestRegressor()

# tune parameters
parameters = {'n_estimators':(1000, 2000)}
clf = grid_search.GridSearchCV(rf, parameters, verbose=1)

# cross validation
print("k-Fold RMSLE:")
cv_rmsle = cross_validation.cross_val_score(clf, train, label_log, scoring='mean_squared_error')
print(cv_rmsle)
cv_rmsle = np.sqrt(np.abs(cv_rmsle))
print(cv_rmsle)
print("Mean: " + str(cv_rmsle.mean()))

# get predictions on test
clf.fit(train, label_log)

# get predictions from the model, convert them and dump them!
preds = np.expm1(clf.predict(test))
preds = pd.DataFrame({"id": idx, "cost": preds})
preds.to_csv('benchmark.csv', index=False)

# Swipe right on tinder ;)