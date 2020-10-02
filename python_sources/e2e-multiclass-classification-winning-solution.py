#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline, FeatureUnion
import xgboost as xgb


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# In[ ]:


from sklearn.base import BaseEstimator, TransformerMixin


# In[ ]:


import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode

init_notebook_mode(connected = True)
# for offline plots
import cufflinks
cufflinks.go_offline(connected = True)


# # Load Dataset

# In[ ]:


get_ipython().system('ls ../input/ericsson-ml-challenge-materialtype-prediction/')


# In[ ]:


df_train = pd.read_csv("../input/ericsson-ml-challenge-materialtype-prediction/train_file.csv")
df_test = pd.read_csv("../input/ericsson-ml-challenge-materialtype-prediction/test_file.csv")


# In[ ]:


df_train.shape, df_test.shape


# In[ ]:


df_train.columns


# In[ ]:


df_train.head()


# In[ ]:


df_train.info()


# In[ ]:


df_train.describe()


# In[ ]:


## UsageClass, CheckoutType, CheckoutYear, CheckoutMonth has unique entries. Hence that would not be useful for analysis
df_train.UsageClass.unique()


# In[ ]:


df_train.CheckoutType.unique()


# In[ ]:


df_train.CheckoutYear.unique()


# In[ ]:


df_train.CheckoutMonth.unique()


# In[ ]:


plt.figure(figsize = (15,5))
plt.subplot(2,2,1)
sns.countplot(x ='UsageClass', data = df_train)

plt.subplot(2,2,2)
sns.countplot(x ='CheckoutType', data = df_train)

plt.subplot(2,2,3)
sns.countplot(x= 'CheckoutYear', data = df_train)

plt.subplot(2,2,4)
sns.countplot(x ='CheckoutMonth', data = df_train)


# In[ ]:


## Checking the above 4 columns in test dataset and we have unique values in test set too

plt.figure(figsize = (15,5))
plt.subplot(2,2,1)
sns.countplot(x ='UsageClass', data = df_test)

plt.subplot(2,2,2)
sns.countplot(x ='CheckoutType', data = df_test)

plt.subplot(2,2,3)
sns.countplot(x= 'CheckoutYear', data = df_test)

plt.subplot(2,2,4)
sns.countplot(x ='CheckoutMonth', data = df_test)


# # EDA

# In[ ]:


## function for plotting categorical variables count

def categorical_feature_distribution(feature_name, target_name, top_counts = None):
    material_trace =[]
    
    for material in df_train[target_name].unique():
        if not top_counts:
            tmp_material = df_train[df_train[target_name]==material][feature_name].value_counts()
        else:
            tmp_material = df_train[df_train[target_name]==material][feature_name].value_counts()[:top_counts]
        
        tmp_trace = go.Bar(
                        x = tmp_material.index,
                        y = tmp_material.values,
                        name = material
                        )
        material_trace.append(tmp_trace)
        
    layout = go.Layout(
                barmode ='group',
                title =feature_name + ' vs ' + target_name +' - Distribution',
                yaxis = dict(title = 'Counts'),
                xaxis = dict(title = feature_name)
                    )
    
    fig = go.Figure(data = material_trace, layout = layout)
    iplot(fig, filename ='grouped-bar')
    


# In[ ]:


import plotly
plotly.offline.init_notebook_mode()
df_train['MaterialType'].iplot(kind='hist', xTitle='Material Types',
                              yTitle ='Count', title ='Target Distribution')


# In[ ]:


categorical_feature_distribution('Checkouts','MaterialType')


# In[ ]:


len(df_train['Creator'].unique()) # There are totally 6k creators, lets view 20 creators


# In[ ]:


categorical_feature_distribution('Creator','MaterialType',20)


# In[ ]:


len(df_train['Publisher'].unique())


# In[ ]:


categorical_feature_distribution('Publisher','MaterialType',20) # Lets view only 20 publishers


# In[ ]:


len(df_train['Subjects'].unique())


# In[ ]:


categorical_feature_distribution('Subjects','MaterialType',20)


# In[ ]:


## Creating wordclouds

def create_wordcloud(material):
    title = " ".join(t for t in df_train[df_train['MaterialType']==material]['Title'])
    print("There are totally {} words".format(len(title)))
    wordcloud = WordCloud(width = 1000, height = 400, margin = 0).generate(title)
    
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation ='bilinear')
    plt.axis('off')
    #plt.margins(x =0 , y=0)
    plt.show()


# In[ ]:


create_wordcloud('BOOK')


# In[ ]:


create_wordcloud('SOUNDDISC')


# In[ ]:


create_wordcloud('VIDEODISC')


# In[ ]:


create_wordcloud('CR')


# # Missing data handling

# In[ ]:


(df_train.isnull().sum() / df_train.shape[0])*100


# In[ ]:


df_test.isnull().sum()/df_test.shape[0] *100


# In[ ]:


## imputing as nopublisher, nocreater, nosubject

df_train['Publisher'].fillna('NoPublisher', inplace = True)
df_test['Publisher'].fillna('NoPublisher', inplace = True)

df_train['Subjects'].fillna('NoSubjects', inplace = True)
df_test['Subjects'].fillna('NoSubjects', inplace = True)

df_train['Creator'].fillna('NoCreator', inplace = True)
df_test['Creator'].fillna('NoCreator', inplace = True)


# In[ ]:


df_train.isnull().sum(), df_test.isnull().sum()


# 
# # Pipeline
# 
# ![Pipeline](https://github.com/asingleneuron/Ericsson-Machine-Learning-Challenge/blob/master/images/PIPELINE.jpg?raw=True)
# 
# Reference: https://www.youtube.com/watch?v=DW6gUvb8U8c&t=12s

# Create info column as combination of - Title, Subjects, Publisher, Creator

# In[ ]:


df_train['info'] = df_train['Title'] +' '+ df_train['Subjects']+' '+df_train['Publisher']+' '+ df_train['Creator']
df_test['info'] = df_test['Title']+' '+df_test['Subjects']+' '+df_test['Publisher']+' '+df_train['Creator']


# Numerical encode categorical features

# In[ ]:


target_encoder = LabelEncoder()
y = target_encoder.fit_transform(df_train['MaterialType'])

categorical_features = ['Checkouts','Creator','Subjects','Publisher']

for col in categorical_features:
    print(col)
    le = LabelEncoder()
    le.fit(list(df_train[col]) + list(df_test[col]))
    df_train[col] = le.transform(df_train[col])
    df_test[col] = le.transform(df_test[col])
    


# Add some functions and transformer class

# In[ ]:


stopwords = set(stopwords.words('english'))


# In[ ]:


def tokenize(text):
    '''
        Input: text
        Returns: clean tokens
        Desc:
            Generates a clean token of text (words) by first getting words from the text.
            Applies Lemmatization on the words.
            Normalize the text by lowering it and removes the extra spaces.
    '''
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        #
        if tok not in string.punctuation:# and tok not in stop_words:
            clean_tok = tok.lower().strip()
            #clean_tok = lemmatizer.lemmatize(tok).lower().strip()
            clean_tokens.append(clean_tok)

    return clean_tokens


# In[ ]:


class TextLengthExtractor(BaseEstimator, TransformerMixin):
    '''
        Input: X
        return: pandas series of length of text
        TextLengthExtractor is a transformer , can be used in pipeline to extract the length of the text from a given input.
        Input can be an array of text or pandas Series.
    '''

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return pd.Series(X).apply(lambda x: len(x)).values.reshape(-1,1)


# In[ ]:


class WordCountExtractor(BaseEstimator, TransformerMixin):
    '''
        Input: X
        return: pandas series of word count
        WordCountExtractor is a transformer , can be used in pipeline to extract the number of words of the text from a given input.
        Input can be an array of text or pandas Series.
    '''
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return pd.Series(X).apply(lambda x: len(x.split())).values.reshape(-1,1)
    


# In[ ]:


class MessageExtractor(BaseEstimator, TransformerMixin):        
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X["info"]
    
    


# In[ ]:


class FeatureSelector( BaseEstimator, TransformerMixin ):
    #Class Constructor     
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        return X[ [ 'Checkouts','Creator','Publisher','Subjects'] ] 


# # Pipeline

# In[ ]:


pipeline = Pipeline([
        ('features', FeatureUnion([

            ('text_pipeline', Pipeline([
                ('text', MessageExtractor()),
                ('tfidf', TfidfVectorizer(tokenizer=tokenize,
                                         ngram_range=(1,2),
                                         max_df=0.5,
                                         max_features=5000,
                                         use_idf=False)),
            ])),
            
            ('categorical_features', Pipeline([
                ('cat_features', FeatureSelector()),
                
            ])),
            
            ('text_length_pipeline', Pipeline([
                ('text', MessageExtractor()),
                ('text_len', TextLengthExtractor()),
                
            ])),

            ('word_count_pipeline', Pipeline([
                ('text', MessageExtractor()),
                ('word_count', WordCountExtractor()),                
            ])),

        ])),
        
]) 


# In[ ]:


pipeline.fit(df_train)


# In[ ]:


XTest_trans = pipeline.transform(df_test)
dxtest = xgb.DMatrix(XTest_trans)


# In[ ]:


XTest_trans.todense()


# # XGB parameters

# In[ ]:


param = {'objective':'multi:softprob',
        'eta':0.1,
        'max_depth':6,
        'silent':1,
        'nthread':4,
        'num_class':8,
        'eval_metric':['mlogloss'],
        'seed':1}


# # OOF
# 
# ![OOF](https://github.com/asingleneuron/Ericsson-Machine-Learning-Challenge/blob/master/images/OOF_PREDICTION.png?raw=True)
# 
# Reference: https://www.youtube.com/watch?v=DW6gUvb8U8c&t=12s

# In[ ]:


num_splits = 5
skf = StratifiedKFold(n_splits = num_splits, shuffle = True, random_state=1)


# In[ ]:


y_test_pred = np.zeros((df_test.shape[0],8))
print(y_test_pred.shape)
y_valid_scores =[]

X = df_train
fold_cnt = 1
for train_index, val_index in skf.split(X, y):
    print("Fold....", fold_cnt)
    fold_cnt+=1
    
    X_train, X_valid = X.iloc[train_index], X.iloc[val_index]
    y_train, y_valid = y[train_index], y[val_index]
    
    X_train_trans = pipeline.transform(X_train)
    dtrain = xgb.DMatrix(X_train_trans, label = y_train)
    
    X_valid_trans = pipeline.transform(X_valid)
    dvalid = xgb.DMatrix(X_valid_trans, label = y_valid)
    
    evallist = [(dtrain, 'train'), (dvalid,'valid')]
    
    num_round = 10000
    bst = xgb.train(param, dtrain, num_round, evallist, early_stopping_rounds=10, verbose_eval = 50)
    
    #prediction -oof
    y_pred_valid = bst.predict(dvalid, ntree_limit = bst.best_ntree_limit)
    y_valid_scores.append(f1_score(y_valid, np.argmax(y_pred_valid, axis = 1), average = 'weighted'))
    
    #prediction -test set
    
    y_pred = bst.predict(dxtest, ntree_limit = bst.best_ntree_limit)
    y_test_pred += y_pred
    
    


# In[ ]:


y_test_pred /= num_splits


# In[ ]:


y_valid_scores


# In[ ]:


np.mean(y_valid_scores)


# # Output

# In[ ]:


pred_material = np.argmax(y_test_pred, axis = 1)
output = df_test[['ID']].copy()
output['MaterialType'] = target_encoder.inverse_transform(pred_material)


# In[ ]:


output.MaterialType.unique()


# Reference:
# I would like to give complete credit to Shobhit upadhyaya for sharing his solution and dataset https://www.youtube.com/watch?v=DW6gUvb8U8c&t=12s
# 
# 

# In[ ]:




