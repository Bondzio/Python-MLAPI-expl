#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Importing required packages
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 


# In[ ]:


#Loading dataset
hc = pd.read_csv('../input/hate_crimes.csv')#Loading dataset


# In[ ]:


#Let's check how the data is distributed
hc.head()


# In[ ]:


#Let's check how the data is distributed
hc.describe()


# In[ ]:


#now we will check about imputation
(hc.isnull().sum())


# In[ ]:


#fll some predifined data 
hc['share_non_citizen'].fillna(hc['share_non_citizen'].mean(),inplace=True)


# In[ ]:


hc['hate_crimes_per_100k_splc'].fillna(hc['hate_crimes_per_100k_splc'].mean(),inplace=True)


# In[ ]:


hc['avg_hatecrimes_per_100k_fbi'].fillna(hc['avg_hatecrimes_per_100k_fbi'].mean(),inplace=True)


# In[ ]:


#comformation of imputation process
(hc.isnull().sum())


# In[ ]:


#droping target variable .
correlations = hc.corr()['avg_hatecrimes_per_100k_fbi'].drop('avg_hatecrimes_per_100k_fbi')
print(correlations)


# In[ ]:


#heat map for corelation matrix
sns.heatmap(hc.corr().round(2),annot=True)
plt.show()



# In[ ]:



from pandas.plotting import scatter_matrix
hc.hist()
plt.show()


# In[ ]:


#When youneed to look at several plots, 
#such as at the beginning of a multiple regression analysis, a scatter plot matrix is avery useful tool.
scatter_matrix(hc)
plt.show()


# In[ ]:


#dividing one of attributes into target variable
x = hc.drop("avg_hatecrimes_per_100k_fbi", axis=1)
y = hc["avg_hatecrimes_per_100k_fbi"]
print(x.shape)
print(y.shape)


# In[ ]:


x


# In[ ]:


y


# In[ ]:


round(y)


# In[ ]:


import seaborn as sns 
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.distplot(hc['avg_hatecrimes_per_100k_fbi'], bins=30)
plt.show()


# In[ ]:


#spliting of dataset into test dataset and train dataset
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.1,random_state=4)


# In[ ]:


print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)


# In[ ]:


#linear regression is a linear approach to modeling the relationship between
#a scalar response (or dependent variable) and one or more explanatory variables (or independent variables).

reg = LinearRegression()
reg.fit(x_train,y_train)


# In[ ]:


reg.coef_


# In[ ]:


train_pred = reg.predict(x_train)
train_pred


# In[ ]:


test_pred = reg.predict(x_test)
test_pred


# In[ ]:


from sklearn.metrics import mean_squared_error
train_rmse = mean_squared_error(train_pred, y_train) ** 0.5
train_rmse


# In[ ]:


test_rmse = mean_squared_error(test_pred, y_test) ** 0.5
test_rmse


# In[ ]:


#it is also one  type of predicting models
from sklearn.metrics import r2_score
# model evaluation for training set
y_train_predict = reg.predict(x_train)

rmse = (np.sqrt(mean_squared_error(y_train, y_train_predict)))

r2 = r2_score(y_train, y_train_predict)

print("The model performance for training set")
print("--------------------------------------")
print('RMSE is {}'.format(rmse))
print('R2 score is {}'.format(r2))
print("\n")

# model evaluation for testing set
y_test_predict = reg.predict(x_test)
rmse = (np.sqrt(mean_squared_error(y_test, y_test_predict)))
r2 = r2_score(y_test, y_test_predict)

print("The model performance for testing set")
print("--------------------------------------")
print('RMSE is {}'.format(rmse))
print('R2 score is {}'.format(r2))


# In[ ]:


from sklearn.metrics import r2_score
train_r2=r2_score(y_train,train_pred)
train_r2


# In[ ]:


test_r2=r2_score(y_test,test_pred)
test_r2


# In[ ]:


#Pipeline processing refers to overlapping operations by moving data or instructions into a conceptual pipe with all stages of the pipe performing simultaneously. 
#mainly as we got less acuracy,to increase it, will implement this process
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
pipe_lr = Pipeline([('scl', StandardScaler()),

			('pca', PCA(n_components=8)),

			('clf', LinearRegression())])
pipe_lr.fit(x_train, y_train)
print(pipe_lr.score(x_test, y_test))


# In[ ]:




