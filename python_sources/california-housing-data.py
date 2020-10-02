#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
print(os.listdir("../input"))
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style = 'darkgrid')


# In[3]:


file = '../input/housing.csv'
housing = pd.read_csv(file)


# In[5]:


housing.head()


# In[6]:


housing.info()


# In[7]:


housing.describe()


# In[8]:


housing['ocean_proximity'].value_counts()


# In[9]:


sns.countplot(x = 'ocean_proximity',data = housing)


# In[10]:


housing.hist(bins = 50,figsize = (17,15),xrot = 45)
plt.show()


# In[11]:


housing.plot(x = 'longitude',y = 'latitude',kind = 'scatter',figsize = (10,12))


# In[12]:


housing.plot(x = 'longitude',y = 'latitude',kind = 'scatter',alpha = 0.1,figsize = (10,12))


# In[13]:


housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4,
s=housing["population"]/100, label="population",
c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=True,figsize = (10,12))
plt.title('California Housing Prices')
plt.legend()


# In[14]:


from pandas.tools.plotting import scatter_matrix
attributes = ["median_house_value", "median_income", "total_rooms",
"housing_median_age"]
scatter_matrix(housing[attributes], figsize=(12, 8))


# In[15]:


housing.plot(kind="scatter", x="median_income", y="median_house_value",
alpha=0.1)


# In[16]:


housing.plot(x = 'population',y = 'longitude',kind = 'scatter',figsize = (5,7))


# In[17]:


sns.jointplot(x = 'population',y = 'longitude',data = housing,color = 'gold')


# In[18]:


from sklearn import linear_model
regr = linear_model.LinearRegression()
train_x = np.asanyarray(housing[['longitude']])
train_y = np.asanyarray(housing[['population']])
regr.fit (train_x, train_y)
# The coefficients
print ('Coefficients: ', regr.coef_)
print ('Intercept: ',regr.intercept_)


# In[19]:


plt.figure(figsize = (10,12))
plt.scatter(housing.longitude,housing.population,  color='gold')
plt.plot(train_x, regr.coef_[0][0]*train_x + regr.intercept_[0], '-r')
plt.xlabel("Population")
plt.ylabel("longitude")


# In[20]:


from sklearn.metrics import r2_score

test_x = np.asanyarray(housing[['longitude']])
test_y = np.asanyarray(housing[['population']])
test_y_ = regr.predict(test_x)

print("Mean absolute error: %.2f" % np.mean(np.absolute(test_y_ - test_y)))
print("Residual sum of squares (MSE): %.2f" % np.mean((test_y_ - test_y) ** 2))
print("R2-score: %.2f" % r2_score(test_y_ , test_y) )


# In[ ]:




