#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import plotly.express as px
from random import randint
from tpot import TPOTRegressor
from sklearn.model_selection import train_test_split

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# ## Reading Data
# It reads the data provided by the host

# In[ ]:


df_stores = pd.read_csv("/kaggle/input/walmart-recruiting-store-sales-forecasting/stores.csv")
df_features = pd.read_csv('/kaggle/input/walmart-recruiting-store-sales-forecasting/features.csv.zip')
df_train = pd.read_csv('/kaggle/input/walmart-recruiting-store-sales-forecasting/train.csv.zip')
df_test = pd.read_csv('/kaggle/input/walmart-recruiting-store-sales-forecasting/test.csv.zip')


# ## Converting Date
# It convert to date format in order to handle datetime.

# In[ ]:


df_train.Date =  pd.to_datetime(df_train.Date) 
df_test.Date =  pd.to_datetime(df_test.Date) 
df_features.Date = pd.to_datetime(df_features.Date)


# ## Data Exploration
# During data exploration, I breafly observed data variables distribution

# In[ ]:


df_train.describe()


# In[ ]:


df_features.describe()


# ## Handling Outliers
# In order to avoid outliers I just clipped the data based on assumption like: negative sales does not make sense at least from the context I had so far on the data provided and considering that probably top and bottom 1% could be treated as outliers

# In[ ]:


df_train_clipped = df_train
df_train_clipped['Weekly_Sales'] = df_train.Weekly_Sales.clip(0,df_train.Weekly_Sales.max())
df_train_clipped.describe()


# In[ ]:


df_features_clipped = df_features
df_features_clipped['Temperature'] = df_features.Temperature.clip(df_features.Temperature.quantile(0.01),df_features.Temperature.quantile(0.99))
df_features_clipped['Fuel_Price'] = df_features.Fuel_Price.clip(df_features.Fuel_Price.quantile(0.01),df_features.Fuel_Price.quantile(0.99))
df_features_clipped['MarkDown1'] = df_features.MarkDown1.clip(df_features.MarkDown1.quantile(0.01),df_features.MarkDown1.quantile(0.99))
df_features_clipped['MarkDown2'] = df_features.MarkDown2.clip(df_features.MarkDown2.quantile(0.01),df_features.MarkDown2.quantile(0.99))
df_features_clipped['MarkDown3'] = df_features.MarkDown3.clip(df_features.MarkDown3.quantile(0.01),df_features.MarkDown3.quantile(0.99))
df_features_clipped['MarkDown4'] = df_features.MarkDown4.clip(df_features.MarkDown4.quantile(0.01),df_features.MarkDown4.quantile(0.99))
df_features_clipped['MarkDown5'] = df_features.MarkDown5.clip(df_features.MarkDown5.quantile(0.01),df_features.MarkDown5.quantile(0.99))
df_features_clipped['CPI'] = df_features.CPI.clip(df_features.CPI.quantile(0.01),df_features.CPI.quantile(0.99))
df_features_clipped['Unemployment'] = df_features.Unemployment.clip(df_features.Unemployment.quantile(0.01),df_features.Unemployment.quantile(0.99))
df_features_clipped.describe()


# In[ ]:


df_features_clipped.describe()


# Just wondering on the size of sales time series

# In[ ]:


gTrain = df_train.groupby(['Store','Dept']).count()['Date']
gTrain.value_counts()


# ## Ploting series
# Again exploring features time series visualy to have a superficial understanding curves characteristics and on the effect of holidays and markdown action.

# In[ ]:


#dept = randint(1,45)
dept = 77
sel_dept = df_train_clipped['Dept']== dept
df = df_train_clipped[sel_dept]
fig = px.line(df, x='Date', y='Weekly_Sales', color='Store', 
              width=1200, height=800, title='Time Series with Rangeslider')

fig.update_xaxes(rangeslider_visible=True)
fig.show()


# In[ ]:


#store = randint(1,45)
store = 45
sel_store = df_train_clipped['Store']== store
df = df_train_clipped[sel_store]
fig = px.line(df, x='Date', y='Weekly_Sales', color='Dept', 
              width=1200, height=800, title='Time Series with Rangeslider')

fig.update_xaxes(rangeslider_visible=True)
fig.show()


# In[ ]:


store = randint(1,45)
sel_store = df_test['Store']== store
df1 = df_test[sel_store]
fig = px.line(df1, x='Date', y='IsHoliday', color='Dept', 
              width=1200, height=800, title='Time Series with Rangeslider')

fig.update_xaxes(rangeslider_visible=True)
fig.show()


# In[ ]:


# store = randint(1,45)
# sel_store = feature['Store']== store
# df_test = test[sel_store]
fig = px.line(df_features, x='Date', y='Temperature', color='Store', 
              width=1200, height=800, title='Time Series with Rangeslider')

fig.update_xaxes(rangeslider_visible=True)
fig.show()


# ## Adding a column to point out a specific holiday
# I have decided to build up a variable that no only tell about if it is holiday, but to say specifically which holiday it is.

# * Super Bowl: 12-Feb-10, 11-Feb-11, 10-Feb-12, 8-Feb-13
# * Labor Day: 10-Sep-10, 9-Sep-11, 7-Sep-12, 6-Sep-13
# * Thanksgiving: 26-Nov-10, 25-Nov-11, 23-Nov-12, 29-Nov-13
# * Christmas: 31-Dec-10, 30-Dec-11, 28-Dec-12, 27-Dec-13

# In[ ]:


def getHoliday(date):
    if date in ['2010-02-12','2011-02-11','2012-02-10','2013-02-08']:
        return str('super_bowl')
    if date in ['2010-09-10','2011-09-09','2012-09-07','2013-09-06']:
        return str('labor_day')
    if date in ['2010-11-26','2011-11-25','2012-11-23','2013-11-29']:
        return str('thx_giving')
    if date in ['2010-12-31','2011-12-30','2012-12-28','2013-12-13']:
        return str('xmas')
    else:
        return 'not_holiday'


# In[ ]:


df_features_clipped['Holiday'] = df_features_clipped.apply(lambda x: getHoliday(x['Date']),axis=1)


# In[ ]:


df_features_clipped.drop(columns='IsHoliday', inplace=True)


#    I also applied NA treatment replacing na by feature median

# In[ ]:


df_features_clipped.fillna(df_features_clipped.median(), inplace=True)


# Here, another decision was to make use of week of year representation, e.g. week 26 other than 2013-06-28 and it will be used as a feature

# In[ ]:


df_features_clipped['Week_of_Year'] = df_features_clipped.Date.dt.week


# In[ ]:


df_features_clipped.tail()


# Putting together features, train and stores data sets.

# In[ ]:


df_train_feat = pd.merge(df_train_clipped,df_features_clipped, how='inner', on=['Store','Date'])


# In[ ]:


df_train_feat.drop(columns='IsHoliday', inplace=True)


# In[ ]:


df_train_feat = pd.merge(df_train_feat,df_stores, how='inner', on=['Store'])


# In[ ]:


df_train_feat.info()


# Putting together features, test and stores data sets.

# In[ ]:


df_test_feat = pd.merge(df_test,df_features_clipped, how='inner', on=['Store','Date'])


# In[ ]:


df_test_feat = pd.merge(df_test_feat,df_stores, how='inner', on=['Store'])


# In[ ]:


df_test_feat.info()


# ## ML Modeling
# To generate ML model, I took advantage TPOT automl framework 

# Preparing data to feed framework
# > I decided to select as features to feed the model: Temperature, Fuel Price, Markdown1-5, CPI, Unemployment, Week_of_Year, Size of Store, Store Type, Holiday information, Dept.

# In[ ]:


def getInputData(df):
    numeric_cols = ['Temperature', 'Fuel_Price', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', 'CPI','Unemployment', 'Week_of_Year','Size']
    
    stores_cols = pd.get_dummies(df['Store'])
    dept_cols = pd.get_dummies(df['Dept'])
    holiday_cols = pd.get_dummies(df['Holiday'])
    # weekOfYear_cols = pd.get_dummies(df['Week_of_Year'])
    type_cols = pd.get_dummies(df['Type'])
    
    input_data = pd.concat([df[numeric_cols],
              stores_cols, dept_cols, holiday_cols, type_cols], axis=1)
    return input_data


# In[ ]:


input_data = getInputData(df_train_feat)


# In[ ]:


target = df_train_feat['Weekly_Sales']


# Model selection and training

# In[ ]:


# splitting train and test data
X_train, X_test, y_train, y_test = train_test_split(input_data, target,
                                                    train_size=0.80, test_size=0.20)


# This part is responsible for tunning and selecting a model.

# In[ ]:


model = TPOTRegressor(generations=5, population_size=20, 
                                   verbosity=2, n_jobs=3, scoring = 'neg_mean_absolute_error')
model.fit(X_train, y_train)


# In[ ]:


print(model.score(X_test,y_test))


# In[ ]:


model.export('/kaggle/working/sales_forecast.py')


# ## Predicting for test file provided by challenge host

# In[ ]:


X_validation = getInputData(df_test_feat)


# In[ ]:


Weekly_Sales = model.predict(X_validation)


# In[ ]:


pd.Series(Weekly_Sales)


# In[ ]:


keys = ['Store','Dept','Date']
df_submission = pd.concat([df_test_feat[keys],pd.Series(Weekly_Sales, name='Weekly_Sales')], axis=1)


# In[ ]:


df_submission


# In[ ]:


df_submission['Id'] = df_submission.apply(lambda x: '_'.join([str(x['Store']),str(x['Dept']),str(x['Date'])]),axis=1)
df_submission['Id'] = df_submission.Id.apply(lambda x: x.split()[0])


# In[ ]:


challenge_file = df_submission[['Id','Weekly_Sales']]


# In[ ]:


challenge_file


# In[ ]:


challenge_file.to_csv('/kaggle/working/df_submission.csv',index=False)

