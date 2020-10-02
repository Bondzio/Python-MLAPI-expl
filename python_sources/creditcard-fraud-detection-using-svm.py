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
df=pd.read_csv('../input/creditcardfraud/creditcard.csv')
df.head()


# df.describe()

# In[ ]:


df.columns


# In[ ]:


#fraud data
fraud_df=df[df['Class']==1]
fraud_df.head()


# In[ ]:


#visualizing fraud data
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.scatter(fraud_df['Time'],fraud_df['Amount'])
plt.xlabel('Time')
plt.ylabel('Amount')
plt.show()


# In[ ]:


print('Total number of frauds:',len(fraud_df))


# In[ ]:


df.fillna(df.mean())


# In[ ]:


x=df.drop(['Time','Class'],axis=1)
x


# In[ ]:


y=df['Class']
y


# In[ ]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=4)


# In[ ]:


from sklearn import svm
clf=svm.SVC(kernel='linear')
clf.fit(x_train,y_train)
y_pred=clf.predict(x_test)
y_pred


# In[ ]:


from sklearn.metrics import accuracy_score
print(accuracy_score(y_test,y_pred))


# In[ ]:


from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_pred)
cm

