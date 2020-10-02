#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import numpy as np
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


df = pd.read_csv('../input/house-prices-advanced-regression-techniques/train.csv')
df_copy = df


# In[ ]:


df.head()


# # Missing Values:

# In[ ]:


df.isnull().sum()[df.isnull().sum() > 0]


# In[ ]:


df['LotFrontage'] = df.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))


# In[ ]:


df_cat = df.select_dtypes(include = 'object')
df_num = df.select_dtypes(exclude = 'object')

df.update(df[df_cat.columns].fillna('na'))
df.update(df[df_num.columns].fillna(0))


# # Correlation:

# In[ ]:


#for categorical variables:

def correlation_ratio(categories, measurements):
    fcat, _ = pd.factorize(categories)
    cat_num = np.max(fcat)+1
    y_avg_array = np.zeros(cat_num)
    n_array = np.zeros(cat_num)
    for i in range(0,cat_num):
        cat_measures = measurements[np.argwhere(fcat == i).flatten()]
        n_array[i] = len(cat_measures)
        y_avg_array[i] = np.average(cat_measures)
    y_total_avg = np.sum(np.multiply(y_avg_array,n_array))/np.sum(n_array)
    numerator = np.sum(np.multiply(n_array,np.power(np.subtract(y_avg_array,y_total_avg),2)))
    denominator = np.sum(np.power(np.subtract(measurements,y_total_avg),2))
    if numerator == 0:
        eta = 0.0
    else:
        eta = np.sqrt(numerator/denominator)
    return eta


# Correlation function from: https://towardsdatascience.com/the-search-for-categorical-correlation-a1cf7f1888c9

# In[ ]:


df.MSSubClass = df.MSSubClass.apply(str)
df_cat = df.select_dtypes(include = 'object')

for i in df_cat.columns:
    data = df[i]
    if (correlation_ratio(data, df.SalePrice) > 0):
        print(i,':', correlation_ratio(data, df.SalePrice))


# In[ ]:


#for numerical variables

corr = df.corr()
corr_list = corr['SalePrice'].sort_values(ascending = False)
corr_list


# In[ ]:


plt.figure(figsize = (10,6))
sns.heatmap(corr)


# In[ ]:


df.drop(['Id', 'Street', 'Utilities'], axis = 1, inplace = True)
df_cat = df.select_dtypes(include = 'object')
df_num = df.select_dtypes(exclude = 'object')


# # EDA:

# In[ ]:


sns.lmplot(data = df, x = 'GrLivArea', y = 'SalePrice')


# In[ ]:


fig, ax = plt.subplots(1,2, figsize = (20,5))
sns.boxplot(data = df, x = 'Neighborhood', y = 'SalePrice', ax = ax[0])
sns.boxplot(data = df, x = 'MSSubClass', y = 'SalePrice', ax = ax[1])


# In[ ]:


fig, ax = plt.subplots(1,2, figsize = (20,5))
sns.boxplot(data = df, x = 'CentralAir', y = 'SalePrice', ax = ax[0])
sns.boxplot(data = df, x = 'PavedDrive',y = 'SalePrice', ax = ax[1])


# # Cross Validation function:

# In[ ]:


def crossval(X, y, reg):
    result = []
    for i in range(10):
        result.append(cross_val_score(reg, X, y).mean())
    return np.mean(result)


# # Transforming categorical features:

# In[ ]:


df = pd.get_dummies(df)


# # Random Forest Regressor:

# In[ ]:


X = df.drop('SalePrice', axis = 1)
y = df.SalePrice
reg = RandomForestRegressor()
crossval(X, y,reg)


# # Outliers:

# In[ ]:


#outliers
sns.lmplot(data = df, x = 'GrLivArea', y = 'SalePrice')


# In[ ]:


df[df.GrLivArea > 4000]['SalePrice']


# In[ ]:


df.drop(1298, inplace = True)
df.drop(523, inplace = True)


# # RFR after outliers treatment:

# In[ ]:


X = df.drop('SalePrice', axis = 1)
y = df.SalePrice
reg = RandomForestRegressor()
crossval(X, y, reg)


# # Normalization:

# In[ ]:


sns.distplot(df.SalePrice)


# In[ ]:


for i in df_num.columns:
    df[i] = np.log1p(df[i])
    df.reset_index(drop=True, inplace=True)
sns.distplot(df.SalePrice)


# # XGB Regressor

# In[ ]:


result = []
for i in np.arange(1,10):
    X_treino, X_teste, Y_treino, Y_teste = train_test_split(X, y, test_size = 0.33, random_state = i)
    xgb = XGBRegressor(learning_rate = 0.08)
    xgb.fit(X_treino, Y_treino, verbose=False)
    score = xgb.score(X_teste,Y_teste)
    result.append(score)
np.mean(result)


# # df_test transformation and submit:

# In[ ]:


df_test = pd.read_csv('../input/house-prices-advanced-regression-techniques/test.csv')

df_copy['test'] = 0
df_test['test'] = 1
feat = pd.concat([df_copy, df_test])



#df_num.drop('SalePrice', axis = 1, inplace = True)
for i in df_num.columns:
    feat[i] = np.log1p(feat[i])
    feat.reset_index(drop=True, inplace=True)
feat.drop(['Id', 'Street', 'Utilities'], axis = 1, inplace = True)

feat.MSSubClass = feat.MSSubClass.apply(str)
feat.update(feat[df_cat.columns].fillna('na'))
feat.update(feat[df_num.columns].fillna(0))
feat['LotFrontage'] = feat.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))
feat = pd.get_dummies(feat)


# In[ ]:


test = feat[feat.test == 1]
train = feat[feat.test == 0]

test.drop('SalePrice', axis = 1, inplace = True)


# In[ ]:


xgb = XGBRegressor(learning_rate = 0.08)
X = train.drop('SalePrice', axis = 1)
y = train.SalePrice
xgb.fit(X, y, verbose=False)
resp = xgb.predict(test)


# In[ ]:


resp = np.expm1(resp)

submit = pd.Series(resp, index=df_test['Id'], name='SalePrice')
submit.to_csv("model.csv", header=True)

