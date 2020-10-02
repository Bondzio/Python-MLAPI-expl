#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


dataset=pd.read_csv('../input/market-based-optimization/Market_Basket_Optimisation.csv',header=None)


# In[ ]:


dataset.head()


# In[ ]:


transcations1=[]
for i in range(0,7501):
    transcations1.append([str(dataset.values[i,j]) for j in range(0,20)])


# In[ ]:


pip install apyori  


# In[ ]:


from apyori import apriori
rules=apriori(transcations1,min_support=0.003,min_confidence=0.2,min_lift=3,min_length=2)


# In[ ]:


results=list(rules)


# In[ ]:


results


# In[ ]:


def inspect(results):
    lhs         = [tuple(result[2][0][0])[0] for result in results]
    rhs         = [tuple(result[2][0][1])[0] for result in results]
    supports    = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts       = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))
resultsinDataFrame = pd.DataFrame(inspect(results), columns = ['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])


# In[ ]:


resultsinDataFrame

