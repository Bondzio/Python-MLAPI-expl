#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


data = pd.read_csv('../input/heights-and-weights/data.csv')
data.head()


# In[ ]:


X = data.iloc[:,0:1]
y = data.iloc[:, 1]
X


# In[ ]:


y


# In[ ]:


import seaborn as sns
sns.pairplot(data)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3, random_state=0)


# In[ ]:


from sklearn.ensemble import RandomForestRegressor
RFReg = RandomForestRegressor(n_estimators=500, random_state=0)
RFReg.fit(X_train,y_train)


# In[ ]:


y_predict_rfr = RFReg.predict((X_test))
from sklearn import metrics
r_square = metrics.r2_score(y_test,y_predict_rfr)
print('R-Square associated with Random Forest Regression is:', r_square)


# In[ ]:


X_val = np.arange(min(X_train),max(X_train),0.01)
X_val = X_val.reshape((len(X_val), 1))
plt.scatter(X_train,y_train,color='blue')
plt.plot(X_val,RFReg.predict(X_val), color='red')
plt.title('Weight prediction using Random Forest Regression')
plt.xlabel('Height')
plt.ylabel('Weight')
plt.figure(figsize=(1,1))
plt.show()


# In[ ]:


weight_pred = RFReg.predict([[1.6]])
print("Predicted Weight: %d"%weight_pred)

