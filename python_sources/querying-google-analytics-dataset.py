#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from google.cloud import bigquery


# #### Retrieving Dataset

# In[ ]:


client = bigquery.Client()

dataset_ref = client.dataset('google_analytics_sample', project='bigquery-public-data')

dataset = client.get_dataset(dataset_ref)


# #### Viewing Tables

# In[ ]:


tables = list(client.list_tables(dataset))

list_of_tables = [table.table_id for table in tables]

print(list_of_tables)


# #### Viewing columns inside the last table

# In[ ]:


last_table_ref = dataset_ref.table('ga_sessions_20170801')

last_table = client.get_table(last_table_ref)

client.list_rows(last_table, max_results=5).to_dataframe()


# #### First Query: Finding total hits for 2017-08-01

# In[ ]:


q1 = '''
     SELECT date, COUNT(hits) AS hits
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`
     GROUP BY date
     '''

safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
q1_job = client.query(q1, job_config=safe_config)

q1_results = q1_job.to_dataframe()

print(q1_results)


# #### Second Query: Visits per Continent

# In[ ]:


q2 = '''
     SELECT geoNetwork AS place
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`
     '''

safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
q2_job = client.query(q2, job_config=safe_config)

q2_results = q2_job.to_dataframe()

continent_lst = []
for x in q2_results['place']:
    x = x['continent']
    continent_lst.append(x)
q2_results['continents'] = continent_lst

continent_count = {'Americas': 0, 'Asia': 0, 'Europe': 0, 'Oceania': 0, 'Africa': 0}
for continent in q2_results['continents']:
    if continent == 'Americas':
        continent_count['Americas'] += 1
    if continent == 'Asia':
        continent_count['Asia'] += 1
    if continent == 'Europe':
        continent_count['Europe'] += 1
    if continent == 'Oceania':
        continent_count['Oceania'] += 1
    if continent == 'Africa':
        continent_count['Africa'] += 1
    


# In[ ]:


labels = continent_count.keys()
data = continent_count.values()
explode = (0.05, 0, 0,0,0)

plt.figure(figsize=(5,5))
plt.pie(data, labels=labels, explode=explode, autopct='%1.1f%%', startangle=55)
plt.title('Visits per Continent')
plt.axis('equal') 

plt.show()


# #### Third Query: 2-day channel comparison 

# In[ ]:


q3 = '''
     SELECT date, a.channelGrouping AS channel, COUNT(a.channelGrouping) AS total
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801` AS a
     GROUP BY date, a.channelGrouping
     UNION ALL
     SELECT date, b.channelGrouping AS channel, COUNT(b.channelGrouping) AS total
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170731` AS b
     GROUP BY date, b.channelGrouping
     '''

safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
q3_job = client.query(q3, job_config=safe_config)

q3_results = q3_job.to_dataframe()

print(q3_results)


# In[ ]:


day1_lst = []
for x in q3_results['total'][0:7]:
    day1_lst.append(x)
    
day2_lst = []
for x in q3_results['total'][7:14]:
    day2_lst.append(x)    
    
N = 7
ind = np.arange(N)
width = 0.35

fig, ax = plt.subplots()

day1_bars = ax.bar(ind, day1_lst, width)
day2_bars = ax.bar(ind + width, day2_lst, width)

ax.set_ylabel('Total')
ax.set_title('2-Day Channel Comparison')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('Organic Search', 'Direct', 'Referral', 'Display', 'Paid Search', 'Affiliates', 'Social'), rotation='vertical')

ax.legend((day1_bars[0], day2_bars[0]), ('2017/07/31', '2017/08/01'))

plt.show()


# #### Fourth Query: Finding repeat visitors for one day

# In[ ]:


q4 = '''
     SELECT fullVisitorId,
         COUNT(visitNumber)OVER(
                                PARTITION BY visitId
                                ORDER BY visitNumber DESC
                                ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
                               )as repeat_visitor
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`
     WHERE visitNumber >= 2
     '''

safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
q4_job = client.query(q4, job_config=safe_config)

q4_results = q4_job.to_dataframe()

print(q4_results)


# In[ ]:


returning_visitors = 684
new_visitors = 2556 - returning_visitors

labels = ['Returning Visitor', 'New Visitor']
data = [returning_visitors, new_visitors]

plt.figure(figsize=(5,5))
plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=130)
plt.title('Returning vs New Visitors (2017-08-01)')
plt.axis('equal') 

plt.show()


# #### Fifth Query: Finding traffic sources with count larger than 10

# In[ ]:


print(last_table.schema[6])


# In[ ]:


q5 = '''
     SELECT trafficSource.source AS source, COUNT(trafficSource) as counts
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`
     GROUP BY source
     HAVING counts >= 10
     ORDER BY counts DESC
     '''

safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
q5_job = client.query(q5, job_config=safe_config)

q5_results = q5_job.to_dataframe()

print(q5_results)


# In[ ]:


category_names = q5_results['source']
results = {
    'counts': q5_results['counts']
          }


def survey(results, category_names):
   
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(13, 2.5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='large')

    return fig, ax


survey(results, category_names)
plt.show()


# In[ ]:


print(category_names)


# #### Sixth Query: Finding total visits per hour of day

# In[ ]:


print(last_table.schema[5])


# In[ ]:


print(last_table.schema[10])


# In[ ]:


q6 = '''
     SELECT hits.hour AS hour, SUM(totals.visits) AS visits
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`, UNNEST(hits) AS hits
     GROUP BY hour
     ORDER BY hour
     '''

safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
q6_job = client.query(q6, job_config=safe_config)

q6_results = q6_job.to_dataframe()

print(q6_results)


# In[ ]:


x = q6_results['hour']
y = q6_results['visits']

plt.figure(figsize=(15,10))
plt.bar(x, y, width=1)
plt.title('Visits per Hour of Day')
plt.xlabel('Hour')
plt.xticks(q6_results.index, q6_results['hour'])
plt.ylabel('Visits')


plt.show()


# #### Seventh Query: Monthly device visits

# In[ ]:


from time import time

def show_amount_of_data_scanned(query):
    dry_run_config = bigquery.QueryJobConfig(dry_run=True)
    query_job = client.query(query, job_config=dry_run_config)
    print('Data processed: {} GB'.format(round(query_job.total_bytes_processed / 10**9, 3)))
    
def show_time_to_run(query):
    time_config = bigquery.QueryJobConfig(use_query_cache=False)
    start = time()
    query_result = client.query(query, job_config=time_config).result()
    end = time()
    print('Time to run: {} seconds'.format(round(end-start, 3)))


# In[ ]:


print(last_table.schema[7])


# In[ ]:


q7 = '''
     SELECT date, august.device.deviceCategory AS device, SUM(august.totals.visits) AS visits
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801` AS august
     GROUP BY date, device
     UNION ALL
     SELECT date, july.device.deviceCategory as device, SUM(july.totals.visits) as visits
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170701` as july
     GROUP BY date, device
     UNION ALL
     SELECT date, june.device.deviceCategory as device, SUM(june.totals.visits) as visits
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170601` as june
     GROUP BY date, device
     UNION ALL
     SELECT date, may.device.deviceCategory as device, SUM(may.totals.visits) as visits
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170501` as may
     GROUP BY date, device
     UNION ALL
     SELECT date, april.device.deviceCategory as device, SUM(april.totals.visits) as visits
     FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170401` as april
     GROUP BY date, device
     ORDER BY date, device
     '''

safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
q7_job = client.query(q7, job_config=safe_config)

q7_results = q7_job.to_dataframe()

print(q7_results)

show_amount_of_data_scanned(q7)
show_time_to_run(q7)


# In[ ]:


desktop = q7_results['visits'][0::3]
mobile = q7_results['visits'][1::3]
tablet = q7_results['visits'][2::3]
x = ['April', 'May', 'June', 'July', 'August']

y = np.vstack([tablet, mobile, desktop])

labels = ['Tablet', 'Mobile', 'Desktop']

plt.figure(figsize=(10,7))
plt.stackplot(x, tablet, mobile, desktop, labels=labels)
plt.title('Monthly Device Visits (2017)')
plt.ylabel('Visits')
plt.xlabel('Month')
plt.legend(loc='upper left')
plt.show()

