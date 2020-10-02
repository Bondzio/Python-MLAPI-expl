#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sb
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data=pd.read_csv("../input/train.csv")
data.isnull().sum()


# In[ ]:


data.shape


# **Now we analyis our target column i.e, SalePrice (Look for most normalised form)**

# In[ ]:


sb.distplot(data.SalePrice)
# too much right skewed


# In[ ]:


sb.distplot(1/data.SalePrice)
# not good


# In[ ]:


sb.distplot(np.log(data.SalePrice))
# we can used this since it is normalised


# **Now we update our target value by it's log**

# In[ ]:


data.SalePrice=np.log(data.SalePrice)
sb.distplot(data.SalePrice)


# **Let's do Data Cleaning**

# 1. Treatment for missing values

# In[ ]:


# There are 259 values missing in Lot Frontage
med=data.LotFrontage.median()
data.LotFrontage.fillna(med,inplace=True)
sb.distplot(data.LotFrontage)


# In[ ]:


print("Empty Values - ",data.Alley.isnull().sum())
 #   So lots of values that are missing
  #  Since its a features that can be present in the house or not
   # We can Fill empty value by 'NA'
data.Alley.fillna('NA',inplace=True)
plt.hist(data.Alley)
data.Alley.isnull().sum()


# In[ ]:


print("Empty values - ",data.MasVnrType.isnull().sum())
plt.hist(data.MasVnrType)
data.MasVnrType.fillna('None',inplace=True)


# In[ ]:


print('Empty values - ',data.MasVnrArea.isnull().sum())
# there are no MasVnr so there area must be filled as zero
data.MasVnrArea.fillna(0,inplace=True)


# In[ ]:


print(data.FireplaceQu.isnull().sum())
data.FireplaceQu.fillna('NA',inplace=True)


# In[ ]:


plt.hist(data.FireplaceQu)


# In[ ]:


print('emptyvalues - ',data.GarageType.isnull().sum())
data.GarageType.fillna('Na',inplace=True)


# In[ ]:


print('emptyvalues - ',data.GarageYrBlt.isnull().sum())
data.GarageYrBlt.fillna(data.YearBuilt,inplace=True)


# In[ ]:


data.GarageFinish.isnull().sum()
data.GarageFinish.fillna('Na',inplace=True)


# In[ ]:


#Similarly
data.GarageType.fillna('NA', inplace=True)     
data.BsmtExposure.fillna('NA', inplace=True)     
data.BsmtCond.fillna('NA', inplace=True)        
data.BsmtQual.fillna('NA', inplace=True)        
data.BsmtFinType2.fillna('NA', inplace=True)     
data.BsmtFinType1.fillna('NA', inplace=True)  
data.BsmtUnfSF.fillna(0, inplace=True)     
data.BsmtFinSF2.fillna(0, inplace=True)    
data.BsmtFinSF1.fillna(0, inplace=True)  
data.BsmtHalfBath.fillna(0, inplace=True)
data.BsmtFullBath.fillna(0, inplace=True)
data.MasVnrType.fillna('None', inplace=True)   
data.Exterior2nd.fillna('None', inplace=True)
data.GarageCond.fillna('NA', inplace=True)    
data.GarageQual.fillna('NA', inplace=True)
data.Fence.fillna('NA', inplace=True) 
data.PoolQC.fillna('NA', inplace=True)
data.MiscFeature.fillna('NA', inplace=True) 
data.BsmtHalfBath.fillna(0, inplace=True)
data.BsmtFullBath.fillna(0, inplace=True)
data.GarageArea.fillna(0, inplace=True)
data.GarageCars.fillna(0, inplace=True)    
data.TotalBsmtSF.fillna(0, inplace=True)   
data.GarageArea.fillna(0, inplace=True)
data.GarageCars.fillna(0, inplace=True)    
data.TotalBsmtSF.fillna(0, inplace=True)   
data.BsmtUnfSF.fillna(0, inplace=True)     
data.BsmtFinSF2.fillna(0, inplace=True)    
data.BsmtFinSF1.fillna(0, inplace=True)  


# In[ ]:


data.Electrical.fillna('SBrkr',inplace=True)


# In[ ]:


data.isnull().sum().sum()


# SO FINALLY ARE MISSING VALUE ARE TREATED.

# **Encoding is required for Categorical data**

# In[ ]:


data.Alley = data.Alley.map({'NA':0, 'Grvl':1, 'Pave':2})
data.BsmtCond =  data.BsmtCond.map({'NA':0, 'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
data.BsmtExposure = data.BsmtExposure.map({'NA':0, 'No':1, 'Mn':2, 'Av':3, 'Gd':4})
data.BsmtFinType1 = data.BsmtFinType1.map({'NA':0, 'Unf':1, 'LwQ':2, 'Rec':3, 'BLQ':4, 'ALQ':5, 'GLQ':6})
data.BsmtFinType2 = data.BsmtFinType2.map({'NA':0, 'Unf':1, 'LwQ':2, 'Rec':3, 'BLQ':4, 'ALQ':5, 'GLQ':6})
data.BsmtQual = data.BsmtQual.map({'NA':0, 'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
data.ExterCond = data.ExterCond.map({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
data.ExterQual = data.ExterQual.map({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
data.FireplaceQu = data.FireplaceQu.map({'NA':0, 'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
data.Functional = data.Functional.map({'Sal':1, 'Sev':2, 'Maj2':3, 'Maj1':4, 'Mod':5, 'Min2':6, 'Min1':7, 'Typ':8})
data.GarageCond = data.GarageCond.map({'NA':0, 'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
data.GarageQual = data.GarageQual.map({'NA':0, 'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
data.HeatingQC = data.HeatingQC.map({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
data.KitchenQual = data.KitchenQual.map({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
data.LandSlope = data.LandSlope.map({'Sev':1, 'Mod':2, 'Gtl':3}) 
data.PavedDrive = data.PavedDrive.map({'N':1, 'P':2, 'Y':3})
data.PoolQC = data.PoolQC.map({'NA':0, 'Fa':1, 'TA':2, 'Gd':3, 'Ex':4})
data.Street = data.Street.map({'Grvl':1, 'Pave':2})
data.Utilities = data.Utilities.map({'ELO':1, 'NoSeWa':2, 'NoSewr':3, 'AllPub':4})


# **BASELINE MODEL (filling test response variable by mean of train dataset)**

# In[ ]:


base_data = pd.read_csv("../input/test.csv")
filling_mean = data.SalePrice.mean()


# In[ ]:


b=np.full((1459,1),filling_mean)
b.shape


# In[ ]:


base_data['SalePrice']=b
#baseline model completed


# **Linear Regression Model**

# In[ ]:


x_train = data.drop(['Id','SalePrice'],axis=1)
y_train = data.SalePrice


# In[ ]:


l1=data.select_dtypes(include=['object']).columns
x_train = x_train.drop(l1,axis=1)


# In[ ]:


from sklearn.linear_model import LinearRegression
lr=LinearRegression()


# In[ ]:


model1=lr.fit(x_train,y_train)
y_pred=model1.predict(x_train)
model1.score(x_train,y_train)


# *This is quite a good score for Linear Regression model*

# In[ ]:


plt.plot(data.SalePrice,y_pred,'o')
plt.xlabel('Actual SalePrice')
plt.ylabel('Predicted SalePrice')


# Quite a Linear Relationship with estimated slope of 1 indication of closely related predicted and actual value as expected from 88% accuracy score.

# **No need of polynomial regression since we get linear relationship**

# In[ ]:


#residual plot
res=y_pred-data.SalePrice
plt.plot(data.SalePrice,res,'o')
plt.xlabel('Actual SalePrice')
plt.ylabel('Residual')


# **Let's do Cross Validation**

# In[ ]:


from sklearn.cross_validation import cross_val_score


# In[ ]:


X=x_train
Y=y_train


# In[ ]:


from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


# In[ ]:


X_train,X_test,Y_train,Y_test = train_test_split(X,Y,random_state=2)


# In[ ]:


lr2=LinearRegression()
model2 = lr2.fit(X_train,Y_train)
scores=cross_val_score(lr2,X_train,Y_train,cv=10,scoring='neg_mean_squared_error')
scores=-scores
rmse = np.sqrt(scores)
print(model2.score(X_train,Y_train))


# In[ ]:


Y_pred=model2.predict(X_test)
plt.plot(Y_test,Y_pred,'o')
plt.xlabel('Actual SalePrice')
plt.ylabel('Predicted SalePrice')


# In[ ]:


#residual plot
res = Y_pred - Y_test
plt.plot(Y_test, res,'o')
plt.xlabel('Actual SalePrice')
plt.ylabel('Residual')

