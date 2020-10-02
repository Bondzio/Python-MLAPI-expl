#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


df=pd.read_csv("/kaggle/input/salary-data/Salary_Data.csv")


# In[ ]:


df.head()


# In[ ]:


df.corr()[['Salary']]


# In[ ]:


df.info()


# In[ ]:


df.describe()


# In[ ]:


from matplotlib import pyplot as plt
import numpy as np
x = df['YearsExperience']
y = df['Salary']
plt.scatter(x, y, color='r')
plt.xlabel('Year Experience')
plt.ylabel('Salary')
plt.title('Relation ')
plt.show()


# In[ ]:


X=df.iloc[:,:-1].values
Y=df.iloc[:,1].values


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=1/3,random_state=0)


# In[ ]:


#train the data using Linear Regression
from sklearn.linear_model import LinearRegression
simplelinearRegression = LinearRegression()
simplelinearRegression.fit(X_train,y_train)


# In[ ]:


y_predict=simplelinearRegression.predict(X_test)


# In[ ]:


plt.scatter(X_train, y_train,color='red')
plt.plot(X_train,simplelinearRegression.predict(X_train))
plt.show()

