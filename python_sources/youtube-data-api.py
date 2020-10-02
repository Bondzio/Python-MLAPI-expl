#!/usr/bin/env python
# coding: utf-8

# # YouTube Data API Tutorial - Python
# 
# This is a documentation-type tutorial on how you can use the recently-released [advertools](https://github.com/eliasdabbas/advertools) version (0.8.0) which contains a full YouTube GET client. This module contains all the methods that import data (GET methods), but not the ones that allow you to upload, update, or delete content, yet. 
# 
# ## Why you might be interested
# 
# 1. **DataFrame, DataFrame, DataFrame:** All functions return a `pandas` DataFrame, even if they contain errors. This makes it convenient becuase you don't need to worry about parsing the different types and shapes of the JSON responses you get from YouTube. Additionally, you get the metadata of the request in the DataFrame. 
# 2. **Request more than the maximum results allowed:** Each function has a limit on the number of results you can request. So if you need more than that, you will have to make multiple requests, and make sure you include the proper tokens for next pages, and handle pagination of requests. You don't need to do any of that. Using this module, you simply provide the number of results you want, and the pagination and concatenation of results is handled for you automatically.
# 3. **Multiple parameters and multiple requests:** To generate a proper dataset for analysis, you typically want to generate the same data for multiple critirea (countries, languages, keywords, topics, etc). Again you don't have to worry about combining those requests, as it is automatically handled. You simply supply a list of entries for each parameter, and the function handles the product of them. For example, if you want to get the most popular videos in three countries and across three languages, you simply supply `regionCode=['us', 'ca', 'mx']` and `relevanceLanguage=['en', 'fr', 'es']`. The function will request the data for all combinations, 3x3 in this case (three languages per country), which means nine requests are handled automatically. This gets really useful if you want to see results for twenty keywords, across fifty countries for example, or even much more. 
# 3. **Very simple functional API:**  
# `import advertools as adv`  
# `key = 'YOUR KEY'`  
# `adv.youtube.<TAB>` which shows you all available functions. Names are typically self-explanatory, and named almost exactly as they are named in the [documentation.](https://developers.google.com/youtube/v3/docs) The relevant documentation for each parameter is also copied so you have access to it in the docstrings.
# 
# ## General conventions
# 
# #### Requests
# - `key`: Every request needs the `key` parameter, which serves as authentication. Check below for the steps to get one. (This is a paid API, and the costs per request are detailed within the docstrings of the functions). For the similar Google Custom Search API, the cost per one thousand queries is five US dollars. The costs for this one are not as straightforward, because you can request parts of a response, but in general, it should be close to the CSE cost average. 
# - `part`: This is another important parameter that needs to be supplied for pretty much all functions. It allows you specify which "part(s)" of a response you want, so you can get exactly the data you want. Typically `snippet` should be provided, which is basically the summary data about a response, that you would normally see in a listing (or search results page). If you want additional parts of the response, you have to mention them. These need to be provided as comma-separated string `no,spaces,included`. Check the `part` parameter's documentation to know what parts you can ask for for each function.
# 
# #### Responses
# - `queryTime`: This is a column that is always included in the responses. As the name suggests, it registers when you made the request. This is very important if you continuously make the same request to track a certain industry, or keyword, so you know how things have changed in time. 
# - `param_something`: Every response DataFrame also includes all the parameters that you supplied in the request. Those columns start with `param_`, and they basically serve as metadata for the response so you can know where this particular result came from. 
# - `kind`: Responses come with a column that show what kind of response it is. It is usually in the form "youtube#nameOfResponse". Some examples: "youtube#subscriptionListResponse", "youtube#activityListResponse", "youtube#channelListResponse", etc. 
# - Errors: If the response returns an error, you will find a few columns for that, and the error messages are included as well for debugging. 
# 
# #### Set up your account:
# 
# 1. Create a project: https://console.cloud.google.com/projectcreate 
# 2. Enable the YouTube API: https://console.cloud.google.com/apis/api/youtube.googleapis.com/ 
# 3. Activate billing: https://console.cloud.google.com/billing 
# 4. Get your key from the credentials page: https://console.cloud.google.com/apis/api/youtube.googleapis.com/credentials 
# 
# Let's start by exploring a few of the available functions. Please note that the code used to generate the data is commented out. I imported the data, and saved the responses to CSV files, to be reproducible, but if you want to generate similar data you just have to remove the comments, and provide your own `key`.

# In[ ]:


get_ipython().system('pip install "advertools>=0.8.1"')


# In[ ]:


import datetime

import advertools as adv
import pandas as pd
import plotly.graph_objects as go
import plotly


key = 'YOUR_GOOGLE_API_KEY'
pd.options.display.max_columns = None

print('package    version')
print('==================')
for package in [adv,pd, plotly]:
    print(f'{package.__name__:<12}', package.__version__)
print('\nLast updated:', format(datetime.datetime.now(), '%b %d, %Y'))


# #### List of available functions

# In[ ]:


list(enumerate([func for func in dir(adv.youtube) if func[0] != '_'], 1))


# `activities_list`: With this function you are basically asking, "Give me the last X activities that account Y (or several accounts) have made. Video uploads, playlist items, and so on. This can be useful to track how active a certain set of accounts are, or maybe compare them to your own.  

# In[ ]:


# activities = adv.youtube.activities_list(key=key, part='snippet', channelId='UCBR8-60-B28hp2BmDPdntcQ') # see below how you can get an account's ID
activities = pd.read_csv('../input/youtube-data-api-datasets/activities.csv', parse_dates=['queryTime'])
print(activities.shape)
activities


# The above dataset show the last five activities that the YouTube account had made. Each activity is represented by a row that contains all its details.

# In[ ]:


activities[['snippet.channelTitle', 'snippet.publishedAt', 'snippet.type', 'snippet.title']]


# In[ ]:


activities.filter(regex='param_')


# The above are the parameters that were used to generate this dataset. `snippet` says that we want the basic listing page data, the `channelId` is YouTube's account's ID on youtube.com, `maxResults` were not provided, so we get five (the defaults), and it appears in the response as `NaN`. The `pageToken` is for pagination, and you generally don't need to worry about it.  
# As mentioned above, each one of the parameters is prepended with `param_` so you can easily know how to get them.  
# So how did we get the account ID of YouTube, since we only knew its username? The following function does that (and more) for us. 
# 
# `channels_list`: This function gets data about channels based on the criteria provided. In this case, I'm asking for the `snippet`, `statistics`, and `contentDetails` for the `forUsername`s 'google', 'youtube', and 'vevo'.

# In[ ]:


# yt_channels = adv.youtube.channels_list(key=key, part='snippet,statistics,contentDetails',
#                                         forUsername=['google', 'youtube', 'vevo'])
yt_channels = pd.read_csv('../input/youtube-data-api-datasets/yt_channels.csv', parse_dates=['queryTime'])
print(yt_channels.shape)
yt_channels


# In[ ]:


yt_channels.filter(regex='snippet\.title|statistics|query|published').set_index(['queryTime', 'snippet.publishedAt', 'snippet.title']).style.format('{:,}')


# As you can see, you can very easily and quickly compare the high-level stats for a bunch of users/channels. It's interesting how many more subscribers YouTube has vs Google for example (29.5M vs 8.58M) even though the number of vidoes uploaded is much lower (308 vs 2,329). 
# 
# `snippet.publishedAt` shows when the item was published (or when the channel was created in this case). This column is available in pretty much all responses that return data abot vidoes, comments, channels, and so on. 

# In[ ]:


yt_channels.filter(regex='content')


# Now that we have the channel IDs for the three accounts that we are interested in, we can use `activities_list` again to get as many activities as we want. Here we only supply a list of the channel ID's, and the `maxResults`, and the request will be made for each of them automatically. In this case, two hundred activities will be requested for each channel.
# 

# In[ ]:


# channels_activities = adv.youtube.activities_list(key=key, part='contentDetails,snippet',
#                                                   channelId=yt_channels['id'].tolist(), maxResults=200) 
channels_activities = pd.read_csv('../input/youtube-data-api-datasets/channels_activities.csv', parse_dates=['snippet.publishedAt'])
print(channels_activities.shape)
channels_activities.head(3)


# Let's see what kind of activity each account has been engaged in recently: 

# In[ ]:


channels_activities.groupby('snippet.channelTitle')['snippet.type'].value_counts().to_frame()


# We can clearly see how different the most recent activities are. Vevo only uploaded two videos, while Google uploaded 148. It doesn't necessarily mean that Vevo hasn't been uploading, becuase they seem to have created 198 playlist items, and that might be the reason why we see only two uploads. We'll keep this in mind.  
# 
# Let's now visualize the upload activities on a monthly and annual basis, and see (keeping in mind the caveat above). We first create a `pub_month` and `pub_year`column to extract the publication month and year for each activity: 

# In[ ]:


channels_activities['pub_month'] = [pd.Period(p, 'M') for p in channels_activities['snippet.publishedAt']]
channels_activities['pub_year'] = [pd.Period(p, 'A') for p in channels_activities['snippet.publishedAt']]
channels_activities.filter(regex='pub').head()


# In[ ]:


channels_activities['snippet.channelTitle'].unique()


# In[ ]:


fig = go.Figure()
for channel in ['YouTube', 'Google', 'Vevo']:
    df = (channels_activities
          [(channels_activities['snippet.channelTitle']==channel) & (channels_activities['snippet.type']=='upload')]
          .groupby(['pub_month', 'snippet.channelTitle'])
          ['snippet.type']
          .value_counts().to_frame()
          .rename(columns={'snippet.type': 'count'})
          .reset_index())
    fig.add_scatter(x=df['pub_month'].astype(str), y=df['count'], name=channel, mode='lines+markers', marker={'size': 10})

fig.layout.template = 'none'
fig.layout.title = 'Video Uploads per Month'
fig


# It seems the Google channel has been very active in the last few months, YouTube has been fairly consistent in the number of videos they upload every month, and for Vevo, the playlist items is obscuring their upload activity. We saw above that they have 19.1M subscribers, as well as 1,568 videos uploaded.

# In[ ]:


fig = go.Figure()
for channel in ['YouTube', 'Google', 'Vevo']:
    df = (channels_activities
          [(channels_activities['snippet.channelTitle']==channel) & (channels_activities['snippet.type']=='upload')]
          .groupby(['pub_year', 'snippet.channelTitle'])
          ['snippet.type']
          .value_counts().to_frame()
          .rename(columns={'snippet.type': 'count'})
          .reset_index())
    fig.add_scatter(x=df['pub_year'].astype(str), y=df['count'], name=channel, marker={'size': 10})

fig.layout.template = 'none'
fig.layout.title = 'Video Uploads per Year'
fig


# Below we get the `value_counts` for each activity type, as well as the minimum and maximum dates of those activities. We also calculate the time difference, and we can see how active each account was and how often they upload content or engage in other activities. You can see that the last two hundred activities occurred in 274, 2016, and 2 days. So we are clearly not comparing apples to apples. 

# In[ ]:


for channel in channels_activities['snippet.channelTitle'].unique():
    channel_df = channels_activities[channels_activities['snippet.channelTitle']==channel]
    val_counts = (channel_df['snippet.type'].value_counts()
                  .rename_axis(channel, axis=0))
    dates = channel_df['snippet.publishedAt']
    print(val_counts)
    print(' min date: ', dates.min().date(), ' | max date: ', dates.max().date(), ' | time delta: ', dates.max() - dates.min(), sep='')
    print('====\n')


# Make sure you experiment with other parameters available for `activities_list`:
# - `publishedBefore`: provide a datetime to restrict activities published before the given date.
# - `publishedAfter`: the same, make sure the date is in the format `YYYY-MM-DDThh:mm:ss.sZ` although you don't need to specify the time, the date alone is enough.
# - `regionCode`: the country for which you want the results, see below for available regions.
# 

# ### Reference information functions: 
# The following functions don't contain very interesting information, and you wouldn't typically use them very often, only when you need reference information.  
# They return the same DataFrame every time, except in the rare case when YouTube adds a new language for example, or decides to change the available categories. It's good to know that these contain the latest updated information on those topics. 
# 
# 
# * [i18n_languages_list](#langs_regions)  
# * [i18n_regions_list](#langs_regions)  
# * [guide_categories_list](#guide_categories)  
# * [video_categories_list](#video_categories)  

# <a id='langs_regions'></a>
# ### Languages and Regions 
# 
# In many functions, you would want to provide the language(s) and/or the region(s) of relevance that you are interested in. To know what is available, you can simply run any of the two following two functions to see what is available, and provide those as parameters to other requests. The important column is the `id` column which is what you need to use. It is NOT case-sensitive so you can use `en` or `EN`. 

# In[ ]:


# languages = adv.youtube.i18n_languages_list(key=key, part='snippet', hl=['en', 'fr', 'de'])
languages = pd.read_csv('../input/youtube-data-api-datasets/languages.csv', parse_dates=['queryTime'])
languages.head()


# In[ ]:


(languages
 .filter(regex='id|name|param_hl')
 .sort_values('id')[:12]
 .reset_index(drop=True))


# In[ ]:


# regions = adv.youtube.i18n_regions_list(key=key, part='snippet', hl=['en', 'ar', 'ja'])
regions = pd.read_csv('../input/youtube-data-api-datasets/regions.csv', parse_dates=['queryTime'])
regions.head()


# In[ ]:


(regions
 .filter(regex='id|name|param_hl')
 .sort_values('id')[:12]
 .reset_index(drop=True))


# <a id='guide_categories'></a>
# `guide_categories_list`: Another reference function that gets you the possible categories that a YouTube channel can have.

# In[ ]:


# channel_categories = adv.youtube.guide_categories_list(key=key, part='snippet', regionCode='us')
channel_categories = pd.read_csv('../input/youtube-data-api-datasets/channel_categories.csv', parse_dates=['queryTime'])
channel_categories.head(3)


# In[ ]:


channel_categories['snippet.title'].to_frame()


# `video_categories_list`: Similarly, you have another one for available video categories.

# In[ ]:


# video_categories = adv.youtube.video_categories_list(key=key, part='snippet', regionCode='us', hl=['en', 'es', 'zh-CN'])
video_categories = pd.read_csv('../input/youtube-data-api-datasets/video_categories.csv', parse_dates=['queryTime'])
video_categories.head(3)


# In[ ]:


(video_categories
 .iloc[pd.Series([(x,x+32,x+64) for x in range(32)]).explode()]
 [['id', 'snippet.title', 'param_hl']]
 [:15])


# Video categories are interesting when you search or list videos, and want to get results that are only part of a certain category of content. Maybe you are interested in videos about Barcelona, but only sports videos and not tourism for example. 

# ### Comment threads
# Now we dig into the comments threads and replies by using `comment_threads_list` and `comments_list`.  
# Here are the latest 150 comment threads for [Despacito](https://www.youtube.com/watch?v=kJQP7kiw5Fk).  
# Note that top-level comments are referred to as threads, and the replies to them are referred to as comments. So this function retrieves the comments that you would see first (not their replies).

# In[ ]:


# comment_thrd_vid = adv.youtube.comment_threads_list(key=key, part='snippet', videoId='kJQP7kiw5Fk',
#                                                     maxResults=150,)
comment_thrd_vid = pd.read_csv('../input/youtube-data-api-datasets/comment_thrd_vid.csv', 
                               parse_dates=['queryTime', 'snippet.topLevelComment.snippet.publishedAt',
                                            'snippet.topLevelComment.snippet.updatedAt'])
comment_thrd_vid.head(3)


# In[ ]:


comment_thrd_vid['snippet.topLevelComment.snippet.publishedAt'].max() - comment_thrd_vid['snippet.topLevelComment.snippet.publishedAt'].min()


# As expected, such a popular video would get a massive amount of comments in a very short period of time; 150 comments in less than five hours.

# In[ ]:


comment_thrd_vid.filter(regex='authorDisplay|textOriginal|likeCount|publishedAt')


# Below we can see who the top commenters are, in terms of the number of comments they submitted, as well as the total likes they got for their comments. Obviously, this is not a representative sample, a tiny number of comments in a very short period of time do not reflect the general response to the video. 

# In[ ]:


(comment_thrd_vid
 .groupby('snippet.topLevelComment.snippet.authorDisplayName')
 .agg({'snippet.topLevelComment.snippet.likeCount': ['sum', 'count']})
 .sort_values(('snippet.topLevelComment.snippet.likeCount','sum'), ascending=False))


# Other interesting parameters to explore: 
# 
# - `allThreadsRelatedToChannelId`: As the name suggests, this gets you all the comments for a certain channel, comments on the channel itself as well as on videos. 
# - `channelId`: Or get comments for a certain channel (not includig comments on the channel's videos)
# - `order`: How to order the comment threads, `time` and `relevance` are available options. 
# - `searchTerms`: This is potentially the most usefull, especially if you are looking at very popular videos with many comments. You might be interested only in comments that include certain keywords, and get those only. 
# 
# and there's more! 
# 
# In order to get the replies to specific comment threads you would use the `comments_list` function, and supply the comment thread ID's that you got previously, for example:

# In[ ]:


comment_thrd_vid['id'][:10]


# To put the above numbers in perspective, we can quickly get the data for this video with `videos_list`, and get a one-row DataFrame for this video. 

# In[ ]:


# despacito = adv.youtube.videos_list(key=key, part='contentDetails,snippet,statistics', id='kJQP7kiw5Fk')

despacito = pd.read_csv('../input/youtube-data-api-datasets/despacito.csv', parse_dates=['queryTime', 'snippet.publishedAt'])
print(despacito.shape)
despacito


# In[ ]:


(despacito
 .filter(regex='statistics|queryTime')
 .set_index('queryTime')
 .style.format('{:,}'))


# In[ ]:


today = despacito['queryTime'][0]
print('Request date:', format(today, '%b %d, %Y'))
print("Despacito was published " + str((today - despacito['snippet.publishedAt'][0]).days) + " days before this request")


# `playlists_list`
# 
# As the name suggests, this function list the playlists that you request, based on whatever parameters you supply.  
# Getting the `channelId` of Vevo from above, we can request 200 of their playlists (since it seems their activity list contained a lot of playlists).

# In[ ]:


# vevo_playlists = adv.youtube.playlists_list(key=key, part='snippet,contentDetails', maxResults=200,
#                                             channelId='UC2pmfLm7iq6Ov1UwYrWYkZA')
vevo_playlists = pd.read_csv('../input/youtube-data-api-datasets/vevo_playlists.csv', parse_dates=['snippet.publishedAt', 'queryTime'])
print(vevo_playlists.shape)
vevo_playlists.head(2)


# In[ ]:


vevo_playlists['snippet.publishedAt'].max() - vevo_playlists['snippet.publishedAt'].min()


# Two hundred playlists in seventy four days. You can dig a little deeper to see whether they created them, updated them, if they are their own videos, and so on. 

# In[ ]:


vevo_playlists.filter(regex='published|snippet\.title|description|itemCount|id$').head()


# Above is a subset of the dataset, and using the `id` column you can retrieve all data related to that particular playlist (or all of them). 
# Let's quickly explore how many videos there are on average in their playlists.

# In[ ]:


vevo_playlists['contentDetails.itemCount'].value_counts().to_frame().head()


# In[ ]:


fig = go.Figure()
fig.add_bar(x=vevo_playlists['contentDetails.itemCount'].value_counts().index,
            y=vevo_playlists['contentDetails.itemCount'].value_counts().values)

fig.layout.template = 'none'
fig.layout.xaxis.title = 'Number of videos per playlist'
fig.layout.yaxis.title = 'Count of playlists'
fig


# Nothing really surprising here, with the exception of the longest playlist, containing 228 videos. 

# In[ ]:


(vevo_playlists
 .sort_values('contentDetails.itemCount', ascending=False)
 [['snippet.title', 'contentDetails.itemCount', 'id']])


# We can now get the data related to that playlist, and see what it contains. Again, we can do the same with the videos of that playlist, get all their data, by using the video IDs provided if we want.

# In[ ]:


# vevo_playlist_items = adv.youtube.playlist_items_list(key=key, part='snippet', maxResults=300,
#                                                       playlistId='PL9tY0BWXOZFsVNsIUCPoITIuZlzM3Y4bq')

vevo_playlist_items = pd.read_csv('../input/youtube-data-api-datasets/vevo_playlist_items.csv', parse_dates=['snippet.publishedAt', 'queryTime'])
print(vevo_playlist_items.shape)
vevo_playlist_items.head(2)


# In[ ]:


vevo_playlist_items.filter(regex='published|snippet\.(title|description)|videoId')


# `subscriptions_list`
# 
# This function lists the subscriptions based on the criteria specified in the function parameters. In this example, I'm requesting the subscriptions of the Vevo channel (250 of them).

# In[ ]:


# vevo_subscriptions = adv.youtube.subscriptions_list(key=key, part='snippet,subscriberSnippet,contentDetails', 
#                                                     channelId='UC2pmfLm7iq6Ov1UwYrWYkZA', maxResults=250)

vevo_subscriptions = pd.read_csv('../input/youtube-data-api-datasets/vevo_subscriptions.csv', parse_dates=['snippet.publishedAt', 'queryTime'])
print(vevo_subscriptions.shape)
vevo_subscriptions.head(2)


# In[ ]:


vevo_subscriptions.filter(regex='published|title|description|Count')


# ## videos_list
# 
# This function is interesting because it allows you to get full details about videos, in two possible ways: 
# 
# 1. **Directly:** By using this function you can specify any of its parameters and get the data that you want, as you would with any other regular function
# 2. **As a second step to another function:** Many functions return only a snippet of the query you request, and in the snippet you would have video ID's. You can use those to get more details for those videos using `videos_list`. 
# 
# Below are some interesting parameters that might be useful:
# 
# * `part`: Here you specify how much detail you want about the videos, and you have the following options: `contentDetails`, `fileDetails`, `id`, `liveStreamingDetails`, `localizations`, `player`, `processingDetails`, `recordingDetails`
#     `snippet`, `statistics`, `status`, `suggestions`, `topicDetails`. Remember to provide those as a comma-separated string "without,using,any,spaces".
# * `id`: The video ID(s) for which you want more details. Also provided as a comma-separated string.
# * `chart`: In case you want the most popular videos, specify `chart="mostPopular"`.
# * `hl`: Human language. Available through the `i18n_languages_list` function.
# * `regionCode`: The country for which you want videos. Available through the `i18n_regions_list` function.
# 
# As you can see, there are many possible combinations of the options that you can provide and get different results and types of results.  
# The below example requests the top ten videos for all coutries available in the API, along with several ideas on how to visualize and analyze the response.  
# Note that creating the dataset is done with one line of code. 

# In[ ]:


# top10_world_vid = adv.youtube.videos_list(key=key,
#                                           part='snippet,statistics,contentDetails,topicDetails',
#                                           chart='mostPopular', 
#                                           regionCode=regions['id'].tolist(),
#                                           maxResults=10)
top10_world_vid = pd.read_csv('../input/youtube-data-api-datasets/top10_world_vid.csv', 
                              parse_dates=['snippet.publishedAt', 'queryTime'])
print(top10_world_vid.shape)
top10_world_vid.head(2)


# Every parameter that we specified, shows as the first part of the column name, followed by a dot, and then further details.  
# `statistics.viewCount`, `statistics.commentCount` and so on.  
# Video categories come encoded as numbers, and the below dictionary uses the categories dataset to map the numbers to their names so we can more easily read them.

# In[ ]:


category_dict = dict(video_categories.query('param_hl == "en"')[['id', 'snippet.title']].values)
top10_world_vid['category'] = [None if pd.isna(x) else category_dict[x] for x in top10_world_vid['snippet.categoryId']]
top10_world_vid[['snippet.categoryId', 'category']].head()


# One important and tricky aspect of YouTube's data is the fact that video views are reported for their total views globally. In this dataset, where we have countries along with videos (and their respective views and other stats), you might think that a certain video generated that many views in a certain country. The reality is that YouTube is simply saying that a certain video was trending in a certain country, and that its total global views were a certain number.  
# Below you can see that the top video, its views, and the countries where it was trending, all show the same number. This proves that the numbers are for the video globally, and not for each country. We will keep this in mind throughout the analysis, and remove duplicated rows where applicable. 

# In[ ]:


(top10_world_vid
 .sort_values(['statistics.viewCount', 'snippet.title', 'param_regionCode'], 
              ascending=False)
 [['snippet.title', 'statistics.viewCount', 'param_regionCode']]
 .head(15))


# The top videos seem to be trending in many countries at the same time:

# In[ ]:


top10_world_vid['snippet.title'].value_counts().to_frame()[:10]


# Another important thing to check is whether there were errors or missing values: 

# In[ ]:


'errors' in top10_world_vid # a column named "errors" would be in the dataset if we had any


# In[ ]:


top10_world_vid['snippet.title'].isna().sum()


# In[ ]:


top10_world_vid[top10_world_vid['snippet.title'].isna()]


# After checking, you can sett that there are missing values for Egypt, Lybia, and Yemen, and that each has only one row (as opposed to ten for all other countries).

# In[ ]:


top10_world_vid[top10_world_vid['snippet.title'].isna()]['param_regionCode']


# To check the trending videos for any country, you filter the `param_regionCode` column, and sort by `statistics.viewCount`

# In[ ]:


(top10_world_vid
 .query('param_regionCode=="BR"')
 .dropna(subset=['statistics.viewCount'])
 .sort_values('statistics.viewCount', ascending=False)
 [['snippet.title', 'statistics.viewCount']]
 .style.format({'statistics.viewCount': '{:,}'}))


# In[ ]:


(top10_world_vid
 .query('param_regionCode=="FR"')
 .dropna(subset=['statistics.viewCount'])
 .sort_values('statistics.viewCount', ascending=False)
 [['snippet.title', 'statistics.viewCount']]
 .style.format({'statistics.viewCount': '{:,}'}))


# You might also be interested in the top two or three for each country, in which case you run a groupby and then head(n) to get this subset.

# In[ ]:


(top10_world_vid
 .dropna(subset=['statistics.viewCount'])
 .sort_values(['param_regionCode', 'statistics.viewCount'],
              ascending=[True, False])
 .groupby('param_regionCode', as_index=False)
 .head(3)
 [['param_regionCode', 'snippet.title',  'statistics.viewCount']][:15]
 .style.format({'statistics.viewCount': '{:,}'}))


# Now let's see which categoeries of videos were the most popular. Note that it is very important to remove duplicates here (to avoid multiple counts of the same video), and we also need to remove NA values, so we don't get issues while sorting and summing. 

# In[ ]:


category_sum_count = (top10_world_vid
                      .drop_duplicates(subset=['snippet.title'])
                      .dropna(subset=['statistics.viewCount'])
                      .groupby('category')
                      .agg({'statistics.viewCount': ['count', 'sum']})
                      ['statistics.viewCount']
                      .sort_values('sum', ascending=False))
category_sum_count.style.format({'sum': '{:,}'})


# Here we visualize the same table as a treemap. Click on a category to zoom in and out for a better reading of the data. 

# In[ ]:


fig = go.Figure()
labels = (category_sum_count.index.astype(str) + ' (' + category_sum_count['count'].astype(str) + ' videos)').values
fig.add_treemap(labels=labels, 
                parents=['All Categories' for i in range(len(category_sum_count))], 
                values=category_sum_count['sum'],
                texttemplate='<b>%{label}</b><br><br>Total views: %{value}<br>%{percentParent} of total')
fig.layout.template = 'none'
fig.layout.height = 600
fig.layout.title = 'Total views by cateogry of video'
fig


# ### Video age and total views 
# Are the trending videos all new, old, or they don't have to be recently published to be trending? Is there any relationship? 

# In[ ]:


(top10_world_vid
 .drop_duplicates(subset=['id'])
 .dropna(subset=['id'])
 .assign(video_age_days=lambda df: df['queryTime'].sub(df['snippet.publishedAt']).dt.days)
 .groupby('video_age_days', as_index=False)
 ['statistics.viewCount'].sum()
 .sort_values('statistics.viewCount', ascending=False)
 .reset_index(drop=True)
 .head(10)
 .assign(perc=lambda df: df['statistics.viewCount'].div(df['statistics.viewCount'].sum()).round(2))
 .assign(cum_perc=lambda df: df['perc'].cumsum())
 .style.format({'statistics.viewCount': '{:,}', 'perc': '{:.1%}', 'cum_perc': '{:.1%}'}))


# In[ ]:


top10_world_vid['video_age_days'] = top10_world_vid['queryTime'].sub(top10_world_vid['snippet.publishedAt']).dt.days
df = top10_world_vid.dropna(subset=['snippet.title']).drop_duplicates('snippet.title')
fig = go.Figure()
fig.add_histogram(x=df['video_age_days'], nbinsx=22)
fig.layout.bargap = 0.1
fig.layout.template = 'none'
fig.layout.title = 'Video age in days'
fig.layout.xaxis.title = 'Age in days'
fig.layout.yaxis.title = 'Number of videos'
fig


# **Tags**  
# Another more detailed categorization of the videos is by tags. This is much more flexible than categories, and you can add a large number of tags to your videos, to make it easier for categorization. 

# In[ ]:


tags_stats_cats = (top10_world_vid
                   .drop_duplicates(subset=['snippet.title'])
                   .dropna(subset=['statistics.viewCount'])
                   [['snippet.tags', 'statistics.viewCount', 'category']]
                   .reset_index(drop=True))
tags_stats_cats.head()


# When coming from the YouTube API directly the column `snippet.tags` would contain a list in each row.  
# Because this dataset was saved in a file, and read from disk, those lists were read as strings, so we need to convert them to lists with the following line: 

# In[ ]:


tags_stats_cats['snippet.tags'] = [None if pd.isna(x) else eval(x) for x in tags_stats_cats['snippet.tags']]


# Now we can have a count for each tag, and sum the views of all videos that contained the tag.

# In[ ]:


from collections import defaultdict
dd = defaultdict(lambda: ['', 0])


for i, tag_list in enumerate(tags_stats_cats['snippet.tags']):
    if isinstance(tag_list, list):
        for tag in tag_list:
                dd[tag][0] = tags_stats_cats['category'][i]
                dd[tag][1] += tags_stats_cats['statistics.viewCount'][i]
    else:
        if pd.isna(tag_list):
            dd[None][0] = tags_stats_cats['category'][i]
            dd[None][1] += tags_stats_cats['statistics.viewCount'][i]      

by_tag_category = (pd.DataFrame(list(zip(dd.keys(), dd.values()))).assign(category=lambda df: df[1].str[0],
                                                       view_count=lambda df: df[1].str[1]).drop(columns=[1])
                  .sort_values('view_count', ascending=False)
                  .rename(columns={0: 'tag'})
                  .reset_index(drop=True))
               
by_tag_category.head(10).style.format({'view_count': '{:,}'})


# Let's now take a look at the top fifty videos, which categories they belong to, and how much of the total views they contribute to. 

# In[ ]:


top_fifty_vids = (top10_world_vid
                  .drop_duplicates(subset=['id'])
                  .dropna(subset=['statistics.viewCount'])
                  .sort_values('statistics.viewCount', ascending=False)
                  .head(50))
top_fifty_vids.head(3)


# In[ ]:


perc_of_views = top_fifty_vids['statistics.viewCount'].sum() / top10_world_vid.drop_duplicates(subset=['id'])['statistics.viewCount'].sum()
num_of_videos = top10_world_vid['id'].nunique()
print(format(perc_of_views, '.2%'), 'of total views were generated by fifty out of', num_of_videos, 'videos (' + format(50/580, '.1%'), 'of the videos).')


# In[ ]:


import plotly.express as px
fig =  px.treemap(top_fifty_vids.assign(All='All categories'), path=['All', 'category', 'snippet.title'], values='statistics.viewCount')
fig.data[0]['texttemplate'] = '<b>%{label}</b><br><br>Total views: %{value}<br>%{percentParent} of %{parent}'
fig.data[0]['hovertemplate'] = '<b>%{label}</b><br><br>Total views: %{value}<br>%{percentParent:.2%} of %{parent}'
fig.layout.height = 650
fig.layout.title = 'Top 50 trending videos on YouTube by category (65% of total views) - Feb 7, 2020<br>(click on videos and categories to zoom in and out)'
fig.layout.template = 'none'
fig


# There are many more functions and options available as mentioned above, and I will be updating this tutorial with more examples and ideas.  
# Questions and suggestions more than welcome here or on the [package repo page.](https://github.com/eliasdabbas/advertools)
