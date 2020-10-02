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



import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
get_ipython().run_line_magic('matplotlib', 'inline')
from statsmodels.formula.api import ols
import statsmodels.api as sm
import scipy.stats as stat
from sklearn.linear_model import LinearRegression 
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import r2_score


# In[ ]:


import pandas as pd
AB_NYC_2019 = pd.read_csv("../input/new-york-city-airbnb-open-data/AB_NYC_2019.csv")


# In[ ]:


# Headings  
AB_NYC_2019.head()


# In[ ]:


# dimension
rows, columns = AB_NYC_2019.shape
(f"AB_NYC_2019 consists {rows} rows and {columns} columns")


# In[ ]:


# checking for missing vlaues or null
AB_NYC_2019.isnull().sum()


# In[ ]:


AB_NYC_2019.dropna(how = "any", inplace = True)
AB_NYC_2019.info()


# In[ ]:


# replacing null values with 0
AB_NYC_2019["last_review"].fillna(0, inplace = True)
AB_NYC_2019["reviews_per_month"].fillna(0, inplace = True)


# In[ ]:


# neighbourhood and room counts
plt.figure(figsize = (12,8))
sns.countplot(AB_NYC_2019["neighbourhood_group"])

plt.figure(figsize = (12,8))
sns.countplot(AB_NYC_2019["room_type"])


# In[ ]:


# Distribution of neighbourhood groups in new york 
plt.figure(figsize = (12,8))
sns.scatterplot(AB_NYC_2019["latitude"], AB_NYC_2019["longitude"], hue = "neighbourhood_group", data = AB_NYC_2019, alpha = "auto")


# In[ ]:


# Distribution of different room types in Newyork 
plt.figure(figsize = (12,8))
sns.scatterplot(AB_NYC_2019["latitude"], AB_NYC_2019["longitude"], hue = "room_type", data = AB_NYC_2019, alpha = "auto")


# In[ ]:


# Filtering and grouping data 
rom_neig = AB_NYC_2019.groupby(["room_type", "neighbourhood_group"])["price"]. mean()


# In[ ]:


bnb_pvt = AB_NYC_2019.query("room_type == 'Private room'").groupby("neighbourhood_group")["price"].mean()


# In[ ]:


bnb_apt = AB_NYC_2019.query("room_type == 'Entire home/apt'").groupby("neighbourhood_group")["price"].mean()


# In[ ]:


bnb_shr = AB_NYC_2019.query("room_type == 'Shared room'").groupby("neighbourhood_group")["price"].mean()


# In[ ]:


plt.figure(figsize = (12,8))
plt.xticks(rotation = 45)
sns.barplot(x = AB_NYC_2019["neighbourhood_group"], y = AB_NYC_2019["price"], estimator = np.mean, saturation=.75)


# In[ ]:


# Reviews and listings in each state
no_rev = AB_NYC_2019.groupby(["neighbourhood_group", "neighbourhood"])["number_of_reviews"].sum().sort_values(ascending = False).head(5)


# In[ ]:


no_lst = AB_NYC_2019.groupby(["neighbourhood_group", "neighbourhood"])["calculated_host_listings_count"].sum().sort_values(ascending = False).head(5)


# In[ ]:


rev_per_mon = AB_NYC_2019.groupby(["neighbourhood_group", "neighbourhood"])["reviews_per_month"].sum().sort_values(ascending = False).head(5)


# In[ ]:


# Reviews on the basis of hostname
no_of_rev_host = AB_NYC_2019.query("neighbourhood_group == ['Brooklyn', 'Manhattan', 'Queens', 'Bronx', 'Staten Island']").groupby(["neighbourhood_group", "neighbourhood", "host_name",])["number_of_reviews"].sum().sort_values(ascending = False).head(5)


# In[ ]:


no_of_rev_host_mnth = AB_NYC_2019.query("neighbourhood_group == ['Brooklyn', 'Manhattan', 'Queens', 'Bronx', 'Staten Island']").groupby(["neighbourhood_group", "neighbourhood", "host_name",])["reviews_per_month"].sum().sort_values(ascending = False).head(5)


# In[ ]:


no_of_host_lst = AB_NYC_2019.query("neighbourhood_group == ['Brooklyn', 'Manhattan', 'Queens', 'Bronx', 'Staten Island']").groupby(["neighbourhood_group", "neighbourhood", "host_name",])["calculated_host_listings_count"].sum().sort_values(ascending = False).head(5)


# In[ ]:


# Prediction
# encoding coverting cateogoriacal varaible into numercial variable 
def Encode(AB_NYC_2019):
    for column in AB_NYC_2019.columns[AB_NYC_2019.columns.isin(['neighbourhood_group', 'room_type'])]:
        AB_NYC_2019[column] = AB_NYC_2019[column].factorize()[0]
    return AB_NYC_2019
airbnb_en = Encode(AB_NYC_2019.copy())


# In[ ]:


# Correlation map 
plt.figure(figsize=(12,8))
sns.heatmap(airbnb_en.corr())


# In[ ]:



# Preparaing independent and dependent variable 
for i in airbnb_en.head():
    print(i)


# In[ ]:


x = np.array(pd.get_dummies(airbnb_en.iloc[:,[4,8,10,11,14]]))
y = np.array(airbnb_en["price"])


# In[ ]:


# Generating test and train data from variables linearregression 
x_train,x_test,y_train,y_test = train_test_split(x,y)


# In[ ]:



lm_mod = LinearRegression()

lm_train = lm_mod.fit(x_train, y_train)


# In[ ]:


# Intercept and Coefficient of each independent variable 
lm_train.intercept_


# In[ ]:


lm_train.coef_


# In[ ]:


y_predict = lm_mod.predict(x_test)


# In[ ]:


# Rsquare value is too low
r2_score(y_test,y_predict)


# In[ ]:


plt.scatter(y_test,y_predict)


# In[ ]:


# To validate the regression model three steps has to be done 
# Mean Absolute Error
# Mean Squared Error
# Root Mean Squared Error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error


# In[ ]:


Mean_Absolute_Error = mean_absolute_error(y_test,y_predict)


# In[ ]:


Mean_Squared_Error =  mean_squared_error(y_test,y_predict)


# In[ ]:


Root_Mean_Squared_Error = np.sqrt(mean_squared_error(y_test,y_predict))


# In[ ]:


# Generating test and train data from variables Decsion tree regression 
d_tree = DecisionTreeRegressor(min_samples_leaf = 0.0001)

dtree_train = d_tree.fit(x_train, y_train)


# In[ ]:


dtree_train.score(x,y)


# In[ ]:


dtree_y_predict = d_tree.predict(x_test)


# In[ ]:


r2_score(y_test,dtree_y_predict)


# # Both model value suggests, its not suitable for production. 
