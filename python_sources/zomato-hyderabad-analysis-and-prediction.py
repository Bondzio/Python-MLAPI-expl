#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Libraries Needed:
import numpy as np                        ## Matrix functions
import matplotlib.pyplot as plt           ## PLotting
import pandas as pd                       ## To Work WIth Dataframes 
import plotly.express as px               ## For Interactive Visualization
import plotly.graph_objects as go         ## For Detailed visual plots
from collections import Counter         
from plotly.subplots import make_subplots ## To Plot Subplots
from wordcloud import WordCloud           ## To Generate Wordcloud
from datetime import datetime             ## Work with timeseries data

import warnings
warnings.filterwarnings('ignore')


# ## MetaData

# In[ ]:


metadata = pd.read_csv("../input/zomato-restaurants-hyderabad/Restaurant names and Metadata.csv")
print("MetaData Shape:", metadata.shape)


# In[ ]:


metadata.head()


# In[ ]:


metadata.isnull().sum()


# In[ ]:


metadata.info()


# #### Linked attribute will be of no use in our analysis. Also, Cost attribute should be of float type.

# In[ ]:


metadata.drop(['Links'], axis=1, inplace=True)
metadata['Cost'] = metadata['Cost'].apply(lambda x : float(x.replace(',', '')))


# ### Cost Distribution

# In[ ]:


cost = metadata[['Name', 'Cost']]

bins = pd.DataFrame(pd.cut(cost['Cost'], bins= 10))
bins.columns = ['bins']
bins['bins'] = bins['bins'].astype(str)

bins = bins['bins'].value_counts().reset_index()
bins.columns = ['Bin', 'Count']
bins["Cumsum"] = bins['Count'].cumsum()


# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(name = "Restaurants in Range", x = bins['Bin'], y=bins['Count']))
fig.add_trace(go.Scatter(name = "Restaurants below or in Range", x = bins['Bin'], y=bins['Cumsum']))
fig.update_layout(title="No Of Restaurents by Price Range",
                 xaxis_title = "Price Range",
                 yaxis_title = "No Of Restaurants")


# In[ ]:


fig = go.Figure()

temp = cost.sort_values(by='Cost')

fig.add_trace(go.Bar(name = "Cheapest Restaurant", x = temp.head()['Name'], y=temp.head()['Cost']))
fig.add_trace(go.Bar(name="Expensive Restaurent", x = temp.tail()['Name'], y=temp.tail()['Cost']))
fig.update_layout(title = "Least and Most Expensive Restaurants:",
                 xaxis_title = "Restaurant Name",
                 yaxis_title = "Cost")
fig.show()
del temp


# ### Cuisins

# In[ ]:


cuisines = metadata['Cuisines']
cuisines = cuisines.apply(lambda x : x.lower())


# In[ ]:


all_cuisines = ', '.join(i for i in cuisines.tolist())
all_cuisines = Counter(all_cuisines.split(', '))
all_cuisines = pd.DataFrame.from_dict(all_cuisines, orient='index', dtype='int')
all_cuisines.columns = ['No Of Restaurents']
all_cuisines.sort_values(by='No Of Restaurents', ascending=False, inplace=True)


# In[ ]:


cuisines = cuisines.apply(lambda x : x.split(', '))
cuisines = pd.DataFrame(cuisines)

for i in all_cuisines.index.tolist():
    cuisines['{}'.format(i)] = cuisines['Cuisines'].apply(lambda x : i in x)

cuisines.drop('Cuisines', axis=1, inplace=True)
cuisines = pd.concat([metadata, cuisines], axis=1)
cuisines.drop(['Collections', 'Cuisines', 'Timings'], axis=1, inplace=True)
cuisines = pd.melt(cuisines, id_vars=['Name', 'Cost'], var_name='Cuisine')
cuisines = cuisines[cuisines['value']]
cuisines.drop(['value'], axis=1, inplace=True)
del all_cuisines


# In[ ]:


temp = cuisines['Cuisine'].value_counts().reset_index()

fig = px.bar(x = temp['index'], y=temp['Cuisine'])
fig.update_layout(title = "Cuisines availability",
                 xaxis_title = "Cusisine",
                 yaxis_title = "No of restaurants cuisine available at")
fig.show()
del temp


# In[ ]:


## Value_counts() functions returns in descending order. So we don't need to sort expliitly.
top_cuisines = cuisines['Cuisine'].value_counts().reset_index()
top_cuisines = top_cuisines['index'].tolist()[:8]


# In[ ]:


temp = cuisines[cuisines['Cuisine'].isin(top_cuisines)]

fig = px.histogram(data_frame=temp, x='Cost',
            facet_col = 'Cuisine', facet_col_wrap=4,
            title = "Price Distribution amongst most popular cuisines:")
fig.show()
del temp


# In[ ]:


mean_cost = cuisines.groupby(by='Cuisine')['Cost'].mean().reset_index()
mean_cost.sort_values(by='Cost', ascending=False, inplace=True)

fig = px.bar(mean_cost, x='Cuisine', y='Cost')
fig.update_layout(title = "Average Cost by Cuisine",
                 xaxis_title = "Cuisine (Most to Least Expensive)",
                 yaxis_title = "Avg Cost of Cuisine")
fig.show()
del mean_cost


# In[ ]:


cuisine_offered = cuisines.groupby(by='Name')['Cuisine'].count().reset_index()
cuisine_offered.columns = ['Name', 'Cuisine_Offered']

metadata = pd.merge(metadata, cuisine_offered, left_on='Name', right_on = 'Name')

del cuisine_offered


# ### Collections

# In[ ]:


collections = metadata['Collections'].dropna().tolist()
collections = ', '.join(i for i in collections)

wc = WordCloud(background_color="white", max_words=200, 
               width=800, height=600, random_state=1).generate(collections)
print("Most Common Taggs:")
plt.imshow(wc)
del collections


# ## Reviews

# In[ ]:


reviews = pd.read_csv("../input/zomato-restaurants-hyderabad/Restaurant reviews.csv")
print("Reviews Shape:", reviews.shape)


# In[ ]:


reviews.head()


# In[ ]:


reviews.isnull().sum()


# In[ ]:


reviews.info()


# In[ ]:


temp = reviews[reviews.Reviewer.isnull()].Restaurant.unique()
print("These are the restaurants where we have missing values:", temp, sep = '\n')
del temp


# #### Picture attribute will not be used in our analysis, we better get rid of it. Also, number of null values is ignorable considering size of the dataset. We're gonna drop null values too.

# In[ ]:


reviews.drop('Pictures', axis = 1, inplace=True)
reviews.dropna(inplace=True)


# ### Data Cleaning

# In[ ]:


reviews['Rating'].unique()


# In[ ]:


reviews.loc[reviews['Rating']=='Like', 'Rating'] = 3.5
reviews['Rating'] = reviews['Rating'].astype('float')


# #### Metadada attribute consistes of followers and reviews. It is better to extract these differently and use in out analysis. We'll rename the reviews as thread review as we already have an attribute named as reviews that are Original Review. Also, After extracting these differently, we'll have no use of the "Metadata" attribute itself. So, we'll drop that.

# In[ ]:


def get_followers(x):
    x = x.split(", ")
    try :
        x = x[1].split()[0]
    except:
        x = 0
    return x


# In[ ]:


reviews['Thread Review'] = reviews['Metadata'].apply(lambda x : x.split(", ")[0].split()[0])
reviews['Followers'] = reviews['Metadata'].apply(get_followers)

reviews['Thread Review'] = reviews['Thread Review'].astype('int')
reviews['Followers'] = reviews['Followers'].astype('int')

reviews.drop('Metadata', axis=1, inplace=True)


# #### Time is in the form of string, for better analysis we can convert this to datetime object.

# In[ ]:


reviews['Time'] = reviews['Time'].apply(lambda x : datetime.strptime(x, '%m/%d/%Y %H:%M'))


# ### No Review Restaurant

# In[ ]:


reviews['Restaurant'].value_counts().nunique()


# In[ ]:


## 100 reviews for each restaurant, Which restaurants have not been reviewd?

temp = set(metadata['Name'].tolist()) - set(reviews['Restaurant'].tolist())

print("Restaurants which have no reviews.", temp, sep = '\n')


# In[ ]:


print("Details of the restaurants that have not been reviewd.")
metadata[metadata['Name'].isin(temp)]


# ### Reviews Distribution

# In[ ]:


reviewers = reviews['Reviewer'].value_counts().reset_index()
reviewers.columns = ['Reviewer', 'Reviews']

fig = px.histogram(reviewers, 'Reviews')
fig.update_layout(title = "Distribution in no of reviews:",
                 xaxis_title = "No of Reviews",
                 yaxis_title = "Given By users")
fig.show()


# #### We can see that most users have only given reviews once.

# In[ ]:


temp = reviewers.head()['Reviewer'].tolist()
print("People who have posted most reviews are :", temp)

del temp, reviewers


# #### Let's see if we'll encounter these names again in our analysis.

# ### Restaurants and Ratings

# In[ ]:


mean_ratings = reviews.groupby('Restaurant')['Rating'].mean().reset_index()
mean_ratings.columns = ['Restaurant', 'Avg. Rating']
reviews = pd.merge(reviews, mean_ratings, left_on = 'Restaurant', right_on = 'Restaurant')
mean_ratings.sort_values(by='Avg. Rating', ascending = False, inplace=True)


# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(name = "Highest Avg. Ratings",
                     x = mean_ratings.head()['Restaurant'], y = mean_ratings.head()['Avg. Rating']))
fig.add_trace(go.Bar(name = "Lowest Avg. Ratings",
                     x = mean_ratings.tail()['Restaurant'], y = mean_ratings.tail()['Avg. Rating']))

fig.update_layout(title = "Restaurents with highest and lowest avg. ratings:",
                 xaxis_title = "Restaurant Name",
                 yaxis_title = "Avg. Rating")
fig.show()


# ### Time and Reviews

# In[ ]:


reviews['Hour'] = reviews['Time'].dt.hour
reviews['Month'] = reviews['Time'].dt.month


# In[ ]:


hour_counts = reviews['Hour'].value_counts().reset_index()
hour_counts.columns = ['Hour', 'Count']
hour_counts.sort_values(by = 'Hour')
fig = px.bar(hour_counts, 'Hour', 'Count')
fig.update_layout(title = "Reviews submissions by day Hours:",
                 xaxis_title = "Day Hour",
                 yaxis_title = "No Of Reviews")
fig.show()
del hour_counts


# #### We can see an obvious pattern in day-hour and no of reviews recorded during that hour. No one just reviews a restaurant as soon as they wake up.

# In[ ]:


month_counts = reviews['Month'].value_counts().reset_index()
month_counts.columns = ['month', 'Count']
month_counts.sort_values(by = 'month')
fig = px.bar(month_counts, 'month', 'Count')
fig.update_layout(title = "Reviews submissions by months:",
                 xaxis_title = "Month",
                 yaxis_title = "No Of Reviews")
fig.show()
del month_counts


# #### We have an unusual pattern here, Recorded reviews are extremely less in the month of June as compared to other months. What chould be the reason?

# In[ ]:


temp = reviews.groupby(by='Hour')['Rating'].mean().reset_index()
print(temp)


# #### We found No Significance difference here, So there is no point plotting it and going deep in it.

# In[ ]:


reviews['Weekday'] = reviews['Time'].dt.weekday
day_map = dict(zip(range(7), ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
reviews['Weekday'] = reviews['Weekday'].map(day_map)
del day_map


# In[ ]:


weekday_count = reviews.groupby(by='Weekday')['Review'].count().reset_index()

fig = go.Figure(data=[
    go.Pie(labels = weekday_count['Weekday'],
           values = weekday_count['Review'],
          )
])

fig.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=20,
                  marker=dict(line=dict(color='#000000', width=2)))
fig.update_layout(title = "No of Reviews by Week-Day:")
fig.show()


# #### We can see a useual pattern here. People tend to go out on weekends more than on weekdays, this is why we have more reviews on weekends than on weekdays.

# In[ ]:


fig = px.histogram(data_frame=reviews, x='Rating',
            facet_col = 'Weekday', facet_col_wrap=4,
            title = "Rating Distribution amongst weekdays:")
fig.show()


# ### Followers and Thread Reviews

# In[ ]:


fig = px.scatter(reviews, x = 'Thread Review', y='Followers')
fig.update_layout(title = "Relationship b/w Threads and Followers",
                 xaxis_title = "No Of Threads",
                 yaxis_title = "No Of Followers")


# ### Reviewers

# In[ ]:


reviewers = reviews.groupby(by='Reviewer')['Followers', 'Thread Review'].sum().reset_index()
reviewers.sort_values(by = ['Followers'], ascending = False, inplace=True)

most_followers = reviewers.head()

reviewers.sort_values(by = ['Thread Review'], ascending = False, inplace=True)

most_threads = reviewers.head()


# In[ ]:


fig = make_subplots(rows = 1, cols = 2, subplot_titles = ['Most Followers', 'Most Threads'])

fig.add_trace(go.Bar(name="Followers", x = most_followers['Reviewer'], y = most_followers['Followers']), 1,1)
fig.add_trace(go.Bar(name="Threads", x = most_followers['Reviewer'], y = most_followers['Thread Review']), 1,1)

fig.add_trace(go.Bar(name="Followers", x = most_threads['Reviewer'], y = most_threads['Followers']), 1,2)
fig.add_trace(go.Bar(name="Threads", x = most_threads['Reviewer'], y = most_threads['Thread Review']), 1,2)


fig.update_xaxes(title_text="Reviewer", row=1, col=1)
fig.update_xaxes(title_text="Reviewer", row=1, col=2)

fig.update_yaxes(title_text="Sum", row=1, col=1)
fig.update_yaxes(title_text="Sum", row=1, col=2)

fig.update_layout(title = "Reviewers with:")


# #### Did you notice something? 'Parijat Ray' in the list of Reviewer with most threads is from our list of people who posted most reviews.

# ## Combining Datasets

# ### Cost vs Rating

# In[ ]:


df = pd.merge(cuisines, reviews, left_on = 'Name', right_on = 'Restaurant')
df.drop(['Name', 'Time', 'Hour', 'Month'], axis = 1, inplace = True)


# In[ ]:


fig = px.scatter(df, 'Cost', 'Avg. Rating', trendline = 'ols')
fig.update_layout(title = "Relationship between Cost and Avg. Raing of the restaurant")
fig.show()


# #### We can see a positive correlation between cost and Avg. Rating of a Cuisine.

# In[ ]:


del metadata, reviews, cuisines


# ## Analyzing Reviews (Text)

# In[ ]:


review = pd.read_csv("../input/zomato-restaurants-hyderabad/Restaurant reviews.csv")
review = review[['Review', 'Rating']]


# In[ ]:


review.isnull().sum()


# In[ ]:


review.dropna(inplace=True)


# In[ ]:


review.head()


# ### Data Cleaning

# In[ ]:


review['Review']= review['Review'].apply(lambda x : x.replace('\n', ' '))
review['Review']= review['Review'].apply(lambda x : x.lower())


# ### Ratings distribution

# In[ ]:


review.groupby(by='Rating')['Review'].count()


# #### Very few reviews have rating like, 1.5, 2.5, 3.5 and 4.5. (We have lesser data for some categories and more data for other categories). This will make classification process difficult.
# - We should merge them to get better performance. 
# - For Analysis as well, this will be more helpful as this few records are similar to outliers.
# - 'Like' is a data redunduncy, better drop this.

# In[ ]:


review = review[review['Rating']!='Like']
review['Rating']= review['Rating'].astype('float')
review['Rating'] = review['Rating'].apply(lambda x : int(x))


# In[ ]:


review.groupby(by='Rating')['Review'].count()


# ### Extracting meaningful words from reviews

# In[ ]:


import nltk
from nltk.tokenize import word_tokenize

review['Words'] = review['Review'].apply(word_tokenize)

from nltk.corpus import stopwords 

StopWords = set(stopwords.words('english'))

def clean_words(x):
    words = []
    for i in x:
        if i.isalnum() and i not in StopWords:
            words.append(i)
    return words

review['Words'] = review['Words'].apply(clean_words)
review['Word Count'] = review['Words'].apply(lambda x : len(x))
del StopWords


# ### Review length by Rating

# In[ ]:


review.groupby(by='Rating')['Word Count'].mean()


# In[ ]:


fig = px.histogram(review, x='Word Count', color='Rating',
            barmode = 'overlay', nbins=50, marginal = 'box')
fig.update_layout(title = "Word Count Distribution in Reviews by Ratings.",
                 xaxis_title = "Word Count",
                 yaxis_title = "No of Reviews")
fig.show()


# In[ ]:


review.drop('Word Count', axis = 1, inplace=True)


# ### Most common words by rating

# In[ ]:


most_common = dict()

for group, data in review.groupby(by='Rating'):
    words = []
    for i in data['Words'].tolist():
        words.extend(i)
    words = nltk.FreqDist(words)
    words = words.most_common(10)
    most_common['{}'.format(group)] = words
print("Most Common Words by ratings and their word-counts:")
pd.DataFrame(most_common)


# ### Parts Of Speech

# In[ ]:


review['POS'] = review['Words'].apply(nltk.pos_tag)


# ### Adjectives

# In[ ]:


def get_adjective(x):
    adj = set(['JJ', 'JJR', 'JJS'])
    word = []
    for i in x:
        if i[1] in adj:
            word.append(i[0])
    return word

review['ADJ'] = review['POS'].apply(get_adjective)

most_common = dict()
for group, data in review.groupby(by='Rating'):
    words = []
    for i in data['ADJ'].tolist():
        words.extend(i)
    words = nltk.FreqDist(words)
    words = words.most_common(10)
    most_common['{}'.format(group)] = words
print("Most Common Adjectives by ratings:")
pd.DataFrame(most_common)


# ### Nouns

# In[ ]:


def get_noun(x):
    noun = set(['NN', 'NNS', 'NNP', 'NNPS'])
    word = []
    for i in x:
        if i[1] in noun:
            word.append(i[0])
    return word

review['Noun'] = review['POS'].apply(get_noun)

review.drop('POS', axis = 1, inplace = True)

most_common = dict()
for group, data in review.groupby(by='Rating'):
    words = []
    for i in data['Noun'].tolist():
        words.extend(i)
    words = nltk.FreqDist(words)
    words = words.most_common(10)
    most_common['{}'.format(group)] = words
print("Most Common Nouns by ratings:")
pd.DataFrame(most_common)


# #### A bigram (group of two words) better describes feelings than a single word. Let's see the bigrams

# ### Common Bigrams

# In[ ]:


most_common = dict()
for group, data in review.groupby(by='Rating'):
    words = []
    for i in data['Words'].tolist():
        words.extend(i)
    bigram = list(nltk.bigrams(words))
    bigram = nltk.FreqDist(bigram)
    bigram = bigram.most_common(10)
    most_common['{}'.format(group)] = bigram

print("Most Common Bi-grams by Ratings:")
pd.DataFrame(most_common)


# #### Now, these bigrams have started making proper sense. Like, "Worst Experiance" is th most common bigram for rating 1, whereas "Must Try" is the most common bigram for rating 5. These bigram mean the same as their ratings.

# In[ ]:


del most_common


# ### Polarity And Subjectivity

# In[ ]:


from textblob import TextBlob

review['Subjectivity'] = review['Review'].apply(lambda x : TextBlob(x).sentiment.subjectivity)
review['Polarity'] = review['Review'].apply(lambda x : TextBlob(x).sentiment.polarity)


# In[ ]:


fig = px.histogram(review, x='Subjectivity', barmode='overlay', color='Rating')
fig.update_layout(title = "Subjectivity distribution in reviews of different ratings.",
                 xaxis_title = "Subjectivity",
                 yaxis_title = "Number of Reviews")
fig.show()


# In[ ]:


fig = px.histogram(review, x='Polarity', barmode='overlay', color='Rating')

fig.update_layout(title = "Polarity distribution in reviews of different ratings.",
                 xaxis_title = "Subjectivity",
                 yaxis_title = "Number of Reviews")
fig.show()


# #### We do see difference in polarity distribution of reviews of different ratings. Which is how this should be. 

# ## Predictions

# ### Tf-idf

# In[ ]:


from sklearn.feature_extraction.text  import TfidfVectorizer
tf = TfidfVectorizer(stop_words = 'english', ngram_range = (1,2),
                    min_df = 1)


# In[ ]:


from sklearn.model_selection import train_test_split

X = review['Review']
y = review['Rating']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = y, random_state = 1)

tf_x_train = tf.fit_transform(x_train)
tf_x_test = tf.transform(x_test)


# ### Models

# In[ ]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
performance = {'Model' : [],
              'Accuracy Score' : [],
              'Precision Score' : [],
              'Recall Score' : [],
              'f1 Score' : []}


# In[ ]:


from sklearn.linear_model import LogisticRegression

lr= LogisticRegression()
lr.fit(tf_x_train, y_train)
pred = lr.predict(tf_x_test)

performance['Model'].append('LogisticRegression')
performance['Accuracy Score'].append(accuracy_score(y_test, pred))
performance['Precision Score'].append(precision_score(y_test, pred, average='macro'))
performance['Recall Score'].append(recall_score(y_test, pred, average='macro'))
performance['f1 Score'].append(f1_score(y_test, pred, average='macro'))


# In[ ]:


from sklearn.linear_model import SGDClassifier

sgd = SGDClassifier()
sgd.fit(tf_x_train, y_train)
pred = sgd.predict(tf_x_test)

performance['Model'].append('SGD')
performance['Accuracy Score'].append(accuracy_score(y_test, pred))
performance['Precision Score'].append(precision_score(y_test, pred, average='macro'))
performance['Recall Score'].append(recall_score(y_test, pred, average='macro'))
performance['f1 Score'].append(f1_score(y_test, pred, average='macro'))


# In[ ]:


from sklearn.naive_bayes import MultinomialNB

mnb = MultinomialNB()
mnb.fit(tf_x_train, y_train)
pred = mnb.predict(tf_x_test)

performance['Model'].append('Multinomial NB')
performance['Accuracy Score'].append(accuracy_score(y_test, pred))
performance['Precision Score'].append(precision_score(y_test, pred, average='macro'))
performance['Recall Score'].append(recall_score(y_test, pred, average='macro'))
performance['f1 Score'].append(f1_score(y_test, pred, average='macro'))


# In[ ]:


from sklearn.naive_bayes import BernoulliNB

bnb = BernoulliNB()
bnb.fit(tf_x_train, y_train)
pred = bnb.predict(tf_x_test)

performance['Model'].append('Bernoulli NB')
performance['Accuracy Score'].append(accuracy_score(y_test, pred))
performance['Precision Score'].append(precision_score(y_test, pred, average='macro'))
performance['Recall Score'].append(recall_score(y_test, pred, average='macro'))
performance['f1 Score'].append(f1_score(y_test, pred, average='macro'))


# In[ ]:


from sklearn.svm import SVC

svc = SVC()
svc.fit(tf_x_train, y_train)
pred = svc.predict(tf_x_test)

performance['Model'].append('SVC')
performance['Accuracy Score'].append(accuracy_score(y_test, pred))
performance['Precision Score'].append(precision_score(y_test, pred, average='macro'))
performance['Recall Score'].append(recall_score(y_test, pred, average='macro'))
performance['f1 Score'].append(f1_score(y_test, pred, average='macro'))


# In[ ]:


from sklearn.svm import LinearSVC

linear_svc = LinearSVC()
linear_svc.fit(tf_x_train, y_train)
pred = linear_svc.predict(tf_x_test)

performance['Model'].append('Linear SVC')
performance['Accuracy Score'].append(accuracy_score(y_test, pred))
performance['Precision Score'].append(precision_score(y_test, pred, average='macro'))
performance['Recall Score'].append(recall_score(y_test, pred, average='macro'))
performance['f1 Score'].append(f1_score(y_test, pred, average='macro'))


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier()
rfc.fit(tf_x_train, y_train)
pred = rfc.predict(tf_x_test)

performance['Model'].append('Random Forest')
performance['Accuracy Score'].append(accuracy_score(y_test, pred))
performance['Precision Score'].append(precision_score(y_test, pred, average='macro'))
performance['Recall Score'].append(recall_score(y_test, pred, average='macro'))
performance['f1 Score'].append(f1_score(y_test, pred, average='macro'))


# In[ ]:


pd.DataFrame(performance)


# ### Voted Classifier

# In[ ]:


from statistics import mode

class voted_classifier():
    def __init__(self):
        self.classifiers = [lr, sgd, mnb, bnb, svc, linear_svc, rfc]
        
    def classify(self, features):
        names = ['lr', 'sgd', 'mnb', 'bnb', 'svc', 'linear_svc', 'rfc']
        i = 0 
        votes = pd.DataFrame()
        for classifier in self.classifiers:
            pred = classifier.predict(features)
            votes[names[i]] = pred
            i+=1
        return votes.mode(axis = 1)[0]


# In[ ]:


vc = voted_classifier()
pred = vc.classify(tf_x_test)

performance['Model'].append('Voted Classifier')
performance['Accuracy Score'].append(accuracy_score(y_test, pred))
performance['Precision Score'].append(precision_score(y_test, pred, average='macro'))
performance['Recall Score'].append(recall_score(y_test, pred, average='macro'))
performance['f1 Score'].append(f1_score(y_test, pred, average='macro'))


# In[ ]:


pd.DataFrame(performance)


# #### Thank you. Do share your thoughts and suggestions in the comments. (Work on progress to ahieve better accuracy.)
