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


from fastai.imports import *
from fastai.tabular import *
from pandas_summary import DataFrameSummary
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from IPython.display import display
from sklearn import metrics


# In[ ]:


df = pd.read_csv('/kaggle/input/bulldoz/Train.csv',low_memory=False,parse_dates=['saledate'])


# In[ ]:


display(df.head())


# In[ ]:


df.drop('SalesID',axis=1,inplace=True)


# In[ ]:


df.columns


# In[ ]:


add_datepart(df, 'saledate')
df.saleYear.head()


# In[ ]:


display(df.loc[:,:].nunique().sort_values(ascending=False))


# In[ ]:


cat_variables = [ 'MachineID', 'ModelID', 'datasource', 'auctioneerID',
       'YearMade', 'UsageBand',
       'fiModelDesc', 'fiBaseModel', 'fiSecondaryDesc', 'fiModelSeries',
       'fiModelDescriptor', 'ProductSize', 'fiProductClassDesc', 'state',
       'ProductGroup', 'ProductGroupDesc', 'Drive_System', 'Enclosure',
       'Forks', 'Pad_Type', 'Ride_Control', 'Stick', 'Transmission',
       'Turbocharged', 'Blade_Extension', 'Blade_Width', 'Enclosure_Type',
       'Engine_Horsepower', 'Hydraulics', 'Pushblock', 'Ripper', 'Scarifier',
       'Tip_Control', 'Tire_Size', 'Coupler', 'Coupler_System',
       'Grouser_Tracks', 'Hydraulics_Flow', 'Track_Type',
       'Undercarriage_Pad_Width', 'Stick_Length', 'Thumb', 'Pattern_Changer',
       'Grouser_Type', 'Backhoe_Mounting', 'Blade_Type', 'Travel_Controls',
       'Differential_Type', 'Steering_Controls','saleElapsed ']
cont_variables = ['SalePrice','MachineHoursCurrentMeter','saleYear', 'saleMonth','saleWeek', 'saleDay', 'saleDayofweek', 'saleDayofyear','saleIs_month_end', 'saleIs_month_start', 'saleIs_quarter_end','saleIs_quarter_start', 'saleIs_year_end', 'saleIs_year_start' ]


# In[ ]:


tmf =Categorify(cat_variables,cont_variables)
tmf(df)


# In[ ]:


df.info()


# In[ ]:


df.UsageBand.cat.set_categories(['High', 'Medium', 'Low'], ordered=True, inplace=True)


# In[ ]:


df.SalePrice = np.log(df.SalePrice)


# In[ ]:


bol_names = df.select_dtypes(include=['bool']).columns
bol_names = bol_names.tolist()
bol_names


# In[ ]:


df[bol_names[2]].unique()


# In[ ]:


from sklearn.preprocessing import LabelBinarizer
clf = LabelBinarizer()
for bol in bol_names:
    df[bol] = clf.fit_transform(np.array(df[bol]).reshape(-1,1))


# In[ ]:


df.info()


# In[ ]:


df.head()


# In[ ]:


df.saleElapsed.dtype


# In[ ]:


from sklearn.impute import SimpleImputer
clf = SimpleImputer(missing_values=np.nan,strategy='most_frequent')
for cat in cat_variables:
    df[cat] = clf.fit_transform(np.array(df[cat]).reshape(-1,1))


# In[ ]:


from sklearn.impute import SimpleImputer
clf = SimpleImputer(strategy='mean')
for cont in cont_variables:
    df[cont] = clf.fit_transform(np.array(df[cont]).reshape(-1,1))


# In[ ]:


display(df.isnull().any().value_counts())


# In[ ]:


tmf = Categorify(cat_variables,cont_variables)
tmf(df)


# In[ ]:


df.info()


# In[ ]:


df.to_csv('bulldozers-raw1.csv',index=False)


# In[ ]:


df_raw = pd.read_csv('bulldozers-raw1.csv',low_memory=False)


# In[ ]:


df_raw.info()


# In[ ]:


df_raw.isnull().any().value_counts()


# In[ ]:


tmf = Categorify(cat_variables,cont_variables)
tmf(df_raw)


# In[ ]:


display(df_raw.T)


# In[ ]:


from sklearn.preprocessing import LabelEncoder
clf = LabelEncoder()
for cat in cat_variables:
    df_raw[cat] = clf.fit_transform(np.ravel(df_raw[cat]))


# In[ ]:


norm = Normalize(cat_variables, cont_variables)


# In[ ]:


norm.apply_train(df_raw)


# In[ ]:


display(df_raw.head().T)


# In[ ]:


def rmse(x,y): return math.sqrt(((x-y)**2).mean())

def print_score(m):
    res = [rmse(m.predict(X_train), y_train), rmse(m.predict(X_valid), y_valid),
                m.score(X_train, y_train), m.score(X_valid, y_valid)]
    if hasattr(m, 'oob_score_'): res.append(m.oob_score_)
    print(res)


# In[ ]:


df ,y = df_raw.drop('SalePrice',axis=1), np.ravel(df_raw[['SalePrice']])


# In[ ]:


def split_vals(a,n): return a[:n].copy(), a[n:].copy()

n_valid = 12000  # same as Kaggle's test set size
n_trn = len(df)-n_valid
raw_train, raw_valid = split_vals(df_raw, n_trn)
X_train, X_valid = split_vals(df, n_trn)
y_train, y_valid = split_vals(y, n_trn)

X_train.shape, y_train.shape, X_valid.shape


# In[ ]:


m = RandomForestRegressor(n_estimators=40, min_samples_leaf=3, max_features=0.5, n_jobs=-1, oob_score=True)
m.fit(df_raw.drop('SalePrice',axis=1), np.ravel(df_raw[['SalePrice']]))
print_score(m)


# In[ ]:





# In[ ]:




