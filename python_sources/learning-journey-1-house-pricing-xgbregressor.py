#!/usr/bin/env python
# coding: utf-8

# **About Me**
# I publish kaggle notebooks to outline my learning journey in Data Science. This is the very first notebook that I have pusblished, and it contains the step-by-step approach I have adopted to solve the "House Prices" problem.
# 
# I am fairly new to Data Science and Kaggle Challenges, and have depended heavily on the guides made public by other Kagglers. Namely I have adopted much of my data exploration techniques from both Pedro Marcelino's guide (https://www.kaggle.com/pmarcelino/comprehensive-data-exploration-with-python) as well as Serigne's guide (https://www.kaggle.com/serigne/stacked-regressions-top-4-on-leaderboard). However I have also processed data using my own understanding, and at certain points have chosen to make different decisions from the two guides published above.
# 
# **Disclaimers**
# As this is my first time  publishing a notebook on Kaggle, I hope you find the guide helpful in some ways. If you find any areas for improvement, please feel free to suggest new approaches I may adopt. I welcome all feedbacks. 
# 
# **Content Outline**
# My approach can be largely categorised into 4 major steps:
# STEP 1: IMPORTING LIBRARIES AND DATASET
# STEP 2: EXPLORATORY DATA ANALYSIS ON TRAINING SET
# STEP 3: DATA PRE-PROCESSING AND FEATURE ENGINEERING ON COMBINED DATASET
# STEP 4: XGBOOST MODELING WITH PARAMETER TUNING
# 
# Let's dive in!

# **#STEP 1: IMPORTING LIBRARIES AND DATASET**
# 
# I believe this step begins like all other kaggle submission, importing the relevant libraries for data science challenges, and of course importing of train and test data set. It is also at this point I have chosen to assign the target variable 'SalePrice' to a variable 'outcome'. This is because I wanted to build a set of codes/templates that can easily be reused for other challenges. 

# In[ ]:


#STEP 1: IMPORTING LIBRARIES AND DATASET

# Importing the libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm, skew
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold, cross_val_score, train_test_split, cross_validate, GridSearchCV
import xgboost as xgb
from xgboost.sklearn import XGBClassifier, XGBRegressor
from sklearn import metrics
from sklearn.metrics import mean_absolute_error

# Importing the dataset from Kaggle
traindf = pd.read_csv('../input/house-prices-advanced-regression-techniques/train.csv')
testdf = pd.read_csv('../input/house-prices-advanced-regression-techniques/test.csv')

outcome = 'SalePrice' # Within quotes


# **#STEP 2: EXPLORATORY DATA ANALYSIS ON TRAIN DATASET**
# 
# Personally, I find that it is important to understand the problem that we're trying to solve right from the start. In this particular problem, we are to predict an independent variable 'SalePrice' based on a long list of dependent variables. The first step for me, would then be to understand more about the 'SalePrice' variable - We're interested in what's the count of data and how are they distributed?

# In[ ]:


traindf[outcome].describe()


# In[ ]:


# Plotting the curve to understand data distribution
sns.distplot(traindf[outcome], fit=norm);
fig = plt.figure()
res = stats.probplot(traindf[outcome], plot=plt)


# So based on initial analysis, we can see a total count of 1460 data count in the labelled train set, centred around the mean of ~180,921. However we will not say that the data is normally distributed, and have demonstrated postive skewness. The probability plot is a technique picked up from Pedro Marcelino's guide - normally distributed data should be following the diagonal line closely.
# 
# So next step would be to resolve the skewness and normalise our target variable. This is important as most machine learning techniques are either built on, or simply works better with normally distributed data. A simple technique would be to apply log transformation to resolve the skewness.

# In[ ]:


# Applying log transformation to resolve skewness
traindf[outcome] = np.log(traindf[outcome])
sns.distplot(traindf[outcome], fit=norm);
fig = plt.figure()
res = stats.probplot(traindf[outcome], plot=plt)


# There! Now that we have a normally distributed target variable, the next step would be to explore the remaining variables. Let's begin with numerical features.
# 
# As our dataset has a plethora of independent variable, feature selection is more critical than feature engineering in this particular problem. Thankfully, we can use seaborn to plot a correlation matrix. Seaborn not only helps us to identify 2 important things:
# 1. Correlation between numerical features and our target variable
# 2. Correlation between numerical features and other key features
# 
# You can choose to plot the entire features map, but personally I find it overwhelming (see below). 

# In[ ]:


#correlation matrix for all numerical features
cor = traindf.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(cor, vmax=.8, square=True, cmap="YlGnBu");


# So let's plot a second seaborn map, but this time we'll only focus on the top 10 correlated numerical features.

# In[ ]:


# top 10 correlated numerical features
k = 10 #number of variables for heatmap
cols = cor.nlargest(k, outcome)[outcome].index
cm = np.corrcoef(traindf[cols].values.T)
sns.set(font_scale=1.25)
f, ax = plt.subplots(figsize=(12, 9))
hm = sns.heatmap(cm, vmax=.8, cbar=True, cmap="YlGnBu", annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
plt.show()


# Much better! And we can see from the get-go that 'GarageCars' and 'GarageArea' is strongly correlated. And intuitively, that should not come as a surprise. They're basically measuring the same thing, just in different units (number of cars vs number of squarefeet). Now that we have narrowed down on the critical features to focus on. The next step would be to catch outliers that may not be representative of the data.
# 
# As these are the most strongly correlated features, any outliers should show up immediately through a scatterplot of just our top 5 features. I have skipped 'GarageArea', as we have concluded that it should not present us with any new information that 'GarageCars' isn't. 

# In[ ]:


# Identifying outliers through scatterplot
sns.set()
cols = ['SalePrice', 'OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF']
sns.pairplot(traindf[cols], height = 2.5)
plt.show();


# Beautiful. At first it might be overwhelming, but that's precisely why we chose top 5 features instead of all 10 features for this step. That would be confusing and frankly unnecessary. From these scatterplots, we can already identify some data points that are clearly outliers. So let's weed them out, we can do so by zooming into SalePrice/GrLivArea to identify the specific index of two outlier points. Then we'll re-do the scatterplot again to verify.

# In[ ]:


#deleting outliers points by index --> GrLivArea
var = 'GrLivArea'
temp = pd.concat([traindf[var], traindf[outcome]], axis=1)
temp.plot.scatter(x=var, y=outcome)
temp.sort_values(by = var, ascending = True)
traindf = traindf.drop(traindf[traindf[var] == 4676].index, axis=0)
traindf = traindf.drop(traindf[traindf[var] == 5642].index, axis=0)


# Identifying outliers through scatterplot
sns.set()
cols = ['SalePrice', 'OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF']
sns.pairplot(traindf[cols], height = 2.5)
plt.show();


# Some may argure that the SalePrice/GrLivArea plot shows 2 more outlier points. I have decided to keep them even though they may be further from other points, but they seem to still be following the same trend.
# 
# Okay! So far we have normalised the target variable, identified key numerical features and weeded out outlier points. I think we're done with data exploration with the training set, so let's move on!
# 
# 
# **#STEP 3: DATA PRE-PROCESSING AND FEATURE ENGINEERING ON COMBINED DATASET**
# 
# Firstly, we'll combine the train and dataset, so that any data transformation will be applied to all data uniformly. Once done, we'll need to find out what exactly are the missing data we need to handle.

# In[ ]:


#STEP 3: DATA PRE-PROCESSING AND FEATURE ENGINEERING ON COMBINED DATASET
#finding number of missing data
df = pd.concat([traindf, testdf], axis=0, sort=False).reset_index(drop=True) #combining the datasets
total = df.isnull().sum().sort_values(ascending=False)
percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(50)


# There are multiple methods to handle missing data:
# * Fill missing data with or 0 (Common for Numerical Features)
# * Fill missing data with 'None' (Common for Categorical Features)
# * Fill missing data with Mean (Common for Numerical Features)
# * Fill missing data with Mode (Common for Categorical Features)
# * Drop the Column (Common for features with large percentage of missing data)
# * Drop the Row (Common for rare occurances among data)
# * Replace with any other value you deem logical
# 
# In our case, many of the "missing data" actually meant that the house does not have that particular feature (e.g. absence of pool results in empty field for 'PoolQC' etc).
# 

# In[ ]:


#Systematic approach to missing data in each feature

#Columns to fill with 'None'
cols_to_fill = ['PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu', 'GarageQual', 'GarageFinish', 'GarageCond', 'GarageType', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'MasVnrType']
for col in cols_to_fill:
    df[col] = df[col].fillna('None')

#Columns to fill with 0
cols_to_fill = ['GarageYrBlt', 'GarageArea', 'GarageCars', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF','TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath', 'MasVnrArea']
for col in cols_to_fill:
    df[col] = df[col].fillna(0)

#Columns to fill with mean
cols_to_fill = []
for col in cols_to_fill:
    df[col] = df[col].fillna(df[col].mean()[0])
    
#Columns to fill with mode
cols_to_fill = ['MSZoning', 'Electrical', 'KitchenQual', 'Exterior1st', 'Exterior2nd','SaleType']
for col in cols_to_fill:
    df[col] = df[col].fillna(df[col].mode()[0])

#Miscelleneous replacements
df['Functional'] = df['Functional'].fillna('Typ')

#Columns to drop
cols_to_drop = ['LotFrontage', 'Utilities', '1stFlrSF', 'GarageArea', 'GarageYrBlt']
for col in cols_to_drop:
    df = df.drop([col], axis=1)

#Check for missing data again
total = df.isnull().sum().sort_values(ascending=False)
percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(50)


# Now that all missing data have been handled, we'll take a look at the distribution pattern for some of our critical features. As mentioned at the beginning of this journal, most machine learning techniques work better with normalised data. I'll be using the same technique to identify and correct for skewness for 'GrLivArea' and 'TotalBsmtSF' features.
# 
# The technique for normalising 'TotalBsmtSF' can be found in Pedro's notebook. An extra step is needed as data consist of several '0' values that cannot be logarithmized. However, unlike Pedro, I have decided to drop the additional 'HasBsmt' column after normalisation. 

# In[ ]:


# Analysing and normalising target variable
var = 'GrLivArea'
sns.distplot(df[var], fit=norm);
fig = plt.figure()
res = stats.probplot(df[var], plot=plt)

# Applying log transformation to resolve skewness
df[var] = np.log(df[var])
sns.distplot(df[var], fit=norm);
fig = plt.figure()
res = stats.probplot(df[var], plot=plt)

# Analysing and normalising target variable
var = 'TotalBsmtSF'
sns.distplot(df[var], fit=norm);
fig = plt.figure()
res = stats.probplot(df[var], plot=plt)

# Creating a new variable column for 'HasBsmt'
df['HasBsmt'] = 0
df.loc[df['TotalBsmtSF']>0, 'HasBsmt'] = 1

# Applying log transformation to resolve skewness
df.loc[df['HasBsmt'] == 1, 'TotalBsmtSF'] = np.log(df['TotalBsmtSF'])
sns.distplot(df[df[var]>0][var], fit=norm);
fig = plt.figure()
res = stats.probplot(df[df[var]>0][var], plot=plt)
df = df.drop(['HasBsmt'],axis=1)


# In the final step of data pre-processing, we need to ensure that all features are holding numerical values, so that we can run them through the XGBRegressor model. We need tho do the following:
# * Recast any numerical features that are actually categorical
# * Conduct Label Encoding for ordinal features
# * Conduct OneHotEncoder for remaining categorical features

# In[ ]:


#recasting numerical data that are actually categorical
cols_to_cast = ['MSSubClass']
for col in cols_to_cast:
    df[col] = df[col].astype(str)

#Label encoding for ordinal values
cols_to_label = ['FireplaceQu', 'BsmtQual', 'BsmtCond', 'GarageQual', 'GarageCond', 
        'ExterQual', 'ExterCond','HeatingQC', 'PoolQC', 'KitchenQual', 'BsmtFinType1', 
        'BsmtFinType2', 'Functional', 'Fence', 'BsmtExposure', 'GarageFinish', 'LandSlope',
        'LotShape', 'PavedDrive', 'Street', 'Alley', 'CentralAir', 'OverallCond', 
        'YrSold', 'MoSold']

for col in cols_to_label:
    lbl = LabelEncoder()
    lbl.fit(list(df[col].values))
    df[col] = lbl.transform(list(df[col].values))

#OneHotEncoder/get_dummies for remaining categorical features
df = pd.get_dummies(df)


# And now, finally, our data is cleaned up and ready for modelling. That brings us to the next step.
# 
# **#STEP 4: XGBOOST MODELING WITH PARAMETER TUNING**
# 
# For this journal, I have chosen a single model of XGBRegressor. The approach I have adopted for parameter-tuning can be found here: https://blog.cambridgespark.com/hyperparameter-tuning-in-xgboost-4ff9100a3b2f
# 
# I have gone with the common 'Mean Absolute Error' as the measuring metric, and will be applying a 5-fold cross-validation technique for training. Before we begin, we'll do a train_test_split, and load them into DMatrix (data format required for XGB models).

# In[ ]:


#STEP 4: XGBOOST MODELING WITH PARAMETER TUNING

#Creating train_test_split for cross validation
X = df.loc[df[outcome]>0]
X = X.drop([outcome], axis=1)
y = df[[outcome]]
y = y.drop(y.loc[y[outcome].isnull()].index, axis=0)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.2, random_state=8)

#Creating DMatrices for XGBoost
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)


# Next we'll set the initial parameters for the model. I have followed the logics laid out in this guide for the setting of original parameters: https://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/
# 
# And with the initial parameters, we'll determine the ideal 'num_boost_round' and set a baseline MAE to beat. This way, we'll know whether the parameters we're tuning will indeed be resulting in a lower MAE.

# In[ ]:


#Setting initial parameters
params = {
    # Parameters that we are going to tune.
    'max_depth':5,
    'min_child_weight': 1,
    'eta':0.3,
    'subsample': 0.80,
    'colsample_bytree': 0.80,
    'reg_alpha': 0,
    'reg_lambda': 0,
    # Other parameters
    'objective':'reg:squarederror',
}


#Setting evaluation metrics - MAE from sklearn.metrics
params['eval_metric'] = "mae"

num_boost_round = 5000

#Begin training of XGB model
model = xgb.train(
    params,
    dtrain,
    num_boost_round=num_boost_round,
    evals=[(dtest, "Test")],
    early_stopping_rounds=50
)

print("Best MAE: {:.2f} with {} rounds".format(
                 model.best_score,
                 model.best_iteration+1))

#replace num_boost_round with best iteration + 1
num_boost_round = model.best_iteration+1

#Establishing baseline MAE
cv_results = xgb.cv(
    params,
    dtrain,
    num_boost_round=num_boost_round,
    seed=8,
    nfold=5,
    metrics={'mae'},
    early_stopping_rounds=50
)
cv_results
cv_results['test-mae-mean'].min()


# We can see that the baseline MAE to beat is ~0.1004. And initial num_boost_round will be set as 29. From here on, we will begin parameter-tuning in 3 phases:
# * Tuning max_depth & min_child_weight (Tree-specific parameter)
# * Tuning subsample & colsample (Tree-specific parameter)
# * Tuning reg_alpha & reg_lambda (Regularisation parameter)
# * Tuning eta (Learning Rate)
# 
# By using gridsearch technique, we can narrow down on various values we want to test for each phase. Once the ideal value is determined, we need to update the parameters and recalibrate num_boost_round.

# In[ ]:


#Parameter-tuning for max_depth & min_child_weight (First round)
gridsearch_params = [
    (max_depth, min_child_weight)
    for max_depth in range(0,12,2)
    for min_child_weight in range(0,12,2)
]

min_mae = float("Inf")
best_params = None
for max_depth, min_child_weight in gridsearch_params:
    print("CV with max_depth={}, min_child_weight={}".format(
                             max_depth,
                             min_child_weight))
    # Update our parameters
    params['max_depth'] = max_depth
    params['min_child_weight'] = min_child_weight
    # Run CV
    cv_results = xgb.cv(
        params,
        dtrain,
        num_boost_round=num_boost_round,
        seed=8,
        nfold=5,
        metrics={'mae'},
        early_stopping_rounds=50
    )
    # Update best MAE
    mean_mae = cv_results['test-mae-mean'].min()
    boost_rounds = cv_results['test-mae-mean'].idxmin()
    print("\tMAE {} for {} rounds".format(mean_mae, boost_rounds))
    if mean_mae < min_mae:
        min_mae = mean_mae
        best_params = (max_depth,min_child_weight)
print("Best params: {}, {}, MAE: {}".format(best_params[0], best_params[1], min_mae))


#Parameter-tuning for max_depth & min_child_weight (Second round)
gridsearch_params = [
    (max_depth, min_child_weight)
    for max_depth in [3,4,5]
    for min_child_weight in [3,4,5]
]

min_mae = float("Inf")
best_params = None
for max_depth, min_child_weight in gridsearch_params:
    print("CV with max_depth={}, min_child_weight={}".format(
                             max_depth,
                             min_child_weight))
    # Update our parameters
    params['max_depth'] = max_depth
    params['min_child_weight'] = min_child_weight
    # Run CV
    cv_results = xgb.cv(
        params,
        dtrain,
        num_boost_round=num_boost_round,
        seed=8,
        nfold=5,
        metrics={'mae'},
        early_stopping_rounds=50
    )
    # Update best MAE
    mean_mae = cv_results['test-mae-mean'].min()
    boost_rounds = cv_results['test-mae-mean'].idxmin()
    print("\tMAE {} for {} rounds".format(mean_mae, boost_rounds))
    if mean_mae < min_mae:
        min_mae = mean_mae
        best_params = (max_depth,min_child_weight)
print("Best params: {}, {}, MAE: {}".format(best_params[0], best_params[1], min_mae))


#Parameter-tuning for max_depth & min_child_weight (Third round)
gridsearch_params = [
    (max_depth, min_child_weight)
    for max_depth in [3]
    for min_child_weight in [i/10. for i in range(30,50,2)]
]

min_mae = float("Inf")
best_params = None
for max_depth, min_child_weight in gridsearch_params:
    print("CV with max_depth={}, min_child_weight={}".format(
                             max_depth,
                             min_child_weight))
    # Update our parameters
    params['max_depth'] = max_depth
    params['min_child_weight'] = min_child_weight
    # Run CV
    cv_results = xgb.cv(
        params,
        dtrain,
        num_boost_round=num_boost_round,
        seed=8,
        nfold=5,
        metrics={'mae'},
        early_stopping_rounds=50
    )
    # Update best MAE
    mean_mae = cv_results['test-mae-mean'].min()
    boost_rounds = cv_results['test-mae-mean'].idxmin()
    print("\tMAE {} for {} rounds".format(mean_mae, boost_rounds))
    if mean_mae < min_mae:
        min_mae = mean_mae
        best_params = (max_depth,min_child_weight)
print("Best params: {}, {}, MAE: {}".format(best_params[0], best_params[1], min_mae))


# In[ ]:


#Updating max_depth and mind_child_weight parameters
params['max_depth'] = 3
params['min_child_weight'] = 3.2


# In[ ]:


#Recalibrating num_boost_round after parameter updates
num_boost_round = 5000

model = xgb.train(
    params,
    dtrain,
    num_boost_round=num_boost_round,
    evals=[(dtest, "Test")],
    early_stopping_rounds=50
)

print("Best MAE: {:.2f} with {} rounds".format(
                 model.best_score,
                 model.best_iteration+1))

#replace num_boost_round with best iteration + 1
num_boost_round = model.best_iteration+1


# In[ ]:


#Parameter-tuning for subsample & colsample (First round)
gridsearch_params = [
    (subsample, colsample)
    for subsample in [i/10. for i in range(3,11)]
    for colsample in [i/10. for i in range(3,11)]
]

min_mae = float("Inf")
best_params = None
# We start by the largest values and go down to the smallest
for subsample, colsample in reversed(gridsearch_params):
    print("CV with subsample={}, colsample={}".format(
                             subsample,
                             colsample))
    # We update our parameters
    params['subsample'] = subsample
    params['colsample_bytree'] = colsample
    # Run CV
    cv_results = xgb.cv(
        params,
        dtrain,
        num_boost_round=num_boost_round,
        seed=8,
        nfold=5,
        metrics={'mae'},
        early_stopping_rounds=50
    )
    # Update best score
    mean_mae = cv_results['test-mae-mean'].min()
    boost_rounds = cv_results['test-mae-mean'].idxmin()
    print("\tMAE {} for {} rounds".format(mean_mae, boost_rounds))
    if mean_mae < min_mae:
        min_mae = mean_mae
        best_params = (subsample,colsample)
print("Best params: {}, {}, MAE: {}".format(best_params[0], best_params[1], min_mae))

#Parameter-tuning for subsample & colsample (Second round)
gridsearch_params = [
    (subsample, colsample)
    for subsample in [i/100. for i in range(80,100)]
    for colsample in [i/100. for i in range(70,90)]
]

min_mae = float("Inf")
best_params = None
# We start by the largest values and go down to the smallest
for subsample, colsample in reversed(gridsearch_params):
    print("CV with subsample={}, colsample={}".format(
                             subsample,
                             colsample))
    # We update our parameters
    params['subsample'] = subsample
    params['colsample_bytree'] = colsample
    # Run CV
    cv_results = xgb.cv(
        params,
        dtrain,
        num_boost_round=num_boost_round,
        seed=8,
        nfold=5,
        metrics={'mae'},
        early_stopping_rounds=50
    )
    # Update best score
    mean_mae = cv_results['test-mae-mean'].min()
    boost_rounds = cv_results['test-mae-mean'].idxmin()
    print("\tMAE {} for {} rounds".format(mean_mae, boost_rounds))
    if mean_mae < min_mae:
        min_mae = mean_mae
        best_params = (subsample,colsample)
print("Best params: {}, {}, MAE: {}".format(best_params[0], best_params[1], min_mae))


# In[ ]:


#Updating subsample and colsample parameters
params['subsample'] = 0.84
params['colsample'] = 0.71


# In[ ]:


#Recalibrating num_boost_round after parameter updates
num_boost_round = 5000

model = xgb.train(
    params,
    dtrain,
    num_boost_round=num_boost_round,
    evals=[(dtest, "Test")],
    early_stopping_rounds=50
)

print("Best MAE: {:.2f} with {} rounds".format(
                 model.best_score,
                 model.best_iteration+1))

#replace num_boost_round with best iteration + 1
num_boost_round = model.best_iteration+1


# In[ ]:


#Parameter-tuning for reg_alpha & reg_lambda
gridsearch_params = [
    (reg_alpha, reg_lambda)
    for reg_alpha in [1e-5, 1e-4, 1e-3, 1e-2, 0.1]
    for reg_lambda in [1e-5, 1e-4, 1e-3, 1e-2, 0.1]
]

min_mae = float("Inf")
best_params = None

for reg_alpha, reg_lambda in gridsearch_params:
    print("CV with reg_alpha={}, reg_lambda={}".format(
                             reg_alpha,
                             reg_lambda))
    # We update our parameters
    params['reg_alpha'] = reg_alpha
    params['reg_lambda'] = reg_lambda
    # Run CV
    cv_results = xgb.cv(
        params,
        dtrain,
        num_boost_round=num_boost_round,
        seed=8,
        nfold=5,
        metrics={'mae'},
        early_stopping_rounds=50
    )
    # Update best score
    mean_mae = cv_results['test-mae-mean'].min()
    boost_rounds = cv_results['test-mae-mean'].idxmin()
    print("\tMAE {} for {} rounds".format(mean_mae, boost_rounds))
    if mean_mae < min_mae:
        min_mae = mean_mae
        best_params = (reg_alpha,reg_lambda)
print("Best params: {}, {}, MAE: {}".format(best_params[0], best_params[1], min_mae))


# In[ ]:


#Updating reg_alpha and reg_lambda parameters
params['reg_alpha'] = 1e-05
params['reg_lambda'] = 0.001


# In[ ]:


#Resetting num_boost_round to 5000
num_boost_round = 5000

#Parameter-tuning for eta
min_mae = float("Inf")
best_params = None
for eta in [0.3, 0.2, 0.1, 0.05, 0.01, 0.005]:
    print("CV with eta={}".format(eta))

    params['eta'] = eta
    cv_results = xgb.cv(
            params,
            dtrain,
            num_boost_round=num_boost_round,
            seed=8,
            nfold=5,
            metrics=['mae'],
            early_stopping_rounds=50
          )
    # Update best score
    mean_mae = cv_results['test-mae-mean'].min()
    boost_rounds = cv_results['test-mae-mean'].idxmin()
    print("\tMAE {} for {} rounds\n".format(mean_mae, boost_rounds))
    if mean_mae < min_mae:
        min_mae = mean_mae
        best_params = eta
print("Best params: {}, MAE: {}".format(best_params, min_mae))


# In[ ]:


params['eta'] = 0.005


# Now that all ideal parameters are found, let us recap:
# 
# params = {
#     'max_depth':3,
#     'min_child_weight': 3.2,
#     'eta':0.005,
#     'subsample': 0.84,
#     'colsample_bytree': 0.71,
#     'reg_alpha': 1e-05,
#     'reg_lambda': 0.001,
# }
# 

# 

# In[ ]:


model = xgb.train(
    params,
    dtrain,
    num_boost_round=5000,
    evals=[(dtest, "Test")],
    early_stopping_rounds=50
)

num_boost_round = model.best_iteration + 1
best_model = xgb.train(
    params,
    dtrain,
    num_boost_round=num_boost_round,
    evals=[(dtest, "Test")]
)

mean_absolute_error(best_model.predict(dtest), y_test)


# And with this model, we'll now fit the actual test data to the model. Don't forget to reverse the logarhithm we applied on 'SalePrice' during normalisation.

# In[ ]:


testdf = df.loc[df[outcome].isnull()]
testdf = testdf.drop([outcome],axis=1)
sub = pd.DataFrame()
sub['Id'] = testdf['Id']
testdf = xgb.DMatrix(testdf)

y_pred = np.expm1(best_model.predict(testdf))
sub['SalePrice'] = y_pred

sub.to_csv('submission.csv', index=False)


# And.... done! I welcome all feedbacks, please feel free to point out any areas I can do better.
# Thank you!
