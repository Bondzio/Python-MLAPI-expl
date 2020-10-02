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


import numpy as np
import pandas as pd 
import numpy as np
import os
print(os.listdir("../input"))


# **Setting input directory ******

# In[ ]:


os.chdir("../input/employ-data")


# In[ ]:



emply_Da=pd.read_csv("Employ_detail.csv")


# Outlier detection and handling 

# In[ ]:


emply_Da.info()
emply_Da['Salary'].max()
emply_Da['Salary'].min()
emply_Da['Salary'].mean()


# In[ ]:


emply_Da['Salary'].hist(bins=20)


# In[ ]:


import matplotlib.pyplot as plt

emply_Da.boxplot(return_type='dict')
plt.plot()


# Log Method

# In[ ]:


emply_Da['Salary_log']=np.log(emply_Da['Salary'])
emply_Da['Salary_log'].hist(bins=20)


# In[ ]:


emply_Da['Salary_sqrt']=np.sqrt(emply_Da['Salary'])
emply_Da['Salary_sqrt'].hist(bins=20)


# In[ ]:


emply_Da['Salary_cbrt']=np.cbrt(emply_Da['Salary'])
emply_Da['Salary_cbrt'].hist(bins=20)


# In[ ]:




