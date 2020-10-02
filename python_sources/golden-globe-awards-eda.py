#!/usr/bin/env python
# coding: utf-8

# ### Hello everybody! This is my first EDA and I choose this simple dataset about something I like!
# ### Hope you enjoy it, and if you have any tip, please let me know! Thank you!

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


# ### **Importing the libraries**

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from wordcloud import WordCloud
import re


# ### Importing dataset and seeing general information

# In[ ]:


Data=pd.read_csv('/kaggle/input/golden-globe-awards/golden_globe_awards.csv')
Data.info()


# In[ ]:


# checking why film column has some missing data and collecting other informations
Data.head(20)


# Appears that when the nominee is the film itself, the column film is empty. I Think there is no problem in that
# 
# We also saw that all the data in win columns is True, we gonna have to check this later

# In[ ]:


Data.describe()


# In[ ]:


Data.columns


# In[ ]:


# to rename the columns to a style that I find more aesthetic and readable
Data.rename(columns={'year_film':'YearFilm','year_award':'YearAward', 'ceremony':'Ceremony', 'category':'Category',
                     'nominee':'Nominee', 'film':'Film','win':'Win'}, inplace=True)


# In[ ]:


# as I said before, the firsts rows only show the winners, so we want to check when False start occuring 
Data.loc[:,('YearAward','Win')].loc[Data.Win==False].head(10)


# In[ ]:


# how many differents categories do we have?
Data.Category.unique()


# ### Transforming some data and visualizing

# In[ ]:


#as we have a lot of categories, some with many similarities, I will group them
#this function will be used to group them in three categories
def ActorActressDirector(x):
    if 'Actor' in x:
        return 'Actor/Actress'
    elif 'Actress' in x:
        return 'Actor/Actress'
    elif 'New Star Of The Year' in x:
        return 'Actor/Actress'
    elif 'Director' in x:
        return 'Director'
    else:
        return 'Others'


# In[ ]:


Data['GroupedCategory']=Data.Category.apply(ActorActressDirector)


# In[ ]:


#My original idea was to bring the top 10, but we have to take care if there is someone tied in the last places
#so I'll bring the 15 firsts to check this
TopNominees=Data.Nominee.value_counts().reset_index()
TopNominees.head(15)


# In[ ]:


#as we saw above, there are five persons tied in total nominees around the 10th place, so I'll 
#change to a top 12 to keep them
Top12Nominees=TopNominees.head(12)
plt.figure(figsize=(12,5))
plt.title('Top 12 Total Nominees')
sns.barplot(y='index',x='Nominee', data=Top12Nominees, palette='summer')
plt.xlabel('Count')
plt.ylabel('Nominee')


# In[ ]:


#now I want to show the top 5 winners
TopWinners=Data.loc[Data.Win==True].Nominee.value_counts().reset_index()
TopWinners.head(10)


# In[ ]:


#the same happens here, so I'll change to a top 7
Top7Winners=TopWinners.head(7)
plt.figure(figsize=(12,4))
plt.title('Top 7 Winners')
sns.barplot(y='index', x='Nominee', data=Top7Winners, palette='summer')
plt.xlabel('Count')
plt.ylabel('Nominee')


# In[ ]:


#films with 7 or more nominations in the same year
Films7=pd.DataFrame(Data.groupby('YearAward').Film.value_counts())
Films7.rename(columns={'Film':'Count'},inplace=True)
Films7=Films7.reset_index()
Films7=Films7.query('Count >= 7')
Films7.sort_values(by='Count',ascending=False,inplace=True)


# In[ ]:


plt.figure(figsize=(12,7))
plt.title('Films with 7 or more nominations in the same year')
sns.barplot(y='Film',x='Count',data=Films7, palette='summer')


# In[ ]:


#let's see if we have somebody nominated for Actor/Actress and Director
Director=set(Data.loc[Data.GroupedCategory=='Director'].Nominee.unique())
ActorActress=set(Data.loc[Data.GroupedCategory=='Actor/Actress'].Nominee.unique())
Both=Director.intersection(ActorActress)
Both


# In[ ]:


len(Both)


# There are 17 persons that were nominated to Actor/Actress and Director categories in Golden Globe Awards history
# 
# Let's see the first and last year of their nominations

# In[ ]:


for name in Both:
    Names=Data.loc[Data.Nominee == name].YearAward.reset_index()
    print(name,end=' ')
    print(Names.iloc[0,1],end='-')
    print(Names.iloc[-1,1])
    print()


# In[ ]:


# starting a wordcloud
NewList=list(Data.Nominee.loc[Data.GroupedCategory=='Actor/Actress'])


# In[ ]:


NomineeCloud=''
for name in NewList:
    name=re.sub('\s','',name)
    NomineeCloud+=name+' '


# In[ ]:


wordcloud = WordCloud(width = 1000, height = 800, 
                background_color ='white').generate(NomineeCloud)


# In[ ]:


plt.figure(figsize=(14,12))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()


# In[ ]:




