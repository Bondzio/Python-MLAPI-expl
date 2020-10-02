#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


df = pd.read_csv("/kaggle/input/uncover/county_health_rankings/county_health_rankings/us-county-health-rankings-2020.csv")


# In[ ]:


df.head(5)


# In[ ]:


df.size


# In[ ]:


keep = ["state","county","percent_non_hispanic_white","percent_hispanic","percent_female","percent_rural","num_deaths"]
df_small = df[keep]


# In[ ]:





# In[ ]:


import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from joblib import dump, load


# In[ ]:


# Read the data
df = df_small.copy()

# Remove rows with missing target
target = "num_deaths"
df.dropna(axis=0, subset=[target], inplace=True)

# Reset index
df.reset_index(drop=True, inplace=True)

# Replace (possible) None types with np.NaN
df.fillna(value=pd.np.nan, inplace=True)

# Separate target from predictors
y = df[target]        
X = df.drop([target], axis=1)

# Break off validation set from training data
X_train_full, X_test_full, y_train, y_test = train_test_split(X, y,
                                                                train_size=0.8,
                                                                test_size=0.2,
                                                                random_state=0)

# "Cardinality" means the number of unique values in a column
# Select categorical columns with relatively low cardinality (convenient but arbitrary)
categorical_cols = [str(cname) for cname in X_train_full.columns if X_train_full[cname].dtype == "object"]

# Select numeric columns
numerical_cols = [str(cname) for cname in X_train_full.columns if X_train_full[cname].dtype in ['int64', 'float64']]

print(len(categorical_cols),len(numerical_cols))

# Keep selected columns only
my_cols = categorical_cols + numerical_cols
X_train = X_train_full[my_cols].copy()
X_test = X_test_full[my_cols].copy()

# Preprocessing for numerical data
numerical_transformer = SimpleImputer(strategy='constant')

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Define model
model = RandomForestRegressor(n_estimators=100, random_state=0)

# Bundle preprocessing and modeling code in a pipeline
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('model', model)
                     ])

# Preprocessing of training data, fit model 
clf.fit(X_train, y_train)


# In[ ]:


def evaluate(predictions, y_valid):
    errors = abs(predictions - y_valid)
    mape = 100 * np.mean(errors / y_valid)
    accuracy = 100 - mape
    print('Model Performance')
    print('MAE: {}'.format(mean_absolute_error(y_valid, preds)))
    print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))
    
    return accuracy


# In[ ]:


# Preprocessing of validation data, get predictions
preds = clf.predict(X_test)

evaluate(preds, y_test)


# In[ ]:




