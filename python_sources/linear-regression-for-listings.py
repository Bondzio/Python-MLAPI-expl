#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


dataset = pd.read_csv('../input/listings.csv')


# In[ ]:


dataset.shape


# In[ ]:


dataset.describe()


# In[ ]:


dataset.isnull().any()


# In[ ]:


dataset = dataset.fillna(method='ffill')


# In[ ]:


dataset["price"] = dataset["price"].str.replace(',', '')
dataset["price"] = dataset["price"].str.replace('$', '')
dataset["price"] = dataset["price"].astype('float64') 


# In[ ]:


dataset.plot(x='bedrooms', y='price', style='o')  
plt.title('bedrooms vs price')  
plt.xlabel('bedrooms')  
plt.ylabel('price')  
plt.show()


# In[ ]:


plt.figure(figsize=(15,10))
plt.tight_layout()
seabornInstance.distplot(dataset['price'])


# In[ ]:


X = dataset['bedrooms'].values.reshape(-1,1)
y = dataset['price'].values.reshape(-1,1)


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)


# In[ ]:


regressor = LinearRegression()  
regressor.fit(X_train, y_train)


# In[ ]:


print(regressor.intercept_)
print(regressor.coef_)


# In[ ]:


y_pred = regressor.predict(X_test)


# In[ ]:


df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
df


# In[ ]:


df1 = df.head(25)
df1.plot(kind='bar',figsize=(16,10))
plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
plt.show()


# In[ ]:


plt.scatter(X_test, y_test,  color='gray')
plt.plot(X_test, y_pred, color='red', linewidth=2)
plt.show()


# In[ ]:


print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

