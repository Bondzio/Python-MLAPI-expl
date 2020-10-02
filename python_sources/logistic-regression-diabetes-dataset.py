#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sklearn import linear_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[ ]:


dataset=pd.read_csv("/kaggle/input/diabetes-dataset/diabetes2.csv")
dataset.head


# In[ ]:


dataset.isnull().sum()


# In[ ]:


dataset.Outcome.unique()


# In[ ]:


y=dataset["Outcome"]
x=dataset.drop("Outcome",axis=1)
x.head


# In[ ]:


reg=linear_model.LogisticRegression(C=0.5)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33,random_state=10)
x_train.head


# In[ ]:


reg.fit(x_train,y_train)
from sklearn.metrics import confusion_matrix,accuracy_score
y_predict=reg.predict(x_test)
print(y_predict)
confusion_matrix(y_predict,y_test)


# In[ ]:


accuracy_score(y_predict,y_test)


# In[ ]:


import seaborn as sns
sns.pairplot(dataset)

