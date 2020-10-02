#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
print(os.listdir("../input"))


# In[2]:


import warnings
warnings.filterwarnings('ignore')

from nltk.tokenize import sent_tokenize, word_tokenize, WhitespaceTokenizer
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# add sentiment anaylsis columns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# create doc2vec vector columns
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument


# In[3]:


df_train=pd.read_csv('../input/train.csv')
df_test=pd.read_csv('../input/test.csv')
df_subm=pd.read_csv('../input/sample_submission.csv')


# In[4]:


df_train.info()


# In[5]:


df_train.sample(5)


# In[6]:


df_train.shape, df_test.shape


# In[7]:


# for i in range(len(df_train.columns)):
#     if i in [0,2,3,6,7,8,9]:
#         pass
#     else:
#         print(df_train.iloc[:,i].value_counts())


# In[8]:


df_train.dtypes


# In[9]:


df_train.isnull().sum()


# In[10]:


col = ['score_1', 'score_2', 'score_3', 'score_4', 'score_5']
for c in col:
    df_train[c].fillna(df_train[c].dropna().median(), inplace=True)
    df_test[c].fillna(df_train[c].dropna().median(), inplace=True)

col1 = ['negatives', 'summary', 'advice_to_mgmt']
for c in col1:
    df_train[c].fillna('', inplace=True)
    df_test[c].fillna('', inplace=True)


# In[11]:


df_train.shape, df_test.shape


# In[12]:


df_train.isnull().sum().any(), df_test.isnull().sum().any()


# In[13]:


# df_test.isnull().sum()
# location column has lots of Nan values. lets drop it.


# In[ ]:


drop_col = ['ID', 'location', 'date']
df_train.drop(columns=drop_col, inplace=True)
df_test.drop(columns=drop_col, inplace=True)


# In[ ]:


df_train.shape, df_test.shape


# In[ ]:


df_train['Place'].value_counts()


# In[ ]:


OEncoder  = OrdinalEncoder()
Enc_train = OEncoder.fit_transform(df_train[['Place', 'status']])
Enc_test  = OEncoder.transform(df_test[['Place', 'status']])


# In[ ]:


Enc_train[:5]


# In[ ]:


Enc_train.shape, df_train.shape


# In[ ]:


# Enc_mapped = map(lambda x: x[0], Enc_train.tolist())
# print(list(Enc_mapped))


# In[ ]:


def Create_ENC(df, Enc):
#   Create empty arrays with random elements with dimensions of the encoded column
    Place_enc = np.empty((len(Enc),))  
    Status_enc = np.empty((len(Enc),))
    for i in range(len(Enc)):
        Place_enc[i] = Enc[i][0]
        Status_enc[i] = Enc[i][1]
    df['place_enc'] = Place_enc
    df['status_enc'] = Status_enc


# In[ ]:


Create_ENC(df_train, Enc_train)
Create_ENC(df_test,  Enc_test)


# In[ ]:


df_train.isnull().sum().any(), df_test.isnull().sum().any()


# In[ ]:


df_train.sample(5)


# In[ ]:


df_train.groupby('overall').Place.count()


# In[ ]:


df_train.groupby('Place').overall.count()


# In[ ]:


# df_train.groupby('job_title').overall.count()
# no information from this


# In[ ]:


def Review_len(df):
    df['len_pos'] = df['positives'].str.len()
    df['len_neg'] = df['negatives'].str.len()


# In[ ]:


Review_len(df_train)
Review_len(df_test)


# In[ ]:


df_train.sample(3)


# In[ ]:


def ChangeToInt(df,col):
    df[col]=df[col].astype('int')


# In[ ]:


label='overall'
ChangeToInt(df_train,label)


# In[ ]:


def show_wordcloud(data, title = None):
    V_wordcloud = WordCloud(
        background_color = 'white',
        max_words = 200,
        max_font_size = 40, 
        scale = 3,
        random_state = 7
    ).generate(str(data))

    fig = plt.figure(1, figsize = (20, 20))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize = 20)
        fig.subplots_adjust(top = 2.3)

    plt.imshow(V_wordcloud)
    plt.show()


# In[ ]:


# print positive wordcloud
show_wordcloud(df_train["positives"])


# In[ ]:


# print negatives wordcloud
show_wordcloud(df_train["negatives"])


# In[ ]:


# print summary wordcloud
show_wordcloud(df_train["summary"])


# In[ ]:


# Get the lemmas of words from wordnet corpus reader
def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


# In[ ]:


def clean_text(text):
    # lower text
    text = text.lower()
    # tokenize text and remove puncutation
    text = [word.strip(string.punctuation) for word in text.split(" ")]
    # remove words that contain numbers
    text = [word for word in text if not any(c.isdigit() for c in word)]
    # remove stop words
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    # remove empty and less than 3 length tokens
    text = [t for t in text if len(t) >= 3]
    # pos tag text
    pos_tags = pos_tag(text)
    # lemmatize text
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    # remove words with less than 3 letters
    text = [t for t in text if len(t) >= 3]
    # join all
    text = " ".join(text)
    return(text)


# In[ ]:


df_train["Clean_positives"] = df_train["positives"].apply(lambda x: clean_text(x))
df_train["Clean_negatives"] = df_train["negatives"].apply(lambda x: clean_text(x))


# In[ ]:


df_test["Clean_positives"] = df_test["positives"].apply(lambda x: clean_text(x))
df_test["Clean_negatives"] = df_test["negatives"].apply(lambda x: clean_text(x))


# In[ ]:


df_train.shape, df_test.shape


# In[ ]:


df_train.isnull().sum().any(), df_test.isnull().sum().any()


# In[ ]:


df_test.sample(2)


# In[ ]:


df_train["Clean_reviews"] = df_train["Clean_positives"]+' '+df_train["Clean_negatives"]
df_test["Clean_reviews"] = df_test["Clean_positives"]+' '+df_test["Clean_negatives"]


# In[ ]:


df_train.head(2)


# In[ ]:


df_train.isnull().sum().any(), df_test.isnull().sum().any()


# In[ ]:


# scores = ['score_1', 'score_2', 'score_3', 'score_4', 'score_5', 'score_6']
# for col in scores:
#     print(df_train[col].value_counts())
# # score_6 column doesn't have uniform realistic values. Ignore this column in analysis


# In[ ]:


def num_words(df):
    df['num_words_pos'] = df['positives'].apply(lambda x: len(x.split()))
    df['num_words_neg'] = df['negatives'].apply(lambda x: len(x.split()))


# In[ ]:


num_words(df_train)
num_words(df_test)


# In[ ]:


df_train.columns


# In[ ]:


def SIAscores(df):
    SIA = SentimentIntensityAnalyzer()
    df["sentiments"] = df["Clean_reviews"].apply(lambda x: SIA.polarity_scores(x))
    return pd.concat([df.drop(['sentiments'], axis=1), df['sentiments'].apply(pd.Series)], axis=1)


# In[ ]:


# SIA.polarity_scores returns a dictionary of 4 scores for each sentence.
# {'neg': 0.0, 'neu': 0.404, 'pos': 0.596, 'comp': 0.7096}


# In[ ]:


df_train = SIAscores(df_train)
df_test = SIAscores(df_test)


# In[ ]:


df_train.shape, df_test.shape


# In[ ]:


df_train.columns


# In[ ]:


df_test.head(3)


# In[ ]:


dummy_cols=['place_enc','status_enc']
train_d = pd.get_dummies(data=df_train, columns=dummy_cols)
test_d  = pd.get_dummies(data=df_test, columns=dummy_cols)


# In[ ]:


len(train_d.columns), len(test_d.columns)


# In[ ]:


def drop_D2V(df):
    D2V = [col for col in df.columns if 'D2V_' in col]
    df.drop(columns=D2V, inplace=True)


# In[ ]:


drop_D2V(train_d)
drop_D2V(test_d)


# In[ ]:


# create doc2vec vector columns
def Create_Doc2Vec(df):
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(df["Clean_reviews"].apply(lambda x: x.split(" ")))]
    # train a Doc2Vec model with our text data
    model = Doc2Vec(documents, size=10, window=2, min_count=2, workers=4)
    # transform each document into a vector data
    doc2vec_df = df["Clean_reviews"].apply(lambda x: model.infer_vector(x.split(" "))).apply(pd.Series)
    doc2vec_df.columns = ["D2V_" + str(x) for x in doc2vec_df.columns]
    return pd.concat([df, doc2vec_df], axis=1)


# In[ ]:


train_d = Create_Doc2Vec(train_d)
test_d  = Create_Doc2Vec(test_d)


# In[ ]:


# tfidf = TfidfVectorizer(min_df = 3)
# tfidf_train = tfidf.fit_transform(df_train["Clean_reviews"]).toarray()
# tfidf_test  = tfidf.transform(df_test["Clean_reviews"]).toarray()

# def Create_TFIDF(df, tfidf_result):
#     tfidf_df = pd.DataFrame(tfidf_result, columns = tfidf.get_feature_names())
#     tfidf_df.columns = ["word_" + str(x) for x in tfidf_df.columns]
#     tfidf_df.index = df.index
#     return pd.concat([df, tfidf_df], axis=1)


# In[ ]:


# df_train = Create_TFIDF(df_train, tfidf_train)
# df_test  = Create_TFIDF(df_test,  tfidf_test)


# In[ ]:


train_d.columns


# In[ ]:


len(train_d.columns)


# In[ ]:


# feature selection
label = "overall"
ignore_cols = [label, 'Place', 'status', 'job_title', 'summary', 'positives', 'negatives', 'advice_to_mgmt', 
               'score_6', 'Clean_positives', 'Clean_negatives', 'Clean_reviews']
features = [c for c in train_d.columns if c not in ignore_cols]


# In[ ]:


len(features), train_d.shape, test_d.shape


# In[ ]:


X = train_d[features]
y = train_d[label]
X_test = test_d[features]


# In[ ]:


X.shape, y.shape, X_test.shape


# In[ ]:


# del df_train, df_test
# # , tfidf, tfidf_test, tfidf_train
# # deleted to save RAM
# import gc
# gc.collect()


# In[ ]:


# who_ls


# In[ ]:


def evaluate(model, train_x, val_x, train_y, val_y):
    model.fit(train_x,train_y)
    pred_y = model.predict(val_x)
    train_acc = model.score(train_x, train_y)
    test_acc = accuracy_score(val_y, pred_y)
    f1_sc = f1_score(val_y, pred_y, average='weighted')
    return train_acc, test_acc, f1_sc


# In[ ]:


# StratifiedKFold and Model Training & Evaluation
kfold = 6
skf = StratifiedKFold(n_splits=kfold,shuffle=True,random_state=7)
models = [
          LogisticRegression(n_jobs=-1, random_state=6), 
          XGBClassifier(random_state=5, n_jobs=-1),
          ExtraTreesClassifier(random_state=97, n_estimators=100, n_jobs=-1),
          LGBMClassifier(objective='multiclass', random_state=5)
         ]
scores_df = pd.DataFrame(index=range(kfold * len(models)))
df_row = []
for i, (train_idx, test_idx) in enumerate(skf.split(X, y)):
    X_train, X_val = X.loc[train_idx], X.loc[test_idx]
    y_train, y_val = y.loc[train_idx], y.loc[test_idx]
    print('[Fold: {}/{}]'.format(i + 1, kfold))
    for model in models:
        model_name = model.__class__.__name__
        trn, acc, f1 = evaluate(model, X_train, X_val, y_train, y_val)
        df_row.append((model_name, i, f1, acc, trn))
        
print('Training Done!')

#SVM model
#     model_SVC = LinearSVC(random_state=7)
# worse metric evaluation for SVM. Do not use it. 
    


# In[ ]:


scores_df = pd.DataFrame(df_row, columns=['model_name', 'fold_idx', 'F1_score', 'Test_acc', 'Train_acc'])
scores_df.sort_values(by=['model_name', 'fold_idx'], inplace=True)
scores_df.reset_index(drop=True, inplace=True)


# In[ ]:


scores_df


# In[ ]:


scores_df.groupby(['model_name'])['F1_score'].mean()


# Default parameters LogReg:
# >     Avg_CV_score: 0.4040081841492168, Avg_F1_score: 0.3763991552269393
# 
# Default parameters XGB:
# >     Avg_CV_score: 0.41343607919726366, Avg_F1_score: 0.39661000929134393
# 
# Default parameters DTC:
# >     Avg_CV_score: 0.3374539112115183, Avg_F1_score: 0.3376255378164512

# In[ ]:


models = [ LogisticRegression(n_jobs=-1, random_state=0), XGBClassifier(random_state=5, n_jobs=-1) ]
CV = 5
cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []
for model in models:
    model_name = model.__class__.__name__
    f1_scores = cross_val_score(model, X, y, scoring='f1_weighted', cv=CV)
    for cv_idx, f1 in enumerate(f1_scores):
        entries.append((model_name, cv_idx, f1))

cv_df = pd.DataFrame(entries, columns=['model_name', 'cv_idx', 'F1_score'])


# In[ ]:


cv_df


# In[ ]:


cv_df.groupby(['model_name'])['F1_score'].mean()


# > References: 
# > > https://towardsdatascience.com/detecting-bad-customer-reviews-with-nlp-d8b36134dc7e
# > > https://medium.com/@mishra.thedeepak/doc2vec-simple-implementation-example-df2afbbfbad5
# > > https://towardsdatascience.com/mapping-word-embeddings-with-word2vec-99a799dc9695
# > > https://medium.com/explore-artificial-intelligence/word2vec-a-baby-step-in-deep-learning-but-a-giant-leap-towards-natural-language-processing-40fe4e8602ba
# > > https://blog.insightdatascience.com/how-to-solve-90-of-nlp-problems-a-step-by-step-guide-fda605278e4e
# > > https://blog.insightdatascience.com/using-nlp-to-gain-insights-from-employee-review-data-da15687f311a
