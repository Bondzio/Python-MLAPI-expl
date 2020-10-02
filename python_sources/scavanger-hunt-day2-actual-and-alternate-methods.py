# import package with helper functions 
import bq_helper

# create a helper object for this dataset
hacker_news = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="hacker_news")
                                   
# query to pass to count the number of stories by Type of Story
query = """SELECT type , COUNT(id) as Total_stories
            FROM `bigquery-public-data.hacker_news.full`
            GROUP BY type
            HAVING COUNT(id) > 0
        """
        
# the query_to_pandas_safe method will cancel the query if
# it would use too much of your quota, with the limit set 
# to 1 GB by default
popular_stories = hacker_news.query_to_pandas_safe(query)

# Printing the results
print(popular_stories)

# query to count the number of stories are deleted
query = """SELECT COUNT(id) as Deleted_Comments
            FROM `bigquery-public-data.hacker_news.comments`
            WHERE deleted = True
        """
        
# the query_to_pandas_safe method will cancel the query if
# it would use too much of your quota, with the limit set 
# to 1 GB by default
deleted_comments = hacker_news.query_to_pandas_safe(query)

# Printing the results
print(deleted_comments)

# Alternate query to count the number of stories by Type of Story
query = """SELECT type , sum(1) as Total_Stories
            FROM `bigquery-public-data.hacker_news.full`
            GROUP BY type
        """
        
# the query_to_pandas_safe method will cancel the query if
# it would use too much of your quota, with the limit set 
# to 1 GB by default
popular_stories_sum = hacker_news.query_to_pandas_safe(query)

# Printing the results
print(popular_stories_sum)

# query to count the number of stories are deleted
query = """SELECT deleted, sum(1) as Total_Deleted
            FROM `bigquery-public-data.hacker_news.comments`
            WHERE deleted = True
            GROUP BY deleted
        """
        
# the query_to_pandas_safe method will cancel the query if
# it would use too much of your quota, with the limit set 
# to 1 GB by default
deleted_comments_sum = hacker_news.query_to_pandas_safe(query)

# Printing the results
print(deleted_comments_sum)
