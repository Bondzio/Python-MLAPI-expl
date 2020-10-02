#!/usr/bin/env python
# coding: utf-8

# # Importing Neccessary Libraries
# ### Import tweepy for accessing Tweets

# In[ ]:


get_ipython().system('pip install tweepy')
import tweepy
from tweepy import Stream
from tweepy import StreamListener
import json
from textblob import TextBlob
import re
import csv
import nltk
import pandas as pd
import time
nltk.download('punkt')


# # Writing my Access key to Access the tweets

# In[ ]:


consumer_key = "Type your access key"
consumer_secret = "Type your access key"
access_token = "Type your access key"
access_token_secret = "Type your access key"


# # Creating a blank CSV file to store the sentiments

# In[ ]:


df = pd.DataFrame(list())
df.to_csv('sentiment.csv')


# # Accessing tweets and storing in CSV file.

# In[ ]:


biden=0
trump=0
#setting the columns for csv file
header_name = ['Trump', 'Biden']
with open('sentiment.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=header_name)
    writer.writeheader()

class Listener(StreamListener):
    #setting the time limit for processing
    def __init__(self, time_limit=120):
        self.start_time = time.time()
        self.limit = time_limit
        super(Listener, self).__init__()
    
    def on_data(self, data):
        
        if (time.time() - self.start_time) < self.limit:
            raw_tweets = json.loads(data)
            try:
                tweets = raw_tweets['text']
                #using regular expression to extract the text of the tweets.
                tweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())
                tweets = ' '.join(re.sub('RT',' ', tweets).split())
                #applying textblob to tweets for sentiment analysis
                blob = TextBlob(tweets.strip())


                global biden
                global trump



                bidenS=0
                trumpS=0


                for sent in blob.sentences:
                    #extracting sentiment of a tweet
                    if "Trump" in sent and not "Biden" in sent:
                        trumpS = trumpS + sent.sentiment.polarity
                    elif "Biden" in sent and not "Trump" in sent:
                        bidenS = bidenS + sent.sentiment.polarity


                #calculating cumulative sentiment for all tweets
                biden = biden + bidenS
                trump = trump + trumpS

                with open('sentiment.csv', 'a') as file:
                    writer = csv.DictWriter(file, fieldnames=header_name)
                    info = {
                        'Trump' : trump,
                        'Biden' : biden
                    }
                    writer.writerow(info)

                return(True)
            
            except:
                pass
            
        else:
            return(False)
        
    def on_error(self, status):
        print(status)


# # Authentication

# In[ ]:


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# # Streaming the Tweets

# In[ ]:


twitter_stream = Stream(auth, Listener())
twitter_stream.filter(track = ['Trump','Biden'])


# # Plotting the Visualizations

# In[ ]:


import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'notebook')

plt.style.use('fivethirtyeight')


# In[ ]:


fig = plt.figure(figsize=(10,8))

data = pd.read_csv('sentiment.csv')
y1 = data['Biden']
y2 = data['Trump']

plt.cla()
plt.plot(y1, label='Joe Biden')
plt.plot(y2, label='Donald Trump')

plt.legend(loc='upper left')
plt.tight_layout()


# # Conclusion
# * The program ran for 2 minutes and analysed aprroximately 6000 tweets.
# * From the above graph we can see that in the last 6000 tweets cumulative sentiment for VP Biden is increasing stabally.
# * From the above graph we can see that cumulative sentiment for President Trump is drastically increasing at some interval and also decreasing drastically.

# In[ ]:




