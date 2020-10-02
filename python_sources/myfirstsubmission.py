#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[ ]:


train_df = pd.read_csv('../input/train.csv')
test_df = pd.read_csv('../input/test.csv')


# In[ ]:


print(f'train len {len(train_df)}) | test len {len(test_df)}')
display(train_df.head(5))
display(test_df.head(5))


# ### Now let's get a prediction

# In[ ]:


ybar = train_df.SalePrice.mean()
ybar


# In[ ]:


submission_pd = pd.DataFrame(test_df.Id)


# In[ ]:


submission_pd.head(5)


# In[ ]:


submission_pd['SalePrice'] = ybar


# In[ ]:


submission_pd.head(5)


# In[ ]:


submission_pd.to_csv('submission0.csv')


# In[ ]:


os.listdir()


# In[ ]:


submission_pd.to_csv('submission.csv', index=False)


# In[ ]:




