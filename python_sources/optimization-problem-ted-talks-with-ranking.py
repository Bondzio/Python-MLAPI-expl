#!/usr/bin/env python
# coding: utf-8

# In[96]:


# import the libraries
#plot outputs will be  visible and stored within the notebook
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd    # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np        #for using linear algebra
import scipy     #for optimization problem solving
import matplotlib.pyplot as plt #pyplot is matplotlib's plotting framework which import line from the module "matplotlib.pyplot" and binds that to the name "plt".
import ast #abstract syntax tree


# In[97]:


# load the dataset
df = pd.read_csv('../input/ted_main.csv')
# download the csv file in your local directory and play with it
df.columns
print(df) #print the data frame according to column 


# In[98]:


#sorting data
df = df[['name', 'title', 'description', 'main_speaker', 'speaker_occupation', 'num_speaker', 'duration', 'event', 'film_date', 'published_date', 'comments', 'tags', 'languages', 'ratings', 'related_talks', 'url', 'views']]
print (df)


# In[114]:


#df.head(n) returns a DataFrame holding the first n rows of df, here it is used to see a glimpse of dataset
df.head()


# In[100]:


len(df) #len shows what is the length of data   


# In[101]:


#sorting popular talks in decending order according to view
pop_talks = df[['title', 'main_speaker', 'views']].sort_values('views', ascending=False)[:10]
pop_talks


# In[ ]:


#ranking depending on views
pop_talks['ranking_on_views']=df['views'].rank(ascending=False)
pop_talks


# In[103]:


df.iloc[1]['ratings'] #Purely integer-location based indexing for selection by position


# In[104]:


df['ratings'] = df['ratings'].apply(lambda x:ast.literal_eval(x)) 
#Safely evaluate an expression node or a Unicode or Latin-1 encoded string containing a Python expression. 
#this syntax makes sure that only ratings datas will go as input


# In[109]:


#lambda is used in conjunction with typical functional concepts like filter(), map() and reduce().
#filter() calls our lambda function for each element of the list, and returns a new list that contains only those elements for which the function returned "True".
# map() is used to convert our list
#The return value of the last call is the result of the reduce() construct.
df['jawdrop'] = df['ratings'].apply(lambda x: x[-3]['count'])
df['beautiful'] = df['ratings'].apply(lambda x: x[3]['count'])
df['confusing'] = df['ratings'].apply(lambda x: x[2]['count'])


# In[110]:


#sorting ted talks in decending order according to rating
beautiful = df[['title', 'main_speaker', 'views', 'beautiful']].sort_values('beautiful', ascending=False)[:10]
beautiful


# In[111]:


#ranking depending on rating
beautiful['ranking_on_rating:beautiful']=df['beautiful'].rank(ascending=False)
beautiful


# In[112]:


#sorting ted talks in decending order according to rating
jawdrop = df[['title', 'main_speaker', 'views', 'jawdrop']].sort_values('jawdrop', ascending=False)[:10]
jawdrop


# In[113]:


#ranking depending on rating
jawdrop['ranking_on_rating(jawdrop)']=df['jawdrop'].rank(ascending=False)
jawdrop


# In[37]:


#sorting ted talks in decending order according to rating
confusing = df[['title', 'main_speaker', 'views', 'confusing']].sort_values('confusing', ascending=False)[:10]
confusing


# In[38]:


#ranking depending on rating
confusing['ranking_on_rating(confusing)']=df['confusing'].rank(ascending=False)
confusing


# In[40]:


import tensorflow as tf
feature_columns = []
views = tf.feature_column.numeric_column('views')
feature_columns.append(views)


# In[41]:


views_buckets = tf.feature_column.bucketized_column(
                        tf.feature_column.numeric_column('views'), 
                        boundaries = [10000000,20000000,30000000,40000000]

)
feature_columns.append(views_buckets)


# In[42]:


print(views_buckets)

