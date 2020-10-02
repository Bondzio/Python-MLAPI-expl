#!/usr/bin/env python
# coding: utf-8

# # Trending Youtube Video Statistics: EDA with Plotly
# 
# Kernel by Luc Tremsal

# ![Youtube](http://i.ytimg.com/vi/GZmGmkOJ9ME/maxresdefault.jpg)

# # Table of contents
# - <a href='#1'>1 Introduction</a>  
# - <a href='#2'>2 Getting ready</a> 
#     - <a href='#2.1'>2.1 Module import</a> 
#     - <a href='#2.2'>2.2 Data import</a>
#     - <a href='#2.3'>2.3 (Optional) JupyterLab extensions</a>
# - <a href='#3'>3. Overview</a>
#     - <a href='#3.1'>3.1 Head and merge tables</a>
#     - <a href='#3.2'>3.2 Missing data</a>
# - <a href='#4'>4 Distributions, data wrangling and new features</a>
#     - <a href='#4.1'>4.1 category</a>
#     - <a href='#4.2'>4.2 trending time</a>
#     - <a href='#4.3'>4.3 views, likes, dislikes and comments (interactions)</a>
#     - <a href='#4.4'>4.4 comments_disabled & ratings_disabled</a>
#     - <a href='#4.5'>4.5 description</a>
#     - <a href='#4.6'>4.6 tags</a>
#     - <a href='#4.7'>4.7 title</a>
#     - <a href='#4.8'>4.8 channel_title</a>
# - <a href='#5'>5 Correlations</a>
# - <a href='#6'>6 Predicting trending time with Machine Learning</a>

# # <a id='1'>1. Introduction

# Hi there, my name's Luc, I'm a French 23 years old Data Science student about to graduate from my engineering school. This is my first kernel and I hope you'll like it. It is mainly focus on **data exploration** using graphic library Plotly and **predictive modeling**. For this study, I chose a recent dataset: Trending Youtube Videos Statistics. 

# # <a id='2'>2. Getting ready

# ## <a id='2.1'>2.1. Modules import

# In[ ]:


# Essentials
import numpy as np
import pandas as pd

# Visualisation
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

# Others
from wordcloud import WordCloud


# ## <a id='2.2'>2.2. Data import

# In[ ]:


# Let's start with the trending French videos
fr_videos_raw = pd.read_csv('../input/youtube-new/FRvideos.csv', sep=',')


# ## <a id='2.3'>2.3. (Optional) JupyterLab extensions

# If, like me, you like working on JupyterLab and want it to render Plotly figures, you'll find a few mandatory steps [here](https://github.com/plotly/plotly.py#jupyterlab-support-python-35). Otherwise, Jupyter notebook supports Plotly well.

# # <a id='3'>3. Overview

# ### <a id='3.1'>3.1. Head and merge tables

# In[ ]:


fr_videos_raw.head()


# Also, we're given this json file:

# In[ ]:


fr_category_id = pd.read_json('../input/youtube-new/FR_category_id.json')


# In[ ]:


fr_category_id.head()


# In[ ]:


fr_category_id['items'].iloc[0]


# ![](http://)Let's get video category and id to merge with main dataframe.

# In[ ]:


# We retreive category_id and category_title in two lists (with same order) contained in a dict
fr_category_id_dict = {'category_id':[key for key in fr_category_id['items'].keys()],
                       'category_title':[y['snippet']['title'] for x,y in fr_category_id['items'].items()]}
fr_category_id_dict.keys(), fr_category_id_dict.values()


# Then join on our main table.

# In[ ]:


# Create dataframe from dict
fr_category_id_df = pd.DataFrame.from_dict(fr_category_id_dict)

# Merge on category_id then drop it
fr_videos = fr_videos_raw.merge(fr_category_id_df, how='inner', on='category_id').drop(columns='category_id')
fr_videos.loc[:5, ['title', 'category_title']]


# ### <a id='3.2'>3.2. Missing data

# Since this data were directly retreived from Youtube with an API, we assume it's quite clean.

# In[ ]:


# Dataset dimensions
fr_videos.shape


# In[ ]:


# Missing values by column
fr_videos.isna().sum()


# Indeed, few videos have no description. But we're not here for NLP, this shouldn't be an issue.

# # <a id='4'>4. Distributions, data wrangling and new features

# We'll start by exploring each column using brand new version [Plotly 4.0](https://community.plot.ly/t/introducing-plotly-py-4-0-0/25639), hoping to discover some interesting aspects of the data that may lead us to a relevant prediction problem.  
# Also, I just heard about [plotly express](https://plot.ly/python/plotly-express) which allows us to create plotly graphs quite easily. Plotly team describes it this way: "*plotly.express is to plotly what seaborn is to matplotlib*". Let's try it already !

# ## <a id='4.1'>4.1 category_title --> category

# In[ ]:


# Renaming columns for cleaner code
fr_videos = fr_videos.rename(columns={'category_title':'category'})
px.histogram(fr_videos, x='category', title='Number of videos per category').update_xaxes(categoryorder='total descending')


# ## <a id='4.2'>4.2 trending_date & publish_time --> trending_time

# In[ ]:


# Trending_date  & publish_time
fr_videos.loc[:5, ['video_id', 'trending_date', 'publish_time']]


# There's some work to do with these two datetime-like columns: formats are different and we aim to compute the time a video took to be considered trending.

# In[ ]:


# Converting series to datetime series
fr_videos['trending_date'] = pd.to_datetime(fr_videos['trending_date'], format='%y.%d.%m')
fr_videos['publish_time'] = pd.to_datetime(fr_videos['publish_time'], format='%Y-%m-%d')

# Adding a time to trending_date in order to compare with publish_time
# Input last minute of day in order to avoid negative differences
fr_videos['trending_date'] = pd.to_datetime(fr_videos['trending_date'].astype(str) + ' ' + pd.Series(['23:59:59+00:00']*fr_videos.shape[0]),
                                            format='%Y-%m-%d %H:%M:%S')

# Create new feature trending_time in seconds
fr_videos['trending_time'] = pd.to_timedelta(fr_videos['trending_date'] - fr_videos['publish_time']).apply(lambda x: int(x.total_seconds()))

# Assert there's no negative time
try:
    if (fr_videos['trending_time'] < 0).any():
        raise ValueError
except ValueError:
    print("Negative timedelta found ! You should have a look.")


# Let's first have a look at trending_time distribution:

# In[ ]:


# I first used px.histogram but the data was so spread again it didn't help
# Even a boxplot is stretched too much to have a good overview
# We plot in hours
(fr_videos['trending_time']//3600).describe()


# In[ ]:


# More precision
for quantile, trd_time in fr_videos['trending_time'].quantile([0.80, 0.85, 0.90, 0.95, 0.97, 0.99]).iteritems():
    print("{}% of videos become trending in less than {} hours".format(int(quantile*100), int(trd_time//(3600))))


# ## <a id='4.3'> 4.3 Views, likes, dislikes and comments (interactions)</a>

# When it comes to a video, you can:
# - **watch it**: this will count as a view
# - **interact with it**: like, dislike and/or comment it. These three interactions tell long about how trending a video is and how divergent the opinions can be.
# 
# Also we'll compare with trending_time we computed.

# In[ ]:


# Renaming columns for cleaner code
fr_videos = fr_videos.rename(columns={'comment_count':'comments'})

fig = px.scatter_matrix(fr_videos, dimensions=['views', 'likes', 'dislikes', 'comments'])
# You can add diagonal_visible=False as argument in update_traces if you want to skip the diagonal
fig.update_traces(opacity=0.3, showupperhalf=False)
fig.show()


# This scatter_matrix can quickly show any simple relationship between these 4 columns **all Categories combined**. When it comes to opinions about videos, we expect them to diverge i.e. we expect outliers. Therefore, setting opacity < 1 helps seeing a tendency if there is one. For example, it looks like:
# - The number of **views** is correlated with the number of **comments** and **likes**.
# - The number of **likes** is correlated with the number of **comments**.
# - The number of **dislikes** doesn't seem correlated with other interactions except maybe for **comments**.  
# 
# Computing correlations between these variables could confirm these assumptions.

# ## <a id='4.4'> 4.4 comments_disabled, rating_disabled & video_error_or_removed --> is_any_disabled</a>

# In[ ]:


px.histogram(fr_videos, x='comments_disabled', facet_col='video_error_or_removed', color='ratings_disabled')


# Observations:
# - Only very few videos can be trending when the flag video_error_or_removed is up. I'm not sure what it means: has the video become trending then it was removed by the author ? Or by Youtube ? Or is it a simple flag to say the video has been uploaded several times before it became trending ?
# - Overall, few videos become trending with any of these options disabled.
# 
# Thefore, we'll add a column containing a boolean set to True (or 1) if any of these 3 options is disabled:

# In[ ]:


any_disabled = pd.Series([True if any([com, rat, err]) else False for com, rat, err in zip(fr_videos['comments_disabled'],
                                         fr_videos['ratings_disabled'],
                                         fr_videos['video_error_or_removed'])])


# In[ ]:


# Let's quickly check if any_disabled did the trick:
try:
    assert fr_videos[(fr_videos['comments_disabled'] == False) & 
          (fr_videos['ratings_disabled'] == False) & 
          (fr_videos['video_error_or_removed'] == False)].shape[0] == (any_disabled == False).sum()
    fr_videos['any_disabled'] = any_disabled
except AssertionError:
    print("any_disabled was not successfully computed !")


# ## <a id='4.5'> 4.5 description</a>

# In[ ]:


fr_videos['description'].head()


# In[ ]:


fr_videos['description'].isna().sum()


# Few videos have no description. Now, we could study the content using NLP but that's not my goal for this kernel.  
# Still, we can create a feature with the description length.

# In[ ]:


# Count length of the description
fr_videos['description_length'] = fr_videos['description'].str.len()

# Input 0 for missing values and convert series to integer type
fr_videos['description_length'] = fr_videos['description_length'].fillna(0).astype(int)


# ## <a id='4.6'> 4.6 tags</a>

# In[ ]:


fr_videos['tags'].head()


# Here, we can retreive the number of tags of the video and tags themselves with simple string work.

# In[ ]:


# Lower case tags, remove "" then retreive each tag separated from '|'
# It's delicate to work with accents & encoding because some characters might be erased e.g. arabic characters
split_tags = fr_videos['tags'].str.replace('"', '').str.lower().str.split('|')
split_tags.head()


# In[ ]:


# Second row contains [[none]] which is weird: is it a tag itself or an error ? Let's find out
split_tags.iloc[1]


# In[ ]:


# First check if there are empty lists
print(split_tags.apply(lambda l: len(l) == 0).sum())

# Check if there are videos with 'none' as tag
matchers = ['none','None', 'NONE']
# This retreive matchers only
# Convert to tuple temporarily because using value_counts() on lists objects raise error with pandas 0.25.0
nones = split_tags.apply(lambda l: tuple(s for s in l if any(xs in s for xs in matchers)))
nones.value_counts()


# In[ ]:


# We don't want to remove tags containing 'none' but the [[none]]
split_tags.apply(lambda l: l == ['[none]']).sum()


# In[ ]:


split_tags_cleaned = split_tags.apply(lambda l: np.nan if l == ['[none]'] else l)

# Input number of tags in the list and 0 if there's none (NaN)
fr_videos['tags_count'] = split_tags_cleaned.apply(lambda x: int(len(x)) if type(x) == list else 0)


# In[ ]:


# I'm not sure what to do with all these tags. I guess the order may be important therefore I'll add 5 features for the first 5 tags

def input_n_tag(tags, n):
    try:
        n_tag = tags[n]
    # When dealing with NaN
    except TypeError:
        n_tag = 'notag'
    # When list too short
    except IndexError:
        n_tag = 'notag' 
    return n_tag 
    
fr_videos['tag1'] = split_tags_cleaned.apply(lambda l: input_n_tag(l, 0))
fr_videos['tag2'] = split_tags_cleaned.apply(lambda l: input_n_tag(l, 1))
fr_videos['tag3'] = split_tags_cleaned.apply(lambda l: input_n_tag(l, 2))
fr_videos['tag4'] = split_tags_cleaned.apply(lambda l: input_n_tag(l, 3))
fr_videos['tag5'] = split_tags_cleaned.apply(lambda l: input_n_tag(l, 4))


# In[ ]:


fr_videos.loc[:5, ['title', 'tags_count', 'tag1', 'tag2', 'tag5']]


# In[ ]:


# Adding all tags in a single list
all_tags = split_tags_cleaned.explode().astype(str)
text = ', '.join(all_tags)

# Create wordcloud from single string
wordcloud = WordCloud().generate(text)
wordcloud = WordCloud(background_color="white", max_words=1000, max_font_size=40, relative_scaling=.5).generate(text)

plt.figure(figsize=(14, 10))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


# ## <a id='4.7'> 4.7 title</a>

# There's nothing much to do except count the title's length.

# In[ ]:


fr_videos['title_length'] = fr_videos['title'].str.len()


# In[ ]:


fr_videos.loc[:5, ['title', 'title_length']]


# ## <a id='4.8'> 4.8 channel_title</a>

# If there are too many unique values, we should remove this column otherwise it will be poor information for the model.

# In[ ]:


print("Number of videos: {} for {} different channels.".format(fr_videos.shape[0], len(fr_videos['channel_title'].unique())))


# This could be a strong predictor - depending on the channel. Let's just lowercase the values.

# In[ ]:


fr_videos['channel_title'] = fr_videos['channel_title'].str.lower()


# # <a id='5'> 5 Correlations</a>

# In[ ]:


corr = fr_videos.loc[:, ['views', 'likes', 'dislikes', 'comments', 'trending_time', 'tags_count', 'description_length', 'title_length']].corr()


# In[ ]:


fig2 = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.index,
        y=corr.index,
        colorscale="Earth",
        zmin=-1,
        zmax=1
    # negative values
))
fig2.update_layout(title='Correlations all Categories combined')
fig2.show()


# As we guessed:
# - views and likes are highly correlated (**0.81**) and are correlated with comments (**0.71**)
# - likes and comments are highly correlated (**0.85**)
# - dislikes are correlated with comments (**0.66**)
# 
# Regarding other features:
# - **trending_time is not linearly correlated with any feature**.
# - neither are tags_count, description_length & title_length

# It's important to recall these statistics do not take the video category into account. Comparing these correlations between each category could underline stronger correlations. Let's add a dropdown button to switch category.

# In[ ]:


# Prepare correlation dataframes for heatmaps
categories = fr_videos['category'].unique()
interactions_corr_list = [fr_videos[fr_videos['category'] == cat].loc[:, ['views', 'likes', 'dislikes', 'comments', 'trending_time', 'tags_count',
                                                                          'description_length', 'title_length']].corr() for cat in categories]

#Initialize figure
fig3 = go.Figure()

# Add each heatmap, let the first one visible only to avoid traces stacked
for idx, corr in enumerate(interactions_corr_list):
    if idx==0:
        fig3.add_trace(
            go.Heatmap(
                z=corr.values,
                x=corr.index,
                y=corr.index,
                colorscale="Earth",
                zmin=-1,
                zmax=1,
                visible=True))
    else:
         fig3.add_trace(
            go.Heatmap(
                z=corr.values,
                x=corr.index,
                y=corr.index,
                colorscale="Earth",
                zmin=-1,
                zmax=1,
                visible=False)) 

# Add buttons
fig3.update_layout(
    updatemenus=[
        go.layout.Updatemenu(
            active=0,
            x=0.8,
            y=1.2,
            buttons=list([
                dict(label=cat,
                     method="update",
                     # This comprehension list let visible the current trace only by setting itself to True and others to False
                     args=[{"visible": [False if sub_idx != idx else True for sub_idx, sub_cat in enumerate(categories)]},
                           {"title": "Correlation heatmap for category: " + cat}])
                for idx, cat in enumerate(categories)
            ] ) 
        )
    ])


# > Be aware of the **colorscale**: it fits the different values but you'll see **different colors for very close values** when the range is short (e.g. Trailers).  
# Also, the sliding bar is thin and grey hence might be hard to see. But you can use it: it's just right to the dropdown list, starting at the top.

# This shows news more precise insights and, as expected, shows categories with more or less interaction and of different kinds. For example:
# - **Music** only reveals interactions between **views and dislikes (0.90)** and between **likes and comments (0.79)**. In the first case, this happens when a music video goes viral but is overall not appreciated. It actually goes beyond non-appreciation because most people click on the dislike button only when they deeply dislike or disagree with its content (politics, nudity, really cheap/bad content, ...).
# - **Shows** and **Trailers** display high correlations with any combination, which is weird. If we look closely, Shows and Trailers gather respectively **114 and 11 videos**. Hence, **statistics are less reliable.**
# 
# In addition to that, there's an **enhanced disappointement effect**. Indeed, watching a video doesn't mean you'll like it. Regarding trending videos, this feeling can be strengthened when Youtube shows you a viral video and you may have high expectations. Therefore, it can push you to dislike it or leave a (negative) comment.

# # <a id='6'> 6 Predicting trending time with Machine Learning</a>

# Coming soon !

# In[ ]:




