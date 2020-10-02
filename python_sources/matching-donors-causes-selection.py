#!/usr/bin/env python
# coding: utf-8

# Table of contents
# 1. Data loading
# 2. variables relationship
# 3. variables selection
# 4. modulation
# 5. testing
# 

# # import package

# In[1]:


import os
import gc
import glob
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA, KernelPCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import pairwise_distances_argmin_min, pairwise_distances
import arrow
get_ipython().run_line_magic('matplotlib', 'inline')
# import cufflinks and offline mode
import cufflinks as cf
cf.go_offline()

from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread
import base64

from sklearn import preprocessing
# Supress unnecessary warnings so that presentation looks clean
import warnings
warnings.filterwarnings("ignore")

# Print all rows and columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[2]:


donations = pd.read_csv('../input/Donations.csv')
donors = pd.read_csv('../input/Donors.csv', low_memory=False)
schools = pd.read_csv('../input/Schools.csv', error_bad_lines=False)
teachers = pd.read_csv('../input/Teachers.csv', error_bad_lines=False)
projects = pd.read_csv('../input/Projects.csv', error_bad_lines=False, warn_bad_lines=False, parse_dates=["Project Posted Date","Project Fully Funded Date"])
resources = pd.read_csv('../input/Resources.csv', error_bad_lines=False, warn_bad_lines=False)


# In[5]:


projects.head(1)
#projects.describe()


# In[6]:


projects.describe()


# In[11]:


missing_projects=projects.isnull().sum(axis=0).reset_index()
missing_projects.columns=['column_name', 'missing_count']
missing_projects['filling_factor']=(missing_projects.shape[0]-missing_projects['missing_count'])/missing_projects.shape[0]*100
missing_projects.sort_values('filling_factor').reset_index(drop = True)


# In[12]:


missing_donations=donations.isnull().sum(axis=0).reset_index()
missing_donations.columns=['column_name', 'missing_count']
missing_donations['filling_factor']=(missing_donations.shape[0]-missing_donations['missing_count'])/missing_donations.shape[0]*100
missing_donations.sort_values('filling_factor').reset_index(drop = True)


# In[13]:


missing_donors=donors.isnull().sum(axis=0).reset_index()
missing_donors.columns=['column_name', 'missing_count']
missing_donors['filling_factor']=(missing_donors.shape[0]-missing_donors['missing_count'])/missing_donors.shape[0]*100
missing_donors.sort_values('filling_factor').reset_index(drop = True)


# # EDA
# # 2.1 combine donations and projects

# In[2]:


project_donations=projects.merge(donations, on='Project ID', how='left')
project_donations.head(1)


# # 2.2 get Time Elapse and extra column of donation month

# In[4]:


from datetime import datetime
d1=project_donations['Project Posted Date']
project_donations['Donation Received Date']=pd.to_datetime(project_donations['Donation Received Date'], infer_datetime_format=True)
d2=project_donations['Donation Received Date'].dt.to_period('D')


# In[5]:


project_donations['Time Elapse']=(pd.to_datetime(project_donations['Donation Received Date'])-pd.to_datetime(project_donations['Project Posted Date'])).apply(lambda x: x.days)


# In[12]:


project_donations.head(2)


# In[6]:


# donation Time Elapse distribution
temp = project_donations['Time Elapse'].value_counts().head(5)
temp.iplot(kind='bar', xTitle = 'Time Elapse', yTitle = "Count", title = 'Distribution of Time Elapse', color='green')


# more than 50% donation within one to two day afters project post, 10.4/17.8

# In[10]:


temp.head(10)


# # 2.3 Project Type: Teacher-Led (according other person analysis) : more than 95%
# 

# # 2.4 Text mining for project title, essay and sub category

# # 2.4.1 Text mining for Project Title

# In[7]:


# dataset name : project_donations
names = project_donations["Project Title"][~pd.isnull(project_donations["Project Title"])].sample(1000)
#print(names)
wordcloud = WordCloud(max_font_size=50, width=600, height=300).generate(' '.join(names))
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.title("Wordcloud for Top Keywords from project Titles", fontsize=35)
plt.axis("off")
plt.show() 


# In[8]:


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

stop = set(stopwords.words('english'))
stop.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '@', '#', 'rt', 'amp', 'realdonaldtrump', 'http', 'https', '/', '://', '_', 'co', 'trump', 'donald', 'makeamericagreatagain'])

series_tweets = project_donations["Project Title"]
tweet_str = series_tweets.str.cat(sep = ' ')
list_of_words = [i.lower() for i in wordpunct_tokenize(tweet_str) if i.lower() not in stop and i.isalpha()]
wordfreqdist = nltk.FreqDist(list_of_words)
mostcommon = wordfreqdist.most_common(30)
print(mostcommon)

plt.barh(range(len(mostcommon)),[val[1] for val in mostcommon], align='center')
plt.yticks(range(len(mostcommon)), [val[0] for val in mostcommon])
plt.show()


# # 2.4.2 project Essay text mining

# In[9]:


# top topic in the Project Subject Category Tree
#Top Keywords from project Essay
from wordcloud import WordCloud, STOPWORDS
names = project_donations["Project Essay"][~pd.isnull(project_donations["Project Essay"])].sample(10000)
#print(names)
wordcloud = WordCloud(max_font_size=50, width=600, height=300).generate(' '.join(names))
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.title("Wordcloud for Top Keywords from project Essay", fontsize=35)
plt.axis("off")
plt.show() 


# In[ ]:


series_tweets = project_donations["Project Essay"]
tweet_str = series_tweets.str.cat(sep = ' ')
list_of_words = [i.lower() for i in wordpunct_tokenize(tweet_str) if i.lower() not in stop and i.isalpha()]
wordfreqdist = nltk.FreqDist(list_of_words)
mostcommon = wordfreqdist.most_common(30)
print(mostcommon)

plt.barh(range(len(mostcommon)),[val[1] for val in mostcommon], align='center')
plt.yticks(range(len(mostcommon)), [val[0] for val in mostcommon])
plt.show()


# In[ ]:


# 2.4.3 Text mining for project sub category tree


# In[ ]:


# project Essay
series_tweets = project_donations["Project Essay"]
tweet_str = series_tweets.str.cat(sep = ' ')
list_of_words = [i.lower() for i in wordpunct_tokenize(tweet_str) if i.lower() not in stop and i.isalpha()]
wordfreqdist = nltk.FreqDist(list_of_words)
mostcommon = wordfreqdist.most_common(30)
print(mostcommon)

plt.barh(range(len(mostcommon)),[val[1] for val in mostcommon], align='center')
plt.yticks(range(len(mostcommon)), [val[0] for val in mostcommon])
plt.show()


# In[ ]:


series_tweets = project_donations["Project Title"]
tweet_str = series_tweets.str.cat(sep = ' ')
list_of_words = [i.lower() for i in wordpunct_tokenize(tweet_str) if i.lower() not in stop and i.isalpha()]
wordfreqdist = nltk.FreqDist(list_of_words)
mostcommon = wordfreqdist.most_common(30)
print(mostcommon)

plt.barh(range(len(mostcommon)),[val[1] for val in mostcommon], align='center')
plt.yticks(range(len(mostcommon)), [val[0] for val in mostcommon])
plt.show()


# Missing values

# In[1]:


missing_project_donations=project_donations.idnull().sum(axis=0).reset_index()
missing_project_donations.columns=['column_name', 'missing_count']
missing_project_donations['filling_factor']=(missing_project_donations.shape[0]-missing_project_donations['missing_count'])/df_initial.shape[0]*100
missing_project_donations.sort_values('filling_factor').reset_index(drop = True)


# In[ ]:




