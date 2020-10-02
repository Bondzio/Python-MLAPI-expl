#!/usr/bin/env python
# coding: utf-8

# This notebook provide a basic model which can find comman movies for two users by taking the choices of each users.

# In[ ]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import re
nltk.download('stopwords')
from nltk.corpus import stopwords


# In[ ]:


df =pd.read_csv("../input/All_movies.csv")


# In[ ]:


df.head()


# In[ ]:


df.drop(columns=["Unnamed: 0","Rating"],inplace=True)


# In[ ]:


df1=df.copy()


# In[ ]:


df1["Actors"]=[x.lower().replace(' ','') for x in df1['Actors']]
df1["Director"]=[x.lower().replace(' ','') for x in df1['Director']]


# In[ ]:


df1["details"]=df1["Genre"]+" "+df1["Director"]+" "+df1["Actors"]+" "+df1["Description"]


# In[ ]:


df1.drop(columns=['Genre', 'Director', 'Actors',"Description"],inplace=True)


# In[ ]:


df1.head()


# In[ ]:


import string


# In[ ]:


df1["details"]=df1["details"].apply(lambda x: x.lower())


# In[ ]:


stopwords=set(stopwords.words('english'))


# In[ ]:


def clean(text):
  text1=" ".join([x for x in text.split() if x not in stopwords])
  text1=re.sub("[^a-zA-Z]+"," ",text1)
  text1=re.sub(' +', ' ', text1)
  text1 = re.sub(r"\s+[a-zA-Z]\s+", ' ', text1)
  text1 = re.sub(r'\s+', ' ', text1)
  return text1


# In[ ]:


df1["details"]=df1["details"].apply(lambda x: clean(x))


# In[ ]:


df1["details"][0]


# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()


# In[ ]:


from sklearn.metrics.pairwise import cosine_similarity
tfidf = tfidf_vectorizer.fit_transform(df1["details"])


# In[ ]:


import operator


# In[ ]:


movies=list(df["Title"])
#years=list(df["Year"])


# In[ ]:


movie_name=list(df1["Title"].to_numpy())


# In[ ]:


def similar_func(movie_in_func):                               

  similarity={}
  for f in range(len(movies)):
    if movie_in_func == movies[f] :
      index=f

  for f in range(len(movies)):
    if f!=index:
      score= cosine_similarity(tfidf[index], tfidf[f]).astype("float")[0][0]
      similarity[f]=score

  similarity_sort=sorted(similarity.items(), key=operator.itemgetter(1),reverse=True)
  return(similarity_sort)


# In[ ]:


def recommended_movies(movie_in):
  rating={}
  #movie_in=['Zindagi Na Milegi Dobara','Game Night']                                         #Input movies                                                                              #Input movies index

  for f in range(len(movies)):
    rating[f]=[] 

  for f in range(len(movie_in)):
    movie_list = similar_func(movie_in[f])

    for x in range(len(movie_list)):
      rating[movie_list[x][0]].append(movie_list[x][1])

    for y in range(len(movies)):
      if movie_in[f] == movies[y] :
        index=y
    
    rating[index].append(-100)

  rating_sum={}                                            
  for f in range(len(movies)):
    rating_sum[f]= []
  

  for f in range(len(movies)):
    a= rating[f]
    sum_=0
    for x in range(len(a)):
      sum_ = sum_ + a[x]
  
    rating_sum[f] = sum_

  #n=10
  similarity_sort=sorted(rating_sum.items(), key=operator.itemgetter(1),reverse=True)
  #print("You should watch these movies \n")
  #for x in range(n):
    #name=movies[similarity_sort[x][0]]
    #year=years[similarity_sort[x][0]]
    #score1=similarity_sort[x][1]
    #print("Movie name  " ,name,"       SCORE  ",score1)
    #print("------------------------------------------------------------------------------")
  return similarity_sort


# In[ ]:


movie_user_1=['Badla','Super 30','Article 15'] 
movie_user_2=['Article 15','Kesari','Andhadhun']  


# In[ ]:


user1=recommended_movies(movie_user_1)
user2=recommended_movies(movie_user_2)


# In[ ]:


u=3 #number of movies to be recommended


# In[ ]:


def similar_movie(similarity_sort,similarity_sort1):
  list_of_movies=[]
  list_of_movies_index=[]
  r=0
  i=0
  for f in range(10,558,20):
    for x in range(r,f):
      for y in range(r,f):
        if similarity_sort[x][0] == similarity_sort1[y][0] and i<u:
          #print(similarity_sort[x][0],similarity_sort1[y][0])
          list_of_movies_index.append(similarity_sort[x][0])
          i=i+1

    if i==3:
      break
    r=f
    
  list_of_movies = [movies[x] for x in list_of_movies_index]
  return list_of_movies


# In[ ]:


movies_list = similar_movie(user1,user2)


# In[ ]:


movies_list                                                             #These are the recommended movies for user1 and user2 


# In[ ]:




