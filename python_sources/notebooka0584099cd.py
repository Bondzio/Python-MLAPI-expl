#!/usr/bin/env python
# coding: utf-8

# In[65]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[66]:


get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model


# Read the input data

# In[86]:


data = pd.read_csv("../input/HR_comma_sep.csv")
data.info()


# In[87]:


data.head()


# In[88]:


#data.sort(["satisfaction_level","left"],ascending=[1,1])


# In[90]:


department_groups = {'sales': 1, 
                     'marketing': 2, 
                     'product_mng': 3, 
                     'technical': 4, 
                     'IT': 5, 
                     'RandD': 6, 
                     'accounting': 7, 
                     'hr': 8, 
                     'support': 9, 
                     'management': 10 
                    }
data['sales_index'] = data.sales.map(department_groups)
salary_groups = {'low': 0, 'medium': 1, 'high': 2}
data['salary_index']=data.salary.map(salary_groups)
data['salary_index']


# In[109]:


left_emp = data[data["left"] == 1]
left_to_total = left_emp.groupby(["sales"]).count() / data.groupby(["sales"]).count()
left_to_total["satisfaction_level"]


# In[112]:


plt.plot(left_emp["satisfaction_level"], left_emp["number_project"],  "o")
plt.show()


# In[72]:


data[data.columns[:]].corr()['left'][:]


# In[73]:


data.groupby(["sales"]).count()
cols = data.columns.tolist()
#cols
cols = cols[0:6] + cols[7:10] + cols[6:7]
#cols
data = data[cols]
cols=data.shape[1]


# In[74]:


X = data.iloc[:,0:cols-1]
Y = data.iloc[:,cols-1:cols]
X,Y


# In[75]:


mask = np.random.rand(len(data)) < 0.8
train = data[mask]
test = data[~mask]
len(train), len(test)
X1 = train.iloc[:,0:cols-1]
Y1 = train.iloc[:,cols-1:cols]
X2 = test.iloc[:,0:cols-1]
Y2 = test.iloc[:,cols-1:cols]
X1, Y1


# In[76]:


X1 = X1.drop(["sales", "salary"], axis=1)
X2 = X2.drop(["sales", "salary"], axis=1)


# In[77]:


model = linear_model.LogisticRegression(penalty='l2', C=1.0)
model.fit(X1, Y1)


# In[78]:


model.score(X2, Y2)


# In[79]:


model.score(X1, Y1)


# In[ ]:


model.predict(X)

