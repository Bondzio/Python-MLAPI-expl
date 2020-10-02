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
import math
import warnings
warnings.filterwarnings("ignore")
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


user_reviews = pd.read_csv("/kaggle/input/google-play-store-apps/googleplaystore_user_reviews.csv")


# In[ ]:


user_reviews.head()


# In[ ]:


user_reviews.info()


# In[ ]:


user_reviews.shape


# In[ ]:


user_reviews.columns


# In[ ]:


user_reviews.Translated_Review.isnull().value_counts()


# In[ ]:


googleplaystore = pd.read_csv("/kaggle/input/google-play-store-apps/googleplaystore.csv")


# In[ ]:


googleplaystore.head()


# In[ ]:


googleplaystore.info()


# In[ ]:


googleplaystore.Rating.isnull().value_counts()


# In[ ]:


googleplaystore.describe()


# In[ ]:


user_reviews.describe()


# In[ ]:


cnt = googleplaystore.Category.value_counts()


# In[ ]:


cnt


# In[ ]:


plt.figure(figsize = (16, 10))
sns.barplot(x = cnt[:10].index, y = cnt[:10])
plt.title("Top 10 Categories")
plt.xlabel("Categories")
plt.ylabel("Count")
plt.xticks(rotation = 45)
plt.show()


# In[ ]:


cnt1 = googleplaystore.Genres.value_counts()


# In[ ]:


cnt1


# In[ ]:


plt.figure(figsize = (21, 10))
sns.barplot(x = cnt1[:15].index, y = cnt1[:15])
plt.xlabel("Genres")
plt.ylabel("Count")
plt.title("Top 15 Genres")
plt.xticks(rotation=45)
plt.show()


# In[ ]:


k = googleplaystore.Category.value_counts().index[:10]
k


# In[ ]:


cnt_category = googleplaystore.Category.value_counts().values[:10]
plt.figure(figsize = (20, 10))
sns.barplot(x = cnt_category, y = googleplaystore.Installs.value_counts().index[:10], hue = k, data = googleplaystore)
plt.yticks(rotation = 0)
plt.show()


# In[ ]:


user_reviews.Sentiment.value_counts(dropna = True)


# In[ ]:


plt.figure(figsize = (10, 5))
sns.countplot(x = "Sentiment", data = user_reviews)
plt.xticks(rotation = 45)
plt.xlabel("Sentiment", fontsize = 12)
plt.ylabel("Count", fontsize = 12)
plt.title("User Sentiment Chart", fontsize = 18)
plt.show()


# In[ ]:


user_reviews.Sentiment_Polarity.value_counts()


# In[ ]:


k = user_reviews.Sentiment_Polarity.mean()
k


# In[ ]:


user_reviews["Sentiment_Polarity"] = user_reviews["Sentiment_Polarity"].fillna(k)


# In[ ]:


user_reviews.Sentiment_Polarity.isnull().sum()


# In[ ]:


plt.figure(figsize = (16, 10))
plt.hist(user_reviews.Sentiment_Polarity, bins = 10, edgecolor = "black")
plt.show()


# In[ ]:


googleplaystore.Rating.describe()


# In[ ]:


googleplaystore2 = googleplaystore.rename(columns = {"Content Rating": "Content_Rating"})


# In[ ]:


googleplaystore2.Content_Rating.unique()


# In[ ]:


plt.figure(figsize=(30,10))
sns.boxplot(y="Rating",x="Content_Rating",hue="Type",data=googleplaystore2, palette="Set3")
plt.xticks(rotation=45)
plt.xlabel("Content Rating categories", fontsize=12)
plt.ylabel("Rating",fontsize=12)
plt.title("Rating by Content Rating",fontsize=15)
plt.show()

