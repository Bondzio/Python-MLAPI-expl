#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import os
print(os.listdir("../input"))


# In[ ]:


names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
data = pd.read_csv("../input/pima_data.csv",names=names)
array = data.values
X = array[:,0:8]
Y = array[:,8]
seed = 2
test_size = 0.33
model = LogisticRegression()
X_train, X_test, Y_traing, Y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
model.fit(X_train,Y_traing)
result = model.score(X_test,Y_test)
print("result:",result)


# In[ ]:


model_file = "model.sav"
with open(model_file,mode='wb') as model_f:
    joblib.dump(model,model_f)


# In[ ]:


with open(model_file,mode='rb') as model_f:
    model = joblib.load(model_f)
    result = model.score(X_test,Y_test)
    print("result:",result)


# In[ ]:




