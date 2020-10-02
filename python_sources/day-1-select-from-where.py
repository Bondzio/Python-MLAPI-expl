
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import bq_helper

hacker_news = bq_helper.BigQueryHelper(active_project= "bigquery-public-data", dataset_name = "hacker_news")
hacker_news.list_tables()
hacker_news.table_schema("full")
hacker_news.head("full")
hacker_news.head("full",selected_columns="by",num_rows=10)
query = """SELECT score FROM `bigquery-public-data.hacker_news.full` WHERE type = "job" """
hacker_news.estimate_query_size(query)
hacker_news.query_to_pandas_safe(query,max_gb_scanned=0.2)
job_post_score = hacker_news.query_to_pandas_safe(query)
job_post_score.score.mean()
job_post_score.to_csv('job_post_score.csv')