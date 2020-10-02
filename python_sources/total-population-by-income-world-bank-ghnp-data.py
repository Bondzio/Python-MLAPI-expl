#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import bq_helper
from bq_helper import BigQueryHelper

# create a helper object for the bigquery dataset World Bank: Global Health, Nutrition, and Population Data
ghnp = bq_helper.BigQueryHelper(active_project='bigquery-public-data',
                                dataset_name='world_bank_health_population')


# Print a list of all the tables in the **world_bank_health_population** dataset.

# In[ ]:


ghnp.list_tables()


# Print information on all the columns in the *health_nutrition_population* table in the **world_bank_health_population** dataset.

# In[ ]:


ghnp.table_schema('health_nutrition_population')


# Preview the first thirty lines of the *health_nutrition_population* table.

# In[ ]:


ghnp.head('health_nutrition_population', num_rows=30)


# Number of lines of the *health_nutrition_population *table.

# In[ ]:


query_count = """
SELECT
COUNT(*)
FROM
`bigquery-public-data.world_bank_health_population.health_nutrition_population`
;
"""

res_count = ghnp.query_to_pandas_safe(query_count)
res_count.head()


# Show indicator names removing duplicates with corresponding indicator codes that comply with '%POP%TOTL' pattern.

# In[ ]:


query_indicator_name = """
SELECT
DISTINCT(indicator_name)
AS
indicator_name,
indicator_code
FROM
`bigquery-public-data.world_bank_health_population.health_nutrition_population`
WHERE
indicator_code LIKE '%POP%TOTL'
ORDER BY
indicator_name
;
"""

# check how big the query will be
ghnp.estimate_query_size(query_indicator_name)


# The estimated query size is 0.15 GB. Now it is time to run the query. The results will be get back as a pandas DataFrame. To avoid potential mistakes running large queries, there is a safe version of the query runner that will cancel large requests that exceed a defined value.

# In[ ]:


res_indicator_name = ghnp.query_to_pandas_safe(query_indicator_name, max_gb_scanned=1/10**3)


# The query runner has a default scan limit of 1 GB. This time the query will be executed as the query size is roughly 0.15 GB.

# In[ ]:


res_indicator_name = ghnp.query_to_pandas_safe(query_indicator_name)
res_indicator_name.head(20)


# The total population is the only result that complies with the query.

# Show total population values for countries that finish with *income* for decades from 1985 to 2015.

# In[ ]:


query_pop_income = """
SELECT
DISTINCT country_name
AS
country_name, country_code, year, value
FROM
`bigquery-public-data.world_bank_health_population.health_nutrition_population`
WHERE
indicator_code = 'SP.POP.TOTL' 
AND (country_name LIKE '%income' OR country_name = 'World')
AND year IN (1985,1995,2005,2015)
ORDER BY
country_name DESC,
year ASC
LIMIT 100
;
"""

# check how big the query will be
ghnp.estimate_query_size(query_pop_income)


# In[ ]:


res_pop_income = ghnp.query_to_pandas_safe(query_pop_income)
res_pop_income.head(50)


# In[ ]:


# library for plotting
import matplotlib.pyplot as plt

# colors used in plot
color_sequence = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# list of unique country names
country_names = list(res_pop_income.country_name.unique())
print(country_names)

fig, ax = plt.subplots(1, 1, figsize=(12, 14))

# x axis in years 1985-2015
ax.set_xlim(1984.5, 2015.1)
# y axis in millions of people
ax.set_ylim(0, 8100)

plt.xticks(range(1985, 2016, 10), fontsize=14)
plt.yticks(range(0, 8100, 1000), fontsize=14)

plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

for country in res_pop_income.country_name.unique():
    # Plot each line separately with its own color
    country_filter = res_pop_income.loc[res_pop_income['country_name']==country]
    line = plt.plot(country_filter.year,
                    country_filter.value/1000000,
                    lw=2.5,
                    color=color_sequence[country_names.index(country)])
    
    # Add for every line a text label to the right end
    y_pos = (country_filter.value/1000000).iloc[-1]
    plt.text(2015.5, y_pos, country, fontsize=14, 
             color=color_sequence[country_names.index(country)])

# Make the title descriptive enough to avoid including axis labels
fig.suptitle('Total population in the World (millions) by income (1985-2015)\n', 
             fontsize=20, ha='center')

plt.show()

