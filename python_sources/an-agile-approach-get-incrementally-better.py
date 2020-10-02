#!/usr/bin/env python
# coding: utf-8

# In this notebook, I want to test a few techniques to get a simple regression model to an acceptable result.
# 
# The main question I want to find an answer to is: **how much can I improve the quality of my results in a given time?**
# 
# In all fairness, one of my problems is that I usually get too curious when I look at the data and find myself in spending a lot of time for nothing. So I thought: let's at least fail very quickly.
# 
# To this end, I decided to structure the kernel as follows:
# 
# * Define a baseline, an extremely simple model to confront my results with.
# * Be a butcher, clean the data in a few minutes and start from there
# * Iterate the process to find what works and what doesn't
# 
# In doing so, I will try to avoid any data leak or other bad practices (the most obvious one is using the information contained in the test set to manipulate the training set). Some of those practices may lead to a better score on the Leaderboard, but in a realistic situation will never be applicable.
# 
# To be fair towards realism, I also have to say that this is not the first time I look at these data and, therefore, my eyes and mind are not fresh as they should be for a faithful experiment. After preparing the material, I am fairly sure that my previous experiments with this dataset are influential only in terms of time saved in deciding what to do with some of the features.
# 
# The key of the entire approach is **embracing the iteration process**. If a problem emerge, get anyway till the end and then come back and solve it during the next iteration. This allows me to be more focused and to more easily keep track of what is helping my model and what isn't.
# 
# In preparing the process, I keep track of the cross-validated scores of each step and use that for decision making. However, since everybody likes to see a score on the leaderboard, I also produced a bunch of output data for each step so that I can trace back the progress on truly unseen data. These public results are not used in any way for decision making because, realistically, I won't have access to those data when I am building the model.
# 
# 
# # Preparation: libraries, data, functions
# 
# Nothing fancy, I want to use Lasso and Ridge regression because they are simple enough to tune and this will save me a lot of time.
# 
# They both work well if the data are scaled, so I will make that happen in a pipeline. If I was not doing so, my cross-validation would not be trustable since the scaling would happen by seeing the entire dataset.
# 
# *In a pipeline you have fewer chances of leakage*.
# 
# To evaluate the model, I use the metric Kaggle suggests, with is the mean squared error and definitely a very appropriate one. In addition, only because it is easier to interpret, I will also have a look at the mean absolute error.
# 
# **NOTE**: I wanted to use ElasticNet as well, but I kept having convergence problems. Any suggestions about why it happens are welcome.

# In[ ]:


# standard
import pandas as pd
import numpy as np

#visualization
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.model_selection import KFold, cross_validate, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from sklearn.model_selection import learning_curve

#machine learning
from sklearn.linear_model import Lasso, Ridge

import warnings
warnings.filterwarnings('ignore')  # sorry for that, really


# In[ ]:


# ---------- DF IMPORT -------------
df_train = pd.read_csv('../input/train.csv')
df_test = pd.read_csv('../input/test.csv')
combine = [df_train, df_test]
df_train.name = 'Train'
df_test.name = 'Test'


# I now create my folds for the cross-validation and define my target variable.

# In[ ]:


kfolds = KFold(n_splits=10, shuffle=True, random_state=14)
target = np.log1p(df_train['SalePrice'])
old_target = df_train['SalePrice']


# In[ ]:


def get_dollars(estimator, kfolds, data, target, old_target):
    scores = []
    train = data.copy()
    for i,(train_index, test_index) in enumerate(kfolds.split(target)):
        training = train.iloc[train_index,:]
        valid = train.iloc[test_index,:]
        tr_label = target.iloc[train_index]
        val_label = target.iloc[test_index]
        estimator.fit(training, tr_label)
        pred = estimator.predict(valid) 
        or_result = old_target.iloc[test_index]
        score = mean_absolute_error(y_pred=np.expm1(pred), y_true=or_result)
        scores.append(score)     
    return round(np.mean(scores),3)


def get_coef(clsf, ftrs):
    imp = clsf.steps[1][1].coef_.tolist() #it's a pipeline
    feats = ftrs
    result = pd.DataFrame({'feat':feats,'score':imp})
    result = result.sort_values(by=['score'],ascending=False)
    return result


# # Baseline
# 
# As a baseline, I simply use a model that takes the median of the price and uses that to predict. The following code allows me to test this idea with cross-validation.

# In[ ]:


scores = []
or_scores = []

for i,(train_index, test_index) in enumerate(kfolds.split(target)):
    df_train['prediction'] = np.nan
    print("Fold {} in progress".format(i))
    base = target.iloc[train_index].median()
    result = target.iloc[test_index]
    or_result = old_target.iloc[test_index]
    df_train['prediction'].iloc[test_index] = base 
    prediction = [p for p in df_train['prediction'].dropna()]
    print("Predicting with median {}".format(round(base,3)))
    score = mean_squared_error(y_pred= prediction, y_true=result)
    or_score = mean_absolute_error(y_pred=np.expm1(prediction), y_true=or_result)
    print("Scoring {}".format(score))
    print("MAE {}$".format(or_score))
    scores.append(score)
    or_scores.append(or_score)
    df_train.drop('prediction', axis=1, inplace=True)
    print("_"*40)
    
print("Baseline: {} +- {}".format(round(np.mean(scores),3), round(np.std(scores),3)))
print('MAE: {} +- {}'.format(round(np.mean(or_scores),3), round(np.std(or_scores),3)))


# This entire process took me 5 minutes, got a score of 0.16 which translates into missing the price of a house by 55000 dollars on average.
# 
# At this stage, my model would predict for every house a price of 163000 dollars, scoring a 0.41899 on Kaggle. Let's keep track of these results.

# In[ ]:


modelname = ['Baseline']
lassoscore = [0.16] #not true, but we need it later
ridgescore = [0.16]
kaggle_lasso = [0.41899]
kaggle_ridge = [0.41899]
timeelapsed = [600]
maecv_lasso = [55646.558]
maecv_ridge = [55646.558]


# # Fast and Butchery
# 
# Just drop everything missing and go with the wind.
# 
# This is what is missing.

# In[ ]:


for df in combine:
    if df.name == 'Train':
        mis_train = []
        cols = df.columns
        for col in cols:
            mis = df[col].isnull().sum()
            if mis > 0:
                print("{}: {} missing, {}%".format(col, mis, round(mis/df.shape[0] * 100, 3)))
                mis_train.append(col)
        print("_"*40)
        print("_"*40)
    if df.name == 'Test':
        mis_test = []
        cols = df.columns
        for col in cols:
            mis = df[col].isnull().sum()
            if mis > 0:
                print("{}: {} missing, {}%".format(col, mis, round(mis/df.shape[0] * 100, 3)))
                mis_test.append(col)

print("\n")
print(mis_train)
print("_"*40)
print(mis_test)


# Quite a lot, I will just drop everything, create dummies because these models require that and obtain the following.

# In[ ]:


butch_train = df_train[[col for col in df_test.columns if col not in mis_test]].dropna(axis=1)
butch_test = df_test[[col for col in df_test.columns if col not in mis_train]].dropna(axis=1)

butch_train.drop("Id", axis=1, inplace=True)
butch_test.drop("Id", axis=1, inplace=True)

butch_train = pd.get_dummies(butch_train)
butch_test = pd.get_dummies(butch_test)

#some of the dummies are not in both datasets (will be cured later)
butch_train = butch_train[[col for col in butch_test.columns]] 

(butch_train.columns != butch_test.columns).sum()


# With both models I need a scaler

# In[ ]:


scl = ('scl', RobustScaler())


# Now I make the pipeline and do some very quick grid search.

# In[ ]:


pipe = Pipeline([scl, ('lasso', Lasso(max_iter=2000))]) # to avoid convergence problems

param_grid = [{'lasso__alpha' : [0.0001, 0.0005, 0.00075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_lasso = grid.best_estimator_
print(best_lasso)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print("_"*40)
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_lasso, kfolds, butch_train, target, old_target)
dol


# Let's see what is getting a larger coefficient.

# In[ ]:


coefs = get_coef(best_lasso, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# Something makes sense, other things I can't explain but let's do the ridge regression and move on

# In[ ]:


pipe = Pipeline([scl, ('ridge', Ridge())])

param_grid = [{'ridge__alpha' : [0.0001, 0.0005, 0.0075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5,
                                10, 15, 17.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_ridge = grid.best_estimator_
print(best_ridge)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_ridge, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_ridge, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# In[ ]:


modelname.append('Butcher')
lassoscore.append(0.1499)
ridgescore.append(0.1488)
kaggle_lasso.append(0.13321)
kaggle_ridge.append(0.13410)
timeelapsed.append(1800)
maecv_lasso.append(18544.430)
maecv_ridge.append(18327.714)


# To sum up, we spent 25 more minutes, got slightly better in cross-validation (a lot better on the leaderboard, and our mean absolute error dropped of about 35000 dollars)
# 
# # Follow the documentation
# 
# If instead of dropping everything we focus on what we know from the documentation, we can use more data and get a more credible model. I talked about the topic already in this other kernel and here is the result.
# 
# First, the documentation talks about 2 outliers to be removed.

# In[ ]:


target = np.log1p(df_train[df_train.GrLivArea < 4500]['SalePrice'])
old_target = df_train[df_train.GrLivArea < 4500]['SalePrice']


# Next, I simply do the following (I also flag the missing entries)

# In[ ]:


for df in combine:
    #LotFrontage
    df.loc[df.LotFrontage.isnull(), 'LotFrontage'] = 0
    #Alley
    df.loc[df.Alley.isnull(), 'Alley'] = "NoAlley"
    #MSSubClass
    df['MSSubClass'] = df['MSSubClass'].astype(str)
    #MissingBasement
    fil = ((df.BsmtQual.isnull()) & (df.BsmtCond.isnull()) & (df.BsmtExposure.isnull()) &
          (df.BsmtFinType1.isnull()) & (df.BsmtFinType2.isnull()))
    fil1 = ((df.BsmtQual.notnull()) | (df.BsmtCond.notnull()) | (df.BsmtExposure.notnull()) |
          (df.BsmtFinType1.notnull()) | (df.BsmtFinType2.notnull()))
    df.loc[fil1, 'MisBsm'] = 0
    df.loc[fil, 'MisBsm'] = 1
    #BsmtQual
    df.loc[fil, 'BsmtQual'] = "NoBsmt" #missing basement
    #BsmtCond
    df.loc[fil, 'BsmtCond'] = "NoBsmt" #missing basement
    #BsmtExposure
    df.loc[fil, 'BsmtExposure'] = "NoBsmt" #missing basement
    #BsmtFinType1
    df.loc[fil, 'BsmtFinType1'] = "NoBsmt" #missing basement
    #BsmtFinType2
    df.loc[fil, 'BsmtFinType2'] = "NoBsmt" #missing basement
    #FireplaceQu
    df.loc[(df.Fireplaces == 0) & (df.FireplaceQu.isnull()), 'FireplaceQu'] = "NoFire" #missing
    #MisGarage
    fil = ((df.GarageYrBlt.isnull()) & (df.GarageType.isnull()) & (df.GarageFinish.isnull()) &
          (df.GarageQual.isnull()) & (df.GarageCond.isnull()))
    fil1 = ((df.GarageYrBlt.notnull()) | (df.GarageType.notnull()) | (df.GarageFinish.notnull()) |
          (df.GarageQual.notnull()) | (df.GarageCond.notnull()))
    df.loc[fil1, 'MisGarage'] = 0
    df.loc[fil, 'MisGarage'] = 1
    #GarageYrBlt
    df.loc[df.GarageYrBlt > 2200, 'GarageYrBlt'] = 2007 #correct mistake
    df.loc[fil, 'GarageYrBlt'] = 0
    #GarageType
    df.loc[fil, 'GarageType'] = "NoGrg" #missing garage
    #GarageFinish
    df.loc[fil, 'GarageFinish'] = "NoGrg" #missing
    #GarageQual
    df.loc[fil, 'GarageQual'] = "NoGrg" #missing
    #GarageCond
    df.loc[fil, 'GarageCond'] = "NoGrg" #missing
    #Fence
    df.loc[df.Fence.isnull(), 'Fence'] = "NoFence" #missing fence
    
df_test[['BsmtUnfSF', 
         'TotalBsmtSF', 
         'BsmtFinSF1', 
         'BsmtFinSF2']] = df_test[['BsmtUnfSF', 
                                   'TotalBsmtSF', 
                                   'BsmtFinSF1', 
                                   'BsmtFinSF2']].fillna(0) #checked


# After this operation, we are left with the following missing entries

# In[ ]:


for df in combine:
    if df.name == 'Train':
        mis_train = []
        cols = df.columns
        for col in cols:
            mis = df[col].isnull().sum()
            if mis > 0:
                print("{}: {} missing, {}%".format(col, mis, round(mis/df.shape[0] * 100, 3)))
                mis_train.append(col)
        print("_"*40)
        print("_"*40)
    if df.name == 'Test':
        mis_test = []
        cols = df.columns
        for col in cols:
            mis = df[col].isnull().sum()
            if mis > 0:
                print("{}: {} missing, {}%".format(col, mis, round(mis/df.shape[0] * 100, 3)))
                mis_test.append(col)

print("\n")
print(mis_train)
print("_"*40)
print(mis_test)


# In other words, we have a few more features to feed our models with. Let's do this iteration before doing anything else.

# In[ ]:


butch_train = df_train[[col for col in df_test.columns if col not in mis_test]].dropna(axis=1)
butch_test = df_test[[col for col in df_test.columns if col not in mis_train]].dropna(axis=1)

butch_train.drop("Id", axis=1, inplace=True)
butch_test.drop("Id", axis=1, inplace=True)

butch_train = pd.get_dummies(butch_train)
butch_test = pd.get_dummies(butch_test)

butch_train = butch_train[[col for col in butch_test.columns if col in butch_train.columns]]
butch_test = butch_test[[col for col in butch_train.columns]]

#because redundant with MisGarage
butch_train = butch_train.drop([col for col in butch_train.columns if 'NoGrg' in col], axis=1) 
butch_test = butch_test.drop([col for col in butch_test.columns if 'NoGrg' in col], axis=1)
#because redundant with MisBsm
butch_train = butch_train.drop([col for col in butch_train.columns if 'NoBsmt' in col], axis=1) 
butch_test = butch_test.drop([col for col in butch_test.columns if 'NoBsmt' in col], axis=1)

butch_train = butch_train[butch_train.GrLivArea < 4500] #according to documentation
df_train = df_train[df_train.GrLivArea < 4500] #for consistency

(butch_train.columns != butch_test.columns).sum()


# In[ ]:


pipe = Pipeline([scl, ('lasso', Lasso(max_iter=2000))])

param_grid = [{'lasso__alpha' : [0.0001, 0.0005, 0.00075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_lasso = grid.best_estimator_
print(best_lasso)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_lasso, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_lasso, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# Both the absolute mean error and the mean squared error are dropping.

# In[ ]:


pipe = Pipeline([scl, ('ridge', Ridge())])

param_grid = [{'ridge__alpha' : [0.0001, 0.0005, 0.0075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5,
                                10, 15, 17.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_ridge = grid.best_estimator_
print(best_ridge)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_ridge, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_ridge, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# In[ ]:


modelname.append('Doc_Impute')
lassoscore.append(0.1186)
ridgescore.append(0.1185)
kaggle_lasso.append(0.11980)
kaggle_ridge.append(0.11974)
timeelapsed.append(9000)
maecv_lasso.append(14411.229)
maecv_ridge.append(14495.809)


# # Full imputation
# 
# With this I mean the following:
# 
# * drop columns that I know are problematic already
# * drop every entry with a missing value in the train dataset, because I don't want to reinforce existing patterns
# * since I can't do the same on the test set or Kaggle will punish me, I impute with mean or medians the missing colums

# In[ ]:


print(df_train.shape, df_test.shape)
df_train.drop("PoolQC", axis=1, inplace=True) #I know these are going to be missing always and I don't care
df_train.drop("MiscFeature", axis=1, inplace=True)
df_test.drop("PoolQC", axis=1, inplace=True)
df_test.drop("MiscFeature", axis=1, inplace=True)
print(df_train.shape, df_test.shape)


# Now I drop the missing values in the training set
# 
# **Note**: if the number of problematic entries was higher, I would test several imputers inside of the pipeline right before the scaler. In this way, I would have a trustable comparison between different models. Imputing outside of the pipeline would use the information of the entire dataset and, thus, would make my cross-validation less trustable.

# In[ ]:


print("Size of train set before my butchering: {}".format(df_train.shape))
for f in df_train.columns:
    df_train = df_train[pd.notnull(df_train[f])]

cols = df_train.columns
print("Start printing the missing values...")
mis_train = []
for col in cols:
    mis = df_train[col].isnull().sum()
    if mis > 0:
        print("{}: {} missing, {}%".format(col, mis, round(mis/df_train.shape[0] * 100, 3)))
        mis_train.append(col)
print("...done printing the missing values")
print(mis_train)
print("Size of train set after my butchering: {}".format(df_train.shape))


# They won't be missed so much after all.
# 
# Next, a few functions to help me for the imputation of the test. The idea is to use mean and median taken not from the entire set but rather from the similar entries.

# In[ ]:


#To find the segment of the missing values, can be useful to impute the missing values
def find_segment(df, feat): 
    mis = df[feat].isnull().sum()
    cols = df.columns
    seg = []
    for col in cols:
        vc = df[df[feat].isnull()][col].value_counts(dropna=False).iloc[0]
        if (vc == mis): #returns the columns for which the missing entries have only 1 possible value
            seg.append(col)
    return seg

# to find the mode of the missing feature, by choosing the right segment to compare (uses find_segment)
def find_mode(df, feat): #returns the mode to fill in the missing feat
    md = df[df[feat].isnull()][find_segment(df, feat)].dropna(axis=1).mode()
    md = pd.merge(df, md, how='inner')[feat].mode().iloc[0]
    return md

# identical to the previous one, but with the median
def find_median(df, feat): #returns the median to fill in the missing feat
    md = df[df[feat].isnull()][find_segment(df, feat)].dropna(axis=1).mode()
    md = pd.merge(df, md, how='inner')[feat].median()
    return md

# find the mode in a segment defined by the user
def similar_mode(df, col, feats): #returns the mode in a segment made by similarity in feats
    sm = df[df[col].isnull()][feats]
    md = pd.merge(df, sm, how='inner')[col].mode().iloc[0]
    return md

# Find the median in a segment defined by the user
def similar_median(df, col, feats): #returns the median in a segment made by similarity in feats
    sm = df[df[col].isnull()][feats]
    md = pd.merge(df, sm, how='inner')[col].median()
    return md


# In[ ]:


#MSZoning
md = find_mode(df_test, 'MSZoning')
print("MSZoning {}".format(md))
df_test[['MSZoning']] = df_test[['MSZoning']].fillna(md)
#Utilities
md = 'AllPub'
df_test[['Utilities']] = df_test[['Utilities']].fillna(md)
#MasVnrType
md = find_mode(df_test, 'MasVnrType')
print("MasVnrType {}".format(md))
df_test[['MasVnrType']] = df_test[['MasVnrType']].fillna(md)
#MasVnrArea
md = find_mode(df_test, 'MasVnrArea')
print("MasVnrArea {}".format(md))
df_test[['MasVnrArea']] = df_test[['MasVnrArea']].fillna(md)
#BsmtQual
simi = ['BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2']
md = similar_mode(df_test, 'BsmtQual', simi)
print("BsmtQual {}".format(md))
df_test[['BsmtQual']] = df_test[['BsmtQual']].fillna(md)
#BsmtCond
simi = ['BsmtQual', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2']
md = similar_mode(df_test, 'BsmtCond', simi)
print("BsmtCond {}".format(md))
df_test[['BsmtCond']] = df_test[['BsmtCond']].fillna(md)
#BsmtCond
simi = ['BsmtQual', 'BsmtCond', 'BsmtFinType1', 'BsmtFinType2']
md = similar_mode(df_test, 'BsmtExposure', simi)
print("BsmtExposure {}".format(md))
df_test[['BsmtExposure']] = df_test[['BsmtExposure']].fillna(md)
#BsmtFullBath
simi = ['BsmtQual', 'BsmtCond', 'BsmtFinType1', 'BsmtFinType2']
md = similar_median(df_test, 'BsmtFullBath', simi)
print("BsmtFullBath {}".format(md))
df_test[['BsmtFullBath']] = df_test[['BsmtFullBath']].fillna(md)
#BsmtHalfBath
simi = ['BsmtQual', 'BsmtCond', 'BsmtFinType1', 'BsmtFinType2']
md = similar_median(df_test, 'BsmtHalfBath', simi)
print("BsmtHalfBath {}".format(md))
df_test[['BsmtHalfBath']] = df_test[['BsmtHalfBath']].fillna(md)
#KitchenQual
md = df_test.KitchenQual.mode().iloc[0]
print("KitchenQual {}".format(md))
df_test[['KitchenQual']] = df_test[['KitchenQual']].fillna(md)
#Functional
md = 'Typ'
df_test[['Functional']] = df_test[['Functional']].fillna(md)
#GarageYrBlt
simi = ['GarageType', 'MisGarage']
md = similar_median(df_test, 'GarageYrBlt', simi)
print("GarageYrBlt {}".format(md))
df_test[['GarageYrBlt']] = df_test[['GarageYrBlt']].fillna(md)
#GarageFinish
md = 'Unf'
print("GarageFinish {}".format(md))
df_test[['GarageFinish']] = df_test[['GarageFinish']].fillna(md)
#GarageArea
simi = ['GarageType', 'MisGarage']
md = similar_median(df_test, 'GarageArea', simi)
print("GarageArea {}".format(md))
df_test[['GarageArea']] = df_test[['GarageArea']].fillna(md)
#GarageQual
simi = ['GarageType', 'MisGarage', 'GarageFinish']
md = similar_mode(df_test, 'GarageQual', simi)
print("GarageQual {}".format(md))
df_test[['GarageQual']] = df_test[['GarageQual']].fillna(md)
#GarageCond
simi = ['GarageType', 'MisGarage', 'GarageFinish']
md = similar_mode(df_test, 'GarageCond', simi)
print("GarageCond {}".format(md))
df_test[['GarageCond']] = df_test[['GarageCond']].fillna(md)
#GarageCars
simi = ['GarageType', 'MisGarage']
md = similar_median(df_test, 'GarageCars', simi)
print("GarageCars {}".format(md))
df_test[['GarageCars']] = df_test[['GarageCars']].fillna(md)

cols = df_test.columns
mis_test = []
print("Start printing the missing values...")
for col in cols:
    mis = df_test[col].isnull().sum()
    if mis > 0:
        print("{}: {} missing, {}%".format(col, mis, round(mis/df_test.shape[0] * 100, 3)))
        mis_test.append(col)
print("...done printing the missing values")


# Not much left, I don't want to think about it anymore. Let's run this new iteration.

# In[ ]:


butch_train = df_train[[col for col in df_test.columns if col not in mis_test]].dropna(axis=1)
butch_test = df_test[[col for col in df_test.columns if col not in mis_train]].dropna(axis=1)

butch_train.drop("Id", axis=1, inplace=True)
butch_test.drop("Id", axis=1, inplace=True)

butch_train = pd.get_dummies(butch_train)
butch_test = pd.get_dummies(butch_test)

print(list(set(butch_train.columns) - set(butch_test.columns)))

butch_train = butch_train[[col for col in butch_test.columns if col in butch_train.columns]]
butch_test = butch_test[[col for col in butch_train.columns]]

#because redundant with MisGarage
butch_train = butch_train.drop([col for col in butch_train.columns if 'NoGrg' in col], axis=1) 
butch_test = butch_test.drop([col for col in butch_test.columns if 'NoGrg' in col], axis=1)
#because redundant with MisBsm
butch_train = butch_train.drop([col for col in butch_train.columns if 'NoBsmt' in col], axis=1) 
butch_test = butch_test.drop([col for col in butch_test.columns if 'NoBsmt' in col], axis=1)

butch_train = butch_train[butch_train.GrLivArea < 4500] #according to documentation
target = np.log1p(df_train[df_train.GrLivArea < 4500]['SalePrice']) #for consistency
old_target = df_train[df_train.GrLivArea < 4500]['SalePrice']

(butch_train.columns != butch_test.columns).sum()


# Quite a few dummies are not in both datasets, I will deal with that later.

# In[ ]:


butch_train.shape


# In[ ]:


pipe = Pipeline([scl, ('lasso', Lasso(max_iter=2000))])

param_grid = [{'lasso__alpha' : [0.0001, 0.0005, 0.00075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_lasso = grid.best_estimator_
print(best_lasso)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_lasso, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_lasso, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# In[ ]:


pipe = Pipeline([scl, ('ridge', Ridge())])

param_grid = [{'ridge__alpha' : [0.0001, 0.0005, 0.00075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5,
                                10, 15, 17.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_ridge = grid.best_estimator_
print(best_ridge)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_ridge, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_ridge, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# In[ ]:


modelname.append('Impute_full')
lassoscore.append(0.1115)
ridgescore.append(0.1125)
kaggle_lasso.append(0.11847)
kaggle_ridge.append(0.11727)
timeelapsed.append(12600)
maecv_lasso.append(13250.529)
maecv_ridge.append(13383.857)


# In[ ]:


# just to have it as output
prediction = np.expm1(best_ridge.predict(butch_test)) 

sub = pd.DataFrame()
sub['Id'] = df_test['Id']
sub['SalePrice'] = prediction
sub.to_csv('best_ridge_full_imputation.csv',index=False)


# At this stage, spoiler alert, the ridge result is the best I was able to achieve with these models on Kaggle. Of course, the difference is at the third decimal and way within the normal fluctuations in result one may expect.
# 
# One more hour to get at this point. Let's start manipulating our features.
# 
# # Transformations
# 
# Here, unfortunately, I can't show the 3 scripts that led me to this decision but I can describe the process:
# 
# * drop the useless features from the previous step
# * Explore the data better, for example as I did in [this kernel](https://www.kaggle.com/lucabasa/house-price-detailed-data-exploration)
# * Propose a transformation
# * Check if the cv result improves significantly
# * Gather all the meaningful transformations and add them one by one by checking that the cv score is going down
# 
# Until the end, I purposely never checked on Kaggle the public score because I know it would influence me.
# 
# The transformations are proposed as follows:
# 
# * In an ordinal feature, use a value from 0 to, say, 5 instead of making dummies out of it. This makes sense since Excellent is bigger than Good.
# * Sometimes, the difference between Excellent and Good is not the same as the one between Good and Typical. Account for that.
# * Propose transformation to correct for sparsity.
# 
# At times, it is even better to not transform an ordinal feature and leave it as a dummy. My explanation for that, which explains also why I have 2 strategies to make them numerical, is that these features are subjective, as far as I know, they were gathered by different people and there is no parameter for defining something good or excellent.

# In[ ]:


df_train.drop("Exterior1st", axis=1, inplace=True) #these I know they are not helpful already
df_test.drop("Exterior1st", axis=1, inplace=True)
df_train.drop("Exterior2nd", axis=1, inplace=True)
df_test.drop("Exterior2nd", axis=1, inplace=True)
df_train.drop("SaleType", axis=1, inplace=True)
df_test.drop("SaleType", axis=1, inplace=True)


# Now all the transformation I came up with

# In[ ]:


def tr_ExtQual(df):
    df.loc[df.ExterQual == 'Fa', 'ExterQual'] = 0
    df.loc[df.ExterQual == 'TA', 'ExterQual'] = 1
    df.loc[df.ExterQual == 'Gd', 'ExterQual'] = 2
    df.loc[df.ExterQual == 'Ex', 'ExterQual'] = 3
    df.ExterQual = pd.to_numeric(df.ExterQual)
    return df
def tr_ExtQual_plus(df):
    df.loc[df.ExterQual == 'Fa', 'ExterQual'] = 1
    df.loc[df.ExterQual == 'TA', 'ExterQual'] = 1
    df.loc[df.ExterQual == 'Gd', 'ExterQual'] = 2
    df.loc[df.ExterQual == 'Ex', 'ExterQual'] = 3
    df.ExterQual = pd.to_numeric(df.ExterQual)
    return df

def tr_ExtCond(df):
    df.loc[df.ExterCond == 'Po', 'ExterCond'] = 0
    df.loc[df.ExterCond == 'Fa', 'ExterCond'] = 1
    df.loc[df.ExterCond == 'TA', 'ExterCond'] = 2
    df.loc[df.ExterCond == 'Gd', 'ExterCond'] = 3
    df.loc[df.ExterCond == 'Ex', 'ExterCond'] = 4
    df.ExterCond = pd.to_numeric(df.ExterCond)
    return df
def tr_ExtCond_plus(df):
    df.loc[df.ExterCond == 'Po', 'ExterCond'] = 1
    df.loc[df.ExterCond == 'Fa', 'ExterCond'] = 1
    df.loc[df.ExterCond == 'TA', 'ExterCond'] = 1
    df.loc[df.ExterCond == 'Gd', 'ExterCond'] = 2
    df.loc[df.ExterCond == 'Ex', 'ExterCond'] = 2
    df.ExterCond = pd.to_numeric(df.ExterCond)
    return df

def tr_BsmtQu(df):
    df.loc[df.BsmtQual == 'NoBsmt', 'BsmtQual'] = 0
    df.loc[df.BsmtQual == 'Fa', 'BsmtQual'] = 1
    df.loc[df.BsmtQual == 'TA', 'BsmtQual'] = 2
    df.loc[df.BsmtQual == 'Gd', 'BsmtQual'] = 3
    df.loc[df.BsmtQual == 'Ex', 'BsmtQual'] = 4
    df.BsmtQual = pd.to_numeric(df.BsmtQual)
    return df
def tr_BsmtQu_plus(df):
    df.loc[df.BsmtQual == 'NoBsmt', 'BsmtQual'] = 0
    df.loc[df.BsmtQual == 'Fa', 'BsmtQual'] = 1
    df.loc[df.BsmtQual == 'TA', 'BsmtQual'] = 4
    df.loc[df.BsmtQual == 'Gd', 'BsmtQual'] = 10
    df.loc[df.BsmtQual == 'Ex', 'BsmtQual'] = 21
    df.BsmtQual = pd.to_numeric(df.BsmtQual)
    return df

def tr_BsmtCo(df):
    df.loc[df.BsmtCond == 'NoBsmt', 'BsmtCond'] = 0
    df.loc[df.BsmtCond == 'Po', 'BsmtCond'] = 1
    df.loc[df.BsmtCond == 'Fa', 'BsmtCond'] = 2
    df.loc[df.BsmtCond == 'TA', 'BsmtCond'] = 3
    df.loc[df.BsmtCond == 'Gd', 'BsmtCond'] = 4
    df.BsmtCond = pd.to_numeric(df.BsmtCond)
    return df

def tr_BsmtExp(df):
    df.loc[df.BsmtExposure == 'NoBsmt', 'BsmtExposure'] = 0
    df.loc[df.BsmtExposure == 'No', 'BsmtExposure'] = 1
    df.loc[df.BsmtExposure == 'Mn', 'BsmtExposure'] = 2
    df.loc[df.BsmtExposure == 'Av', 'BsmtExposure'] = 3
    df.loc[df.BsmtExposure == 'Gd', 'BsmtExposure'] = 4
    df.BsmtExposure = pd.to_numeric(df.BsmtExposure)
    return df
def tr_BsmtExp_plus(df):
    df.loc[df.BsmtExposure == 'NoBsmt', 'BsmtExposure'] = 0
    df.loc[df.BsmtExposure == 'No', 'BsmtExposure'] = 6
    df.loc[df.BsmtExposure == 'Mn', 'BsmtExposure'] = 7
    df.loc[df.BsmtExposure == 'Av', 'BsmtExposure'] = 8
    df.loc[df.BsmtExposure == 'Gd', 'BsmtExposure'] = 12
    df.BsmtExposure = pd.to_numeric(df.BsmtExposure)
    return df

def tr_HeatQ(df):
    df.loc[df.HeatingQC == 'Po', 'HeatingQC'] = 0
    df.loc[df.HeatingQC == 'Fa', 'HeatingQC'] = 1
    df.loc[df.HeatingQC == 'TA', 'HeatingQC'] = 2
    df.loc[df.HeatingQC == 'Gd', 'HeatingQC'] = 3
    df.loc[df.HeatingQC == 'Ex', 'HeatingQC'] = 4
    df.HeatingQC = pd.to_numeric(df.HeatingQC)
    return df
def tr_HeatQ_plus(df):
    df.loc[df.HeatingQC == 'Po', 'HeatingQC'] = 1
    df.loc[df.HeatingQC == 'Fa', 'HeatingQC'] = 1
    df.loc[df.HeatingQC == 'TA', 'HeatingQC'] = 3
    df.loc[df.HeatingQC == 'Gd', 'HeatingQC'] = 4
    df.loc[df.HeatingQC == 'Ex', 'HeatingQC'] = 7
    df.HeatingQC = pd.to_numeric(df.HeatingQC)
    return df

def tr_KitcQu(df):
    df.loc[df.KitchenQual == 'Fa', 'KitchenQual'] = 1
    df.loc[df.KitchenQual == 'TA', 'KitchenQual'] = 2
    df.loc[df.KitchenQual == 'Gd', 'KitchenQual'] = 3
    df.loc[df.KitchenQual == 'Ex', 'KitchenQual'] = 4
    df.KitchenQual = pd.to_numeric(df.KitchenQual)
    return df
def tr_KitcQu_plus(df):
    df.loc[df.KitchenQual == 'Fa', 'KitchenQual'] = 1
    df.loc[df.KitchenQual == 'TA', 'KitchenQual'] = 4
    df.loc[df.KitchenQual == 'Gd', 'KitchenQual'] = 10
    df.loc[df.KitchenQual == 'Ex', 'KitchenQual'] = 21
    df.KitchenQual = pd.to_numeric(df.KitchenQual)
    return df

def tr_FireQu(df):
    df.loc[df.FireplaceQu == 'NoFire', 'FireplaceQu'] = 0
    df.loc[df.FireplaceQu == 'Po', 'FireplaceQu'] = 1
    df.loc[df.FireplaceQu == 'Fa', 'FireplaceQu'] = 2
    df.loc[df.FireplaceQu == 'TA', 'FireplaceQu'] = 3
    df.loc[df.FireplaceQu == 'Gd', 'FireplaceQu'] = 4
    df.loc[df.FireplaceQu == 'Ex', 'FireplaceQu'] = 5
    df.FireplaceQu = pd.to_numeric(df.FireplaceQu)
    return df
def tr_FireQu_plus(df):
    df.loc[df.FireplaceQu == 'NoFire', 'FireplaceQu'] = 0
    df.loc[df.FireplaceQu == 'Po', 'FireplaceQu'] = 0
    df.loc[df.FireplaceQu == 'Fa', 'FireplaceQu'] = 2
    df.loc[df.FireplaceQu == 'TA', 'FireplaceQu'] = 3
    df.loc[df.FireplaceQu == 'Gd', 'FireplaceQu'] = 4
    df.loc[df.FireplaceQu == 'Ex', 'FireplaceQu'] = 8
    df.FireplaceQu = pd.to_numeric(df.FireplaceQu)
    return df

def tr_GarQu(df):
    df.loc[df.GarageQual == 'NoGrg', 'GarageQual'] = 0
    df.loc[df.GarageQual == 'Po', 'GarageQual'] = 1
    df.loc[df.GarageQual == 'Fa', 'GarageQual'] = 2
    df.loc[df.GarageQual == 'TA', 'GarageQual'] = 3
    df.loc[df.GarageQual == 'Gd', 'GarageQual'] = 4
    if df.name == 'Train':
        df.loc[df.GarageQual == 'Ex', 'GarageQual'] = 5
    df.GarageQual = pd.to_numeric(df.GarageQual)
    return df

def tr_GarCo(df):
    df.loc[df.GarageCond == 'NoGrg', 'GarageCond'] = 0
    df.loc[df.GarageCond == 'Po', 'GarageCond'] = 1
    df.loc[df.GarageCond == 'Fa', 'GarageCond'] = 2
    df.loc[df.GarageCond == 'TA', 'GarageCond'] = 3
    df.loc[df.GarageCond == 'Gd', 'GarageCond'] = 4
    df.loc[df.GarageCond == 'Ex', 'GarageCond'] = 5
    df.GarageCond = pd.to_numeric(df.GarageCond)
    return df

def tr_MSZo(df):
    df.loc[(df.MSZoning == 'RH') | (df.MSZoning == 'RM'), 'MSZoning'] = 'ResMedHig'
    df.loc[(df.MSZoning == 'FV'), 'MSZoning'] = 'Vil'
    df.loc[(df.MSZoning == 'RL')| (df.MSZoning == 'C (all)'), 'MSZoning'] = 'ResLowCom'
    return df

def tr_Alley(df):
    df.loc[(df.Alley == 'Grvl') | (df.Alley == 'Pave'), 'Alley'] = 'Alley'
    df.loc[df.Alley == 'NoAlley', 'Alley'] = 'NoAlley'
    return df

def tr_LotSh(df):
    irr = ['IR1', 'IR2', 'IR3']
    df.loc[(df.LotShape.isin(irr)), 'LotShape'] = 'Irreg'
    df.loc[df.LotShape == 'Reg', 'LotShape'] = 'Reg'
    return df

def tr_Cond1(df):
    ArtFee = ['Artery', 'Feedr']
    stat = ['RRAe', 'RRAn', 'RRNe', 'RRNn']
    pos = ['PosA', 'PosN']
    df.loc[(df.Condition1.isin(ArtFee)), 'Condition1'] = 'ArtFee'
    df.loc[(df.Condition1.isin(stat)), 'Condition1'] = 'Station'
    df.loc[(df.Condition1.isin(pos)), 'Condition1'] = 'Station'
    df.loc[df.Condition1 == 'Norm', 'Condition1'] = 'Norm'
    return df

def tr_BldTy(df):
    df.loc[(df.BldgType == '2fmCon') | (df.BldgType == 'Duplex'), 'BldgType'] = '2FamDup'
    df.loc[(df.BldgType == 'Twnhs') | (df.BldgType == 'TwnhsE'), 'BldgType'] = 'Twnhs+E'
    df.loc[(df.BldgType == '1Fam'), 'BldgType'] = '1Fam'
    return df

def tr_HSty(df):
    onepl = ['1.5Fin', '1.5Unf']
    twopl = ['2.5Fin', '2.5Unf', '2Story']
    spl = ['SFoyer', 'SLvl']
    df.loc[df.HouseStyle.isin(onepl), 'HouseStyle'] = '1.5'
    df.loc[df.HouseStyle.isin(twopl), 'HouseStyle'] = '2plus'
    df.loc[df.HouseStyle.isin(spl), 'HouseStyle'] = 'Split'
    df.loc[df.HouseStyle == '1Story', 'HouseStyle'] = "1Story"
    return df

def tr_Found(df):
    fancy = ['BrkTil', 'Stone', 'Wood']
    cement = ['PConc', 'Slab']
    df.loc[df.Foundation.isin(fancy), 'Foundation'] = 'Fancy'
    df.loc[df.Foundation.isin(cement), 'Foundation'] = 'Cement'
    df.loc[df.Foundation == 'CBlock', 'Foundation'] = 'Cider'
    return df

def tr_MasVnrTy(df):
    df.loc[df.MasVnrType == 'None', 'MasVnrType'] = 'None'
    df.loc[df.MasVnrType == 'Stone', 'MasVnrType'] = 'Stone'
    df.loc[(df.MasVnrType == 'BrkCmn') | (df.MasVnrType == 'BrkFace'), 'MasVnrType'] = 'Bricks'
    return df

def tr_Elec(df):
    df.loc[df.Electrical == "SBrkr", "Electrical"] = "SBrkr"
    fuse = ['FuseA', 'FuseF', 'FuseP', 'Mix']
    df.loc[df.Electrical.isin(fuse), "Electrical"] = "Fuse"
    return df
    
def tr_GrgTy(df):
    incl = ['Attchd', 'Basment', 'BuiltIn']
    escl = ['2Types', 'CarPort', 'Detchd']
    df.loc[df.GarageType.isin(incl), 'GarageType'] = 'Connected'
    df.loc[df.GarageType.isin(escl), 'GarageType'] = 'NonConnected'
    df.loc[df.GarageType == 'NoGrg', 'GarageType'] = 'NoGrg'
    return df

def tr_PvdDr(df):
    df.loc[df.PavedDrive == 'N', 'PavedDrive'] = 'N'
    df.loc[df.PavedDrive == 'P', 'PavedDrive'] = 'N'
    df.loc[df.PavedDrive == 'Y', 'PavedDrive'] = 'Y'
    return df

def tr_Fence(df):
    df.loc[df.Fence == 'NoFence', 'Fence'] = 'NoFence'
    df.loc[(df.Fence == 'MnPrv') | (df.Fence == 'GdPrv'), 'Fence'] = 'Prv'
    df.loc[(df.Fence == 'MnWw') | (df.Fence == 'GdWo'), 'Fence'] = 'Wo'
    return df


# Now only the ones that work, from the most relevant (in terms of impact on the cv score) to the least one.

# In[ ]:


tr_train = df_train.copy() #because memory is free... sort of
tr_test = df_test.copy()

tr_train.name = 'Train' #because some dummies were different, see the transformation above
tr_test.name = 'Test'

tr_train = tr_GarQu(tr_train)
tr_test = tr_GarQu(tr_test)
tr_train = tr_FireQu(tr_train)
tr_test = tr_FireQu(tr_test)
tr_train = tr_HeatQ_plus(tr_train)
tr_test = tr_HeatQ_plus(tr_test)
tr_train = tr_PvdDr(tr_train)
tr_test = tr_PvdDr(tr_test)
tr_train = tr_GrgTy(tr_train)
tr_test = tr_GrgTy(tr_test)
tr_train = tr_ExtQual_plus(tr_train)
tr_test = tr_ExtQual_plus(tr_test)
tr_train = tr_MasVnrTy(tr_train)
tr_test = tr_MasVnrTy(tr_test) 
tr_train = tr_GarCo(tr_train)
tr_test = tr_GarCo(tr_test) 
tr_train = tr_BsmtCo(tr_train)
tr_test = tr_BsmtCo(tr_test) 
tr_train = tr_Elec(tr_train)
tr_test = tr_Elec(tr_test) 
tr_train = tr_BsmtQu_plus(tr_train)
tr_test = tr_BsmtQu_plus(tr_test) 
tr_train = tr_LotSh(tr_train)
tr_test = tr_LotSh(tr_test)
tr_train = tr_Alley(tr_train)
tr_test = tr_Alley(tr_test)


# Let's go again, run everything to see how better we got

# In[ ]:


butch_train = tr_train[[col for col in tr_test.columns if col not in mis_test]].dropna(axis=1)
butch_test = tr_test[[col for col in tr_test.columns if col not in mis_train]].dropna(axis=1)

butch_train.drop("Id", axis=1, inplace=True)
butch_test.drop("Id", axis=1, inplace=True)

butch_train = pd.get_dummies(butch_train)
butch_test = pd.get_dummies(butch_test)

print(set(df_train.columns) - set(df_test.columns))

butch_train = butch_train[[col for col in butch_test.columns if col in butch_train.columns]]
butch_test = butch_test[[col for col in butch_train.columns]]

#because redundant with MisGarage
butch_train = butch_train.drop([col for col in butch_train.columns if 'NoGrg' in col], axis=1) 
butch_test = butch_test.drop([col for col in butch_test.columns if 'NoGrg' in col], axis=1)
#because redundant with MisBsm
butch_train = butch_train.drop([col for col in butch_train.columns if 'NoBsmt' in col], axis=1)
butch_test = butch_test.drop([col for col in butch_test.columns if 'NoBsmt' in col], axis=1)

butch_train = butch_train[butch_train.GrLivArea < 4500] #according to documentation
target = np.log1p(df_train['SalePrice']) #for consistency

(butch_train.columns != butch_test.columns).sum()


# The problem of the dummies mismatch is gone.

# In[ ]:


butch_train.shape


# In[ ]:


pipe = Pipeline([scl, ('lasso', Lasso(max_iter=2000))])

param_grid = [{'lasso__alpha' : [0.0001, 0.0005, 0.00075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_lasso = grid.best_estimator_
print(best_lasso)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_lasso, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_lasso, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# In[ ]:


pipe = Pipeline([scl, ('ridge', Ridge())])

param_grid = [{'ridge__alpha' : [0.0001, 0.0005, 0.00075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5,
                                10, 15, 17.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_ridge = grid.best_estimator_
print(best_ridge)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_ridge, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_ridge, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# In[ ]:


modelname.append('Transform')
lassoscore.append(0.1106)
ridgescore.append(0.1114)
kaggle_lasso.append(0.11910)
kaggle_ridge.append(0.11838)
timeelapsed.append(16200)
maecv_lasso.append(13259.404)
maecv_ridge.append(13375.657)


# With about one hour of work, we can reduce our cv score a little bit more.
# 
# Thanks to the extensive eda performed before the imputation from the documentation, we have already done 2 more incremental steps at a relatively low time investment.
# 
# Actually, the insights I received from that eda allow me to do a couple more quick steps.
# 
# # Feature Selection from EDA
# 
# I have seen already that some features make little to no sense in how they can be related to the final price. I can help the learning and the execution time of my models by simply removing them.
# 
# Since I was able to make it work in a few lines of code, this time I can show you the entire process.
# 
# First, I pick some candidates thanks to my EDA.

# In[ ]:


candidates = ['Condition1', 'Condition2', 'YearRemodAdd', "RoofStyle", 
              'RoofMatl','BsmtFinSF1', 'BsmtFinSF2', 'Heating', 'Electrical', 
              '1stFlrSF', '2ndFlrSF', 'LowQualFinSF','Functional', 'TotRmsAbvGrd',
             'GarageCars', 'YrSold', 'MoSold']


# Now, I don't know which one I should drop in order to see an improvement in my cv score. So I will just test them all individually and pick only the one that gives me a better performance for, say, the Lasso regression (it is faster and I am lazy). 
# 
# Then, I will sequentially remove every good candidate starting from the one with the best impact and keep going until my cv score stops improving.
# 
# The entire loop took 1 minute and a half on my pc.

# In[ ]:


get_ipython().run_cell_magic('time', '', '\nwinners = []\n\npipe = Pipeline([scl, (\'lasso\', Lasso(max_iter=2000))])\n\nparam_grid = [{\'lasso__alpha\' : [0.0001, 0.0005, 0.00075,\n                                 0.001, 0.005, 0.0075, \n                                 0.01, 0.05, 0.075,\n                                 0.1, 0.5, 0.75, \n                                 1, 5, 7.5]}]\n\ngrid = GridSearchCV(pipe, param_grid=param_grid, \n                    cv=kfolds, scoring=\'neg_mean_squared_error\', return_train_score=True, n_jobs=-1)\n\nfor feat in candidates:\n    sel_train = tr_train.drop(feat, axis=1) #copies of the dataframe optained with the transformations above\n    sel_test = tr_test.drop(feat, axis=1) # minus one feature.\n    butch_train = sel_train[[col for col in sel_test.columns if col not in mis_test]].dropna(axis=1)\n    butch_test = sel_test[[col for col in sel_test.columns if col not in mis_train]].dropna(axis=1)\n    butch_train.drop("Id", axis=1, inplace=True)\n    butch_test.drop("Id", axis=1, inplace=True)\n    butch_train = pd.get_dummies(butch_train)\n    butch_test = pd.get_dummies(butch_test)\n    #print(set(df_train.columns) - set(df_test.columns))\n    butch_train = butch_train[[col for col in butch_test.columns if col in butch_train.columns]]\n    butch_test = butch_test[[col for col in butch_train.columns]]\n    butch_train = butch_train.drop([col for col in butch_train.columns if \'NoGrg\' in col], axis=1)\n    butch_test = butch_test.drop([col for col in butch_test.columns if \'NoGrg\' in col], axis=1)\n    butch_train = butch_train.drop([col for col in butch_train.columns if \'NoBsmt\' in col], axis=1)\n    butch_test = butch_test.drop([col for col in butch_test.columns if \'NoBsmt\' in col], axis=1)\n    butch_train = butch_train[butch_train.GrLivArea < 4500] #according to documentation\n    target = np.log1p(df_train[\'SalePrice\']) #for consistency\n    grid.fit(butch_train, target)\n    score = np.sqrt(-grid.best_score_)\n    if score <= 0.11065: #give some margin\n        print(feat, score-0.11063297306583295) #previous best result\n        print(score)\n        winners.append(feat)\n        print("_"*40)\n    \nprint(winners)')


# In[ ]:


# in the comments the cv result you would get by just stopping there and the reason why I considered them.

#not really relevant
sel_train = tr_train.drop('LowQualFinSF', axis=1)
sel_test = tr_test.drop('LowQualFinSF', axis=1) #0.110506961384
# redundant with GrLivArea
sel_train.drop('TotRmsAbvGrd', axis=1, inplace=True)
sel_test.drop('TotRmsAbvGrd', axis=1, inplace=True) #0.110401590715
# looking at pictures of the 3 categories, I couldn't appreciate any difference
sel_train.drop('RoofStyle', axis=1, inplace=True)
sel_test.drop('RoofStyle', axis=1, inplace=True) #0.110335024836
# very sparse classes
sel_train.drop('Heating', axis=1, inplace=True)
sel_test.drop('Heating', axis=1, inplace=True) #0.110301207584
# couldn't see any pattern or imagine that it could matter in any way
sel_train.drop('MoSold', axis=1, inplace=True)
sel_test.drop('MoSold', axis=1, inplace=True) #0.110266414516
# very sparse classes
sel_train.drop('Electrical', axis=1, inplace=True)
sel_test.drop('Electrical', axis=1, inplace=True) #0.110241668859
# surprisingly, not showing any trend in the dataset
sel_train.drop('YrSold', axis=1, inplace=True)
sel_test.drop('YrSold', axis=1, inplace=True) #0.110208857877
# Like roof style
sel_train.drop('RoofMatl', axis=1, inplace=True)
sel_test.drop('RoofMatl', axis=1, inplace=True) #0.110189729503
# reduntant with the other features
sel_train.drop('BsmtFinSF1', axis=1, inplace=True)
sel_test.drop('BsmtFinSF1', axis=1, inplace=True) #0.11017219933
# redundant with GrLivArea
sel_train.drop('2ndFlrSF', axis=1, inplace=True)
sel_test.drop('2ndFlrSF', axis=1, inplace=True) #0.11016945367


# Moreover, seeing who of the candidates won the race to be dropped, I decided to drop a few more categories out of consistency and intuition

# In[ ]:


sel_train.drop('BsmtFinSF2', axis=1, inplace=True)
sel_test.drop('BsmtFinSF2', axis=1, inplace=True) #0.110080460877
sel_train.drop('LandSlope', axis=1, inplace=True)
sel_test.drop('LandSlope', axis=1, inplace=True) #0.1099013725


# Now we are ready to go, we will see faster models due to the fact it will learn on 185 features instead of 211.

# In[ ]:


butch_train = sel_train[[col for col in sel_test.columns if col not in mis_test]].dropna(axis=1)
butch_test = sel_test[[col for col in sel_test.columns if col not in mis_train]].dropna(axis=1)

butch_train.drop("Id", axis=1, inplace=True)
butch_test.drop("Id", axis=1, inplace=True)

butch_train = pd.get_dummies(butch_train)
butch_test = pd.get_dummies(butch_test)

print(set(df_train.columns) - set(df_test.columns))

butch_train = butch_train[[col for col in butch_test.columns if col in butch_train.columns]]
butch_test = butch_test[[col for col in butch_train.columns]]

#because redundant with MisGarage
butch_train = butch_train.drop([col for col in butch_train.columns if 'NoGrg' in col], axis=1) 
butch_test = butch_test.drop([col for col in butch_test.columns if 'NoGrg' in col], axis=1)
#because redundant with MisBsm
butch_train = butch_train.drop([col for col in butch_train.columns if 'NoBsmt' in col], axis=1) 
butch_test = butch_test.drop([col for col in butch_test.columns if 'NoBsmt' in col], axis=1)

butch_train = butch_train[butch_train.GrLivArea < 4500] #according to documentation
target = np.log1p(df_train['SalePrice']) #for consistency

(butch_train.columns != butch_test.columns).sum()


# In[ ]:


butch_train.shape


# In[ ]:


pipe = Pipeline([scl, ('lasso', Lasso(max_iter=2000))])

param_grid = [{'lasso__alpha' : [0.0001, 0.0005, 0.00075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_lasso = grid.best_estimator_
print(best_lasso)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_lasso, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_lasso, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# And for Ridge

# In[ ]:


pipe = Pipeline([scl, ('ridge', Ridge())])

param_grid = [{'ridge__alpha' : [0.0001, 0.0005, 0.00075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5,
                                10, 15, 17.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_ridge = grid.best_estimator_
print(best_ridge)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_ridge, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_ridge, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# In[ ]:


modelname.append('Feat_Sel_EDA')
lassoscore.append(0.1099)
ridgescore.append(0.1107)
kaggle_lasso.append(0.11953)
kaggle_ridge.append(0.11861)
timeelapsed.append(18000)
maecv_lasso.append(13161.658)
maecv_ridge.append(13273.673)


# Only 30 minutes to make decisions, write the code, and run it to see this kind of improvement. 
# 
# I feel we are getting closer to the max predictive power of these 2 models but I still have something that came to my mind during the EDA and I didn't test it yet.
# 
# # Simple feature engineering
# 
# Nothing fancy really. Again there was some try and error (in cv only, of course) involved but it regards features that didn't help after all and thus you will never see them.
# 
# First, we have *LotFrontage: Linear feet of street connected to property* and *LotArea: Lot size in square feet** 
# 
# I thought, well, assuming a rectangular lot, I can have the *depth* of the lot and this can indicate how "isolated" the house is from the street. I put some 0's in LotFrontage during the imputation, so I will take the inverse of the depth for convenience.

# In[ ]:


eng_train = sel_train.copy()
eng_test = sel_test.copy()
eng_test['LotDepth'] = eng_test['LotFrontage'] / eng_test['LotArea']
eng_train['LotDepth'] = eng_train['LotFrontage'] / eng_train['LotArea']


# Then we have half and full bathrooms. I thought that I might be interested in the total number of bathrooms.

# In[ ]:


eng_train['TotBath'] = eng_train.FullBath + eng_train.HalfBath
eng_test['TotBath'] = eng_test.FullBath + eng_test.HalfBath


# At last, we have a lot of features regarding the outside porch in all its types. I thought it could be interesting to have a total of that.

# In[ ]:


eng_train['TotPorch'] = (eng_train['WoodDeckSF'] + eng_train['OpenPorchSF'] + eng_train['EnclosedPorch'] + 
                       eng_train['3SsnPorch'] + eng_train['ScreenPorch'])
eng_test['TotPorch'] = (eng_test['WoodDeckSF'] + eng_test['OpenPorchSF'] + eng_test['EnclosedPorch'] + 
                       eng_test['3SsnPorch'] + eng_test['ScreenPorch'])


# I tried a couple of other things such as "Has a Second Floor" but they were not helping after all (which makes sense, we removed 2nfFloorSF that was giving a more accurate information because it was "distracting" the model).
# 
# Let's roll again.

# In[ ]:


butch_train = eng_train[[col for col in eng_test.columns if col not in mis_test]].dropna(axis=1)
butch_test = eng_test[[col for col in eng_test.columns if col not in mis_train]].dropna(axis=1)

butch_train.drop("Id", axis=1, inplace=True)
butch_test.drop("Id", axis=1, inplace=True)

butch_train = pd.get_dummies(butch_train)
butch_test = pd.get_dummies(butch_test)

print(set(df_train.columns) - set(df_test.columns))

butch_train = butch_train[[col for col in butch_test.columns if col in butch_train.columns]]
butch_test = butch_test[[col for col in butch_train.columns]]

#because redundant with MisGarage
butch_train = butch_train.drop([col for col in butch_train.columns if 'NoGrg' in col], axis=1) 
butch_test = butch_test.drop([col for col in butch_test.columns if 'NoGrg' in col], axis = 1)
#because redundant with MisBsm
butch_train = butch_train.drop([col for col in butch_train.columns if 'NoBsmt' in col], axis=1) 
butch_test = butch_test.drop([col for col in butch_test.columns if 'NoBsmt' in col], axis=1)

butch_train = butch_train[butch_train.GrLivArea < 4500] #according to documentation
target = np.log1p(df_train['SalePrice']) #for consistency

(butch_train.columns != butch_test.columns).sum()


# In[ ]:


butch_train.shape


# In[ ]:


pipe = Pipeline([scl, ('lasso', Lasso(max_iter=2000))])

param_grid = [{'lasso__alpha' : [0.0001, 0.0005, 0.00075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_lasso = grid.best_estimator_
print(best_lasso)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_lasso, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_lasso, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# And Ridge, as usual.

# In[ ]:


pipe = Pipeline([scl, ('ridge', Ridge())])

param_grid = [{'ridge__alpha' : [0.0001, 0.0005, 0.00075,
                                 0.001, 0.005, 0.0075, 
                                 0.01, 0.05, 0.075,
                                 0.1, 0.5, 0.75, 
                                 1, 5, 7.5,
                                10, 15, 17.5]}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_ridge = grid.best_estimator_
print(best_ridge)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))
print(pd.DataFrame(grid.cv_results_)[['params','mean_test_score','std_test_score']])


# In[ ]:


dol = get_dollars(best_ridge, kfolds, butch_train, target, old_target)
dol


# In[ ]:


coefs = get_coef(best_ridge, butch_train.columns)
coefs.head(10)


# In[ ]:


coefs.tail(10)


# In[ ]:


modelname.append('Feat_eng')
lassoscore.append(0.1089)
ridgescore.append(0.1094)
kaggle_lasso.append(0.11928)
kaggle_ridge.append(0.11828)
timeelapsed.append(19800)
maecv_lasso.append(13027.341)
maecv_ridge.append(13060.855)


# Other 30 minutes of coding and quick experiments and we got another small boost in performance.
# 
# The well of the EDA is now dry for me, I will take a moment to have a look at some learning curve to see if it triggers some idea.
# 
# # Checking the learning process.
# 
# Looking at a number is quick and gives some insights but it is always a good thing (at any stage really) to check how a model is learning the data.
# 
# To do so, I can look at the learning curves.
# 
# These show me how the performance on the train and test sets evolves if we vary the size of the training set. Again, I use cross-validation because it is cooler.
# 
# In terms of time, I am cheating because I made the function a while back, so it is not really fair to consider this step in this experiment.

# In[ ]:


def learning_print(estimator, train, label, folds):
    """
    estimator: an estimator
    train: set with input data
    label: target variable
    folds: cross validation
    """
    train_sizes = np.arange(0.1, 1, 0.05)
    train_sizes, train_scores, validation_scores = learning_curve(
                                                   estimator=estimator, X=train,
                                                   y=label, train_sizes=train_sizes, cv=folds,
                                                   scoring='neg_mean_squared_error')
    train_scores_mean = np.mean(np.sqrt(-train_scores), axis=1)
    train_scores_std = np.std(np.sqrt(-train_scores), axis=1)
    validation_scores_mean = np.mean(np.sqrt(-validation_scores), axis=1)
    validation_scores_std = np.std(np.sqrt(-validation_scores), axis=1)
    fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.plot(train_sizes, train_scores_mean, label='Training error')
    ax1.plot(train_sizes, validation_scores_mean, label='Validation error')
    ax2.plot(train_sizes, train_scores_std, label='Training std')
    ax2.plot(train_sizes, validation_scores_std, label='Validation std')
    ax1.legend()
    ax2.legend()


# In[ ]:


learning_print(best_lasso, butch_train, target, kfolds)


# In[ ]:


learning_print(best_ridge, butch_train, target, kfolds)


# From these plots I can say the following:
# 
# * they learn very similarly
# * Both have a bias around 0.1, which is about 4 times better than the baseline and I would consider it as low
# * Both models would benefit if they could learn from more data (they 2 curves have still margin to converge)
# * Ridge has more variance (the gap between the training and validation is bigger)
# 
# Since I can't get my hands on more data, I could try to increase the regularization and/or reduce the number of features (which would definitely increase the bias).
# 
# Let's give them a chance with a more accurate grid search. From all the previous steps I can narrow down the parameter space and make it more granular.

# In[ ]:


pipe = Pipeline([scl, ('lasso', Lasso(max_iter=2000))])

param_grid = [{'lasso__alpha' : np.arange(0.0001,0.001, 0.00001)}] #because it was always 0.0005

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_lasso = grid.best_estimator_
print(best_lasso)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))


# In[ ]:


dol = get_dollars(best_lasso, kfolds, butch_train, target, old_target)
dol


# In[ ]:


pipe = Pipeline([scl, ('ridge', Ridge())])

param_grid = [{'ridge__alpha' : np.arange(5,15,0.5)}]

grid = GridSearchCV(pipe, param_grid=param_grid, 
                    cv=kfolds, scoring='neg_mean_squared_error', return_train_score=True, n_jobs=-1)

get_ipython().run_line_magic('time', 'grid.fit(butch_train, target)')

#let's see the best estimator
best_ridge = grid.best_estimator_
print(best_ridge)
print("_"*40)
#with its score
print(np.sqrt(-grid.best_score_))


# So according to my cv scores, I should decrease the regularization of Lasso a bit for a small improvement (not observable on the Leaderboard) and Ridge was already at its best.
# 
# # What I have learned and next steps
# 
# A total of 5 hours and a half have passed. I am out of ideas on how to get my models a better version of themselves without using more complicated and fancy algorithms. I feel it is a good moment to stop and think about what I have learned.
# 
# I always had the problem of finding something interesting in the data and dig into it with all the passion I have. This is **a lot** of fun (and we are all here for that) but more often than not I find myself spending 10 hours on something that will not help me solve the problem. 
# 
# This "agile" setting forced me to see a problem, ignore it for the time being, see how it goes, fix it in the next iteration. I felt way more productive and efficient because I was not getting distracted by the next problem that I was finding while fixing the previous one.
# 
# Moreover, I feel I had the chance of learning what can most likely help a model rather than not because I could see the effect of a single action in my results and thus it was easier to isolate that effect.
# 
# One thing that I am happy about is that my cross-validated scores are very reliable in predicting how the model will generalize (some fluctuations, but what doesn't fluctuate after all). The main reason for that is that I am careful of not use information I am not supposed to use. In other words, data leakage can help your public score (you can use the answers to help the question) but it won't make your model generalizable as you might think because it is easy to *overfit the test* .
# 
# The model here won't change the real estate industry but it is the product of half a day of work and we are talking about a very conservative industry. My concern with the data is that there are too many subjective features that get a lot of importance (Overall Quality above all) and these are not reliable in the long term unless the criteria are very strict.
# 
# This is a playground competition and this is, by any means, a game and an excuse to receive some feedback on how we can all do better. A few things came to my mind so far:
# 
# * I keep all the dummies and this can cause collinearity issues. It is true that we are talking about 2 regularized model and it should not matter too much, but it would be a good thing to check that.
# * I didn't remove the skewness. Looking at other kernels and other experiments I did, a boxcox transformation would help. The one thing that I would do is to put the boxcox inside of the pipeline so that it doesn't use information of the validation set during cross-validation.
# * Use a model like RandomForest to select the features. Again, inside of the pipeline. It would make it much slower but we spent already 5.5 hours in failing fast, we can try to fail slowly for once.
# * Get fancy with ensemble and stacking models because it is a cool thing to do.
# 
# When I submitted my results, I got around the 550th position on the leaderboard (top 13%, kaggle said). The best score I got is 0.11727 and a top 100 result would be 0.114. One may evaluate in a realistic situation if that 0.003 of improvement in the mean squared error is worth the work that would require.
# 
# At last, here a summary of what happened in this kernel.

# In[ ]:


scoresummary = pd.DataFrame({'Model Name' : modelname,
                            'CVScore Lasso': lassoscore,
                            'CVScore Ridge': ridgescore,
                            'KaggleScore Lasso': kaggle_lasso,
                            'KaggleScore Ridge': kaggle_ridge,
                            'MAE Lasso': maecv_lasso,
                            'MAE Ridge': maecv_ridge,
                            'Cumulative Time': timeelapsed})

scoresummary[['Model Name', 'CVScore Lasso', 'CVScore Ridge', 'KaggleScore Lasso', 
             'KaggleScore Ridge', 'MAE Lasso', 'MAE Ridge', 'Cumulative Time']]


# At the very last, hope you have enjoyed and got some kind of inspiration (at the very least, inspired of *not* doing something) and I hope to receive some feedback from you.
# 
# Cheers.
