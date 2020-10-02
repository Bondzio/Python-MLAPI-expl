#!/usr/bin/env python
# coding: utf-8

# # Facebook Data and Activity Visualizations

# Importing some basic libraries we are going to need
# 
# Adding a list of Roman Urdu stopwords as most of Facebook posts and comments have a lot of Roman Urdu usage.
# 
# Roman Urdu stopwords source: https://github.com/haseebelahi/roman-urdu-stopwords

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
from csv import QUOTE_NONE
import nltk

from wordcloud import WordCloud, STOPWORDS

custom_stopwords = ['happy', 'birthday', 'hbd', 'brthday', 'thanks', 'thank']
roman_urdu_stopwords = ['ai', 'ayi', 'hy', 'hai', 'main',
                        'ki', 'tha', 'koi', 'ko', 'sy', 'woh', 'bhi', 'aur', 'wo', 'yeh', 
                        'rha', 'hota', 'ho', 'ga', 'ka', 'le', 'lye', 'kr', 'kar', 'lye', 
                        'liye', 'hotay', 'waisay', 'gya', 'gaya', 'kch', 'ab', 'thy', 'thay', 
                        'houn', 'hain', 'han', 'to', 'is', 'hi', 'jo', 'kya', 'thi', 'se', 'pe', 
                        'phr', 'wala', 'waisay', 'us', 'na', 'ny', 'hun', 'rha', 'raha', 'ja',
                        'rahay', 'abi', 'uski', 'ne', 'haan', 'acha', 'nai', 'sent', 'photo', 
                        'you', 'kafi', 'gai', 'rhy', 'kuch', 'jata', 'aye', 'ya', 'dono', 'hoa', 
                        'aese', 'de', 'wohi', 'jati', 'jb', 'krta', 'lg', 'rahi', 'hui', 'karna', 
                        'krna', 'gi', 'hova', 'yehi', 'jana', 'jye', 'chal', 'mil', 'tu', 'hum', 'par', 
                        'hay', 'kis', 'sb', 'gy', 'dain', 'krny', 'tou', 'ha']


# ## Utility Functions

# Function for reading the csv files

# In[ ]:


def read_and_reformat(csv_path):
    df = pd.read_csv(csv_path,
                     dtype=object)
    return df


# Cleaning a single word of any punctuation marks or trailing spaces or new lines

# In[ ]:


import re
def cleaner_word(word):
    word = re.sub(r'\#\.', '', word)
    word = re.sub(r'\n', '', word)
    word = re.sub(r',', '', word)
    word = re.sub(r'\-', ' ', word)
    word = re.sub(r'\.', '', word)
    word = re.sub(r'\\', ' ', word)
    word = re.sub(r'\\x\.+', '', word)
    word = re.sub(r'\d', '', word)
    word = re.sub(r'^_.', '', word)
    word = re.sub(r'_', ' ', word)
    word = re.sub(r'^ ', '', word)
    word = re.sub(r' $', '', word)
    word = re.sub(r'\?', '', word)
    
    if len(word) == 1:
        word = ''
    
    return word.lower() 


# Cleaning sentences

# In[ ]:


def cleaner_sentence(sentence):
    clean_sentence = ''
    tokens = sentence.split()
    for token in tokens:
        token = cleaner_word(token)
        clean_sentence += token + ' '
    return clean_sentence


# Function for plotting the frequency of top x ngrams in a given text

# In[ ]:


def draw_top_ngrams(top, raw_text, title, color, ngram=2):
    tokens = nltk.word_tokenize(raw_text)

    tokens = [word for word in tokens if word not in STOPWORDS]
    tokens = [word for word in tokens if word not in custom_stopwords]
    tokens = [word for word in tokens if word not in roman_urdu_stopwords]
    tokens = [word for word in tokens if len(word) > 2]

    #Create your bigrams
    

    bgs = nltk.ngrams(tokens, n=ngram)
    
    #compute frequency distribution for all the bigrams in the text
    fdist = nltk.FreqDist(bgs)
    most_common = fdist.most_common(top)
    common_bigrams = [(' '.join(x[0]), x[1]) for x in most_common]

    itr = zip(*common_bigrams)
    bigrams = next(itr)
    frequency = next(itr)
    x_pos = np.arange(len(frequency)) 

    plt.figure(num=None, figsize=(15, 7), dpi=80, facecolor='w', edgecolor='k')

    plt.title(title + ' most common ngrams (n = ' + str(ngram) + ')')
    bar = plt.bar(x_pos, frequency,align='center', color=color, edgecolor='black')
    
    for rect in bar:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')

    
    plt.xticks(x_pos, bigrams, rotation=75) 
    plt.ylabel('Frequency')
    plt.show()


# Group post and comments data by year

# In[ ]:


def get_by_year_data(df, only_count = False):
    items_by_year = {}
    item_lengths_by_year = {}
    item_count_by_year = {}
    
    for i, row in df.iterrows():
        if not only_count:
            clean_sentence = cleaner_sentence(row['text'].lower())
        try:
            if not only_count:
                items_by_year[get_year_from_timestamp(row['timestamp'])] += clean_sentence
                item_lengths_by_year[get_year_from_timestamp(row['timestamp'])] += len(clean_sentence)
            item_count_by_year[get_year_from_timestamp(row['timestamp'])] += 1
        except:
            if not only_count:
                items_by_year[get_year_from_timestamp(row['timestamp'])] = clean_sentence
                item_lengths_by_year[get_year_from_timestamp(row['timestamp'])] = len(clean_sentence)
            item_count_by_year[get_year_from_timestamp(row['timestamp'])] = 1
    
    if not only_count:
        return (items_by_year, item_lengths_by_year, item_count_by_year)
    return item_count_by_year


# Create a wordcloud for given text

# In[ ]:


def create_wordcloud(text, custom_stopwords):
    for sw in custom_stopwords:
        STOPWORDS.add(sw);
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='black', width=800, height=400).generate(text)
    plt.figure( figsize=(20,10))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()


# Get year from UNIX style timestamps

# In[ ]:


from datetime import datetime
def get_year_from_timestamp(ts):
    ts = int(ts)
    return datetime.utcfromtimestamp(ts).strftime('%Y')


# Get date from UNIX style timestamps

# In[ ]:


def get_date_from_timestamp(ts, format='%Y-%m-%d'):
    ts = int(ts)
    return datetime.utcfromtimestamp(ts).strftime(format)


# ## Stats and Visualizations on Facebook Posts, Comments and Location
# 
# ##### Facebook actually does not provide the data in CSV format, I downloaded the data in JSON and converted it to CSVs using this script:
# https://gist.github.com/haseebelahi/0ef3a52b89b6890e66290d006c94ac10

# ## Facebook Posts

# In[ ]:


df = read_and_reformat('../input/csvs/csvs/posts.csv')
df.head()


# #### Getting posts data grouped by year

# In[ ]:


posts_by_year, posts_lengths_by_year, posts_count_by_year  = get_by_year_data(df)


# ### Generating Word Clouds for Facebook Posts by each year since 2010

# In[ ]:


for key in sorted(posts_by_year.keys()):
    print("Year: " + key)
    create_wordcloud(posts_by_year[key], custom_stopwords + roman_urdu_stopwords)


# ### Number of Facebook Posts each Year (including posts in Groups)

# In[ ]:


from collections import OrderedDict
posts_count_by_year = OrderedDict(sorted(posts_count_by_year.items(), key=lambda t: t[0]))

plt.figure(num=None, figsize=(15, 7), dpi=80, facecolor='w', edgecolor='k')
bar = plt.bar(range(len(posts_count_by_year)), list(posts_count_by_year.values()), align='center', edgecolor='black')
plt.xticks(range(len(posts_count_by_year)), list(posts_count_by_year.keys()))
plt.ylabel('Number of Posts')
plt.title('Number of Facebook posts by Year (including posts in Groups)')

for rect in bar:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')

plt.show()


# ![Wow](https://media.giphy.com/media/PUBxelwT57jsQ/giphy.gif)
# 
#                                                     500 posts in 2014

# ### Average length of a post (in words) for each year

# In[ ]:


avg_post_length_by_year = {}

for key in sorted(posts_lengths_by_year.keys()):
    avg_post_length_by_year[key] = round(posts_lengths_by_year[key] / posts_count_by_year[key], 2)

plt.figure(num=None, figsize=(15, 7), dpi=80, facecolor='w', edgecolor='k')
bar = plt.bar(range(len(avg_post_length_by_year)), list(avg_post_length_by_year.values()), align='center', color='#aa61a7', edgecolor='black')
plt.xticks(range(len(avg_post_length_by_year)), list(avg_post_length_by_year.keys()))
plt.ylabel('Average Length of Post (in words)')
plt.title('Average length of Facebook posts by Year (including posts in Groups)')

for rect in bar:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')

plt.show()


# ### Post Count vs Avg. Post Length in each Year
# 
# #### This is a very interesting stat, which shows that with time maybe, the quality and content of Facebook posts has increased but the frequency of posting has decreased. It also shows the evolution of Facebook from a platform for posting silly jokes to posting serious detailed posts.

# In[ ]:


import numpy as np

plt.figure(num=None, figsize=(15, 7), dpi=80, facecolor='w', edgecolor='k')
ax = plt.subplot(111)
X = np.arange(len(posts_count_by_year))
bar1 = ax.bar(X, posts_count_by_year.values(), width=0.3, color='y', align='center', edgecolor='black')
bar2 = ax.bar(X-0.3, avg_post_length_by_year.values(), width=0.3, color='g', align='center', edgecolor='black')
ax.legend(('Post Count','Avg. post length (in words)'))
plt.xticks(X, avg_post_length_by_year.keys())
plt.title("Post Count vs Avg. post length by year")

for rect in bar1 + bar2:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')


plt.show()


# ### 30 Most Frequent Bigrams
# 
# #### Overall this seems to be heavily affected by a lot of spam posting I did to promote university events.

# In[ ]:


all_posts_text = ''
for posts in posts_by_year.values():
    all_posts_text += posts + ' '
    
draw_top_ngrams(raw_text=all_posts_text, top=30, title='All time', color='#e58f4e', ngram=2)


# ## Facebook Comments

# In[ ]:


df_comments = read_and_reformat('../input/csvs/csvs/comments.csv')
df_comments.head()


# #### Getting comments data grouped by year

# In[ ]:


comments_by_year, comments_lengths_by_year, comments_count_by_year  = get_by_year_data(df_comments)


# ### Generating Word Clouds for Facebook Comments by each year since 2010

# In[ ]:


for key in sorted(comments_by_year.keys()):
    print("Year: " + key)
    create_wordcloud(comments_by_year[key], custom_stopwords + roman_urdu_stopwords)


# ### Number of Facebook Comments each Year (including posts in Groups)

# In[ ]:


from collections import OrderedDict
comments_count_by_year = OrderedDict(sorted(comments_count_by_year.items(), key=lambda t: t[0]))

plt.figure(num=None, figsize=(15, 7), dpi=80, facecolor='w', edgecolor='k')
bar = plt.bar(range(len(comments_count_by_year)), list(comments_count_by_year.values()), align='center', color='#e5db4e', edgecolor='black')
plt.xticks(range(len(comments_count_by_year)), list(comments_count_by_year.keys()))
plt.ylabel('Number of Comments')
plt.title('Number of Facebook comments by Year (including comments in Groups)')

for rect in bar:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')

plt.show()


# ## Facebook Location Data
# 
# ##### This is the location data that facebook app collects from your phone and stores

# #### Reading and normalizing location data

# In[ ]:


df_locations = read_and_reformat('../input/csvs/csvs/locations.csv')
df_locations['date'] = df_locations.apply(lambda row: get_date_from_timestamp(row['timestamp']), axis=1)
df_locations['datetime'] = df_locations.apply(lambda row: get_date_from_timestamp(row['timestamp'], format='%Y-%m-%d %H:%M:%S'), axis=1)
df_locations[['lat', 'long']] = df_locations[['lat', 'long']].apply(pd.to_numeric)


df_locations.head()


# ### Plotting the Facebook location data on a Map

# In[ ]:


import folium

map=folium.Map(location=[df_locations['lat'].mean(),df_locations['long'].mean()],zoom_start=6)

for i, row in df_locations.iterrows():
    folium.Circle(
    radius=30,
    location=[row['lat'], row['long']],
    color='blue',
    fill=True).add_to(map)

print('Total location entries: ' + str(df_locations['timestamp'].count()))
map


# ### Grouping location data by year

# In[ ]:


locations_per_year = get_by_year_data(df_locations, True)


# ### Location collections by year

# In[ ]:


from collections import OrderedDict
locations_per_year = OrderedDict(sorted(locations_per_year.items(), key=lambda t: t[0]))

plt.figure(num=None, figsize=(15, 7), dpi=80, facecolor='w', edgecolor='k')
bar = plt.bar(range(len(locations_per_year)), list(locations_per_year.values()), align='center', color='#4ee576', edgecolor='black')
plt.xticks(range(len(locations_per_year)), list(locations_per_year.keys()))
plt.ylabel('Location collection count')
plt.title('Number of times Facebook collected Location by Year')

for rect in bar:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')
    
plt.text(bar[0].get_x() + rect.get_width()/2.0, 1200, 'Total collections: ' + str(df_locations['timestamp'].count()), ha='center', va='bottom')
plt.show()


# ### Top 10 Highest Location Gathering days

# In[ ]:


plt.figure(num=None, figsize=(15, 7), dpi=80, facecolor='w', edgecolor='k')
ax = df_locations.groupby('date').count().sort_values('lat', ascending=False).head(10)['timestamp'].plot.bar(edgecolor='black', rot=75)
plt.ylabel('Location collection count')
plt.title('Top 10 highest Location Gathered days')

for p in ax.patches: 
    ax.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')

plt.show()


# ### Number of location captures by hour of the day

# In[ ]:


plt.figure(num=None, figsize=(15, 7), dpi=80, facecolor='w', edgecolor='k')

df_locations['datetime'] = pd.to_datetime(df_locations['datetime'])
ax=df_locations['datetime'].dt.hour.value_counts().plot.bar(edgecolor='black', rot=75)
plt.ylabel('Frequency')
plt.title('Number of location captures by hour')

for p in ax.patches: 
    ax.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')

plt.show()

