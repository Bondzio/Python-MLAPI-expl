#!/usr/bin/env python
# coding: utf-8

# # Sberbank Russian Housing Prices 
# https://www.kaggle.com/c/sberbank-russian-housing-market/
# 
# ## This is a silly model - a quick run to get familiar with uploading & running kernels on Kaggle
# 
# It's yet to have any serious cleaning, transforming, feature engineering, or analysis.
# 
# My goals:
# (1) to get my hands on this new dataset 
# (2) upload a kernel to Kaggle

# ## Define the problem
# 
# Supervised regression: Predict a continuous target, Sale Price, in Test set given labeled Train Set.
# We want generalizable model. We don't need to understand deeply how it works or use the coefficients elsewhere.
# 
# ## Input data
# 
# Train: August 2011 to June 2015
# 
# Test: July 2015 to May 2016
# 
# Target: price_doc

# ## Load up

# In[ ]:


import pandas as pd 
import numpy as np
import matplotlib
from scipy.stats import skew
from sklearn.linear_model import LassoCV
from sklearn.model_selection import cross_val_score

train = pd.read_csv('../input/train.csv', header=0)
test = pd.read_csv('../input/test.csv', header=0)

# Alldata = everything but price_doc, which is only in Train.
alldata = pd.concat((train.loc[:,:'market_count_5000'],test))
alldata = alldata.reset_index(drop=True)


# In[ ]:


train.info()


# In[ ]:


alldata.head()


# What've we got?
#   - Train: 30471 rows, 290 features + target + ID
#   - Test: 7662 rows, 290 features + ID
#   - Features: mix of numeric and categorical
#   - Missing values to clean up

# ## Prepare the dataset

# In[ ]:


def log_transforms(df):
    
    minimum_skew=0.75
   
    numeric_feats = df.dtypes[df.dtypes != "object"].index # Find numeric features
    skewed_feats = df[numeric_feats].apply(lambda x: skew(x.dropna())) # Compute skewness of non-null rows
    skewed_feats = skewed_feats[skewed_feats > minimum_skew] # Only look at indices with minimum skew
    print("Number of features with minimum skew", skewed_feats.shape)
    skewed_feats = skewed_feats.index
    df[skewed_feats] = np.log1p(df[skewed_feats]) # Apply log transform to skewed numeric features

    return df


# In[ ]:


preprocessed = alldata.copy()

print("Log transform...")
preprocessed = log_transforms(preprocessed)

print("Stupid cleaning (placeholder for now)...")
preprocessed = preprocessed.fillna(preprocessed.mean())

print('Entering dummyland:',preprocessed.shape)
preprocessed = pd.get_dummies(preprocessed, dummy_na=True)
print('Leaving dummyland:',preprocessed.shape)

preprocessed.drop(['id'], axis=1,inplace=True) # Drop ID column
X_train = preprocessed[:train.shape[0]] # Take a train-sized chunk out of alldata
X_test = preprocessed[train.shape[0]:] # Everything after
y = np.log1p(train.price_doc)  # log transform the target


# In[ ]:


X_train.head()


# ## Analysis: Lasso with cross-validation

# In[ ]:


def writepredictions(prediction_array,output_file_name):
    Ids=test.id
    df=pd.DataFrame({"id": Ids,"price_doc": prediction_array})
    df.to_csv(output_file_name, header=["id","price_doc"], index=False)


# https://www.kaggle.com/apapiu/house-prices-advanced-regression-techniques/regularized-linear-models/discussion
# 
# Drawing from Alexandru Papiu's excellent notebook on regularized linear regression. 
# 
# I've made a few small adaptations, like normalizing.

# In[ ]:


def rmse_cv(model):
    rmse= np.sqrt(-cross_val_score(model, X_train, y, scoring="neg_mean_squared_error", cv = 5))
    return(rmse)


# In[ ]:


model_lasso = LassoCV(alphas = [1, 0.1, 0.001, 0.0005], normalize=True).fit(X_train, y)
# model_lasso = LassoCV(alphas = [0.1]).fit(X_train, y)
rmse_cv(model_lasso).mean()


# In[ ]:


coef = pd.Series(model_lasso.coef_, index = X_train.columns)
print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " +  str(sum(coef == 0)) + " variables")


# 

# In[ ]:


imp_coef = pd.concat([coef.sort_values().head(10),coef.sort_values().tail(10)])
matplotlib.rcParams['figure.figsize'] = (8.0, 10.0)
imp_coef.plot(kind = "barh")
plt.title("Coefficients in the Lasso Model")


# In[ ]:


# Peek at residuals

matplotlib.rcParams['figure.figsize'] = (6.0, 6.0)

preds = pd.DataFrame({"preds":model_lasso.predict(X_train), "true":y})
preds["residuals"] = preds["true"] - preds["preds"]
preds.plot(x = "preds", y = "residuals",kind = "scatter")


# In[ ]:


model_lasso.score(X_train, y)


# In[ ]:


predictions_lasso=np.expm1(model_lasso.predict(X_test))
writepredictions(predictions_lasso,"Lasso_Model.csv")

