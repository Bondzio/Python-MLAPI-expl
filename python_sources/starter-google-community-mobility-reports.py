#!/usr/bin/env python
# coding: utf-8

# # 1. Initial Setup
# First, import necessary python libraries including google.cloud:

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import plotly.express as px
from google.cloud import bigquery


# Next, list tables in a public dataset `covid19_google_mobility`

# In[ ]:


client = bigquery.Client()

# List the tables in covid19_google_mobility dataset which resides in bigquery-public-data project:
dataset = client.get_dataset('bigquery-public-data.covid19_google_mobility')
tables = list(client.list_tables(dataset))
print([table.table_id for table in tables])


# # 2. Data Exploration
# ## 2.1. How have San Francisco's mobility patterns changed a week before and after the "shelter-in-place" order was issued?
# This query examines the changes in mobility patterns within San Francisco county before and after the city's "shelter-in-place" order was issued March 17th, 2020. The first date (03-10-2020) is a week before the order was issued, and the second date (03-24-2020) is a week after the order was issued.

# In[ ]:


sql = '''
SELECT
  *
FROM
  `bigquery-public-data.covid19_google_mobility.mobility_report` 
WHERE
  country_region = "United States"
  AND sub_region_1 = "California"
  AND sub_region_2 = "San Francisco County"
  AND date BETWEEN "2020-03-10" AND "2020-03-24"
ORDER BY
  date
'''
# Set up the query
query_job = client.query(sql)

# Make an API request  to run the query and return a pandas DataFrame
df = query_job.to_dataframe()
df.head(5)


# In[ ]:


fig = plt.figure();
df.plot(x='date', rot=45, y=['retail_and_recreation_percent_change_from_baseline',                                  
                             'grocery_and_pharmacy_percent_change_from_baseline',
                             'parks_percent_change_from_baseline',
                             'transit_stations_percent_change_from_baseline',
                             'workplaces_percent_change_from_baseline',
                             'residential_percent_change_from_baseline'])
plt.legend(bbox_to_anchor=(1, 0.5), loc='lower left')
plt.xlabel('Date')
plt.ylabel('Percent Change From Baseline')
plt.show()


# ## 2.2. Show the latest changes in retail and recreation for each US state
# For each US state, select the most recent `retail_and_recreation_percent_change_from_baseline` averaged by county.

# In[ ]:


sql = '''
select sub_region_1, avg(retail_and_recreation_percent_change_from_baseline) percent_change
from (
  SELECT 
    sub_region_1,
    sub_region_2,
    date,
    retail_and_recreation_percent_change_from_baseline,
    max(date) over (partition by sub_region_1) max_date
  FROM `bigquery-public-data`.covid19_google_mobility.mobility_report
  where country_region_code = 'US' and sub_region_1 is not null
)
where date = max_date
group by sub_region_1
'''
# Set up the query
query_job = client.query(sql)

# Make an API request  to run the query and return a pandas DataFrame
df = query_job.to_dataframe()
df.head(5)


# Next, plot the results on the US map. To do so, you'll need to use state abbreviations. So, create a helper dataframe and merge it with the above results:

# In[ ]:


states = {
    'state': [
        'Alabama',
        'Alaska',
        'Arizona',
        'Arkansas',
        'California',
        'Colorado',
        'Connecticut',
        'Delaware',
        'District of Columbia',
        'Florida',
        'Georgia',
        'Hawaii',
        'Idaho',
        'Illinois',
        'Indiana',
        'Iowa',
        'Kansas',
        'Kentucky',
        'Louisiana',
        'Maine',
        'Maryland',
        'Massachusetts',
        'Michigan',
        'Minnesota',
        'Mississippi',
        'Missouri',
        'Montana',
        'Nebraska',
        'Nevada',
        'New Hampshire',
        'New Jersey',
        'New Mexico',
        'New York',
        'North Carolina',
        'North Dakota',
        'Ohio',
        'Oklahoma',
        'Oregon',
        'Pennsylvania',
        'Rhode Island',
        'South Carolina',
        'South Dakota',
        'Tennessee',
        'Texas',
        'Utah',
        'Vermont',
        'Virginia',
        'Washington',
        'West Virginia',
        'Wisconsin',
        'Wyoming',
        'Puerto Rico'], 
    'abbreviation': [
        'AL',
        'AK',
        'AZ',
        'AR',
        'CA',
        'CO',
        'CT',
        'DE',
        'DC',
        'FL',
        'GA',
        'HI',
        'ID',
        'IL',
        'IN',
        'IA',
        'KS',
        'KY',
        'LA',
        'ME',
        'MD',
        'MA',
        'MI',
        'MN',
        'MS',
        'MO',
        'MT',
        'NE',
        'NV',
        'NH',
        'NJ',
        'NM',
        'NY',
        'NC',
        'ND',
        'OH',
        'OK',
        'OR',
        'PA',
        'RI',
        'SC',
        'SD',
        'TN',
        'TX',
        'UT',
        'VT',
        'VA',
        'WA',
        'WV',
        'WI',
        'WY',
        'PR']}
state_abbr = pd.DataFrame(states)
state_abbr


# In[ ]:


df = df.merge(state_abbr, left_on='sub_region_1', right_on='state')[['percent_change', 'abbreviation']]


# Finally, plot the results on the map:

# In[ ]:


fig = px.choropleth(df, locationmode="USA-states", locations='abbreviation', color='percent_change', scope="usa")
fig.show()

