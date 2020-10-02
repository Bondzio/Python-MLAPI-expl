#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv("../input/churndata1/Churn_Modelling.csv")


# In[ ]:


df.head()


# In[ ]:


df.dtypes


# In[ ]:


np.unique(df.Gender)


# In[ ]:


df['Geography'] = df['Geography'].str.replace('France','1')
df['Geography'] = df['Geography'].str.replace('Germany','2')
df['Geography'] = df['Geography'].str.replace('Spain','3')

df['Gender'] = df['Gender'].str.replace('Female','0')
df['Gender'] = df['Gender'].str.replace('Male','1')


# In[ ]:


df.head(3)


# In[ ]:


df['Geography'] = df['Geography'].astype(int)
df['Gender'] = df['Gender'].astype(int)


# In[ ]:


df.dtypes


# In[ ]:


df.groupby(['Exited']).CreditScore.mean().plot.bar(color ='red')
plt.ylim(600,660)
plt.xticks([0,1],['Current','Exited'])
plt.title('Average Credit Score by Exited')
plt.xlabel('')
plt.ylabel('Credit Score')
plt.style.use('default')


# In[ ]:


df.groupby(['Gender']).Exited.count().plot.bar(color ='blue')
plt.title('Count of Gender by Exited')
plt.ylim(4000,5500)
plt.ylabel('Total Number')


# In[ ]:


df.groupby(['Geography']).Exited.count().plot.pie(autopct='%.1f%%', labels = ['France','Germany','Spain'])
plt.ylabel('')


# In[ ]:


df.groupby(['Tenure']).Exited.count().sort_values(ascending=False).head().plot.bar(color ='darkred')
plt.ylim(900,1050)


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(df[['CreditScore', 'Geography',
       'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard',
       'IsActiveMember', 'EstimatedSalary']],df.Exited, test_size = 0.3, random_state = 1)


# In[ ]:


Model = LogisticRegression()
Model.fit(X_train,y_train)


# In[ ]:


Model.predict(X_test)


# In[ ]:


Model.score(X_test,y_test)


# In[ ]:


Model.predict_proba(X_test)


# In[ ]:


Model.coef_


# In[ ]:




