#!/usr/bin/env python
# coding: utf-8

# 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

#from subprocess import check_output
#print(check_output(["ls", "../input"]).decode("utf8"))
df = pd.read_csv("../input/all.csv")
X_train, X_test = train_test_split(df, test_size=0.2, random_state=42)    
# Any results you write to the current directory are saved as output.


# In[ ]:


df = pd.read_csv("../input/all.csv")


# In[ ]:




