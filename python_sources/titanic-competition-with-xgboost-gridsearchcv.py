#!/usr/bin/env python
# coding: utf-8

# # Competition Description
# The sinking of the RMS Titanic is one of the most infamous shipwrecks in history.  On April 15, 1912, during her maiden voyage, the Titanic sank after colliding with an iceberg, killing 1502 out of 2224 passengers and crew. This sensational tragedy shocked the international community and led to better safety regulations for ships.
# 
# One of the reasons that the shipwreck led to such loss of life was that there were not enough lifeboats for the passengers and crew. Although there was some element of luck involved in surviving the sinking, some groups of people were more likely to survive than others, such as women, children, and the upper-class.
# 
# In this challenge, we ask you to complete the analysis of what sorts of people were likely to survive. In particular, we ask you to apply the tools of machine learning to predict which passengers survived the tragedy.
# 
# ## Practice Skills
# + Binary classification
# + Python and R basics

# In[61]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# ## Import and Explore Data

# Our approach is to concatenate train and test data for processing, then separate them later for modelling.

# In[62]:


import pandas as pd
from sklearn.model_selection import train_test_split

# Read the data
orig_X = pd.read_csv('../input/train.csv')
orig_X['Label'] = 'train'

orig_X_test = pd.read_csv('../input/test.csv')
orig_X_test['Label'] = 'test'

# Process as full dataset
orig_X.dropna(axis=0, subset=['Survived'], inplace=True) # Drop rows with uknown survival
X_full = pd.concat([orig_X.drop('Survived', axis = 1), orig_X_test], axis = 0)
X_full.drop('PassengerId', axis = 1, inplace=True)

# Select categorical columns
print("Categorical features: ", [cname for cname in X_full.columns if X_full[cname].dtype == "object"])

# Select numeric columns
print("Numeric features: ", [cname for cname in X_full.columns if X_full[cname].dtype in ['int64', 'float64']])

X_full.head()


# Examining the column names, we will keep all but two: name and ticket number. These are additional unique identifiers to PassengerId.

# In[63]:


# Determine the number of missing values in each column of training data
missing_val_count_by_column = (X_full.isnull().sum())
print(missing_val_count_by_column[missing_val_count_by_column > 0])


# It appears we are missing values from four columns. Two of them are categorical, two of them are numeric.

# ## Process the Data
# Here we will impute missing values in these columns and transform relevant categorical data through one-hot encoding.

# In[64]:


X_full.dtypes


# In[65]:


from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Remove unuseful features
X_full.drop('Name', axis=1, inplace=True)
X_full.drop('Ticket', axis=1, inplace=True)
X_full.drop('Cabin', axis=1, inplace=True)

# Setup method for missing data using a median imputer for important numeric features
num_simple_imputer = SimpleImputer(strategy='median')
numeric_features = ['Age', 'Fare', 'Pclass', 'SibSp', 'Parch']
num_transformed = pd.DataFrame(num_simple_imputer.fit_transform(X_full[numeric_features]))
num_transformed.columns = numeric_features

# Setup one hot enoding for catagorical features
cat_simple_imputer = SimpleImputer(strategy='constant', fill_value='missing')
categorical_features = ['Embarked','Sex', 'Label']
cat_transformed = pd.DataFrame(cat_simple_imputer.fit_transform(X_full[categorical_features]))
cat_transformed.columns = categorical_features
X_dummies = pd.get_dummies(cat_transformed, columns = categorical_features)
X_full = pd.concat([num_transformed, X_dummies], axis = 1)

print(X_full.dtypes)
print(X_full.head())


# ## Examine Attribute Correlations

# In[66]:


import seaborn as sns
corr = X_full.corr()
sns.heatmap(corr, cmap = sns.color_palette("coolwarm", 10))


# In[67]:


# Split your data
X = X_full[X_full['Label_train'] == 1].copy()
X_test = X_full[X_full['Label_test'] == 1].copy()

# Drop your labels
X.drop('Label_train', axis=1, inplace=True)
X.drop('Label_test', axis=1, inplace=True)
X_test.drop('Label_test', axis=1, inplace=True)
X_test.drop('Label_train', axis=1, inplace=True)
y = orig_X.Survived


# In[68]:


# Framework via: https://towardsdatascience.com/feature-selection-correlation-and-p-value-da8921bfb3cf
print("Full column list: ", X.columns)
import statsmodels.formula.api as sm
def backwardElimination(x, Y, sl, columns):
    numVars = len(x[0])
    for i in range(0, numVars):
        regressor_OLS = sm.OLS(Y, x).fit()
        maxVar = max(regressor_OLS.pvalues).astype(float)
        if maxVar > sl:
            for j in range(0, numVars - i):
                if (regressor_OLS.pvalues[j].astype(float) == maxVar):
                    x = np.delete(x, j, 1)
                    columns = np.delete(columns, j)

    regressor_OLS.summary()
    return x, columns

SL = 0.05
data_modeled, selected_columns = backwardElimination(X.values, y.values, SL, X.columns)

# Creating a Dataframe with the columns selected using the p-value and correlation
new_df = pd.DataFrame(data = data_modeled, columns = selected_columns)

print("Columns to remove: ", set(X.columns).symmetric_difference(new_df.columns))


# In[69]:


# Remove columns
X.drop('Fare', axis=1, inplace=True)
X.drop('Parch', axis=1, inplace=True)
X_test.drop('Fare', axis=1, inplace=True)
X_test.drop('Parch', axis=1, inplace=True)

# Break off validation set from training data
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.7, test_size=0.3,
                                                                random_state=0)


# ## Use of GridSearchCV Search to Determine the Best Model Parameters

# In[70]:


# from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV

# Initial model
model = XGBClassifier(random_state = 18)

# Set up GridSearchCV in order to determine the best parameters for a gradient boosting model
grid_param = {  
    'n_estimators': [12, 25, 50, 75],
    'max_depth': [3, 4, 5],
    'learning_rate': [0.01, 0.05, 0.1],
    'early_stopping_rounds': [3, 4, 5, 6]
    }

gd_sr = GridSearchCV(estimator = model, param_grid = grid_param, 
                     cv = 3, n_jobs = -1, verbose = 2)

gd_sr.fit(X_train, y_train)  
best_parameters = gd_sr.best_params_
print(best_parameters)  


# In[71]:


# Create a final model fit to these parameters
xgb = XGBClassifier(early_stopping_rounds = 3, eval_set = [(X_valid, y_valid)], learning_rate = 0.05, 
                    max_depth = 5, n_estimators = 50)

xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_valid)

# Get mean absolute error
print('MAE:', mean_absolute_error(y_valid, y_pred))


# In[72]:


# Form confusion matrix
from sklearn.metrics import confusion_matrix
confusion_matrix(y_valid, y_pred)


# ## Create Submission

# In[73]:


final_preds = xgb.predict(X_test)

# Save test predictions to file
output = pd.DataFrame({'PassengerId': orig_X_test.PassengerId,'Survived': final_preds})
output
output.to_csv('submission.csv', index=False)

