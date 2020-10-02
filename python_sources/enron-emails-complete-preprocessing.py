#!/usr/bin/env python
# coding: utf-8

# ## Import and have a Look

# In[ ]:


import numpy as np
import pandas as pd

import os, gc, re

df = pd.read_csv('/kaggle/input/enron-email-dataset/emails.csv')
df.head(5)


# Wow, only two columns! What's inside the message? Let's look at an example:

# In[ ]:


print(df.iloc[22,1])


# ## Information Part
# 
# Let's seperate the "info" and "content" parts, and deal with the information part first.

# In[ ]:


def info_part(i):
    """split infomation part out"""
    return i.split('\n\n', 1)[0]
def content_part(i):
    """split content part out"""
    return i.split('\n\n', 1)[1]
df['pre_info'] = df.message.map(info_part)
df['content'] = df.message.map(content_part)
df['test_true'] = True

words2split = ['Message-ID: ', 'Date: ', 'From: ', 'To: ', 'Subject: ', 'Cc: ', 'Mime-Version: ', 'Content-Type: ',
               'Content-Transfer-Encoding: ', 'Bcc: ', 'X-From: ', 'X-To: ', 'X-cc: ', 'X-bcc: ', 'X-Folder: ', 'X-Origin: ',
               'X-FileName: ']
features_naming = [i[:-2] for i in words2split]
split_condition = '|'.join(words2split)


# In[ ]:


# Some emails' subject confuse the string-spliting function, so I make a little change
def duplicated_info(i):
    return i.replace(' Date: ', ' Date- ').replace(' Subject: ', ' Subject2: ').replace(' To: ',
                    ' To- ').replace(' (Subject: ', ' (Subject- ')
df['pre_info'] = df['pre_info'].map(duplicated_info)

# let's check how many categories are there in these emails
def num_part(i):
    return len(re.split(split_condition, i))
df['num_info'] = df['pre_info'].map(num_part)

# around 20k emails do not have the 'To: ' category, so I add one
def add_to(i):
    return i.replace('\nSubject: ', '\nTo: \nSubject: ')
temp_condition = (df['num_info'] == 17) | (df['num_info'] == 15)
df.loc[temp_condition, 'pre_info'] = df.loc[temp_condition, 'pre_info'].map(add_to)


# similar way to deal with the "Cc:" and "Bcc:" categories
temp_condition = (df['num_info'] == 16) | (df['num_info'] == 15)
def add_bcc(i):
    return i.replace('\nX-From: ', '\nBcc: \nX-From: ')
df.loc[temp_condition, 'pre_info'] = df.loc[temp_condition, 'pre_info'].map(add_bcc)
def add_cc(i):
    return i.replace('\nMime-Version: ', '\nCc: \nMime-Version: ')
df.loc[temp_condition, 'pre_info'] = df.loc[temp_condition, 'pre_info'].map(add_cc)


# Now let's see how many wrong-formatted email are left:

# In[ ]:


df['num_info'] = df['pre_info'].map(num_part)
df['num_info'].value_counts()


# Oh, there are 3 of them.
# I would simply choose to print them out to have a look, then remove from dataset.

# In[ ]:


df_remove = df.loc[df['num_info'] != 18].copy()
df = df.loc[df['num_info'] == 18].copy()


# In[ ]:


global feature_idx
def info_split(i):
    ## split the i th part out and remove \n for the feature
    return re.split(split_condition, i)[feature_idx+1][:-2]
def info_split_last(i):
    ## no need to remove \n for last category -- X-FileName
    return re.split(split_condition, i)[feature_idx+1]
for feature_idx in range(len(words2split)):
    if feature_idx != len(words2split) - 1:
        df[features_naming[feature_idx]] = df['pre_info'].map(info_split)
    else:
        df[features_naming[feature_idx]] = df['pre_info'].map(info_split_last) 


# Let's check one category if I did well:

# In[ ]:


df['Content-Transfer-Encoding'].value_counts()


# There is still one not quite right, I would just take it away too...

# In[ ]:


df_remove2 = df.loc[df['Content-Transfer-Encoding'] == 'text/plain; charset=us-asci']
df = df.loc[df['Content-Transfer-Encoding'] != 'text/plain; charset=us-asci']


# Have a read at these discarded emails...

# In[ ]:


# print(df_remove.iloc[0,1])
# print(df_remove2.iloc[0,1])


# ## Content part 
# 
# There are a lot of emails contain non plain English info such as attach file and "Forwarded" message, I discovered that many of them were seperated by "-------------". Therefore I use this to discard these parts and add indicators.

# In[ ]:


df.loc[df["content"].str.contains("-------------"), "content"]


# In[ ]:


def split_other_content(i):
    """split other forms of contents out"""
    return i.split('-------------', 1)[0]
df["has_other_content"] = df["content"].str.contains("-------------")
df["if_forwarded"] = df["content"].str.contains("------------- Forwarded")
df['content'] = df.content.map(split_other_content)


# I know this is not a perfect way, but it is efficient enough.  
# Finally we drop the auxiliary columns and export it:

# In[ ]:


df = df.drop(['pre_info','test_true', 'num_info'], axis = 1).set_index("file")
df.to_csv("emails_cleaned.csv")


# Note that the content part can be cleaned deeper, you will need extra effort to fight with it. Good Luck!

# In[ ]:


df.head(5)


# ### If this kernel helps you, please upvote!
