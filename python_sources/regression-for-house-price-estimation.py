#!/usr/bin/env python
# coding: utf-8

# # Regression For House Price Estimation
# 
# In this notebook, I'll try solving the problem of house price estimation given by the Kaggle challenge *House Prices: Advanced Regression Techniques*.
# 
# Let's start by importing some useful librairies.

# In[ ]:


#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('pylab', 'inline')
pylab.rcParams['figure.figsize'] = (10, 6)


# In[ ]:


# Load the data
import os
test_df = pd.read_csv('../input/house-prices-advanced-regression-techniques/train.csv')
train_df = pd.read_csv('../input/house-prices-advanced-regression-techniques/train.csv')


# # Feature selection
# In this part, we'll have a look at the features we have and try to establish which one are relevant in order to obtain the sale price.

# In[ ]:


#Let's have a look at the data we have
train_df.head()


# In[ ]:


# Some columns don't show above so let's have a look at the list of columns
print('There are', len(train_df.columns),'columns.')


# That's 80 potential features, that's a lot. We'll try to narrow it using to criterias (based on the tutorial cited in the references):
# - Not too many null values
# - Correlated with the sale price

# In[ ]:


#Let's look at the number of value per column
null_in_train_csv = train_df.isnull().sum()
null_in_train_csv = null_in_train_csv[null_in_train_csv > 0]
null_in_train_csv.sort_values(inplace=True)
null_in_train_csv.plot.bar();


# We can see that some columns are almost empty. We'll now check the correlation map.

# In[ ]:


sns.heatmap(train_df.corr(), vmax=1, square=True);


# The higher the value, the stronger the correlation. Thanks to this heatmap, we can easily see which variables are correlated, for example the year of construction of the house's garage is strongly linked to the year of construction of the house itself. Let's have a look at the variables that have a positive correlation to the sale price.

# In[ ]:


arr_train_cor = train_df.corr()['SalePrice']
idx_train_cor_gt0 = arr_train_cor[arr_train_cor > 0].sort_values(ascending=False).index.tolist()
arr_train_cor[idx_train_cor_gt0]


# Based on the correlation with sale price and their low inter-correlation, let's chose the following features :
# * **Overall Quality**
# * **GrLivArea**
# * **Garage Cars**
# * **Total Basement Surface**
# * **Construction Year**
# * **FullBath**
# * **Masonry veneer area**
# * **Fireplaces**

# In[ ]:


features = ['SalePrice','OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath', 'YearBuilt', 'Fireplaces']
train_features = train_df[features].copy()


# We'll now look for the empty cells and fill them with the median value of each column.

# In[ ]:


for feature in features:
    train_features[train_features[feature].isnull()]=train_features[feature].median()


# In[ ]:


sns.pairplot(train_features)


# We can see there are a few outliers, values that are extreme and might be wrong, for example, we can see a zero in the year construction. Those extreme values can have a negative impact on training, that's why it's better to remove them.

# In[ ]:


train_no_outliers = train_features.copy()
# Year Built
train_no_outliers = train_no_outliers.drop(train_features[train_features["YearBuilt"] < 1600].index)
# TotalBsmtSF
train_no_outliers = train_no_outliers.drop(train_features[train_features["TotalBsmtSF"] > 5000].index)
#GrLivArea;
to_remove = train_features[(train_features['GrLivArea'] > 4000) & (train_features['SalePrice'] < 200000)].index.tolist()
train_no_outliers = train_no_outliers.drop(to_remove[0])
train_no_outliers = train_no_outliers.drop(to_remove[1]+1)


# In[ ]:


sns.pairplot(train_no_outliers)


# We also note that some of the graphs display parallel lines of points, that's because the values of their column aren't not continuous. These type of values aren't really suitable for some regression models, that's why we'll divide those columns into categorical columns called dummy variables.

# In[ ]:


train_df = train_no_outliers.copy()
dummies = ['FullBath', 'OverallQual', 'Fireplaces', 'GarageCars']
for dummy in dummies:
    dum = pd.get_dummies(train_no_outliers[dummy], prefix=dummy).iloc[:,1:]
    train_df = pd.concat([train_df, dum], axis=1)
train_df = train_df.drop(columns=dummies)
train_df['GarageCars_5'] = 0
train_df['Fireplaces_4'] = 0


# # Training

# In[ ]:


from sklearn.model_selection import train_test_split
random_state = 7

xt_train_test, xt_valid, yt_train_test, yt_valid = train_test_split(train_no_outliers['SalePrice'], train_no_outliers.drop('SalePrice', axis=1), test_size=.2, random_state=random_state)
xt_train, xt_test, yt_train, yt_test = train_test_split(yt_train_test, xt_train_test, test_size=.2, random_state=random_state)

xd_train_test, xd_valid, yd_train_test, yd_valid = train_test_split(train_df['SalePrice'], train_df.drop('SalePrice', axis=1), test_size=.2, random_state=random_state)
xd_train, xd_test, yd_train, yd_test = train_test_split(yd_train_test, xd_train_test, test_size=.2, random_state=random_state)


# In[ ]:


print("number of training set: %d\nnumber of testing set: %d\nnumber of validation set: %d\ntotal: %d" % (len(xt_train), len(xt_test), len(xt_valid), (len(xt_train)+len(xt_test)+len(xt_valid))))


# In[ ]:


def rmse(arr1, arr2):
    return np.sqrt(np.mean((arr1-arr2)**2))


# In[ ]:


from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(xd_train, yd_train)
yd_lm = lm.predict(xd_test)
rmse_linear = rmse(yd_test, yd_lm)
sns.regplot(yd_test, yd_lm)
print("RMSE for Linear Regression Model in sklearn: %.2f" % rmse_linear)


# In[ ]:


import xgboost as xgb
from xgboost import plot_importance
params = {
    'booster': 'gbtree',
    'objective': 'reg:gamma',
    'gamma': 0.1,
    'max_depth': 5,
    'lambda': 3,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'min_child_weight': 3,
    'silent': 1,
    'eta': 0.1,
    'seed': 1000,
    'nthread': 4,
}

plst = params.items()
dtrain = xgb.DMatrix(xt_train, yt_train)
dtest = xgb.DMatrix(xt_test)
num_rounds = 500
xgb_model = xgb.train(plst, dtrain, num_rounds)
yt_xgb = xgb_model.predict(dtest)
rmse_xgb = rmse(yt_test, yt_xgb)
sns.regplot(yt_test, yt_xgb)
print("RMSE for xgboost: %.2f" % rmse_xgb)


# In[ ]:


idx_clean_final = features.copy()
idx_clean_final.remove('SalePrice')
final_clean = test_df[idx_clean_final]
final_clean.head(n=5)


# In[ ]:


dtest_final = xgb.DMatrix(final_clean)
yt_final = xgb_model.predict(dtest_final)
summission = pd.concat([test_df['Id'], pd.DataFrame(yt_final)], axis=1)
summission.columns = ['Id', 'SalePrice']


# In[ ]:


sns.distplot(summission['SalePrice'])


# In[ ]:


summission.to_csv('summission.csv', encoding='utf-8', index = False)


# The score obtained by the submission file is around **0.16**.
# # References
# * https://www.kaggle.com/yiidtw/a-complete-guide-for-regression-problem
# * https://www.kaggle.com/pmarcelino/comprehensive-data-exploration-with-python
# * https://www.kaggle.com/serigne/stacked-regressions-top-4-on-leaderboard
# * https://www.youtube.com/watch?v=0s_1IsROgDc
# * https://www.youtube.com/watch?v=9yTui_LoSOc&t=242s
# * https://www.youtube.com/watch?v=8vwSf0_MYU0&t=179s
