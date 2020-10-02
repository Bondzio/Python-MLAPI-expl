#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


from sklearn.model_selection import KFold, cross_val_score, train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score


# In[ ]:


train = pd.read_csv('../input/competitive-data-science-predict-future-sales/sales_train.csv')
test = pd.read_csv('../input/competitive-data-science-predict-future-sales/test.csv')
categories = pd.read_csv('../input/competitive-data-science-predict-future-sales/item_categories.csv')
item = pd.read_csv('../input/competitive-data-science-predict-future-sales/items.csv')
shop = pd.read_csv('../input/competitive-data-science-predict-future-sales/shops.csv')


# In[ ]:


train.head()


# In[ ]:


train['date'] = pd.to_datetime(train.date,format="%d.%m.%Y")


# In[ ]:


sns.distplot(train["item_price"])
print('Skewness: %f' % train['item_price'].skew(), ", highly skewed")


# In[ ]:


test.columns
train['ID'] = test.ID


# In[ ]:


test.head()


# In[ ]:


train_id = train.ID
test_id = test.ID
y_sales = train.item_cnt_day


# In[ ]:


try:
    train.drop(labels=['ID','date','item_cnt_day'], axis=1, inplace=True)
except Exception as e:
    pass


# In[ ]:


train.head()


# In[ ]:


try:
    test.drop(labels=['ID'], axis=1, inplace=True)
except Exception as e:
    pass


# In[ ]:


test.head()


# In[ ]:


combined_data = pd.concat([train,test], ignore_index=True)
combined_data.sample(5)


# In[ ]:


combined_data.columns


# In[ ]:


combined_data ["item_price"] = combined_data["item_price"].fillna((combined_data["item_price"].mode()[0] ))
combined_data ["date_block_num"] = combined_data["date_block_num"].fillna((combined_data["date_block_num"].mode()[0] ))
combined_data.isna()
combined_data.isnull().sum()


# In[ ]:


X_train = combined_data[:len(train)]
X_test = combined_data[len(train):]
trainX, testX, trainY, testY = train_test_split(X_train, y_sales,test_size = 0.2, random_state = 0)


# In[ ]:


from  sklearn.preprocessing  import StandardScaler
slc= StandardScaler()
trainX = slc.fit_transform(trainX)
X_test = slc.transform(X_test)
testX = slc.transform(testX)


# In[ ]:


num_folds = 10
seed = 0
scoring = 'neg_mean_squared_error'
kfold = KFold(n_splits=num_folds, random_state=seed)


# In[ ]:


model = XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1, max_depth = 10, alpha = 10, n_estimators = 70)
score_= cross_val_score(model, trainX, trainY, cv=kfold, scoring=scoring)
model.fit(trainX, trainY)
predictions = model.predict(testX)
print(r2_score(testY, predictions))
rmse = np.sqrt(mean_squared_error(testY, predictions))


# In[ ]:


rmse = np.sqrt(mean_squared_error(testY, predictions))
rmse


# In[ ]:




