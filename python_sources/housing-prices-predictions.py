#!/usr/bin/env python
# coding: utf-8

# **Import modules**

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error


# **Reading in input file**

# In[ ]:


house_train_df = pd.read_csv('../input/train.csv')
house_test_df = pd.read_csv('../input/test.csv')
ntrain = house_train_df.shape
ntest = house_test_df.shape
print ((ntrain), (ntest))


# Look at few rows

# In[ ]:


n_train = house_train_df.shape[0]
n_test = house_test_df.shape[0]
house_train_df.head()


# Dropping the ID

# In[ ]:


train_ID = house_train_df['Id']
test_ID = house_test_df['Id']
house_train_df.drop("Id", axis = 1, inplace = True)
house_test_df.drop("Id", axis = 1, inplace = True)


# **Review data**
# 
# Statistical Description

# In[ ]:


house_train_df.describe()


# **Handling missing value**
# 
# *Numericall columns within the train dataset*

# In[ ]:


house_train_df.select_dtypes(exclude=['object']).columns


# *numerical missing values witin train dataset*

# In[ ]:


house_train_df.select_dtypes(exclude=['object']).isnull().sum().sort_values(ascending=False).head(5)


# *Categorical columns within the train dataset*

# In[ ]:


house_train_df.select_dtypes(include=['object']).columns


# *categrical missing values witin train dataset*

# In[ ]:


house_train_df.select_dtypes(include=['object']).isnull().sum().sort_values(ascending=False).head(20)


# *numerical missing values witin test dataset*

# In[ ]:


house_test_df.select_dtypes(exclude=['object']).isnull().sum().sort_values(ascending=False).head(12)


# *categrical missing values witin train dataset*

# In[ ]:


house_test_df.select_dtypes(include=['object']).isnull().sum().sort_values(ascending=False).head(25)


# *target price and combining whole data to fill missing values*

# In[ ]:


n_train = house_train_df.shape[0]
n_test = house_test_df.shape[0]

target_price = house_train_df.SalePrice.values

house_data = pd.concat((house_train_df, house_test_df)).reset_index(drop=True)

house_data.drop(['SalePrice'], axis=1, inplace=True)
house_data.shape


# Missing Vaneer type and vaneer area

# In[ ]:


house_data[house_data["MasVnrType"] == 'NaN'].MasVnrArea.mean()


# *filling missing numerical values*

# In[ ]:


for col in ('GarageArea', 'GarageCars'):
    house_data[col] = house_data[col].fillna(0)
for col in ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF','TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath', 'MasVnrArea'):
    house_data[col] = house_data[col].fillna(0)
house_data["LotFrontage"] = house_data.groupby("Neighborhood")["LotFrontage"].transform(lambda x: x.fillna(x.median())) 
house_data["GarageYrBlt"] = house_data['GarageYrBlt'].fillna(house_data['YearBuilt'])


# filling missing cateorical values

# In[ ]:


for col in ('GarageCond', 'GarageQual', 'GarageFinish', 'GarageType' ):
    house_data[col] = house_data[col].fillna("None")
for col in ('BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1','MasVnrType', 'BsmtFinType2'):
    house_data[col] = house_data[col].fillna("None")
for col in ('PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu' ):
    house_data[col] = house_data[col].fillna("None")
for col in ('MSZoning', 'Utilities', 'Functional', 'KitchenQual', 'SaleType', 'Exterior2nd','Electrical', 'Exterior1st'):    
    house_data[col] = house_data[col].fillna(house_data[col].mode()[0])  


# Checking for any missing values

# In[ ]:


house_data.isnull().sum().sort_values(ascending=False).head()


# Separating the training and test data set

# In[ ]:


train_df = house_data[:n_train]
test_df = house_data[n_train:]
train_df['SalePrice'] = target_price


# **First Thing : Analysing Saleprice**

# In[ ]:


plt.hist(house_train_df.SalePrice)
plt.show()
#sns.distplot(house_train_df['SalePrice'])


# In[ ]:


target = train_df.SalePrice
plt.figure(figsize=(8,5))
sns.distplot(target)
plt.title('Distribution of SalePrice')


# In[ ]:


sns.distplot(np.log(target))
plt.title('Distribution of Log-transformed SalePrice')
plt.xlabel('log(SalePrice)')


# **Saleprice and relationship with neighbourhood **

# In[ ]:


from matplotlib.pyplot import xticks
plt.figure(figsize=(15,9))
sns.boxplot(x = train_df['Neighborhood'], y = train_df['SalePrice'])
xticks(rotation=90)


# **Saleprice and relationship with Overall quality **

# In[ ]:


#fig, (ax1, ax2) = plt.subplots(1, 2)
plt.figure(figsize=(8,5))
ax1 = train_df.groupby('OverallQual')['SalePrice'].mean().plot.bar()
plt.figure(figsize=(8,5))
ax2 = sns.boxplot(x = train_df['OverallQual'], y = train_df['SalePrice'])


# **Saleprice and relationship with Garagearea**

# In[ ]:


sns.lmplot(x="GarageArea", y="SalePrice", data=train_df)


# In[ ]:


plt.figure(figsize=(15,9))
sns.boxplot(x = train_df['Neighborhood'], y = train_df['SalePrice'])


# In[ ]:


house_data['YrSold'] = house_data['YrSold'].astype(str)
house_data['MoSold'] = house_data['MoSold'].astype(str)


# **correlation matrix **

# In[ ]:


corrmat = train_df.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True)


# **SalePrice correlation matrix **

# In[ ]:


k = 10 
cols = corrmat.nlargest(k, 'SalePrice')['SalePrice'].index
cm = np.corrcoef(train_df[cols].values.T)
sns.set(font_scale=1.25)
hm = sns.heatmap(cm, cbar=True, annot=True, square=True, annot_kws={'size': 10},  yticklabels=cols.values, xticklabels=cols.values)


# *removing some variable*

# In[ ]:


low_cardinality_cols = [cname for cname in house_data.columns if 
                                house_data[cname].nunique() < 30 and
                                house_data[cname].dtype == "object"]
numeric_cols = [cname for cname in house_data.columns if 
                                house_data[cname].dtype in ['int64', 'float64']]
my_cols = low_cardinality_cols + numeric_cols
#low_cardinality_cols
house_data = house_data[my_cols]


# *getting Dummy data for categorical variable*

# In[ ]:


house_data_dummy = pd.get_dummies(house_data)


# In[ ]:


train_data = house_data_dummy[:n_train]
test_data  = house_data_dummy[n_train:]


# *Standardize features *

# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train, X_test, y_train, y_test = train_test_split(train_data, target_price, test_size = 0.25, random_state = 0)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
test_data = scaler.fit_transform(test_data)


# In[ ]:


X_train.shape


# In[ ]:


X_test.shape


# **XGBRegressor**

# In[ ]:


my_model = XGBRegressor(n_estimators=1000, learning_rate=0.05)
my_model.fit(X_train, y_train, early_stopping_rounds=10, eval_set=[(X_test, y_test)], verbose=False)


# *mean_absolute_error*

# In[ ]:


predictions = my_model.predict(X_test)
print("Mean Absolute Error : " + str(mean_absolute_error(predictions, y_test)))


# *predictions*

# In[ ]:


pred_test = my_model.predict(test_data)
print(pred_test)


# *Submissions*

# In[ ]:


sub = pd.DataFrame()
sub['Id'] = test_ID
sub['SalePrice'] = pred_test
sub.to_csv('submission_price.csv', index=False)

