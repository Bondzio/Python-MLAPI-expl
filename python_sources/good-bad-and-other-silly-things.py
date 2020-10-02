#!/usr/bin/env python
# coding: utf-8

# 
# 
#  ![alt-text](https://www.filmtv.it/public/images/logo-filmtv.png "FilmTV.it")

# # LEGENDA
# 
# - [CHAPTER 0: libraries](#a0)
# - [CHAPTER 1: the dataframe](#a1)
# - [CHAPTER 2: a first look](#a2)
# - [CHAPTER 3: the decade](#a3)
# - [CHAPTER 4: the genres](#a4)
# - [CHAPTER 5: who is a GOOD boy?](#a5)

# # CHAPTER 0: libraries <a name="a0"></a>

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import math

import os
from subprocess import check_output

import re
print("Setup Complete")


# # CHAPTER 1: the dataframe <a name="a1"></a>

# In[ ]:


path_data = '../input/FilmTV Dataset - ENG.csv'
film_data = pd.read_csv(path_data, index_col='filmtv_ID')
film_data.head()


# In[ ]:


film_data.describe()


# # CHAPTER 2: a first look <a name="a2"></a>

# In[ ]:


plt.figure(figsize=(15,10))
plt.title('Film TV by the year', size=20)
sns.distplot(film_data.year, kde=False, color=plt.cm.cool(0.99))
plt.ylabel('nr. of Movie', size=15)
plt.xlabel('year',size=15)
plt.axis([1911, 2018, 0, 2800])
plt.xticks(np.arange(1910, 2018, step=5),rotation=45, ha='right')
plt.show()


# In[ ]:


plt.figure(figsize=(15,10))
plt.title('Trend of production', size=20)
sns.distplot(film_data.year, kde=True, color=plt.cm.cool(0),bins=7)
plt.ylabel('nr. of Movie', size=15)
plt.xlabel('year',size=15)
plt.axis([1911, 2010, 0, 0.03])
plt.xticks(np.arange(1910, 2015, step=5),rotation=45, ha='right')
plt.show()


# **A NOTE:** the production of content good for this media start, obviously, from the beginnig of th 20th century and keeps growing but non linearly. We can assume the television as an 'everyday object' since '50, but the production does not seem to be growing in those years. We have to wait after 1990, in the middle of Blockbuster's period to have a great increase of the production. According to dataset description ther'is 50% of the production after 1995.

# In[ ]:


sns.jointplot(x=film_data['year'], y=film_data['avg_vote'], color = plt.cm.cool(0.99),
              kind="kde", cmap="cool").fig.set_size_inches(10,10,)


# In[ ]:


film_data['genre'].fillna('Unknow',inplace=True)
film_data['genre'].unique()


# In[ ]:


plt.figure(figsize=(15,10))
plt.title('Film TV by the genre', size=20)
sns.barplot(x=film_data.genre.value_counts().index, y=film_data.genre.value_counts(), palette="cool")
plt.ylabel('nr. of Movie', size=15)
plt.xlabel('genre',size=15)
plt.xticks(rotation=45, ha='right')
plt.show()


# **NOTE: ** we assume as GOOD rating every avg_vote > 6.0. (the meaning is 5.8)

# In[ ]:


list_GOOD_or_BAD = []
for element in film_data['avg_vote']:
    if element > 6:
        list_GOOD_or_BAD.append('GOOD')
    else:
        list_GOOD_or_BAD.append('BAD')
film_data['rating'] = list_GOOD_or_BAD
film_data.head()


# In[ ]:


plt.figure(figsize=(15,10))
sns.scatterplot(x=film_data['year'], y=film_data['avg_vote'], hue=film_data['rating'], 
                palette=[plt.cm.cool(0), plt.cm.cool(0.99)])
plt.show()


# In[ ]:


sns.lmplot(x='year', y='avg_vote', hue='rating',
           data=film_data,  palette=[plt.cm.cool(0), plt.cm.cool(0.99)]).fig.set_size_inches(10,10,)


# In[ ]:


sns.pairplot(film_data, hue='rating', height=5, palette='cool')


# **NOTE:** across the year the overall quality of the production it seems to getting worse. Get a closer look with the next chapter.

# # CHAPTER 3: the decade <a name="a3"></a>

# In[ ]:


decade = []
for element in film_data['year']:
    if element < 1920:
        decade.append(1910)
    else:
        decade.append(int((math.ceil(element / 10.0)) * 10)-10)
abs_vote = []
for element in film_data['avg_vote']:
    abs_vote.append(int(element))
dz={'1910':0, '1920':0, '1930':0, '1940':0, '1950':0, '1960':0, '1970':0, '1980':0, '1990':0, '2000':0, '2010':0}
for element in dz:
    dz[element]={'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
c=0
while c<len(decade):
    dz[str(decade[c])][str(abs_vote[c])]+=1
    c+=1
df_decade=pd.DataFrame(dz)
df_decade=df_decade.replace(0, np.nan)
    


# In[ ]:


df_decade


# In[ ]:


plt.figure(figsize=(15,12))
plt.title("Heatmap of absolute quantity avg_vote for decade")
sns.heatmap(data=df_decade, annot=True, cmap='cool')
plt.xlabel("Decade")
plt.ylabel("avg_vote")
plt.show()


# In[ ]:


df_decade.sum(axis = 0, skipna = True)


# In[ ]:


df_decade_prop=df_decade.copy()
df_decade_prop['1910']=df_decade_prop['1910']/91
df_decade_prop['1920']=df_decade_prop['1920']/326
df_decade_prop['1930']=df_decade_prop['1930']/1206
df_decade_prop['1940']=df_decade_prop['1940']/1809
df_decade_prop['1950']=df_decade_prop['1950']/3206
df_decade_prop['1960']=df_decade_prop['1960']/3969
df_decade_prop['1970']=df_decade_prop['1970']/4067
df_decade_prop['1980']=df_decade_prop['1980']/5277
df_decade_prop['1990']=df_decade_prop['1990']/8306
df_decade_prop['2000']=df_decade_prop['2000']/9413
df_decade_prop['2010']=df_decade_prop['2010']/9237
df_decade_prop=df_decade_prop.replace(0, np.nan)
df_decade_prop


# In[ ]:


plt.figure(figsize=(15,12))
plt.title("Heatmap of proportional avg_vote for decade")
sns.heatmap(data=df_decade_prop, annot=True, cmap='cool')
plt.xlabel("Decade")
plt.ylabel("avg_vote")
plt.show()


# **NOTE:** the old movie are really better or is there some bias? I think the answer is: BIAS. Ther'are a lot of old movie that are re-evaluated by critics and public, and other new movie that need time to be accepted.

# # CHAPTER 4: the genres <a name="a4"></a>

# In[ ]:


genre_value=pd.crosstab(film_data.genre,film_data.rating)
genre_value


# In[ ]:


group_names=film_data.genre.value_counts().head(10).index
group_size=film_data['genre'].value_counts().head(10)
subgroup_names=['GOOD','BAD','GOOD','BAD','GOOD','BAD','GOOD','BAD','GOOD','BAD',
               'GOOD','BAD','GOOD','BAD','GOOD','BAD','GOOD','BAD','GOOD','BAD']
sz=[]
for element in group_names:
    sz.append(genre_value.loc[element]['GOOD'])
    sz.append(genre_value.loc[element]['BAD'])
subgroup_size=sz
 
# Create colors
a, b=[plt.cm.cool, 'grey']

# First Ring (outside)
fig, ax = plt.subplots()
ax.axis('equal')
mypie, _ = ax.pie(group_size, radius=4, labels=group_names, 
                  colors=[a(0.05),a(0.1),a(0.15),a(0.2),a(0.25),a(0.3),a(0.35),a(0.4),a(0.45),a(0.5)] )
plt.setp( mypie, width=1, edgecolor='white')
 
# Second Ring (Inside)
mypie2, _ = ax.pie(subgroup_size, radius=3, labels=subgroup_names, labeldistance=0.83, 
                   colors=[a(0.55),b,a(0.60),b,a(0.65),b,a(0.70),b,a(0.75),b,
                           a(0.80),b,a(0.85),b,a(0.90),b,a(0.95),b,a(1.00),b,])
plt.setp( mypie2, width=0.4, edgecolor='white')
plt.margins(0,0)
 
# show it
plt.show()


# **NOTE:** it has sense make so many Comedy, Thriller, Action, Horror, Adventure or Fantasy movie if they have so many BAD ratings? Maybe the meaning is that a BAD rating is not connected with bad revenues or the people that post on filmtv.it watch a lot of BAD movies and i like to watch it and say how they BAD are. 

# # CHAPTER 5: who is a GOOD boy? <a name="a5"></a>

# In[ ]:


film_data.actors.fillna('unknow', inplace=True)
film_data.actors.replace('', 'unknow', inplace=True)
list_actors=[]
for element in film_data.actors:
    tmp=element.split(', ')
    list_actors.append(tmp)
film_data.director.fillna('unknow', inplace=True)
film_data.director.replace('', 'unknow', inplace=True)
list_directors=[]
for element in film_data.director:
    tmp=element.split(', ')
    list_directors.append(tmp)


# In[ ]:


n = film_data['actors']
film_data=film_data.drop(['actors'], axis=1)
film_data['actors'] = list_actors
film_data['directors'] = list_directors
film_data.head()


# In[ ]:


all_dir=[]
for element in film_data['directors']:
    for name in element:
        if name != '':
            all_dir.append(name)
directors_names=set(all_dir)
all_act=[]
for element in film_data['actors']:
    for name in element:
        if name != '':
            all_act.append(name)
actors_names=set(all_act)


# In[ ]:


diz_directors={}
for element in all_dir:
    if element != 'unknow':
        if element in diz_directors:
            diz_directors[element]+=1
        else:
            diz_directors[element]=1
diz_actors={}
for element in all_act:
    if element != 'unknow':
        if element in diz_actors:
            diz_actors[element]+=1
        else:
            diz_actors[element]=1


# In[ ]:


diz_directors_ord=sorted(diz_directors.items(), key=lambda kv: kv[1], reverse=True)
diz_actors_ord=sorted(diz_actors.items(), key=lambda kv: kv[1], reverse=True)


# In[ ]:


top_dir_x=[]
for element in diz_directors_ord:
    top_dir_x.append(element[0])
top_dir_y=[]
for element in diz_directors_ord:
    top_dir_y.append(element[1])
    
plt.figure(figsize=(15,10))
plt.title('20 Most active directors', size=20)
sns.barplot(x=top_dir_x[:20], y=top_dir_y[:20], palette="cool")
plt.ylabel('nr of movie', size=15)
plt.xlabel('directors',size=15)
plt.xticks(rotation=45, ha='right')
plt.show()


# In[ ]:


top_act_x=[]
for element in diz_actors_ord:
    top_act_x.append(element[0])
top_act_y=[]
for element in diz_actors_ord:
    top_act_y.append(element[1])
    
plt.figure(figsize=(15,10))
plt.title('20 Most active actors', size=20)
sns.barplot(x=top_act_x[:20], y=top_act_y[:20], palette="cool")
plt.ylabel('nr of movie', size=15)
plt.xlabel('actors',size=15)
plt.xticks(rotation=45, ha='right')
plt.show()


# In[ ]:


number_of_movie=30
dict_direct_avg={}
for element in film_data.index:
    for element2 in film_data['directors'][element]:
        if element2 in diz_directors:
            if diz_directors[element2]>=number_of_movie:
                if film_data['rating'][element]=='GOOD':
                    if element2 in dict_direct_avg:
                        dict_direct_avg[element2]+=1
                    else:
                        dict_direct_avg[element2]=1
                else:
                    if element2 in dict_direct_avg:
                        dict_direct_avg[element2]-=1
                    else:
                        dict_direct_avg[element2]=-1
dict_direct_avg2={}
for element in dict_direct_avg:
    dict_direct_avg2[element]=(dict_direct_avg[element])/(diz_directors[element])
dict_direct_avg_order=sorted(dict_direct_avg2.items(), key=lambda xc:xc[1], reverse=True)

dict_act_avg={}
for element in film_data.index:
    for element2 in film_data['actors'][element]:
        if element2 in diz_actors:
            if diz_actors[element2]>=number_of_movie:
                if film_data['rating'][element]=='GOOD':
                    if element2 in dict_act_avg:
                        dict_act_avg[element2]+=1
                    else:
                        dict_act_avg[element2]=1
                else:
                    if element2 in dict_act_avg:
                        dict_act_avg[element2]-=1
                    else:
                        dict_act_avg[element2]=-1
dict_act_avg2={}
for element in dict_act_avg:
    dict_act_avg2[element]=(dict_act_avg[element])/(diz_actors[element])
dict_act_avg_order=sorted(dict_act_avg2.items(), key=lambda xc:xc[1], reverse=True)
   


# In[ ]:


print('20 most GOOD directors according the average with at least 30 movies shot')
top_dir_x=[]
for element in dict_direct_avg_order:
    top_dir_x.append(element[0])
top_dir_y=[]
for element in dict_direct_avg_order:
    top_dir_y.append(element[1])
    
plt.figure(figsize=(15,10))
plt.title('20 Most GOOD directors', size=20)
sns.barplot(x=top_dir_x[:20], y=top_dir_y[:20], palette="winter")
plt.ylabel('% of GOOD ratings', size=15)
plt.xlabel('directors',size=15)
plt.xticks(rotation=45, ha='right')
plt.show()


# In[ ]:


print('20 most BAD directors according the average with at least 30 movies shot')
top_dir_x=[]
for element in dict_direct_avg_order:
    top_dir_x.append(element[0])
top_dir_y=[]
for element in dict_direct_avg_order:
    top_dir_y.append(-(element[1]))
    
plt.figure(figsize=(15,10))
plt.title('20 Most BAD directors', size=20)
sns.barplot(x=top_dir_x[-20:], y=top_dir_y[-20:], palette="inferno")
plt.ylabel('% of BAD ratings', size=15)
plt.xlabel('directors',size=15)
plt.xticks(rotation=45, ha='right')
plt.show()


# In[ ]:


print('20 most GOOD actors according the average with at least 30 movies shot')
top_dir_x=[]
for element in dict_act_avg_order:
    top_dir_x.append(element[0])
top_dir_y=[]
for element in dict_act_avg_order:
    top_dir_y.append(element[1])
    
plt.figure(figsize=(15,10))
plt.title('20 Most GOOD actors', size=20)
sns.barplot(x=top_dir_x[:20], y=top_dir_y[:20], palette="winter")
plt.ylabel('% of GOOD ratings', size=15)
plt.xlabel('actors',size=15)
plt.xticks(rotation=45, ha='right')
plt.show()


# In[ ]:


print('20 most BAD actors according the average with at least 30 movies shot')
top_dir_x=[]
for element in dict_act_avg_order:
    top_dir_x.append(element[0])
top_dir_y=[]
for element in dict_act_avg_order:
    top_dir_y.append(-(element[1]))
    
plt.figure(figsize=(15,10))
plt.title('20 Most BAD actors', size=20)
sns.barplot(x=top_dir_x[-20:], y=top_dir_y[-20:], palette="inferno")
plt.ylabel('% of BAD ratings', size=15)
plt.xlabel('actors',size=15)
plt.xticks(rotation=45, ha='right')
plt.show()


# **A NOTE FOR ME:** actually my some of my favorite actors..

# In[ ]:




