#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


##Load libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc


# In[ ]:


data = pd.read_csv("../input/Womens Clothing E-Commerce Reviews.csv")


# In[ ]:


data.head(3)


# In[ ]:


data.describe()


# In[ ]:


data.info()


# In[ ]:


data.isnull().sum()


# In[ ]:


data.shape


# In[ ]:


###Plot missing values
sns.set(rc={'figure.figsize':(11,4)})
pd.isnull(data).sum().plot(kind='bar')
plt.ylabel('Number of missing values')
plt.title('Missing values per Feature')


# In[ ]:


sns.set(rc={'figure.figsize':(11,5)})
plt.hist(data['Age'],bins=40)
plt.xlabel("Age")
plt.ylabel("Review")
plt.title("Number of review per page")


# ### above histogram shows that age between 25-50 are most revivwing age group

# In[ ]:


sns.boxplot(x='Rating',y='Age',data=data)
plt.title('Rating Distribution per age')


# In[ ]:


###Plot frequency distribution of Recommended IND
sns.countplot(x='Recommended IND',data=data)
plt.title("Distribution of Recommended IND")


# In[ ]:


##Frequency distribution of rating
sns.countplot(x='Rating',data=data)
plt.title("Frequency Distribution of Rating")


# In[ ]:


##Frequency distribution of division name
sns.countplot(x='Division Name',data=data)
plt.title("Distribution of Division Name")


# In[ ]:


###Frequency distribution of Department Name
sns.countplot(x='Department Name',data=data)
plt.title("Distribution of Department Name")


# In[ ]:


### Frequency distribution of class name
sns.countplot(x='Class Name',data=data)
plt.title("Distribution of Class Name")
plt.xticks(rotation=45)


# In[ ]:


###plot the most Recommended and not Recommended item 
recommended = data[data['Recommended IND']==1]
not_recommended = data[data['Recommended IND']==0]


# In[ ]:


fig = plt.figure(figsize=(14,14))
ax1 = plt.subplot2grid((2,2),(0,0))
ax1 = sns.countplot(recommended['Division Name'],color="green",alpha=0.8,label="Recommended")
ax1 = sns.countplot(not_recommended['Division Name'],color="red",alpha=0.8,label="Not Recommended")
ax1 = plt.title("Recommended items in each Division")
ax1 = plt.legend()


# #### from above Initmates Division Name are most recommended

# In[ ]:


ax2 = plt.subplot2grid((2,2),(0,0))
ax2 = sns.countplot(recommended['Department Name'] , color="yellow",alpha=0.8,label="Recommended")
ax2 = sns.countplot(not_recommended['Department Name'] , color="red",alpha=0.8,label="Not Recommended")
ax2 = plt.title("Recommended Items in each Department name")
ax2 = plt.legend()


# ### Bottoms department is most recommended where as Trend Departmet as rarely recommended

# In[ ]:


ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)
ax3 = plt.xticks(rotation=45)
ax3 = sns.countplot(recommended['Class Name'], color="cyan", alpha = 0.8, label = "Recommended")
ax3 = sns.countplot(not_recommended['Class Name'], color="blue", alpha = 0.8, label = "Not Recommended")
ax3 = plt.title("Recommended Items in each Class")
ax3 = plt.legend()


# In[ ]:


####Top 50 Most Popular item
fig = plt.figure(figsize=(14, 9))
plt.xticks(rotation=45)
plt.xlabel('item ID')
plt.ylabel('popularity')
plt.title("Top 50 Popular Items")
data['Clothing ID'].value_counts()[:50].plot(kind='bar');


# In[ ]:


##Check co relation between the variables
corrmat = data.corr()
sns.heatmap(corrmat,square=True, cmap="YlGnBu");


# ### from above plot we can see variables are strongly corelated with itslef and strong relationship found between rating and recommended IND

# ### Data Preprocess

# In[ ]:


data['Review Text'] = data['Review Text'].fillna('')


# In[ ]:


import re 
import nltk
nltk.download('wordnet')

def clean_and_tokenize(review):
    text = review.lower()
    
    tokenizer = nltk.tokenize.TreebankWordTokenizer()
    tokens = tokenizer.tokenize(text)
    
    stemmer = nltk.stem.WordNetLemmatizer()
    text = " ".join(stemmer.lemmatize(token) for token in tokens)
    text = re.sub("[^a-z']"," ", text)
    return text
data["Clean_Review"] = data["Review Text"].apply(clean_and_tokenize)


# In[ ]:


data.head(3)


# In[ ]:


### Set rating flase if it is >=4 else set it as positive
data = data[data['Rating'] !=3]
data['Sentiment'] = data['Rating'] >=4
data.head()


# In[ ]:


###Set True sentiment  as positive review and False as negative review
positive_reviews = data[data['Sentiment'] == True]
negative_reviews = data[data['Sentiment'] == False]


# In[ ]:


def wc(data,bgcolor,title):
    plt.figure(figsize = (100,100))
    wc = WordCloud(background_color = bgcolor, max_words = 1000,  max_font_size = 50)
    wc.generate(' '.join(data))
    plt.imshow(wc)
    plt.axis('off')


# In[ ]:


wc(positive_reviews['Review Text'],'black','Most Used Words')


# In[ ]:


wc(negative_reviews['Review Text'],'black','Most Used Words')


# ## Predict model

# In[ ]:


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data['Review Text'])
y = data['Recommended IND']


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.8,random_state=0)


# In[ ]:


lr = LogisticRegression()
lr.fit(X_train,y_train)


# In[ ]:


lr_pred = lr.predict(X_test)


# In[ ]:


##making confusion matrix
from sklearn.metrics import confusion_matrix 
cm = confusion_matrix(y_test,lr_pred)
cm


# In[ ]:


from sklearn.metrics import accuracy_score
accuracy_score(y_test,lr_pred)


# In[ ]:


# calculate the fpr and tpr for all thresholds of the classification
from sklearn import metrics
probs = lr.predict_proba(X_test)
preds = probs[:,1]
fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
roc_auc = metrics.auc(fpr, tpr)


# In[ ]:


plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()


# In[ ]:




