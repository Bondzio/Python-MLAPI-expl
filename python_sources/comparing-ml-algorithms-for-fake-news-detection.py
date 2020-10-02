#!/usr/bin/env python
# coding: utf-8

# <h1><center>Fake News Detection with NLP and ML Models</center></h1>

# Fake news detection is an important classification problem in machine learning community. In this article, we present the implementation of fake news detection with 11 different ML models and compare their results. This notebook will definitely be helpful for beginners. Kindly upvote if you find it useful.

# Steps involved in fake news detection can be described as below. <center>Background Information --- Data Pre-processing --- Model Building<center>

# **1. Background Information :** Research suggests that fake news articles typically have longer titles and their contents are repetitive in nature.<br>
# **2. Data Pre-Processing :** Based on the hypothesis, we pre-processed the data so as to use number of words in title and count of words in text as features. (Using CountVectorizer)<br>
# **3. Model Building :** Multiple machine learning models (Logistic Regression, Random Forest, Light Gradient Boosting etc.) were built and hyperparameters were tuned.

# So, let's get started.

# # 1. Importing Libraries

# In[ ]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

import numpy as np
import pandas as pd
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import TruncatedSVD


get_ipython().system('pip install -q wordcloud')
import wordcloud

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[ ]:


from sklearn.model_selection import GridSearchCV


# # 2. Data Pre-processing

# In[ ]:


data = pd.read_csv('../input/fake-news-dataset/news.csv')


# In[ ]:


data.head()


# In[ ]:


data['label'].value_counts()   # No class imbalance


# In[ ]:


data = data.rename(columns = {'Unnamed: 0': 'Id'})     # Replacing the unnamed column with 'Id'


# In[ ]:


# Creating new feature : Number of words in news 'title'

def num_words(string):
    words = string.split()
    return len(words)

data['num_word_title'] = data['title'].apply(num_words)

print(data.groupby(data['label']).mean())

cols = ['title','num_word_title','text', 'label']
data = data[cols]


# In[ ]:


data.head()


# In[ ]:


data[data['num_word_title']>25].groupby('label').count()    # This clearly shows if title length is more than 25, it's highly likely to be a fake news.


# ## 2.1. Train-Test Split

# In[ ]:


# Function to split data into train and test set
def train_test_split(df, train_percent=.80, validate_percent=.20, seed=10):
    np.random.seed(seed)
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    train = df.iloc[perm[:train_end]]
    test = df.iloc[perm[train_end:]]
    return train, test


# In[ ]:


train, test = train_test_split(data[['num_word_title','text','label']], seed = 12)


# In[ ]:


train.shape, test.shape


# ## 2.2. Feature Generation (CountVectorizer)

# In[ ]:


# Necessary for lemmatization
class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


# In[ ]:


# CountVectorizer
count_vectorizer = CountVectorizer(stop_words = 'english', tokenizer=LemmaTokenizer(), 
                                   ngram_range = (1,2), dtype = np.uint8)

count_train = count_vectorizer.fit_transform(train['text'].values)


# In[ ]:


count_test = count_vectorizer.transform(test['text'].values)


# In[ ]:


"""
We won't use TfidfVectorizer. However, if any one wants to use it, pre-processing step is similar.
# TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize a TfidfVectorizer object: tfidf_vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words = 'english', max_df = 0.7, tokenizer=LemmaTokenizer(), 
                                   ngram_range = (1,2), dtype = np.float32)

# Transform the training data: tfidf_train 
tfidf_train = tfidf_vectorizer.fit_transform(train['text'].values)
# Transform the test data
tfidf_test = tfidf_vectorizer.transform(test['text'].values)
"""


# ## 2.3. Latent Semantic Analysis (For Dimensionality Reduction)

# In[ ]:


from sklearn.decomposition import TruncatedSVD


# In[ ]:


lsa_count = TruncatedSVD(n_components = 400, random_state = 20)
lsa_count.fit(count_train)
print(lsa_count.explained_variance_ratio_.sum())          # Explained_variance = 84.66 %


# In[ ]:


#count_train_df = pd.DataFrame.sparse.from_spmatrix(count_train, columns = count_vectorizer.get_feature_names())


# In[ ]:


count_train_lsa = pd.DataFrame(lsa_count.transform(count_train))
count_test_lsa = pd.DataFrame(lsa_count.transform(count_test))


# In[ ]:


# Adding number of words in news title as a feature
count_train_lsa['num_word_title'] = train['num_word_title'] / data['num_word_title'].max()
count_test_lsa['num_word_title'] = test['num_word_title'] / data['num_word_title'].max()


# In[ ]:


count_train_lsa.fillna(count_train_lsa.mean(), inplace = True)
count_test_lsa.fillna(count_test_lsa.mean(), inplace = True)


# In[ ]:


count_train_lsa.shape


# # 3. Model Building

# ## 3.1. Naive-Bayes Model

# In[ ]:


from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns


# In[ ]:


# Trying out with Gaussian Naive Bayes and CountVectorizer model
# Here we are iteratively doing grid search with different hyperparameters in an informed manner.
# params_NB = {'var_smoothing' : [1e-1, 1, 40, 100, 1000]} # var_smoothing = 40 gives the best result.
params_NB = {'var_smoothing' : [20,25,30,35,40,45, 50, 55, 60, 80]} # var_smoothing = 55 gives the best result.


# In[ ]:


clf_NB = GridSearchCV(estimator = GaussianNB(),param_grid = params_NB, cv = 3, refit = True, scoring = 'accuracy', n_jobs = 4)


# In[ ]:


clf_NB.fit(count_train_lsa, train['label'])


# In[ ]:


clf_NB.best_params_


# In[ ]:


clf_NB.best_score_


# In[ ]:


test_count_pred_NB = clf_NB.predict(count_test_lsa)


# In[ ]:


accuracy_score(test['label'], test_count_pred_NB)


# In[ ]:


cm_NB = confusion_matrix(test['label'], test_count_pred_NB, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_NB/ np.sum(cm_NB),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_NB = classification_report(test['label'], test_count_pred_NB, labels = ['FAKE','REAL'], output_dict = True)
count_report_NB = pd.DataFrame(count_report_NB).transpose()
count_report_NB


# ## 3.2. Logistic Regression

# In[ ]:


from sklearn.linear_model import LogisticRegression


# In[ ]:


params_LR = {'C' : [10, 5, 1,0.7, 0.5,0.3]}

# C = 0.5 gives the best result after Grid Search.


# In[ ]:


clf_LR = GridSearchCV(estimator = LogisticRegression(class_weight = 'balanced', random_state = 6),param_grid = params_LR, 
                      cv = 3, refit = True, scoring = 'accuracy', n_jobs = 4)


# In[ ]:


clf_LR.fit(count_train_lsa, train['label'])


# In[ ]:


clf_LR.best_score_


# In[ ]:


clf_LR.best_params_


# In[ ]:


test_count_pred_LR = clf_LR.predict(count_test_lsa)


# In[ ]:


cm_LR = confusion_matrix(test['label'], test_count_pred_LR, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_LR/ np.sum(cm_LR),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_LR = classification_report(test['label'], test_count_pred_LR, labels = ['FAKE','REAL'], output_dict = True)
count_report_LR = pd.DataFrame(count_report_LR).transpose()
count_report_LR


# ## 3.3. K-Nearest Neighbor Method

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier


# In[ ]:


# Here we are iteratively doing grid search with different hyperparameters in an informed manner.
# params_knn = {'n_neighbors' : [2, 4, 8, 16] } # We obtain 4 as the best hyperparameter.
params_knn = {'n_neighbors' : [3,4,5,6,7] }     # 5 is the final tuned hyperparameter.


# In[ ]:


clf_knn = GridSearchCV(estimator = KNeighborsClassifier(algorithm = 'ball_tree'), param_grid = params_knn, 
                       scoring = 'accuracy', n_jobs = 4, cv = 3, refit = True, verbose = 3)


# In[ ]:


clf_knn.fit(count_train_lsa, train['label'])


# In[ ]:


clf_knn.best_score_


# In[ ]:


clf_knn.best_params_


# In[ ]:


test_count_pred_knn = clf_knn.predict(count_test_lsa)


# In[ ]:


cm_knn = confusion_matrix(test['label'], test_count_pred_knn, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_knn/ np.sum(cm_knn),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_knn = classification_report(test['label'], test_count_pred_knn, labels = ['FAKE','REAL'], output_dict = True)
count_report_knn = pd.DataFrame(count_report_knn).transpose()
count_report_knn


# ## 3.4. Support Vector Machine Classifier

# In[ ]:


from sklearn.svm import SVC


# In[ ]:


# Here we are iteratively doing grid search with different hyperparameters in an informed manner.
# params_svc = {'kernel' : ['linear', 'poly', 'rbf', 'sigmoid'], 'C' : [0.1, 1, 50]} # 'rbf' and 50 give the best combination
# params_svc = {'kernel' : ['rbf', 'sigmoid'], 'C' : [10, 30, 50,100]}  # 100 and 'rbf' give the best combination.
params_svc = {'kernel' : ['rbf', 'sigmoid'], 'C' : [100, 150, 200]}   # 100 and 'rbf' give the best combination.


# In[ ]:


clf_svc = GridSearchCV(estimator = SVC(class_weight = 'balanced', random_state = 6), param_grid = params_svc, 
                       scoring = 'accuracy', n_jobs = 4, cv = 3, refit = True, verbose = 2)


# In[ ]:


clf_svc.fit(count_train_lsa, train['label'])


# In[ ]:


clf_svc.best_params_


# In[ ]:


clf_svc.best_score_


# In[ ]:


test_count_pred_svc = clf_svc.predict(count_test_lsa)


# In[ ]:


cm_svc = confusion_matrix(test['label'], test_count_pred_svc, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_svc/ np.sum(cm_svc),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_svc = classification_report(test['label'], test_count_pred_svc, labels = ['FAKE','REAL'], output_dict = True)
count_report_svc = pd.DataFrame(count_report_svc).transpose()
count_report_svc


# ## 3.5. Linear Discriminant Analysis

# In[ ]:


from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


# In[ ]:


params_LDA = {'solver' : ['svd', 'lsqr', 'eigen'], 'shrinkage' : ['auto', None]}

# (shrinkage = None and solver = svd) give the best result.


# In[ ]:


clf_LDA = GridSearchCV(estimator = LinearDiscriminantAnalysis(), param_grid = params_LDA, scoring = 'accuracy', n_jobs = 4,
                       cv = 3, refit = True, verbose = 2)


# In[ ]:


clf_LDA.fit(count_train_lsa, train['label'])


# In[ ]:


clf_LDA.best_params_


# In[ ]:


clf_LDA.best_score_


# In[ ]:


test_count_pred_LDA = clf_LDA.predict(count_test_lsa)


# In[ ]:


cm_LDA = confusion_matrix(test['label'], test_count_pred_LDA, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_LDA/ np.sum(cm_LDA),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_LDA = classification_report(test['label'], test_count_pred_LDA, labels = ['FAKE','REAL'], output_dict = True)
count_report_LDA = pd.DataFrame(count_report_LDA).transpose()
count_report_LDA


# ## 3.6. Decision Tree Classifier

# In[ ]:


from sklearn.tree import DecisionTreeClassifier


# In[ ]:


params_dt = {'criterion' : ['entropy'], 'min_samples_split' : [2, 4, 8, 16, 32], 
             'min_samples_leaf' : [1,2,4,8],'max_depth' : [4, 7, 10], 'max_features' : ['sqrt', None],  'class_weight' : ['balanced']}

# (max_depth = 7, min_samples_leaf = 4, min_samples_split = 32, max_features = None) give the best result.


# In[ ]:


clf_dt = GridSearchCV(estimator = DecisionTreeClassifier(random_state = 7), param_grid = params_dt, 
                      scoring = 'accuracy', n_jobs = 4, cv = 3, refit = True, verbose = 3)


# In[ ]:


clf_dt.fit(count_train_lsa, train['label'])


# In[ ]:


clf_dt.best_params_


# In[ ]:


clf_dt.best_score_


# In[ ]:


test_count_pred_dt = clf_dt.predict(count_test_lsa)


# In[ ]:


cm_dt = confusion_matrix(test['label'], test_count_pred_dt, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_dt/ np.sum(cm_dt),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_dt = classification_report(test['label'], test_count_pred_dt, labels = ['FAKE','REAL'], output_dict = True)
count_report_dt = pd.DataFrame(count_report_dt).transpose()
count_report_dt


# ## 3.7. Random Forest Classifier

# In[ ]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


params_RF = {'n_estimators' : [400, 1000, 1600], 'criterion' : ['entropy'], 'min_samples_split' : [2, 4, 8, 16], 
             'min_samples_leaf' : [1,2], 'class_weight' : ['balanced']}  

# (min_samples_leaf = 1, min_samples_split = 4 , n_estimators = 1000) give the best result.


# In[ ]:


clf_RF = GridSearchCV(estimator = RandomForestClassifier(oob_score = True, random_state = 7), param_grid = params_RF, 
                      scoring = 'accuracy', n_jobs = 4, cv = 3, refit = True, verbose = 2)


# In[ ]:


clf_RF.fit(count_train_lsa, train['label'])


# In[ ]:


clf_RF.best_params_


# In[ ]:


clf_RF.best_score_


# In[ ]:


test_count_pred_RF = clf_RF.predict(count_test_lsa)


# In[ ]:


cm_RF = confusion_matrix(test['label'], test_count_pred_RF, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_RF/ np.sum(cm_RF),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_RF = classification_report(test['label'], test_count_pred_RF, labels = ['FAKE','REAL'], output_dict = True)
count_report_RF = pd.DataFrame(count_report_RF).transpose()
count_report_RF


# ## 3.8. AdaBoost Classifier

# In[ ]:


from sklearn.ensemble import AdaBoostClassifier


# In[ ]:


# Here we are iteratively doing grid search with different hyperparameters in an informed manner.
# params_ada = {'n_estimators' : [50, 100, 500], 'learning_rate' : [1, 0.3]} # 500 and 1 give the best combination.
params_ada = {'n_estimators' : [500, 1000, 1500, 2000], 'learning_rate' : [1]} 
# (n_estimators = 1500, learning_rate = 1) is the best combination.


# In[ ]:


clf_ada = GridSearchCV(estimator = AdaBoostClassifier(random_state = 8), param_grid = params_ada, 
                       scoring = 'accuracy', n_jobs = 4, cv = 3, refit = True, verbose = 2)


# In[ ]:


clf_ada.fit(count_train_lsa, train['label'])


# In[ ]:


clf_ada.best_params_


# In[ ]:


clf_ada.best_score_


# In[ ]:


test_count_pred_ada = clf_ada.predict(count_test_lsa)


# In[ ]:


cm_ada = confusion_matrix(test['label'], test_count_pred_ada, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_ada/ np.sum(cm_ada),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_ada = classification_report(test['label'], test_count_pred_ada, labels = ['FAKE','REAL'], output_dict = True)
count_report_ada = pd.DataFrame(count_report_ada).transpose()
count_report_ada


# ## 3.9. Light Gradient Boosting Method 

# In[ ]:


import lightgbm as lgb


# In[ ]:


# Here we are iteratively doing grid search with different hyperparameters in an informed manner.
#params_lgb = {'n_estimators' : [100, 400, 800], 'learning_rate' : [0.03, 0.1], 'min_child_samples' : [4, 12, 24]}
# 800, 0.1 , 4 are the best ones.
#params_lgb = {'n_estimators' : [1200, 2400], 'learning_rate' : [ 0.1], 'min_child_samples' : [2,4]}  
# (n_estimators = 2400 and min_child_samples = 2) are the best ones.
# Let's just try with n_estimators 3600.
params_lgb = {'n_estimators' : [3600], 'learning_rate' : [ 0.1], 'min_child_samples' : [1,2]} 
# (n_estimators = 3600, learning_rate = 0.1, min_child_samples = 1) perform best.


# In[ ]:


clf_lgb = GridSearchCV(estimator = lgb.LGBMClassifier(), param_grid = params_lgb, scoring = 'accuracy', n_jobs = 4,
                       cv = 3, refit = True, verbose = 2)


# In[ ]:


clf_lgb.fit(count_train_lsa, train['label'])


# In[ ]:


clf_lgb.best_params_


# In[ ]:


print(clf_lgb.best_score_)


# In[ ]:


test_count_pred_lgb = clf_lgb.predict(count_test_lsa)   


# In[ ]:


cm_lgb = confusion_matrix(test['label'], test_count_pred_lgb, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_lgb/ np.sum(cm_lgb),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_lgb = classification_report(test['label'], test_count_pred_lgb, labels = ['FAKE','REAL'], output_dict = True)
count_report_lgb = pd.DataFrame(count_report_lgb).transpose()
count_report_lgb


# ## 3.10. CatBoosting

# In[ ]:


import catboost as cb


# In[ ]:


params_cat = {'n_estimators' : [800,1000,2000] }   #  2000 is the best one


# In[ ]:


clf_cat = GridSearchCV(estimator = cb.CatBoostClassifier(task_type = 'GPU', learning_rate = 0.2, max_depth = 6), param_grid = params_cat,
                       scoring = 'accuracy', n_jobs = 1, cv = 3, refit = True, verbose = 2 )


# In[ ]:


clf_cat.fit(count_train_lsa, train['label'])


# In[ ]:


clf_cat.best_params_


# In[ ]:


test_count_pred_cat = clf_cat.predict(count_test_lsa)


# In[ ]:


cm_cat = confusion_matrix(test['label'], test_count_pred_cat, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_cat/ np.sum(cm_cat),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_cat = classification_report(test['label'], test_count_pred_cat, labels = ['FAKE','REAL'], output_dict = True)
count_report_cat = pd.DataFrame(count_report_cat).transpose()
count_report_cat


# ## 3.11. TPOT Classifier (Genetic Algorithm)

# In[ ]:


from tpot import TPOTClassifier


# In[ ]:


clf_tpot = TPOTClassifier(generations = 6, population_size = 6, random_state = 3, cv = 2, n_jobs = 4)


# In[ ]:


clf_tpot.fit(count_train_lsa, train['label'])


# In[ ]:


clf_tpot.fitted_pipeline_


# In[ ]:


test_count_pred_tpot = clf_tpot.predict(count_test_lsa)


# In[ ]:


cm_tpot = confusion_matrix(test['label'], test_count_pred_tpot, labels = ['FAKE', 'REAL'])
sns.heatmap(cm_tpot/ np.sum(cm_tpot),fmt='.2%', annot=True, cmap = 'Blues', xticklabels = ['FAKE', 'REAL'], yticklabels = ['FAKE', 'REAL'])


# In[ ]:


from sklearn.metrics import classification_report

count_report_tpot = classification_report(test['label'], test_count_pred_tpot, labels = ['FAKE','REAL'], output_dict = True)
count_report_tpot = pd.DataFrame(count_report_tpot).transpose()
count_report_tpot


# We observe that boosting techniques like LGBM, CatBoost and AdaBoost gave good results. Also some linear techniques like Logistic Regression and SVM performed well.
