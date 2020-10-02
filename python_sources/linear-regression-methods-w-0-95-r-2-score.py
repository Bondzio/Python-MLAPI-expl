#!/usr/bin/env python
# coding: utf-8

# In this Kernel, we are going to visualize and then regressively predict the ground energy states of molecules based on certain quantum parameters. 
# 
# Packages used:
# 1. pandas/numpy
# 2. seaborn/matplotlib
# 3. scikit learn
# 
# Table of Contents
# 1. Data Visualization
# 2. Linear Models(Ordinary Linear Regression, Lasso, Ridge)
# 3. Model Interpretation
# 
# Read on if you want to learn any of these!

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import sklearn
import seaborn as sns

df = pd.read_csv('../input/roboBohr.csv')


# **VISUALIZATION**

# In[ ]:


df.head()
X = df.iloc[:,:1275]
y = df.iloc[:,-1:]
#drop unnamed id column and pubchem column
df = df.drop(['Unnamed: 0','pubchem_id'],axis=1)
#rename target feature to Energy State
df = df.rename(columns={'Eat':'Energy_State'})


# In[ ]:


print('We have {0} rows/training examples and {1} columns/features'.format(df.shape[0],df.shape[1]-1))
#describe various parameters of each feature, exclude count statistic because included in rows
df.iloc[:,1:(len(df.columns)-1)].describe()[1:]


# Using descriptive statistics is sometimes difficult to understand, but we have too many dimensions to plot in 2 or 3 dimensions. Instead, we will selectively pick some random columns to plot. 

# In[ ]:


#regression plotting b/w features and target variable
ax=sns.regplot(df['4'],df['Energy_State'])
ax=sns.regplot(df['8'],df['Energy_State'])
ax.set(xlabel='Feature Value', ylabel='Energy State')


# In[ ]:


#Violinplot some features
ax1=sns.violinplot(df[['100','200','300']],palette='muted',orient='v')
#Note skewed distribution and outliers


# In[ ]:


#lets try some transformations to make distributions more normal
logs = np.log(df[['100','200','300']]+1) # +1 because log(0) is NAN
ax1=sns.violinplot(logs,palette='muted',orient='v')


# In[ ]:


#Lets try square rooting as well
squares = (df[['100','200','300']]+1)*0.5 # +1 because log(0) is NAN
ax1=sns.violinplot(squares,palette='muted',orient='v')


# In[ ]:


#violinplot of target variable
sns.violinplot(df['Energy_State'])
#Note that chemical bonding energy is measured from 0 negatively


# **Linear Models**

# In[ ]:


#scales features so they have means of 0, std of 1
def normalization(X_train, X_test):
    from sklearn import preprocessing
    scaler = preprocessing.StandardScaler().fit(X_train) 
    #mean = scaler.mean_
    #std = scaler.var_
    X_train_std = scaler.transform(X_train)
    X_test_std = scaler.transform(X_test)
    return X_train_std, X_test_std, scaler
#splits dataset in to test and train sets
def test_train_split(X,y,split=0.33):
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split)
    return X_train,X_test,y_train,y_test


# In[ ]:


def lin_reg_workflow(X,y):
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn import linear_model
    #split into test/train data and normalize
    X_train, X_test, y_train, y_test = test_train_split(X,y)
    X_train, X_test, scaler = normalization(X_train,X_test)
    y_train,y_test = y_train.values.ravel(),y_test.values.ravel()
    
    regr = linear_model.LinearRegression()
    regr.fit(X_train,y_train)
    y_pred = regr.predict(X_test)
    
    print("Lin Reg Mean squared error: %.2f"% mean_squared_error(y_test, y_pred))
    print('Lin Reg Variance score aka r^2: %.2f' % r2_score(y_test, y_pred))
    
    coefficients = regr.coef_
    return y_test,y_pred,coefficients

OLE_y_test,OLE_y_pred,OLE_coef = lin_reg_workflow(X,y)
print('Linear Regression coefficients', OLE_coef)


# Clearly, linear regression is a very poor predictor of Energy States. We can attribute this to the non-normal distribution of features ansd non-linear relationship between the features and the target variable.
# Now, it is also possible that some of the features were poor predictors or had low variances. We will now implement Lasso and Ridge Regression, which are feature selectors and linear regressors, and compare performances.
# Notice that some coefficients are relatively large(10^2) while some are very small(10^-2). We will see how other linear regression methods can deal with this

# In[ ]:


#Lasso regression is L1 regression and is often used for feature selection as well
#Note that sklearn offers built-in cross val
def lassoCV_reg_workflow(X,y):
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.linear_model import LassoCV
    #split into test/train and normalize
    X_train, X_test, y_train, y_test = test_train_split(X,y)
    X_train, X_test, scaler = normalization(X_train,X_test)
    #sklearn has trouble with panda df, convert to matrix
    y_train,y_test = y_train.values.ravel(),y_test.values.ravel()
    #set of alphas we use to cross validate
    alphas = np.logspace(-4, 4, 14) #10**start, 10**end, num_samples,
    lasso_cv = LassoCV(max_iter=10**6,alphas=alphas)
    lasso_cv.fit(X_train,y_train)
    y_pred = lasso_cv.predict(X_test)
    
    print("Lasso CV Mean squared error:", mean_squared_error(y_test, y_pred))
    print('Lasso CV Variance score aka r^2:', r2_score(y_test, y_pred))
    
    coefficients = lasso_cv.coef_
    #best alpha chosen by cv
    alpha = lasso_cv.alpha_ 
    return y_test,y_pred,coefficients,alpha

lasso_y_test,lasso_y_pred,lasso_coef,lasso_alpha = lassoCV_reg_workflow(X,y)
print('Lasso CV Regression coefficients', lasso_coef)
print('Lasso CV Regression optimal alpha', lasso_alpha)


# In[ ]:


#Ridge regression is L2 regression and tends to offer higher accuracy than L1
def ridgeCV_reg_workflow(X,y):
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.linear_model import RidgeCV
    #split into test/train and normalize
    X_train, X_test, y_train, y_test = test_train_split(X,y)
    X_train, X_test, scaler = normalization(X_train,X_test)
    #another method to convert panda dataframes into normal arrays
    y_train,y_test = y_train.values.ravel(),y_test.values.ravel()
    alphas = np.logspace(-4, 4, 14) #10**start, 10**end,num_samples,
    
    ridge_cv = RidgeCV(alphas=alphas)
    ridge_cv.fit(X_train,y_train)
    y_pred = ridge_cv.predict(X_test)
    
    print("Ridge CV Mean squared error:", mean_squared_error(y_test, y_pred))
    print('Ridge CV Variance score aka r^2:', r2_score(y_test, y_pred))
    
    coef = ridge_cv.coef_
    alpha = ridge_cv.alpha_
    return y_test,y_pred,coef,alpha

ridge_y_test,ridge_y_pred,ridge_coef,ridge_alpha = ridgeCV_reg_workflow(X,y)
print('Ridge CV Regression coefficients', ridge_coef)
print('Ridge CV Regression optimal alpha', ridge_alpha)


# **Model Interpretation**

# Note how Lasso Regression forces many of its coefficients to be zero, rather than arbitrarily close. This is a result of the underlying cost function, which minimizes coefficients to zero, rather than arbitrarily close to 0, as Ridge does.

# In[ ]:


#Finding number of coefficients equal to zero
#Ordinary Linear Regression
plt.figure()
ax1 = sns.distplot(OLE_coef,bins=15)
ax1.set_title("OLE Distribution of Coefficients")
ax1.set(xlabel="Distribution of Coefficient Values")
plt.show()


# In[ ]:


#Lasso and Ridge CV Coefficients
#lasso
plt.figure()
ax2 = sns.distplot(lasso_coef,bins=15)
ax2.set_title("LassoCV Distribution of Coefficients")
ax2.set(xlabel="Distribution of Coefficient Values")
plt.show()

#Ridge
plt.figure()
ax3 = sns.distplot(ridge_coef,bins=15)
ax3.set_title("RidgeCV Distribution of Coefficients")
ax3.set(xlabel="Distribution of Coefficient Values")
plt.show()


# Finally, lets examine the distribution of our error value i.e. the distribution of how far off we were. 

# In[ ]:


def error_histogram(y_pred,y_test):    
    MAE = abs(y_pred-y_test)
    MAE = MAE[:(len(MAE)-1)]
    print('min', y_test.min())
    print('max', y_test.max())
    print('MAE max', MAE.max())
    print('MAE min', MAE.min())
    MAE = [i for i in MAE if i<10 ]
    return sns.distplot(MAE,bins=50)


# In[ ]:


#Ordinary Linear Regression
#We limit the distribution from errors of 0 to 10 because of outliers changing the graph shape
plt.figure()
ax = error_histogram(OLE_y_pred,OLE_y_test)
ax.set(xlabel="Error Residual")
plt.show()


# In[ ]:


#Lasso CV
#Ordinary Linear Regression
    
plt.figure()
ax = error_histogram(lasso_y_pred,lasso_y_test)
ax.set(xlabel="Error Residual")
plt.show()
#Notice the much lower max MAE!


# In[ ]:


#Ridge CV
    
plt.figure()
ax = error_histogram(ridge_y_pred,ridge_y_test)
ax.set(xlabel="Error Residual")
plt.show()


# In this kernel, we went over using advanced linear regression methods, such as Lasso and Ridge Linear Regression with Cross Validation via scikit learn for predicting ground state energies of molecules. If you have any questions, feel free to leave one in the comments and if you learned something from this kernel, please leave an upvote!
