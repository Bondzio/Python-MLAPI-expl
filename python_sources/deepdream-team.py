#!/usr/bin/env python
# coding: utf-8

# # Problem Statement

# This project is focues on testing the impact of regularzation techniques Lasso and Ridge and compare it with the plain Linear Regression model

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt 

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# # Data Cleaning and EDA

# In[2]:


# load the dataset
train = pd.read_csv("../input"+'/train.csv')
test = pd.read_csv("../input"+'/test.csv')
# Store test ID for output step
# Drop the 'SalePrice' and 'Id' from the treining datadrame
# Store 'SalePrice' as the target column y
test_ID = test.pop('Id') 
y = train.pop('SalePrice')
train.pop('Id');
train.shape, y.shape, test.shape


# ### Distripution of y values

# In[3]:


#histogram
sns.distplot(y);


# In[4]:


baseline = np.mean(y)
print('Baseline score = ',baseline)


# ### The heatmap of columns correlation

# In[5]:


sns.heatmap(train.corr(), square=True, center=0);


# In[6]:


# Concatenate Training and Testing lists 
# Fill the NAN values with "NA" as a group of not applicable 
lst = [train, test]
concat_list = pd.concat(lst)
# concat_list.shape
concat_list = concat_list.fillna('NA')


# # Preprocessing and Modeling

# In[7]:


# Encode the categorical columns 
# Seperate the Training and Testing lists
concat_list = pd.get_dummies(concat_list)
train_Encoded = concat_list.iloc[:len(y),:]
test_Encoded = concat_list.iloc[len(y):,:]


# In[8]:


# Rescale the columns so we can compare apples with apples 
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
train_Encoded_ss = pd.DataFrame(ss.fit_transform(train_Encoded));
test_Encoded_ss = pd.DataFrame(ss.transform(test_Encoded));


# In[9]:


# Split the Training list to a sub-training and sub-testing lists 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train_Encoded_ss,y,shuffle=True)


# ### model 1

# In[26]:


# Initiate Linear Regression model
# fit it 
# then get the the model score
# store the model predictions 
from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(X_train,y_train)
print('Test Score = ', reg.score(X_test, y_test), 'Train Score = ', reg.score(X_train, y_train))
reg_y_hat = reg.predict(test_Encoded_ss)
# # output file 
reg_y_hat = pd.DataFrame(reg_y_hat)
reg_y_hat.columns=['SalePrice']
reg_output = pd.concat([test_ID, reg_y_hat], axis=1)
# reg_output.to_csv()
reg_output.head()


# ### model 2

# In[11]:


# Initiate RidgeCV model
# fit it 
# then get the the model score
# store the model predictions 
from sklearn.linear_model import RidgeCV
rid = RidgeCV()
rid.fit(X_train,y_train)
print('Test Score = ', rid.score(X_test, y_test), 'Train Score = ', rid.score(X_train,y_train))
rid_y_hat = rid.predict(test_Encoded_ss)
# output file 
rid_y_hat = pd.DataFrame(rid_y_hat)
rid_y_hat.columns=['SalePrice']
rid_output = pd.concat([test_ID, rid_y_hat], axis=1)
# rid_output.to_csv()
rid_output.head()


# ### model 3

# In[13]:


# Initiate LassoCV model
# fit it 
# then get the the model score
# store the model predictions 
from sklearn.linear_model import LassoCV
lasso = LassoCV()
lasso.fit(X_train,y_train)
print('Test Score = ', lasso.score(X_test, y_test), 'Train Score = ', lasso.score(X_train, y_train))
lasso_y_hat = lasso.predict(test_Encoded_ss)
# output file 
# lasso_y_hat = pd.DataFrame(lasso_y_hat)
# lasso_y_hat.columns=['SalePrice']
# lasso_output = pd.concat([test_ID, lass_y_hat], axis=1)
# lasso_output.head()


# In[17]:


# output file 
lasso_y_hat = pd.DataFrame(lasso_y_hat)
lasso_y_hat.columns=['SalePrice']
lasso_output = pd.concat([test_ID, lasso_y_hat], axis=1)
# lasso_output.to_csv()
lasso_output.head()


# # Evaluation and Conceptual Understanding

# In[18]:


from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics


# ### Evaluating `Linear Regression` model

# In[19]:


# Perform 5-fold cross validation
reg_scores = cross_val_score(reg, X_train, y_train, cv=5);
print("Cross-validated scores:", reg_scores);
print("Mean of Ccoss-validated scores:", reg_scores.mean());


# ### Evaluating `Linear Regression with Ridge` model

# In[20]:


# Perform 5-fold cross validation
rid_scores = cross_val_score(rid, X_train, y_train, cv=5);
print("Cross-validated scores:", rid_scores);
print("Mean of Ccoss-validated scores:", rid_scores.mean());


# ### Evaluating `Linear Regression with Lasso` model

# In[21]:


print('features kept = ',sum(lasso.coef_!=0), 'features eliminated = ',sum(lasso.coef_==0))
print('alpha = ',lasso.alpha_)
print('the number of folds = ', lasso.cv) # the none means 3 folds by default


# In[22]:


# Perform 5-fold cross validation
scores = cross_val_score(lasso, X_train, y_train, cv=5);
print("Cross-validated scores:", scores);
print("Mean of Ccoss-validated scores:", scores.mean());


# # Conclusion and Recommendations

# The plain Linear Regression tend to overfit, becuse it performes perfectly on the training data, but in the test data sometimes it performes worse than the baseline (based on the the training-testing split). This behavior is expected because of the number of features is too large. We need to do regularized regression to solve the overfitting problem.
# Two regularized regression were tested, Ridge Regression and Lasso Regression. After applying ridge regression slitly improvment were noticed in compare to lasso regression wich shows at least 10% improvment in compare to plain Linear Regression. We concluded that becuse of the large number of features the least valuable features must be elemenated to improve the model. The figure below shows the Lasso's coefficients for each feature, and some looks like they have most significant impact while most were set to weight zero.  Further investigation well be focused on the features with hiest coefficients

# In[24]:


plt.figure(figsize=(12,10)) 
lass_coef = lasso.coef_
plt.plot(range(len(train_Encoded_ss.columns)), lass_coef)
plt.xticks(range(len(train_Encoded_ss.columns)), train_Encoded_ss.columns.values, rotation=60)
plt.margins(0.02)
plt.xlabel('Features')
plt.ylabel('Coefficients')
plt.show()

