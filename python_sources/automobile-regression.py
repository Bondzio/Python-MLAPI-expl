#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression


# In[ ]:


data=pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data ",names=['symboling','normalize_losses','make','fueal_type','aspiration','num_of_doors','body_style','drive_wheels','engine_locatio','wheel_base'
     ,'length','width','height','curb_weight','engine_type','num_of_cylinders','engine_size','fuel_system'
     ,'bore','stroke','compression_ratio','horsepower','peak_rpm','city_mpg','highway_mpg','price'],na_values="?")
data.head()


# In[ ]:


data.dtypes


# In[ ]:


data.isnull().any()


# In[ ]:


data[data.isnull().any(axis=1)][data.columns[data.isnull().any()]]


# In[ ]:


data.dtypes


# In[ ]:


data.drop(["symboling","normalize_losses","make","fueal_type","fuel_system","aspiration","num_of_doors","body_style","drive_wheels","engine_locatio","engine_type"],axis=1,inplace=True)
data


# In[ ]:


data.dtypes


# In[ ]:


data["num_of_cylinders"].unique()


# In[ ]:


data["cylinders"]=data["num_of_cylinders"].replace({'four':4, 'six':6, 'five':5, 'three':3, 'twelve':12, 'two':2, 'eight':8})


# In[ ]:



data["cylinders"]


# In[ ]:


data.drop(['num_of_cylinders'],axis=1,inplace=True)
data.head()


# In[ ]:


data.describe()


# In[ ]:


data.isnull().any()


# In[ ]:


data["bore"]=data["bore"].fillna(data["bore"].median())
data["stroke"]=data["stroke"].fillna(data["stroke"].median())
data["horsepower"]=data["horsepower"].fillna(data["horsepower"].median())
data["peak_rpm"]=data["peak_rpm"].fillna(data["peak_rpm"].median())
data["price"]=data["price"].fillna(data["price"].median())


# **#all are false.no nan value**

# In[ ]:


data.isnull().any()


# #visualization

# In[ ]:


sns.pairplot(data)


# price distribution plot
# #positive skewed

# In[ ]:


sns.distplot(data["price"])


# In[ ]:


X=data.drop("price",axis=1)
y=data[["price"]]


# #train_test_split 

# In[ ]:


from sklearn.model_selection import train_test_split 


# In[ ]:


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=1)


# In[ ]:


regression_model=LinearRegression()
regression_model.fit(X_train,y_train)


# In[ ]:


X_train.columns


# # coeffiecient & intercept

# In[ ]:


for i,col_name in enumerate(X_train.columns):
    print(" coefficient of {} is {}".format(col_name,regression_model.coef_[0][i]))


# In[ ]:


intercept=regression_model.intercept_[0]
print(" intercept for model ",intercept)

#coefficient of ditermination 
83.61%  can explain by this independet variable 
# In[ ]:


regression_model.score(X_test,y_test)


# In[ ]:


import statsmodels.formula.api as smf


# combining dependent and independent variable

# In[ ]:


cars=pd.concat([y_train,X_train],axis=1)
cars


# In[ ]:


incars=smf.ols(formula='price~wheel_base + length + width+ height+ curb_weight+ engine_size+bore+stroke+ compression_ratio+ horsepower +peak_rpm+ city_mpg+ highway_mpg+ cylinders',data=cars).fit()





#another way to find coefficiet
# In[ ]:


incars.params


# In[ ]:


print(incars.summary())


# In[ ]:




