#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# In[ ]:


df = pd.read_csv('../input/train.csv')
test=pd.read_csv('../input/test.csv')


# In[ ]:


df.isnull().sum()


# In[ ]:


df['Gender']=df['Gender'].astype('category')
df['Age']=df['Age'].astype('category')
df['Occupation']=df['Occupation'].astype('category')
df['City_Category']=df['City_Category'].astype('category')
df['Stay_In_Current_City_Years']=df['Stay_In_Current_City_Years'].astype('category')
df['Marital_Status']=df['Marital_Status'].astype('category')
test['Gender']=test['Gender'].astype('category')
test['Age']=test['Age'].astype('category')
test['Occupation']=test['Occupation'].astype('category')
test['City_Category']=test['City_Category'].astype('category')
test['Stay_In_Current_City_Years']=test['Stay_In_Current_City_Years'].astype('category')
test['Marital_Status']=test['Marital_Status'].astype('category')


# In[ ]:


df['Product_Category_2']=df['Product_Category_2'].astype(object)
df['Product_Category_3']=df['Product_Category_3'].astype(object)
df['Product_Category_1']=df['Product_Category_1'].astype(object)
test['Product_Category_2']=test['Product_Category_2'].astype(object)
test['Product_Category_3']=test['Product_Category_3'].astype(object)
test['Product_Category_1']=test['Product_Category_1'].astype(object)


# In[ ]:


df=df.drop('User_ID',axis=1)
df=df.drop('Product_ID',axis=1)
test=test.drop('User_ID',axis=1)
test=test.drop('Product_ID',axis=1)
df=pd.get_dummies(df,drop_first=True)
test=pd.get_dummies(test,drop_first=True)


# In[ ]:


df.shape


# In[ ]:


test.shape


# In[ ]:


df.columns


# In[ ]:


y=df[['Purchase']]
X=df.drop('Purchase',axis=1)


# In[ ]:


X.head()


# In[ ]:


X, test = X.align(test,join='left',axis=1)


# In[ ]:


test.head()


# In[ ]:


from xgboost import XGBRegressor
regressor = XGBRegressor(learning_rate =0.1,
 n_estimators=500,
 max_depth=5,
 min_child_weight=6,
 gamma=0,
  reg_alpha=0.005,
 subsample=0.8,
 colsample_bytree=0.8,
 nthread=4,
 scale_pos_weight=1,
 seed=27)

regressor.fit(X,y)


# In[ ]:


y_pred=regressor.predict(X)


# In[ ]:


sns.scatterplot(x=y['Purchase'],y=y_pred)


# In[ ]:


from sklearn import metrics
metrics.r2_score(y,y_pred)


# In[ ]:


result=pd.read_csv('../input/Sample_Submission.csv')


# In[ ]:


t=pd.read_csv('../input/test.csv')


# In[ ]:


result['User_ID']=t['User_ID']


# In[ ]:


result['Product_ID']=t['Product_ID']


# In[ ]:


result['Purchase']=regressor.predict(test)


# In[ ]:


result.to_csv("result.csv")


# In[ ]:


result.head()


# In[ ]:




