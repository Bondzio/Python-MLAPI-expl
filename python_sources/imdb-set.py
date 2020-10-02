#!/usr/bin/env python
# coding: utf-8

# Imdb review sentiment classification
# 
# 25k positive + 25k negative ( no need to do class balancing )
# 
# Aim: maximize the expectation of correctly classified sentiment labels
# 
# Bag of word model
# Simplified representation assuming word are important, and order matter less
# Assume the order of word are not important
# 
# 
# 
# Traditional classifier
# 
# Clustering
# 
# Neural network
# Dense 50 * 3 layer
# 
# Network with embedding as input
# 
# Optimized model
# embedding
# 
# Further neural network
# Forward lstm
# Backward lstm (for test)
# Bidirectional lstm
# 
# Bert/Elmo
# 
# 
# 
# 

# In[ ]:





# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import nltk
from sklearn.feature_extraction import text
text.TfidfVectorizer


# Taken from kaggle End-to-End Text Processing for Beginners.
# https://www.kaggle.com/praveenkotha2/end-to-end-text-processing-for-beginners

# In[ ]:


# Reading the text data present in the directories. Each review is present as text file.
if True:#not (os.path.isfile('/kaggle/input/end-to-end-text-processing-for-beginners/train.csv' and 
    #                   '/kaggle/input/end-to-end-text-processing-for-beginners/test.csv')):
    path = '/kaggle/input/imdb-movie-reviews-dataset/aclimdb/aclImdb/'
    train_text = []
    train_label = []
    test_text = []
    test_label = []
    train_data_path_pos = os.path.join(path,'train/pos/')
    train_data_path_neg = os.path.join(path,'train/neg/')

    for data in ['train','test']:
        for label in ['pos','neg']:
            for file in sorted(os.listdir(os.path.join(path,data,label))):
                if file.endswith('.txt'):
                    with open(os.path.join(path,data,label,file)) as file_data:
                        if data=='train':
                            train_text.append(file_data.read())
                            train_label.append( 1 if label== 'pos' else 0)
                        else :
                            test_text.append(file_data.read())
                            test_label.append( 1 if label== 'pos' else 0)

    train_df = pd.DataFrame({'Review': train_text, 'Label': train_label})
    test_df = pd.DataFrame({'Review': test_text, 'Label': test_label})
    train_df = train_df.sample(frac=1).reset_index(drop=True)
    test_df = test_df.sample(frac=1).reset_index(drop=True)
    
    train_df.to_csv('train.csv')
    test_df.to_csv('test.csv')
    
else:
    train_df = pd.read_csv('/kaggle/input/end-to-end-text-processing-for-beginnerstrain.csv',index_col=0, chunksize=100000)
    test_df = pd.read_csv('/kaggle/input/end-to-end-text-processing-for-beginnerstest.csv',index_col=0, chunksize=100000)
    
print('The shape of train data:',train_df.shape)
print('The shape of test data:', test_df.shape) 


# In[ ]:


train_df.head()


# In[ ]:


from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import re

lemmer=WordNetLemmatizer()
#def lemmeterize(text):
#    return ' '.join([lemmer.lemmatize(lemmer.lemmatize(lemmer.lemmatize(lemmer.lemmatize(word, pos= wn.NOUN), pos= wn.ADJ), pos= wn.ADV), pos= wn.VERB) for word in text.split(' ')])
def lemmeterize(text):
    return ' '.join([lemmer.lemmatize(lemmer.lemmatize(lemmer.lemmatize(lemmer.lemmatize(word, pos= wn.NOUN), pos= wn.ADJ), pos= wn.ADV), pos= wn.VERB) for word in re.findall('(\w+|[\!\?]+)',text) if len(word)>2 or not word.isalnum()])


# In[ ]:


lemmeterize(train_df["Review"][1])


# In[ ]:


from multiprocessing import Pool
def parallelize_dataframe(df, func, n_cores=4):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


# In[ ]:


train_df["Review"] = train_df["Review"].apply(lambda x:x.lower()).apply(lemmeterize)
test_df["Review"] = test_df["Review"].apply(lambda x:x.lower()).apply(lemmeterize)


# In[ ]:


train_df.to_csv('train.csv')
test_df.to_csv('test.csv')


# In[ ]:


# Removing the duplicate rows
train_df_nodup = train_df.drop_duplicates(keep='first',inplace=False)
test_df_nodup = test_df.drop_duplicates(keep='first',inplace=False)
print('No of duplicate train rows that are dropped:',len(train_df)-len(train_df_nodup))
print('No of duplicate test rows that are dropped:',len(test_df)-len(test_df_nodup))


# In[ ]:


from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        self.tag_map = defaultdict(lambda : wn.NOUN)
        self.tag_map['J'] = wn.ADJ
        self.tag_map['V'] = wn.VERB
        self.tag_map['R'] = wn.ADV
        self.tokenizer = text.CountVectorizer().build_tokenizer()
    def __call__(self, articles):
        return [self.wnl.lemmatize(t,self.tag_map[tag[0]]) for t,tag in pos_tag(self.tokenizer(articles))]


# In[ ]:





# In[ ]:


import spacy
spacy.load('en')
lemmatizer = spacy.lang.en.English()
def my_tokenizer(doc):
    tokens = lemmatizer(doc)
    return([token.lemma_ for token in tokens])


# In[ ]:


count_vect = text.CountVectorizer(token_pattern=r"(?u)\b\w\w+\b|!|\?|\"|\'",max_df = 0.7, min_df=0.001,stop_words="english",strip_accents="unicode")#max_df = 0.7, min_df=0.0005
count_train =count_vect.fit_transform(train_df_nodup["Review"].transform(lambda x:x.lower()))
count_test = count_vect.transform(test_df_nodup["Review"].transform(lambda x:x.lower()))


# In[ ]:


count_vect.get_feature_names()


# In[ ]:


tfidf_trans = text.TfidfTransformer(sublinear_tf=True)
tfidf_train = tfidf_trans.fit_transform(count_train)
tfidf_test = tfidf_trans.transform(count_test)


# 

# 
# tfidf_train_vect = text.TfidfVectorizer(stop_words="english", max_df=0.7, min_df=0.001,strip_accents="unicode",tokenizer = LemmaTokenizer())
# tfidf_train = tfidf_train_vect.fit_transform(train_df_nodup["Review"])
# tfidf_test = tfidf_train_vect.transform(test_df_nodup["Review"])

# In[ ]:


tfidf_train.shape


# In[ ]:


for i,j in count_vect.vocabulary_.items():
    if j<10: print(i,j)


# In[ ]:


count_vect.stop_words_


# In[ ]:


one_train = count_train.copy()
one_train[one_train.nonzero()[0],one_train.nonzero()[1]] =1
one_test = count_test.copy()
one_test[one_test.nonzero()[0],one_test.nonzero()[1]] =1


# In[ ]:


import sklearn
import sklearn.decomposition
from scipy import sparse
input_datas = [(one_train,one_test),(count_train,count_test),(tfidf_train,tfidf_test)]
for pca_train,pca_test in input_datas:
    models = [
        #linear_model.BayesianRidge(),
        #sklearn.naive_bayes.GaussianNB(),
        linear_model.LogisticRegression(),
    ]
    """
    if getattr(tfidf_train,"toarray",None):
        tfidf_train = tfidf_train.toarray()
        tfidf_test = tfidf_test.toarray()
    """
    for i in  models:
        i.fit(pca_train,train_df_nodup["Label"])
        if getattr(i,"predict",None):
            result = i.predict(pca_test)
        elif getattr(i,"transform",None):
            result = i.transform(pca_test)
        else:
            raise Exception
        acc = metrics.accuracy_score(test_df_nodup["Label"],result)
        print(f"model {i}: {acc}")


# In[ ]:


get_ipython().run_cell_magic('time', '', 'from sklearn import linear_model\nfrom sklearn import metrics\nimport sklearn.mixture\nimport sklearn.naive_bayes\nimport sklearn.svm\nimport sklearn.neighbors\nimport sklearn.neural_network\nimport xgboost as xgb\nimport lightgbm\nmodels0 = [\n    #linear_model.BayesianRidge(),\n    sklearn.naive_bayes.GaussianNB(),\n    linear_model.LogisticRegression(),\n    #linear_model.RidgeClassifierCV(),\n    #sklearn.neighbors.KNeighborsClassifier(),\n    #sklearn.neural_network.MLPClassifier(hidden_layer_sizes=(16,16),activation="logistic") #16,16\n    #xgb.XGBClassifier(),\n    #lightgbm.LGBMClassifier()\n    #linear_model.RidgeClassifierCV(),\n    sklearn.svm.LinearSVC(),\n]\n#"""\nif getattr(tfidf_train,"toarray",None):\n    tfidf_train = tfidf_train.toarray()\n    tfidf_test = tfidf_test.toarray()\n#"""\nfor i in  models0:\n    i.fit(tfidf_train,train_df_nodup["Label"])\n    if getattr(i,"predict",None):\n        result = i.predict(tfidf_test)\n    elif getattr(i,"transform",None):\n        result = i.transform(tfidf_test)\n    else:\n        raise Exception\n    acc = metrics.accuracy_score(test_df_nodup["Label"],result)\n    print(f"model {i}: {acc}")')


# 

# In[ ]:


tfidf_train.shape


# In[ ]:


import sklearn
import sklearn.decomposition
from scipy import sparse
dims = [500,300,200,100,50,10,5,3]
for j in dims:
    pca = sklearn.decomposition.TruncatedSVD(n_components =j) #300 dim Glove
    pca_train = pca.fit_transform(tfidf_train)#.toarray())
    pca_test = pca.transform(tfidf_test)#.toarray())
    models = [
        #linear_model.BayesianRidge(),
        sklearn.naive_bayes.GaussianNB(),
        linear_model.LogisticRegressionCV(),
    ]
    """
    if getattr(tfidf_train,"toarray",None):
        tfidf_train = tfidf_train.toarray()
        tfidf_test = tfidf_test.toarray()
    """
    for i in  models:
        i.fit(pca_train,train_df_nodup["Label"])
        if getattr(i,"predict",None):
            result = i.predict(pca_test)
        elif getattr(i,"transform",None):
            result = i.transform(pca_test)
        else:
            raise Exception
        acc = metrics.accuracy_score(test_df_nodup["Label"],result)
        print(f"model {i}: {acc}")


# In[ ]:


import sklearn
import sklearn.decomposition
from scipy import sparse
pca = sklearn.decomposition.TruncatedSVD(n_components =300) #300 dim Glove
pca_train = pca.fit_transform(tfidf_train)#.toarray())
pca_test = pca.transform(tfidf_test)#.toarray())


# import sklearn.manifold
# dim = sklearn.manifold.LocallyLinearEmbedding(n_components=3)#sklearn.manifold.TSNE(3)
# output = dim.fit_transform(np.concatenate([tfidf_train,tfidf_test]))
# tfidf_train,tfidf_test = output[:tfidf_train.shape[0]],output[tfidf_train.shape[0]:]

# In[ ]:


get_ipython().run_cell_magic('time', '', 'from sklearn import linear_model\nfrom sklearn import metrics\nimport sklearn.mixture\nimport sklearn.naive_bayes\nimport sklearn.svm\nimport sklearn.neighbors\nimport sklearn.neural_network\nimport xgboost as xgb\nimport lightgbm\nmodels = [\n    #linear_model.BayesianRidge(),\n    sklearn.naive_bayes.GaussianNB(),\n    linear_model.LogisticRegressionCV(),\n    #sklearn.neighbors.KNeighborsClassifier(),\n    linear_model.PassiveAggressiveClassifier(),\n    linear_model.Perceptron(),\n    linear_model.RidgeClassifierCV(),\n    sklearn.neural_network.MLPClassifier(hidden_layer_sizes=(16,16),activation="logistic"), #16,16\n    xgb.XGBClassifier(),\n    lightgbm.LGBMClassifier(),\n    #linear_model.RidgeClassifier(),\n    sklearn.svm.LinearSVC(),\n]\n"""\nif getattr(tfidf_train,"toarray",None):\n    tfidf_train = tfidf_train.toarray()\n    tfidf_test = tfidf_test.toarray()\n"""\nfor i in  models:\n    i.fit(pca_train,train_df_nodup["Label"])\n    if getattr(i,"predict",None):\n        result = i.predict(pca_test)\n    elif getattr(i,"transform",None):\n        result = i.transform(pca_test)\n    else:\n        raise Exception\n    acc = metrics.accuracy_score(test_df_nodup["Label"],result)\n    print(f"model {i}: {acc}")')


# In[ ]:


np.array(result).shape


# In[ ]:


result = []
train_result = []
for i in  models0:
 
    if getattr(i,"predict_proba",None):
        result.append(i.predict_proba(tfidf_test)[:,0])
        train_result.append(i.predict_proba(tfidf_train)[:,0])
    elif getattr(i,"predict",None):
        result.append(i.predict(tfidf_test))
        train_result.append(i.predict(tfidf_train))
    elif getattr(i,"transform",None):
        result = i.transform(tfidf_test)
    else:
        raise Exception
for i in  models[:-2]:
 
    if getattr(i,"predict_proba",None):
        result.append(i.predict_proba(pca_test)[:,0])
        train_result.append(i.predict_proba(pca_train)[:,0])
    elif getattr(i,"predict",None):
        result.append(i.predict(pca_test))
        train_result.append(i.predict(pca_train))
    elif getattr(i,"transform",None):
        result = i.transform(pca_test)
    else:
        raise Exception
        
xgb_stack = xgb.XGBClassifier()    
xgb_stack.fit(np.stack(train_result).T,train_df_nodup["Label"])
result = xgb_stack.predict(np.stack(result).T)
acc = metrics.classification_report(test_df_nodup["Label"],result)
    
print(acc)
acc = metrics.accuracy_score(test_df_nodup["Label"],result)
    
print(acc)


# Top 10 weighting words

# In[ ]:


from seaborn import barplot
lr = linear_model.LogisticRegressionCV()
lr.fit(pca_train,train_df_nodup["Label"])
coef=pca.inverse_transform(lr.coef_)[0]
ind = np.argsort(np.abs(coef))[-20:]#, -20
names = np.array(count_vect.get_feature_names())[ind]
print(*zip(names,coef[ind]))
barplot(names,coef[ind])


# In[ ]:


from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color='white', 
                      max_words=300
                         ).fit_words(dict(zip(count_vect.get_feature_names(),-coef)))
plt.clf()
plt.imshow(wordcloud)
plt.axis('off')
plt.show()


# In[ ]:


pca.explained_variance_ratio_


# Word to vector

# In[ ]:


def read_data(file_name,s):
    with open(file_name,'r') as f:
        word_vocab = set() # not using list to avoid duplicate entry
        word2vector = {}
        for line in f:
            line_ = line.strip() #Remove white space
            words_Vec = line_.split()
            if words_Vec[0] in s:
                word_vocab.add(words_Vec[0])
                word2vector[words_Vec[0]] = np.array(words_Vec[1:],dtype=float)
    print("Total Words in DataSet:",len(word_vocab))
    return word_vocab,word2vector


# In[ ]:


vocab, w2v = read_data("/kaggle/input/glove-global-vectors-for-word-representation/glove.6B.200d.txt",set(count_vect.get_feature_names()))


# In[ ]:


dimm = 100


# In[ ]:


w2v["000"]


# In[ ]:


word_vec = np.stack([w2v[i] if i in w2v else np.zeros(dimm) for i in count_vect.get_feature_names() ])


# In[ ]:


del w2v, vocab


# In[ ]:


del models


# In[ ]:


k =  np.mean(tfidf_train,axis=1)


# In[ ]:


np.mean(tfidf_train,axis=1)


# In[ ]:


w2v_train = tfidf_train@word_vec#/ np.mean(count_train,axis=1)
w2v_test = tfidf_test@word_vec #/ np.mean(count_test,axis=1)


# In[ ]:


tfidf_train.shape, w2v_train.shape


# In[ ]:


w2v_train.shape


# w2v_train = np.concatenate([w2v_train,tfidf_train],axis=1)
# w2v_test = np.concatenate([w2v_test,tfidf_test],axis=1)

# In[ ]:


w2v_train.shape


# In[ ]:


get_ipython().run_cell_magic('time', '', 'from sklearn import linear_model\nfrom sklearn import metrics\nimport sklearn.mixture\nimport sklearn.naive_bayes\nimport sklearn.svm\nimport sklearn.neighbors\nimport sklearn.neural_network\nimport xgboost as xgb\nimport lightgbm\nmodels = [\n    #linear_model.BayesianRidge(),\n    #sklearn.naive_bayes.GaussianNB(),\n    linear_model.LogisticRegression(),\n    #linear_model.PassiveAggressiveClassifier(),\n    #linear_model.Perceptron(),\n    #linear_model.RidgeClassifierCV(),\n    #sklearn.neighbors.KNeighborsClassifier(),\n    #sklearn.neural_network.MLPClassifier(hidden_layer_sizes=(128,64),activation="logistic") #16,16\n    #xgb.XGBClassifier(),\n    #lightgbm.LGBMClassifier()\n    #linear_model.RidgeClassifierCV(),\n    #sklearn.svm.LinearSVC(),\n]\n"""\nif getattr(tfidf_train,"toarray",None):\n    tfidf_train = tfidf_train.toarray()\n    tfidf_test = tfidf_test.toarray()\n"""\nfor i in  models:\n    i.fit(w2v_train,train_df_nodup["Label"])\n    if getattr(i,"predict",None):\n        result = i.predict(w2v_test)\n    elif getattr(i,"transform",None):\n        result = i.transform(w2v_test)\n    else:\n        raise Exception\n    acc = metrics.accuracy_score(test_df_nodup["Label"],result)\n    print(f"model {i}: {acc}")')


# In[ ]:


tfidf_train[0]


# In[ ]:


def my_reset(*varnames):
    """
    varnames are what you want to keep
    """
    globals_ = globals()
    to_save = {v: globals_[v] for v in varnames}
    to_save['my_reset'] = my_reset  # lets keep this function by default
    del globals_
    get_ipython().magic("reset")
    globals().update(to_save)


# In[ ]:


my_reset("g")


# In[ ]:


import gc
gc.collect()

