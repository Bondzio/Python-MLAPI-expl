#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# libraries:
import ast # for reformatting strings of lists to lists
import time # time processes
import pandas as pd # load database
from tqdm import tqdm # show progress for iteratives
import matplotlib.pyplot as plt # for plotting


# ### Loading the Database
# #### In total, it takes ~70 seconds to load the whole database. 

# In[ ]:


# load the data
start_time = time.time()
stock_tweet_database = pd.read_csv('/kaggle/input/800k-stock-tweet-database/stock_related_tweets.csv', index_col = 0)
end_time = time.time()
print('Time to load database: {} seconds'.format(round(end_time - start_time, 3)))


# In[ ]:


# some items in the dataset are strings of lists. this reformats them into usable lists.
start_time = time.time()
string_of_list_columns = ['stocks_mentioned', 'urls_mentioned'] # these columns are strings of lists
for column in string_of_list_columns:
    for i in tqdm(stock_tweet_database.index):
        item = stock_tweet_database.loc[i, column]
        if type(item) == str:
            item = ast.literal_eval(item)
            stock_tweet_database.at[i, column] = item
end_time = time.time()
print('Time to load process lists: {} seconds'.format(round(end_time - start_time, 3)))


# ### Sample EDA
# #### The database has been completely loaded. Everything else below is just basic EDA.

# In[ ]:


print('Number of unique stocks: {}'.format(len(stock_tweet_database['stock'].unique())))
print('Number of unique tweet creators: {}'.format(len(stock_tweet_database['tweet_creator'].unique())))


# In[ ]:


value_counts = stock_tweet_database['tweet_creator'].value_counts()


# In[ ]:


print(value_counts)


# In[ ]:


explode_pcts = [0.3] + ([0.0] * (len(value_counts[:100]) - 1))


# In[ ]:


plt.pie(value_counts[:100], explode = explode_pcts, labels = value_counts[:100].index, shadow = True)
plt.show()


# In[ ]:


# add your code here and below:


# ...


# In[ ]:




