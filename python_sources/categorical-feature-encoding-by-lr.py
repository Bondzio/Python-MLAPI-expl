#!/usr/bin/env python
# coding: utf-8

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


train = pd.read_csv('/kaggle/input/cat-in-the-dat-ii/train.csv')
test = pd.read_csv('/kaggle/input/cat-in-the-dat-ii/test.csv')


# In[ ]:


train.head()


# As most of the data is in 0's and 1's format OneHot Encoding can be used for catagorical encoding 

# But before encoding we need to pass to clean and arrange it for the encoding.

# In[ ]:


train_id = train['id']
test_id = test['id']
target = train['target']
train.drop(['target','id'],axis=1,inplace=True)
test.drop('id',axis=1,inplace=True)
train_test_set = pd.concat([train,test]) 


# In[ ]:


train_test_set.shape


# In[ ]:


dummy = pd.get_dummies(train_test_set,columns=train_test_set.columns,drop_first=True,sparse=True)


# In[ ]:


train_ohe = dummy.iloc[:train.shape[0],:]
test_ohe = dummy.iloc[train.shape[0]:, :]

train_ohe = train_ohe.sparse.to_coo().tocsr()
test_ohe = test_ohe.sparse.to_coo().tocsr()


# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


# In[ ]:


train_x,test_x,train_y,test_y = train_test_split(train_ohe,target,test_size = 0.25)


# In[ ]:


LR = LogisticRegression(C=0.1,max_iter=1000)


# In[ ]:


LR.fit(train_x,train_y)


# In[ ]:


y_pred = LR.predict(test_x)


# In[ ]:


from sklearn.metrics import roc_auc_score as auc
score = auc(test_y,y_pred)


# In[ ]:


print(score)


# In[ ]:


LR.fit(train_ohe,target)


# In[ ]:


y_pred2 = LR.predict(test_ohe)


# In[ ]:


sub_df = pd.DataFrame({'id': test_id, 'target' : y_pred2})
sub_df.to_csv("LR_pred.csv",index=False)


# In[ ]:


from sklearn.model_selection import cross_val_score
LR_accuracies = cross_val_score(estimator = LR, X = train_ohe, y = target, cv = 10)
print("Mean_LR_Acc : ", LR_accuracies.mean())


# In[ ]:


from sklearn.model_selection import cross_val_predict
y = target[:test_ohe.shape[0]]
y_pred_2 = y_pred = cross_val_predict(LR, test_ohe, y, cv=2)


# In[ ]:


sub_df_1 = pd.DataFrame({'id': test_id, 'target' : y_pred_2})
sub_df_1.to_csv("LR_pred_2.csv",index=False)


# We tried to increase the score by cross validating the process

# In[ ]:


from category_encoders.leave_one_out import LeaveOneOutEncoder
LOOE_encoder = LeaveOneOutEncoder()
train_looe = LOOE_encoder.fit_transform(train, target)
test_looe = LOOE_encoder.transform(test)


# In[ ]:


from sklearn.impute import SimpleImputer

my_imputer = SimpleImputer()
imputed_X_train = my_imputer.fit_transform(train_looe)
imputed_X_test = my_imputer.transform(test_looe)


# In[ ]:


from sklearn.metrics import roc_auc_score as auc
t_X,t_x,t_Y,t_y = train_test_split(imputed_X_train,target,test_size=0.25)
LR.fit(t_X,t_Y)
Y_p_x = LR.predict(t_x)
print(auc(Y_p_x,t_y))


# In[ ]:


y_test_pred = LR.predict(imputed_X_test)
sub_df = pd.DataFrame({'id': test_id, 'target' : y_test_pred})
sub_df.to_csv("LR_pred_3.csv",index=False)


# In[ ]:




