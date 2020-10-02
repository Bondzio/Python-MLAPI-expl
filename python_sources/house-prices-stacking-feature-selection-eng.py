#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import warnings
from sklearn.exceptions import DataConversionWarning, ConvergenceWarning
warnings.filterwarnings(action='ignore')
warnings.filterwarnings(action='ignore', category=DataConversionWarning)
warnings.filterwarnings(action='ignore', category=ConvergenceWarning)


# # House Prices 
# <img src="http://bridgingandcommercial.co.uk/cms/upload/image/dab1369294471_213_126864066.jpg">
# Data set is [here](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data).

# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.set()


# In[ ]:


import pandas as pd
import numpy as np
import os
TRAIN_PATH = '../input/house-prices-advanced-regression-techniques'
TEST_PATH = '../input/house-prices-advanced-regression-techniques'
def load_houses_data(TRAIN_PATH=TRAIN_PATH, TEST_PATH=TEST_PATH):
    train_csv = os.path.join(TRAIN_PATH, 'train.csv')
    test_csv = os.path.join(TEST_PATH, 'test.csv')
    return pd.read_csv(train_csv), pd.read_csv(test_csv)


# In[ ]:


X_train, X_test = load_houses_data()
y_train = X_train['SalePrice']
y_train_first = y_train


# In[ ]:


X_train.head()


# In[ ]:


X_train.info()


# In[ ]:


X_train.std()


# In[ ]:


X_train.hist(figsize=(20, 20), bins=20)
plt.show()


# In[ ]:


X_train['3SsnPorch'].describe()


# In[ ]:


np.unique(X_train['BedroomAbvGr'].values)


# In[ ]:


X_train.groupby('BedroomAbvGr').count()['Id']


# In[ ]:


X_train.groupby('BsmtFullBath').count()['Id']


# In[ ]:


X_train[['TotalBsmtSF', 'BsmtFinSF2', 'BsmtFinSF1', 'BsmtUnfSF']].head()


# In[ ]:


X_train[['OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch']].describe()


# In[ ]:


X_train[['GarageType']].info()


# In[ ]:


X_train.groupby('GarageFinish').count()['Id'] # Let it be in our dataset


# In[ ]:


X_train.corr()['GarageArea']['GarageCars']


# In[ ]:


sns.distplot(X_train['LotArea'], bins=100)


# In[ ]:


X_train.corr()['SalePrice'].sort_values()


# In[ ]:


X_train[['MasVnrArea']].hist(bins=100)


# * should drop id.
# * almost all 3SsnPorch are zero and we can delete it.
# * we can group rooms 5 or more into one single column.
# * can merge full and half bathrooms into one filed name bathroom
# * we can drop two type of finished and have one finished basement feet
# * we can change basement unfinished into a fraction of finished/unfinished (It got bad correlation)
# * can merge porchs into one field.
# * garage year built can be droped and have a single year built for house.
# * we could have just garage area between cars and area.
# * we cad drop kitchen also. becasue a bunch of them are one.
# * can filter Lot Area above 50000 to 50001
# * we **can** drop MSSubClass, OverallCond, YrSold, LowQualFinSF, Id, MiscVal, BsmtHalfBath, BsmtFinSF2, 3SsnPorch, MoSold, PoolArea because of their corrolation
# * It's not important when it was sold. So we drop MoSold and YrSold.
# * Overall Qual is important but Overall cond not!
# * We can add a luxury style field to show having pool or not and other fantasy features.
# * we can have just one of YearRemodAdd or YearBuilt.
# 

# In[ ]:


X_train['YrSold'] = X_train['YrSold'].astype(str)
X_train['MoSold'] = X_train['MoSold'].astype(str)


# In[ ]:


label_attrs = X_train.select_dtypes([object]).columns.values
num_attrs = X_train.select_dtypes([np.int64, np.float64]).columns.values
num_attrs = num_attrs[~(num_attrs == 'SalePrice')]


# ### Normalize Sale Price
# 

# In[ ]:


from sklearn.base import TransformerMixin, BaseEstimator
import seaborn as sns
class Normalize(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        dataset = y_train.copy()
        dataset = np.log1p(dataset)
        return dataset
y_train = Normalize().transform(y_train)
sns.distplot(y_train)


# In[ ]:


X_train_label = X_train[label_attrs]
X_train_num = X_train[num_attrs]


# In[ ]:


from sklearn.preprocessing import StandardScaler
X_train_num_std = pd.DataFrame(StandardScaler().fit_transform(X_train_num), columns=X_train_num.columns)


# ## Colinearity

# In[ ]:


cols = X_train_num_std.columns


# In[ ]:


corr = X_train_num_std.corr()
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))
# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, vmax=1, center=0,vmin=-1 , 
            square=True, linewidths=.005)


# Its hard to select from them by eye. so we filter it!

# In[ ]:


corr = corr.iloc[1:, 1:]
corr = corr.applymap(lambda x : 1 if x > 0.75 else -1 if x < -0.75 else 0)
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))
# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, vmax=1, center=0,vmin=-1 , 
            square=True, linewidths=.005)


# In[ ]:


X_train.corr()['SalePrice'].sort_values()


# * We should drop from orange blocks
# * `GarageCars` should remain, and `GarageArea` should be deleted.
# * `GrLivArea` should remain, and `BedroomAbvGr` and `TotRmsAbvGrd` should be deleted.
# * `TotalBsmtSF` should remain, and `1stFlrSF` should be deleted.
# * `YearBuilt` should remain, and `GarageYrBlt` should be deleted.

# In[ ]:


num_colinear_drop_attrs = ['GarageArea', 'BedroomAbvGr', 'TotRmsAbvGrd', 'GarageYrBlt', '1stFlrSF']


# ## Work With Numbers

# ### Merge FullBath and HalfBath

# In[ ]:


class MergeBath(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self;
    def transform(self, X, y=None):
        X = X.copy()
        X['Bath'] = X['HalfBath'] * X['FullBath']
        X['HalfBath2'] = X['HalfBath'] ** 2
        X['FullBath2'] = X['FullBath'] ** 2
        X['BsmtBath'] = X['BsmtHalfBath'] * X['BsmtFullBath']
        X['BsmtHalfBath2'] = X['BsmtHalfBath'] ** 2
        X['BsmtFullBath2'] = X['BsmtFullBath'] ** 2
        return X
X_num_merged = MergeBath().transform(X_train_num)


# ### Merge BsmntFS and add Unfinished Fraction

# In[ ]:


class MergeBsmntFs(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self;
    def transform(self, X, y=None):
        X = X.copy()
        X['BsmtFinSF'] = X['BsmtFinSF1'] * X['BsmtFinSF2']
        X['BsmtFinSF12'] = X['BsmtFinSF1'] ** 2
        X['BsmtFinSF22'] = X['BsmtFinSF2'] ** 2
        return X
X_num_bsmnt_proved = MergeBsmntFs().transform(X_num_merged)


# ### Merge Porchs 

# In[ ]:


# PolynomialFeatures?
class MergePorches(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self;
    def transform(self, X, y=None):
        X = X.copy()
        X['Porch'] = X['OpenPorchSF'] + X['EnclosedPorch'] + X['3SsnPorch'] + X['ScreenPorch']
        X.drop(['OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch'], axis=1, inplace=True)
        return X
X_num_porch_merged = MergePorches().transform(X_num_bsmnt_proved)


# ### Filter Lot Area above 50000 and Room above 5

# In[ ]:


class FilterLotAreaAndRooms(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self;
    def transform(self, X, y=None):
        X = X.copy()
        X['LotArea'] = X['LotArea'].apply(lambda l: 50001 if l > 50000 else l)
        X['BedroomAbvGr'] = X['BedroomAbvGr'].apply(lambda l: 5 if l > 5 else l)
        return X
X_num_lot_filtered = FilterLotAreaAndRooms().transform(X_num_porch_merged)


# ### Merge Lots
# 

# In[ ]:


class MergeLots(BaseEstimator, TransformerMixin) :
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X = X.copy()
        X['Lot'] = X['LotArea'] + X['LotFrontage']
        X.drop(['LotArea', 'LotFrontage'], axis=1, inplace=True)
        X['Lot'] = X['Lot'].apply(lambda l: 30000 if l > 30000 else l)
        return X
X_num_lots_merged = MergeLots().transform(X_num_lot_filtered)
sns.regplot(x='Lot', y=y_train, data = X_num_lots_merged)


# ### Linearing And Removing Outliers

# In[ ]:


i = 1;
plt.figure(figsize=(20, 35))
for col in X_num_lots_merged.drop(num_colinear_drop_attrs, axis=1):
    if col is not 'Id' and col is not 'SalePrice':
        plt.subplot(10, 4, i)
        sns.regplot(x=col, y=y_train, data=X_num_lots_merged)
        i = i+1


# In[ ]:


num_scatter_drop = ['MSSubClass', 'LowQualFinSF']


# In[ ]:


to_delete_outlires = ['GrLivArea', 'OverallCond', 'BsmtFinSF1', 'GarageCars',
                      '2ndFlrSF', 'YearBuilt', 'YearRemodAdd'] #Think about garage cars


# In[ ]:


from sklearn.impute import SimpleImputer
X_train_num_std_imputed = pd.DataFrame(SimpleImputer().fit_transform(X_train_num_std), 
                                       columns= X_train_num_std.columns)


# In[ ]:


i = 1;
plt.figure(figsize=(20, 35))
for col in X_train_num.drop(num_colinear_drop_attrs, axis=1):
    if col is not 'Id' and col is not 'SalePrice':
        plt.subplot(10, 4, i)
        sns.boxplot(x=X_train[col])
        i = i+1


# In[ ]:


from scipy import stats
import numpy as np
z = pd.DataFrame(np.abs(stats.zscore(X_train_num)), columns=X_train_num.columns)


# In[ ]:


X_train.shape


# In[ ]:


X_train_without_outlier = X_train[(z[to_delete_outlires] < 3).all(axis=1)]


# In[ ]:


y_train_without_outlier = y_train[(z[to_delete_outlires] < 3).all(axis=1)]


# In[ ]:


X_train_without_outlier.shape


# In[ ]:


# sns.distplot(X_train_num_std_imputed.LotFrontage)


# ### Dropping 

# In[ ]:


class DataFrameDropper(BaseEstimator, TransformerMixin):
    def __init__(self, drop_attrs=[]):
        self.drop_attrs = drop_attrs
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X = X.copy()
        X.drop(self.drop_attrs, axis=1, inplace=True, errors='ignore')
        return X


# In[ ]:


num_drop_attrs = num_scatter_drop + num_colinear_drop_attrs
X_num_dropped = DataFrameDropper(num_drop_attrs).transform(X_num_lot_filtered)


# ## Work With Labels

# In[ ]:


X_train_label.info()


# ### Dropping very null attributes

# In[ ]:


label_drop_attrs = ['Alley', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature'] # Think about FireplaceQu
X_label_dropped = DataFrameDropper(label_drop_attrs).transform(X_train_label)


# ### Impute

# In[ ]:


from sklearn.impute import SimpleImputer
X_label_imputed = pd.DataFrame(SimpleImputer(strategy="most_frequent").fit_transform(X_label_dropped.values),
                               columns=X_label_dropped.columns)


# ### Encoding Label

# In[ ]:


from sklearn.preprocessing import OneHotEncoder
class OneHotGoodEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.encoder = OneHotEncoder()
    def fit(self, X, y=None): 
        self.encoder.fit(X)
    def transform(self, X, y=None):
        columns = X.columns
        X_transformed = self.encoder.transform(X).toarray()
        cats = self.encoder.categories_
        i = 0
        labels = []
        for cat in cats:
            for c in cat:
                labels.append(columns[i] + ' : ' + c)
            i = i+1
        return pd.DataFrame(X_transformed, columns=labels)
            


# In[ ]:


encoder = OneHotGoodEncoder()
encoder.fit(X_label_imputed)
X_label_encoded = encoder.transform(X_label_imputed)


# ### Analys labels using p-value
# 

# In[ ]:


from sklearn.feature_selection import f_regression
F, p_value = f_regression(X_label_encoded, y_train)
np.array(X_label_encoded.columns) + " = " + (p_value < 0.05).astype(str) 


# If all classes of a category was false we will delete it.

# In[ ]:


from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder, OneHotEncoder, OrdinalEncoder
encoder = OrdinalEncoder()
X_label_encoded = pd.DataFrame(OrdinalEncoder().fit_transform(X_label_imputed), columns=X_label_imputed.columns)


# ### Analys Labels

# In[ ]:


X_label_analys = X_label_encoded.copy()
X_label_analys['PriceSale'] = y_train.values


# In[ ]:



label_new_drop_attrs = ['Utilities', 'LandSlope', 'YrSold', 'MoSold']
X_label_new_analys = DataFrameDropper(label_new_drop_attrs).transform(X_label_analys)


# ## Create Pipeline 

# In[ ]:


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attrs):
        self.attrs = attrs
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        return X.loc[:, self.attrs]
class LabelBinarizerPipelineFriendly(OneHotEncoder):
    def fit(self, X, y=None):
        """this would allow us to fit the model based on the X input."""
        super(LabelBinarizerPipelineFriendly,self).fit(X)
    def transform(self, X, y=None):
        return super(LabelBinarizerPipelineFriendly, self).transform(X).toarray()
    def fit_transform(self, X, y=None):
        return super(LabelBinarizerPipelineFriendly, self).fit(X).transform(X)


# In[ ]:


from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MultiLabelBinarizer


num_pipeline = Pipeline([
    ('selection', DataFrameSelector(num_attrs)),
    ('merge_bath', MergeBath()),
    ('merge_bsmnt', MergeBsmntFs()),
    ('merge_porch', MergePorches()),
    ('filter', FilterLotAreaAndRooms()),
    ('drop', DataFrameDropper(num_drop_attrs)),
    ('impute', SimpleImputer()),
    ('std_scale', StandardScaler()),
])

label_pipeline = Pipeline([
    ('selection', DataFrameSelector(label_attrs)),
    ('drop', DataFrameDropper(label_new_drop_attrs)),
    ('impute', SimpleImputer(strategy="most_frequent")),
#     ('encode', OrdinalEncoder()), # one hot is  better 
    ('encode', OneHotEncoder(sparse=False, handle_unknown='ignore')),
    ('std_scale', StandardScaler()),
])

full_pipeline = FeatureUnion([
    ('num_pipline', num_pipeline),
    ('label_pipeline', label_pipeline),
])


X_train_cleaned = pd.DataFrame(full_pipeline.fit_transform(X_train_without_outlier))


# In[ ]:


y_train = y_train_without_outlier


# In[ ]:


X_train_cleaned.head()


# ## Train Linear Regression

# In[ ]:


from sklearn.linear_model import LinearRegression
linear_model = LinearRegression()
linear_model.fit(X_train_cleaned, y_train)


# In[ ]:


from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_validate

def analys_model(model):
    some_data = X_train.iloc[:5]
    some_label = y_train.iloc[:5]
    some_data_prepared = full_pipeline.transform(some_data)
    print(f"\x1b[31mPredictions are \033[92m{model.predict(some_data_prepared)}")
    print(f"\x1b[31mLables are \033[92m{list(some_label)}")
    housing_prediction = model.predict(X_train_cleaned)
    scores = cross_validate(model, X_train_cleaned, y_train, scoring="neg_mean_squared_error", cv=3)
    rmse_scores = np.sqrt(-scores['test_score'])
    print(f"\x1b[31mScores : \033[92m{rmse_scores}")
    print(f"\x1b[31mMean : \033[92m{rmse_scores.mean()}")
    print(f"\x1b[31mStandard Deviation : \033[92m{rmse_scores.std()}")


# In[ ]:


analys_model(linear_model)


# ## Train SGD Regressor

# In[ ]:


from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import RandomizedSearchCV
sgd_grid = {
    'n_iter_no_change': [10, 20, 30, 40, 50, 60, 80, 100, 130, 140],
    'eta0': [0.4, 0.2, 0.1, 0.05, 0.03, 0.01, 0.009, 0.004],
}
sgd_model = SGDRegressor()
sgd_best = RandomizedSearchCV(sgd_model, sgd_grid, verbose=2, cv=3,n_jobs=-1, 
                              scoring="neg_mean_squared_error").fit(X_train_cleaned, y_train).best_estimator_

sgd_best
sgd_best.fit(X_train_cleaned, y_train)
analys_model(sgd_best)


# Because sgd is also a linear model but with selection of theta using stochastic gradient it should not go very better than linear regression.

# ## Train Polynomial Regression
# 

# In[ ]:


from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
poly_model = Pipeline([
    ('poly_feature', PolynomialFeatures(degree=2, include_bias=False)),
    ('std_scale', StandardScaler()),
    ('lin_reg', LinearRegression())
])
poly_model.fit(X_train_cleaned, y_train)
analys_model(poly_model)
plt.plot(y_train[:100])
plt.plot(poly_model.predict(X_train_cleaned[:100]), 'r')


# It seems polynomial regression overfitted. With more degrees also it doesnt get better and get very slow. 

# # Regularized Linear Models
# ## TrainRidge Regression

# In[ ]:


from sklearn.linear_model import Ridge 
ridge_grid = {
    'alpha': np.linspace(0, 1, num=500),
    'solver' : ['cholesky'],
}
ridge_model = Ridge()
ridge_best =  RandomizedSearchCV(ridge_model, ridge_grid, verbose=2, cv=3,n_jobs=-1, 
                              scoring="neg_mean_squared_error").fit(X_train_cleaned, y_train).best_estimator_
ridge_best.fit(X_train_cleaned, y_train)
analys_model(ridge_best)


# ## Train Lasso Regression

# In[ ]:


from sklearn.linear_model import Lasso
lasso_grid = {
    'alpha': np.linspace(0, 1e-3, num=1000),
}
lasso_model =  Lasso()
lasso_best =  RandomizedSearchCV(lasso_model, lasso_grid, verbose=2, cv=3,n_jobs=-1, 
                              scoring="neg_mean_squared_error").fit(X_train_cleaned, y_train).best_estimator_
lasso_best.fit(X_train_cleaned, y_train)
analys_model(lasso_best)


# In[ ]:


from sklearn.linear_model import LassoLars
lasso_lars_grid = {
    'alpha': np.linspace(0, 1e-3, num=10000),
    'max_iter' : [int(x) for x in np.linspace(1, 110, num = 100)]
}
lasso_lars_model = LassoLars()
lasso_lars_best =  RandomizedSearchCV(lasso_lars_model, lasso_lars_grid, verbose=2, cv=3,n_jobs=-1, 
                              scoring="neg_mean_squared_error").fit(X_train_cleaned, y_train).best_estimator_
lasso_lars_best.fit(X_train_cleaned, y_train)
analys_model(lasso_lars_best)


# ### Try to boost with gradient method

# In[ ]:


from sklearn.base import clone
class GradientBoostingOtherRegressor(TransformerMixin, BaseEstimator):
    def __init__(self, estimator, n_estimates = 3):
        self.estimator = estimator
        self.estimators = []
        self.n_estimates = n_estimates
    def fit(self, X, y_train=None):
        last_estimator = self.estimator
        last_estimator.fit(X, y_train)
        y = y_train.values
        self.estimators.append(last_estimator)
        for i in range(self.n_estimates):
            y = y - last_estimator.predict(X)
            new_estimator = clone(self.estimator)
            new_estimator.fit(X, y)
            last_estimator = new_estimator
            self.estimators.append(last_estimator)
        return self
    def predict(self, X_test):
        y_pred = sum(tree.predict(X_test) for tree in self.estimators)
        return y_pred


# In[ ]:


gbor = GradientBoostingOtherRegressor(ridge_best, n_estimates=4)
gbor.fit(X_train_cleaned, y_train)
analys_model(gbor)


# ## Train Elastic Net

# In[ ]:


from sklearn.linear_model import ElasticNet
elastic_grid = {
    'alpha': np.linspace(0, 1e-2, num=10000),
    'l1_ratio' : np.linspace(0, 1, num=10)
}
elastic_model = ElasticNet()
elastic_best =  RandomizedSearchCV(elastic_model, elastic_grid, verbose=2, cv=3,n_jobs=-1, 
                              scoring="neg_mean_squared_error").fit(X_train_cleaned, y_train).best_estimator_
elastic_best.fit(X_train_cleaned, y_train)
analys_model(elastic_best)


# ## Train SVM Regression

# In[ ]:


from sklearn.svm import SVR


# ### SVM - Linear

# In[ ]:


from sklearn.model_selection import GridSearchCV
svm_linear_grid = {
    'epsilon' : np.linspace(0, 0.5, num=200),
}
svm_linear_model = SVR(kernel='linear')
svm_linear_best = RandomizedSearchCV(svm_linear_model, svm_linear_grid, verbose=2, cv=3, n_jobs=-1, 
                              scoring='neg_mean_squared_error').fit(X_train_cleaned, y_train).best_estimator_
svm_linear_best.fit(X_train_cleaned, y_train)
analys_model(svm_linear_best)


# ### SVM - Poly

# In[ ]:


svm_poly_grid = {
    'epsilon' : np.linspace(0, 0.5, num=200),
}
svm_poly_model = SVR(kernel='poly')
svm_poly_best = RandomizedSearchCV(svm_poly_model, svm_poly_grid, verbose=2, cv=3, n_jobs=-1, 
                              scoring='neg_mean_squared_error').fit(X_train_cleaned, y_train).best_estimator_
svm_poly_best.fit(X_train_cleaned, y_train)
analys_model(svm_poly_best)


# ## Train Decision Tree Regression

# In[ ]:


from sklearn.tree import DecisionTreeRegressor
dt_model = DecisionTreeRegressor()
dt_model.fit(X_train_cleaned, y_train)

max_features = [int(x) for x in np.linspace(1, 270, num = 30)]
max_depth = [1, 2, 4, 5, 6, 9, 10, 12 , None]
min_samples_leaf = [int(x) for x in np.linspace(1, 10, num = 5)]
random_grid = {'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_leaf': min_samples_leaf}

random_search =  RandomizedSearchCV(estimator = dt_model, param_distributions = random_grid,
                                    n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1, scoring="neg_mean_squared_error")
random_search.fit(X_train_cleaned, y_train) 
dt_best = random_search.best_estimator_
dt_best.fit(X_train_cleaned, y_train)
analys_model(dt_best)


# ### Boost Decison Tree
# 

# In[ ]:


from sklearn.ensemble import AdaBoostRegressor
dt_ada_model = AdaBoostRegressor(dt_best, n_estimators=200, learning_rate=0.5)
dt_ada_model.fit(X_train_cleaned, y_train)
analys_model(dt_ada_model)


# ## Train Random Forest Regression
# 

# In[ ]:


from sklearn.ensemble import RandomForestRegressor
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 2000, num = 5)]
max_features = ['auto', 10, 20, 40, 90, 140, 200, 250]
max_depth = [int(x) for x in np.linspace(1, 1000, num = 20)]
max_depth.append(None)
min_samples_leaf = [5, 10, 15]
bootstrap = [True, False]
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
rf = RandomForestRegressor()


# In[ ]:


random_search =  RandomizedSearchCV(estimator = rf, param_distributions = random_grid,
                                    n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1, scoring="neg_mean_squared_error")
random_search.fit(X_train_cleaned, y_train) 


# In[ ]:


rf_best = random_search.best_estimator_
rf_best.fit(X_train_cleaned, y_train)
analys_model(rf_best)


# ### Boost Random Forest

# * First we use ada boost with our random

# In[ ]:


from sklearn.ensemble import AdaBoostRegressor
dt_ada_model = AdaBoostRegressor(rf_best, n_estimators=10, learning_rate=0.5)
dt_ada_model.fit(X_train_cleaned, y_train)
analys_model(dt_ada_model)


# * Then try a gradient boost with a weak random forest ( max_depth = 5 ); also, we try to find number of estimator with early stoping. 

# In[ ]:


from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
X_t, X_v, y_t, y_v = train_test_split(X_train_cleaned, y_train, random_state=42, test_size=0.2)

gradient_reg = GradientBoostingRegressor(
    n_estimators=1000, 
    random_state=42, 
    learning_rate=0.1, 
    min_samples_split=10,
    max_features='sqrt',
    max_depth=5
)
gradient_reg.fit(X_t, y_t)

errors = [mean_squared_error(y_v, y_pred) for y_pred in gradient_reg.staged_predict(X_v)]
best_n_estimators = np.argmin(errors)

plt.plot(errors)

gradient_best = GradientBoostingRegressor(
    n_estimators=best_n_estimators, 
    random_state=42, 
    learning_rate=0.1, 
    min_samples_split=10,
    max_features='sqrt',
    max_depth=5
)
gradient_best.fit(X_train_cleaned, y_train)

analys_model(gradient_best)

print(f'min estimator {best_n_estimators}')


# # Ensemble Methods
# 
# ## Voting 

# In[ ]:


from sklearn.ensemble import VotingRegressor
voting_model = VotingRegressor(
    estimators=[('ridge', ridge_best), ('lasso', lasso_best), ('elastic', elastic_best), ('svm', svm_linear_best),
               ('rf', gradient_best), ('dt', dt_ada_model)],
    n_jobs=-1
)
voting_model.fit(X_train_cleaned, y_train)
analys_model(voting_model)


# ## Stacking Our Model
# 

# In[ ]:


from sklearn.model_selection import KFold
from sklearn.base import clone, RegressorMixin
class StackingAveragedModels(BaseEstimator, RegressorMixin, TransformerMixin):
    def __init__(self, base_models, meta_model, n_folds=5):
        self.base_models = base_models
        self.meta_model = meta_model
        self.n_folds = n_folds
    def fit(self, X, y=None):
        X = X.values
        y = y.values
        self.base_models_ = [list() for x in self.base_models]
        self.meta_model_ = clone(self.meta_model)
        kfold = KFold(n_splits=self.n_folds, shuffle=True, random_state=42)
        out_of_fold_predictions = np.zeros((X.shape[0], len(self.base_models)))
        for i, model in enumerate(self.base_models):
            for train_index, holdout_index in kfold.split(X, y):
                instance = clone(model)
                self.base_models_[i].append(instance)
                instance.fit(X[train_index], y[train_index])
                y_pred = instance.predict(X[holdout_index])
                out_of_fold_predictions[holdout_index, i] = y_pred
        self.meta_model_.fit(out_of_fold_predictions, y)
        return self
    def get_metafeatures(self, X):
        return np.column_stack([
            np.column_stack([model.predict(X) for model in base_models]).mean(axis=1)
            for base_models in self.base_models_ ])
    def predict(self, X):
        meta_features = np.column_stack([
            np.column_stack([model.predict(X) for model in base_models]).mean(axis=1)
            for base_models in self.base_models_ ])
        return self.meta_model_.predict(meta_features)


# In[ ]:


stacked_averaged_models = StackingAveragedModels(base_models = [gradient_best, dt_ada_model, elastic_best, lasso_lars_best, svm_linear_best],
                                                 meta_model = LinearRegression())
stacked_averaged_models.fit(X_train_cleaned, y_train)


# In[ ]:


meta_features = pd.DataFrame(stacked_averaged_models.get_metafeatures(X_train_cleaned))


# In[ ]:


i = 0;
plt.figure(figsize=(20, 15))
for col in meta_features:
    plt.subplot(3, 3, i+1)
    sns.regplot(x=meta_features[i], y=y_train)
    i = i+1


# In[ ]:


analys_model(stacked_averaged_models)


# # Sumbit Test Set

# In[ ]:


X_test_clean = full_pipeline.transform(X_test)
predictions = stacked_averaged_models.predict(X_test_clean)
final_prediction = pd.DataFrame({'Id': X_test['Id'],
                                'SalePrice': np.expm1(predictions)})


# In[ ]:


final_prediction.to_csv('prediction.csv', index=False)

