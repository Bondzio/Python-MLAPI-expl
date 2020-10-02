#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
import pandas as pd

from surprise import NormalPredictor
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate

# Creation of the dataframe. Column names are irrelevant.
ratings_dict = {'itemID': [2, 5, 1, 3, 1, 1, 1, 4, 4, 2, 1, 5, 5, 4, 4, 5, 5, 1, 4, 1, 5, 1, 2, 5, 5, 4, 4, 4, 3, 3, 5, 4, 5, 5, 5, 3, 4, 2, 5, 5, 5, 5, 1, 5, 4, 3, 2, 2, 2, 5, 4, 1, 4, 4, 1, 2, 1, 2, 1, 2, 2, 4, 5, 5, 4, 2, 1, 3, 1, 4, 4, 1, 1, 4, 1, 2, 4, 1, 2, 2, 4, 3, 4, 4, 5, 2, 3, 3, 2, 3, 3, 3, 4, 4, 5, 2, 4, 4, 5, 2],
                'userID': [45, 32, 9, 45, 23, 9, 23, 23, 9, 2, 23, 32, 9, 23, 32, 45, 32, 32, 32, 32, 45, 23, 9, 9, 45, 23, 9, 2, 2, 23, 2, 2, 45, 9, 45, 32, 23, 2, 45, 32, 9, 32, 23, 23, 45, 32, 2, 9, 9, 23, 45, 45, 23, 45, 32, 23, 2, 9, 45, 32, 45, 23, 23, 45, 23, 23, 9, 32, 9, 23, 32, 2, 2, 32, 23, 45, 23, 9, 9, 32, 45, 9, 23, 45, 32, 32, 9, 23, 9, 45, 23, 32, 45, 2, 32, 2, 2, 2, 23, 23],
                'rating': [3, 4, 3, 3, 5, 4, 3, 5, 5, 3, 4, 4, 5, 5, 4, 3, 3, 5, 5, 4, 4, 3, 5, 4, 3, 3, 4, 4, 5, 3, 5, 3, 4, 5, 4, 3, 3, 4, 5, 3, 3, 4, 4, 5, 4, 5, 5, 3, 4, 3, 5, 3, 5, 4, 4, 3, 3, 5, 5, 5, 5, 4, 3, 5, 5, 5, 4, 3, 4, 4, 4, 3, 3, 4, 3, 4, 4, 4, 3, 3, 3, 5, 5, 4, 5, 3, 5, 3, 5, 4, 5, 4, 3, 4, 4, 3, 5, 5, 5, 5]}
df = pd.DataFrame(ratings_dict)
#df = pd.DataFrame(ratings_dict)

#pandas.DataFrame(D, index=['quantity']).plot(kind='bar')

# A reader is still needed but only the rating_scale param is requiered.
reader = Reader(rating_scale=(1, 5))
# The columns must correspond to user id, item id and ratings (in that order).
data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

# We can now use this dataset as we please, e.g. calling cross_validate
cross_validate(NormalPredictor(), data, cv=3)


# In[3]:


import matplotlib.pyplot as plt
rmsemoy=(1.13491727+ 1.092215  + 1.2540817 )/3
maemoy=(1.0957106+0.94835465+0.74344701)/3
print(rmsemoy)
A = {u'RMSE=1.13':1.13491727, u'RMSE=1.09 ': 1.092215 , u'RMSE=1.25 ':1.2540817, u'RMSE-MOY=1.16':rmsemoy}

plt.bar(range(len(A)), list(A.values()), align='center', color=['b','b','b','g'])
plt.xticks(range(len(A)), list(A.keys()))
plt.show()


# In[4]:


import matplotlib.pyplot as plt
maemoy=(1.0957106+0.94835465+0.74344701)/3
print(maemoy)
B = {u'MAE=1.096':1.0957106, u'MAE=0.948 ': 0.94835465, u'MAE=0.743 ':0.74344701, u'MAE-MOY=0.929':maemoy}

plt.bar(range(len(B)), list(B.values()), align='center', color=['c','c','c','g'])
plt.xticks(range(len(B)), list(B.keys()))
plt.show()

