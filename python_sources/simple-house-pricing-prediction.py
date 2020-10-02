#!/usr/bin/env python
# coding: utf-8

# This is my second Kaggle conpetition I decided to take part. I'd like to study using regression for a prediction and I believe I can succeed a bit. 

# The next block is done for me.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew
from scipy.special import boxcox1p
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import Lasso, LassoCV


# In[ ]:


train_dataset = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/train.csv')
test_dataset = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/test.csv')


# The variable *test* I need to keep *Id* value

# In[ ]:


x_train = train_dataset.select_dtypes(include=['float','int'])
x_test = test_dataset.select_dtypes(include=['float','int'])
test   = test_dataset.select_dtypes(include=['float','int'])
#mean = x_train.mean(axis=0)
#std = x_train.std(axis=0)


# There are some NuN values that don't let me solve the task

# In[ ]:


x_train=x_train.fillna(x_train.mean())
x_test=x_test.fillna(x_train.mean())


# In[ ]:


x_train = x_train[x_train['GrLivArea']<4000]
x_train['SalePrice']=np.log(x_train['SalePrice'])


# In[ ]:


x_train.drop('Id', axis=1, inplace=True)
x_test.drop('Id', axis=1, inplace=True)


# In[ ]:


x=x_train.drop('SalePrice', axis=1)
y=x_train['SalePrice']


# In[ ]:


rsc=RobustScaler()
x=rsc.fit_transform(x)
x_test=rsc.transform(x_test)


# In[ ]:


model=Lasso(alpha =0.001, random_state=1)
model.fit(x,y)


# In[ ]:


predict=model.predict(x_test)
predicts=np.exp(predict)
result=pd.DataFrame({'Id':test.Id, 'SalePrice':predicts})
result.to_csv('submission.csv', index=False)


# In[ ]:


print(result)

