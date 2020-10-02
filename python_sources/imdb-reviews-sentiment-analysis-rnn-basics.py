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


from matplotlib import pyplot as plt
import seaborn as sns

sns.set()


# In[ ]:


data = pd.read_csv("../input/imdb_master.csv", encoding="latin1", index_col=0)


# In[ ]:


data.head()


# In[ ]:


train_data = data[data.type == "train"]
test_data = data[data.type == "test"]


# In[ ]:


X_train = train_data[["review"]]
y_train = train_data["label"]
X_test = test_data[["review"]]
y_test = test_data["label"]


# In[ ]:


y_train.value_counts().plot(kind="bar", rot=0, figsize=(13, 8))
plt.ylabel("count", fontsize=13)
plt.xlabel("label", fontsize=13)
plt.show()


# In[ ]:




