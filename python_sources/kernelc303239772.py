#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data_train= pd.read_csv("../input/train.csv")
data_test=pd.read_csv("../input/test.csv")


# In[ ]:


data_train.head()


# In[ ]:


data_train.info()


# In[ ]:


plt.figure(figsize=(14,10))
sns.heatmap(data_train.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


sns.distplot(data_train['SalePrice'],bins=30)
data_train['SalePrice'].skew()


# In[ ]:


data_train['SalePrice']=np.log(data_train['SalePrice'])
sns.distplot(data_train['SalePrice'],bins=30)
data_train['SalePrice'].skew()


# In[ ]:


data_train.drop('Id',axis=1,inplace=True)
data_test.drop('Id',axis=1,inplace=True)
numerical_feats = data_train.dtypes[data_train.dtypes != "object"].index
print("Number of Numerical features: ", len(numerical_feats))

categorical_feats = data_train.dtypes[data_train.dtypes == "object"].index
print("Number of Categorical features: ", len(categorical_feats))


# In[ ]:


data_train[numerical_feats].head()


# In[ ]:


total = data_train.isnull().sum()
missing_data = data_train.isnull().sum()/len(data_train)*100
missing_data = missing_data[missing_data>0]
total= total[total>0]
total.sort_values(inplace=True, ascending=False)
missing_data.sort_values(inplace=True, ascending=False)
missing_data


# In[ ]:



missing_data = pd.concat([total, missing_data], axis=1, keys=['Total', 'Percent'])
print(missing_data)


# In[ ]:


missing_data.index


# In[ ]:


cols_fillna = ['PoolQC','MiscFeature','Alley','Fence','MasVnrType','FireplaceQu',
               'GarageQual','GarageCond','GarageFinish','GarageType', 'Electrical',
               'BsmtExposure','BsmtCond','BsmtQual','BsmtFinType1','BsmtFinType2']

# replace 'NaN' with 'None' in these columns
for col in cols_fillna:
    data_train[col].fillna('None',inplace=True)
    data_test[col].fillna('None',inplace=True)


# In[ ]:


total = data_train.isnull().sum()
missing_data = data_train.isnull().sum()/len(data_train)*100
missing_data = missing_data[missing_data>0]
total= total[total>0]
total.sort_values(inplace=True, ascending=False)
missing_data.sort_values(inplace=True, ascending=False)
missing_data


# In[ ]:


data_train.fillna(data_train.mean(), inplace=True)
data_test.fillna(data_test.mean(), inplace=True)


# In[ ]:


data_train.head()


# In[ ]:


data_test.head()


# In[ ]:


plt.figure(figsize=(6,6))
sns.heatmap(data_train.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


plt.figure(figsize=(6,6))
sns.heatmap(data_test.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# In[ ]:


categorical_feats


# In[ ]:


from sklearn.preprocessing import LabelEncoder
for c in categorical_feats:
    lbl = LabelEncoder() 
    lbl.fit(list(data_train[c].values)) 
    data_train[c] = lbl.transform(list(data_train[c].values))
    


# In[ ]:


for c in categorical_feats:
    lbl.fit(list(data_test[c].values))
    data_test[c]=lbl.transform(list(data_test[c].values))


# In[ ]:


corr = data_train.corr()
top_feature = corr.index[abs(corr['SalePrice'])>0.3]
corr = data_train.corr()
corr.sort_values(['SalePrice'], ascending=False, inplace=True)
corr_sale= corr.SalePrice
print(top_feature)
abs(corr.SalePrice)


# In[ ]:



from sklearn.preprocessing import StandardScaler
scaler= StandardScaler()
scaler.fit(data_train.drop(['SalePrice'],axis=1))
scaled_features_train= scaler.transform(data_train.drop('SalePrice',axis=1))


# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler_=StandardScaler()
scaler_.fit(data_test)
scaled_features_test= scaler_.transform(data_test)


# In[ ]:


scaled_features_test= scaler_.transform(data_test)


# In[ ]:


df_train= pd.DataFrame(scaled_features_train,columns=data_train.columns[:-1])
df_train.head()


# In[ ]:


data_test.info()


# In[ ]:


df_test= pd.DataFrame(scaled_features_test,columns=data_test.columns[:])
df_test.head()


# In[ ]:


from sklearn.model_selection import train_test_split, cross_val_score
X= df_train[['LotFrontage', 'OverallQual', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea',
       'ExterQual', 'Foundation', 'BsmtQual', 'BsmtExposure', 'BsmtFinSF1',
       'TotalBsmtSF', 'HeatingQC', 'CentralAir', '1stFlrSF', '2ndFlrSF',
       'GrLivArea', 'FullBath', 'HalfBath', 'KitchenQual', 'TotRmsAbvGrd',
       'Fireplaces', 'GarageType', 'GarageYrBlt', 'GarageFinish', 'GarageCars',
       'GarageArea', 'GarageCond', 'PavedDrive', 'WoodDeckSF', 'OpenPorchSF']]
y= data_train["SalePrice"] 


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)


# In[ ]:


from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics 


# In[ ]:


models=[]
models.append(('DTC',DecisionTreeRegressor()))
models.append(('KNC',KNeighborsRegressor()))
models.append(('LR',LinearRegression()))
models.append(('RFC',RandomForestRegressor()))
models.append(("MLP",MLPRegressor()))
models.append(("GBC",GradientBoostingRegressor()))


# In[ ]:


names=[]
for name,algo in models:
    algo.fit(X_train,y_train)
    prediction= algo.predict(X_test)
    a= metrics.mean_squared_error(y_test,prediction) 
    print("%s: %f "%(name, a))


# In[ ]:


rm= GradientBoostingRegressor(random_state=22, n_estimators=400)


# In[ ]:


rm.fit(X_train,y_train)


# In[ ]:


prediction = rm.predict(X_test)


# In[ ]:


print(prediction)


# In[ ]:


compare = pd.DataFrame({'Prediction': prediction, 'Test Data' : y_test})
compare.head(10)


# In[ ]:


sns.distplot((y_test-prediction),bins=50)


# In[ ]:


from sklearn.model_selection import cross_val_score
scores = cross_val_score(rm, X, y, cv=10)
print("Cross-validation scores: {}".format(scores))
print("Average cross-validation score: {:.2f}".format(scores.mean()))


# In[ ]:


X_= df_test[['LotFrontage', 'OverallQual', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea',
       'ExterQual', 'Foundation', 'BsmtQual', 'BsmtExposure', 'BsmtFinSF1',
       'TotalBsmtSF', 'HeatingQC', 'CentralAir', '1stFlrSF', '2ndFlrSF',
       'GrLivArea', 'FullBath', 'HalfBath', 'KitchenQual', 'TotRmsAbvGrd',
       'Fireplaces', 'GarageType', 'GarageYrBlt', 'GarageFinish', 'GarageCars',
       'GarageArea', 'GarageCond', 'PavedDrive', 'WoodDeckSF', 'OpenPorchSF']]


# In[ ]:


pred= rm.predict(X_)


# In[ ]:


test= pd.read_csv("../input/test.csv")


# In[ ]:




sub = pd.DataFrame()
sub['Id'] = test['Id']
sub['SalePrice'] = pred 


sub['SalePrice'] = np.exp(sub['SalePrice']) 

sub.to_csv('rf.csv',index=False)


# In[ ]:


submission= pd.read_csv('rf.csv')
submission.head()

