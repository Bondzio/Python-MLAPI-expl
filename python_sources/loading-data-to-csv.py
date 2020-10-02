#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os
import glob
import json


# In[ ]:


positive_list = glob.glob("../input/malaysia-twitter-sentiment/positive/*.json")
negative_list = glob.glob("../input/malaysia-twitter-sentiment/negative/*.json")

positive_list.sort()
negative_list.sort()

data = pd.DataFrame(columns=('text', 'label'))
data.head()


# In[ ]:


for path in positive_list[:5]:
    with open(path) as f:
        text_list = json.load(f)
        for text in text_list:
            data = data.append({'text': text,
                                'label': 1},
                                ignore_index=True)
            
for path in negative_list[:5]:
    with open(path) as f:
        text_list = json.load(f)
        for text in text_list:
            data = data.append({'text': text,
                                'label': 0},
                                ignore_index=True)

print(data.shape)
data.head()


# In[ ]:


data.label.value_counts()


# In[ ]:


print("Negative percentage: {}%".format( (data.label.value_counts()[0] / data.shape[0]) * 100))
print("Positive percentage: {}%".format( (data.label.value_counts()[1] / data.shape[0]) * 100))


# In[ ]:


data.to_csv("malay_twitter_sentiment.csv", index=False)
data.head()


# In[ ]:




