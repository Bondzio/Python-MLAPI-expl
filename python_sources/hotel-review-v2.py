#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


file_path="/kaggle/input/515k-hotel-reviews-data-in-europe/Hotel_Reviews.csv"
reviews= pd.read_csv(file_path)
reviews.head()


# In[ ]:


reviews.rename(columns={'Review_Total_Negative_Word_Counts': 'Total_Negative_Word','Review_Total_Positive_Word_Counts':'Total_Positive_Word',
                        'Additional_Number_of_Scoring':'Additional_Scoring'}, inplace=True)


# In[ ]:


reviews.describe()


# In[ ]:


reviews.info()


# In[ ]:


reviews.isnull().sum()


# In[ ]:


reviews.duplicated().sum()


# In[ ]:


duplicateRowsreviews = reviews[reviews.duplicated()]
duplicateRowsreviews.head()


# In[ ]:


reviews.Reviewer_Score.value_counts()


# In[ ]:


reviews.Average_Score.value_counts()


# In[ ]:


data_plot =reviews[["Hotel_Name","Average_Score"]].drop_duplicates()
fig, ax = pyplot.subplots(figsize=(30, 12))
sns.countplot(ax = ax,x = "Average_Score",data=data_plot)


# In[ ]:


reviews['year'] = pd.DatetimeIndex(reviews['Review_Date']).year
reviews['month'] = pd.DatetimeIndex(reviews['Review_Date']).month
reviews["score"] = np.where(reviews.eval("Reviewer_Score > 5"), "1", "0")
reviews.drop(columns=['Hotel_Address', 'Review_Date'],inplace=True)


# In[ ]:


reviews.score.value_counts()


# In[ ]:


sns.pairplot(reviews)


# # Correlation

# In[ ]:


df_corr = reviews.corr()
plt.figure(figsize=(15,10))
sns.heatmap(df_corr, annot = True)
plt.title("Correlation between the variables", fontsize = 22)
plt.show()


# In[ ]:


nans = lambda reviews: reviews[reviews.isnull().any(axis=1)]
nans_df = nans(reviews)
nans_df = nans_df[['Hotel_Name','lat','lng']]
print('No of missing values in the dataset: {}'.format(len(nans_df)))


# In[ ]:


len(nans_df.groupby('Hotel_Name').Hotel_Name.count())


# In[ ]:


reviews.Reviewer_Nationality.value_counts()


# In[ ]:


reviews.Hotel_Name.value_counts()


# In[ ]:


reviews.groupby(["Reviewer_Nationality","score"])["score"].count()


# In[ ]:


reviews.groupby(["Hotel_Name"]).Reviewer_Score.agg([max,min])


# In[ ]:


reviews.groupby(["Hotel_Name",'Reviewer_Nationality']).Reviewer_Score.count().head()


# In[ ]:


reviews.groupby(["Hotel_Name",'Reviewer_Nationality']).Reviewer_Score.max().head()


# In[ ]:


plt.figure(figsize=(25,10))
sns.scatterplot(x=reviews['Total_Negative_Word'], y=reviews['Total_Positive_Word'],hue=reviews['score'])


# In[ ]:


plt.figure(figsize=(25,10))
sns.scatterplot(x=reviews['Total_Positive_Word'], y=reviews['Average_Score'],hue=reviews['score'])


# In[ ]:


reviews.groupby(["month"]).Average_Score.max()


# In[ ]:


plt.figure(figsize=(25,6))
plt.ylabel("Average_Score")
sns.barplot(x=reviews.month, y=reviews['Average_Score'])


# In[ ]:


plt.figure(figsize=(10,6))
plt.ylabel("Average_Score")
sns.barplot(x=reviews.year, y=reviews['Average_Score'])


# In[ ]:


plt.figure(figsize=(25,6))
plt.ylabel("Average_Score")
sns.barplot(x=reviews.year, y=reviews['Total_Positive_Word'],hue=reviews['score'])


# In[ ]:


plt.figure(figsize=(15,6))
plt.ylabel("Average_Score")
sns.barplot(x=reviews.month, y=reviews['Total_Positive_Word'],hue=reviews['score'])


# In[ ]:


sns.lineplot(x=reviews.month, y=reviews['Total_Positive_Word'],hue=reviews['score'], data=reviews)


# In[ ]:


plt.figure(figsize=(20,6))

sns.lineplot(x=reviews.month, y=reviews['Total_Negative_Word'],hue=reviews['score'], data=reviews)


# In[ ]:


plt.figure(figsize=(10,6))
sns.scatterplot(x=reviews.lat, y=reviews.lng, hue=reviews['score'])


# In[ ]:


from matplotlib import pyplot
fig, ax = pyplot.subplots(figsize=(30, 8))
sns.countplot(ax = ax,x = "month",hue="score",data=reviews)


# # **WordCloud**

# In[ ]:


from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def show_wordcloud(data, title = None):
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud( background_color = 'white',max_words = 200,max_font_size = 40,scale=3,random_state = 50,stopwords=stopwords).generate(str(data))

    fig = plt.figure(1, figsize = (20, 20))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize = 15)
        fig.subplots_adjust(top = 2.3)

    plt.imshow(wordcloud)
    plt.show()


# In[ ]:


show_wordcloud(reviews["Positive_Review"])


# In[ ]:


show_wordcloud(reviews["Negative_Review"])


# In[ ]:


show_wordcloud(reviews["Reviewer_Nationality"])


# # Positive and Negative count

# In[ ]:


reviews["pos_count"] = 1
reviews["neg_count"] = 1
reviews["pos_count"] = reviews.apply(lambda x: 0 if x["Positive_Review"] in ['No Positive',"Nothing",'n a','no','none'] else x["pos_count"],axis =1)
reviews["neg_count"] = reviews.apply(lambda x: 0 if x["Negative_Review"] in ['No Negative',"Nothing",'n a','no','none'] else x["neg_count"],axis =1)


# In[ ]:


reviews.head()


# In[ ]:


pos=reviews.groupby(["Hotel_Name","Average_Score"])["pos_count","neg_count"].sum()
pos.head(10)


# In[ ]:


pos=reviews.groupby(["Average_Score"])["pos_count","neg_count"].sum()
pos.head(10)


# In[ ]:


word_dic = {}
for index, row in reviews.iterrows():
    sent=row['Negative_Review']
    sent = sent.split()
    for word in sent:
        if word in word_dic:
            word_dic[word] += 1 
        else:
            word_dic[word] = 1 

word_dic


# In[ ]:




