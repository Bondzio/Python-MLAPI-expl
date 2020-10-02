#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np # linear algebra
import matplotlib.pyplot as plt
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
get_ipython().run_line_magic('matplotlib', 'inline')

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

print ("its working \n\n");
# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv("/kaggle/input/RePORTER_PRJABS_C_FY2019_053.csv",encoding = 'unicode_escape')
data.head()
 


# In[ ]:


data.info()


# In[ ]:


desc = data['ABSTRACT_TEXT'].values
#print (desc);


# In[ ]:


punc = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
stop_words = text.ENGLISH_STOP_WORDS.union(punc)
vectorizer = TfidfVectorizer(stop_words = stop_words)
X = vectorizer.fit_transform(desc)


# In[ ]:


word_features = vectorizer.get_feature_names()
print(len(word_features))


# In[ ]:


from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

#samples = ["This is a test","a very good test","some more text"]
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(desc)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
neigh = NearestNeighbors(n_neighbors=5, radius=1.0, n_jobs=-1) 
neigh.fit(X_train_tfidf)

test=["The PDX Core is the epicenter of the WU-PDTC","shock causing of"]
X_test_counts = count_vect.transform(test)

X_test_tfidf = tfidf_transformer.transform(X_test_counts)

res = neigh.kneighbors(X_test_tfidf, return_distance=True)

print (res);


# In[ ]:


print(word_features[5000:5100])


# In[ ]:


stemmer = SnowballStemmer('english')
tokenizer = RegexpTokenizer(r'[a-zA-Z\']+')

def tokenize(text):
    return [stemmer.stem(word) for word in tokenizer.tokenize(text.lower())]


# In[ ]:


vectorizer2 = TfidfVectorizer(stop_words = stop_words, tokenizer = tokenize)
X2 = vectorizer2.fit_transform(desc)
word_features2 = vectorizer2.get_feature_names()
print(len(word_features2))
print(word_features2[:50]) 


# In[ ]:


vectorizer3 = TfidfVectorizer(stop_words = stop_words, tokenizer = tokenize, max_features = 1000)
X3 = vectorizer3.fit_transform(desc)
words = vectorizer3.get_feature_names()
print(len(words))
print(words[:50]) 


# In[ ]:


from sklearn.cluster import KMeans
wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0)
    kmeans.fit(X3)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,11),wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.savefig('elbow.png')
plt.show()


# In[ ]:


kmeans = KMeans(n_clusters = 3, n_init = 20, n_jobs = 1) # n_init(number of iterations for clsutering) n_jobs(number of cpu cores to use)
kmeans.fit(X3)
# We look at 3 the clusters generated by k-means.
common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))


# In[ ]:


kmeans = KMeans(n_clusters = 5, n_init = 20, n_jobs = 1)
kmeans.fit(X3)
# We look at 5 the clusters generated by k-means.
common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))


# In[ ]:


kmeans = KMeans(n_clusters = 8, n_init = 20, n_jobs = 1)
kmeans.fit(X3)
# Finally, we look at 8 the clusters generated by k-means.
common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))


# In[ ]:


centroids = kmeans.cluster_centers_

plt.scatter(centroids[:, 0], centroids[:, 1], marker='+', s=80, linewidths=55, cmap='rainbow')
plt.show()


# In[ ]:


from sklearn.manifold import TSNE
centroids = kmeans.cluster_centers_

tsne_init = 'pca'  # could also be 'random'
tsne_perplexity = 20.0
tsne_early_exaggeration = 4.0
tsne_learning_rate = 1000
random_state = 1
model = TSNE(n_components=2, random_state=random_state, init=tsne_init, perplexity=tsne_perplexity,
         early_exaggeration=tsne_early_exaggeration, learning_rate=tsne_learning_rate)

transformed_centroids = model.fit_transform(centroids)
print (transformed_centroids)
plt.scatter(transformed_centroids[:, 0], transformed_centroids[:, 1], marker='x')
plt.show()


# In[ ]:


kmeans = KMeans(n_clusters = 10, n_init = 20, n_jobs = 1)
kmeans.fit(X3)
# Finally, we look at 10 the clusters generated by k-means.
common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))


# In[ ]:


from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer, TfidfTransformer
  
samples = ["This is a test","a very good test","some more text"]
count_vect = CountVectorizer(stop_word="english")
X_train_counts = count_vect.fit_transform(samples)
print (X_train_counts) 

tfidf_transformer = TfidfTransformer()

X_train_tfidf = tfidf_transformer.fit_transform(samples)
print (X_train_tfidf) 
neigh = NearestNeighbors(n_neighbors=1, n_jobs=-1) 
neigh.fit(X_train_tfidf)

test=["test zoom"]
X_test_counts = count_vect.transform(test)

X_test_tfidf = tfidf_transformer.transform(X_test_counts)

res = neigh.kneighbors(X_test_tfidf, return_distance=True)
print (res)

