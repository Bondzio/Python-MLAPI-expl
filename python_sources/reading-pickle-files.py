#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
import sys
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


for i in os.listdir("../input"):
    try:
        df = pd.read_pickle('../input/'+i, compression='gzip')
        print(i, ", SHAPE:", df.shape, ", SIZE: {:,} bytes".format(sys.getsizeof(df)))
        del df
    except Exception as e:
        print(i, "Error loading file", repr(e))


# In[ ]:




