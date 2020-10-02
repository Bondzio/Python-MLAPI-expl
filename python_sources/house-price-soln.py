#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt  # Matlab-style plotting
import seaborn as sns
color = sns.color_palette()
sns.set_style('darkgrid')
import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn #ignore annoying warning (from sklearn and seaborn)

from scipy import stats
from scipy.stats import norm, skew #for some statistics


# In[3]:


#Now let's import and put the train and test datasets in  pandas dataframe

train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')

train.describe()


# In[4]:


print ("Size of train data : {}" .format(train.shape))

print ("Size of test data : {}" .format(test.shape))


# In[5]:


train_ID = train['Id']
test_ID = test['Id']

#Now drop the  'Id' colum since it's unnecessary for  the prediction process.
train.drop("Id", axis = 1, inplace = True)
test.drop("Id", axis = 1, inplace = True)


# In[6]:


print ("Size of train data after dropping Id: {}" .format(train.shape))
print ("Size of test data after dropping Id: {}" .format(test.shape))


# In[7]:


fig, ax = plt.subplots()
ax.scatter(x = train['GrLivArea'], y = train['SalePrice'])
plt.ylabel('SalePrice', fontsize=13)
plt.xlabel('GrLivArea', fontsize=13)
plt.show()


# In[8]:


#Deleting outliers
train = train.drop(train[(train['GrLivArea']>4000) & (train['SalePrice']<300000)].index)


# In[9]:


# most correlated features
corrmat = train.corr()
top_corr_features = corrmat.index[abs(corrmat["SalePrice"])>0.5]
plt.figure(figsize=(10,10))
g = sns.heatmap(train[top_corr_features].corr(),annot=True,cmap="RdYlGn")


# In[10]:


sns.barplot(train.OverallQual,train.SalePrice)


# In[11]:


for dataset in [train, test]:
    
    dataset["PoolQC"] = dataset["PoolQC"].fillna("None")
    dataset["MiscFeature"] = dataset["MiscFeature"].fillna("None")
    dataset["Alley"] = dataset["Alley"].fillna("None")
    dataset["Fence"] = dataset["Fence"].fillna("None")
    dataset["FireplaceQu"] = dataset["FireplaceQu"].fillna("None")
    dataset["LotFrontage"] = dataset.groupby("Neighborhood")["LotFrontage"].transform (lambda x: x.fillna(x.median()))
    for col in ['GarageType', 'GarageFinish', 'GarageQual', 'GarageCond']: dataset[col] = dataset[col].fillna('None')
    for col in ('GarageYrBlt', 'GarageArea', 'GarageCars'): dataset[col] = dataset[col].fillna(0)
    for col in ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF','TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath'): dataset[col] = dataset[col].fillna(0)
    for col in ('BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2'): dataset[col] = dataset[col].fillna('None')  
    dataset["MasVnrType"] = dataset["MasVnrType"].fillna("None")
    dataset["MasVnrArea"] = dataset["MasVnrArea"].fillna(0)
    dataset['MSZoning'] = dataset['MSZoning'].fillna(dataset['MSZoning'].mode()[0])
    
    dataset["Functional"] = dataset["Functional"].fillna("Typ")
    mode_col = ['Electrical','KitchenQual', 'Exterior1st', 'Exterior2nd', 'SaleType']
    for col in mode_col: dataset[col] = dataset[col].fillna(dataset[col].mode()[0])
    dataset['MSSubClass'] = dataset['MSSubClass'].fillna("None")
    


# In[12]:


[df.drop(columns=['Utilities'], inplace = True) for df in [train, test]]


# In[13]:


for df in [train, test]:
    print(df.shape)
    print()
    print(df.isna().sum())


# In[14]:


for dataset in [train, test]:
    
    dataset['MSSubClass'] = dataset['MSSubClass'].apply(str)
    dataset['OverallCond'] = dataset['OverallCond'].astype(str)
    dataset['YrSold'] = dataset['YrSold'].astype(str)
    dataset['MoSold'] = dataset['MoSold'].astype(str)


# In[15]:



from sklearn.preprocessing import LabelEncoder
cols = ('FireplaceQu', 'BsmtQual', 'BsmtCond', 'GarageQual', 'GarageCond', 
        'ExterQual', 'ExterCond','HeatingQC', 'PoolQC', 'KitchenQual', 'BsmtFinType1', 
        'BsmtFinType2', 'Functional', 'Fence', 'BsmtExposure', 'GarageFinish', 'LandSlope',
        'LotShape', 'PavedDrive', 'Street', 'Alley', 'CentralAir', 'MSSubClass', 'OverallCond', 
        'YrSold', 'MoSold')
# process columns, apply LabelEncoder to categorical features
for dataset in [train, test]:
     for c in cols:
        lbl = LabelEncoder() 
        lbl.fit(list(dataset[c].values)) 
        dataset[c] = lbl.transform(list(dataset[c].values))

       
   


# In[16]:


for dataset in [train,test]:
    print('Shape all_data: {}'.format(dataset.shape))


# In[17]:


# Adding total sqfootage feature 
for dataset in [train,test]:
    dataset['TotalSF'] = dataset['TotalBsmtSF'] + dataset['1stFlrSF'] + dataset['2ndFlrSF']


# In[18]:


[train, test] = [pd.get_dummies(data = df) for df in [train, test]]


# In[19]:


print(train.columns.values)
print(train.shape)
print(test.columns.values)
print(test.shape)


# In[20]:


a = train.drop(['SalePrice'],axis=1)
a
a.columns.values
cols = a.columns.values
cols


# In[21]:


cols.shape


# In[22]:


X = a.iloc[:, 0:220].values


# In[23]:


y = train['SalePrice']


# In[24]:


from sklearn.ensemble import RandomForestRegressor


# In[25]:


def feature_select(X, y, cols, cutoff):
    regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
    regressor.fit(X, y)
    feat_imps = pd.concat([pd.DataFrame(cols, columns=['Features']),
                       pd.DataFrame(regressor.feature_importances_, columns=['Importances'])],
                     axis=1)
    feat_imps = feat_imps.sort_values(['Importances'], ascending=False)
    feat_imps['Cumulative Importances'] = feat_imps['Importances'].cumsum()
    feat_imps = feat_imps[feat_imps['Cumulative Importances'] < cutoff]
    return feat_imps['Features'].tolist()


# In[26]:


imp_cols = feature_select(X, y, cols, 0.95)
imp_cols


# In[27]:


X = train[imp_cols].values
X.shape


# In[28]:


y = train['SalePrice']


# In[29]:


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, 
                                                    random_state = 0)


# In[30]:


#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# In[31]:


# Fitting Multi Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression(n_jobs=-1)
regressor.fit(X_train, y_train)


# In[32]:


# Predicting the Test set results
y_pred = regressor.predict(X_test)
y_pred


# In[33]:


from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test,y_pred)
print('MSE: ',mse)
rmse = mse**0.5
print('RMSE: ',rmse)


# In[34]:


# Fitting Random Forest Regression to the dataset
from sklearn.ensemble import RandomForestRegressor
rf_regressor = RandomForestRegressor(n_estimators = 150, random_state = 0)
rf_regressor.fit(X_train, y_train)


# In[36]:


from sklearn.metrics import mean_squared_error

print('RMSE for Random Forest Regression with Selected Features: ',
      mean_squared_error(y_test,rf_regressor.predict(X_test))**0.5)


# In[37]:


# Now we will pass the validation set provided for creating our submission
# Pick the same columns as in X_test
X_validation = test[imp_cols].values
X_validation
X_validation = sc.fit_transform(X_validation)
# Call the predict from the created classifier
y_valid = rf_regressor.predict(X_validation)


# In[40]:


sub = pd.DataFrame()
sub['Id'] = test_ID
my_submission = pd.DataFrame(data={'Id':test_ID, 'SalePrice':y_valid})


# In[41]:


my_submission.to_csv('submission.csv', index = False)


# In[ ]:




