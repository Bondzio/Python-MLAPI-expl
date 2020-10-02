#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
import seaborn as sb
from sklearn.linear_model import Lasso
from sklearn.model_selection import KFold, train_test_split, GridSearchCV, cross_val_predict, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder,MinMaxScaler, normalize,RobustScaler
from sklearn.feature_selection import VarianceThreshold
from scipy import stats
from scipy.stats import norm, skew #for some statistics
import lightgbm as lgb
from scipy.special import boxcox, inv_boxcox, boxcox1p


#loss function
def loss(predictions,observations):
    return np.sqrt(mean_squared_error(np.log(predictions),np.log(observations)))


# In[2]:


train_df = pd.read_csv('../input/train.csv')
train_df.head()


# In[3]:


train_df.shape


# ## feature types

# In[4]:


print ('number of categorial variables:', len(train_df.select_dtypes(object).columns))
print ('number of numerical variables:', len(train_df.select_dtypes([int,float]).columns))


# # outliers
# detection of outliers is very important since some of the models we will work with later are based on linearity and having outliers can break this assumption.
# 
# I will examine the distribution of SalePrice with two continous features

# In[5]:


fig, ax = plt.subplots(1,2,figsize=(15,4))
fig.suptitle('Target variable scatter with other features')
plt.subplot(1,2,1)
sb.scatterplot(train_df['TotalBsmtSF'],train_df['SalePrice'])
plt.subplot(1,2,2)
sb.scatterplot(train_df['GrLivArea'],train_df['SalePrice'])
plt.show()


# In[6]:


# removing outliers recommended
train_df.drop(train_df[(train_df['GrLivArea']>4000)].index,inplace=True)


# In[7]:


fig, ax = plt.subplots(1,2,figsize=(15,4))
fig.suptitle('Target variable scatter with other features')
plt.subplot(1,2,1)
sb.scatterplot(train_df['TotalBsmtSF'],train_df['SalePrice'])
plt.subplot(1,2,2)
sb.scatterplot(train_df['GrLivArea'],train_df['SalePrice'])
plt.show()


# the features look better and closer to linear now

# # target

# In[8]:


target = train_df['SalePrice']
train_df.drop('SalePrice',axis=1,inplace=True)


fig, ax = plt.subplots(1,2,figsize=(15,4))
fig.suptitle('Target variable')
plt.subplot(1,2,1)
sb.boxplot(y = target, width=0.1)
plt.subplot(1,2,2)
target.hist()
plt.show()


# In[9]:


print ('skewness of target:', target.skew(), 'kortosis of target:', target.kurt())


# the target variable is right skewed. log transformation should help fixing skewness and kurtosis

# In[10]:


# log transformation for the target variable 
target_orig = target.copy()
target = np.log(target)
# plotting out transformed target variable
fig, ax = plt.subplots(1,2,figsize=(15,4))
fig.suptitle('Target variable')
plt.subplot(1,2,1)
sb.boxplot(target, width=0.1,orient='v')
plt.subplot(1,2,2)
target.hist()
plt.show()


# In[11]:


print ('after log transformation - skewness of target:', target.skew(), 'kortosis of target:', target.kurt())


# In[12]:


## loading test set and concating with df
test_df = pd.read_csv('../input/test.csv')
concat_df = pd.concat([train_df,test_df], sort = False)
print ('total number of observations:',len(concat_df))


# In[13]:


null_df = concat_df.isnull().sum()
null_df = (null_df[null_df>0]).sort_values(ascending=False)


# In[14]:


null_df


# i will delete columns with more than 300 (~10%) missing values.

# In[15]:


concat_df.drop(null_df[null_df>300].index,axis=1,inplace=True)


# filling missing values in the other columns (according to type of variable and unique values)

# In[16]:


fill_na_none = ['BsmtCond','BsmtExposure','BsmtQual','BsmtFinType2','BsmtFinType1','GarageQual','GarageFinish','GarageCond','GarageType','MasVnrType','MSZoning','Functional','Utilities','Electrical','KitchenQual']
fill_na_zero = ['BsmtFullBath','BsmtHalfBath','BsmtFinSF1','BsmtFinSF2','TotalBsmtSF','BsmtUnfSF','MasVnrArea','GarageCars','GarageArea']                
concat_df[fill_na_none] = concat_df[fill_na_none].fillna('None')
concat_df[fill_na_zero] = concat_df[fill_na_zero].fillna(0)
concat_df['GarageYrBlt'] = concat_df['GarageYrBlt'].fillna(0)
concat_df[['Exterior1st','Exterior2nd']] = concat_df[['Exterior1st','Exterior2nd']].fillna('Other')
concat_df['SaleType'] = concat_df['SaleType'].fillna('Oth')


# In[17]:


# changing object type columns to category and save df
for col in concat_df.select_dtypes('O').columns:
    concat_df[col] = concat_df[col].astype('category')

concat_df['MoSold'] = concat_df['MoSold'].astype('category') #not ordinal
concat_df['YrSold'] = concat_df['YrSold'].astype('category') #not ordinal
concat_df['MSSubClass'] = concat_df['MSSubClass'].astype('category') #not ordinal
concat_df_copy = concat_df.copy()


# In[18]:


concat_df = concat_df_copy.copy()


# In[19]:


concat_df.columns


# 
# constant features :

# In[20]:


len_df = len(concat_df)
constant_A = []
for col in concat_df.columns:
    if concat_df[col].value_counts()[concat_df[col].mode()[0]] > (len_df*0.9):
        constant_A.append(col)
        
concat_df.drop(constant_A,axis=1,inplace=True)


# correlated features:

# In[21]:


corr_matrix = concat_df.select_dtypes([int,float]).corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
to_drop = [c for c in upper.columns if any(upper[c] > 0.8)]   #threshold

concat_df.drop(to_drop,axis=1,inplace=True)


# In[22]:


# fixing skewness 
for col in concat_df.select_dtypes([int,float]).columns:
    if abs(concat_df[col].skew())>0.75:
        concat_df[col] = boxcox1p(concat_df[col],0.15)


# In[23]:


train_df_orig = train_df.copy()
len_train = len(train_df_orig)


# # LASSO

# In[24]:


concat_df = pd.get_dummies(concat_df)
train_df = concat_df[0:len_train]
test_df = concat_df[len_train:]


rs = RobustScaler()
train_df = rs.fit_transform(train_df)
test_df = rs.transform(test_df)


# In[25]:


lasso_model = Lasso(alpha=0.0001,fit_intercept=True,normalize=True)

cross_val_score(lasso_model,X=train_df,y=target,cv=5)


# In[26]:


lasso_model.fit(train_df,target)

preds_lasso = lasso_model.predict(test_df)
preds_lasso = np.exp(preds_lasso)


# # LIGHT GBM

# In[27]:


concat_df = concat_df_copy.copy()
train_df = concat_df[0:len_train]
test_df = concat_df[len_train:]

train_data_lgb = lgb.Dataset(train_df, label = target)

params = {'metric':'mse', 'application':'regression','boosting':'gbdt',
          'feature_fraction':0.7, 'bagging_fraction':0.9, 'learning_rates':0.0001,
           'bagging_freq':1,'max_leaves':9,'min_data_in_leaf':21} 

cv_results = lgb.cv(params, train_data_lgb,nfold=4,stratified=False, num_boost_round=5000,                    early_stopping_rounds=500)

print (cv_results['l2-mean'][-1])


# In[28]:


# building a first level model using all the data

params = {'metric':'mse', 'application':'regression','boosting':'gbdt',
          'feature_fraction':0.7, 'bagging_fraction':0.9, 'learning_rates':0.0001,
           'bagging_freq':1,'max_leaves':9,'min_data_in_leaf':21}

lgb_model = lgb.train(params,
                        train_set = train_data_lgb,
                        num_boost_round=5000)


preds_lgbm = lgb_model.predict(test_df)
preds_lgbm = np.exp(preds_lgbm)


# ### LIGHT GBM (feature importance)

# In[29]:


# a model only with important feature
importance_df = pd.DataFrame({'feature':train_df.columns,'importance':lgb_model.feature_importance()})
important_features = importance_df[importance_df['importance']>0]['feature'].tolist()
#importance_df.sort_values('importance',ascending=False)


# In[30]:


# CV

concat_df = concat_df[important_features]
train_df = concat_df[0:len_train]
test_df = concat_df[len_train:]

train_data_lgb = lgb.Dataset(train_df, label = target)

params = {'metric':'mse', 'application':'regression','boosting':'gbdt',
          'feature_fraction':0.7, 'bagging_fraction':0.7, 'learning_rates':0.0001,
           'bagging_freq':1,'max_leaves':9,'min_data_in_leaf':19}

cv_results = lgb.cv(params, train_data_lgb,nfold=4,stratified=False, num_boost_round=5000,                    early_stopping_rounds=500)

print (cv_results['l2-mean'][-1])


# In[31]:


# building a first level model using important features only

train_data_lgb = lgb.Dataset(train_df, label = target)

params = {'metric':'mse', 'application':'regression','boosting':'gbdt',
          'feature_fraction':0.7, 'bagging_fraction':0.7, 'learning_rates':0.0001,
           'bagging_freq':1,'max_leaves':10,'min_data_in_leaf':21}

lgb_model = lgb.train(params,
                        train_set = train_data_lgb,
                        num_boost_round=5000)

preds_less_features = lgb_model.predict(test_df)
preds_less_features = np.exp(preds_less_features)


# In[32]:


preds_avg = ( preds_lasso + preds_lgbm + preds_less_features) / 3.0
submission_avg = pd.DataFrame({'Id':test_df.index,'SalePrice':preds_avg})
submission_avg.to_csv("submission_avg.csv", index=False)

