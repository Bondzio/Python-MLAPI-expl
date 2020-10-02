#!/usr/bin/env python
# coding: utf-8

# # Exploring Trending Youtube Video Statistics for the U.S.
# 
# Growing up watching YouTube shaped a lot of my interests and humor. I still remember the early days when nigahiga's How To Be Gangster and ALL YOUR BASE ARE BELONG TO US was peak comedy. So I thought it would be fun to see the state of YouTube and what's popular now.

# ## Loading Libraries

# In[ ]:


import numpy as np
import pandas as pd
from pandas import DataFrame

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator 

import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sb

get_ipython().run_line_magic('matplotlib', 'inline')
rcParams['figure.figsize'] = 8, 6
sb.set()


# ## Reading and Cleaning Data

# In[ ]:


# Read in dataset

vids = pd.read_csv('../input/youtube-new/USvideos.csv')

# Add category names
vids['category'] = np.nan

vids.loc[(vids["category_id"] == 1),"category"] = 'Film & Animation'
vids.loc[(vids["category_id"] == 2),"category"] = 'Autos & Vehicles'
vids.loc[(vids["category_id"] == 10),"category"] = 'Music'
vids.loc[(vids["category_id"] == 15),"category"] = 'Pets & Animals'
vids.loc[(vids["category_id"] == 17),"category"] = 'Sports'
vids.loc[(vids["category_id"] == 19),"category"] = 'Travel & Events'
vids.loc[(vids["category_id"] == 20),"category"] = 'Gaming'
vids.loc[(vids["category_id"] == 22),"category"] = 'People & Blogs'
vids.loc[(vids["category_id"] == 23),"category"] = 'Comedy'
vids.loc[(vids["category_id"] == 24),"category"] = 'Entertainment'
vids.loc[(vids["category_id"] == 25),"category"] = 'News & Politics'
vids.loc[(vids["category_id"] == 26),"category"] = 'How-To & Style'
vids.loc[(vids["category_id"] == 27),"category"] = 'Education'
vids.loc[(vids["category_id"] == 28),"category"] = 'Science & Technology'
vids.loc[(vids["category_id"] == 29),"category"] = 'Nonprofits & Activism'

# Add like, dislike, commment ratios
vids['like_pct'] = vids['likes'] / (vids['dislikes'] + vids['likes']) * 100
vids['dislike_pct'] = vids['dislikes'] / (vids['dislikes'] + vids['likes']) * 100
vids['comment_pct'] = vids['comment_count'] / vids['views'] * 100

# Order by Views
vids.sort_values('views', ascending = False, inplace = True)

# Remove Duplicate Videos
vids.drop_duplicates(subset = 'video_id', keep = 'first', inplace = True)


# In[ ]:


vids.head()


# After removing videos with the same id, we see there are now only 6,351 videos to analyze. These 6,351 videos should reflect the row with the highest view count for the video.
# 
# I also created the variables like_pct, dislike_pct, and comment_pct. Like_pct and dislike_pct are calculated as the ratio of likes/dislikes relating to the total number of likes/dislikes on the video. Comment_pct is the the % of comments left on the video relative to the total number of views. I thought that these ratios were more intuitive, rather than having every one relating to the total number of views.

# ## Summary Statistics and Top Trending

# In[ ]:


pd.options.display.float_format = "{:,.0f}".format
vids.describe().iloc[:,1:5]


# The average number of views for a trending video was ~2M, with a standard deviation of ~7M. Interestingly, the minimum number of views was 559 and the maximum was ~225M. This is a pretty broad range. Makes you wonder how YouTube selects which videos are trending. It doesn't really make sense to me that there is a video with 0 likes, dislikes, and comments that is trending.
# 
# I'd like now to see the Top 10 Videos by Views, Likes, Dislikes, and Comments.

# ### Top 10 Videos
# #### Top 10 Videos By Views

# In[ ]:


pd.options.display.float_format = "{:,.2f}".format

top10_vids = vids.nlargest(10, 'views')
display(top10_vids.iloc[:, [2,3,7,16]])


# #### Top 10 Videos By Likes

# In[ ]:


top10_vids = vids.nlargest(10, 'likes')
top10_vids.iloc[:, [2,3,7,8,17,16]]


# #### Top 10 Videos By Dislikes

# In[ ]:


top10_vids = vids.nlargest(10, 'dislikes')
top10_vids.iloc[:, [2,3,7,9,18,16]]


# #### Top 10 Videos By Comments

# In[ ]:


top10_vids = vids.nlargest(10, 'comment_count')
top10_vids.iloc[:, [2,3,7,10,19,16]]


# ### Correlation Heatmap

# In[ ]:


corr = vids[['views', 'likes', 'dislikes', 'comment_count', 'like_pct', 'dislike_pct', 'comment_pct']].corr()
sb.heatmap(corr, annot = True, fmt = '.2f', center = 1)
plt.show()


# Reading this heatmap, we note that views has a high correlation with likes -- not so much dislikes. Comment_count and likes/dislikes have strong correlation as well, but comment_count does not have a particularly strong correlation with views.

# ### Bottom 10 Videos by Views
# 
# I'm curious what the trending videos with low views actually are. Seeing below, it appears that they are pretty randomly assorted. Not sure why they are on the trending list, and YouTube is decidedly not transparent with its algorithm. Perhaps they are getting a high ratio of shares?

# In[ ]:


bot10_vids = vids.nsmallest(10, 'views')
bot10_vids.iloc[:, [2,3,7,8,9,10,16]]


# ### Top 10 Channels
# 
# Let's take a look at the top 10 channels that appear the most frequently on the trending videos list. They're comprised of late night shows and channels otherwise run by companies, not individual YouTubers.

# In[ ]:


top10_chan = vids['channel_title'].value_counts()
top10_chan = top10_chan[1:10].to_frame()
top10_chan.columns = ['number of videos']

top10_chan


# ## Category Analysis

# In[ ]:


categories = vids['category'].value_counts().to_frame()
categories['index'] = categories.index
categories.columns = ['count', 'category']
categories.sort_values('count', ascending = True, inplace = True)

plt.barh(categories['category'], categories['count'], color='#007ACC')
plt.xlabel('Count')
plt.title('Number of Trending Videos Per Category')
plt.show()


# ### Averages Per Category

# In[ ]:


vids_cat = vids[['category','views', 'likes', 'dislikes', 'comment_count', 'like_pct', 'dislike_pct', 'comment_pct']]
vids_cat_groups = vids_cat.groupby(vids_cat['category'])
vids_cat_groups = vids_cat_groups.mean()
vids_cat_groups['category'] = categories.index

vids_cat_groups.sort_values('views', ascending = True, inplace = True)
plt.barh(vids_cat_groups['category'], vids_cat_groups['views'], color='#007ACC')
plt.xlabel('Average # Views')
plt.title('Average Number of Views Per Video By Category')
plt.show()


# In[ ]:


vids_cat_groups.sort_values('comment_count', ascending = True, inplace = True)
plt.barh(vids_cat_groups['category'], vids_cat_groups['comment_count'], color='#007ACC')
plt.xlabel('Average # Comments')
plt.title('Average Number of Comments Per Video By Category')
plt.show()


# In[ ]:


vids_cat_groups.sort_values('likes', ascending = True, inplace = True)
plt.barh(vids_cat_groups['category'], vids_cat_groups['likes'], color='#007ACC')
plt.xlabel('Average # Likes')
plt.title('Average Number of Likes Per Video By Category')
plt.show()


# In[ ]:


vids_cat_groups.sort_values('dislikes', ascending = True, inplace = True)
plt.barh(vids_cat_groups['category'], vids_cat_groups['dislikes'], color='#007ACC')
plt.xlabel('Average # Dislikes')
plt.title('Average Number of Dislikes Per Video By Category')
plt.show()


# When it comes to averages, People & Blogs and Science & Technology contend for the highest enagement levels, swapping for spot 1 and 2 for highest average number of likes, dislikes, and comments.

# ### Distributions Per Category

# In[ ]:


plt.figure(figsize = (16, 10))

sb.boxplot(x = 'category', y = 'like_pct', data = vids, palette = 'Pastel1')
plt.xticks(rotation=45)
plt.xlabel('')
plt.ylabel('% Likes', fontsize = 14)
plt.title('Boxplot of % Likes on a Video By Category', fontsize = 16)
plt.show()


# In[ ]:


plt.figure(figsize = (16, 10))

sb.boxplot(x = 'category', y = 'dislike_pct', data = vids, palette = 'Pastel1')
plt.xticks(rotation=45)
plt.xlabel('')
plt.ylabel('% Likes', fontsize = 14)
plt.title('Boxplot of % Dislikes on a Video By Category', fontsize = 16)
plt.show()


# In[ ]:


plt.figure(figsize = (16, 10))

sb.boxplot(x = 'category', y = 'comment_pct', data = vids, palette = 'Pastel1')
plt.xticks(rotation=45)
plt.xlabel('')
plt.ylabel('% Comments', fontsize = 14)
plt.title('Boxplot of % Comments on a Video By Category', fontsize = 16)
plt.show()


# Unsurprisingly, News & Politics is the most controversial category, with a higher median and larger spread of dislikes/likes. Along with Gaming, it is also more frequently commented on.

# ## Title Wordcloud

# In[ ]:


text = " ".join(title for title in vids.title)
# print("{} words total".format(len(text)))

plt.figure(figsize = (10, 12))
title_cloud = WordCloud(background_color = "white").generate(text)
plt.imshow(title_cloud, interpolation = 'bilinear')
plt.axis('off')
plt.show()


# Movie trailers and music videos seem particularly popular.

# ## Tags Wordcloud

# In[ ]:


text = " ".join(tags for tags in vids.tags)
# print("{} words total".format(len(text)))

plt.figure(figsize = (10, 12))
tag_cloud = WordCloud(background_color = "white").generate(text)
plt.imshow(tag_cloud, interpolation = 'bilinear')
plt.axis('off')
plt.show()


# Funny videos, talk shows, movies, and Star Wars in particular are notable tags.

# ## Time Trends

# In[ ]:


from datetime import datetime

# Reformat publish_time
vids['publish_time'] = vids['publish_time'].str[:10]

# Reformat trending_date
year = vids['trending_date'].str[:2]
month = vids['trending_date'].str[-2:]
date = vids['trending_date'].str[:-3].str[3:]
vids['trending_date'] = '20' + year + '-' + month + '-' + date

vids['publish_time'] = pd.to_datetime(vids['publish_time'])
vids['trending_date'] = pd.to_datetime(vids['trending_date'])
vids['publish_trend_lag'] = vids['trending_date'] - vids['publish_time']


# In[ ]:


timehist = plt.hist(vids['publish_trend_lag'].dt.days, bins = 30, range = (0, 30))
plt.xlabel('Days')
plt.title('Number of Days Between Video Publishing Date and Trending Date')
plt.xticks(np.arange(0, 30, 3))
plt.show()


# Videos tend to trend within a week of publication, and never on the day-of. As time passes past the publication date, we see it is increasingly rare for a video to start trending.

# #### Thank you!
# 
# Hope this was an enjoyable read.
