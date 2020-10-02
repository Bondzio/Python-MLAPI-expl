#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


#load the csv file and make the data frame
ps_df = pd.read_csv('../input/googleplaystore.csv')


# In[ ]:


#display the data frame
ps_df


# In[ ]:


#display how many rows and columns are there
print("the data frame has {} rows and {}columns".format(ps_df.shape[0],ps_df.shape[1]))


# In[ ]:


#display the info of data frame
ps_df.info()


# In[ ]:


#display how many null values are there in each column
ps_df.apply(lambda x :sum(x.isnull()))


# In[ ]:


import re
def convert_to_number(x):
    if(re.search(',',x)):
        x = x.replace(',','')
        return(x)
    else:
        return(x)
ps_df['Installs_Modification'] = ps_df['Installs'].apply(convert_to_number)


# In[ ]:


def remove_plus_sign(x):
    x = x.replace('+','')
    return(x)
ps_df['Installs_Modification'] = ps_df['Installs_Modification'].apply(remove_plus_sign)


# In[ ]:


ps_df['Installs_Modification'] = ps_df['Installs_Modification'].astype('str')


# In[ ]:


ps_df['Installs_Modification'].replace('Free','0',inplace=True)


# In[ ]:


ps_df['Installs_Modification'] = ps_df['Installs_Modification'].astype('int')


# In[ ]:


#display which apps has maximum number of Installs
ps_df[ps_df['Installs_Modification'] == ps_df['Installs_Modification'].max()]


# In[ ]:


#display which app has minimum number of installs
ps_df[ps_df['Installs_Modification'] == ps_df['Installs_Modification'].min()]


# In[ ]:


ps_df.info()


# In[ ]:


print("The number of unique apps are {}".format(len(ps_df['App'].unique())))


# In[ ]:


ps_df.groupby(by=['Category']).count().index


# In[ ]:


#display graphically which app has most share
fig1,ax1 = plt.subplots()
ax1.pie(ps_df.groupby(by=['Category'])['App'].count(),labels=ps_df.groupby(by=['Category']).count().index,shadow=True,rotatelabels=30)
plt.show()

