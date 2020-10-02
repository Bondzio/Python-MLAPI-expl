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


data = pd.read_csv(("../input/kc_house_data.csv"))
print(data)


# In[ ]:


data.shape


# In[ ]:


data.describe()


# In[ ]:


data.isnull().sum()


# In[ ]:


data.plot(x='sqft_living', y='price', style='o')  
plt.title('space vs price')  
plt.xlabel('space')  
plt.ylabel('price')  
plt.show()


# In[ ]:


plt.figure(figsize=(15,10))
plt.tight_layout()
seabornInstance.distplot(data['price'])


# In[ ]:


X = data['sqft_living'].values.reshape(-1,1)
y = data['price'].values.reshape(-1,1)


# In[ ]:


#time to train the set with 20% of the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


# In[ ]:


regressor = LinearRegression()  
regressor.fit(X_train, y_train) #training the algorithm


# In[ ]:


#To retrieve the intercept:
print(regressor.intercept_)
#For retrieving the slope:
print(regressor.coef_)


# In[ ]:


#This means that for every one unit of change in space, the change in the price is about 0.00


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
mean_squared_error=metrics.mean_squared_error(y_test,y_pred)
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
print('Sqaured mean error', round(np.sqrt(mean_squared_error),2))
print('R squared training',round(regressor.score(X_train,y_train),3))
print('R sqaured testing',round(regressor.score(X_test,y_test),3) )


# In[ ]:


_, ax = plt.subplots(figsize= (12, 10))
plt.scatter(X_test, y_test, color= 'darkgreen', label = 'data')
plt.plot(X_test, regressor.predict(X_test), color='red', label= ' Predicted Regression line')
plt.xlabel('Living Space (sqft)')
plt.ylabel('price')
plt.legend()
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['right'].set_visible(False)


# In[ ]:




