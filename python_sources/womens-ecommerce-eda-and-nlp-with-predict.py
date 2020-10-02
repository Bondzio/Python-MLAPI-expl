#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re, string
from nltk.corpus import stopwords
from wordcloud import WordCloud
get_ipython().run_line_magic('matplotlib', 'inline')

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# If you like this notebook please upvoted

# In[ ]:


train = pd.read_csv("../input/womens-ecommerce-clothing-reviews/Womens Clothing E-Commerce Reviews.csv", index_col=0)


# In[ ]:


train.head()


# In[ ]:


train.describe()


# In[ ]:


train.info()


# In[ ]:


train.isnull().sum()


# In[ ]:


plt.figure(figsize=(7,7))
sns.heatmap(train.isnull())


# So, we have Title with 3800 null cells, and Review Text with 845.
# I can just drop null cels or fill with something.
# 
# First: My target will be Recommended IND
# My X will be just Recommended IND or Recommended IND + Title
# 
# Let's see what is missing in Review Text:
# Probably just filled 'Rating' and Recommended IND and who filled did not want to fill another option.

# In[ ]:


train[train['Review Text'].isnull()].head()


# We have more nun values.. let's see:

# In[ ]:


none = train[train['Division Name'].isnull()]
none


# We can see that all 'Division Name', 'Department', and Class Name are null values...
# Interesting that we have repeated values in 'Clothing ID'
# 
# So probably its a store registration error, and should be fixed by the E-Commerce.
# Here, I'm going to fill everything with "none".

# In[ ]:


none['Clothing ID'].unique()


# In[ ]:


train.fillna('none', inplace=True)


# Let's see how many ratings we have in each "class rating"

# In[ ]:


plt.figure(figsize=(6,6))
plt.title('Rating Counts')
sns.countplot(train['Rating'])


# Almost all of them are 4 or 5 and how many uniques objects we have in each object column?

# In[ ]:


objectcol = train.select_dtypes(include='object')
for col in objectcol.columns:
    print(f'{col}: {train[col].nunique()}')


# Next, we can see which of them have more Positive Feedback Count?
# It's important because if someone make a bad feedback, and a lot of people see, people can stop to by just because of this Review.. so, let's see something about it

# In[ ]:


train.sort_values(by='Positive Feedback Count', ascending = False).head()


# We can see the first, second and third with more counts...
# The first is rating 3,
# second is rating 5,
# and last one is rating 1
# 

# In[ ]:


train.sort_values(by='Positive Feedback Count', ascending = False)['Review Text'][0]


# In[ ]:


train.sort_values(by='Positive Feedback Count', ascending = False)['Review Text'][2]


# In[ ]:


train.sort_values(by='Positive Feedback Count', ascending = False)['Review Text'][1]


# In[ ]:


department = train[['Department Name', 'Rating']].groupby('Department Name').mean().sort_values(by='Rating', ascending = False)


# In[ ]:


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = round(float(rect.get_height()),2)
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


# In[ ]:


fig, ax = plt.subplots(figsize=(10,6))
rect1 = ax.bar(x=department.index, height=department['Rating'])
plt.title('Rating by department')
plt.ylabel('Rating %')
plt.xlabel('Department')
autolabel(rect1)


# Which class have the best rating? 
# 
# In this chart we see that Casual Bottons get the best rating, in next chart we see that younger people buy more Casual Bottoms than older people

# In[ ]:


class_name = train[['Class Name', 'Rating']].groupby('Class Name').mean().sort_values(by='Rating', ascending = False)
plt.figure(figsize=(10,10))
plt.title('Rating by Class')
sns.barplot(y=class_name.index, x=class_name['Rating'])


# In[ ]:


plt.figure(figsize=(7,7))
plt.title('Age distribution')
train['Age'].hist()
plt.xlabel('Age')


# In[ ]:


age = train[['Class Name','Age']].groupby('Class Name').mean().sort_values(by='Age', ascending = False)
age
plt.figure(figsize=(10,10))
plt.title('Class by Age')
sns.barplot(y=age.index, x=age['Age'])


# Now I'll clean the reviews and create another column with the new text.
# I will create a list with Review Text words and Title words 

# In[ ]:


def get_text(text):
    text = text.lower()

    text = re.sub("I'm",'I m',text)
    text = re.sub(":", " ", text)
    text = re.sub("He's","he is", text)
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)        
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text) 
    text = re.sub(r"\'ll", " will", text)  
    text = re.sub(r"\'ve", " have", text)  
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"don't", "do not", text)
    text = re.sub(r"did't", "did not", text)
    text = re.sub(r"can't", "can not", text)
    text = re.sub(r"it's", "it is", text)
    text = re.sub(r"couldn't", "could not", text)
    text = re.sub(r"have't", "have not", text)
    text = re.sub(r"[,.\"!@#$%^&*(){}?/;`~:<>+=-]", "", text)
    text = re.sub(r"[00-99]", "", text)
    text = re.sub(r"none", "", text)

    nopunc = [char for char in text if char not in string.punctuation] # del punctuation
    nopunc = "".join(nopunc)
    
    clean = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]   # or get_stop_words('english')
    clean = " ".join(clean)
    
    clean2 = [word for word in clean.split() if len(word) > 1] # get len more than 1 (del A, I, s, d)
    clean2 = " ".join(clean2)
    return clean2


# In[ ]:


train['Review Text1'] = train['Review Text'].apply(get_text)
train['Title1'] = train['Title'].apply(get_text)


# In[ ]:


lista = []
for word in train['Review Text1']:
    word = word.split()
    for n in word:
        lista.append(n)
        
lista = " ".join(lista)


# In[ ]:


wordcloud = WordCloud(width=1600, height=650, margin=0).generate(lista)

plt.figure(figsize=(15,15))
plt.title('Most written words in Review Text')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()


# In[ ]:


lista1 = []
for word in train['Title1']:
    word = word.split()
    for n in word:
        lista1.append(n)
lista1 = " ".join(lista1)


# In[ ]:


wordcloud1 = WordCloud(width=1600, height=650, margin=0).generate(lista1)
plt.figure(figsize=(15,15))
plt.title('Most written words in Title Words')
plt.imshow(wordcloud1, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()


# In[ ]:


recommended = train[train['Recommended IND']==1]
recommended_list = []
for word in recommended['Review Text1']:
    word = word.split()
    for n in word:
        recommended_list.append(n)
recommended_list = " ".join(recommended_list)


# In[ ]:


not_recommended_list = []
not_recommended = train[train['Recommended IND']==0]
for word in not_recommended['Review Text1']:
    word = word.split() 
    for n in word:
        not_recommended_list.append(n)
not_recommended_list = " ".join(not_recommended_list)


# In[ ]:


recomendedcloud = WordCloud(width=1600, height=650, margin=0).generate(recommended_list)
notrecomendedcloud = WordCloud(width=1600, height=650, margin=0).generate(not_recommended_list)


# In[ ]:


plt.figure(figsize=(15,15))
recomendedcloud
plt.imshow(recomendedcloud, interpolation='bilinear')
plt.title('Most written words in Recommended IND')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()


# In[ ]:


plt.figure(figsize=(15,15))
notrecomendedcloud
plt.imshow(notrecomendedcloud, interpolation='bilinear')
plt.title('Most written words in not Recommended IND')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()


# **MODEL AND TRAIN SPLIT**
# 
# First test x = 'review text1'
#            y = 'Recommended IND'
#           
#  Models:
# *  Random Forest
# *  MultinomialNB

# In[ ]:


x=train['Review Text1']
y=train['Recommended IND']


# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(x)


# In[ ]:


from sklearn.model_selection import train_test_split
xtrain, xtest,ytrain,ytest = train_test_split(X,y, random_state = 42)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix,classification_report
model_rf = RandomForestClassifier(random_state=42)
model_rf.fit(xtrain,ytrain)
predict_rf = model_rf.predict(xtest)


# In[ ]:


scoretest_rf = model_rf.score(xtest,ytest)
print(f' Score Test: {scoretest_rf}')
print(classification_report(ytest,predict_rf))


# In[ ]:


from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
nb.fit(xtrain,ytrain)
nb_predict = nb.predict(xtest)


# In[ ]:


scoretest_nb = nb.score(xtest,ytest)
print(f' Score Test: {scoretest_nb}')
print(classification_report(ytest,nb_predict))


# In[ ]:


from sklearn.metrics import confusion_matrix
random_forest_matrix = confusion_matrix(ytest,predict_rf)
random_forest_matrix


# In[ ]:


nb_matrix = confusion_matrix(ytest,nb_predict)
nb_matrix


# In[ ]:


fig,ax=plt.subplots(1,2,figsize=(18,8))
ax[0] = sns.heatmap(random_forest_matrix, annot=True, ax=ax[0])
ax[0].set_title('Confusion Matrix Random Forest')
ax[1] = sns.heatmap(nb_matrix,annot=True, ax=ax[1])
ax[1].set_title('Confusion Matrix Naive Bayes')


# Now, I going to create a new feature:
#     'Review Text' + 'Title'

# In[ ]:


def get_all(col):
    review_text = col[0]
    title = col[1]
    text = str(review_text) + str(title)
    return text


train['full'] = train[['Review Text1', 'Title1']].apply(lambda x: get_all(x), axis=1)


# In[ ]:


train.head()


# **MODEL WITH NEW FEATURE**

# In[ ]:


xbest=train['full']
y=train['Recommended IND']


# In[ ]:


cv = CountVectorizer()
Xbest = cv.fit_transform(xbest)
xtrain, xtest,ytrain,ytest = train_test_split(Xbest,y, random_state = 42)


# In[ ]:


model_rf_full = RandomForestClassifier(random_state=42)
model_rf_full.fit(xtrain,ytrain)
predict_rf_full = model_rf_full.predict(xtest)


# In[ ]:


scoretest_rf_full = model_rf_full.score(xtest,ytest)
print(f' Score Test: {scoretest_rf_full}')
print(classification_report(ytest,predict_rf_full))


# In[ ]:


nb_full = MultinomialNB()
nb_full.fit(xtrain,ytrain)
nb_predict_full = nb_full.predict(xtest)


# In[ ]:


nb_score_test = nb_full.score(xtest,ytest)
print(f' Score Test: {nb_score_test}')
print(classification_report(ytest,nb_predict_full))


# In[ ]:


rf_matrix_full = confusion_matrix(ytest,predict_rf_full)
rf_matrix_full


# In[ ]:


nb_matrix_full = confusion_matrix(ytest,nb_predict_full)
nb_matrix_full


# In[ ]:


fig,ax=plt.subplots(1,2,figsize=(18,8))
ax[0] = sns.heatmap(rf_matrix_full, annot=True, ax=ax[0])
ax[0].set_title('Confusion Matrix Random Forest')
ax[1] = sns.heatmap(nb_matrix_full,annot=True, ax=ax[1])
ax[1].set_title('Confusion Matrix Naive Bayes')


# In[ ]:


print(f' First NB test: {scoretest_nb}')
print(f' First RF test: {scoretest_rf}')
print(f' Second NB test: {nb_score_test}')
print(f' Second RF test: {scoretest_rf_full}')


# We got a best score with multinominal, but with new feature we did not improve so much.
# 
# If you like this notebook please upvote

# In[ ]:




