#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from bs4 import BeautifulSoup
import re

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


forums = pd.read_csv('../input/meta-kaggle/Forums.csv',
                    usecols=["Id", 'Title']).rename(columns={"Title":"ForumTitle"}).set_index("Id")
forums.head()


# In[ ]:


topics =  pd.read_csv('../input/meta-kaggle/ForumTopics.csv',
                      usecols=["Id", 'ForumId',  'Title']
                     ) ## most other attributes are "leaky"

topics = topics.merge(forums, left_on="ForumId",right_index=True).drop(["ForumId"],axis=1)
topics.head()


# In[ ]:


messages = pd.read_csv('../input/meta-kaggle/ForumMessages.csv',usecols=[ 'ForumTopicId', 'PostUserId', 'PostDate', 'ReplyToForumMessageId',
       'Message', 'Medal'])
messages = messages[messages.Message.notna()]
messages["Medal"] = messages["Medal"].fillna(0).astype(int)
messages = messages.drop_duplicates(subset=['Message', 'Medal'])
messages['PostDate'] = pd.to_datetime(messages['PostDate'], infer_datetime_format=True)
messages['ReplyToForumMessageId'] = messages['ReplyToForumMessageId'].isna().astype(int) # replace wit hfeature of whether message was reply or not


messages["preCleaning_word_length"] =messages['Message'].str.split(" ").str.len() # count of words before we clean out the html and code


# In[ ]:


messages = messages.merge(topics,right_on="Id", left_on="ForumTopicId").drop(["ForumTopicId"],axis=1)
messages.head()


# In[ ]:


# cleaning messages from HTML tags
messages_str = ' |sep| '.join(messages.Message.tolist())

messages_str = re.sub(r'<code>.*?</code>', '', messages_str, flags=re.DOTALL)
messages_str = re.sub('<-', '', messages_str)

messages_str = BeautifulSoup(messages_str, 'lxml').get_text()

messages_str = re.sub(r'http\S+', '', messages_str)
messages_str = re.sub(r'@\S+', '', messages_str)

messages['Message'] = messages_str.split(' |sep| ')

messages = messages.drop_duplicates(subset=['Message', 'Medal'])
messages['Message'].head()


# In[ ]:


print(messages.shape[0])


# ## Minor EDA
# * remove some super long messages (space/memory's sake)
# * We count # character s and words in a message

# In[ ]:


messages["character_length"] = messages['Message'].str.len()
messages["word_length"] =messages['Message'].str.split(" ").str.len()
messages.describe()


# In[ ]:


messages.Medal.value_counts()


# In[ ]:


print(messages["character_length"].quantile(0.999))
print(messages["word_length"].quantile(0.999))


# * we see we have medals in this range of long messages. Specifically, there are gold medal posts that are super long

# In[ ]:


messages.loc[messages["character_length"]>5000].Medal.describe()


# In[ ]:


messages.loc[messages["word_length"]>5000].Medal.describe()


# In[ ]:


messages.loc[messages["Medal"]>=1]["word_length"].describe()


# In[ ]:


messages.loc[messages["Medal"]==3]["word_length"].describe()


# In[ ]:


messages.loc[messages["word_length"]>10000]["Message"].head()


# ##### drop some of the extremely long messages

# In[ ]:


print(messages.shape[0])
messages = messages.loc[((messages["word_length"]<4000) & messages["character_length"]<15000)]

print(messages.shape[0])


# ### Export data

# In[ ]:


messages.to_csv("kaggle_forum_messages_medals.csv.gz",index=False,compression="gzip")

