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


data=pd.read_csv("/kaggle/input/heart-disease-uci/heart.csv")
data.columns


# In[ ]:


data.info()


# In[ ]:


data.describe().T
data.drop(["age"],axis=1,inplace=True)
#sex , exang , target 


# In[ ]:


y=data["slope"].values
x_data = data.drop(["slope"],axis=1)
x = (x_data - np.min(x_data))/(np.max(x_data)-np.min(x_data))


# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2,random_state=1)
x_train = x_train.T
x_test = x_test.T
y_train = y_train.T
y_test = y_test.T
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(x_train.T,y_train.T)
print("test sonucu {}".format(lr.score(x_test.T,y_test.T)))


# In[ ]:





# In[ ]:





# In[ ]:




