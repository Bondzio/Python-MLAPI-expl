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


apps_data = pd.read_csv('/kaggle/input/17k-apple-app-store-strategy-games/appstore_games.csv')
apps_data.head(n=10)


# In[ ]:


apps_data.shape


# In[ ]:


apps_data.describe()


# In[ ]:


apps_data.dtypes


# In[ ]:


apps_data.plot(x='Size', y='Price',kind='scatter')


# In[ ]:


apps_data.plot(x='Size', y='User Rating Count',kind='scatter');


# In[ ]:


apps_data.plot(x='Average User Rating', y='User Rating Count',kind='scatter');


# In[ ]:


apps_data.head(n=10)


# In[ ]:


apps_data['In-app Purchases'].fillna(0, inplace=True) 
apps_data.head(n=6)


# In[ ]:


apps_data['In-app Purchases'] = apps_data['In-app Purchases'].astype(bool).astype(int)
apps_data.dtypes


# In[ ]:


apps_data.head(n=10)


# In[ ]:


apps_data.plot(x='Size', y='Price',c='In-app Purchases', kind='scatter',colormap='Paired');


# In[ ]:


apps_data['In-app Purchases'].describe()


# In[ ]:


apps_data.plot(x='Average User Rating', y='Price',c='In-app Purchases', kind='scatter',colormap='Paired',colorbar=False);


# In[ ]:


apps_data.loc[apps_data['Price'] == 179.99]


# In[ ]:


pd.options.display.max_rows = 999
apps_data.loc[apps_data['Developer'] == 'Andrew Kudrin']


# In[ ]:


apps_data.loc[apps_data['Developer'] == 'Andrew Kudrin'].shape


# In[ ]:




