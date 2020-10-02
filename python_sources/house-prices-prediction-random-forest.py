#!/usr/bin/env python
# coding: utf-8

# ## Load Libraries
# 

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os, sys, time
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics

import matplotlib.pyplot as plt
import seaborn as sns 
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Create Helper Functions 

# In[ ]:


def ExamineData(df):
    """Prints various data charteristics, given x, where x is a pandas data frame
    """
    print("Data shape:", df.shape)
    print("\nColumn:", df.columns)
    print("\nData types", df.dtypes)
    print("\nDescribe data", df.describe())
    print("\nData ", df.head(2))
    print ("\nSize of data", sys.getsizeof(df)/1000000, "MB" )    # Get size of dataframes
    print("\nAre there any NULLS", np.sum(df.isnull()))
    
# Fill in missing values
def fillMissingValuesAsOther(df , filler = "other"):
    '''Fills missing values with "other" df is a pandas data frame
    '''
    df.fillna(value = filler, inplace = True)

def fillMissingValuesAsMean(df):
    '''Fills missing values with "data frame mean" df is a pandas data frame
    '''
    df.fillna(df.mean(), inplace = True)

def fillMissingValuesAsZero(df):
    '''Fills missing values with "0" df is a pandas data frame
    '''
    df.fillna(value=0, inplace = True)
    
def ColWithNAs(x):            
    z = x.isnull()
    df = np.sum(z, axis = 0)       # Sum vertically, across rows
    col = df[df > 0].index.values 
    return (col)

def prepareData(df):
    for col in df:
        if np.issubdtype(df[col].dtype, np.number):
            fillMissingValuesAsMean(df[col])
        elif np.sum(df[col].isnull()) > 0:
            fillMissingValuesAsOther(df[col])


# ## Load Data 

# In[ ]:


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')


# ## Examine Train Data 

# In[ ]:


ExamineData(train)


# ## Examine Test Data

# In[ ]:


ExamineData(test)


# ## Cleanup Data 
# 
# just by visually inspecting we can determine that based on the data frame size of 1459 rows some of the columns/features, have more than 1000 ('Alley' , 'PoolQC', 'Fence', 'MiscFeature',  null values, so those columns can be taken out of both train and test data sets. Also the Id column can removed

# In[ ]:


#Train data clean up 
#Get Target column out of train 
y  = train['SalePrice']
train.dropna(thresh=1000, inplace=True, axis='columns')
train.drop('Id', inplace=True, axis='columns')
train.drop('SalePrice', inplace=True, axis='columns')
train.head(1)


# In[ ]:


#Test Data clean up 
test.dropna(thresh=1000, inplace=True, axis='columns')
test.drop('Id', inplace=True, axis='columns')
test.head(1)


# ## Prepare Data 

# In[ ]:





# In[ ]:


prepareData(train)
prepareData(test)
#check that the values were filled with mean where NaN was before f.e LotFrontage col row 7
print('-'*40 + 'TTrain Data' + '-' * 40)
print(train.head(20))
print('-'*40 + 'Test Data' + '-' * 40)
print(test.head(20))


# In[ ]:


#Verify that no NaNs are present on the data set 
np.sum(test.isnull())


# In[ ]:


np.sum(train.isnull())


# ## Visualize Correlation with Heat Map 
# 

# In[ ]:


plt.figure(figsize=(15,10))
sns.heatmap(train.corr())


# In[ ]:


# "cardinality" means the number of unique values in a column.
# We use it as our only way to select categorical columns here. This is convenient, though
# a little arbitrary.
low_cardinality_cols = [cname for cname in train.columns if 
                                train[cname].nunique() < 10 and
                                train[cname].dtype == "object"]
numeric_cols = [cname for cname in train.columns if 
                                train[cname].dtype in ['int64', 'float64']]
my_cols = low_cardinality_cols + numeric_cols
train_predictors = train[my_cols]
test_predictors = test[my_cols]
train_predictors.dtypes.sample(30)


# **Object **indicates a column has text (there are other things it could be theoretically be, but that's unimportant for our purposes). It's most common to one-hot encode these "object" columns, since they can't be plugged directly into most models. Pandas offers a convenient function called get_dummies to get one-hot encodings. Call it like this:

# In[ ]:


train_data_one_hot_encoding = pd.get_dummies(train_predictors)

test_data_one_hot_encoding = pd.get_dummies(test_predictors)

x_train = train_data_one_hot_encoding
y_train = y
X_train, X_test, Y_train, Y_test = train_test_split(
                                     x_train, y_train,
                                     test_size=0.30,
                                     random_state=42
                                     )


# ## Train the RF Model
# 

# In[ ]:


# Instantiate a RandomRegressor object
MAXDEPTH = 60
rf_model = RandomForestRegressor(n_estimators=1200,   # No of trees in forest
                             criterion = "mse",       # Can also be mae
                             max_features = "sqrt",   # no of features to consider for the best split
                             max_depth= MAXDEPTH,     #  maximum depth of the tree
                             min_samples_split= 2,    # minimum number of samples required to split an internal node
                             min_impurity_decrease=0, # Split node if impurity decreases greater than this value.
                             oob_score = True,        # whether to use out-of-bag samples to estimate error on unseen data.
                             n_jobs = -1,             #  No of jobs to run in parallel
                             random_state=0,
                             verbose = 10             # Controls verbosity of process
                             )

rf_model.fit(X_train,Y_train)


# In[ ]:


predictions = rf_model.predict(X_test)


# ## Make a scatter plot of the predictions vs y_test values

# In[ ]:


plt.figure(figsize=(8,6))
plt.scatter(predictions,Y_test,cmap='plasma')
plt.title("Random Forest")


# ## Metrics MAE, MSE, RMSE

# In[ ]:


print('MAE:', metrics.mean_absolute_error(Y_test, predictions))
print('MSE:', metrics.mean_squared_error(Y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(np.log1p(Y_test), np.log1p(predictions))))


# 
