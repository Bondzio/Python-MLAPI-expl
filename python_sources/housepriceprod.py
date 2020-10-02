#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os
import sys
import tqdm
from multiprocessing import  Pool
import warnings
warnings.filterwarnings("ignore")
from math import sqrt
train_on_gpu = False

# Visualisation libs
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_log_error
from sklearn.decomposition import PCA
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from xgboost.sklearn import XGBRegressor


# In[ ]:



sample_submission = pd.read_csv("../input/house-prices-advanced-regression-techniques/sample_submission.csv")
test = pd.read_csv("../input/house-prices-advanced-regression-techniques/test.csv")
train = pd.read_csv("../input/house-prices-advanced-regression-techniques/train.csv")


# In[ ]:


def score(y_actual, y_predicted):
    return sqrt(mean_squared_log_error(y_actual, y_predicted))
    
def fillNaNInfinity(df):
    df.replace([np.inf, -np.inf], np.nan)
    df.fillna(0, inplace=True)
    return df

def fillInfinity(df):
    df.replace([np.inf, -np.inf], np.nan)
    return df


# In[ ]:


nans = pd.isnull(train).sum()
nans[ nans > 0 ]


# In[ ]:


columns_to_remove = nans[ nans > 500 ].reset_index()['index'].tolist()
columns_to_remove


# In[ ]:


train.dtypes.value_counts()


# In[ ]:


data = pd.concat([
    train.loc[:, train.columns != 'SalePrice'], test
])

target = np.log(train['SalePrice'] + 1)

data = fillInfinity(data)

data.shape, target.shape


# In[ ]:


data.drop(labels=columns_to_remove, axis=1, inplace=True)
data.shape


# In[ ]:


data = pd.get_dummies(data)
data.shape


# In[ ]:


imp = Imputer(missing_values='NaN', strategy='most_frequent', copy=False)

imp.fit_transform(data)
data.shape


# In[ ]:


scaler = StandardScaler()

data = scaler.fit_transform(data)

data.shape


# In[ ]:


data[np.isnan(data)] = 0


# In[ ]:


clf = RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42)


# In[ ]:


X = data[:1460]
y = target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
np.savetxt('y.csv',y_test,delimiter=',')
np.savetxt('x.csv',X_test,delimiter=',')


# In[ ]:


clf.fit(X_train, y_train)


# In[ ]:


y_pred =clf.predict(X_test)


# In[ ]:


test = data[1460:]
sample_submission['SalePrice'] = clf.predict(test)
sample_submission['SalePrice'] = np.exp(sample_submission['SalePrice']) - 1
sample_submission.to_csv('submission.csv', index=False)
sample_submission.head()


# In[ ]:


from sklearn.externals import joblib
joblib.dump(clf, 'my_model.pkl', compress=9) 


# In[ ]:


model_clone = joblib.load('my_model.pkl')

