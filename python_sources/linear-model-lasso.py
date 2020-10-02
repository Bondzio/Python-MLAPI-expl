#!/usr/bin/env python
# coding: utf-8

# # **Lasso Regression**

# Lasso regression, or the Least Absolute Shrinkage and Selection Operator, is a modification of linear regression.
# 
# In Lasso, the loss function is modified to minimize the complexity of the model by limiting the sum of the absolute values of the model coefficients.
# 
# The loss function for Lasso Regression can be expressed as below:
# 
# **Loss function = OLS + alpha * summation (absolute values of the magnitude of the coefficients)**
# 
# In the above loss function, alpha is the penalty parameter we need to select. 
# 
# Using an l1 norm constraint forces some weight values to zero to allow other coefficients to take non-zero values.

# # Ridge Regression

# Ridge regression is an extension of linear regression where the loss function is modified to minimize the complexity of the model. 
# 
# This modification is done by adding a penalty parameter that is equivalent to the square of the magnitude of the coefficients.
# 
# **Loss function = OLS + alpha * summation (squared coefficient values)**
# 
# In the above loss function, alpha is the parameter we need to select. 
# 
# A low alpha value can lead to over-fitting, whereas a high alpha value can lead to under-fitting.

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


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib

import matplotlib.pyplot as plt
from scipy.stats import skew
from scipy.stats.stats import pearsonr

get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina' #set 'png' here when working on notebook")
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


train = pd.read_csv("../input/train.csv")
test = pd.read_csv("../input/test.csv")

all_data = pd.concat((train.loc[:,'MSSubClass':'SaleCondition'],
                      test.loc[:,'MSSubClass':'SaleCondition']))

train["SalePrice"] = np.log1p(train["SalePrice"])
numeric_feats = all_data.dtypes[all_data.dtypes != "object"].index

skewed_feats = train[numeric_feats].apply(lambda x: skew(x.dropna())) 
skewed_feats = skewed_feats[skewed_feats > 0.75]
skewed_feats = skewed_feats.index

all_data[skewed_feats] = np.log1p(all_data[skewed_feats])

all_data = pd.get_dummies(all_data)
all_data = all_data.fillna(all_data.mean())

X_train = all_data[:train.shape[0]]
X_test = all_data[train.shape[0]:]
y = train.SalePrice


# ### Lasso Linear Model

# In[ ]:


from sklearn.linear_model import Ridge, RidgeCV, ElasticNet, LassoCV, LassoLarsCV
from sklearn.model_selection import cross_val_score

def rmse_cv(model):
    rmse= np.sqrt(-cross_val_score(model, X_train, y, scoring="neg_mean_squared_error", cv = 5))
    return(rmse)


# In[ ]:


#model_ridge = Ridge()

#alphas = [0.05, 0.1, 0.3, 1, 3, 5, 10, 15, 30, 50, 75]
#cv_ridge = [rmse_cv(Ridge(alpha = alpha)).mean() 
            #for alpha in alphas]

#cv_ridge = pd.Series(cv_ridge, index = alphas)
#cv_ridge.plot(title = "Validation - Just Do It")
#plt.xlabel("alpha")
#plt.ylabel("rmse")

#cv_ridge.min()


# In[ ]:


model_lasso = LassoCV(alphas = [1, 0.1, 0.001, 0.0005]).fit(X_train, y)
rmse_cv(model_lasso).mean()
coef = pd.Series(model_lasso.coef_, index = X_train.columns)


# In[ ]:


preds = pd.DataFrame({"preds":model_lasso.predict(X_train), "true":y})
preds["residuals"] = preds["true"] - preds["preds"]

lasso_preds = np.expm1(model_lasso.predict(X_test))
preds = lasso_preds

solution = pd.DataFrame({"id":test.Id, "SalePrice":preds})
solution.to_csv("submission.csv", index = False)

