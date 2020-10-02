#!/usr/bin/env python
# coding: utf-8

# In my previous notebook I did a high-level EDA on all the features - checked missing values and explored a list of numeric and categorical attributes that could be useful in training the regression model (you can find my previous notebook here if you are interested: [Predicting House Prices - Data Processing and EDA](https://www.kaggle.com/biyuyang/predicting-house-prices-data-processing-and-eda)). In this notebook, I will explore what's the best model as well as the features that contribute most to the model performances. Below are the topics in this notebook:
# * Write up a data pipeline to execute basic data transformation
# * Batch train some baseline models and pick one for further training
# * Update the data processing pipeline with model tuning and feature selection processes

# In[ ]:


import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 100)

import warnings
warnings.filterwarnings("ignore")


# In[ ]:


houseTrainRaw = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/train.csv')
houseTestRaw = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/test.csv')


# In[ ]:


houseTrain = houseTrainRaw.copy()
houseTest = houseTestRaw.copy()


# ## Data processing
# * Turn built years into ages until current date/time
# * Add in an indicator to show if a record has missing values for certain attributes (make it optional so that can be added/dropped in grid search)
# * Categorize numeric and categorical attributes and process them separately

# In[ ]:


from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from datetime import datetime as dt


# In[ ]:


# add an attribute year age 
class YearsToAges(BaseEstimator, TransformerMixin):
    def __init__(self, yearCols):
        self.cols = yearCols
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        for col in self.cols:
            X[col + 'Age'] = dt.now().year - X[col]
            X = X.drop(columns = col).rename(columns = {col + 'Age': col})
        return X 


# In[ ]:


# track missing columns before imputing if needed
class AddMissingIndicator(BaseEstimator, TransformerMixin):
    def __init__(self, include_missing_cols = False):
        self.include_missing_cols = include_missing_cols
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        if self.include_missing_cols == True:
            cols = X.columns
            for col in cols:
                X[col + '_MissingInd'] = pd.isna(X[col])
            return X
        else:
            return X


# In[ ]:


# select numeric VS categorical attributes
class NumCatSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names, include_missing_cols = False):
        self.attribute_names = attribute_names
        self.include_missing_cols = include_missing_cols
        
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        if self.include_missing_cols == True:
            missingCols = [col + '_MissingInd' for col in self.attribute_names]
            return pd.concat([X[self.attribute_names], X[missingCols]], axis = 1)
        else:
            return X[self.attribute_names]


# In[ ]:


# process numeric attributes
class ProcessNumAttr(BaseEstimator, TransformerMixin):
    def __init__(self, include_missing_cols = False):
        self.include_missing_cols = include_missing_cols
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        imputer = SimpleImputer(strategy = 'median')
        scaler = StandardScaler()
        if self.include_missing_cols == True:
            missingCols = [col for col in X.columns if col.endswith('_MissingInd')]
            cols = X.drop(columns = missingCols).columns
            XImp = imputer.fit_transform(X[cols])
            XScale = scaler.fit_transform(XImp)
            return np.c_[XScale, X[missingCols]]
        
        else:
            XImp = imputer.fit_transform(X)
            XScale = scaler.fit_transform(XImp)
            return XScale


# In[ ]:


# process categorical features
class ProcessCatAttr(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        for col in X.columns:
            X[col] = X[col].astype('object')
            X.loc[X[col].isnull(), col] = 'No Feature'

        encoder = OneHotEncoder(handle_unknown = 'ignore')
        return encoder.fit_transform(X)


# In[ ]:


# put them all together
# categorize columns
IdCol = ['Id']
label = ['SalePrice']
num = [
    'YearBuilt', 'YearRemodAdd', 'GarageYrBlt', 'YrSold', 'LotArea', 'LotFrontage', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 
    'LowQualFinSF', 'GrLivArea', 'BsmtFullBath','BsmtHalfBath', 'FullBath', 'HalfBath', 'TotRmsAbvGrd', 'BedroomAbvGr', 'KitchenAbvGr', 'Fireplaces', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', 
    '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal', 'MoSold', 'OverallQual', 'OverallCond'
]
yrCols = ['YearBuilt', 'YearRemodAdd', 'GarageYrBlt', 'YrSold']
cat = houseTrain.drop(columns = IdCol + label + num, axis = 1).columns

# Numeric attributes pipeline
num_pipeline = Pipeline([
    ('years_to_ages', YearsToAges(yrCols)),
    ('add_missing_ind', AddMissingIndicator(False)),
    ('select_num_attr', NumCatSelector(num, False)),
    ('process_num_attr', ProcessNumAttr(False))
])

# categorical attributes pipeline
cat_pipeline = Pipeline([
    ('add_missing_ind', AddMissingIndicator(False)),
    ('select_cat_attr', NumCatSelector(cat, False)),
    ('process_cat_attr', ProcessCatAttr())
])

full_pipeline = FeatureUnion(
    transformer_list = [
        ('num_pipeline', num_pipeline),
        ('cat_pipeline', cat_pipeline)
    ]
)


# In[ ]:


houseTrainClean = full_pipeline.fit_transform(houseTrain)


# ## Model Training
# * Split data set into train and test
# * Batch train several models and pick the best performer OR try stacking the regressors
# * Grid search with CV on hyperparameter tuning - full data and model pipeline will be used

# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, RidgeCV, Lasso, LassoCV, ElasticNet
from sklearn.svm import SVR, LinearSVR
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error, r2_score 
import time as t


# In[ ]:


def batch_fit_models(xT, yT, xV, yV, models):

    # initiate a dictionary to record model results
    resultCols = [
        'Model', 'Train Time', 
        'Train RMSE', 'Validation RMSE',
        'Train MAE', 'Validation MAE',
        'Train MSLE', 'Validation MSLE',
        'Train R2', 'Validation R2'
    ]

    result = dict([(key, []) for key in resultCols])
    
    # batch train models
    for model_name, model in models.items():
        
        result['Model'].append(model_name)
        
        # train model and record time laps
        trainStart = t.process_time()
        fit = model.fit(xT, yT)
        trainEnd = t.process_time()
        
        # back fit the model on train data
        predTrain = fit.predict(xT)
        
        # fit the model on validation data
        predValid = fit.predict(xV)
        
        # create data for result dict
        result['Train Time'].append(trainEnd - trainStart)
        result['Train RMSE'].append(np.sqrt(mean_squared_error(yT, predTrain)))
        result['Validation RMSE'].append(np.sqrt(mean_squared_error(yV, predValid)))
        result['Train MAE'].append(mean_absolute_error(yT, predTrain))
        result['Validation MAE'].append(mean_absolute_error(yV, predValid))
        result['Train MSLE'].append(mean_squared_log_error(yT, predTrain))
        result['Validation MSLE'].append(mean_squared_log_error(yV, predValid))
        result['Train R2'].append(r2_score(yT, predTrain))
        result['Validation R2'].append(r2_score(yV, predValid))
        
    # turn result dict into a df
    dfResult = pd.DataFrame.from_dict(result)
    
    return dfResult


# In[ ]:


y = houseTrain[label]
xTrain, xValid, yTrain, yValid = train_test_split(houseTrainClean, y, test_size = 0.2, random_state = 1206)


# In[ ]:


modelsToFit = {
    'Linear Regression': LinearRegression(),
    'Ridge': Ridge(alpha = 0.1, random_state = 777),
    'Lasso': Lasso(alpha = 0.1, random_state = 777),
    'Elastic Net': ElasticNet(alpha = 0.1, random_state = 777),
    'Logistic Regression': LogisticRegression(random_state = 777),
    'SVR (linear kernel)': SVR(kernel = 'linear'),
    'Linear SVR': LinearSVR(random_state = 777),
    'Random Forest': RandomForestRegressor(random_state = 777),
    'AdaBoost': AdaBoostRegressor(random_state = 777),
    'GBR': GradientBoostingRegressor(random_state = 777),
    'Stacked Regressors': StackingRegressor(estimators = [('linear_reg', LinearRegression()), ('ridge', Ridge(alpha = 0.1, random_state = 777)), ('lasso', Lasso(alpha = 0.1, random_state = 777)), ('linear_svr', LinearSVR(random_state = 777)), ('linear_kernel_svm', SVR(kernel = 'linear')), ('rf', RandomForestRegressor(random_state = 777)), ('adaboost', AdaBoostRegressor(random_state = 777)), ('gbr', GradientBoostingRegressor(random_state = 777))], final_estimator = ElasticNet(alpha = 0.1, random_state = 777))
}


# In[ ]:


baselineModel = batch_fit_models(xTrain, yTrain, xValid, yValid, modelsToFit)
baselineModel.sort_values(by = 'Validation RMSE')


# The results show that stacked regressors can perform better than individual regressors (although more regularization is probably needed - noticed overfitting from differences in train and validation RMSE). What about adding the missing indicators on each column? 

# In[ ]:


# Numeric attributes pipeline
num_pipeline = Pipeline([
    ('years_to_ages', YearsToAges(yrCols)),
    ('add_missing_ind', AddMissingIndicator(True)),
    ('select_num_attr', NumCatSelector(num, True)),
    ('process_num_attr', ProcessNumAttr(True))
])

# categorical attributes pipeline
cat_pipeline = Pipeline([
    ('add_missing_ind', AddMissingIndicator(True)),
    ('select_cat_attr', NumCatSelector(cat, True)),
    ('process_cat_attr', ProcessCatAttr())
])

full_pipeline = FeatureUnion(
    transformer_list = [
        ('num_pipeline', num_pipeline),
        ('cat_pipeline', cat_pipeline)
    ]
)


# In[ ]:


houseTrainMisInd = full_pipeline.fit_transform(houseTrain)
xTrain2, xValid2, yTrain2, yValid2 = train_test_split(houseTrainMisInd, y, test_size = 0.2, random_state = 1206)


# In[ ]:


baselineModelMisInd = batch_fit_models(xTrain2, yTrain2, xValid2, yValid2, modelsToFit)
baselineModelMisInd.sort_values(by = 'Validation RMSE')


# Hmmm... Looks like we should forget about adding missing indicators?

# ## Feature selection
# * Univariate feature selection
# * Recursive feature elimination
# * Based on model

# In[ ]:


from sklearn.feature_selection import GenericUnivariateSelect, RFECV, SelectFromModel, f_regression, mutual_info_regression


# In[ ]:


def feature_selection_strategy(xT, yT, xV, yV, strats):
    
    # initiate a dictionary to record model results
    resultCols = [
        'Strategy', 'Train Time', 
        'Train RMSE', 'Validation RMSE',
        'Train MAE', 'Validation MAE',
        'Train MSLE', 'Validation MSLE',
        'Train R2', 'Validation R2'
    ]

    result = dict([(key, []) for key in resultCols])
    
    # fit a stacked regression to data
    estimators = [
        ('linear_reg', LinearRegression()), 
        ('ridge', Ridge(alpha = 0.1, random_state = 777)), 
        ('lasso', Lasso(alpha = 0.1, random_state = 777)), 
        ('linear_svr', LinearSVR(random_state = 777)), 
        ('linear_kernel_svm', SVR(kernel = 'linear')), 
        ('rf', RandomForestRegressor(random_state = 777)), 
        ('adaboost', AdaBoostRegressor(random_state = 777)), 
        ('gbr', GradientBoostingRegressor(random_state = 777)) 
    ]

    stackedRegressor = StackingRegressor(estimators = estimators, final_estimator = ElasticNet(alpha = 0.1, random_state = 777))
    
    # batch train models
    for strat_name, strat in strats.items():
        
        result['Strategy'].append(strat_name)
 
        # transform data, train model and record time laps
    
        trainStart = t.process_time()
        selector = strat.fit(xT, yT)
        xTU = selector.transform(xT)
        xVU = selector.transform(xV)
        fit = stackedRegressor.fit(xTU, yT)
        trainEnd = t.process_time()
        
        # back fit the model on train data
        predTrain = fit.predict(xTU)
        
        # fit the model on validation data
        predValid = fit.predict(xVU)
        
        # create data for result dict
        result['Train Time'].append(trainEnd - trainStart)
        result['Train RMSE'].append(np.sqrt(mean_squared_error(yT, predTrain)))
        result['Validation RMSE'].append(np.sqrt(mean_squared_error(yV, predValid)))
        result['Train MAE'].append(mean_absolute_error(yT, predTrain))
        result['Validation MAE'].append(mean_absolute_error(yV, predValid))
        result['Train MSLE'].append(mean_squared_log_error(yT, predTrain))
        result['Validation MSLE'].append(mean_squared_log_error(yV, predValid))
        result['Train R2'].append(r2_score(yT, predTrain))
        result['Validation R2'].append(r2_score(yV, predValid))
        
    # turn result dict into a df
    dfResult = pd.DataFrame.from_dict(result)
    
    return dfResult


# In[ ]:


featureSelectionStrats = {
    'K Best': GenericUnivariateSelect(mutual_info_regression, 'k_best', 20),
    'Percentile': GenericUnivariateSelect(mutual_info_regression, 'percentile', 10),
    'RFECV': RFECV(ElasticNet(alpha = 0.1, random_state = 777), scoring = 'neg_root_mean_squared_error'),
    'From Model': SelectFromModel(ElasticNet(alpha = 0.1, random_state = 777))
}


# In[ ]:


featureSelectionResults = feature_selection_strategy(xTrain, yTrain, xValid, yValid, featureSelectionStrats)


# In[ ]:


featureSelectionResults.sort_values(by = 'Validation RMSE')


# Looks like the best strategy is to select based on a model of choice. The question is then which model should be the best. Will search for the best combination of everything.

# ## Hyperparameter tuning
# * What is the best hyperparameter combination based on no missing indicators and model?
# * Do we want to include missing indicators?
# * Which model should be used for feature selection?

# In[ ]:


from sklearn.model_selection import GridSearchCV, RandomizedSearchCV


# In[ ]:


# Complete data/model pipeline
# put them all together
# categorize columns
IdCol = ['Id']
label = ['SalePrice']
num = [
    'YearBuilt', 'YearRemodAdd', 'GarageYrBlt', 'YrSold', 'LotArea', 'LotFrontage', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 
    'LowQualFinSF', 'GrLivArea', 'BsmtFullBath','BsmtHalfBath', 'FullBath', 'HalfBath', 'TotRmsAbvGrd', 'BedroomAbvGr', 'KitchenAbvGr', 'Fireplaces', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', 
    '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal', 'MoSold', 'OverallQual', 'OverallCond'
]
yrCols = ['YearBuilt', 'YearRemodAdd', 'GarageYrBlt', 'YrSold']
cat = houseTrain.drop(columns = IdCol + label + num, axis = 1).columns

# Numeric attributes pipeline
num_pipeline = Pipeline([
    ('years_to_ages', YearsToAges(yrCols)),
    ('add_missing_ind', AddMissingIndicator(False)),
    ('select_num_attr', NumCatSelector(num, False)),
    ('process_num_attr', ProcessNumAttr(False))
])

# categorical attributes pipeline
cat_pipeline = Pipeline([
    ('add_missing_ind', AddMissingIndicator(False)),
    ('select_cat_attr', NumCatSelector(cat, False)),
    ('process_cat_attr', ProcessCatAttr())
])

data_transformation = FeatureUnion(
    transformer_list = [
        ('num_pipeline', num_pipeline),
        ('cat_pipeline', cat_pipeline)
    ]
)

full_pipeline = Pipeline([
    ('data_transformation', data_transformation),
    ('feature_selection', SelectFromModel(ElasticNet(alpha = 0.1, random_state = 777)))
])


# In[ ]:


# stacked regression model
estimators = [
        ('linear_reg', LinearRegression()), 
        ('ridge', Ridge(random_state = 777)), 
        ('lasso', Lasso(random_state = 777)), 
        ('linear_svr', LinearSVR(random_state = 777)), 
        ('linear_kernel_svm', SVR(kernel = 'linear')), 
        ('rf', RandomForestRegressor(random_state = 777)), 
        ('adaboost', AdaBoostRegressor(random_state = 777)), 
        ('gbr', GradientBoostingRegressor(random_state = 777)) 
    ]

stackedRegressor = StackingRegressor(estimators = estimators, final_estimator = ElasticNet(random_state = 777))

modelParaGrid = {
    'ridge__alpha': [0.0001, 0.001, 0.01, 0.1, 1],
    'lasso__alpha': [0.0001, 0.001, 0.01, 0.1, 1],
    'linear_svr__C': [1, 10, 100, 1000],
    'linear_kernel_svm__C': [1, 10, 100, 1000],
    'rf__n_estimators': [100, 500, 1000],
    'rf__max_depth': [3, 5, 10],
    'adaboost__n_estimators': [50, 100, 500],
    'adaboost__learning_rate': [0.005, 0.01, 0.1, 1],
    'gbr__n_estimators': [100, 500, 1000],
    'gbr__learning_rate': [0.005, 0.01, 0.1, 1],
    'gbr__min_samples_leaf': [5, 10, 100],
    'final_estimator__alpha': [0.001, 0.01, 0.1, 1, 5]
}

randomSearchStackedReg = RandomizedSearchCV(stackedRegressor, modelParaGrid, cv = 5, scoring = 'neg_mean_squared_error', n_iter = 5, verbose = 3, n_jobs = -1)


# In[ ]:


houseTrainFinal = full_pipeline.fit_transform(houseTrain, y)
randomSearchStackedReg.fit(houseTrainFinal, y)


# In[ ]:


modelCVResults = randomSearchStackedReg.cv_results_
for mean_score, params in zip(modelCVResults['mean_test_score'], modelCVResults['params']):
    print(np.sqrt(-mean_score), params)


# In[ ]:


randomSearchStackedReg.best_estimator_


# In[ ]:


# finalize full pipeline with stack regressor
bestStackedRegressor = randomSearchStackedReg.best_estimator_

# Numeric attributes pipeline
num_pipeline = Pipeline([
    ('years_to_ages', YearsToAges(yrCols)),
    ('selector', NumCatSelector(num)),
    ('imputer', SimpleImputer(strategy = 'median')),
    ('scaler', StandardScaler())
])

# categorical attributes pipeline
cat_pipeline = Pipeline([
    ('selector', NumCatSelector(cat)),
    ('imputer', SimpleImputer(strategy = 'constant', fill_value = 'No Feature')),
    ('encoder', OneHotEncoder(handle_unknown = 'ignore'))
])

data_transformation = FeatureUnion(
    transformer_list = [
        ('num_pipeline', num_pipeline),
        ('cat_pipeline', cat_pipeline)
    ]
)

full_pipeline_updated = Pipeline([
    ('data_transformation', data_transformation),
    ('feature_selection', SelectFromModel(ElasticNet(alpha = 0.1, random_state = 777))),
    ('stack_regression', bestStackedRegressor)
])


# ## Submission!
# * Fit the full pipeline on train data
# * Apply it on test data
# * Submit!

# In[ ]:


model = full_pipeline_updated.fit(houseTrain, y)


# In[ ]:


testID = houseTest['Id']
testPred = model.predict(houseTest)


# In[ ]:


submission = pd.concat([testID, pd.DataFrame(testPred)], axis = 1)
submission = submission.rename(columns = {0: 'SalePrice'})
submission.to_csv('house_prices_submission_20200705.csv', index = False)


# In[ ]:


submission

