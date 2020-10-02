#!/usr/bin/env python
# coding: utf-8

# **This notebook is for basic feature selection methods and appling different algorithms**
# * If you find this helpful upvote it and for any queries feel free to comment down.

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


import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


#reading dataset
df = pd.read_csv("/kaggle/input/breast-cancer-wisconsin-data/data.csv")


# In[ ]:


#take quick look at our dataset
df.head()


# In[ ]:


df.info()


# * Dataset has 33 columns out of which 32 are type float64 and one column is object type.
# * Unnamed: 32 column has all NaN values.
# * We will remove the id and Unnamed : 32 columns.
# 

# In[ ]:


dropout = ['Unnamed: 32', 'id'] #selecting columns to drop
df.drop(dropout, axis=1, inplace=True)


# Class label diagnosis is object type so we have to convert it into int. We will do this by mapping values 0 for Malignant and 1 for Benign.

# In[ ]:


mappings = {'M': 0, "B": 1} #mapping for diagnosis column
df.replace({"diagnosis": mappings}, inplace=True)


# In[ ]:


#Let's look at the class distribution of diagnosis column
sns.countplot(df['diagnosis'])


# In[ ]:


corr_matrix = df.corr() #correlation between variables
corr_matrix


# In[ ]:


#Looking at correlation matrix is overwhelming so let's plot the correlation matrix.
plt.figure(figsize=(18,18))
sns.heatmap(corr_matrix, annot=True)
plt.show()


# * Meaning of correlation 1 means, they are positively correlated.
# * Meaning of correaltion 0 means, they are not having any correlion at all.
# * Meaning of correlation -1 means, they are negatively correlated.

# In[ ]:


corr_matrix['diagnosis'].sort_values(ascending=False)


# Looking at correlation between class label(diagnosis) and every other variables, we can see that only four variables are positively correlated and every other variables are negatively correlated with the class label(diagnosis).

# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


# In[ ]:


def train_models(X_train, y_train, X_test, y_test, X, y):
    '''training models and gathering accuracy score and cross validation score for each model'''
    #Algorithms we are going to use
    models = [LogisticRegression(random_state=42, max_iter=150), SVC(kernel='linear', C=1), 
            RandomForestClassifier(n_estimators=20)]
    model_names = ['logisticRegression', 'SupportVectorClassifier', 'RandomForest']
    accuracy = []
    cross_score = [] 
    for model in models:
        model.fit(X_train, y_train)
        accuracy.append(accuracy_score(y_test, model.predict(X_test)))
        cross_score.append(cross_val_score(model, X, y, cv=5).mean())
        
    result_df = pd.DataFrame(list(zip(accuracy, cross_score)),columns=['accuracy','cross_score'], index=model_names)
        
    return result_df


# * First we have created function which takes train set, test set , X (all features) and y (label) and this function returns dataframe containing accuracy score and cross validation score of each algorithm.
# * We are going to use LogisticRegression, SupportVectorClassifier and RandomForest algorithms.

# **Selecting Features depends on Correlation**

# In[ ]:


#selecting columns which has correlation less than 0.9
columns = np.full((corr_matrix.shape[0],), True, dtype=bool)
for i in range(corr_matrix.shape[0]):
    for j in range(i+1, corr_matrix.shape[0]):
        if corr_matrix.iloc[i,j] >= 0.9:
            if columns[j]:
                columns[j] = False


# In[ ]:


selected_columns = df.columns[columns] #these are the columns which has correlation less that 0.9
selected_columns


# In[ ]:


copy_df = df[selected_columns].copy()


# In[ ]:


X = np.array(copy_df.drop('diagnosis', axis=1))
y = np.array(copy_df['diagnosis'])

#train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# In[ ]:


corr_result = train_models(X_train, y_train, X_test, y_test, X, y)
corr_result


# * Accuracy score of LogisticRegression is 0.92 and Cross Validation Score is 0.92.
# * Accuracy score of SupportVectorClassifier is 0.90 and Cross Validation Score is 0.94.
# * Accuracy score of RandomForest is 0.93 and Cross Validation Score is 0.95.

# **Forward Feature Selection**

# In[ ]:


new_df = df.copy() #copy df

X = new_df.drop('diagnosis', axis=1)
y = new_df['diagnosis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) #train test split


# In[ ]:


def evaluate_metric(X_test, y_test, model):
    """Evalutaion metric for our classifier"""
    accuracy = accuracy_score(y_test, model.predict(X_test))
    return accuracy


# In[ ]:


def forward_feature_selection(X_train, X_test, y_train, y_test, n):
    """Forward feature selection return set of features"""
    feature_set = []
    for num_features in range(n):
        metric_list = []
        model = LogisticRegression(random_state=42)
        for feature in X_train.columns:
            if feature not in feature_set:
                f_set = feature_set.copy()
                f_set.append(feature)
                model.fit(X_train[f_set], y_train)
                metric_list.append((evaluate_metric(X_test[f_set], y_test, model), feature))
        metric_list.sort(key=lambda x : x[0], reverse = True)
        feature_set.append(metric_list[0][1])
    return feature_set


# In[ ]:


forward_selection_selected_features = forward_feature_selection(X_train, X_test, y_train, y_test, 10) #selecting top 10 features 
forward_selection_selected_features 


# In[ ]:


new_df = new_df[forward_selection_selected_features]


# In[ ]:


forward_result = train_models(X_train, y_train, X_test, y_test, new_df, y)
forward_result


# * Accuracy score of LogisticRegression is 0.92 and Cross Validation Score is 0.94.
# * Accuracy score of SupportVectorClassifier is 0.92 and Cross Validation Score is 0.95.
# * Accuracy score of RandomForest is 0.95 and Cross Validation Score is 0.95.

# **Backward Elimination Method**

# In[ ]:


back_df = df.copy()

X = back_df.drop('diagnosis', axis=1)
y = back_df['diagnosis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# In[ ]:


cols = list(X.columns)
pmax = 1
while(len(cols) > 0):
    p = []
    X_1 = X[cols]
    X_1 = sm.add_constant(X_1)
    model = sm.OLS(y, X_1)
    res = model.fit()
    p = pd.Series(res.pvalues.values[1:], index=cols)
    pmax = max(p)
    feature_with_max_p = p.idxmax()
    if (pmax>0.05):
        cols.remove(feature_with_max_p)
    else:
        break
        
backward_elimination_selected_feature = cols
backward_elimination_selected_feature


# In[ ]:


back_df = back_df[backward_elimination_selected_feature]


# In[ ]:


backward_selection_result = train_models(X_train, y_train, X_test, y_test, back_df, y)
backward_selection_result


# * Accuracy score of LogisticRegression is 0.94 and Cross Validation Score is 0.94.
# * Accuracy score of SupportVectorClassifier is 0.95 and Cross Validation Score is 0.95.
# * Accuracy score of RandomForest is 0.99 and Cross Validation Score is 0.95.

# **Conclusion**
# * Main motive to share this notebook is selecting features by different methods and using those feature apply different algorithms and see performance
# * I'm newbie if I did some mistakes feel free to comment down.

# In[ ]:




