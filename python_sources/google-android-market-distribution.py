#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly
import plotly.graph_objs as go
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


google_reviews = pd.read_csv('../input/googleplaystore_user_reviews.csv')
google_apps = pd.read_csv('../input/googleplaystore.csv')


# **Categories Distribution**

# In[ ]:


plt.figure(figsize=(16,5))
google_apps['Category'].value_counts().plot.bar()
# google_apps_value = pd.DataFrame(google_apps_value)
# google_apps_value.plot.bar()


# In[ ]:


google_apps.isnull().sum()


# In[ ]:


google_apps.shape


# **Data Cleaning**

# In[ ]:


google_apps_clean = google_apps.dropna(axis=0,how='any')


# In[ ]:


google_apps_clean.shape


# In[ ]:


google_apps_clean['Size'] = google_apps_clean['Size'].apply(lambda x: str(x).replace('Varies with device', 'NaN') if 'Varies with device' in str(x) else x)
google_apps_clean['Size'] = google_apps_clean['Size'].apply(lambda x: str(x).replace('M', '') if 'M' in str(x) else x)
google_apps_clean['Size'] = google_apps_clean['Size'].apply(lambda x: float(str(x).replace('k', '')) / 1000 if 'k' in str(x) else x)


# In[ ]:


google_apps_clean = google_apps_clean.dropna(axis=0,how='any')


# In[ ]:


google_apps_clean['Installs'] = google_apps_clean['Installs'].apply(lambda x : str(x).replace('+','') if '+' in str(x) else x)
google_apps_clean['Installs'] = google_apps_clean['Installs'].apply(lambda x : str(x).replace(',','') if ',' in str(x) else x)
google_apps_clean['Installs'] = google_apps_clean['Installs'].apply(lambda x : int(x))


# In[ ]:


google_apps_clean.isnull().sum()


# In[ ]:


google_apps_clean = google_apps_clean.dropna(axis=0,how='any')
google_apps_clean['Price'] = google_apps_clean['Price'].apply(lambda x : str(x).replace('$','') if '$' in str(x) else x)
google_apps_clean['Price'] = google_apps_clean['Price'].apply(lambda x : float(x))
google_apps_clean= google_apps_clean[google_apps_clean['Size']!='NaN']
paid_apps=google_apps_clean[google_apps_clean['Price']>0]


# In[ ]:


paid_apps=paid_apps.groupby('Category').count().sort_values('App',ascending=False).head()
paid_apps['App']


# In[ ]:


sns.countplot(data=google_apps_clean, y='Installs')
plt.xlabel('No. of Apps Installed')


# In[ ]:


f,(ax1,ax2)=plt.subplots(1,2,figsize=(16,5))
google_apps_clean['Size'] = google_apps_clean['Size'].apply(lambda x : float(x))
sns.distplot(google_apps_clean['Size'],bins=30,ax=ax1)
plt.xlabel('Size Distribution')
sns.distplot(google_apps_clean['Rating'],bins=20,ax=ax2)
plt.xlabel('Rating Distribution')
print("Average Rating of Apps ",google_apps_clean['Rating'].mean())
print("Average Size of Apps ",google_apps_clean['Size'].mean())


# **Mean Distribution of Rating, Size, Installs, Price**

# In[ ]:


google_apps_clean.groupby(['Category']).mean()


# In[ ]:


sns.countplot(data= google_apps_clean,x='Type')

# for index, row in google_apps_clean.iterrows():
#     g.text(row.name,row.tip, round(row.total_bill,2), color='black', ha="center")


# In[ ]:


google_reviews_clean = google_reviews.dropna(axis=0,how='any')
reviews_groups = google_reviews_clean.groupby(['App','Sentiment']).count().reset_index()
reviews_groups[['App','Sentiment','Translated_Review']]


# In[ ]:


from wordcloud import WordCloud
review_trans = google_reviews_clean['Translated_Review'].unique().tolist()
review_trans = ' '.join(google_reviews_clean['Translated_Review'].unique().tolist())
review_trans = WordCloud().generate(review_trans)
plt.figure(figsize=(10,5))
plt.imshow(review_trans)
plt.show


# **Word Cloud based on the Sentiment Score**

# In[ ]:


import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def POS_NEG(test_subset):
    test_subset=pos_neg.split()
    sid = SentimentIntensityAnalyzer()
    pos_word_list=[]
    neu_word_list=[]
    neg_word_list=[]
    for word in test_subset:
        if (sid.polarity_scores(word)['compound']) >= 0.3:
            pos_word_list.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.3:
            neg_word_list.append(word)
        else:
            neu_word_list.append(word)
    pos_word_list = ' '.join(pos_word_list)
    neg_word_list = ' '.join(neg_word_list)
    neu_word_list = ' '.join(neu_word_list)
    
    from wordcloud import WordCloud
    cloud = WordCloud().generate(pos_word_list)
    plt.figure(figsize=(16,10))
    plt.title('Positive WordCloud Distribution')
    plt.imshow(cloud)
    plt.show
        
    cloud = WordCloud().generate(neg_word_list)
    plt.figure(figsize=(16,10))
    plt.title('NEGATIVE WORDCLOUD Distribution')
    plt.imshow(cloud)
    plt.show
    
    cloud = WordCloud().generate(neu_word_list)
    plt.figure(figsize=(16,10))
    plt.title('Neutral WordCloud Distribution')
    plt.imshow(cloud)
    plt.show


# In[ ]:


pos_neg=' '.join(google_reviews_clean['Translated_Review'].unique().tolist())
POS_NEG(pos_neg)


# In[ ]:


from wordcloud import WordCloud
review_trans = google_reviews_clean['App'].unique().tolist()
review_trans = ' '.join(google_reviews_clean['App'].unique().tolist())
review_trans = WordCloud().generate(review_trans)
plt.figure(figsize=(10,5))
plt.title('Apps Names')
plt.imshow(review_trans)
plt.show


# In[ ]:


plt.figure(figsize=(10,16))
google_reviews_clean['App'].value_counts().head(50).plot.barh()
plt.xlabel('No. of Reviewers')
plt.ylabel('Top 50 Apps')


# **Conclusion**
# 1.  Average Size of Apps = 23MB.
# 2. Average Rating of Apps = 4.17 out of 5
# 3. There are 3 Categories Family, Game, Tools(like Share It,File Manager) of apps which are most rated and Reviewed.
# 4. There are 5 Categories Family, Medical, Game, Tools, Personlization of Paid Apps are rated and Reviewed.
# 5. Users will download app if it has been reviewed by a large number of people of particular Category.
