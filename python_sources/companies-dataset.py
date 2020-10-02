#!/usr/bin/env python
# coding: utf-8

# # Trying to create a large companies dataset
# 
# Look at me fail miserably in trying to create a list of "large" companies - at least for Australian companies.
# 
# ## Sources so far
# 
# - GRID database (research organisations) https://www.grid.ac/downloads
# - People Data Labs 7+ Million Company Dataset https://www.kaggle.com/peopledatalabssf/free-7-million-company-dataset
# 
# ## Want to add in the future
# 
# - Australian Business Register
# - Australian Taxation Office Tax Transparency Data

# In[ ]:


import pandas as pd

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


df = pd.read_csv('/kaggle/input/free-7-million-company-dataset/companies_sorted.csv', usecols = ['name', 'locality', 'country', 'total employee estimate'])
df.columns = [x.replace(' ','_') for x in df.columns]
df = (df.query('country==country')
        .query('total_employee_estimate >= 100'))

df.to_parquet('large_companies.parquet', index=False)


# In[ ]:


institutes = pd.read_csv('/kaggle/input/grid-database-2019/grid-2019-12-10/full_tables/institutes.csv',
                         usecols=['grid_id', 'name'])

addresses = pd.read_csv('/kaggle/input/grid-database-2019/grid-2019-12-10/full_tables/addresses.csv',
                        low_memory=False,
                        usecols=['grid_id', 'city', 'state', 'country', 'state_code', 'country_code'])

df = institutes.merge(addresses, on='grid_id', how='left')

del institutes, addresses

for column in df.columns:
    df[column] = df[column].str.lower()

df['state_code'] = df.state_code.str.split('-').apply(pd.Series).loc[:,1]

df.to_parquet('grid.parquet', index=False)


# In[ ]:




