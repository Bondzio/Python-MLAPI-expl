#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn import linear_model
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


sample = pd.read_csv('/kaggle/input/mlbio1/sample_submission.csv')
test = pd.read_csv('/kaggle/input/mlbio1/test.csv')
train = pd.read_csv('/kaggle/input/mlbio1/train.csv')


# In[ ]:


sample


# In[ ]:


train.head()


# In[ ]:


train['smoking_status'].fillna('nan').value_counts()


# In[ ]:


mean_bmi = train['bmi'].mean()
train['bmi'] = train['bmi'].fillna(mean_bmi)
test['bmi'] = test['bmi'].fillna(mean_bmi)


# In[ ]:


test.head()


# In[ ]:


train['ever_married'].value_counts()


# In[ ]:


ever_married_dict = {'Yes': 1, 'No':0 }


# In[ ]:


train['ever_married'] =train['ever_married'].replace(ever_married_dict)
test['ever_married'] = test['ever_married'].replace(ever_married_dict)


# In[ ]:


train['smoking_status'].unique()


# In[ ]:





# In[ ]:


feautures_list = ['age', 'avg_glucose_level', 'bmi', 'ever_married']


# In[ ]:





# In[ ]:





# In[ ]:


clf = linear_model.SGDClassifier(max_iter=1000,  loss='log', penalty = 'l1')


clf.fit(train[feautures_list], train['stroke'])


# In[ ]:


clf.predict_proba(test[feautures_list])


# In[ ]:


prediction = clf.predict_proba(test[feautures_list])[:,1]


# In[ ]:


sample['stroke'] = prediction


# In[ ]:


sample.to_csv('submi2.csv', index = None )


# In[ ]:




