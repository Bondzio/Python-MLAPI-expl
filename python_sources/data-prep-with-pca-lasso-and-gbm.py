#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


house_train = pd.read_csv("../input/train.csv")
house_test = pd.read_csv("../input/test.csv")


# ## Data Preparation ##

# This is a very interesting competition with a quantitative target variable. Kaggle has had way too many image competitions, so this is nice to see a traditional model build squeak in again. Since we have a numeric target, it is a good idea to see the distribution of it and to make sure no observations have missing values in the training set.

# In[ ]:


#Lets take a look at the distribution of the target real quick
#Checking the distribution of the target variable
plt.hist(house_train['SalePrice'])


# This distribution has a left skew to it, which is a hint that maybe a LN+1 transformation will help improve our modeling process. Below is the graph of the newly transformed target.

# In[ ]:


house_train['SalePrice'] = np.log1p(house_train['SalePrice'])
plt.hist(house_train['SalePrice'])


# This distribution has that bell shape curved Statisticians love and looks pretty good. This target variable will be a lot easier to model off of and then transform back at the end.

# **Setting up the numeric and categorical feature datasets**

# In[ ]:


#This step puts the saleprice and ID at front of data
full = pd.concat([house_train,house_test])
cols = list(full)
cols.insert(0, cols.pop(cols.index('Id')))
cols.insert(1, cols.pop(cols.index('SalePrice')))
full = full.ix[:,cols]
#creating a SalePrice column that will be attached after all feature engineering 
saleprice = full.ix[:,1]

#separating numeric and categorical features into two datasets
numeric_feats = full.select_dtypes(include=['int','int64','float','float64'])
cat_feats = full.select_dtypes(include=['object'])


# In[ ]:


#Drop SalePrice from numeric Feats so we do not impute by accident
numeric_feats = numeric_feats.drop('SalePrice',axis=1)

#We will first begin taking care of numeric features. 
miss_check = numeric_feats.isnull().sum()
print(miss_check)


# In[ ]:


#Lets take a look at GarageYrBlt, LotFrontage, and MasVnrArea
numeric_feats[['GarageYrBlt','LotFrontage', 'MasVnrArea']].describe()
#Seems like GarageYrBlt has a weird extreme value so we will cap that variable
numeric_feats['GarageYrBlt'] = np.where(numeric_feats['GarageYrBlt'] > 2010, 2010, numeric_feats['GarageYrBlt'])

#Looks like we should be okay imputing the median for all missing numeric features
#We will make an indicator for missing values of GarageYrBlt, LotFrontage and MasVnrArea
miss_list = ['GarageYrBlt','LotFrontage','MasVnrArea']
name_list = ['miss_garageyrblt','miss_LF','miss_MasVnrArea']
for i, j in zip(miss_list[0:3],name_list[0:3]):
    numeric_feats[j] = np.where(numeric_feats[i].isnull(), 1, 0)
    
numeric_feats=numeric_feats.fillna(numeric_feats.median())
miss_check = numeric_feats.isnull().sum()


# In[ ]:


#Doing a final check to make sure there are no more numeric variables that should be categorical
cols_list = numeric_feats.columns.tolist()
check = {}
for i in cols_list:
    check[i] = numeric_feats[i].value_counts()

#Checking scatter plots of low distinct count variables
numeric_feats  = pd.concat([saleprice,numeric_feats],axis=1)
numeric_train = numeric_feats[~numeric_feats['SalePrice'].isnull()]
numeric_test = numeric_feats[numeric_feats['SalePrice'].isnull()]


# **Flooring and Capping numeric features**

# In[ ]:


#BedroomAbvGr
sns.regplot(x='BedroomAbvGr', y='SalePrice', data=numeric_train, color='Red')
numeric_feats['BedroomAbvGr'] = np.where(numeric_feats['BedroomAbvGr'] > 4, 4, numeric_feats['BedroomAbvGr'])


# In[ ]:


#BsmtFullBath
sns.regplot(x='BsmtFullBath', y='SalePrice', data=numeric_train, color='Red')
numeric_feats['BsmtFullBath'] = np.where(numeric_feats['BsmtFullBath'] > 2, 2, numeric_feats['BsmtFullBath'])


# In[ ]:


#BsmtHalfBath
sns.regplot(x='BsmtHalfBath', y='SalePrice', data=numeric_train, color='Red')
numeric_feats['BsmtHalfBath'] = np.where(numeric_feats['BsmtHalfBath'] > 1, 1, numeric_feats['BsmtHalfBath'])


# In[ ]:


#FullBath
sns.regplot(x='FullBath', y='SalePrice', data=numeric_train, color='Red')
numeric_feats['FullBath'] = np.where(numeric_feats['FullBath'] < 1, 1, numeric_feats['FullBath'])


# In[ ]:


#GarageCars
sns.regplot(x='GarageCars', y='SalePrice', data=numeric_train, color='Red')
numeric_feats['GarageCars'] = np.where(numeric_feats['GarageCars'] > 3, 3, numeric_feats['GarageCars'])


# In[ ]:


#HalfBath
sns.regplot(x='HalfBath', y='SalePrice', data=numeric_train, color='Red')
numeric_feats['HalfBath'] = np.where(numeric_feats['HalfBath'] > 1, 1, numeric_feats['HalfBath'])


# In[ ]:


#KitchenAbvGr
sns.regplot(x='KitchenAbvGr', y='SalePrice', data=numeric_train, color='Red')
numeric_feats['KitchenAbvGr'] = np.where(numeric_feats['KitchenAbvGr'] < 1, 1, numeric_feats['KitchenAbvGr'])


# In[ ]:


#Checking to make sure the changes were implemented
numeric_feats[['BedroomAbvGr','BsmtFullBath','BsmtHalfBath','Fireplaces','FullBath','GarageCars','HalfBath','KitchenAbvGr']].describe()


# In[ ]:


#Making the numeric training and test again
numeric_train = numeric_feats[~numeric_feats['SalePrice'].isnull()]
numeric_test = numeric_feats[numeric_feats['SalePrice'].isnull()]

#Making X-train and x_test for numerics
#Making xtrain and y values
id_sal_values = numeric_feats.ix[:,[0,1]]
numeric_feats = numeric_feats.drop(['Id','SalePrice'], axis=1)
x_train_numeric = numeric_feats[:numeric_train.shape[0]]
x_test_numeric = numeric_feats[numeric_train.shape[0]:]
y_train = numeric_train.SalePrice


# **Categorical Feature Clean up**

# In[ ]:


#Now we can check the frequency of distinct values of each categorical variable
cols_list =  cat_feats.columns.tolist()
freq = {}
for i in cols_list:
    freq[i] = cat_feats[i].value_counts(dropna=False)


# In[ ]:


#Drop bad variables
cat_feats = cat_feats.drop(['Street','Alley','Utilities','PoolQC'],axis=1)


# In[ ]:


#Lets clean up the missing values of the categorical features
import itertools as it
cols_list =  cat_feats.columns.tolist()
for i in it.chain(cols_list[0:8],cols_list[10:11], cols_list[14:16],cols_list[18:24],cols_list[26:29],cols_list[31:37]):
    cat_feats[i]=np.where(cat_feats[i].isnull(),'NA',cat_feats[i])

#These variables below had so little missing values that we just imputed the most common level
cat_feats['Electrical']=np.where(cat_feats['Electrical'].isnull(), 'SBrkr', cat_feats['Electrical'])
cat_feats['Exterior1st']=np.where(cat_feats['Exterior1st'].isnull(), 'Other', cat_feats['Exterior1st'])
cat_feats['Exterior2nd']=np.where(cat_feats['Exterior2nd'].isnull(), 'Other', cat_feats['Exterior2nd'])
cat_feats['KitchenQual']=np.where(cat_feats['KitchenQual'].isnull(), 'TA', cat_feats['KitchenQual'])
cat_feats['Functional']=np.where(cat_feats['Functional'].isnull(), 'Typ', cat_feats['Functional'])
cat_feats['SaleType']=np.where(cat_feats['SaleType'].isnull(), 'Oth', cat_feats['SaleType'])
cat_feats['MSZoning']=np.where(cat_feats['MSZoning'].isnull(), 'RL', cat_feats['MSZoning'])

miss_check = cat_feats.isnull().sum()


# In[ ]:


#Getting the dummy variables
cat_feats = pd.get_dummies(cat_feats)
#Setting up train and test categorical features for PCA
cat_feats_train = cat_feats[0:1460]
cat_feats_test = cat_feats[1460:2919]

x_train_cats = cat_feats[:cat_feats_train.shape[0]]
x_test_cats = cat_feats[cat_feats_train.shape[0]:]


# ## Principal Component Analysis ##
# 
# After dummy coding, he amount of categorical features is way too large for the number of observations we have available to model. A great way to reduce the number of variables you have in this situation is principal component analysis. I am choosing not to do this on the numeric features because there are a lot of them that are linearly related with our target variable.

# In[ ]:


#PCA on the categorical data
from sklearn.decomposition import PCA
pca = PCA(n_components=0.95)

x_train_cats_pca=pca.fit_transform(x_train_cats)
x_test_cats_pca=pca.transform(x_test_cats)

def col_list(n):
    results = []
    i=1
    while i <= n:
        results.append('Component_'+str(i))
        i += 1
    return results
col_names=col_list(93)

x_train_cats_pca=pd.DataFrame(data=x_train_cats_pca,columns=col_names)
x_test_cats_pca=pd.DataFrame(data=x_test_cats_pca,columns=col_names)


# In[ ]:


#Concatenating the categorical and numeric features
x_train = pd.concat([x_train_numeric,x_train_cats_pca],axis=1)
x_test = pd.concat([x_test_numeric,x_test_cats_pca],axis=1)


# ## Modeling Time!!! ##

# I am going to use some aspects of other kernels made for this competition. My creative part was doing PCA on the categorical features only. 

# In[ ]:


#Define the RMSE function to evaluate models
from sklearn.cross_validation import cross_val_score
def rmse_cv(model):
    rmse=np.sqrt(-cross_val_score(model, x_train, y_train, scoring='mean_squared_error', cv=5))
    return(rmse)


# **Lasso Regression**

# In[ ]:


from sklearn.linear_model import LassoCV
model_lasso = LassoCV(alphas = [1,0.1,0.001,0.0005]).fit(x_train,y_train)
#Finding out which coefficients were taken from lasso
coef = pd.Series(model_lasso.coef_, index=x_train.columns)
print('Lasso picked' + str(sum(coef != 0)) + 'variables and eliminated the other' + str(sum(coef == 0)) + 'variables')
#Picking out the important coefficents through lasso
imp_coef = pd.concat([coef.sort_values().head(10), coef.sort_values().tail(10)])
print(imp_coef)
matplotlib.rcParams['figure.figsize'] = (10.0,10.0)
imp_coef.plot(kind='barh')
plt.title('Coefficients in the Lasso Model')


# It seems like a lot of the principal components are pretty powerful for the lasso regression procedure.

# In[ ]:


rmse_cv(model_lasso).mean()


# **Gradient Boosting Machine**

# In[ ]:


from sklearn.ensemble import GradientBoostingRegressor
from sklearn.grid_search import GridSearchCV
#Finding best n_estimators
#param_test1 = {'n_estimators': [180,185,190]}#180
#Finding best min_samples_split
#param_test2 = {'min_samples_split': [2,3,4]}#2
#Finding best max_depth
#param_test3 = {'max_depth': [3,4,5]}#3
#gsearch1 = GridSearchCV(estimator=GradientBoostingRegressor(learning_rate=0.1,n_estimators=180), param_grid=param_test3, scoring='mean_squared_error', n_jobs=4, iid=False, cv=5)
#gsearch1.fit(x_train, y_train)
#gsearch1.grid_scores_, gsearch1.best_params_,gsearch1.best_score_
gbm_model = GradientBoostingRegressor(n_estimators=180).fit(x_train,y_train)


# I commented out the gridsearch stuff I did because I did that in a tedious manner not suitable for presenting.

# In[ ]:


rmse_cv(gbm_model).mean()


# Clearly the Gradient boosted machine is performing better but for this submission I will take the average of the two modeling methods and submit it for results!

# In[ ]:


lasso_preds=np.expm1(model_lasso.predict(x_test))
gbm_preds = np.expm1(gbm_model.predict(x_test))
sns.regplot(lasso_preds,gbm_preds,color='blue')


# Lets take the average and create the submission file.

# In[ ]:


y_preds = (lasso_preds+gbm_preds) / 2
final_product = pd.DataFrame({'SalePrice':y_preds,'id':house_test.Id })
final_product.to_csv('GBM_Lasso.csv', index=False)


# ## Conclusions ##
# 
# It appears this model performed pretty well and got me an RMSE score of 0.123(something something). This modeling technique got me to the top 36% of this competition which isn't anything to brag about, but I think it teaches a good lesson about modeling with PCA to reduce the number of features and to avoid overfitting. 
# 
# Note: PCA in the real world is hard because the components will be different on new model building datasets. Modelers need to make sure they know the equations for each component and can use those on new data to remake the principal components!
