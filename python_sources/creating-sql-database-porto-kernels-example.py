#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd
import sqlite3

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))


# In[ ]:


# Read data
df = pd.read_csv("../input/portoKernels.csv",index_col=0)
df.head()


# In[ ]:


# Create database
database = 'database.sqlite'
conn = sqlite3.connect(database)


# In[ ]:


# Add table to database
df.to_sql('porto_kernels', conn)


# In[ ]:


# Display schema
query = '''
SELECT * FROM sqlite_master;
'''
pd.read_sql( query, conn )


# In[ ]:


# Display table
query = '''
SELECT * FROM porto_kernels
'''
pd.read_sql( query, conn )


# In[ ]:


# Example of a query
query = '''
SELECT * from PORTO_KERNELS
WHERE votes > 50
ORDER BY votes DESC
'''
pd.read_sql( query, conn )


# In[ ]:




