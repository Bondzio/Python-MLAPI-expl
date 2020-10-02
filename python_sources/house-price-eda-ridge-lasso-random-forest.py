#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge

from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV

import warnings


# In[ ]:


warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


# ## Reading and Understanding Data

# In[ ]:


housing = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/train.csv')
housing_test = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/test.csv')
print(housing.info())
print(housing.shape)


# In[ ]:


housing_test.shape


# In[ ]:


testId = housing_test['Id']


# In[ ]:


housing.head(10)


# In[ ]:


housing.describe().T


# In[ ]:


housing.columns


# ## Data cleaning and EDA
# 
# - Missing Value Treatment

# In[ ]:


missing_info = pd.DataFrame(round(100*(housing.isnull().sum()/len(housing.index)),2))
missing_info = missing_info.loc[missing_info[0]!=0]
missing_info


# In[ ]:


missing_info_test = pd.DataFrame(round(100*(housing_test.isnull().sum()/len(housing_test.index)),2))
missing_info_test = missing_info_test.loc[missing_info_test[0]!=0]
missing_info_test


# In[ ]:


all_data = pd.concat([housing.drop(['SalePrice'],axis=1),housing_test])
all_data.info()


# In[ ]:


#dropping cols with large missing values
missing_val_cols = ['MiscFeature','Fence','PoolQC','Alley','FireplaceQu']
housing.drop(missing_val_cols,inplace=True,axis=1)
housing_test.drop(missing_val_cols,inplace=True,axis=1)
print(housing.shape)
print(housing_test.shape)

missing_info = pd.DataFrame(round(100*(housing.isnull().sum()/len(housing.index)),2))
missing_info = missing_info.loc[missing_info[0]!=0]
missing_info


# #### Treating garage related missing values

# In[ ]:


garageCols = housing.columns[housing.columns.str.startswith('Gar')]
for col in garageCols:
    if (col != "GarageYrBlt") & (col != "GarageArea"):
        print("===={}====".format(col))
        print(housing[col].value_counts(dropna=False))
        print("\n")


# In[ ]:


garageCols = housing_test.columns[housing_test.columns.str.startswith('Gar')]
for col in garageCols:
    if (col != "GarageYrBlt") & (col != "GarageArea"):
        print("===={}====".format(col))
        print(housing_test[col].value_counts(dropna=False))
        print("\n")


# In[ ]:


#checking null values

housing.loc[housing['GarageType'].isnull(),housing.columns.str.startswith('Gar')]


# In[ ]:


housing_test.loc[housing_test['GarageType'].isnull(),housing_test.columns.str.startswith('Gar')]


# #### Inferences:
# - For the properties where garageType is NaN,the value for GarageCars and GarageCars is 0.
# - From this we can infer that these properties do not have a garage of its own. 
# - Therefore, instead of deleting these rows, replacing the NaN values with 'NA' for No Garage as described in the data dictionary
# - For continuous variable 'GarageYrBlt' missing value will be replaced with 0. (Year column will be used to calculate age of the garage if we replace with max date, it will be considered as newly constructed depending on age. Therefore using 0.)

# In[ ]:


housing.loc[housing['GarageType'].isnull(),['GarageType','GarageFinish','GarageQual','GarageCond']] = 'NA'
housing_test.loc[housing_test['GarageType'].isnull(),['GarageType','GarageFinish','GarageQual','GarageCond']] = 'NA'


# In[ ]:


housing_test.loc[housing_test.GarageFinish.isnull()]


# In[ ]:


housing_test.loc[housing_test.GarageFinish.isnull(),'GarageFinish'] = 'Unf'
housing_test.loc[housing_test.GarageCond.isnull(),'GarageCond'] = 'TA'
housing_test.loc[housing_test.GarageQual.isnull(),'GarageQual'] = 'TA'


# In[ ]:


housing_test.groupby(by = 'GarageType')['GarageArea'].mean()


# - Replacing with mean Garage Area of Garage Type 'Detached'

# In[ ]:


housing_test.loc[housing_test.GarageArea.isnull(),'GarageArea'] = 412.2


# In[ ]:


housing_test.loc[housing_test.GarageType == 'Detchd','GarageCars'].mode()


# In[ ]:


housing_test.loc[housing_test.GarageCars.isnull(),'GarageCars'] = 1


# In[ ]:


all_data.GarageFinish.value_counts(dropna=False)


# Replacing GarageYrBlt with YearBuilt values and putting it 0 might skew the age of Garage

# In[ ]:


housing['GarageYrBlt'] = housing[['GarageYrBlt','YearBuilt']].apply(lambda x: x['YearBuilt'] if np.isnan(x['GarageYrBlt']) else x['GarageYrBlt'],axis=1)
housing_test['GarageYrBlt'] = housing_test[['GarageYrBlt','YearBuilt']].apply(lambda x: x['YearBuilt'] if np.isnan(x['GarageYrBlt']) else x['GarageYrBlt'],axis=1)


# #### Treating basement related missing values

# In[ ]:


bsmtCols = housing.columns[housing.columns.str.startswith('Bsmt')]
for col in bsmtCols:
    if (col != "BsmtFinSF1") & (col != "BsmtFinSF2") & (col != "BsmtUnfSF"):
        print("===={}====".format(col))     
        print(housing[col].value_counts(dropna=False))
        print("\n")


# In[ ]:


bsmtCols = housing_test.columns[housing_test.columns.str.startswith('Bsmt')]
for col in bsmtCols:
    if (col != "BsmtFinSF1") & (col != "BsmtFinSF2") & (col != "BsmtUnfSF"):
        print("===={}====".format(col))     
        print(housing_test[col].value_counts(dropna=False))
        print("\n")


# In[ ]:


housing.loc[housing['BsmtQual'].isnull(),housing.columns.str.startswith('Bsmt')]


# There is one row where BsmtCond and BsmtExposure is not available but other basement details are available. Lets keep this row for now and replacing other missing values for basement with NA as No Basement as mentioned in Data Dictionary
# 

# In[ ]:


housing_test.loc[housing_test['BsmtQual'].isnull(),housing_test.columns.str.contains('Bsmt')]


# In[ ]:


housing.loc[housing['BsmtQual'].isnull(),['BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2']] = 'NA'


# In[ ]:


housing_test.loc[((housing_test['BsmtQual'].isnull()) & (housing_test['BsmtCond'].isnull())) ,['BsmtQual']] = 'NA'


# In[ ]:


housing_test.loc[((housing_test['BsmtExposure'].isnull()) & (housing_test['BsmtCond'].isnull())),['BsmtExposure']] = 'NA'


# In[ ]:


housing_test.loc[housing_test['BsmtCond'].isnull(),['BsmtCond']] = 'NA'
housing_test.loc[housing_test['BsmtFinType1'].isnull(),['BsmtFinType1']] = 'NA'
housing_test.loc[housing_test['BsmtFinType2'].isnull(),['BsmtFinType2']] = 'NA'
housing_test.loc[housing_test['BsmtFinSF2'].isnull(),['BsmtFinSF2']] = 0.0
housing_test.loc[housing_test['BsmtFinSF1'].isnull(),['BsmtFinSF1']] = 0.0
housing_test.loc[housing_test['BsmtUnfSF'].isnull(),['BsmtUnfSF']] = 0.0
housing_test.loc[housing_test['TotalBsmtSF'].isnull(),['TotalBsmtSF']] = 0.0
housing_test.loc[housing_test['BsmtFullBath'].isnull(),['BsmtFullBath']] = 0.0
housing_test.loc[housing_test['BsmtHalfBath'].isnull(),['BsmtHalfBath']] = 0.0


# #### Treating BsmtQual

# In[ ]:


all_data['BsmtQual'].value_counts()


# In[ ]:


housing_test[housing_test['BsmtQual'].isnull()]


# In[ ]:


housing_test.loc[(housing_test['Neighborhood']=='IDOTRR') &(housing_test.LotConfig=='Corner') & (housing_test.MSZoning=='C (all)')]


# In[ ]:


housing_test.loc[housing_test['BsmtQual'].isnull(),['BsmtQual']] = 'TA'


# #### Treating BsmtExposure

# In[ ]:


housing.loc[housing['BsmtExposure'].isnull(),housing.columns.str.startswith('Bsmt')]


# In[ ]:


housing_test.loc[housing_test['BsmtExposure'].isnull(),housing_test.columns.str.startswith('Bsmt')]


# In[ ]:


print(housing_test['BsmtExposure'].value_counts())


# It does have other values of basement. Replacing the missing value with No - No Exposure instead of NA as per the data dictionary

# In[ ]:


housing_test.loc[housing_test['BsmtExposure'].isnull(),['BsmtExposure']] = 'No'
housing.loc[housing['BsmtExposure'].isnull(),['BsmtExposure']] = 'No'


# #### Treating BsmtFinType2

# In[ ]:


housing.loc[housing['BsmtFinType2'].isnull(),housing.columns.str.startswith('Bsmt')]


# In[ ]:


housing_test.loc[housing_test['BsmtFinType2'].isnull(),housing_test.columns.str.startswith('Bsmt')]


# In[ ]:


all_data['BsmtFinType2'].value_counts()


# It cant be replaced with 'Unf' as we see that it has BsmtFinSF2 (type 2 finished square feet) value associated.

# In[ ]:


pd.DataFrame(housing.loc[housing['BsmtFinType1']=='GLQ'].groupby(by=['BsmtFinType1','BsmtFinType2'])['BsmtFinSF2'].describe())


# In[ ]:


sns.boxplot(y="BsmtFinSF2",x="BsmtFinType2",data=housing)


# Based on the value of BsmtFinType1 (GLQ), and BsmtFinSF2(479) replacing missing value for BsmtFinType2 with 'BLQ'.

# In[ ]:


housing.BsmtFinType2 = housing.BsmtFinType2.fillna('BLQ')


# #### Treating missing values for `LotFrontage`

# In[ ]:


sns.boxplot(y = housing['LotFrontage'])


# In[ ]:


housing['LotFrontage'].describe(percentiles = (0.25,0.4,0.5,0.75,0.8,0.9))


# In[ ]:


plt.hist(housing['LotFrontage'],bins=50)


# In[ ]:


print(all_data['LotFrontage'].mean())
print(all_data['LotFrontage'].median())


# We noticed that all the values that were missing for `LotFrontage` - (Linear feet of street connected to property) have `Paved` Street (Type of road access to property).
# Therefore, replacing the missing values with the median value of Paved Streets.

# In[ ]:


housing.loc[pd.isnull(housing['LotFrontage']),'LotFrontage'] = 68.0
housing_test.loc[pd.isnull(housing_test['LotFrontage']),'LotFrontage'] = 68.0


# #### Treating Electrical

# In[ ]:


all_data['Electrical'].value_counts(dropna=False)


# In[ ]:


housing.loc[housing['Electrical'].isnull(),'Electrical'] = 'SBrKr'


# #### Treating MasVnrType

# In[ ]:


housing.loc[housing['MasVnrType'].isnull()]


# In[ ]:


housing_test['MasVnrType'].value_counts(dropna=False)


# In[ ]:


housing.loc[housing['MasVnrType']=='None',['MasVnrType','MasVnrArea']].head()


# In[ ]:


#replacing missing MasVnrType with None and MasVnrArea with 0.0
housing.loc[housing['MasVnrArea'].isnull(),['MasVnrArea']] = 0.0
housing.loc[housing['MasVnrType'].isnull(),['MasVnrType']] = 'None'

housing_test.loc[housing_test['MasVnrArea'].isnull(),['MasVnrArea']] = 0.0
housing_test.loc[housing_test['MasVnrType'].isnull(),['MasVnrType']] = 'None'


# In[ ]:


missing_info = pd.DataFrame(housing.isnull().sum())
missing_info = missing_info.loc[missing_info[0]!=0]
missing_info


# In[ ]:


missing_info = pd.DataFrame(housing_test.isnull().sum())
missing_info = missing_info.loc[missing_info[0]!=0]
missing_info


# In[ ]:


housing_test['MSZoning'].value_counts(dropna=False)


# In[ ]:


housing_test.loc[housing_test['MSZoning'].isnull(),'MSZoning'] = 'RL'


# In[ ]:


housing_test[housing_test['Utilities'].isnull()]


# In[ ]:


all_data['Utilities'].value_counts()


# In[ ]:


housing_test.loc[housing_test['Utilities'].isnull(),'Utilities'] = 'AllPub'


# In[ ]:


all_data['Exterior2nd'].value_counts(dropna=False)


# In[ ]:


housing_test['Exterior1st'].value_counts(dropna=False)
housing_test[housing_test['Exterior1st'].isnull()]


# In[ ]:


all_data.loc[((all_data.Neighborhood == 'Edwards') & (all_data.RoofStyle == 'Flat'))]


# - Looking at the above data for neighbourhood 'Edwards' and exterior quality, the missing Exterior value will be replaced by 'BrkComm'

# In[ ]:


housing_test.loc[housing_test['Exterior1st'].isnull(),'Exterior1st'] = 'BrkComm'
housing_test.loc[housing_test['Exterior2nd'].isnull(),'Exterior2nd'] = 'Brk Cmn'


# ### Treating *KitchenQual*

# In[ ]:


all_data['KitchenQual'].value_counts()


# In[ ]:


housing_test.loc[housing_test['KitchenQual'].isnull(),'KitchenQual'] = 'TA'


# ### Treating *Functional*

# In[ ]:


all_data['Functional'].value_counts()


# In[ ]:


housing_test.loc[housing_test['Functional'].isnull(),'Functional'] = 'Typ'


# In[ ]:


all_data['SaleType'].value_counts()


# In[ ]:


housing_test.loc[housing_test['SaleType'].isnull(),'SaleType'] = 'WD'


# In[ ]:


missing_info = pd.DataFrame(housing_test.isnull().sum())
missing_info = missing_info.loc[missing_info[0]!=0]
missing_info


# - Data type check

# In[ ]:


for i in ['MSSubClass','BsmtFullBath','BsmtHalfBath','FullBath','HalfBath','GarageCars']:
  housing[i] = housing[i].astype(str)
  housing_test[i] = housing_test[i].astype(str)

housing['GarageYrBlt'] = housing['GarageYrBlt'].astype(int)
housing_test['GarageYrBlt'] = housing_test['GarageYrBlt'].astype(int)
#housing['OverallQual'] = housing['OverallQual'].astype(str)
#housing['OverallCond'] = housing['OverallCond'].astype(str)


# - Derived Variables

# In[ ]:


yearCols = ['YearBuilt','YearRemodAdd','GarageYrBlt','YrSold']
#Coverting year cols 
housing['AgeBuilt'] = max(all_data['YearBuilt']) - housing['YearBuilt']
housing['AgeRemodAdd'] = max(all_data['YearRemodAdd']) - housing['YearRemodAdd']
housing['AgeGarageBlt'] = max(all_data['GarageYrBlt']) - housing['GarageYrBlt']
housing['AgeSold'] = max(all_data['YrSold']) - housing['YrSold']
housing[['AgeBuilt','AgeRemodAdd','AgeGarageBlt','AgeSold']].describe()
housing.drop(['YearBuilt','YearRemodAdd','GarageYrBlt','YrSold'],axis=1,inplace=True)

housing_test['AgeBuilt'] = max(all_data['YearBuilt']) - housing_test['YearBuilt']
housing_test['AgeRemodAdd'] = max(all_data['YearRemodAdd']) - housing_test['YearRemodAdd']
housing_test['AgeGarageBlt'] = max(all_data['GarageYrBlt']) - housing_test['GarageYrBlt']
housing_test['AgeSold'] = max(all_data['YrSold']) - housing_test['YrSold']
housing_test[['AgeBuilt','AgeRemodAdd','AgeGarageBlt','AgeSold']].describe()
housing_test.drop(['YearBuilt','YearRemodAdd','GarageYrBlt','YrSold'],axis=1,inplace=True)


# ## Exploratory Data Analysis

# In[ ]:


housing.drop(['Id'],axis=1,inplace=True)
housing_test.drop(['Id'],axis=1,inplace=True)
catColsData = housing.select_dtypes(include=['object'])
catCols = catColsData.columns
numCols = list(set(housing.columns) - set(catCols))
len(catCols)


# #### Checking the skewness

# In[ ]:


# checking target variable
housing['SalePrice'].describe(percentiles = (0.25,0.4,0.5,0.75,0.8,0.9,0.95))
plt.hist(housing['SalePrice'],bins=50)


# #### Inference: 
# We notice that the data is skewed. Skewness in the data is because of the presence of outliers.
# To handle these outlier we choose not to delete as the houses with higher sales price are indispensable.
# Tranforming the Values in SalePrice between 0 to 1  will help in normalizing the data without losing any information.
# Lets use sigmoid function to transform our target variable

# In[ ]:


housing['SalePrice'] = housing['SalePrice'].astype(float)
housing['SalePrice'] = np.log(housing['SalePrice'])
housing['SalePrice'].describe()


# In[ ]:


sns.distplot(housing['SalePrice'],bins=50)


# In[ ]:


housing['SalePrice'].head()


# #### Visualizing Categortical Variables

# In[ ]:


len(catCols)


# In[ ]:


def boxplot_catVariables(cols):
    plt.figure(figsize=(20, 40))
    for i in range(0,len(cols)):
        plt.subplot(15,5,i+1)
        sns.boxplot(x = cols[i], y = 'SalePrice', data = housing)
    plt.tight_layout()
    plt.show()
    
boxplot_catVariables(catCols[:-1])


# In[ ]:


def countplot_catVariables(cols):
    plt.figure(figsize=(20, 40))
    for i in range(0,len(cols)):
        plt.subplot(14,3,i+1)
        sns.countplot(x = cols[i], data = housing)
    plt.show()
    
#countplot_catVariables(catCols[:-1])


# In[ ]:


#housing[numCols].corr()


# In[ ]:


plt.figure(figsize=(20, 20))
sns.heatmap(housing[numCols].corr())


# Inferences: Some of the highly correlated variables are '
# - BsmtFinSF1 and BsmtUnfSF
# - TotalRoomsAbvGround and GrLivArea
# - Garage Area and Garage Cars
# - Sale Price is highly corelated
#     - Total rooms Above Ground
#     - Overall Quality
#     - Ground Living Area
#     - Total Bsmnt Surface Area

# In[ ]:


# Dropping highly corelated variables
#housing.drop(['BsmtUnfSF','TotRmsAbvGrd','GarageCars','AgeGarageBlt'],axis=1,inplace=True)
#housing_test.drop(['BsmtUnfSF','TotRmsAbvGrd','GarageCars','AgeGarageBlt'],axis=1,inplace=True)


# ## Data Preparation

# - Create dummy variables for categorical data

# In[ ]:


print(housing.shape)
print(housing_test.shape)


# In[ ]:


catCols


# In[ ]:





# In[ ]:


all_data_dummies = pd.concat([housing[catCols],housing_test[catCols]])


# In[ ]:


all_data_dummies.shape


# In[ ]:


all_data_dummies = pd.get_dummies(all_data_dummies[catCols],drop_first=True)
all_data_dummies.head()


# In[ ]:


housing_test_dummies = all_data_dummies[1460:]
housing_dummies = all_data_dummies[0:1460]


# In[ ]:


housing_dummies.info()


# In[ ]:


print(housing_test_dummies.info())
print(housing_dummies.info())


# In[ ]:


housing = housing.drop(catCols,inplace=False,axis=1)
housing_test = housing_test.drop(catCols,inplace=False,axis=1)

housing.head()


# In[ ]:


housing = pd.concat([housing,housing_dummies],axis=1)
housing_test = pd.concat([housing_test,housing_test_dummies],axis=1)


# In[ ]:


housing.shape


# In[ ]:


X = housing.drop(['SalePrice'],axis=1,inplace=False)
y = housing['SalePrice']
X.head()


# In[ ]:


y.head()


# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=100)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
housing_test_scaled = scaler.transform(housing_test)


# In[ ]:


X_train.shape


# In[ ]:


housing_test.shape


# In[ ]:


X_train.shape


# In[ ]:


X_train[:10]


# In[ ]:


#lm = LinearRegression(alpha=500)
#ridge.fit(X_train,y_train)
#rfe = RFE(ridge,37)
#rfe.fit(X_train,y_train)


# In[ ]:


#rfeCols = list(X.columns[rfe.support_])
#rfeCols


# In[ ]:


#X_rfe = X[rfeCols]
#X_train,X_test,y_train,y_test = train_test_split(X[rfeCols],y,test_size=0.3,random_state=100)


#scaler = StandardScaler()
#X_train = scaler.fit_transform(X_train)
#X_test = scaler.transform(X_test)


# ## Ridge Regression

# In[ ]:


params = {'alpha':[0.1,
 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 3.0, 
 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,20,50,100, 200, 500,600,700,800,1000]}

ridge = Ridge()
folds = KFold(n_splits=5,shuffle=True,random_state=101)

model_cv = GridSearchCV(estimator = ridge,
                       param_grid = params,
                       scoring = 'neg_mean_squared_error',
                       cv = folds,
                       return_train_score = True,
                       verbose =1)

model_cv.fit(X_train,y_train)


# In[ ]:


cv_results = pd.DataFrame(model_cv.cv_results_)
cv_results.head()


# In[ ]:


# plotting mean test and train scoes with alpha 
cv_results['param_alpha'] = cv_results['param_alpha'].astype('int32')

# plotting
plt.plot(cv_results['param_alpha'], np.sqrt(-cv_results['mean_train_score']))
plt.plot(cv_results['param_alpha'], np.sqrt(-cv_results['mean_test_score']))
plt.xlabel('alpha')
plt.ylabel('RMSE')
plt.title("RMSE and alpha")
plt.legend(['train score', 'test score'], loc='upper left')
plt.show()


# In[ ]:


print(model_cv.best_params_['alpha'])
print(np.sqrt(-model_cv.best_score_))


# - Best value of alpha for ridge regression model is 500

# In[ ]:


alpha = model_cv.best_params_['alpha']
ridge = Ridge(alpha = alpha)
ridge.fit(X_train,y_train)
#ridge.coef_
y_train_pred = ridge.predict(X_train) 
y_test_pred = ridge.predict(X_test)
print("Training r2: {}".format(round(r2_score(y_train,y_train_pred),3)))
print("Training RMSE: {}".format(round(np.sqrt(mean_squared_error(y_train,y_train_pred)),3)))
print("Testing r2: {}".format(round(r2_score(y_test,y_test_pred),3)))
print("Testing RMSE: {}".format(round(np.sqrt(mean_squared_error(y_test,y_test_pred)),3)))


# In[ ]:


coefs = pd.Series(ridge.coef_, index = X.columns)
coefs.sort_values(ascending = False).head()


# In[ ]:


plt.figure(figsize=(10,10))
imp_coefs = pd.concat([coefs.sort_values().head(10),
                     coefs.sort_values().tail(10)])
imp_coefs.plot(kind = "barh", color='yellowgreen')

plt.xlabel("ridge coefficient", weight='bold')
plt.title("Feature importance in the ridge Model", weight='bold')
plt.show()


# In[ ]:


final_ridge_pred = np.exp(ridge.predict(housing_test_scaled))
ridge_submission = pd.DataFrame({
        "Id": testId,
        "SalePrice": final_ridge_pred
    })
ridge_submission.to_csv("ridge_submission.csv", index=False)
ridge_submission.head()


# ## Lasso Regression

# In[ ]:


lasso = Lasso()

params = {'alpha':[0.0001,0.0005,0.0011, 0.001, 0.01,0.02,0.03, 0.05, 0.1, 
 0.2]}

# cross validation
model_cv = GridSearchCV(estimator = lasso, 
                        param_grid = params, 
                        scoring= 'neg_mean_squared_error', 
                        cv = folds, 
                        return_train_score=True,
                        verbose = 1)            

model_cv.fit(X_train, y_train) 


# In[ ]:


cv_results = pd.DataFrame(model_cv.cv_results_)
cv_results.head()


# In[ ]:


# plotting mean test and train scoes with alpha 
cv_results['param_alpha'] = cv_results['param_alpha'].astype('float32')

# plotting
plt.plot(cv_results['param_alpha'], np.sqrt(-cv_results['mean_train_score']))
plt.plot(cv_results['param_alpha'], np.sqrt(-cv_results['mean_test_score']))
plt.xlabel('alpha')
plt.ylabel('RMSE')
plt.title("RMSE and alpha")
plt.legend(['train score', 'test score'], loc='upper left')
plt.show()


# In[ ]:


print(model_cv.best_params_)
print(np.sqrt(-model_cv.best_score_))


# In[ ]:


alpha =model_cv.best_params_['alpha']
lasso = Lasso(alpha = alpha)
lasso.fit(X_train,y_train)
y_train_pred = lasso.predict(X_train)
y_test_pred = lasso.predict(X_test)
print("Training r2: {}".format(round(r2_score(y_train,y_train_pred),3)))
print("Training RMSE: {}".format(round(np.sqrt(mean_squared_error(y_train,y_train_pred)),3)))
print("Testing r2: {}".format(round(r2_score(y_test,y_test_pred),3)))
print("Testing RMSE: {}".format(round(np.sqrt(mean_squared_error(y_test,y_test_pred)),3)))


# In[ ]:


sum(lasso.coef_!=0)


# In[ ]:


coefs = pd.Series(lasso.coef_, index = X.columns)
coefs.sort_values(ascending = False).head()


# In[ ]:


plt.figure(figsize=(15,15))

imp_coefs = pd.concat([coefs.sort_values().head(20),
                     coefs.sort_values().tail(16)])
imp_coefs.plot(kind = "barh", color='yellowgreen')

plt.xlabel("Lasso coefficient", weight='bold')
plt.title("Feature importance in the Lasso Model", weight='bold')
plt.show()


# In[ ]:


final_lasso_pred = np.exp(lasso.predict(housing_test_scaled))
lasso_submission = pd.DataFrame({
        "Id": testId,
        "SalePrice": final_lasso_pred
    })
lasso_submission.to_csv("lasso_submission.csv", index=False)
lasso_submission.head()


# ## RandomForestRegressor

# In[ ]:


from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

param_grid = {
    'max_depth': [20,30,40],
    'min_samples_leaf': [4,5,6],
    'min_samples_split': [4,5,6],
    'n_estimators': [100,200],
    'max_features': [100,150,200]
}

rf_reg = GridSearchCV(rf,
                      param_grid, 
                      cv = 5, 
                      n_jobs =10,
                     verbose=1,
                     scoring = 'neg_mean_squared_error')
#rf_reg.fit(X_train, y_train)

#print(rf_reg.best_estimator_)
#best_estimator=rf_reg.best_estimator_


# In[ ]:


rf_model = RandomForestRegressor(
                                  min_samples_leaf =4,
                                  min_samples_split= 4,
                                  n_estimators=200,
                                  max_features=150,
                                  max_depth=20)
rf_model.fit(X_train,y_train)
y_pred_train = rf_model.predict(X_train)
y_pred_test = rf_model.predict(X_test)

print('Root Mean Square Error train = ' + str(np.sqrt(mean_squared_error(y_train, y_pred_train))))
print('Root Mean Square Error test = ' + str(np.sqrt(mean_squared_error(y_test, y_pred_test)))) 


# In[ ]:


final_rf_pred = np.exp(rf_model.predict(housing_test_scaled))
rf_submission = pd.DataFrame({
        "Id": testId,
        "SalePrice": final_rf_pred
    })
rf_submission.to_csv("rf_submission.csv", index=False)
rf_submission.head()


# In[ ]:




