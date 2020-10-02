#!/usr/bin/env python
# coding: utf-8

# # Number of patents per person for a given list of names
# 
# Adapted from https://www.kaggle.com/jasonduncanwilson/top-inventors-racking-up-patents

# *Step 1: Import the Python Modules and the Datasets*

# In[ ]:


import numpy as np
import pandas as pd
import bq_helper
from bq_helper import BigQueryHelper
import plotly.offline as py
from plotly.offline import init_notebook_mode, iplot
import plotly.figure_factory as ff
init_notebook_mode(connected=True)


# *Step 2: Load Data*

# In[ ]:


list_of_names = ['LI XIAO',
                'YUAN YUAN',
                'LU LU',
                'JIA LI',
                'WEI LIU']
list_of_names = [x.upper() for x in list_of_names]
patents = bq_helper.BigQueryHelper(active_project="patents-public-data",dataset_name="patents") 


# *Step 3: Write queries for the Google Patents Public BigQuery Dataset*

# In[ ]:


inventor_query = """
WITH temp1 AS (
    SELECT
      DISTINCT
      PUB.country_code,
      PUB.application_number AS patent_number,
      inventor_name
    FROM
      `patents-public-data.patents.publications` PUB
    CROSS JOIN
      UNNEST(PUB.inventor) AS inventor_name
    WHERE
          PUB.grant_date > 0
      AND PUB.country_code IS NOT NULL
      AND PUB.application_number IS NOT NULL
      AND PUB.inventor IS NOT NULL
)
SELECT
  *
FROM (
    SELECT
     temp1.country_code AS country,
     temp1.inventor_name AS inventor,
     COUNT(temp1.patent_number) AS count_of_patents
    FROM temp1
    GROUP BY
     temp1.country_code,
     temp1.inventor_name
     )
WHERE
 count_of_patents > 0
;
"""


# *Step 4: Use your queries to download data from the Google Patents Public BigQuery Dataset*

# In[ ]:


print('Query Size: ', patents.estimate_query_size(inventor_query), 'GB')
inventor_query_results = patents.query_to_pandas_safe(inventor_query, max_gb_scanned=7)
top_inventors_in_both_datasets = inventor_query_results[inventor_query_results.inventor.isin(list_of_names)].nlargest(500,'count_of_patents')


# *Step 5: Which names from the "list_of_names" are associated with the largest number of patents?*

# In[ ]:


print('Most Prolific Inventors That Are Also In "list_of_names":')
inventors_in_both_datasets_table = ff.create_table(top_inventors_in_both_datasets)
py.iplot(inventors_in_both_datasets_table, filename='jupyter-table1')


# *Step 6: Sum results for names that show up twice (associated with two different countries)*

# In[ ]:


top_inventors_in_both_datasets_with_combined_duplicates = top_inventors_in_both_datasets.groupby(top_inventors_in_both_datasets.iloc[:,1]).sum()
top_inventors_in_both_datasets_with_combined_duplicates = top_inventors_in_both_datasets_with_combined_duplicates.reset_index()
top_inventors_in_both_datasets_with_combined_duplicates = top_inventors_in_both_datasets_with_combined_duplicates.sort_values(by=['count_of_patents'],ascending=False)
pd.options.display.max_rows = 9999
top_inventors_in_both_datasets_with_combined_duplicates.head(9999)


# *Step 7: Save the results as a .CSV file that can be opened using Google Sheets*

# In[ ]:


top_inventors_in_both_datasets_with_combined_duplicates.to_csv('candidates_sorted_by_patent_number.csv',index=False)

