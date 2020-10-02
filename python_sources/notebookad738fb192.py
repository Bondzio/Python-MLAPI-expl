#!/usr/bin/env python
# coding: utf-8

# Titanic data: Learning from disaster

# In[ ]:


import pandas as pd
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

data_train = pd.read_csv('../input/train.csv')
data_test = pd.read_csv('../input/test.csv')

data_train.sample(3)

sns.barplot(x="Embarked", y="Survived", hue="Sex", data=data_train);


# In[ ]:





# In[ ]:


train_df = pd.read_csv('../input/train.csv')  # train set
test_df  = pd.read_csv('../input/test.csv')   # test  set
combine  = [train_df, test_df]
train_df.drop(['Ticket', 'Cabin'], axis=1)
train_df[['Pclass','Survived']].groupby(['Pclass'],as_index=False).mean()


# In[ ]:




