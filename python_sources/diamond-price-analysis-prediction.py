#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.display.max_columns=999
from sklearn.metrics import confusion_matrix,accuracy_score,r2_score


# In[ ]:


df = pd.read_csv('../input/diamonds/diamonds.csv')
df.info()


# In[ ]:


df.isnull().sum()


# In[ ]:


df.head()


# In[ ]:


fig, (axis1,axis2) = plt.subplots(1,2,figsize=(15,5))
sns.barplot(y=df['Unnamed: 0'],x=df['cut'],ax=axis1).set_title('count VS cut')
sns.barplot(y=df['price'],x=df['cut'],ax=axis2).set_title('price VS count')


# In[ ]:


fig, (axis1,axis2) = plt.subplots(1,2,figsize=(15,5))
sns.barplot(df['color'],df['Unnamed: 0'],ax=axis1).set_title('count VS color')
sns.barplot(df['color'],df['price'],ax=axis2).set_title('price VS color')


# In[ ]:


fig, (axis1,axis2) = plt.subplots(1,2,figsize=(15,5))
sns.barplot(df['clarity'],df['Unnamed: 0'],ax=axis1).set_title('count VS clarity')
sns.barplot(df['clarity'],df['price'],ax=axis2).set_title('price VS clarity')


# In[ ]:


sns.kdeplot(df['carat'], shade=True , color='g')


# In[ ]:


sns.kdeplot(df['x'] ,shade=True , color='r' )
sns.kdeplot(df['y'] , shade=True , color='b' )
sns.kdeplot(df['z'] , shade= True , color='g')
plt.xlim(2,10)


# In[ ]:


ind = ['carat', 'cut', 'color', 'clarity', 'depth', 'table', 'x', 'y', 'z','price']
df = df.reindex(columns=ind)
df.head()


# In[ ]:


from sklearn.preprocessing import LabelEncoder
labelencoder1 = LabelEncoder()
labelencoder2 = LabelEncoder()
labelencoder3 = LabelEncoder()


# In[ ]:


df['cut'] = labelencoder1.fit_transform(df['cut'])
df['color'] = labelencoder2.fit_transform(df['color'])
df['clarity'] = labelencoder3.fit_transform(df['clarity'])


# In[ ]:


df.head()


# In[ ]:


x = df.iloc[:,0:9].values
y = df.iloc[:,-1].values


# In[ ]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)


# In[ ]:


from sklearn.linear_model import LinearRegression
model = LinearRegression()


# In[ ]:


model.fit(x_train,y_train)


# In[ ]:


y_pred = model.predict(x_test)


# In[ ]:


print(r2_score(y_test,y_pred))


# In[ ]:





# In[ ]:





# In[ ]:




