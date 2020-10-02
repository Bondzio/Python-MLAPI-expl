#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import bq_helper


# In[ ]:


github_repos = bq_helper.BigQueryHelper(active_project= "bigquery-public-data", 
                                       dataset_name = "github_repos")
github_repos.list_tables()


# In[ ]:


github_repos.table_schema("sample_contents")


# In[ ]:


github_repos.head("sample_contents")


# In[ ]:


query1= """SELECT content, sample_path
            FROM `bigquery-public-data.github_repos.sample_contents`
            WHERE LENGTH(content) > 100 AND LENGTH(content) <= 1000 AND binary = False
        """
github_repos.estimate_query_size(query1)


# In[ ]:


contents = github_repos.query_to_pandas_safe(query1, max_gb_scanned=24)
contents.head()


# In[ ]:


contents.shape


# In[ ]:


def file_type(path):
    path = str(path)
    try:
        file_extension = path.rpartition('.')[2]
    except IndexError:
        file_extension = 'null'  ## Ihe the path has no '.'
    return(file_extension)
    
file_type("some_random_script.py")


# In[ ]:


contents['type'] = contents.apply(lambda x: file_type(x['sample_path']),axis=1)
contents.head(10)


# In[ ]:


del contents['sample_path']
contents.to_csv("sample_code.csv", index=False)

