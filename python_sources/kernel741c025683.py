#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df_train = pd.read_csv('../input/house-prices-advanced-regression-techniques/train.csv')


# In[ ]:


df_train.shape


# In[ ]:


total = df_train.isnull().sum().sort_values(ascending=False)
percent = (df_train.isnull().sum()/df_train.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(20)


# In[ ]:


df_train = df_train.drop((missing_data[missing_data['Total'] > 1]).index,1)
df_train = df_train.drop(df_train.loc[df_train['Electrical'].isnull()].index)
df_train.isnull().sum().max() 


# In[ ]:


df_train.shape


# In[ ]:


df_train.sort_values(by = 'GrLivArea', ascending = False)[:2]
df_train = df_train.drop(df_train[df_train['Id'] == 1299].index)
df_train = df_train.drop(df_train[df_train['Id'] == 524].index)


# In[ ]:


df_train.info()


# In[ ]:


df_train.shape


# In[ ]:


test_df = pd.read_csv('../input/house-prices-advanced-regression-techniques/test.csv')


# In[ ]:


test_df.shape


# In[ ]:


total1 = test_df.isnull().sum().sort_values(ascending=False)
#percent = (test_df.isnull().sum()/test_df.isnull().count()).sort_values(ascending=False)
#missing_data1 = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
#missing_data1.head(20)
total1.head(30)


# In[ ]:


test_df.columns


# In[ ]:



test_df.drop(['PoolQC','MiscFeature','Alley','Fence','FireplaceQu','LotFrontage','GarageCond','GarageType','GarageYrBlt','GarageFinish','GarageQual','BsmtExposure','BsmtFinType2','BsmtFinType1','BsmtCond','BsmtQual','MasVnrArea','MasVnrType'],axis = 1,inplace=True)


# In[ ]:


test_df.columns


# In[ ]:


test_df.shape


# In[ ]:


test_df.shape


# In[ ]:


test_df.columns


# In[ ]:


columns=['MSZoning','Street','LotShape','LandContour','Utilities','LotConfig','LandSlope','Neighborhood',
         'Condition2','BldgType','Condition1','HouseStyle','SaleType',
        'SaleCondition','ExterCond',
         'ExterQual','Foundation',
        'RoofStyle','RoofMatl','Exterior1st','Exterior2nd','Heating','HeatingQC',
         'CentralAir',
         'Electrical','KitchenQual','Functional',
         'PavedDrive']


# In[ ]:


len(columns)


# In[ ]:


def category_onehot_multcols(multcolumns):
    df_final=final_df
    i=0
    for fields in multcolumns:
        
        print(fields)
        df1=pd.get_dummies(final_df[fields],drop_first=True)
        
        final_df.drop([fields],axis=1,inplace=True)
        if i==0:
            df_final=df1.copy()
        else:
            
            df_final=pd.concat([df_final,df1],axis=1)
        i=i+1
       
        
    df_final=pd.concat([final_df,df_final],axis=1)
        
    return df_final


# In[ ]:


main_df=df_train.copy()


# In[ ]:


final_df=pd.concat([df_train,test_df],axis=0)


# In[ ]:


final_df.shape


# In[ ]:


final_df.info()


# In[ ]:


tot = final_df.isnull().sum().sort_values(ascending=False)
tot.head(20)


# In[ ]:


final_df['MSZoning']=final_df['MSZoning'].fillna(final_df['MSZoning'].mode()[0])
final_df['Functional']=final_df['Functional'].fillna(final_df['Functional'].mode()[0])
final_df['Utilities']=final_df['Utilities'].fillna(final_df['Utilities'].mode()[0])
final_df['BsmtHalfBath']=final_df['BsmtHalfBath'].fillna(final_df['BsmtHalfBath'].mean())
final_df['BsmtFullBath']=final_df['BsmtFullBath'].fillna(final_df['BsmtFullBath'].mean())
final_df['Exterior2nd']=final_df['Exterior2nd'].fillna(final_df['Exterior2nd'].mode()[0])
final_df['BsmtUnfSF']=final_df['BsmtUnfSF'].fillna(final_df['BsmtUnfSF'].mean())
final_df['BsmtFinSF2']=final_df['BsmtFinSF2'].fillna(final_df['BsmtFinSF2'].mean())
final_df['BsmtFinSF1']=final_df['BsmtFinSF1'].fillna(final_df['BsmtFinSF1'].mean())
final_df['Exterior1st']=final_df['Exterior1st'].fillna(final_df['Exterior1st'].mode()[0])
final_df['SaleType']=final_df['SaleType'].fillna(final_df['SaleType'].mode()[0])
final_df['KitchenQual']=final_df['KitchenQual'].fillna(final_df['KitchenQual'].mode()[0])
final_df['GarageArea']=final_df['GarageArea'].fillna(final_df['GarageArea'].mean())
final_df['GarageCars']=final_df['GarageCars'].fillna(final_df['GarageCars'].mean())
final_df['TotalBsmtSF']=final_df['TotalBsmtSF'].fillna(final_df['TotalBsmtSF'].mean())


# In[ ]:





# In[ ]:


final_df=category_onehot_multcols(columns)


# In[ ]:


final_df.shape


# In[ ]:


final_df.isnull().sum().sort_values(ascending=False)


# In[ ]:


final_df = pd.get_dummies(final_df)


# In[ ]:


final_df =final_df.loc[:,~final_df.columns.duplicated()]


# In[ ]:


final_df.shape


# In[ ]:


df_Train=final_df.iloc[:1457,:]
df_Test=final_df.iloc[1457:,:]


# In[ ]:


df_Train.shape


# In[ ]:


df_Test.shape


# In[ ]:


df_Test.drop(['SalePrice'],axis=1,inplace=True)


# In[ ]:


X_train=df_Train.drop(['SalePrice'],axis=1)
y_train=df_Train['SalePrice']


# In[ ]:


from sklearn.ensemble import RandomForestRegressor
reg = RandomForestRegressor(n_estimators = 500,max_depth=3)
reg.fit(X_train,y_train)
y_p = reg.predict(df_Test)


# In[ ]:


import xgboost
regressor = xgboost.XGBRegressor()


# In[ ]:


regressor.fit(X_train,y_train)


# In[ ]:


y_pred=regressor.predict(df_Test)


# In[ ]:


sub_df=pd.read_csv('../input/house-prices-advanced-regression-techniques/sample_submission.csv')
act = sub_df['SalePrice']


# In[ ]:


from sklearn.metrics import r2_score
r2_score(act,y_p)


# In[ ]:


pred=pd.DataFrame(y_p)
sub_df['SalePrice'] = pred
sub_df.to_csv('submission.csv',index=False)

