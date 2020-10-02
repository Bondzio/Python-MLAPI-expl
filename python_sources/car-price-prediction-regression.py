#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


filepath = '../input/vehicle-dataset-from-cardekho/car data.csv'


# In[ ]:


df = pd.read_csv(filepath)
df 


# In[ ]:


df.Car_Name.value_counts()


# In[ ]:


df.Owner.value_counts()


# In[ ]:


target_col = 'Present_Price'
print(df[target_col].unique())
print('-----------------------')
print(df[target_col].value_counts())
print('-----------------------')
print(df.dtypes)
print('-----------------------')
print(df.isna().sum())


# In[ ]:


df_cat = df[['Fuel_Type', 'Seller_Type', 'Transmission']]
from sklearn.preprocessing import LabelEncoder
df_cat = df_cat.apply(LabelEncoder().fit_transform)
df_cat


# In[ ]:


new_df = pd.concat([df.select_dtypes(exclude='object'), df_cat], axis=1)
new_df


# In[ ]:


df = new_df


# In[ ]:


y = df[target_col]
X = df.drop(columns=[target_col])
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)


# In[ ]:


para = list(range(3, 10, 2))
print(para)


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score, mean_absolute_error
results = {}
for n in para:
    print('para=', n)
    model = KNeighborsRegressor(n_neighbors=n)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    #accu = accuracy_score(y_true=y_test, y_pred=preds)
    #f1 = f1_score(y_true=y_test, y_pred=preds, average='micro')
    mae = mean_absolute_error(y_true=y_test, y_pred=preds)
    print(mae)
    #print(classification_report(y_true=y_test, y_pred=preds))
    print('--------------------------')
    results[n] = mae


# In[ ]:


import matplotlib.pylab as plt
# sorted by key, return a list of tuples
lists = sorted(results.items()) 
p, a = zip(*lists) # unpack a list of pairs into two tuples
plt.plot(p, a)
plt.show()


# In[ ]:


best_para = min(results, key=results.get)
print('best para', best_para)
print('value', results[best_para])

