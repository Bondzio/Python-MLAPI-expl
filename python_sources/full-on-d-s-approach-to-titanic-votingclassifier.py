#!/usr/bin/env python
# coding: utf-8

# ## Introduction
# 
# Titanic is a well-studied use case for machine learning. The objective of this notebook is to show my approach to try to inspire other people on how to tackle it. If you want to try out any other approach based on mine, feel free to fork and your feedback is super welcome! 
# 
# The steps I followed were the following:
# 1. EDA: some basic univariate and multivariate analysis to look for obvious patterns or relation between variables that required some attention or that would give me a head start on tackling the problem. 
#     1. On this section, I wrote my ideas/insights between the visualizations of what I saw in the graphs. Also, your comments are super welcomed. 
# 2. Coding some helper functions: after EDA I wrote some helper functions so preping, training and predicting would be easy to do a bunch of times. 
#     1. Please do look into the **fit_model** function, maybe you can tune better any of those models.
# 3. After having created the helper functions, it is quite straight-forward to model and test different approaches.
# 
# 
# #### Something cool about this kernel: at the end there's a section for self-scoring with the test set for the actual competition so you don't have to wast your 10 attempts on little changes you may have applied to the model.

# ### Import libraries

# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler, OneHotEncoder, KBinsDiscretizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier
import xgboost as xgb


# In[ ]:


import warnings
warnings.filterwarnings("ignore")


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv('/kaggle/input/titanic/train.csv')
# data = pd.read_csv('train.csv')


# ## EDA

# In[ ]:


data.head()


# In[ ]:


data.info()


# In[ ]:


data.describe()


# ## Univariate analysis  

# In[ ]:


plt.figure(figsize = (15,10))
grid = '22'

plt.subplot(grid+'1')
sns.countplot(data.Survived)

plt.subplot(grid+'2')
sns.countplot(data.Pclass)

plt.subplot(grid+'3')
sns.countplot(data.SibSp)

plt.subplot(grid+'4')
sns.countplot(data.Parch)


# We can see more peopled died than survived. Regardless, this is not a big unbalance, no need to fix the proportions of the data.
# 
# Also, we have a big third class in the sample and there was a lot of people traveling by themselves or with one or two companions. Big families were not common.

# In[ ]:


plt.figure(figsize = (20,5))


plt.subplot(121)
sns.distplot(data.Age.dropna(), hist = False, kde_kws = {'shade':True, 'alpha':0.3})

plt.subplot(122)
sns.boxplot(data.Age.dropna())


# In[ ]:


plt.figure(figsize = (8,5))

sns.countplot(data.Embarked.dropna())


# ## Multivariate analysis  

# In[ ]:


plt.figure(figsize = (20,15))

grid = '33'

plt.subplot(grid+'1')
sns.barplot(x = 'Embarked', y = 'Survived', data = data)

plt.subplot(grid+'2')
sns.barplot(y = 'Survived', x = 'Pclass', data = data)

plt.subplot(grid+'3')
sns.barplot(y = 'Survived', x = 'Fare', data = pd.concat([data.Survived, pd.cut(data.Fare, 3, labels = 'low medium high'.split())], axis = 1))

plt.subplot(grid+'4')
sns.barplot(x = 'Embarked', y = 'Fare', data = data)

plt.subplot(grid+'5')
sns.barplot(y = 'Fare', x = 'Survived', data = data)

plt.subplot(grid+'6')
sns.barplot(y = 'Fare', x = 'Pclass', data = data)

plt.tight_layout()


# A lot of people from Port C survived relative to the other two ports. Also, in average, people from 1st class had higher probability of surviving than other two classes. 
# 
# It seems that in average, people from Port C, payed more and people that payed more, had much more probability of surviving. Then, maybe we could discard the **Embarked** variable because we may extract the same information from **Pclass** or from **Fare**. These two variables seem to contain similar information and Fare has a little bit of more noice. 

# In[ ]:


plt.figure(figsize = (8,7))
sns.heatmap(data.groupby(['Embarked','Pclass']).size().unstack(0).apply(lambda x: x/x.sum()), annot = True, cbar = False)


# We saw that Port C had something special. With this heatmap, we can appreciate that Port C had the biggest proportion of 1st class passengers from all ports. This explains the high rate of survival. Now, we know that **Embarked**, **Fare** and **Pclass** may have similar information. We can remove one of them, probably **Pclass** as said before and see how it goes. 

# ## Helper Functions: Data Wrangling, Thresholds, Fit Models, Predictions

# In[ ]:


# Evaluate thresholds
def test_thresh(lower = 0.1, upper = 0.95, jump = 0.01):
    
    accs = {}
    for i in np.arange(lower, upper, jump):
        accs[i] = accuracy_score(test[1], predict(test[0], model, transformers, thresh = i, prep = False)['Survived'])
    
    best_thresh = np.round(sorted(accs.items(), key = lambda x: x[1], reverse = True)[0][0], 2)
    
    train_acc = accuracy_score(train[1], predict(train[0], model, transformers, thresh = best_thresh, prep = False)['Survived'])
    print(f'Train score: {train_acc}')
    
    print('Top 5 thresholds (test score):')
    print(sorted(accs.items(), key = lambda x: (1-abs(0.5-x[0]))*x[1], reverse = True)[:5])
    
    
    return best_thresh


# In[ ]:


# All data wrangling is performed here

def process_data(data, transformers = None):
    data = data.copy()
    data.set_index('PassengerId', inplace = True)
        
    # Extract title of person (Mr, Mrs, etc) and see if age changes between those groups significantly

    data['title'] = data.Name.str.split(',').str[1].str.strip().str.split().str[0]
    
    low_freq_titles = data.title.value_counts()[lambda x: x < 10].index
    
    data['title'] = data['title'].apply(lambda x: 'Misc' if x in low_freq_titles else x)
    
    age_by_title = data.groupby('title').Age.median()

    data['Age'] = data.apply(lambda x: age_by_title[x.title] if pd.isna(x.Age) else x.Age, axis = 1)

    data.loc[pd.isna(data.Embarked), 'Embarked'] = 'C'    
    
    data['fam_size'] = data.Parch + data.SibSp
    
    data = data.fillna(method = 'ffill')
    
    vars_for_bins = ['Age', 'Fare']
    vars_for_dummies = ['Sex', 'Embarked']
    
    if transformers is not None:
        bins = transformers[0]
        dummy = transformers[1]
        
        binned_age = bins.transform(np.array(data[vars_for_bins]))
        dummies = dummy.transform(data[vars_for_dummies])
        
 
    else:
        bins = KBinsDiscretizer()
        dummy = OneHotEncoder(sparse = False, drop = 'first')
        
        binned_age = bins.fit_transform(np.array(data[vars_for_bins]))
        dummies = dummy.fit_transform(data[vars_for_dummies])

    dummies = pd.DataFrame(dummies, columns = dummy.get_feature_names())

    binned_age = pd.DataFrame(binned_age.toarray(), columns = ['Age_'+str(i) for i in bins.bin_edges_[0]][:-1] + ['Fare_'+str(i) for i in bins.bin_edges_[1]][:-1])
    
    data.drop(['Cabin', 'Ticket', 'Name', 'Fare', 'Parch', 'SibSp', 'Age', 'Pclass', 'Sex', 'title', 'Embarked'], inplace = True, axis = 1, errors = 'ignore')
    
    data = pd.concat([data.reset_index(), dummies, binned_age], axis = 1).set_index('PassengerId')
    
    if transformers is None:
        return data, bins, dummy
    else:
        return data


# In[ ]:


# fit model
def fit_model(train_data, scale = True):
    preped, bins, dummy = process_data(train_data)
    
    scaler = StandardScaler()
    
    X = preped.drop('Survived', axis = 1)
    
    if scale: 
        X = pd.DataFrame(scaler.fit_transform(X), columns = X.columns, index = X.index)
    else:
        scaler = None
        
    y = preped['Survived']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    print('Training Neural Net')
    best_nn = RandomizedSearchCV(MLPClassifier(), 
                         verbose = 0, 
                         n_iter = 30,
                         param_distributions = {'hidden_layer_sizes':[(50,50,),(100,100,100,),(300,300,),(50,50,50,50,),(50,50,50,50,50,),(200,200,200,)],
                                                        'activation':['relu','tanh'],
                                                        'solver':['adam','lbfgs'],
                                                        'learning_rate':['constant','adaptive'],
                                                        'learning_rate_init': np.logspace(np.log10(0.00001), np.log(1), 20),
                                                        'max_iter':[50,100,200,500],
                                                        'random_state':[0]})
    
    best_nn.fit(X_train, y_train)
    best_nn = best_nn.best_estimator_

    print('Training XGB')
    
    best_xgb = RandomizedSearchCV(xgb.XGBClassifier(), n_iter = 30,
                     param_distributions = {'n_estimators':np.arange(50,550,50),
                                   'booster':['gbtree', 'gblinear','dart'],
                                   'max_depth':np.arange(1,50),
                                   'learning_rate': np.logspace(np.log10(0.00001), np.log(1), 20),
                                   'reg_alpha':np.logspace(np.log10(0.00001), np.log(1), 20)})
    best_xgb.fit(X_train, y_train)
    best_xgb = best_xgb.best_estimator_
    
    
    print('Training Logistic Regression')

    best_log = RandomizedSearchCV(LogisticRegression(), 
                         error_score=0.0, 
                         n_iter = 30,
                         param_distributions = {'penalty':['l1', 'l2', 'elasticnet','none'], 
                                       'dual':[True,False],
                                       'C': np.logspace(np.log10(0.00001), np.log(1), 20), 
                                       'fit_intercept':[True, False], 
                                       'random_state':[0], 
                                       'max_iter':[30,50,100,200,500,1000],
                                       'solver':['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']})
    best_log.fit(X_train, y_train)
    best_log = best_log.best_estimator_

    print('Training Random Forest')

    best_forest = RandomizedSearchCV(RandomForestClassifier(), n_iter = 30, param_distributions = {'bootstrap': [True, False],
                                                     'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
                                                     'max_features': ['auto', 'sqrt'],
                                                     'min_samples_leaf': [1, 2, 4],
                                                     'min_samples_split': [2, 5, 10],
                                                     'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]})
    best_forest.fit(X_train, y_train)
    best_forest = best_forest.best_estimator_

    best_estimators = [('Neural Net', best_nn), ('XGB', best_xgb), ('Logistic Reg', best_log), ('Random Forest', best_forest)]
    
    
    
    ensemble_model = VotingClassifier(best_estimators, voting = 'hard')

#         model = GridSearchCV(DecisionTreeClassifier(), cv = 5, param_grid = {'max_depth':[1,2,3,5,7,10], 
#                                                       'criterion':['entropy','gini'], 
#                                                       'random_state':[0], 
#                                                       'min_samples_leaf':[10,25,50,70,100,150,200]})

    ensemble_model.fit(X_train, y_train)
    
    print(f'Train Acc Score: {accuracy_score(y_train, ensemble_model.predict(X_train))}')
    print(f'Test Acc Score: {accuracy_score(y_test, ensemble_model.predict(X_test))}')
    
    return ensemble_model, (bins, dummy, scaler), preped, (X_train, y_train), (X_test, y_test)


# In[ ]:


# make predictions

def predict(test_df, model, transformers, thresh = 0.5, prep = True):
    if prep:
        temp_df = process_data(test_df, transformers)
        idx = temp_df.index
        if transformers[2] is not None:
            temp_df = pd.DataFrame(transformers[2].transform(temp_df), columns = temp_df.columns)
            
    else:
        temp_df = pd.DataFrame(test_df, columns = preped.drop('Survived',axis = 1).columns).copy()
        idx = temp_df.index
    
    
    if thresh != 0.5:
        predictions = (model.predict_proba(temp_df)[:,1] > thresh) * 1
        return pd.DataFrame(columns = ['PassengerId','Survived'], data = [*zip(idx, predictions)])
    
    else:
        return pd.DataFrame(columns = ['PassengerId','Survived'], data = [*zip(idx, model.predict(temp_df))])


# ## Fit model

# In[ ]:


model, transformers, preped, train, test = fit_model(data, scale = True)


# ## Threshold selection

# Only useful when not using Voting Classifier

# In[ ]:


# best_thresh = test_thresh()


# In[ ]:


test_set = pd.read_csv('/kaggle/input/titanic/test.csv')
# test_set = pd.read_csv('test.csv')
predictions = predict(test_set, model, transformers)
predictions.head()


# 
# #### Let's make sure both train and test set have same number of columns afters passed to the data wrangling function

# In[ ]:


process_data(test_set, transformers).describe()


# In[ ]:


process_data(data.drop('Survived', axis = 1))[0].describe(include = 'all')


# What are the estimators used by the Voting Classifier?

# In[ ]:


model.estimators_


# ## Prediction & Submission

# In[ ]:


predictions.to_csv('submission.csv', index = False)


# ### Self-scoring section
# Note: this wasn't used for any tuning or training purposes. Only for scoring before submitting.
# 
# From here on, the code will only work on local machine if you have the needed files

# In[ ]:


test_labels = pd.read_csv('/kaggle/input/titanic-solutions-for-selfscoring/pub')
accuracy_score(test_labels['survived'], predictions['Survived'])


# ### Submission

# !kaggle competitions submit -c titanic -f submission.csv -m "Here goes nothing?"
