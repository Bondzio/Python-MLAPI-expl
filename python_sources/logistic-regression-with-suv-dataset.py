#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


data = pd.read_csv("../input/suv-data/suv_data.csv")
data.head(5)


# In[ ]:


data.shape


# In[ ]:


data.isnull().sum()


# In[ ]:


sns.countplot(x="Purchased", hue = "Gender", data=data) 


# In[ ]:


data["Age"].plot.hist()


# In[ ]:


data.drop("User ID", axis=1 ,inplace=True)
data


# In[ ]:


sex = pd.get_dummies(data["Gender"], drop_first=True)
sex


# In[ ]:


data =pd.concat([data,sex], axis=1)
data


# In[ ]:


data.drop("Gender",axis=1 ,inplace=True)
data


# In[ ]:


x=data.drop("Purchased", axis=1)
y=data["Purchased"]


# In[ ]:


x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=42)


# In[ ]:


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)


# In[ ]:


model = LogisticRegression()
model.fit(x_train, y_train)


# In[ ]:


from sklearn.metrics import accuracy_score
predic = model.predict(x_test)
accuracy_score(y_test, predic)


# In[ ]:




