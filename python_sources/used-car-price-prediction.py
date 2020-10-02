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


df=pd.read_csv('/kaggle/input/used-cars-price-prediction/train-data.csv')
df.head()


# In[ ]:


df.corr(method='pearson')


# In[ ]:


X=df.drop(['Unnamed: 0','Kilometers_Driven','Price'],axis=1)


# In[ ]:


y=df['Price']


# In[ ]:


X.isnull().sum()


# In[ ]:


X['Engine'].value_counts()


# In[ ]:


X['Engine'].fillna('1197 CC',inplace=True)


# In[ ]:


X['Mileage'].value_counts()


# In[ ]:


X['Mileage'].fillna('18.9 kmpl',inplace=True)


# In[ ]:


X['Power'].value_counts()


# In[ ]:


X['Power'].fillna('74 bhp',inplace=True)


# In[ ]:


X['Seats'].value_counts()


# In[ ]:


X['Seats'].fillna(X['Seats'].mean(),inplace=True)


# In[ ]:


X['New_Price'].value_counts()


# In[ ]:


X['New_Price'].fillna('4.78 Lakh',inplace=True)


# In[ ]:


X=pd.get_dummies(X)


# In[ ]:





# In[ ]:


X['Year'].hist(bins=50)


# In[ ]:


X['Year'].plot('density',color='Green')


# In[ ]:


X.boxplot(column='Year',by='Seats')


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25)
from sklearn.preprocessing import MinMaxScaler
scalerX=MinMaxScaler(feature_range=(0,1))
X_train[X_train.columns]=scalerX.fit_transform(X_train[X_train.columns])
X_test[X_test.columns]=scalerX.transform(X_test[X_test.columns])


# In[ ]:





# In[ ]:


from sklearn.linear_model import LinearRegression
k=LinearRegression()
k.fit(X_train,y_train)
k.score(X_test,y_test)


# In[ ]:


from sklearn.tree import DecisionTreeRegressor
j=DecisionTreeRegressor()
j.fit(X_train,y_train)
j.score(X_test,y_test)


# In[ ]:


from sklearn.ensemble import RandomForestRegressor
d=RandomForestRegressor()
d.fit(X_train,y_train)
d.score(X_test,y_test)


# In[ ]:


from sklearn.neighbors import KNeighborsRegressor
u=KNeighborsRegressor()
u.fit(X_train,y_train)
u.score(X_test,y_test)


# In[ ]:


from sklearn.linear_model import SGDRegressor
t=SGDRegressor()
t.fit(X_train,y_train)
t.score(X_test,y_test)


# In[ ]:


from sklearn.ensemble import ExtraTreesRegressor
g=ExtraTreesRegressor()
g.fit(X_train,y_train)
g.score(X_test,y_test)


# In[ ]:


X_train.shape


# In[ ]:


df1=pd.read_csv('/kaggle/input/used-cars-price-prediction/test-data.csv')
df1.head()
df1.columns


# In[ ]:


X1=df1.drop(['Unnamed: 0','Kilometers_Driven'],axis=1)


# In[ ]:


X1.isnull().sum()


# In[ ]:


X1['Engine'].value_counts()


# In[ ]:


X1['Engine'].fillna('1197 CC',inplace=True)


# In[ ]:


X1['Power'].value_counts()


# In[ ]:


X1['Power'].fillna('74 bhp',inplace=True)


# In[ ]:


X1['Seats'].value_counts()


# In[ ]:


X1['Seats'].fillna(X1['Seats'].mean(),inplace=True)


# In[ ]:


X1['New_Price'].value_counts()


# In[ ]:


X1['New_Price'].fillna('34.1 Lakh',inplace=True)


# In[ ]:


X1=pd.get_dummies(X1)
X1.shape


# In[ ]:


missing_cols=set(X_train.columns)-set(X1.columns)
for c in missing_cols:
    X1[c]=0
X1=X1[X_train.columns]


# In[ ]:


yx=g.predict(X1)
print(yx)


# In[ ]:


df1['Price']=yx


# In[ ]:


df1.head()


# In[ ]:


df1.to_csv('car_price_test_data.csv')


# In[ ]:


z=pd.read_csv('car_price_test_data.csv')
z.head()


# In[ ]:


#SAVE MODEL
import pickle
file_name='Car_Price.sav'
tuples=(g,X)
pickle.dump(tuples,open(file_name,'wb'))


# In[ ]:


print(k.coef_)
print(k.intercept_)


# In[ ]:





# In[ ]:




