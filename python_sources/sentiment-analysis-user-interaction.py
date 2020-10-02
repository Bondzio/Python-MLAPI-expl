#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


raw_rec=pd.read_csv('/kaggle/input/food-com-recipes-and-user-interactions/RAW_recipes.csv')
raw_inter=pd.read_csv('/kaggle/input/food-com-recipes-and-user-interactions/RAW_interactions.csv')


# 1. TO check seniment analysis.I have took files only.One for receipe id and other for customer reviews,

# In[ ]:


raw_rec['tags']
raw_inter['review'][0]

get_ipython().system('pip install vaderSentiment')


# Package used here for sentiment analysis is VaderSentiment
# You can install it using **pip install vaderSentiment**
# 
# More documentation visit to github repo for the same
# 

# In[ ]:


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
sentense_list=raw_inter['review'].tolist()

for i in sentense_list:
    sentense=i
    score = analyser.polarity_scores(sentense)
    print("{:-<40} {}".format(sentense, str(score)))
    


# I will add more code in it furthur commits
# 

# 

# In[ ]:




