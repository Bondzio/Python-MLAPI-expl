#!/usr/bin/env python
# coding: utf-8

# I want to compare different learning models at classifying the Titanic data set. I would like gain some amount of understanding as to why one would choose one model as opposed to the other.

# In[ ]:


import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


X = pd.read_csv('../input/train.csv')
y = X.pop('Survived')


# In[ ]:


X.describe()


# In[ ]:


X['Age'].fillna(X.Age.mean(), inplace=True)

X.describe()


# In[ ]:


numeric_variables = list(X.dtypes[X.dtypes != 'object'].index)
X[numeric_variables].head()


# In[ ]:


model = RandomForestRegressor(n_estimators=100, oob_score=True, random_state=42)

model.fit(X[numeric_variables], y)


# In[ ]:


model.oob_score_


# In[ ]:


# Benchmark
y_oob = model.oob_prediction_
print('c-stat: ', roc_auc_score(y, y_oob))


# In[ ]:


def describe_categorical(X):
    """
    Just like .describe(), but returns the results for 
    categorical variables only.
    """
    from IPython.display import display, HTML
    display(HTML(X[X.columns[X.dtypes == "object"]].describe().to_html()))


# In[ ]:


describe_categorical(X)


# In[ ]:


X.drop(['Name', 'Ticket', 'PassengerId'], axis = 1, inplace = True)


# In[ ]:


def clean_cabin(x):
    try:
        return x[0]
    except TypeError:
        return 'None'
    
X['Cabin'] = X.Cabin.apply(clean_cabin)


# In[ ]:


categorical_variables = ['Sex', 'Cabin', 'Embarked']

for variable in categorical_variables:
    X[variable].fillna('Missing', inplace=True)
    dummies = pd.get_dummies(X[variable], prefix=variable)
    X = pd.concat([X, dummies], axis=1)
    X.drop([variable], axis=1, inplace=True)


# In[ ]:


X


# In[ ]:


def printall(X, max_rows=10):
    from IPython.display import display, HTML
    display(HTML(X.to_html(max_rows=max_rows)))
    
printall(X)


# In[ ]:


# setting n_jobs to -1 is actually very important for optimization, it tells SKLearn to use maximum
# number of cores that you have, which is almost definitely greater than 1.
model = RandomForestRegressor(100, oob_score=True, n_jobs=-1, random_state=42)
model.fit(X, y)
print('C-stat:', roc_auc_score(y, model.oob_prediction_))


# In[ ]:


model.feature_importances_


# In[ ]:


feature_importances = pd.Series(model.feature_importances_, index = X.columns)
feature_importances.sort_values(inplace=True)
feature_importances.plot(kind='barh', figsize=(7,6));


# In[ ]:


# Complex version taht shows the summary view

def graph_feature_importances(model, feature_names, autoscale=True, headroom=0.05, width=10, summarized_columns=None):
    """
    By Mike Bernico 
    """
    if autoscale:
        x_scale = model.feature_importances_.max()+headroom
    else:
        x_scale = 1
        
    feature_dict = dict(zip(feature_names, model.feature_importances_))
    
    if summarized_columns:
        # some dummy columns need to be summarized
        for col_name in summarized_columns:
            sum_value = sum(x for i, x in feature_dict.items() if col_name in i)
            
            keys_to_remove = [i for i in feature_dict.keys() if col_name in i]
            for i in keys_to_remove:
                feature_dict.pop(i)
            feature_dict[col_name] = sum_value
    
    results = pd.Series(feature_dict.values(), index=feature_dict.keys())
    results.sort_values(axis=0)
    results.plot(kind="barh", figsize=(width, len(results)/4), xlim=(0,x_scale))


# In[ ]:


# graph_feature_importances(model, X.columns, summarized_columns=categorical_variables)


# In[ ]:


get_ipython().run_cell_magic('timeit', '', 'model = RandomForestRegressor(1000, oob_score=True, n_jobs=1, random_state=42)\nmodel.fit(X,y)')


# In[ ]:


get_ipython().run_cell_magic('timeit', '', 'model = RandomForestRegressor(1000, oob_score=True, n_jobs=-1, random_state=42)\nmodel.fit(X,y)')


# ### n-estimators

# In[ ]:


results = []
n_estimator_options = [30, 50, 100, 200, 500, 1000, 2000]

for trees in n_estimator_options:
    model = RandomForestRegressor(trees, oob_score=True, n_jobs=-1, random_state=42)
    model.fit(X, y)
    print(trees, 'trees')
    roc = roc_auc_score(y, model.oob_prediction_)
    print('C-stat: ', roc)
    results.append(roc)
    print("")
    
pd.Series(results, n_estimator_options).plot();


# ### max features

# In[ ]:


results = []
max_features_options = ['auto', None, 'sqrt', 'log2', 0.9, 0.2]

for max_features in max_features_options:
    model = RandomForestRegressor(trees, oob_score=True, n_jobs=-1, random_state=42)
    model.fit(X, y)
    print(trees, 'trees')
    roc = roc_auc_score(y, model.oob_prediction_)
    print('C-stat: ', roc)
    results.append(roc)
    print("")
    
pd.Series(results, max_features_options).plot(kind="barh", xlim=(.85,.88));


# ### min_samples_leaf

# In[ ]:


results = []
min_samples_leaf_options = [1,2,3,4,5,6,7,8,9,10]

for min_samples in min_samples_leaf_options:
    model = RandomForestRegressor(n_estimators=1000,
                                 oob_score=True,
                                 n_jobs=-1,
                                 random_state=42,
                                 max_features="auto",
                                 min_samples_leaf=min_samples)
    model.fit(X, y)
    print(min_samples,"min samples")
    roc = roc_auc_score(y, model.oob_prediction_)
    print("C-stat: ",roc)
    results.append(roc)
    print("")
    
pd.Series(results, min_samples_leaf_options).plot()


# ### Final Model

# In[ ]:


X.drop(['Cabin_T'],inplace=True,axis=1)
# X.drop(['Cabin_None'],inplace=True,axis=1)


# In[ ]:


model = RandomForestClassifier(n_estimators=1000,
                             oob_score=True,
                             n_jobs=-1,
                             random_state=42,
                             max_features="auto",
                             min_samples_leaf=5)
model.fit(X[:-200], y[:-200]).score(X[-200:], y[-200:])


# In[ ]:


model = AdaBoostClassifier()
model.fit(X[:-200], y[:-200]).score(X[-200:], y[-200:])


# In[ ]:


model = SVC()
model.fit(X[:-200], y[:-200]).score(X[-200:], y[-200:])


# In[ ]:


model = LogisticRegression()
model.fit(X[:-200], y[:-200]).score(X[-200:], y[-200:])


# In[ ]:


model = XGBClassifier()
model.fit(X[:-200], y[:-200]).score(X[-200:], y[-200:])


# In[ ]:


X.columns.values


# In[ ]:




