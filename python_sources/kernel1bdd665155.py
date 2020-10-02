#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# In[ ]:


df = pd.read_csv('/kaggle/input/covid19-global-forecasting-week-1/train.csv')
test = pd.read_csv('/kaggle/input/covid19-global-forecasting-week-1/test.csv')
submission = pd.read_csv('/kaggle/input/covid19-global-forecasting-week-1/submission.csv')


# In[ ]:


ids = submission['ForecastId']


# In[ ]:


input_cols = ["Lat","Long","Date"]
output_cols = ["ConfirmedCases","Fatalities"]


# In[ ]:


for i in range(df.shape[0]):
    df["Date"][i] = df["Date"][i][:4] + df["Date"][i][5:7] + df["Date"][i][8:]
    df["Date"][i] = int(df["Date"][i])


# In[ ]:


for i in range(test.shape[0]):
    test["Date"][i] = test["Date"][i][:4] + test["Date"][i][5:7] + test["Date"][i][8:]
    test["Date"][i] = int(test["Date"][i])


# In[ ]:


X = df[input_cols]
Y1 = df[output_cols[0]]
Y2 = df[output_cols[1]]


# In[ ]:


X_test = test[input_cols]


# In[ ]:


sk_tree = DecisionTreeClassifier(criterion='entropy')


# In[ ]:


sk_tree.fit(X,Y1)


# In[ ]:


pred1 = sk_tree.predict(X_test)


# In[ ]:


sk_tree.fit(X,Y2)


# In[ ]:


pred2 = sk_tree.predict(X_test)


# In[ ]:


ids.shape


# In[ ]:


pred1.shape


# In[ ]:


pred2.shape


# In[ ]:


output = pd.DataFrame({ 'ForecastId' : ids, 'ConfirmedCases': pred1,'Fatalities':pred2 })
output.to_csv('submission.csv', index=False)


# In[ ]:




