#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Importing Libraries
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import r2_score


# In[ ]:


data = pd.read_csv(r"../input/zomato-bangalore-restaurants/zomato.csv")


# In[ ]:


data.head()


# In[ ]:


data.shape


# In[ ]:


data.describe()


# In[ ]:


data.info()


# In[ ]:


data.dtypes


# In[ ]:


data.duplicated().sum()


# In[ ]:


data.isnull().sum()


# In[ ]:


data.dropna(how='any',inplace=True)


# In[ ]:


data.shape


# In[ ]:


data.columns


# In[ ]:


data = data.rename(columns = {'approx_cost(for two people)':'cost'})


# In[ ]:


data.head()


# In[ ]:


data['cost'] = data['cost'].astype(str) 


# In[ ]:


data['cost'] = data['cost'].apply(lambda x: x.replace(',','.')) #Using lambda function to replace ',' from cost
data['cost'] = data['cost'].astype(float) # Changing the cost to Float
data.info()


# In[ ]:


data.rate.nunique()


# In[ ]:


data.rate.unique()


# In[ ]:


data = data.loc[data.rate !='NEW']
data = data.loc[data.rate !='-'].reset_index(drop=True)
remove_slash = lambda x: x.replace('/5', '') if type(x) == np.str else x
data.rate = data.rate.apply(remove_slash).str.strip().astype('float')
data['rate'].head()


# In[ ]:


data.online_order.replace(('Yes','No'),(1, 0),inplace=True)
data.book_table.replace(('Yes','No'),(1,0),inplace=True)


# In[ ]:


data_reg = data.copy()


# In[ ]:


corr = data_reg.corr(method='kendall')
plt.figure(figsize=(15,8))
sns.heatmap(corr, annot=True)
data_reg.columns


# In[ ]:


def Encode(zomato):
    for column in zomato.columns[~zomato.columns.isin(['rate', 'cost', 'votes'])]:
        zomato[column] = zomato[column].factorize()[0]
    return zomato

zomato_en = Encode(data_reg.copy())


# In[ ]:


zomato_en.head()


# In[ ]:


corr = zomato_en.corr(method='kendall')
plt.figure(figsize=(15,8))
sns.heatmap(corr, annot=True)
zomato_en.columns


# In[ ]:


#Defining the independent variables and dependent variables
x = zomato_en[['rate','listed_in(type)']]
y = zomato_en['cost']
#Getting Test and Training Set
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.1,random_state=353)


# In[ ]:


print(x_train.head())
print(y_train.head())


# In[ ]:


#Prepare a Linear Regression Model
reg=LinearRegression()
reg.fit(x_train,y_train)
y_pred=reg.predict(x_test)
from sklearn.metrics import r2_score
r2_score(y_test,y_pred)


# In[ ]:


from sklearn.tree import DecisionTreeRegressor
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.1,random_state=105)
DTree=DecisionTreeRegressor(min_samples_leaf=.0001)
DTree.fit(x_train,y_train)
y_predict=DTree.predict(x_test)
from sklearn.metrics import r2_score
r2_score(y_test,y_predict)


# In[ ]:


from sklearn.ensemble import RandomForestRegressor
RForest=RandomForestRegressor(n_estimators=500,random_state=329,min_samples_leaf=.0001)
RForest.fit(x_train,y_train)
y_predict=RForest.predict(x_test)
from sklearn.metrics import r2_score
r2_score(y_test,y_predict)


# In[ ]:


from sklearn.linear_model import Ridge


# In[ ]:


rr = Ridge(alpha=0.01)


# In[ ]:


rr.fit(x_train, y_train)


# In[ ]:


Ridge_train_score = rr.score(x_train,y_train)
Ridge_test_score = rr.score(x_test, y_test)
print(Ridge_train_score,Ridge_test_score)


# In[ ]:


rr100 = Ridge(alpha=100) #  comparison with alpha value
rr100.fit(x_train, y_train)


# In[ ]:


Ridge_train_score_100 = rr100.score(x_train,y_train)
Ridge_test_score_100 = rr100.score(x_test, y_test)
print(Ridge_train_score_100,Ridge_test_score_100)


# In[ ]:


from sklearn.linear_model import Lasso
lasso = Lasso()
lasso.fit(x_train,y_train)
train_score=lasso.score(x_train,y_train)
test_score=lasso.score(x_test,y_test)


# In[ ]:


print ("training score:", train_score )
print ("test score: ", test_score)


# In[ ]:





# In[ ]:




