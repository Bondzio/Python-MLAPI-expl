#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_squared_error
import keras
from keras.models import Sequential
from keras.layers import Dense,Dropout


# In[ ]:


file='/kaggle/input/heights-and-weights/data.csv'
data=pd.read_csv(file)
data.head()


# In[ ]:


data.info()


# In[ ]:


data.describe()


# In[ ]:


# Write your answer here

height = data.Height
weight = data.Weight

print("Mean weight: ", height.mean())
print("Mean height: ", weight.mean())

plt.title("Weight VS Height")
plt.plot(weight, height)


# In[ ]:


# split dataset to X and Y
X=data.iloc[:,:-1].values
y=data.iloc[:,-1].values
print(x.shape)
print(y.shape)


# In[ ]:



(X_train,X_test,y_train,y_test)=train_test_split(X,y,test_size=0.1)


# In[ ]:


lr=LinearRegression()


# In[ ]:


lr.fit(X_train,y_train)


# In[ ]:


pred=lr.predict(X_test)


# In[ ]:


plt.scatter(X_test,y_test,color='yellow')
plt.plot(X_test,pred,color='red')
plt.xlabel('Height')
plt.ylabel('Weight')
plt.show()
plt.savefig('mat.png')


# In[ ]:


r2_score(pred,y_test)


# ### Deep Neural Networks
# ## Predicting Weigths based on Heights Based on Keras

# In[ ]:


model=Sequential()
model.add(Dense(16,input_shape=(1,)))
model.add(Dense(1))


# In[ ]:


model.summary()


# In[ ]:


model.compile(optimizer='sgd', loss='mse',metrics=[keras.metrics.accuracy])


# In[ ]:


model.fit(X_train,y_train,epochs=20)


# In[ ]:


pred=model.predict(X_test)


# In[ ]:




