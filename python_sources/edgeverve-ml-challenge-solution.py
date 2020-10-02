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


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# In[ ]:


# Standard plotly imports
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import plotly.figure_factory as ff

# Using plotly + cufflinks in offline mode
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)


# In[ ]:


import string
import nltk
from nltk.corpus import stopwords 
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb
from sklearn.model_selection import StratifiedKFold
import re


# In[ ]:


get_ipython().system('ls ../input/88b2c062-9-dataset/Dataset')


# # Loading the dataset

# In[ ]:


df = pd.read_csv("../input/88b2c062-9-dataset//Dataset/Train.csv")
df_test = pd.read_csv("../input/88b2c062-9-dataset//Dataset/Test.csv")


# In[ ]:


df.shape, df_test.shape


# In[ ]:


df.info()


# In[ ]:


df_test.info()


# In[ ]:


df.head()


# # Understand the data

# In[ ]:


df['Product_Category'].iplot(kind='hist',
                             yTitle='count', 
                             title='Target Distribution', 
                             color='rgb(140,140,40)' )


# In[ ]:


df['Product_Category'].value_counts()


# In[ ]:


def draw_distribution(train_df, test_df, feature_name, top_counts=None):
    _tmp_material = (train_df[feature_name].value_counts() /df.shape[0] * 100) [:top_counts]
    tmp_trace = go.Bar(
                x=_tmp_material.index,
                y=_tmp_material.values,
                name='training_dataset',
            )

    _tmp_material_test = (test_df[feature_name].value_counts() / df_test.shape[0] * 100) [:top_counts]
    tmp_trace_test = go.Bar(
                x=_tmp_material_test.index,
                y=_tmp_material_test.values,
                name='test_dataset'
            )

    layout = go.Layout(
            barmode='group',
            title= " Train/Test " + feature_name + " distribution",
            yaxis=dict(
                title='Counts',
            ),
#             xaxis=dict(
#                 title=feature_name,
#             )

        )

    fig = go.Figure(data=[tmp_trace, tmp_trace_test], layout=layout)
    iplot(fig)


# In[ ]:


draw_distribution(df, df_test, 'GL_Code')


# In[ ]:


print("# of unique categories in GL_Code train dataset: ", df['GL_Code'].nunique())
print("# of unique categories in GL_Code test dataset: ", df_test['GL_Code'].nunique())


# In[ ]:


draw_distribution(df, df_test, 'Vendor_Code', 75)


# In[ ]:


print("# of unique categories in Vendor_Code train dataset: ", df['Vendor_Code'].nunique())
print("# of unique categories in Vendor_Code test dataset: ", df_test['Vendor_Code'].nunique())


# In[ ]:


group_labels = ['train distplot', 'test distplot']
hist_data = [df['Inv_Amt'].values, df_test['Inv_Amt']]
colors = ['#37AA9C','#37AA4C' ]

fig =ff.create_distplot(hist_data, group_labels,  colors=colors,  show_hist=False)
fig['layout'].update(title='Train/Test Inv_Amt Distribution Plot')
iplot(fig)


# # Missing Values:

# In[ ]:


df.isnull().sum()


# In[ ]:


df_test.isnull().sum()


# # Numerical encoding of categorical features:

# In[ ]:


for col in ['GL_Code', 'Vendor_Code']:
    print(col)
    le = LabelEncoder()
    le.fit(list(df[col]) + list(df_test[col]))
    df[col] = le.transform(df[col])
    df_test[col] = le.transform(df_test[col])


# # Create Feature Matrix (X) and target (y):

# In[ ]:


X = df.drop('Product_Category', axis=1)
y = df.Product_Category
target = LabelEncoder()
y_endoded = target.fit_transform(y)


#  

# # Model_1 with selected features:
# 
# ![Model_with_selected_features](https://github.com/asingleneuron/edgeverve_ml_challenge/blob/master/images/model_with_selected_feature.png?raw=True)

# In[ ]:


selected_features = ['GL_Code','Vendor_Code', 'Inv_Amt']


# In[ ]:


X_train, X_valid, y_train, y_valid = train_test_split(X[selected_features],y_endoded, test_size=0.3, random_state=1)


# # parameters of xgboost

# In[ ]:


param = {}
# use softmax multi-class classification
param['objective'] = 'multi:softprob'
param['eta'] = 0.1
param['max_depth'] = 6
param['silent'] = 1
param['nthread'] = 4
param['num_class'] = len(target.classes_)
param['eval_metric'] = ['mlogloss']
param['seed'] = 1


# In[ ]:


dtrain = xgb.DMatrix(X_train.values, label=y_train)
dvalid = xgb.DMatrix(X_valid.values, label=y_valid)
evallist = [(dtrain, 'train'), (dvalid, 'eval')]


# In[ ]:


clf = xgb.train(param, dtrain, 100, evallist, verbose_eval=50)


# In[ ]:


y_pred_valid = clf.predict(dvalid)
print("Accuracy : ",accuracy_score(y_valid, np.argmax(y_pred_valid, axis=1)))


# In[ ]:


xgb.plot_importance(clf, importance_type='gain');


# In[ ]:


dtest = xgb.DMatrix(df_test[selected_features].values)
y_test_pred = clf.predict(dtest)


# In[ ]:


output = df_test[['Inv_Id']].copy()
output['Product_Category'] = target.inverse_transform(np.argmax(y_test_pred, axis=1))


# In[ ]:


output.head()


# In[ ]:


print("Total Product Categories : {0} | predicted categories: {1} ".format(len(target.classes_), output['Product_Category'].nunique()))


# In[ ]:


output.to_csv("./product_category_submission_selected_features.csv", index=False)


# ### Test Accuracy: 0.89
# 
# ![test accuracy_with_selected_features](https://github.com/asingleneuron/edgeverve_ml_challenge/blob/master/images/selected_features.png?raw=True)

# In[ ]:





# # Model_2 ( BOW Features) :
# ![Model_with_selected_features](https://github.com/asingleneuron/edgeverve_ml_challenge/blob/master/images/mode_bow.png?raw=True)

# ### Add BOW(Bag of Words) Features :

# In[ ]:


stop_words = set(stopwords.words('english'))
def tokenize(text):
    '''
        Input: text
        Returns: clean tokens
        Desc:
            Generates a clean token of text (words) by first getting words from the text.
            Normalize the text by lowering it and removes the extra spaces, punctuation and stopwords.
    '''    
    txt = re.sub("[^A-Za-z]+", " ", text)
    tokens = txt.split()

    clean_tokens = []
    for tok in tokens:
        #
        if tok not in string.punctuation and tok not in stop_words:
            clean_tok = tok.lower().strip()
            clean_tokens.append(clean_tok)

    return clean_tokens


# In[ ]:


tfidf = TfidfVectorizer(tokenizer=tokenize, ngram_range=(1,2), use_idf=False, max_features=None)


# In[ ]:


tfidf.fit(X['Item_Description'])


# In[ ]:


X_bow = tfidf.transform(X['Item_Description'])
XTest_bow = tfidf.transform(df_test['Item_Description'])


# In[ ]:


X_train, X_valid, y_train, y_valid = train_test_split(X_bow,y_endoded, test_size=0.3, random_state=1)


# In[ ]:


dtrain = xgb.DMatrix(X_train, label=y_train)
dvalid = xgb.DMatrix(X_valid, label=y_valid)

evallist = [(dtrain, 'train'), (dvalid, 'eval')]

clf = xgb.train(param, dtrain, 100, evallist, verbose_eval=50)


# In[ ]:


y_pred_valid = clf.predict(dvalid)

print("Accuracy : ",accuracy_score(y_valid, np.argmax(y_pred_valid, axis=1)))


# In[ ]:


dtest = xgb.DMatrix(XTest_bow)
y_test_pred = clf.predict(dtest)


# In[ ]:


output['Product_Category'] = target.inverse_transform(np.argmax(y_test_pred, axis=1))


# In[ ]:


print("Total Product Categories : {0} | predicted categories: {1} "
    .format(len(target.classes_), output['Product_Category'].nunique()))


# In[ ]:


output.to_csv("./product_category_submission_bow_features.csv", index=False)


# ### Test Accuracy: 0.99
# 
# ![test accuracy_with_bow_features](https://github.com/asingleneuron/edgeverve_ml_challenge/blob/master/images/bow_features.png?raw=True)

# In[ ]:





# # Model_3 (OOF Prediction) : 
# ![OOF_Prediction](https://github.com/asingleneuron/edgeverve_ml_challenge/blob/master/images/OOF_PREDICTION.png?raw=True)
# 

# In[ ]:


num_splits = 5
skf = StratifiedKFold(n_splits= num_splits, random_state=1, shuffle=True)


# In[ ]:


y_test_pred = np.zeros((df_test.shape[0], len(target.classes_)))
print(y_test_pred.shape)
y_valid_scores = []
X = df['Item_Description']
fold_cnt = 1
dtest = xgb.DMatrix(XTest_bow)

for train_index, test_index in skf.split(X, y_endoded):
    print("\nFOLD .... ",fold_cnt)
    fold_cnt += 1
    
    X_train, X_valid = X.iloc[train_index], X.iloc[test_index]
    y_train, y_valid = y_endoded[train_index], y_endoded[test_index]
    
    X_train_bow = tfidf.transform(X_train)
    X_valid_bow = tfidf.transform(X_valid)
    
    dtrain = xgb.DMatrix(X_train_bow, label=y_train)
    dvalid = xgb.DMatrix(X_valid_bow, label=y_valid)

    evallist = [(dtrain, 'train'), (dvalid, 'eval')]

    clf = xgb.train(param, dtrain, 100, evallist, verbose_eval=50)
    #Predict validation data
    y_pred_valid = clf.predict(dvalid)
    y_valid_scores.append(accuracy_score(y_valid, np.argmax(y_pred_valid, axis=1)))
    
    #Predict test data
    y_pred = clf.predict(dtest)
    
    y_test_pred += y_pred


# In[ ]:


print("Validation Scores :", y_valid_scores)
print("Average Score: ",np.round(np.mean(y_valid_scores),3))


# In[ ]:


y_test_pred /= num_splits


# In[ ]:


output['Product_Category'] = target.inverse_transform(np.argmax(y_test_pred, axis=1))
print("Total Product Categories : {0} | predicted categories: {1} "
    .format(len(target.classes_), output['Product_Category'].nunique()))


# In[ ]:


output.to_csv("./product_category_submission_tfidf_oof.csv", index=False)


# ### Test Accuracy: 1.0
# 
# ![test accuracy_with_oof](https://github.com/asingleneuron/edgeverve_ml_challenge/blob/master/images/tfidf_oof.png?raw=True)

# In[ ]:




