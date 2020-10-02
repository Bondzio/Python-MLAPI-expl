#!/usr/bin/env python
# coding: utf-8

# In this post i used seaborn for charting and pandas data frame. 
# 
# Please consider upvote :) 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import seaborn as sns
from sklearn import preprocessing
import pandas as pd 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt  
matplotlib.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')
import math

input_df = pd.read_csv("../input/appendix.csv",sep=',',parse_dates=['Launch Date'])
input_df['year'] = input_df['Launch Date'].dt.year
print(input_df.columns)

# Any results you write to the current directory are saved as output.


# **Most frequesnt Course Title**

# In[ ]:


from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

wordcloud = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='white',
                          width=1200,
                          height=1000
                         ).generate(" ".join(input_df['Course Title']))


plt.imshow(wordcloud)
plt.axis('off')
plt.show()


# **Most frequesnt Course Subject**

# In[ ]:


from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

wordcloud = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='white',
                          width=1200,
                          height=1000
                         ).generate(" ".join(input_df['Course Subject']))


plt.imshow(wordcloud)
plt.axis('off')
plt.show()


# **Number of course  by  Institution** 

# In[ ]:


sns.factorplot('Institution',data=input_df,kind='count')


# **Number of Course by Institution - year based distribution** 

# In[ ]:


sns.factorplot('year',data=input_df,hue='Institution',kind='count')


# **Number of participants per Institution**

# In[ ]:


no_of_participents = input_df[['Institution',"Participants (Course Content Accessed)"]].groupby('Institution').sum()
no_of_participents = no_of_participents.reset_index()

print(no_of_participents)

sns.factorplot(x='Institution',y='Participants (Course Content Accessed)',kind='bar',data=no_of_participents)


# **Number of participants per Institution - year based** 

# In[ ]:



no_of_participents = input_df[['Institution',"Participants (Course Content Accessed)",'year']].groupby(['Institution','year']).sum()
no_of_participents = no_of_participents.reset_index()

print(no_of_participents)
sns.barplot(x='year',y='Participants (Course Content Accessed)',hue='Institution',data=no_of_participents)


# **Comparison - Total number of Participants, Total number of Participants > 50% Course Content Accessed and Certified**

# In[ ]:


participants_stats = input_df[['Participants (Course Content Accessed)','Audited (> 50% Course Content Accessed)','Certified']]
participants_stats.columns = ['total','50%Accessed','Certified']
no_of_participents = input_df[['Institution',"Participants (Course Content Accessed)","Audited (> 50% Course Content Accessed)","Certified",'year']].groupby(['Institution','year']).sum()
no_of_participents = no_of_participents.reset_index()

print(no_of_participents)


no_of_participents.plot(x='year',kind='bar',alpha=0.5,figsize=(9,5))


# In[ ]:


participants_stats = input_df[['Participants (Course Content Accessed)','Audited (> 50% Course Content Accessed)','Certified']]
participants_stats.columns = ['total','50%Accessed','Certified']

interested_clms = ["% Certified of > 50% Course Content Accessed","% Played Video",
                   "% Posted in Forum","% Grade Higher Than Zero","% Male","% Female",
                   "% Bachelor's Degree or Higher"]


for cname in interested_clms:
    participants_stats[cname] = (input_df['Participants (Course Content Accessed)'] * (input_df[cname] if type(input_df[cname]) is str else 0) /100)

#participants_stats = participants_stats.drop(['Participants (Course Content Accessed)','% Certified','% Audited'],1)

participants_stats.columns = ['total','Audited','Certified','Certified>50%CourseContentAccessed','PlayedVideo','PostedinForum','HigherThanZero','Male','Female','BachelorDegreeorHigher']
sns.pairplot(participants_stats)

