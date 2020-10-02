#!/usr/bin/env python
# coding: utf-8

# # Clustergrammer2 11-21-2019

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


get_ipython().system('pip install clustergrammer2')


# In[ ]:


from clustergrammer2 import net


# In[ ]:


import numpy as np
import pandas as pd

# generate random matrix
num_rows = 1000
num_cols = 5000
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


get_ipython().run_cell_magic('javascript', '', 'document.getElementById("rendered-kernel-content").style.width = "975px";')


# In[ ]:


net.load_df(df)
net.widget()


# In[ ]:




