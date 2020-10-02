#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from pylab import rcParams
import seaborn  as sb


# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
rcParams['figure.figsize']=7,5
plt.style.use('seaborn-whitegrid')


# In[30]:


sales_train = pd.read_csv("../input/Train.csv")
sales_test = pd.read_csv("../input/Test.csv")

sales_data=pd.concat([sales_train, sales_test] , ignore_index = True)
sales_data.head()


# In[31]:


sales_data.info()


# In[32]:


sales_data.isnull().sum()


# In[59]:


sb.distplot(sales_train["Item_Outlet_Sales"])


# In[33]:


plt.bar(sales_train["Outlet_Type"],sales_train["Item_Outlet_Sales"])


# In[34]:


sales_train.groupby('Outlet_Establishment_Year')['Item_Outlet_Sales'].mean().plot.bar()


# In[35]:


sales_data["Item_Weight"] = sales_data["Item_Weight"].fillna((sales_data["Item_Weight"].mean() ))
sales_data.isnull().sum()


# In[36]:


sales_data["Item_Outlet_Sales"] = sales_data["Item_Outlet_Sales"].fillna((sales_data["Item_Outlet_Sales"].mean() ))
sales_data.isnull().sum()


# In[37]:


sales_data ["Outlet_Size"] = sales_data["Outlet_Size"].fillna((sales_data["Outlet_Size"].mode()[0] ))
sales_data.isnull().sum()


# In[38]:


sales_data[sales_data['Item_Visibility']==0].head()


# In[39]:


Zero_Item_Visibility =(sales_data['Item_Visibility']==0)
print (Zero_Item_Visibility.sum())

sales_data.loc[Zero_Item_Visibility,'Item_Visibility']=sales_data["Item_Visibility"].mean() 

Zero_Item_Visibility =(sales_data['Item_Visibility']==0)
print (Zero_Item_Visibility.sum())


# In[40]:


sales_data['new_Item_Identifier']=sales_data['Item_Identifier'].apply(lambda x:x[0:2])
sales_data['new_Item_Identifier']=sales_data['new_Item_Identifier'].replace({'FD':'food','NC':'non-consumable','DR':'drinks'})

sales_data['new_Item_Identifier'].value_counts()


# In[41]:


sales_data['Item_Fat_Content'].value_counts()


# In[42]:


sales_data['Item_Fat_Content']=sales_data['Item_Fat_Content'].replace({'LF':'Low Fat','reg':'Regular','low fat':'Low Fat'})
sales_data['Item_Fat_Content'].value_counts()


# In[43]:


# sales_data["Outlet_Year"]= 2013-sales_data["Outlet_Establishment_Year"]


# In[44]:


sales_data.drop(['Item_Identifier','Outlet_Establishment_Year'],axis=1,inplace=True)


# In[45]:


sales_data = pd.get_dummies(sales_data, columns = [ "new_Item_Identifier","Item_Fat_Content", "Item_Type", "Outlet_Identifier", "Outlet_Size", "Outlet_Location_Type", "Outlet_Type" ], drop_first = True)

sales_data.head()


# In[46]:


y=sales_data['Item_Outlet_Sales']
sales_data.drop(['Item_Outlet_Sales'],axis=1,inplace=True)
x=sales_data

X_train = x[:len(sales_train)]
X_test = x[len(sales_train):]

y_train = y[:len(sales_train)]


# In[50]:


import sklearn
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import KFold, cross_val_score, train_test_split


# In[51]:


Xtraining, Xtesting, Ytraining, Ytesting = train_test_split(X_train, y_train,test_size = 0.2, random_state = 0)


# In[52]:


slc= StandardScaler()
Xtraining = slc.fit_transform(Xtraining)
Xtesting=slc.transform(Xtesting)

X_test=slc.transform(X_test)


# In[53]:


import xgboost
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score


# In[54]:


num_folds = 10
seed = 0
scoring = 'neg_mean_squared_error'
kfold = KFold(n_splits=num_folds, random_state=seed)


# In[55]:


model = XGBRegressor(n_estimators=70 , learning_rate = .1)
score_= cross_val_score(model,Xtraining, Ytraining, cv=kfold, scoring=scoring)
model.fit(Xtraining, Ytraining)
predictions = model.predict(Xtesting)
print(r2_score(Ytesting, predictions))
rmse = np.sqrt(mean_squared_error(Ytesting, predictions))


# In[57]:


rmse = np.sqrt(mean_squared_error(Ytesting, predictions))
rmse


# In[58]:


test_id = sales_test.Item_Identifier
Y_pred = model.predict(X_test)
my_submission = pd.DataFrame({'Id': test_id, 'SalePrice': Y_pred})
my_submission.to_csv('submission_sales.csv', index=False)


# In[ ]:




