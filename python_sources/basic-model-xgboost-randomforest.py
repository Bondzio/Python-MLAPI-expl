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

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Importing packages for plotting
import matplotlib.pyplot as plt
import seaborn as sns

#Importing packages for data preprocessing
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, LabelEncoder

#Importing packages for machine learning
from sklearn.model_selection import train_test_split


# In[ ]:


pd_data = pd.read_csv("../input/train.csv")


# **Quick View of The Data**

# In[ ]:


pd_data.head(10)


# In[ ]:


pd_data.info()


# **Missing Data**

# In[ ]:


total = pd_data.isnull().sum().sort_values(ascending=False)
percent = (pd_data.isnull().sum()/pd_data.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(20)


# Firstly, I straightly remove the variables with too many missing values as well as the "Id" variable

# In[ ]:


pd_data = pd_data.drop(["Alley","FireplaceQu","PoolQC","Fence","MiscFeature","Id","LotFrontage"], axis=1)


# Secondly, I find that the number of missing values of the "Garage..." variabes and the "Bsmt..." variables are respectively the same, so I guess their missing data should be in the same observations. For these variables, I also straightly remove them.

# In[ ]:


pd_data = pd_data.drop(["GarageType","GarageYrBlt","GarageFinish","GarageQual","GarageCond"],axis = 1)
pd_data = pd_data.drop(["BsmtFinType2","BsmtExposure","BsmtFinType1","BsmtCond","BsmtQual"], axis = 1)
pd_data = pd_data.drop(["MasVnrType"], axis = 1)


# For "MasVnrArea" and "Electrical", there is only few misssing values so I just use the median to impute the former and use the most frequent value to impute the latter.

# In[ ]:


pd_data['MasVnrArea'].fillna(pd_data['MasVnrArea'].median(), inplace = True)


# In[ ]:


pd_data = pd_data.fillna(pd_data['Electrical'].value_counts().index[0])


# Just double check whether all the variables are free from missing value.

# In[ ]:


total = pd_data.isnull().sum().sort_values(ascending = False)
percent = (pd_data.isnull().sum()/pd_data.isnull().count()).sort_values(ascending = False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(3)


# **Exploratory Data Analysis**

# In[ ]:


correlations = pd_data.corr()
plt.figure(figsize=(12,12))
g = sns.heatmap(correlations,cbar = True, square = True, fmt= '.2f', annot_kws={'size': 12})


# Here I try to find the top 10 variables that are most correlated with our response "SalePrice"

# In[ ]:


k = 10 
cols = correlations.nlargest(k, 'SalePrice')['SalePrice'].index
cm = np.corrcoef(pd_data[cols].values.T)
sns.set(font_scale = 1)
hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, 
                 yticklabels=cols.values, xticklabels=cols.values)
plt.show()


# **Dealing with Categorical Variables**

# In[ ]:


le = LabelEncoder()

pd_data['MSZoning']      = le.fit_transform(pd_data['MSZoning'])
pd_data['Exterior1st']   = le.fit_transform(pd_data['Exterior1st'])
pd_data['Exterior2nd']   = le.fit_transform(pd_data['Exterior2nd'])
pd_data['KitchenQual']   = le.fit_transform(pd_data['KitchenQual'])
pd_data['Functional']    = le.fit_transform(pd_data['Functional'])
pd_data['SaleType']      = le.fit_transform(pd_data['SaleType'])
pd_data['Street']        = le.fit_transform(pd_data['Street'])   
pd_data['LotShape']      = le.fit_transform(pd_data['LotShape'])   
pd_data['LandContour']   = le.fit_transform(pd_data['LandContour'])   
pd_data['LotConfig']     = le.fit_transform(pd_data['LotConfig'])   
pd_data['LandSlope']     = le.fit_transform(pd_data['LandSlope'])   
pd_data['Neighborhood']  = le.fit_transform(pd_data['Neighborhood'])   
pd_data['Condition1']    = le.fit_transform(pd_data['Condition1'])   
pd_data['Condition2']    = le.fit_transform(pd_data['Condition2'])   
pd_data['BldgType']      = le.fit_transform(pd_data['BldgType'])   
pd_data['HouseStyle']    = le.fit_transform(pd_data['HouseStyle'])   
pd_data['RoofStyle']     = le.fit_transform(pd_data['RoofStyle'])   
pd_data['RoofMatl']      = le.fit_transform(pd_data['RoofMatl'])      
pd_data['ExterQual']     = le.fit_transform(pd_data['ExterQual'])  
pd_data['ExterCond']     = le.fit_transform(pd_data['ExterCond'])   
pd_data['Foundation']    = le.fit_transform(pd_data['Foundation'])   
pd_data['Heating']       = le.fit_transform(pd_data['Heating'])   
pd_data['HeatingQC']     = le.fit_transform(pd_data['HeatingQC'])   
pd_data['CentralAir']    = le.fit_transform(pd_data['CentralAir'])   
pd_data['Electrical']    = le.fit_transform(pd_data['Electrical'])    
pd_data['PavedDrive']    = le.fit_transform(pd_data['PavedDrive'])  
pd_data['SaleCondition'] = le.fit_transform(pd_data['SaleCondition']) 
pd_data['Utilities']     = le.fit_transform(pd_data['Utilities']) 


# **Begin Machine Learning**

# In[ ]:


y = pd_data[['SalePrice']]
X = pd_data.drop('SalePrice',axis=1)


# In[ ]:


Scaler = StandardScaler()

X = pd.DataFrame(Scaler.fit_transform(X))


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)


# **XGBoost**

# In[ ]:


from xgboost import XGBRegressor
XGB = XGBRegressor(max_depth = 5, learning_rate = 0.05, n_estimators = 1500, reg_alpha = 0.001,
                reg_lambda = 0.000001, n_jobs = -1, min_child_weight = 3)
XGB.fit(X_train,y_train)


# In[ ]:


print ("Training score:",XGB.score(X_train,y_train),"Test Score:",XGB.score(X_test,y_test))


# **Random Forest**

# In[ ]:


from sklearn.ensemble import RandomForestRegressor
RFR = RandomForestRegressor(max_depth = 20, random_state = 0, n_estimators = 100)
RFR.fit(X_train,y_train)


# In[ ]:


print ("Training score:",RFR.score(X_train,y_train),"Test Score:",RFR.score(X_test,y_test))

