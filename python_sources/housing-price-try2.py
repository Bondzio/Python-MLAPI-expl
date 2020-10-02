#!/usr/bin/env python
# coding: utf-8

# ## import pandas as pd
# 
# 

# In[ ]:


import pandas as pd

train = pd.read_csv('../input/home-data-for-ml-course/train.csv')
test = pd.read_csv('../input/home-data-for-ml-course/test.csv')


# filling NaN

# In[ ]:


res = train.isnull().sum()
print(res[70:])


# In[ ]:


train.LotFrontage = train.LotFrontage.fillna(0)
train.Alley = train.Alley.fillna('None')
train.MasVnrType = train.MasVnrType.fillna('None')
train.MasVnrArea = train.MasVnrArea.fillna(0)
train.BsmtQual = train.BsmtQual.fillna('noBsm')
train.BsmtCond = train.BsmtCond.fillna('noBsm')
train.BsmtExposure = train.BsmtExposure.fillna('noBsm')
train.BsmtFinType1 = train.BsmtFinType1.fillna('noBsm')
train.BsmtFinType2 = train.BsmtFinType2.fillna('noBsm')
train.Electrical = train.Electrical.fillna('noEle')
train.FireplaceQu = train.FireplaceQu.fillna('noFire')
train.GarageType = train.GarageType.fillna('noGar')
train.GarageYrBlt = train.GarageYrBlt.fillna('noGar')
train.GarageFinish = train.GarageFinish.fillna('noGar')
train.GarageQual = train.GarageQual.fillna('noGar')
train.GarageCond = train.GarageCond.fillna('noGar')
train.PoolQC = train.PoolQC.fillna('noPool')
train.Fence = train.Fence.fillna('noFen')
train.MiscFeature = train.MiscFeature.fillna('noMisc')


# In[ ]:


train[['PoolArea', 'PoolQC', 'Fence', 'MiscFeature', 'MiscVal']][108:]


# convert string to int

# In[ ]:


import binascii

for col in train.columns[2:]:
    for i in range(len(train[col])):
        if type(train[col][i])==type(str()):
            train[col][i] = int(train[col][i].encode().hex(),16)


# preparing for the test

# In[ ]:


y = train.SalePrice
X = train[train.columns[1:-1]]


# In[ ]:


from sklearn.model_selection import train_test_split
train_X, test_X, train_y, test_y = train_test_split(X,y)


# find out what is the best 'features'

# In[ ]:


from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_log_error
import random

model = DecisionTreeRegressor()

features = []
for item in X.columns:
    features += [item]

model.fit(train_X, train_y)
preds = model.predict(test_X)
min_err = mean_squared_log_error(test_y, preds)

count = 0

while count <= 0xffffffff:
    # feeding data with candidate 'features'
    num = random.randint(1,79)
    tmp_features = random.sample(features, num)

    tmp_train_X = train_X[tmp_features]
    model.fit(tmp_train_X, train_y)
    # perform test
    tmp_test_X = test_X[tmp_features]
    preds = model.predict(tmp_test_X)
    msle = mean_squared_log_error(test_y, preds)
    # apply the test result
    if min_err > msle:
        min_err = msle
        min_features = tmp_features
        count = 0
    else:
        count += 1

features = min_features
print(features)
model.fit(train_X[features], train_y)
print(min_err)


# In[ ]:


print(len(features))


# In[ ]:


test.MSZoning = test.MSZoning.fillna(-1)
test.Exterior1st = test.Exterior1st.fillna(-1)
test.BsmtFullBath = test.BsmtFullBath.fillna(-1)
test.BsmtHalfBath = test.BsmtHalfBath.fillna(-1)
test.TotalBsmtSF = test.TotalBsmtSF.fillna(-1)
test.KitchenQual = test.KitchenQual.fillna(-1)
test.LotFrontage = test.LotFrontage.fillna(0)
test.Alley = test.Alley.fillna('None')
test.MasVnrType = test.MasVnrType.fillna('None')
test.MasVnrArea = test.MasVnrArea.fillna(0)
test.BsmtQual = test.BsmtQual.fillna('noBsm')
test.BsmtCond = test.BsmtCond.fillna('noBsm')
test.BsmtExposure = test.BsmtExposure.fillna('noBsm')
test.BsmtFinType1 = test.BsmtFinType1.fillna('noBsm')
test.BsmtFinType2 = test.BsmtFinType2.fillna('noBsm')
test.Electrical = test.Electrical.fillna('noEle')
test.FireplaceQu = test.FireplaceQu.fillna('noFire')
test.GarageType = test.GarageType.fillna('noGar')
test.GarageYrBlt = test.GarageYrBlt.fillna('noGar')
test.GarageFinish = test.GarageFinish.fillna('noGar')
test.GarageQual = test.GarageQual.fillna('noGar')
test.GarageCond = test.GarageCond.fillna('noGar')
test.PoolQC = test.PoolQC.fillna('noPool')
test.Fence = test.Fence.fillna('noFen')
test.MiscFeature = test.MiscFeature.fillna('noMisc')


# In[ ]:


import binascii

for col in test.columns:
    for i in range(len(test[col])):
        if type(test[col][i])==type(str()):
            test[col][i] = int(test[col][i].encode().hex(),16)


# In[ ]:


test[features].isnull().sum()


# making submission

# In[ ]:


print(len(features))
X_test = test[features]
preds = model.predict(X_test)


# In[ ]:


submission = pd.read_csv('../input/home-data-for-ml-course/sample_submission.csv')
submission.head()


# In[ ]:


submission.SalePrice = preds


# In[ ]:


submission.to_csv('submission_2.csv', index=False)

