#!/usr/bin/env python
# coding: utf-8

# # 1. Introduction & EDA
# 
# In this module to find the recommended professionals to answer some questions, we will use 'questions.csv','answers.csv', 'professionals.csv', 'answers_score.csv', 'questions_score.csv', 'tag_users.csv', 'tag_questions.csv' and 'tags.csv' files from "Data Science for Good: CareerVillage.org
# Match career advice questions with professionals in the field".
# 
# During the Exploratory Data Analysis (EDA) of these files, in 'questions.csv' file, we found some question having HTML tags within its text body. Hashtag also attached as well. We also can find some of the questions are placed in questions_title rather than in questions_body column and vice versa. Some of the questions also having URL links within its text.
# 
# 
# 

# In[1]:


import pandas as pd
import operator
import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.externals import joblib
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt



#Load files and datasets
answer=pd.read_csv('../input/answers.csv')
professional=pd.read_csv('../input/professionals.csv')
tags=pd.read_csv('../input/tags.csv')
question_score=pd.read_csv('../input/question_scores.csv')
answer_score=pd.read_csv('../input/answer_scores.csv')
questi=pd.read_csv('../input/questions.csv')
tag_question=pd.read_csv('../input/tag_questions.csv')
tag_user=pd.read_csv('../input/tag_users.csv')


# In[2]:


questi[questi['questions_body']=='<p>I am a sophomore in Boston and I am not sure what I want to do yet. I really think I want to be a pediatric nurse but I am not sure if I will want to go further into the health and medicine field if I really like it. </p>']


# In[3]:


questi[questi['questions_body'].str.contains('http://www.typeoflawyer.com/different-types-of-law-careers/')]


# In[4]:


questi.isnull().sum() 


# # 2. Pre-Processing Data
# 
# Before clustering and labeling process, we need to merge several tables into 'questions.csv'
# 

# In[5]:


#Rename the name of column in 'tag_users.csv' table to be merged with 'tags.csv'
tag_user=tag_user.rename(index=str, columns={'tag_users_tag_id':'tags_tag_id'})
tag_professional=tag_user.merge(tags, how='left', on='tags_tag_id')

#Merging the tag_professional for question with 'professionals.csv'
tag_professional=tag_professional.rename(index=str, columns={'tag_users_user_id':'professionals_id'})
final_professional=professional.merge(tag_professional, how='left', on='professionals_id')

#Rename the name of column in 'Professionals.csv' table to be merged with 'answers.csv'
final_professional=final_professional.rename(index=str, columns={'professionals_id':'answers_author_id'})
answer_prof_merged=answer.merge(final_professional, how='left', on='answers_author_id')

#Rename the name of column in 'answer_score.csv' table to be merged with 'answer_prof_merged'
answer_score1=answer_score.rename(index=str, columns={'id':'answers_id'})
answer_prof_merged=answer_prof_merged.merge(answer_score1, how='left', on='answers_id')

#Rename the name of column in 'question_scores.csv' table to be merged with 'questions.csv'
question_score1=question_score.rename(index=str, columns={'id':'questions_id'})
questi=questi.merge(question_score1, how='left', on='questions_id')

#Rename the name of column in 'tag_questions.csv' table to be merged with 'tags.csv'
tag_question=tag_question.rename(index=str, columns={'tag_questions_question_id':'questions_id'})
tag1=tags.rename(index=str, columns={'tags_tag_id':'tag_questions_tag_id'})

final_tag=tag_question.merge(tag1, how='left', on='tag_questions_tag_id')


#Merging the tags for question with 'questions.csv'
questi1=questi.merge(final_tag, how='left', on='questions_id')


# After that, we need to clean up every question text from HTML tags, hashtag using "cleaned_list" function. We also need to remove all URL links. The main purpose of this process is to provide good quality text data before continuing to tokenization and TFIDF vectorizer.
# 
# 
# In "merged_body_and_title" function, it will merge between question text body and question text title together in "merged_question" column, to avoid any question body that is misplaced in title column and vice versa.

# In[6]:


import nltk

temporary1=[]
temporary2=[]
end=[]
question_new_list=[]

#Cleaned Texts from HTML tags, URL, Hashtag, and then translating all of them to english as the default 
def cleaned_list(file,name):
    text_=list(str(x) for x in file[name])
    question_new_list=[]
    for i in text_:
        cleaned_str=BeautifulSoup(i)
        cleaned_text=cleaned_str.get_text()
        result= re.sub(r"http\S+", "", cleaned_text)
        result0=re.sub("(\\d|\\W)+"," ",result)
        result1=result0.replace('#','')
        question_new_list.append(result1)
    return question_new_list
                   
#Some of questions are posted as title rather than body, so we merged it both of them as 'merged text'
def merged_body_and_title(file):
    bodies= cleaned_list(file,'questions_body')
    titles= cleaned_list(file,'questions_title')
    for i in range(0, len(titles)):
        nltk_tokens_body = nltk.word_tokenize(bodies[i])
        nltk_tokens_title = nltk.word_tokenize(titles[i])
        for f in nltk_tokens_title :
            temporary1.append(f)
            t=' '.join(temporary1)
        for v in nltk_tokens_body :
            temporary2.append(v)
            t1=' '.join(temporary2)
            t3=t+'.'+t1
        end.append(t3)
        temporary1.clear()
        temporary2.clear()
    return end

questi1['merged_question']=merged_body_and_title(questi1)
answer_prof_merged['merged_question']=cleaned_list(answer_prof_merged,'answers_body')


# # 3. Data Processing
# 
# For clustering, we will use KMeans to get the main top words per cluster. This clustering will be labeled on each question in 'questi1' table. But before that, we need to find the optimal number of the cluster as the input for our KMeans. That's why we will do "Elbow Method" to find optimal k.
# 
# For the experiment, let's take range from 80 to 200 number of clusters.

# In[7]:


non_nan_list=list(str(x) for x in questi1['merged_question'].drop_duplicates())
answer_list=list(str(x) for x in answer_prof_merged['answers_body'])

tfidf=TfidfVectorizer(stop_words='english')
X_idf = tfidf.fit_transform(non_nan_list)


# In[8]:


# Sum_of_squared_distances = []
# K = range(80,200)
# for k in K:
#     print(k)
#     model = KMeans(n_clusters=k)
#     km=model.fit(X_idf)
#     Sum_of_squared_distances.append(km.inertia_)


# In[9]:


# plt.figure(figsize=(80,80))
# plt.plot(K, Sum_of_squared_distances, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Sum_of_squared_distances')
# plt.title('Elbow Method For Optimal k')
# plt.show()


# The result shows that the 'elbow' is created between 100 to 150 number of clusters. So, we will take  138 as the optimal k for our KMeans's input.

# # 4. KMeans Process and TFIDF
# 
# Exploring the top tearms for each cluster using this method:

# In[10]:



true_k =138
model = KMeans(n_clusters=true_k, init='k-means++',max_iter=300, n_init=10)
model.fit(X_idf)
    
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = tfidf.get_feature_names()

# print(order_centroids)
for i in range(true_k):
    print("Cluster %d:" % i),
    for t in order_centroids[i, :10]:
        print(' %s' % terms[t]),
print


# In[11]:



true_k =138
model = KMeans(n_clusters=true_k, init='k-means++',max_iter=300, n_init=10)
model.fit(X_idf)
    
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = tfidf.get_feature_names()

# print(order_centroids)
for i in range(true_k):
    print("Cluster %d:" % i),
    for t in order_centroids[i, :10]:
        print(' %s' % terms[t]),
print


# We also check the similarity between the question text as the input with its question in "questi1" to support the accuracy of KMeans clustering using "similarity" function.

# In[12]:


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
 
def similarity(X_list, y_list):
    X = tfidf.transform(X_list)
    y=tfidf.transform(y_list)
    
    d=cosine_similarity(X, y)
    return d
 


# After the KMeans clustering, now we can labeling all question in 'questi1' dataframe.

# In[13]:


def labeling(name_list):
    clustering=[]
    for i in name_list:
        Y = tfidf.transform([i])
        prediction = model.predict(Y)
        for e in prediction:
            clustering.append(e)
    return clustering


# In[14]:


full_list_question=list(str(x) for x in questi1['merged_question'])
questi1['label']=labeling(full_list_question)


# Now, we can merge answer dataframe with questi1 dataframe that has been labeled in "answer_and_question". 

# In[15]:


answer2=answer_prof_merged.rename(index=str, columns={'answers_question_id':'questions_id'})

answer_and_question=answer2.merge(questi1,how='left', on='questions_id')

answer_and_question.head()


# In[16]:


answer_and_question.isnull().sum()


# # 5. Finding How Fast The Response Comes From Professional
# 
# In order to get this data, we need to get interval time between the date of question first posted and the date of that questions answered.

# In[17]:


from datetime import datetime
interval=[]
for i in range (0, len(answer_and_question)):
    answer_date=datetime.strptime(str(answer_and_question['answers_date_added'][i]),'%Y-%m-%d %H:%M:%S UTC+0000')
    sent_date=datetime.strptime(str(answer_and_question['questions_date_added'][i]),'%Y-%m-%d %H:%M:%S UTC+0000')
    diff= (answer_date-sent_date).days
    interval.append(diff)
answer_and_question['interval']=interval


# After we got the interval days of response, we can find mean of response time for each professional using aggregate() and groupby() function. The smaller mean indicates faster that professional in answering a question.

# In[18]:


answer_recommend=answer_and_question.groupby('answers_author_id').agg({'interval':'mean'})
answer_final_end=answer_and_question.merge(answer_recommend, how='left', on='answers_author_id')


# In[19]:


answer_recommend.head()


# # 6. Additional: How to get reccomended professional who hasn't yet answered any question?
# Sometimes, even the professional in 'professionals.csv' hasn't been answered any question, we need to send them a relevant question to open more chance for that question to be answered. In order to do this, we will get any tags name that related with 'label' column. Based on those tags, we can search for other professional in 'professional.csv'.

# In[20]:


def not_answerred_prof(label):
    label=answer_and_question.loc[answer_and_question['label'].isin(label)]
    list_tags=list(str(x) for x in label['tags_tag_name_x'].drop_duplicates())
    for i in list_tags:
        if i is not np.nan:
            final=final_professional.loc[final_professional['tags_tag_name'].isin(list_tags)]
            final1=final[['answers_author_id','tags_tag_name']].drop_duplicates(subset='answers_author_id')
    return final1


# # 7. Presenting The Reccomended Professional
# Using its label to filter specific professional and sorted it based on 'similarity_score' to present its final result. We present The Top 10 recommended professionals to answer.

# In[21]:




def find_the_professional(text_list):
    list_similarity=[]
    label_list=labeling(text_list)
    for i in range(0,len(text_list)):
        df=answer_final_end.loc[answer_final_end['label'].isin(label_list)]
        sim_score=similarity(text_list,list(str(x) for x in df['merged_question_y']))
        for b in sim_score:
            for c in b:
                list_similarity.append(c)
        df['similarity_score']=list_similarity
        df1=df.sort_values(by=['similarity_score'], ascending=False)
        professional_result=df1[['answers_author_id','interval_y', 'similarity_score', 'score_x']].drop_duplicates(subset='answers_author_id')
        professional_result=professional_result.rename(columns={'interval_y':'interval mean', 'score_x':'heart'})
        additional_prof=not_answerred_prof(label_list)
        print('Label number:',label_list)
        print('\033[1m','Top 10 List of Professionals For This Question:',text_list[i],'\033[1m')
        return professional_result[0:10], additional_prof[0:10]



# In[22]:


def final_recommendation(text_list):
    a,b=find_the_professional(text_list)
    display(a)
    print('\033[1m','--------------------------------------------------------------------------------------------------------------','\033[1m')
    print('\033[1m','Top 10 Additional Professionals:','\033[1m')
    display(b)


# In[23]:


final_recommendation(['how to get scholarship ?'])

