#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder 
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from xgboost.sklearn import XGBRegressor


# In[ ]:


df=pd.read_csv('../input/air-quality-data-in-india/city_hour.csv')


# In[ ]:


df.head()


# In[ ]:


df.describe()


# In[ ]:


df.info()


# In[ ]:


df.isnull().sum()


# In[ ]:


df.dropna(how="any",inplace=True)


# In[ ]:


df.describe()


# In[ ]:


df.info()


# In[ ]:


#df


# In[ ]:


df["City"].unique()


# In[ ]:


df['Datetime'].unique()


# In[ ]:


#sns.pairplot(df,hue="AQI_Bucket",vars=['PM2.5','PM10','NO','Benzene'],palette='husl')


# In[ ]:


a=pd.get_dummies(df['City'],drop_first=True)


# In[ ]:


a.describe()


# In[ ]:


#type(df['City'])


# In[ ]:


#df.iloc[:3]


# In[ ]:


#pd.get_dummies(data=df,columns=['City','Datetime'])


# In[ ]:


#df.info()


# In[ ]:


df=df.drop('Datetime',axis=1)


# In[ ]:


df=pd.get_dummies(data=df,columns=['City'])


# In[ ]:


#df.head()


# In[ ]:


df.describe()


# In[ ]:


sns.heatmap(df.corr(),linewidths=1)


# In[ ]:


# in this we can see that AQI is highly correlated with PM 2.5 and PM 10


# In[ ]:


df.info()


# In[ ]:


#x=df.drop(["AQI_Bucket","AQI","City_Amaravati","City_Amritsar","City_Chandigarh","City_Delhi","City_Gurugram","City_Hyderabad","City_Kolkata","City_Patna","NOx","NH3","CO","SO2","O3","Benzene","Toluene","Xylene"],axis=1)


# In[ ]:


#y=df["AQI_Bucket"]


# In[ ]:


#x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33,random_state=1)


# In[ ]:


#model=LogisticRegression()


# In[ ]:


#model.fit(x_train,y_train)


# In[ ]:


#predictions=model.predict(x_test)


# In[ ]:


#print(confusion_matrix(y_test, predictions))
#print(accuracy_score(y_test, predictions))


# In[ ]:


#eval_set = [(x_train, y_train), (x_test, y_test)]
#eval_metric = ["auc","error"]
#%time model.fit(x_train, y_train, eval_metric=eval_metric, eval_set=eval_set, verbose=True)


# In[ ]:


x=df.iloc[:,0:12]
x.head()


# In[ ]:


y=df.iloc[:,13]
y.head()
y.unique()


# In[ ]:


params={
 "learning_rate"    : [0.05, 0.10, 0.15, 0.20, 0.25, 0.30 ] ,
 "max_depth"        : [ 3, 4, 5, 6, 8, 10, 12, 15],
 "min_child_weight" : [ 1, 3, 5, 7 ],
 "gamma"            : [ 0.0, 0.1, 0.2 , 0.3, 0.4 ],
 "colsample_bytree" : [ 0.3, 0.4, 0.5 , 0.7 ]  
}


# In[ ]:


grid_size_per_parameter  = [len(i) for i in params.values()]
print(grid_size_per_parameter)
np.prod(grid_size_per_parameter)


# In[ ]:


classifier =xgb.XGBClassifier()


# In[ ]:


random_search=RandomizedSearchCV(classifier,param_distributions=params,n_iter=5,scoring='roc_auc',n_jobs=-1,cv=5,verbose=3)


# In[ ]:


df.head()


# In[ ]:


type(random_search)


# In[ ]:


df.info()


# In[ ]:


random_search.estimator


# In[ ]:


random_search.fit(x,y)


# In[ ]:


random_search.best_estimator_


# In[ ]:


random_search.best_params_


# In[ ]:


classifier=xgboost.XGBClassifier(base_score=None, booster=None, colsample_bylevel=None,
              colsample_bynode=None, colsample_bytree=0.5, gamma=0.0,
              gpu_id=None, importance_type='gain', interaction_constraints=None,
              learning_rate=0.05, max_delta_step=None, max_depth=8,
              min_child_weight=5, missing=nan, monotone_constraints=None,
              n_estimators=100, n_jobs=None, num_parallel_tree=None,
              objective='binary:logistic', random_state=None, reg_alpha=None,
              reg_lambda=None, scale_pos_weight=None, subsample=None,
              tree_method=None, validate_parameters=False, verbosity=None)


# In[ ]:


from sklearn.model_selection import cross_val_score
score=cross_val_score(classifier,x,y,cv=10)


# In[ ]:


score

