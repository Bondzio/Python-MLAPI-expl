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


# import libraries

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV


# 1. # Data Loading and Exploration 

# In[ ]:


#load data
data=pd.read_csv('../input/house-prices-advanced-regression-techniques/train.csv')
data.head(5)


# In[ ]:


data.shape


# In[ ]:


data.describe()


# In[ ]:


data.SalePrice.hist(bins=20)


# In[ ]:


data["SalePrice_log"] = np.log1p(data.SalePrice)
data.drop(columns="SalePrice", inplace=True)
data.SalePrice_log.hist(bins=20)


# ## Exploratory Data Analysis

# ### 1. Basement

# In[ ]:


basement = ['BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1'
            , 'BsmtFinSF1', 'BsmtUnfSF', 'TotalBsmtSF','BsmtFinType2'
            , 'BsmtFinSF2', "BsmtFullBath", "BsmtHalfBath"]
print(*basement, sep=", ")


# ### 1.1 Numerical features

# In[ ]:


def corr_heatmap(columns=None, saleprice=["SalePrice_log"], df=data
                 , figsize=(8,6), vmin=-1, vmax=1, showvalue=True):
    columns = df.columns if columns == None else columns + saleprice
    corr = df[columns].corr()
    plt.figure(figsize=figsize)
    return sns.heatmap(corr, vmin=vmin, vmax=vmax, annot=showvalue)
corr_heatmap(basement)


# In[ ]:


def pairplot(columns, include_sale=True, data=data, kwargs={}):
    if include_sale & ("SalePrice_log" not in columns):
        columns = columns + ["SalePrice_log"]
    sns.pairplot(data=data[columns], **kwargs)
pairplot(basement, kwargs={"markers":"+", "height":1.25})


# 
# The overall-area variable TotalBsmtSF seems the most linearly predictive. If people are interested in area more than other characteristics of the basement (finished, unfinished, etc.), it may be worth removing the other three area variables BsmtFinSF1, BsmtFinSF2 and BsmtUnfSF to save running time and prevent overfitting. At the end, we will test whether dropping these variables is a good idea. In addition, as for BsmtFinSF1 and BsmtFinSF2, let's see if they are more predictive when combined with BsmtFinType.
# 
# It should also be noted that the majority of BsmtHalfBath is 0. Let's convert it to a dummy that evaluates to 0 if there is no basement halfbath and 1 otherwise.

# ### Data cleaning of train Dataset

# In[ ]:


# to visulize null values in data
data.isnull().sum()


# In[ ]:


sns.heatmap(data.isnull(),yticklabels=False,cbar=False)


# In[ ]:


#to display the column names
data.columns


# In[ ]:


#dropping the columns
data.drop(['Alley'], axis=1, inplace=True)
data.drop(['FireplaceQu'], axis=1, inplace=True)
data.drop(['PoolQC'], axis=1, inplace=True)
data.drop(['Fence'], axis=1, inplace=True)
data.drop(['MiscFeature'], axis=1, inplace=True)
data.drop(['GarageYrBlt'], axis=1, inplace=True)


# In[ ]:


#filling the missing data numerical
data['LotFrontage']=data['LotFrontage'].fillna(data['LotFrontage'].mean())
data['MasVnrArea']= data['MasVnrArea'].fillna(data['MasVnrArea'].mean())


# In[ ]:


#filling the missing data discrete
data['MasVnrType']=data['MasVnrType'].fillna(data['MasVnrType'].mode()[0])
data['BsmtQual']=data['BsmtQual'].fillna(data['BsmtQual'].mode()[0])
data['BsmtCond']=data['BsmtCond'].fillna(data['BsmtCond'].mode()[0])
data['BsmtExposure']=data['BsmtExposure'].fillna(data['BsmtExposure'].mode()[0])
data['BsmtFinType1']=data['BsmtFinType1'].fillna(data['BsmtFinType1'].mode()[0])
data['BsmtFinType2']=data['BsmtFinType2'].fillna(data['BsmtFinType2'].mode()[0])
data['Electrical']=data['Electrical'].fillna(data['Electrical'].mode()[0])
data['GarageType']=data['GarageType'].fillna(data['GarageType'].mode()[0])
data['GarageFinish']=data['GarageFinish'].fillna(data['GarageFinish'].mode()[0])
data['GarageQual']=data['GarageQual'].fillna(data['GarageQual'].mode()[0])
data['GarageCond']=data['GarageCond'].fillna(data['GarageCond'].mode()[0])


# In[ ]:


#after Data Cleaning , Checking the data for missing values
data.isnull().sum()


# In[ ]:


sns.heatmap(data.isnull(),yticklabels=False,cbar=False)


# In[ ]:


#copy the train dataframe
train_dataframe=data.copy()


# In[ ]:


train_dataframe.head()


# # Data loading and cleaning with test Dataset

# In[ ]:


data=pd.read_csv('../input/house-prices-advanced-regression-techniques/test.csv')
data.head(5)


# In[ ]:


data.shape


# In[ ]:


# to visulize null values in data
data.isnull().sum()


# In[ ]:


#visualize with heatmap
sns.heatmap(data.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


#to display the column names
data.columns


# In[ ]:


#dropping the columns with more than half of missing values
data.drop(['Alley','FireplaceQu','PoolQC','Fence','MiscFeature','GarageYrBlt'], axis=1, inplace=True)


# In[ ]:


#filling the missing data numerical
data['LotFrontage']=data['LotFrontage'].fillna(data['LotFrontage'].mean())
data['MasVnrArea']= data['MasVnrArea'].fillna(data['MasVnrArea'].mean())
data['BsmtFinSF1']= data['BsmtFinSF1'].fillna(data['BsmtFinSF1'].mean())
data['BsmtFinSF2']= data['BsmtFinSF2'].fillna(data['BsmtFinSF2'].mean())
data['BsmtUnfSF']= data['BsmtUnfSF'].fillna(data['BsmtUnfSF'].mean())
data['TotalBsmtSF']= data['TotalBsmtSF'].fillna(data['TotalBsmtSF'].mean())
data['GarageArea']= data['GarageArea'].fillna(data['GarageArea'].mean())


# In[ ]:


#filling the missing data discrete
data['MSZoning']=data['MSZoning'].fillna(data['MSZoning'].mode()[0])
data['Utilities']=data['Utilities'].fillna(data['Utilities'].mode()[0])
data['Exterior1st']=data['Exterior1st'].fillna(data['Exterior1st'].mode()[0])
data['Exterior2nd']=data['Exterior2nd'].fillna(data['Exterior2nd'].mode()[0])
data['MasVnrType']=data['MasVnrType'].fillna(data['MasVnrType'].mode()[0])
data['BsmtQual']=data['BsmtQual'].fillna(data['BsmtQual'].mode()[0])
data['BsmtCond']=data['BsmtCond'].fillna(data['BsmtCond'].mode()[0])
data['BsmtExposure']=data['BsmtExposure'].fillna(data['BsmtExposure'].mode()[0])
data['BsmtFinType1']=data['BsmtFinType1'].fillna(data['BsmtFinType1'].mode()[0])
data['BsmtFinType2']=data['BsmtFinType2'].fillna(data['BsmtFinType2'].mode()[0])
data['BsmtFullBath']=data['BsmtFullBath'].fillna(data['BsmtFullBath'].mode()[0])
data['BsmtHalfBath']=data['BsmtHalfBath'].fillna(data['BsmtHalfBath'].mode()[0])
data['KitchenQual']=data['KitchenQual'].fillna(data['KitchenQual'].mode()[0])
data['Functional']=data['Functional'].fillna(data['Functional'].mode()[0])
data['GarageType']=data['GarageType'].fillna(data['GarageType'].mode()[0])
data['GarageFinish']=data['GarageFinish'].fillna(data['GarageFinish'].mode()[0])
data['GarageCars']=data['GarageCars'].fillna(data['GarageCars'].mode()[0])
data['GarageQual']=data['GarageQual'].fillna(data['GarageQual'].mode()[0])
data['GarageCond']=data['GarageCond'].fillna(data['GarageCond'].mode()[0])
data['SaleType']=data['SaleType'].fillna(data['SaleType'].mode()[0])
data['SaleCondition']=data['SaleCondition'].fillna(data['SaleCondition'].mode()[0])


# In[ ]:


#after Data Cleaning , Checking the data for missing values
data.isnull().sum()


# In[ ]:


data.shape


# In[ ]:


#visualize with heatmap
sns.heatmap(data.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


data.head(5)


# In[ ]:


#copy the twat dataframe
test_dataframe=data.copy()


# # Merging Train and Test Data and cleaning the combined Dataset

# In[ ]:


#Concatinating train and test Dataset
combined_dataframe=pd.concat([train_dataframe,test_dataframe],axis=0,sort=True)


# In[ ]:


combined_dataframe.isnull().sum()


# In[ ]:


#visualize with heatmap
sns.heatmap(combined_dataframe.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


combined_dataframe.drop(['SaleCondition'], axis=1, inplace=True)


# In[ ]:


#visualize with heatmap
sns.heatmap(combined_dataframe.isna(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


combined_dataframe['SalePrice'].isna().sum()


# In[ ]:


combined_dataframe['SalePrice']= combined_dataframe['SalePrice'].fillna(combined_dataframe['SalePrice'].mean())


# In[ ]:


#visualize with heatmap
sns.heatmap(combined_dataframe.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


combined_dataframe.shape


# # Data preprocessing 

# In[ ]:


#columns with categorical values
columns=['MSZoning','Street','LotShape','LandContour','Utilities','LotConfig','LandSlope','Neighborhood',
         'Condition2','BldgType','Condition1','HouseStyle','SaleType',
        'ExterCond',
         'ExterQual','Foundation','BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2',
        'RoofStyle','RoofMatl','Exterior1st','Exterior2nd','MasVnrType','Heating','HeatingQC',
         'CentralAir',
         'Electrical','KitchenQual','Functional',
         'GarageType','GarageFinish','GarageQual','GarageCond','PavedDrive']


# In[ ]:


#onehotcoding to convert categorical values to numerical

def category_onehot_multcols(multcolumns):
    df_final=combined_dataframe
    i=0
    for fields in multcolumns:
        
        print(fields)
        df1=pd.get_dummies(combined_dataframe[fields],drop_first=True)
        
        combined_dataframe.drop([fields],axis=1,inplace=True)
        if i==0:
            df_final=df1.copy()
        else:
            
            df_final=pd.concat([df_final,df1],axis=1)
        i=i+1
        
       
    print(df_final)    
    df_final=pd.concat([combined_dataframe,df_final],axis=1)
        
    return df_final


# In[ ]:


#calling the onehotcoding function
combined_dataframe = category_onehot_multcols(columns)


# In[ ]:


#shape of dataframe after one hot encoding
combined_dataframe.shape


# In[ ]:


# To remove duplicate column
combined_dataframe =combined_dataframe.loc[:,~combined_dataframe.columns.duplicated()]


# In[ ]:


combined_dataframe.shape


# In[ ]:


from sklearn.model_selection import train_test_split
X=combined_dataframe.drop(['SalePrice'],axis=1)
y=combined_dataframe['SalePrice']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# In[ ]:


print(X_train.shape, y_train.shape)
print (X_test.shape, y_test.shape)


# # scaling the Dataset with MinMaxscaler

# In[ ]:


scaler=MinMaxScaler()
scaler.fit(X_train)
scaled_X_train=scaler.transform(X_train)
scaled_X_test=scaler.transform(X_test)


# # Implementing Random Forest Regressor
# 

# In[ ]:


from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators =1000, random_state=42)
rf.fit(scaled_X_train,y_train)


# In[ ]:


y_pred = rf.predict(scaled_X_test)


# In[ ]:


print("The Train score of random forest: {:.3f}".format(rf.score(scaled_X_train,y_train)))
print("The Test score of random forest: {:.3f}".format(rf.score(scaled_X_test,y_test)))


# In[ ]:


#the result of predicted y value to  actual value of y
df= pd.DataFrame(data=[y_pred,y_test])
df


# # RMSE value for Random Forest Regressor

# In[ ]:


rss=((y_test-y_pred)**2).sum()
mse=np.mean((y_test-y_pred)**2)
print("Final rmse value is =",np.sqrt(np.mean((y_test-y_pred)**2)))


# # Implementing Random Froest Regressor with cross validation

# In[ ]:


from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
cross_val_score(rf,scaled_X_train,y_train,cv=5).mean()





# In[ ]:


param_grid =  {'n_estimators' : np.arange(1000,4000,1000)}
grid = GridSearchCV(RandomForestRegressor(), param_grid=param_grid, cv=5, return_train_score=True)
grid.fit(scaled_X_train, y_train)
print("Best Parameter: {}".format(grid.best_params_))
print("best_cv_score: {:.2f}".format(grid.best_score_))
print("train_score: {:.3f}".format(grid.score(scaled_X_train,y_train)))
print("test_score: {:.3f}".format(grid.score(scaled_X_test,y_test)))



# In[ ]:


param_grid =  {'n_estimators' : np.arange(1000,4000,1000)}
grid = GridSearchCV(RandomForestRegressor(random_state=5,
                                max_depth=9,min_samples_split=10,max_features='sqrt',
                                min_samples_leaf=15), param_grid=param_grid, cv=5, )
grid.fit(scaled_X_train, y_train)
print("Best Parameter: {}".format(grid.best_params_))
print("best_cv_score: {:.2f}".format(grid.best_score_))
print("train_score: {:.3f}".format(grid.score(scaled_X_train,y_train)))
print("test_score: {:.3f}".format(grid.score(scaled_X_test,y_test)))


# In[ ]:


gridsearch_rfr=RandomForestRegressor(random_state=5,n_estimators=2000)

gridsearch_rfr.fit(scaled_X_train, y_train)


# In[ ]:


y_pred = gridsearch_rfr.predict(scaled_X_test)


# In[ ]:


df= pd.DataFrame(data=[y_pred,y_test])
df


# # RMSE value for GridSearch Random Forest Regressor

# In[ ]:


rss=((y_test-y_pred)**2).sum()
mse=np.mean((y_test-y_pred)**2)
print("Final rmse value is =",np.sqrt(np.mean((y_test-y_pred)**2)))


# # Implementing Gradient Boosting Regressor Technique with grid search

# In[ ]:


#grid search for Gradient Boosting
from sklearn.ensemble import GradientBoostingRegressor 
myparam_grid={'n_estimators' : range(1000,4000,1000)}
mygrid = GridSearchCV(estimator = GradientBoostingRegressor(learning_rate=0.05, min_samples_split=10,min_samples_leaf=15,max_depth=4,max_features='sqrt',random_state=5), 
                      param_grid = myparam_grid,iid=False, cv=5)

mygrid.fit(scaled_X_train,y_train)
print("The grid search GradientBoostingRegressor Train Dataset with score: {:.3f}".format(mygrid.score(scaled_X_train,y_train)))
print("The grid search GradientBoostingRegressor Test Dataset with score: {:.3f}".format(mygrid.score(scaled_X_test,y_test)))
print("Best Parameter: {}".format(mygrid.best_params_))
print("best cv accuracy score:{:.2f}".format(mygrid.best_score_))


# In[ ]:


gbm1 = GradientBoostingRegressor(random_state=5,n_estimators=3000,learning_rate=0.05,
                                max_depth=9,min_samples_split=10,max_features='sqrt',
                                min_samples_leaf=15,loss='huber')
gbm1.fit(scaled_X_train, y_train)


# In[ ]:


y_pred = gbm1.predict(scaled_X_test)


# In[ ]:


print("The Train score of random forest: {:.3f}".format(gbm1.score(scaled_X_train,y_train)))
print("The Train score of random forest: {:.3f}".format(gbm1.score(scaled_X_test,y_test)))


# In[ ]:


df= pd.DataFrame(data=[y_pred,y_test])
df


# # RMSE value for GridSearch Gradient Boosting Regressor

# In[ ]:


rss=((y_test-y_pred)**2).sum()
mse=np.mean((y_test-y_pred)**2)
print("Final rmse value is =",np.sqrt(np.mean((y_test-y_pred)**2)))


# In[ ]:


sample=df_Test[['Id','SalePrice']]


# In[ ]:


sample['SalePrice'] = y_pred
sample.to_csv('final_submission.csv', index=False)

