#!/usr/bin/env python
# coding: utf-8

# # Data mining - IMDB 5000 movie dataset

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from wordcloud import WordCloud
from sklearn import ensemble
from sklearn.model_selection import train_test_split


# # Data presentation

# In[ ]:


data=pd.read_csv(r'../input/movie_metadata.csv')
data


# In[ ]:


data.info()


# In[ ]:


data.describe(include = [np.number]) ##Count,mean value... for numeric attributes


# In[ ]:


data.describe(include = ['O']) ## Count ,number of uniques and most frequent value of non-numeric


# In[ ]:


plt.style.use('seaborn')
data.hist(figsize=[20,20]) ##Histograms for numeric data
plt.show()


# # Data pre-process

# In[ ]:


duplicates=data.duplicated(subset='movie_title', keep=False)
sum(duplicates) ## Number of duplicates based on movie title


# In[ ]:


data=pd.read_csv('../input/movie_metadata.csv').drop_duplicates(subset='movie_title',keep='first') ##Remove duplicates,keep only first
nandata=data.isnull().sum().to_frame('Number of NaN') ## Number of missing (NaN) values
nandata


# Based on the histograms, most variables are left-skewed. So I fill NaN values with either median or mode.

# In[ ]:


##Fill NaN with median and mode
median=data[['num_critic_for_reviews','director_facebook_likes','actor_3_facebook_likes','actor_1_facebook_likes','num_user_for_reviews','gross','budget','actor_2_facebook_likes','movie_facebook_likes']].median()
data=data.fillna(median)
mode=data[['color','duration','facenumber_in_poster','language','country','content_rating','title_year','aspect_ratio']].mode().iloc[0]
data=data.fillna(mode)


# In[ ]:


##Float to int
data[['num_critic_for_reviews','director_facebook_likes','actor_3_facebook_likes','actor_1_facebook_likes','facenumber_in_poster','num_user_for_reviews','title_year','actor_2_facebook_likes']]=data[['num_critic_for_reviews','director_facebook_likes','actor_3_facebook_likes','actor_1_facebook_likes','facenumber_in_poster','num_user_for_reviews','title_year','actor_2_facebook_likes']].astype(int)


# In[ ]:


data=data.dropna() ## Remove whole indice if at least 1 NaN is seen
data


# # EDA

# In[ ]:


scatterdata=data.drop(data.columns[[0,1,5,6,9,10,11,13,14,15,16,17,19,20,21,23,24,26]], axis=1)


# In[ ]:


scatterdata=data[['movie_facebook_likes','title_year','budget','gross','director_facebook_likes',
                  'actor_1_facebook_likes','imdb_score','num_critic_for_reviews','num_user_for_reviews','num_voted_users']]

sns.set(style="ticks")
sns.pairplot(scatterdata)


# In[ ]:


cor=data.corr(method='pearson')## Correlation matrix with pearson method -1 negative , 1 positive correlation
cor.style.background_gradient(cmap='Purples')
#Deeper blue color highlights higher Pearson correlation


# # Features of movies that are popular with the public

# I cluster movies based on attributes that show social impact, such as movie_facebook_likes , num_user_for_reviews , num_critic_for_reviews and num_voted_users.

# In[ ]:


data['actors_facebook_likes']=data['actor_1_facebook_likes']+data['actor_2_facebook_likes']+data['actor_3_facebook_likes']
kmeansdata= data[['movie_facebook_likes','num_user_for_reviews','num_critic_for_reviews','num_voted_users']]


# In[ ]:


## Best silhouette score for given data
n_clusters = list(range(2, 11))
scores = []
for i in n_clusters:
    model = KMeans(n_clusters=i,random_state=0)
    model.fit(kmeansdata)
    results=model.labels_
    scores.append(silhouette_score(kmeansdata,results))


# In[ ]:


scores


# In[ ]:


##Kmeans-3 cluster
model = KMeans(n_clusters=3,random_state=0)
model.fit(kmeansdata)
results=model.labels_
score=silhouette_score(kmeansdata,results)
print("For n_clusters = 3 the average silhouette_score is :", score)
results=pd.Series(data=results,index=data.index)
results=results.to_frame("clusters")
data=data.join(results)


# In[ ]:


plt.ylabel('Population',fontsize=16)
plt.xlabel('Clusters',fontsize=16)
data['clusters'].hist(figsize=(10,5))
plt.show()


# In[ ]:


plt.style.use('seaborn')
data[['actors_facebook_likes','movie_facebook_likes','director_facebook_likes']].groupby(data['clusters']).mean().plot.bar(stacked=False,figsize=(12,7))
plt.xlabel('Clusters',fontsize=15)
plt.legend(loc=0, prop={'size': 15})
plt.title('Mean values of movie,actors and director facebook likes per cluster',fontsize=18)
plt.show()


# Movies cluster with most Facebook likes also has high average actors Facebook likes. We can assume that, to a high extent, for the audience to like a film, the actors must first be liked and then the director.

# In[ ]:


plt.style.use('seaborn')
data[['budget','gross']].groupby(data['clusters']).mean().plot.bar(stacked=False,figsize=(10,6))
plt.legend(loc=0, prop={'size': 14})
plt.xlabel('Clusters',fontsize=15)
plt.title('Mean value of budget and gross revenue of movies per cluster',fontsize=18)
plt.show()


# Cluster 0 where movies have a low number of Facebook likes, we also see that budget is equal to gross revenue. So likes on Facebook definitely play a part in the financial success of each movie.

# In[ ]:


data[['num_user_for_reviews','num_critic_for_reviews']].groupby(data['clusters']).mean().plot.bar(stacked=False,figsize=(10,7))
plt.legend(loc=0, prop={'size': 15})
plt.xlabel('Clusters',fontsize=15)
plt.title('Mean number of users and critics that reviewed the movies per cluster',fontsize=18)
plt.show()


# In[ ]:


##Sort movies based on facebook_likes and get top 10
sorted_fl=data.sort_values(by="movie_facebook_likes",ascending=False)
top10fl=sorted_fl.head(10)
top10fl[['movie_facebook_likes']].groupby(top10fl['movie_title']).sum().plot.bar(stacked=True,figsize=(11,6))
plt.xticks(rotation=70,fontsize=15)
plt.legend(loc=0, prop={'size': 14})
plt.title('Top 10 movies with most facebook likes',fontsize=18)
plt.show()


# In[ ]:


keywords=sorted_fl["plot_keywords"].head(200)
keywords=pd.Series('/'.join(keywords).lower().split("|"))


# In[ ]:


def make_cloud(cloud_data):
    cloud_data=cloud_data.str.lower()
    cloud_list=list(cloud_data) 
    unique_string=(" ").join(cloud_list)
    wordcloud = WordCloud(width = 1000, height = 500,max_words=100).generate(unique_string)
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()    


# # $ Plot $ keywords $ of $ top $ 200 $ movies $ with $ most $ facebook $ likes

# In[ ]:


make_cloud(keywords)


# In[ ]:


genres=sorted_fl["genres"].head(200)
count=pd.Series('/'.join(genres).lower().split("|")).value_counts()[:10]
count.to_frame('Count')


# In[ ]:


plot2=count.plot(x='Genres',kind='bar',color='purple',figsize=(11,5))
plt.title('Most common genres of the top 200 movies with most facebook likes',fontsize=18)
plt.xticks(rotation=70,fontsize=15)
plt.show()


# In[ ]:


content=sorted_fl["content_rating"].head(200)
count=pd.Series(' '.join(content).lower().split(" ")).value_counts()[:5]
print("Most common ratings of top 150 movies with most facebook likes are:\n",count.to_frame('Count'))


# So we see that the movies that most people like are either adventure or drama, they have keywords such as future/relationship/battle/female/drug/war, etc., and from these the most are marked with pg-13 (Parental Guidance - Some material may be inappropriate for children under 13).

# # Gradient Boosting Regression to predict imdb score

# In[ ]:


x=data[['movie_facebook_likes','title_year','budget','gross','director_facebook_likes','actors_facebook_likes']]
y=data['imdb_score']


# In[ ]:


x_train, x_test, y_train, y_test = train_test_split(x, y,test_size=0.4,random_state=13) ##Split train and test set. Test set is 40% of whole data


# We create the model with
# 
# + **Number of trees** (weak learners) = 200
# + **Function to minimize errors** = Minimal squares
# + **Learning rate** , ie the rate at which the contribution of each tree is reduced= 3%
# + **Maximum height** of trees= 4

# In[ ]:


n_trees=200
model=ensemble.GradientBoostingRegressor(loss='ls',learning_rate=0.03,n_estimators=n_trees,max_depth=4)
model.fit(x_train,y_train)


# In[ ]:


pred=model.predict(x_test)
error=model.loss_(y_test,pred) ##Loss function== Mean square error
print("MSE:%.3f" % error)


# In[ ]:


test_error=[]
for i,pred in enumerate(model.staged_predict(x_test)):##staged_predict=predict at each stage 
    test_error.append(model.loss_(y_test,pred))##model.loss(y_test,pred)=mse(y_test,pred)


# In[ ]:


plt.figure(figsize=(12,7))
plt.plot(list(range(1,n_trees+1)),model.train_score_,'b-',label='Train set error') ## model.train_score_=deviance(=loss) of model at each stage
plt.plot(list(range(1,n_trees+1)),test_error,'r-',label='Test set error')
plt.legend(loc='upper right',fontsize=15)
plt.xlabel('Trees',fontsize=15)
plt.ylabel('Error', fontsize=15)
plt.show()


# We see that the error for the train and test set follows a similar behavior, so we have created a pretty good model. After the 200 trees, we would see that the train error will continue to decrease while the test error will remain stable. This would mean that the model is overfitting to the train set, reducing the error for train set but not getting a smaller error in the test set as well.

# In[ ]:


feature_importance=model.feature_importances_
sorted_importance = np.argsort(feature_importance)
pos=np.arange(len(sorted_importance))
plt.figure(figsize=(12,5))
plt.barh(pos, feature_importance[sorted_importance],align='center')
plt.yticks(pos, x.columns[sorted_importance],fontsize=15)
plt.title('Feature Importance ',fontsize=18)
plt.show()


# Calculating each feature importance in defining the imdb score, we see that movie facebook likes is the attribute that has the higest importance in defining an imdb score. Suprisingly, the title year ie the year the movie was released is also an important factor.
