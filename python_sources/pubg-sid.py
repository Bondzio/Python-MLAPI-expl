#!/usr/bin/env python
# coding: utf-8

# In[22]:


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


# In[23]:


data = pd.read_csv('../input/train_V2.csv')


# In[24]:


data = data.loc[:,'assists':]
data.head()


# In[25]:


from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data.loc[:,'matchType'] = le.fit_transform(data.loc[:,'matchType'])


# In[26]:


data.head()


# In[27]:


from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(categorical_features = [12])


# In[28]:


data = data.dropna()
data = ohe.fit_transform(data).toarray()


# In[29]:


data


# In[30]:


data = pd.DataFrame(data)
data.head()


# In[31]:


data = data.iloc[:,1:]
data = data.iloc[:500000,:] #Try iterating here, check for different number of training examples 
data.head()


# In[32]:


X_train  = data.iloc[:,:-1]
y_train = data.iloc[:,-1]


# In[33]:


X_train.head()


# In[34]:


y_train


# In[35]:


from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(n_estimators=70)  
regressor.fit(X_train, y_train)  
regressor.score(X_train, y_train)


# In[36]:


#from xgboost import XGBRegressor

#XGBModel = XGBRegressor()
#XGBModel.fit(X_train, y_train, verbose=False)
#XGBModel.score(X_train, y_train)
# Gives 89.95% score


# In[37]:


X_test = pd.read_csv('../input/test_V2.csv')


# In[38]:


X_test1 = pd.read_csv('../input/test_V2.csv')
X_test1.dropna()
X_test1.head()


# In[39]:


def make_submission(prediction, subject_name):
    my_submission = pd.DataFrame({'Id':X_test1.Id,'winPlacePerc':prediction})
    my_submission.to_csv('{}'.format(subject_name),index=False)
    print('Submission file has been made')
    
X_test.head()    


# In[40]:


X_test = X_test.loc[:,'assists':]
le2 = LabelEncoder()
X_test.loc[:,'matchType'] = le2.fit_transform(X_test.loc[:,'matchType'])
ohe2 = OneHotEncoder(categorical_features = [12])
X_test = X_test.dropna()
X_test = ohe2.fit_transform(X_test).toarray()
X_test = pd.DataFrame(X_test)
X_test = X_test.iloc[:,1:]
X_test.head()


# In[41]:


predictions = regressor.predict(X_test)
predictions


# In[42]:


make_submission(predictions,'SiddharthSRandomForest2.csv')

