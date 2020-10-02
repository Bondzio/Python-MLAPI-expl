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


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from sklearn.preprocessing import LabelBinarizer,LabelEncoder,StandardScaler,MinMaxScaler
from sklearn.linear_model import LogisticRegression,SGDClassifier,LinearRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.model_selection import train_test_split
import keras
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from keras.models import Sequential
from keras.layers import Dense,LSTM
import tensorflow as tf


# In[ ]:


train_df = pd.read_csv("../input/covid19-global-forecasting-week-4/train.csv")
test_df = pd.read_csv("../input/covid19-global-forecasting-week-4/test.csv")
submission = pd.read_csv("../input/covid19-global-forecasting-week-4/submission.csv")


# In[ ]:


train_df.head()


# In[ ]:


test_df.head()


# In[ ]:


train_df.isna().sum()


# In[ ]:


test_df.isna().sum()


# In[ ]:


train_df['Province_State'].fillna("",inplace = True)
test_df['Province_State'].fillna("",inplace = True)


# In[ ]:


train_df['Country_Region'] = train_df['Country_Region'] + ' ' + train_df['Province_State']
test_df['Country_Region'] = test_df['Country_Region'] + ' ' + test_df['Province_State']
del train_df['Province_State']
del test_df['Province_State']


# In[ ]:


train_df.head()


# In[ ]:


def split_date(date):
    date = date.split('-')
    date[0] = int(date[0])
    if(date[1][0] == '0'):
        date[1] = int(date[1][1])
    else:
        date[1] = int(date[1])
    if(date[2][0] == '0'):
        date[2] = int(date[2][1])
    else:
        date[2] = int(date[2])    
    return date
train_df.Date = train_df.Date.apply(split_date)
test_df.Date = test_df.Date.apply(split_date)


# In[ ]:


train_df.head()


# In[ ]:


year = []
month = []
day = []
for i in train_df.Date:
    year.append(i[0])
    month.append(i[1])
    day.append(i[2])


# In[ ]:


train_df['Year'] = year
train_df['Month'] = month
train_df['Day'] = day
del train_df['Date']


# In[ ]:


year = []
month = []
day = []
for i in test_df.Date:
    year.append(i[0])
    month.append(i[1])
    day.append(i[2])


# In[ ]:


test_df['Year'] = year
test_df['Month'] = month
test_df['Day'] = day
del test_df['Date']
del train_df['Id']
del test_df['ForecastId']


# In[ ]:


train_df.head()


# In[ ]:


test_df.head()


# In[ ]:


train_df.Year.unique(),test_df.Year.unique()


# In[ ]:


del train_df['Year']
del test_df['Year']


# In[ ]:


train_df['ConfirmedCases'] = train_df['ConfirmedCases'].apply(int)
train_df['Fatalities'] = train_df['Fatalities'].apply(int)


# In[ ]:


cases = train_df.ConfirmedCases
fatalities = train_df.Fatalities
del train_df['ConfirmedCases']
del train_df['Fatalities']


# In[ ]:


lb = LabelEncoder()
train_df['Country_Region'] = lb.fit_transform(train_df['Country_Region'])
test_df['Country_Region'] = lb.transform(test_df['Country_Region'])


# In[ ]:


plt.figure(figsize = (10,10))
corr = train_df.corr()
sns.heatmap(corr , mask=np.zeros_like(corr, dtype=np.bool) , cmap=sns.diverging_palette(-100,0,as_cmap=True) , square = True)


# In[ ]:


scaler = MinMaxScaler()
x_train = scaler.fit_transform(train_df.values)
x_test = scaler.transform(test_df.values)


# In[ ]:


from xgboost import XGBRegressor


# In[ ]:


rf = XGBRegressor(n_estimators = 2100 , random_state = 0 , max_depth = 22)
rf.fit(x_train,cases)


# In[ ]:


cases_pred = rf.predict(x_test)
cases_pred


# In[ ]:


cases_pred = np.around(cases_pred,decimals = 0)
cases_pred


# In[ ]:


x_train_cas = []
for i in range(len(x_train)):
    x = list(x_train[i])
    x.append(cases[i])
    x_train_cas.append(x)
x_train_cas[0]


# In[ ]:


x_train_cas = np.array(x_train_cas)


# In[ ]:


rf = XGBRegressor(n_estimators = 2100 , random_state = 0 , max_depth = 22)
rf.fit(x_train_cas,fatalities)


# In[ ]:


x_test_cas = []
for i in range(len(x_test)):
    x = list(x_test[i])
    x.append(cases_pred[i])
    x_test_cas.append(x)
x_test_cas[0]


# In[ ]:


x_test_cas = np.array(x_test_cas)


# In[ ]:


fatalities_pred = rf.predict(x_test_cas)
fatalities_pred


# In[ ]:


fatalities_pred = np.around(fatalities_pred,decimals = 0)
fatalities_pred


# In[ ]:


submission['ConfirmedCases'] = cases_pred
submission['Fatalities'] = fatalities_pred


# In[ ]:


submission.head()


# In[ ]:


submission.to_csv("submission.csv" , index = False)


# In[ ]:




