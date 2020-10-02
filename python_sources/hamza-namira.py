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


df = pd.read_csv('../input/amazon-fine-food-reviews/Reviews.csv')


# In[ ]:


df.head(n=2)


# In[ ]:


df1 = df[df['Score']==1]
df1 = df1.head(n=2000)

df2 = df0[df0['Score']==2]
df2 = df2.head(n=2000)

df3 = df0[df0['Score']==3]
df3 = df3.head(n=2000)

df4 = df0[df0['Score']==4]
df4 = df4.head(n=2000)

df5 = df0[df0['Score']==5]
df5 = df5.head(n=2000)


# In[ ]:


frames = [df1, df2, df3, df4, df5]

result = pd.concat(frames)


# In[ ]:


from sklearn.utils import shuffle
result = shuffle(result)


# In[ ]:


result['Score'].head(n=50)


# In[ ]:




