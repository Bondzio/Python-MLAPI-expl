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

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.
dF = pd.read_csv('../input/creditcard.csv', header=0)
dF.head()
dF.tail()


# In[ ]:


y = dF['Class'].values  # Target Class
dF = dF.drop(['Class'], axis=1)
z = dF.corr()
import seaborn as sns
sns.heatmap(z)


# In[ ]:


import matplotlib.pyplot as plt
plt.plot(dF['Time'].values,dF['Amount'].values)
plt.show()

