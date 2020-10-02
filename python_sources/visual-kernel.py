#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


import pandas as pd
train_set = pd.read_csv("../input/Allcity_centry.csv")


# In[3]:


train_set.head()


# In[4]:


same_point = train_set.loc[(train_set['time_entry'] == train_set['time_exit'])]


# In[5]:


diff_point= train_set.loc[(train_set['time_entry'] != train_set['time_exit'])]


# In[6]:


diff_point.info()


# In[7]:


new_sets=pd.DataFrame(columns = diff_point.columns.values)
new_sets=diff_point
#new_sets['time_exit']=train_set['time_exit']


# In[8]:


new_sets['time_entry']=diff_point['time_exit']


# In[9]:


new_sets['x_entry']=new_sets['x_exit']
new_sets['y_entry']=new_sets['y_exit']


# In[10]:


new_sets.info()


# In[11]:


diff_point['time_exit']=diff_point['time_entry']
diff_point['x_exit']=diff_point['x_entry']
diff_point['y_exit']=diff_point['y_entry']


# In[12]:


diff_point.head()


# In[13]:


output=pd.concat([diff_point,new_sets],ignore_index=True)
output.info()


# In[14]:


submit=pd.concat([output,same_point],ignore_index=True)


# In[17]:


from tqdm import tnrange, tqdm_notebook

submit = submit.drop_duplicates()
submit.city_centry.replace(1, 5, inplace=True)
hash_list = submit.hash.unique().tolist()
for hash in tqdm_notebook(hash_list):
    submit[submit['hash'] == hash].iloc[-1].city_centry *= 2


# In[ ]:


submit.to_csv("../working/submit.csv", index=False)


# In[ ]:




