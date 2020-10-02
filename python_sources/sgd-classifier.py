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
import seaborn as sns


# In[ ]:


def converter(x):
    if x=='Iris-setosa':
        return 0
    if x=='Iris-virginica':
        return 2
    else:
        return 1


# In[ ]:


df=pd.read_csv('../input/Iris.csv',converters={'Species':converter})
df.head()
df.drop(columns='Id',axis=0,inplace=True)


# In[ ]:


df.head()


# In[ ]:


df.isnull().sum()


# In[ ]:


f,ax=plt.subplots(1,2,figsize=(14,6))
df['Species'].value_counts().plot.pie(autopct='%1.1f%%',ax=ax[0],shadow=True)
ax[0].set_title('Species')
ax[0].set_ylabel('')
sns.countplot('Species',data=df,ax=ax[1])
ax[1].set_title('Species')
plt.show()


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X=df.iloc[:,:-1]
X.head()
y=df.iloc[:,-1]
y.head()


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


# In[ ]:


X_train.head()


# In[ ]:


y_train.head()


# In[ ]:


from sklearn.linear_model import SGDClassifier


# In[ ]:


clf=SGDClassifier(loss='log',random_state=9,penalty='l1',n_jobs=2)


# In[ ]:


clf.fit(X_train,y_train)


# In[ ]:


y_pred=clf.predict(X_test)


# In[ ]:


from sklearn.metrics import accuracy_score


# In[ ]:


result=accuracy_score(y_test, y_pred, normalize=True, sample_weight=None)


# In[ ]:


result*100


# In[ ]:


import pandas as pd
Iris = pd.read_csv("../input/Iris.csv")

