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


import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# In[ ]:


df_train = pd.read_csv('/kaggle/input/dasprodatathon/train.csv')
df_test = pd.read_csv('/kaggle/input/dasprodatathon/test.csv')


# In[ ]:


print("Dataframe Train")
display(df_train)

print("Dataframe Test")
display(df_test)


# In[ ]:


def missing_percentage(df):
    total = df.isnull().sum().sort_values(ascending = False)[df.isnull().sum().sort_values(ascending = False) != 0]
    percent = round(df.isnull().sum().sort_values(ascending = False)/len(df)*100,2)[round(df.isnull().sum().sort_values(ascending = False)/len(df)*100,2) != 0]
    return pd.concat([total, percent], axis=1, keys=['Total','Percent'])

missing_percentage(df_train)


# In[ ]:


missing_percentage(df_test)


# In[ ]:


df_train.info()


# In[ ]:


display(df_train.describe())


# In[ ]:


fig, ax = plt.subplots(figsize=(15,15))
k = 19
cols = df_train.corr().nlargest(k, 'Price')['Price'].index
cm = np.corrcoef(df_train[cols].values.T)
sns.heatmap(cm, annot=True, square=True, fmt='.2f',yticklabels=cols.values, xticklabels=cols.values, ax=ax)


# In[ ]:


cat_col = ['Year Built', 'Year Renovated', 'Waterfront', 'Zipcode', 'Grade']
for col in cat_col:
    print("UNIQUE VALUE ",col,df_train[col].unique())


# In[ ]:


sns.distplot(df_train['Price'])


# In[ ]:


plt.bar(df_train['Grade'], df_train['Price'])
plt.show()


# In[ ]:


sns.boxplot(df_train['Waterfront'], df_train['Price'])


# In[ ]:


plt.subplots(figsize=(20,10))
sns.distplot(df_train['Year Built'])


# In[ ]:


plt.subplots(figsize=(40,15))
sns.barplot(df_train['Year Built'], df_train['Price'])


# In[ ]:


# df_train = df_train.loc[df_train['Year Renovated'] >0]
df_train['Year Renovated'].unique()


# In[ ]:


plt.subplots(figsize=(25,10))
sns.boxplot(df_train['Year Renovated'], df_train['Price'])


# In[ ]:


sns.scatterplot(df_train['Living Area'], df_train['Price'])


# In[ ]:


sns.distplot(df_train['Living Area'])


# In[ ]:


sns.scatterplot(df_train['Above the Ground Area'], df_train['Price'])


# In[ ]:


sns.distplot(df_train['Above the Ground Area'])


# In[ ]:


sns.distplot(df_train['Bedrooms'])
# berarti ini kategorical


# In[ ]:


sns.boxplot(df_train['Bedrooms'], df_train['Price'])
print(df_test.Bedrooms.unique())


# In[ ]:


print(df_train.Floors.unique())
sns.distplot(df_train['Floors'])


# In[ ]:


sns.scatterplot(df_train['Floors'], df_train['Price'])
# nanti dislicing jadi diatas x <= 1 , 1<x<2 , x>=2


# In[ ]:


sns.distplot(df_train['Bathrooms'])


# In[ ]:


print(df_train.Bathrooms.unique())
sns.boxplot(df_train['Bathrooms'], df_train['Price'])


# In[ ]:


plt.subplots(figsize=(30,15))
display(sns.distplot(df_train['Total Area']))
display(sns.distplot(df_test['Total Area']))


# In[ ]:


sns.scatterplot(df_train['Total Area'], df_train['Price'])


# In[ ]:


print(df_train.View.unique())
sns.scatterplot(df_train['View'], df_train['Price'])


# In[ ]:


sns.scatterplot(df_train['Condition'], df_train['Price'])
# ntar jadiin boolean jadi < 3 dan > 3


# In[ ]:


sns.distplot(df_train['Basement Area'])


# In[ ]:


sns.scatterplot(df_train['Basement Area'], df_train['Price'])
# bikin satu featureuntuk menentukan dia punya basement apa ga


# In[ ]:


sns.distplot(df_train['Zipcode'])
print(df_train['Zipcode'].unique())


# In[ ]:


sns.scatterplot(df_train['Zipcode'], df_train['Price'])


# In[ ]:


sns.distplot(df_train['Latitude'])


# In[ ]:


sns.scatterplot(df_train['Latitude'], df_train['Price'])


# In[ ]:


sns.distplot(df_train['Longitude'])


# In[ ]:


sns.scatterplot(df_train['Longitude'], df_train['Price'])


# In[ ]:


fig, ax = plt.subplots(figsize=(15,15))
plt.scatter(df_train['Latitude'], df_train['Longitude'], c=df_train['Price'])
plt.colorbar()
plt.title("Lat Lon chart")
plt.show()


# **Categorical Features :**
# - Condition
# - View 
# - Zipcode
# - Bedrooms
# - Bathrooms
# - Floor
# - Year Built
# - Year Renovated
# - Lat
# - Long <br> <br>
# **Numerical Features :**
# - Living Area
# - Total Area
# - Floors
# - Waterfront
# - Grade
# - Basement Area
# - Above the Ground Area
# - Neighbors Living Area
# - Neighbors Total Area

# ## Feature Engineering ##
# floors : nanti dislicing jadi diatas x <= 1 , 1<x<2 , x>=2 <br>
# condition :ntar jadiin boolean jadi < 3 dan > 3<br>
# view : biarin <br>
# Zipcode : <98100 dan >98100<br>
# Bedrooms : biarin<br>
# Bathrooms : biarin<br>
# Year built : biarin<br>
# Year Renovated : biarin<br>
# isRenovated : boolean<br>
# lat lon :biarin <br>
# hasBasement : 1 0 boolean

# In[ ]:


all_df = [df_train, df_test]
for df in all_df:
    df['isRenovated'] = df['Year Renovated'] != 0
    df['hasBasement'] = df['Basement Area'] > 0
display(df_train)


# In[ ]:


id_test = df_test['ID']
X_train = df_train.copy()
Y_train = df_train["Price"]
X_train = X_train.drop(['ID', 'Price'], axis=1)
X_test = df_test.drop(['ID'], axis=1)
X_train.shape ,  X_test.shape , Y_train.shape


# In[ ]:


from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error


from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor


# In[ ]:


lnr = LinearRegression()
lnr.fit(X_train, Y_train)
print(cross_val_score(lnr, X_train, Y_train))
pred_lnr = lnr.predict(X_train)
print(mean_squared_error(Y_train, pred_lnr))


# In[ ]:


xgbr = GradientBoostingRegressor()
xgbr.fit(X_train, Y_train)
print(cross_val_score(xgbr, X_train, Y_train))
pred_xgbr = xgbr.predict(X_train)
print(mean_squared_error(Y_train, pred_xgbr))


# In[ ]:


dst = DecisionTreeRegressor()
dst.fit(X_train, Y_train)
print(cross_val_score(dst, X_train, Y_train))
pred_dst = dst.predict(X_train)
print(mean_squared_error(Y_train, pred_dst))


# In[ ]:


rfc = RandomForestRegressor()
rfc.fit(X_train, Y_train)
print(cross_val_score(rfc, X_train, Y_train))
pred_rfc = rfc.predict(X_train)
print(mean_squared_error(Y_train, pred_rfc))


# In[ ]:


svr = SVR()
svr.fit(X_train, Y_train)
print(cross_val_score(svr, X_train, Y_train))
pred_svr = svr.predict(X_train)
print(mean_squared_error(Y_train, pred_svr))


# pake yang gradient boosting yaaa

# In[ ]:


test_pred = xgbr.predict(X_test)
submit_df = pd.DataFrame()
submit_df['ID'] = id_test
submit_df['Price'] = test_pred
display(submit_df.head())


# In[ ]:


submission = submit_df.to_csv("submission.csv")

