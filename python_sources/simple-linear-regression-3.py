#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


data = pd.read_csv("../input/salary-data-simple-linear-regression/Salary_Data.csv")


# In[ ]:


data.head()


# In[ ]:


data.dropna()


# In[ ]:


X = data.iloc[:,:-1].values


# In[ ]:


y = data.iloc[:,1].values


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=0)


# In[ ]:


from sklearn.linear_model import LinearRegression


# In[ ]:


regression = LinearRegression()


# In[ ]:


regression.fit(X_train,y_train)


# In[ ]:


y_predict=regression.predict(X_test)


# In[ ]:


data_output = pd.DataFrame({"actule":y_test,"predict":y_predict})


# In[ ]:


data_output


# In[ ]:


plt.figure(figsize=[8,6])
plt.scatter(X_train,y_train,color="red")
plt.plot(X_train,regression.predict(X_train),color="blue")
plt.title("salary vs experince")
plt.xlabel("experince")
plt.ylabel("salary")
plt.show()


# In[ ]:


plt.figure(figsize=[8,6])
plt.scatter(X_test,y_test,color="blue",marker="*")
plt.plot(X_train,regression.predict(X_train),color="black")
plt.title("salary vs experince")
plt.xlabel("experince")
plt.ylabel("salary")
plt.show()


# In[ ]:




