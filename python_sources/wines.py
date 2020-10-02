#!/usr/bin/env python
# coding: utf-8

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


import pandas as pd

### Read data from Csv file to Pandas DataFrame.
df = pd.read_csv("/kaggle/input/wine-reviews/winemag-data-130k-v2.csv")


df.head()


# In[ ]:


df.shape


# In[ ]:


df.describe()


# #  Task 1 : High Price = High Points? #####
# > ### range = 4 Dollar ~ 200 Dollar.

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns

filt = df[(df['points'] > 94) & (df['price'] < 200)]
df['hpoints'] = filt['points']
df['hprice'] = filt['price']

result = sns.catplot(x='hpoints', y='hprice', 
            data=df, jitter='0.4')

result.set(xlabel="Points", ylabel="Price ($)")
plt.show()


# In[ ]:





# # Task 2 : Most Produced Types of Wine Each Country

# In[ ]:



most_df = df.groupby('country')['variety'].describe()[['top','freq']].reset_index().sort_values(by='freq', ascending=False)
most_df = most_df.head(15)
most_df


# In[ ]:


y = most_df['country']
x = most_df['freq']
types = most_df['top']

ax = sns.barplot(x, y, hue=types, data=most_df, dodge=False, log=True, palette="deep")
plt.xlabel('Total of Types')
plt.ylabel('Country')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()


# In[ ]:





# # Conclusion

# * When if you buy some wine, It might be good wine to buy $75~150 :)
# * Most produced type of wine is "Pinot Noir"
# * Most pinot noirs are made in the US.
# * Surprisingly, most of the top ranking wines are blended wines.

# In[ ]:




