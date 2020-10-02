#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import libraries

get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import scipy.stats as stats
import sklearn.linear_model as linear_model
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn import metrics
from scipy.stats import norm, skew


# In[ ]:


#Load datasets

train = pd.read_csv('C:\\Users\\Marissa\\Downloads\\Regression\\house-prices-advanced-regression-techniques\\train.csv')
test = pd.read_csv('C:\\Users\\Marissa\\Downloads\\Regression\\house-prices-advanced-regression-techniques\\test.csv')


# Train and Test: Shape, Head and Info

# In[ ]:


train.shape


# In[ ]:


test.shape


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


train.info()


# In[ ]:


test.info()


# In[ ]:


#Split data into Quantitative (Numerical) Features and Qualitative (Categorical) Features
#Remove SalePrice and ID columns from Quantitative Features
#SalePrice is the Dependent Variable (y)
#Quantitative + Qualitative are the Independent Variables (X's)

quantitative = [f for f in train.columns if train.dtypes[f] != 'object']
quantitative.remove('SalePrice')
quantitative.remove('Id')
qualitative = [f for f in train.columns if train.dtypes[f] == 'object']


# Exploring the Dependent Variable (y), SalePrice

# In[ ]:


#Applying summary statistics to SalePrice to check data
#No 0 values in price

train['SalePrice'].describe()


# In[ ]:


#Plotting Dependent Variable 
#We can see that SalePrice does not follow a normal distribution, is skewed to the left and has a long tail (Kurotosis)

sns.distplot(train['SalePrice'])


# In[ ]:


#Skewness

train['SalePrice'].skew()


# In[ ]:


#Kurotosis

train['SalePrice'].kurt()


# Normality Statistical Tests

# In[ ]:


#Shapiro-Wilk Test

stat, p = stats.shapiro(train['SalePrice'])
print('Statistics: ' + str(stat))
print('p: ' + str(p))

alpha = 0.05
if p > alpha:
    print('Normal')
else:
    print('Not Normal')


# In[ ]:


#K^2 test

from scipy.stats import normaltest
stat, p = normaltest(train['SalePrice'])
print('Statistics: ' + str(stat))
print('p: ' + str(p))

alpha = 0.05
if p > alpha:
    print('Normal')
else:
    print('Not Normal')


# In[ ]:


import scipy.stats as st

plt.figure(2); plt.title('Normal')
sns.distplot(train['SalePrice'], kde=False, fit=st.norm)


# In[ ]:


plt.figure(3); plt.title('Log Normal')
sns.distplot(train['SalePrice'], kde=False, fit=st.lognorm)


# In[ ]:


plt.figure(1); plt.title('Johnson SU')
sns.distplot(train['SalePrice'], kde=False, fit=st.johnsonsu)


# In[ ]:


#Check for outliers in GrLivArea as per the recommendation in the dataset details

plt.scatter(train.GrLivArea, train.SalePrice, c = 'blue', marker = "s")
plt.title('Looking for outliers')
plt.xlabel('GrLivArea')
plt.ylabel('SalePrice')
plt.show()


# In[ ]:


train_ID = train['Id']
test_ID = test['Id']

train.drop('Id', axis = 1, inplace = True)
test.drop('Id', axis = 1, inplace = True)


# In[ ]:


#Removing any houses with more than 4000 square feet from the dataset as per dataset author's recommendation
#Log Transform SalePrice and set y variable
#Taking logs means that errors in predicting expensive houses and cheap houses will affect the result equally.

train = train.drop(train[(train['GrLivArea']>4000) & (train['SalePrice']<300000)].index)
y = train['SalePrice'].values


# In[ ]:


train['SalePrice'] = np.log1p(train['SalePrice'])


# In[ ]:


train.columns


# Exploring the Independent Variables (X's)

# In[ ]:


#Visualing missing data

missing = train.isnull().sum()
missing = missing[missing > 0]
missing.sort_values(inplace=True)
missing.plot.bar()


# In[ ]:


#Correlation

train.corr()['SalePrice'].sort_values(ascending=False)


# In[ ]:


#Plotting a heatmap of correlations to remove multi-collinearity

plt.rc('xtick', labelsize=25) 
plt.rc('ytick', labelsize=25) 
plt.figure(figsize=[35,25])
sns.heatmap(train.corr(), annot=True)


# In[ ]:


#Visualise Correlation

corrmat = train.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True);


# Imputing Missing Data

# In[ ]:


#As per data description
#In most cases, the qualitative features with missing data indicate that the feature is missing, eg. No Pool,No fireplace, 
#No fence, No alley access..etc.

objects = []
for i in train.columns:
    if train[i].dtype == object:
        objects.append(i)
train.update(train[objects].fillna('None'))


# In[ ]:


#Do the same for test2

objects = []
for i in test.columns:
    if test[i].dtype == object:
        objects.append(i)
test.update(test[objects].fillna('None'))


# In[ ]:


#Imputing the data for LotFrontage with the Median LotFrontage per Neighbourhood

train['LotFrontage'] = train.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))


# In[ ]:


#Imputing the data for LotFrontage with the Median LotFrontage per Neighbourhood

test['LotFrontage'] = test.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))


# In[ ]:


#For all other numeric types, impute missing data with 0 

num_dtypes = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

numtr = []
for i in train.columns:
    if train[i].dtype in num_dtypes:
        numtr.append(i)
train.update(train[numtr].fillna(0))


# In[ ]:


numts = []
for i in test.columns:
    if test[i].dtype in num_dtypes:
        numts.append(i)
test.update(test[numts].fillna(0))


# In[ ]:


train['MSSubClass'] = train['MSSubClass'].astype(str)


train['OverallCond'] = train['OverallCond'].astype(str)
train['OverallQual'] = train['OverallQual'].astype(str)


train['YrSold'] = train['YrSold'].astype(str)
train['MoSold'] = train['MoSold'].astype(str)


# In[ ]:


test['MSSubClass'] = test['MSSubClass'].astype(str)


test['OverallCond'] = test['OverallCond'].astype(str)
test['OverallQual'] = test['OverallQual'].astype(str)

#Year and month sold are transformed into categorical features.
test['YrSold'] = test['YrSold'].astype(str)
test['MoSold'] = test['MoSold'].astype(str)


# In[ ]:


new_train = train.shape[0] # create a new train variable to hold the 0 index shape value
new_test = test.shape[0]   # create a new test variable to to hold the 0 index shape value

combined = pd.concat((train, test)).reset_index(drop=True) 
combined.drop(['SalePrice'], axis=1, inplace=True)


# In[ ]:


from sklearn.preprocessing import LabelEncoder
cols = ('FireplaceQu', 'BsmtQual', 'BsmtCond', 'GarageQual', 'GarageCond', 
        'ExterQual', 'ExterCond','HeatingQC', 'PoolQC', 'KitchenQual', 'BsmtFinType1', 
        'BsmtFinType2', 'Functional', 'Fence', 'BsmtExposure', 'GarageFinish', 'LandSlope',
        'LotShape', 'PavedDrive', 'Street', 'Alley', 'CentralAir', 'MSSubClass', 'OverallCond', 
        'YrSold', 'MoSold')
# process columns, apply LabelEncoder to categorical features
for x in cols:
    lbl = LabelEncoder() 
    lbl.fit(list(combined[x].values)) 
    combined[x] = lbl.transform(list(combined[x].values))


# In[ ]:


combined.shape


# In[ ]:


dum = pd.get_dummies(combined) 


# In[ ]:


moo1 = dum.values


# In[ ]:


scaler = StandardScaler() 
moo1 = scaler.fit_transform(moo1)


# In[ ]:


X = moo1[:new_train] # items from the beginning through stop-1
test_values = moo1[new_train:] # items start through the rest of the array


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

lasso = Lasso(alpha=1210)

lasso.fit(X_train, y_train)

y_pred = lasso.predict(X_test)

y_train_pred = lasso.predict(X_train)


# In[ ]:


final_prices = lasso.predict(test_values)


# In[ ]:


print('MAE:', metrics.mean_absolute_error(y_test, y_pred))
print('MSE:', metrics.mean_squared_error(y_test, y_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))


# In[ ]:


sub = pd.DataFrame()
sub['Id'] = test_ID
sub['SalePrice'] = final_prices
sub.to_csv('sol.csv',index=False)

