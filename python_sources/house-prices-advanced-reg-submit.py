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

#invite people for the Kaggle party
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Imputer
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV, ElasticNetCV
from sklearn.linear_model import Ridge, RidgeCV, ElasticNet, LassoCV, LassoLarsCV
from sklearn.model_selection import cross_val_score, train_test_split
from scipy import stats
from scipy.stats import norm, skew
import warnings
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')
import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


# save filepath to variable for easier access
train_data = '../input/train.csv'
test_data = '../input/test.csv'

# Input datas
train = pd.read_csv(train_data) 
test = pd.read_csv(test_data) 

#Columns names
train.columns


# In[ ]:


# Check data type
train.dtypes.sample(train.shape[1])


# In[ ]:


y =pd.DataFrame(train['SalePrice']) 
train=train.drop(columns=['SalePrice'])

#descriptive statistics summary
y.describe()


# In[ ]:


#histogram
sns.distplot(y);


# In[ ]:


#skewness and kurtosis
print("Skewness: %f" % y.skew())
print("Kurtosis: %f" % y.kurt())


# In[ ]:


concat = [train, test]
result = pd.concat(concat)


# Missing Data

# In[ ]:


#missing data
total = result.isnull().sum().sort_values(ascending=False)
percent = (result.isnull().sum()/result.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(20)


# In[ ]:


all_data_na = (result.isnull().sum() / len(result)) * 100
all_data_na = all_data_na.drop(all_data_na[all_data_na == 0].index).sort_values(ascending=False)[:30]
missing_data1 = pd.DataFrame({'Missing Ratio' :all_data_na})
missing_data1.head(all_data_na.shape[0])
f, ax = plt.subplots(figsize=(15, 12))
plt.xticks(rotation='90')
sns.barplot(x=all_data_na.index, y=all_data_na)
plt.xlabel('Features', fontsize=15)
plt.ylabel('Percent of missing values', fontsize=15)
plt.title('Percent missing data by feature', fontsize=15)


# In[ ]:


# Differentiate numerical features (minus the target) and categorical features
categorical_features = result.select_dtypes(include = ["object"]).columns
numerical_features = result.select_dtypes(exclude = ["object"]).columns
print("Numerical features : " + str(len(numerical_features)))
print("Categorical features : " + str(len(categorical_features)))
result_num = result[numerical_features]
result_cat = result[categorical_features]

# Input missing values
my_imputer = Imputer(strategy='mean')
result[numerical_features] = my_imputer.fit_transform(result[numerical_features])


# In[ ]:


########## Dealing with missing data
# Delete the columns that has more than 1 missing values
result = result.drop((missing_data[missing_data['Percent'] > 0.00]).index,1)


# In[ ]:


train = result[:train.shape[0]]
test = result[train.shape[0]:]

# Add Column price to the train
train=pd.concat([train, y], axis=1, join='inner')


# In[ ]:


# Differentiate numerical features (minus the target) and categorical features
categorical_features = train.select_dtypes(include = ["object"]).columns
numerical_features = train.select_dtypes(exclude = ["object"]).columns
numerical_features = numerical_features.drop("SalePrice")
print("Numerical features : " + str(len(numerical_features)))
print("Categorical features : " + str(len(categorical_features)))
train_num = train[numerical_features]
train_cat = train[categorical_features]


# Relationship with numerical variables

# In[ ]:


#scatterplot
sns.set()
cols = ['SalePrice']
cols.extend(numerical_features[1:5].tolist())
sns.pairplot(train[cols], size = 3.5)
plt.show();


# In[ ]:


train = train.drop(train[(train['SalePrice']>300000) & (train['OverallCond']==2)].index)


# In[ ]:


#scatterplot
sns.set()
cols = ['SalePrice']
cols.extend(numerical_features[5:10].tolist())
sns.pairplot(train[cols], size = 3.5)
plt.show();


# In[ ]:


#scatterplot
sns.set()
cols = ['SalePrice']
cols.extend(numerical_features[10:15].tolist())
sns.pairplot(train[cols], size = 3.5)
plt.show();


# In[ ]:


train = train.drop(train[(train['1stFlrSF']>4000)].index)


# In[ ]:


#scatterplot
sns.set()
cols = ['SalePrice']
cols.extend(numerical_features[15:20].tolist())
sns.pairplot(train[cols], size = 3.5)
plt.show();


# In[ ]:


#scatterplot
sns.set()
cols = ['SalePrice']
cols.extend(numerical_features[20:25].tolist())
sns.pairplot(train[cols], size = 3.5)
plt.show();


# In[ ]:


#scatterplot
sns.set()
cols = ['SalePrice']
cols.extend(numerical_features[25:30].tolist())
sns.pairplot(train[cols], size = 3.5)
plt.show();


# Correlation Matrix

# In[ ]:


corrmat = train.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmin=-1,vmax=1, square=True,center=0)


# In[ ]:


# 'SalePrice' correlation matrix (zoomed heatmap style)
#saleprice correlation matrix
k = 10 #number of variables for heatmap
cols = corrmat.nlargest(k, 'SalePrice')['SalePrice'].index
cm = np.corrcoef(train[cols].values.T)
sns.set(font_scale=1.25)
hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
plt.show()


# In[ ]:


# 'SalePrice' correlation matrix (zoomed heatmap style)
#saleprice correlation matrix
k = 10 #number of variables for heatmap
cols = corrmat.nsmallest(k, 'SalePrice')['SalePrice'].index
cm = np.corrcoef(train[cols].values.T)
sns.set(font_scale=1.25)
hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
plt.show()


# Removing Out Liars

# In[ ]:


#standardizing SalePrice and check the data
# We will standardize the data. In this context, data standardization means converting data values to have mean of 0 
# and a standard deviation of 1.
saleprice_scaled = StandardScaler().fit_transform(train['SalePrice'][:,np.newaxis]);
low_range = saleprice_scaled[saleprice_scaled[:,0].argsort()][:10]
high_range= saleprice_scaled[saleprice_scaled[:,0].argsort()][-10:]
print('outer range (low) of the distribution:')
print(low_range)
print('\nouter range (high) of the distribution:')
print(high_range)


# In[ ]:


#histogram and normal probability plot
sns.distplot(train['SalePrice'], fit=norm);
fig = plt.figure()
res = stats.probplot(train['SalePrice'], plot=plt)


# Skewness

# In[ ]:


y=train['SalePrice']
train=train.drop(columns=['SalePrice'])


# In[ ]:


concat = [train, test]
result = pd.concat(concat)


# In[ ]:


numeric_feats = result.dtypes[result.dtypes != "object"].index

# Check the skew of all numerical features
skewed_feats = result[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
print("\nSkew in numerical features: \n")
skewness = pd.DataFrame({'Skew' :skewed_feats})
skewness.head(10)


# In[ ]:


skewed_feats = skewed_feats[skewed_feats > 0.75]
skewed_feats = skewed_feats.index

result[skewed_feats] = np.log1p(result[skewed_feats])


# In[ ]:


numeric_feats = result.dtypes[result.dtypes != "object"].index

# Check the skew of all numerical features
skewed_feats = result[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
print("\nSkew in numerical features: \n")
skewness = pd.DataFrame({'Skew' :skewed_feats})
skewness.head(10)


# Gettin Dummy Categorical Features

# In[ ]:


print('Before getting dummys',result.shape)
result = pd.get_dummies(result)
print('after getting dummys',result.shape)


# Models

# In[ ]:


# Creating new features 
# nonlinear transformation for the top 5 correlation features
result["OverallQual-s2"] = result["OverallQual"] ** 2
result["OverallQual-s3"] = result["OverallQual"] ** 3
result["OverallQual-Sq"] = np.sqrt(result["OverallQual"])

result["GrLivArea-2"] = result["GrLivArea"] ** 2
result["GrLivArea-3"] = result["GrLivArea"] ** 3
result["GrLivArea-Sq"] = np.sqrt(result["GrLivArea"])

result["1stFlrSF-2"] = result["1stFlrSF"] ** 2
result["1stFlrSF-3"] = result["1stFlrSF"] ** 3
result["1stFlrSF-Sq"] = np.sqrt(result["1stFlrSF"])

result["FullBath-2"] = result["FullBath"] ** 2
result["FullBath-3"] = result["FullBath"] ** 3
result["FullBath-Sq"] = np.sqrt(result["FullBath"])

result["TotRmsAbvGrd-s2"] = result["TotRmsAbvGrd"] ** 2
result["TotRmsAbvGrd-s3"] = result["TotRmsAbvGrd"] ** 3
result["TotRmsAbvGrd-Sq"] = np.sqrt(result["TotRmsAbvGrd"])


# In[ ]:


train = result[:train.shape[0]]
test = result[train.shape[0]:]


# In[ ]:


x=train.drop(columns=['Id'])


# In[ ]:


#histogram and normal probability plot
sns.distplot(y, fit=norm);
fig = plt.figure()
res = stats.probplot(y, plot=plt)


# In[ ]:


# Log in the price
y = np.log1p(y)

#histogram and normal probability plot
sns.distplot(y, fit=norm);
fig = plt.figure()
res = stats.probplot(y, plot=plt)


# In[ ]:


# Partition the dataset in train + validation sets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)


# In[ ]:


# Define error measure for official scoring : RMSE
scorer = make_scorer(mean_squared_error, greater_is_better = False)

def rmse_cv_train(model):
    rmse= np.sqrt(-cross_val_score(model, X_train, y_train, scoring = scorer, cv = 10))
    return(rmse)

def rmse_cv_test(model):
    rmse= np.sqrt(-cross_val_score(model, X_test, y_test, scoring = scorer, cv = 10))
    return(rmse)


# Linear Regression

# In[ ]:


lr = LinearRegression()
lr.fit(X_train, y_train)

# Look at predictions on training and validation set
print("RMSE on Training set :", rmse_cv_train(lr).mean())
print("RMSE on Test set :", rmse_cv_test(lr).mean())
y_train_pred = lr.predict(X_train)
y_test_pred = lr.predict(X_test)


# In[ ]:


# Plot residuals
plt.scatter(y_train_pred, y_train_pred - y_train, c = "blue", marker = "s", label = "Training data")
plt.scatter(y_test_pred, y_test_pred - y_test, c = "lightgreen", marker = "s", label = "Validation data")
plt.title("Linear regression")
plt.xlabel("Predicted values")
plt.ylabel("Residuals")
plt.legend(loc = "upper left")
plt.hlines(y = 0, xmin = 10.5, xmax = 13.5, color = "red")
plt.show()


# Ridge Regression

# In[ ]:


ridge = RidgeCV(alphas = [0.01, 0.03, 0.06, 0.1, 0.3, 0.6, 1, 3, 6, 10, 30, 60])
ridge.fit(X_train, y_train)
alpha = ridge.alpha_
print("Best alpha :", alpha)


# In[ ]:


print("Try again for more precision with alphas centered around " + str(alpha))
ridge = RidgeCV(alphas = [alpha * .6, alpha * .65, alpha * .7, alpha * .75, alpha * .8, alpha * .85, 
                          alpha * .9, alpha * .95, alpha, alpha * 1.05, alpha * 1.1, alpha * 1.15,
                          alpha * 1.25, alpha * 1.3, alpha * 1.35, alpha * 1.4], 
                cv = 10)
ridge.fit(X_train, y_train)
alpha = ridge.alpha_
print("Best alpha :", alpha)


# In[ ]:


print("Ridge RMSE on Training set :", rmse_cv_train(ridge).mean())
print("Ridge RMSE on Test set :", rmse_cv_test(ridge).mean())
y_train_rdg = ridge.predict(X_train)
y_test_rdg = ridge.predict(X_test)


# In[ ]:


# Plot residuals
plt.scatter(y_train_rdg, y_train_rdg - y_train, c = "blue", marker = "s", label = "Training data")
plt.scatter(y_test_rdg, y_test_rdg - y_test, c = "lightgreen", marker = "s", label = "Validation data")
plt.title("Linear regression with Ridge regularization")
plt.xlabel("Predicted values")
plt.ylabel("Residuals")
plt.legend(loc = "upper left")
plt.hlines(y = 0, xmin = 10.5, xmax = 13.5, color = "red")
plt.show()


# In[ ]:


# Plot important coefficients
coefs = pd.Series(ridge.coef_, index = X_train.columns)
print("Ridge picked " + str(sum(coefs != 0)) + " features and eliminated the other " +        str(sum(coefs == 0)) + " features")
imp_coefs = pd.concat([coefs.sort_values().head(10),
                     coefs.sort_values().tail(10)])
imp_coefs.plot(kind = "barh")
plt.title("Coefficients in the Ridge Model")
plt.show()


# Lasso Model

# In[ ]:


lasso = LassoCV(alphas = [0.0001, 0.0003, 0.0006, 0.001, 0.003, 0.006, 0.01, 0.03, 0.06, 0.1, 
                          0.3, 0.6, 1], 
                max_iter = 50000, cv = 10)
lasso.fit(X_train, y_train)
alpha = lasso.alpha_
print("Best alpha :", alpha)


# In[ ]:


print("Try again for more precision with alphas centered around " + str(alpha))
lasso = LassoCV(alphas = [alpha * .6, alpha * .65, alpha * .7, alpha * .75, alpha * .8, 
                          alpha * .85, alpha * .9, alpha * .95, alpha, alpha * 1.05, 
                          alpha * 1.1, alpha * 1.15, alpha * 1.25, alpha * 1.3, alpha * 1.35, 
                          alpha * 1.4], 
                max_iter = 50000, cv = 10)
lasso.fit(X_train, y_train)
alpha = lasso.alpha_
print("Best alpha :", alpha)


# In[ ]:


print("Lasso RMSE on Training set :", rmse_cv_train(lasso).mean())
print("Lasso RMSE on Test set :", rmse_cv_test(lasso).mean())
y_train_las = lasso.predict(X_train)
y_test_las = lasso.predict(X_test)


# In[ ]:


# Plot residuals
plt.scatter(y_train_las, y_train_las - y_train, c = "blue", marker = "s", label = "Training data")
plt.scatter(y_test_las, y_test_las - y_test, c = "lightgreen", marker = "s", label = "Validation data")
plt.title("Linear regression with Lasso regularization")
plt.xlabel("Predicted values")
plt.ylabel("Residuals")
plt.legend(loc = "upper left")
plt.hlines(y = 0, xmin = 10.5, xmax = 13.5, color = "red")
plt.show()


# In[ ]:


# Plot important coefficients
coefs = pd.Series(lasso.coef_, index = X_train.columns)
print("Lasso picked " + str(sum(coefs != 0)) + " features and eliminated the other " +        str(sum(coefs == 0)) + " features")
imp_coefs = pd.concat([coefs.sort_values().head(10),
                     coefs.sort_values().tail(10)])
imp_coefs.plot(kind = "barh")
plt.title("Coefficients in the Lasso Model")
plt.show()


# ElasticNet Model

# In[ ]:


elasticNet = ElasticNetCV(l1_ratio = [0.1, 0.3, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1],
                          alphas = [0.0001, 0.0003, 0.0006, 0.001, 0.003, 0.006, 
                                    0.01, 0.03, 0.06, 0.1, 0.3, 0.6, 1, 3, 6], 
                          max_iter = 50000, cv = 10)
elasticNet.fit(X_train, y_train)
alpha = elasticNet.alpha_
ratio = elasticNet.l1_ratio_
print("Best l1_ratio :", ratio)
print("Best alpha :", alpha )


# In[ ]:


print("Try again for more precision with l1_ratio centered around " + str(ratio))
elasticNet = ElasticNetCV(l1_ratio = [ratio * .85, ratio * .9, ratio * .95, ratio, ratio * 1.05, ratio * 1.1, ratio * 1.15],
                          alphas = [0.0001, 0.0003, 0.0006, 0.001, 0.003, 0.006, 0.01, 0.03, 0.06, 0.1, 0.3, 0.6, 1, 3, 6], 
                          max_iter = 50000, cv = 10)
elasticNet.fit(X_train, y_train)
if (elasticNet.l1_ratio_ > 1):
    elasticNet.l1_ratio_ = 1    
alpha = elasticNet.alpha_
ratio = elasticNet.l1_ratio_
print("Best l1_ratio :", ratio)
print("Best alpha :", alpha )


# In[ ]:


print("Now try again for more precision on alpha, with l1_ratio fixed at " + str(ratio) + 
      " and alpha centered around " + str(alpha))
elasticNet = ElasticNetCV(l1_ratio = ratio,
                          alphas = [alpha * .6, alpha * .65, alpha * .7, alpha * .75, alpha * .8, alpha * .85, alpha * .9, 
                                    alpha * .95, alpha, alpha * 1.05, alpha * 1.1, alpha * 1.15, alpha * 1.25, alpha * 1.3, 
                                    alpha * 1.35, alpha * 1.4], 
                          max_iter = 50000, cv = 10)
elasticNet.fit(X_train, y_train)
if (elasticNet.l1_ratio_ > 1):
    elasticNet.l1_ratio_ = 1    
alpha = elasticNet.alpha_
ratio = elasticNet.l1_ratio_
print("Best l1_ratio :", ratio)
print("Best alpha :", alpha )


# In[ ]:


print("ElasticNet RMSE on Training set :", rmse_cv_train(elasticNet).mean())
print("ElasticNet RMSE on Test set :", rmse_cv_test(elasticNet).mean())
y_train_ela = elasticNet.predict(X_train)
y_test_ela = elasticNet.predict(X_test)


# In[ ]:


# Plot residuals
plt.scatter(y_train_ela, y_train_ela - y_train, c = "blue", marker = "s", label = "Training data")
plt.scatter(y_test_ela, y_test_ela - y_test, c = "lightgreen", marker = "s", label = "Validation data")
plt.title("Linear regression with ElasticNet regularization")
plt.xlabel("Predicted values")
plt.ylabel("Residuals")
plt.legend(loc = "upper left")
plt.hlines(y = 0, xmin = 10.5, xmax = 13.5, color = "red")
plt.show()


# In[ ]:


# Plot important coefficients
coefs = pd.Series(elasticNet.coef_, index = X_train.columns)
print("ElasticNet picked " + str(sum(coefs != 0)) + " features and eliminated the other " +  str(sum(coefs == 0)) + " features")
imp_coefs = pd.concat([coefs.sort_values().head(10),
                     coefs.sort_values().tail(10)])
imp_coefs.plot(kind = "barh")
plt.title("Coefficients in the ElasticNet Model")
plt.show()


# In[ ]:





# Send the prices

# In[ ]:


test
test_ID = test.Id
test =test.drop(columns=['Id'])


# In[ ]:


y_price = elasticNet.predict(test)


# In[ ]:


sub=pd.DataFrame()
sub['Id'] = test_ID
sub['SalePrice']=y_price


# In[ ]:


sub.to_csv('submission.csv',index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




