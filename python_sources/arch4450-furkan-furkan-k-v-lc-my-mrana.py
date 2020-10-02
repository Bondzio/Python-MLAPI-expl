#!/usr/bin/env python
# coding: utf-8

# In[46]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[47]:


Top_hashtag_multi = pd.read_csv('../input/Top_hashtag.csv')
Top_hashtag_multi.head(5)


# In[48]:


Top_hashtag_multi.info()


# In[49]:


Top_hashtag_multi.describe()


# In[50]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[51]:


sns.pairplot(Top_hashtag_multi)


# In[52]:


sns.pairplot(Top_hashtag_multi, x_vars=['Likes','Comments','Posts'],y_vars='Posts',height=8, aspect=0.9)


# In[53]:


X= Top_hashtag_multi[['Posts','Comments','Likes']]
X.head()


# In[54]:


y= Top_hashtag_multi['Hashtag']
y.head()


# In[55]:


Top_hashtag_multi.tail()


# In[56]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=0.7,random_state=100 )


# In[57]:


print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)


# In[58]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[59]:


plt.figure(figsize=(5,5))
sns.heatmap(Top_hashtag_multi.corr(), annot=True)

