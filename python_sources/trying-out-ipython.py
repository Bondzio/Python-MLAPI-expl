#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
import xgboost as xgb
import operator
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt


# In[ ]:


train = pd.read_csv("../input/train.csv", parse_dates=[2])
test = pd.read_csv("../input/test.csv", parse_dates=[3])
store = pd.read_csv("../input/store.csv")


# In[ ]:


train.dtypes


# In[ ]:


store.dtypes


# In[ ]:


train.describe()


# In[ ]:




