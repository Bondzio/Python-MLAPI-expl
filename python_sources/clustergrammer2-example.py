#!/usr/bin/env python
# coding: utf-8

# # Clustergrammer2 Example

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


from clustergrammer2 import net


# In[ ]:


import numpy as np
import pandas as pd

# generate random matrix
num_rows = 1000
num_cols = 1000
np.random.seed(seed=100)
mat = np.random.rand(num_rows, num_cols)

# make row and col labels
rows = range(num_rows)
cols = range(num_cols)
rows = [str(i) for i in rows]
cols = [str(i) for i in cols]

# make dataframe 
df = pd.DataFrame(data=mat, columns=cols, index=rows)


# In[ ]:


df.shape


# In[ ]:


net.load_df(df)
net.cluster(enrichrgram=False)
net.load_df(net.export_df().round(2))
net.widget()


# In[ ]:




