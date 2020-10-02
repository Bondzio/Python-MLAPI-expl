#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import warnings
warnings.filterwarnings('ignore')


# In[ ]:


df = pd.read_excel('/kaggle/input/titanic3/titanic3.xls')


# In[ ]:


from sklearn import (ensemble, preprocessing, tree)
from sklearn.metrics import (auc, confusion_matrix, roc_auc_score, roc_curve)
from sklearn.model_selection import (train_test_split, StratifiedKFold)


# In[ ]:


from yellowbrick.classifier import (ConfusionMatrix, ROCAUC)
from yellowbrick.model_selection import (LearningCurve)


# In[ ]:


type(df)


# In[ ]:


print(df.shape)


# In[ ]:


df.head()


# In[ ]:


df.tail()


# In[ ]:


df.dtypes


# In[ ]:


import pandas_profiling


# In[ ]:


df.columns


# In[ ]:


profile = pandas_profiling.ProfileReport(df); profile


# In[ ]:


import seaborn as sns


# In[ ]:


fig, ax = plt.subplots(figsize=(30, 10))
sns.boxplot(data=df)


# In[ ]:


fig, ax=plt.subplots(figsize=(30, 10))
ax = sns.heatmap(df.corr(), fmt='.2f', annot=True, ax=ax, vmin=-1, vmax=1 )


# In[ ]:


df.isnull().sum()


# In[ ]:


porc_miss = df.isnull().mean()*100
round(porc_miss, 0)


# In[ ]:


import missingno as msno


# In[ ]:


ax = msno.matrix(df.sample(500))


# In[ ]:


fig, ax=plt.subplots(figsize=(30,10))
(1 - df.isnull().mean()).abs().plot.bar(ax=ax)


# In[ ]:


ax = msno.heatmap(df, figsize=(30, 10))


# In[ ]:


ax = msno.dendrogram(df)


# In[ ]:


df1 = df.drop(columns = ['name', 'ticket', 'home.dest', 'cabin', 'boat', 'body'])


# In[ ]:


df1.head()


# In[ ]:


df1.sex.value_counts(dropna=False)


# In[ ]:


df1.embarked.value_counts(dropna=False)


# In[ ]:


df1 = pd.get_dummies(df1, drop_first=True)


# In[ ]:


df1.columns


# In[ ]:


df1.isna().any().any()


# In[ ]:


df1.isnull().sum()


# In[ ]:


y = df1.survived
x = df1.drop(columns='survived')


# In[ ]:


new_df = x.copy()
new_df['target'] = y
vars = ['pclass', 'age', 'fare']
p = sns.pairplot(new_df, vars=vars, hue='target', kind='reg')


# In[ ]:


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)


# In[ ]:


meds = x_train.median()
x_train = x_train.fillna(meds)
x_test = x_test.fillna(meds)


# In[ ]:


x_train.isna().any().any()


# In[ ]:


x_test.isna().any().any()


# In[ ]:


cols = 'pclass,age,sibsp,fare,parch,sex_male,embarked_Q,embarked_S'.split(',')
sca = preprocessing.StandardScaler()
x_train = sca.fit_transform(x_train)
x_train = pd.DataFrame(x_train, columns=cols)
x_test = sca.fit_transform(x_test)
x_test = pd.DataFrame(x_test, columns=cols)


# In[ ]:


x = pd.concat([x_train, x_test])
y = pd.concat([y_train, y_test])
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import xgboost


# In[ ]:


for model in [LogisticRegression, DecisionTreeClassifier, KNeighborsClassifier, GaussianNB, SVC, RandomForestClassifier, xgboost.XGBClassifier]:
    cls = model()
    kfold = model_selection.KFold(n_splits=10)
    s = model_selection.cross_val_score(cls, x, y, scoring='roc_auc', cv=kfold)
    print(f'{model.__name__:22} AUC:' f'{s.mean():.3f} STD: {s.std():.2f}')


# In[ ]:


from mlxtend.classifier import StackingClassifier


# In[ ]:


clfs = [x() for x in [LogisticRegression, DecisionTreeClassifier, KNeighborsClassifier, GaussianNB, SVC, RandomForestClassifier, xgboost.XGBClassifier]]


# In[ ]:


stack = StackingClassifier(classifiers=clfs, meta_classifier = LogisticRegression())


# In[ ]:


kfold = model_selection.KFold(n_splits=10)


# In[ ]:


s = model_selection.cross_val_score(stack, x, y, scoring='roc_auc', cv=kfold)


# In[ ]:


print(f'{stack.__class__.__name__} AUC:' f'{s.mean():.3f} STD: {s.std():.2f}')


# In[ ]:


rf = ensemble.RandomForestClassifier(n_estimators=100)


# In[ ]:


rf.fit(x_train, y_train)
RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini', max_depth=None, max_features='auto', max_leaf_nodes=None, 
                       min_impurity_decrease=0.0, min_impurity_split=None, min_samples_leaf=1, min_samples_split=2, min_weight_fraction_leaf=0.0, 
                       n_estimators=10, n_jobs=1, oob_score=False, verbose=0, warm_start=False)


# In[ ]:


rf.score(x_test, y_test)


# In[ ]:


rf1 = ensemble.RandomForestClassifier()
params = {'max_features':[0.4, 'auto'], 'n_estimators':[15, 200], 'min_samples_leaf':[1, 0.1]}


# In[ ]:


cv = model_selection.GridSearchCV(rf1, params, n_jobs=-1).fit(x_train, y_train)


# In[ ]:


print(cv.best_params_)


# In[ ]:


rf2 = ensemble.RandomForestClassifier()
params = {'max_features':0.4, 'n_estimators':200, 'min_samples_leaf':1}


# In[ ]:


rf2.fit(x_train, y_train)
rf2.score(x_test, y_test)


# In[ ]:


LR = LogisticRegression()
kfold = model_selection.KFold(n_splits=10)
s = model_selection.cross_val_score(LR, x, y, scoring='roc_auc', cv=kfold)
print('LogisticRegression' ' ' 'AUC:' f'{s.mean():.3f} STD: {s.std():.2f}')


# In[ ]:


LR.fit(x_train, y_train)


# In[ ]:


y_pred = LR.predict(x_test)
confusion_matrix(y_test, y_pred)


# In[ ]:


mapping = {0:'died', 1:'survived'}
fig, ax=plt.subplots(figsize=(10,6))
cm_viz = ConfusionMatrix(LR, classes=['died', 'survived'], label_encoder=mapping)
cm_viz.score(x_test, y_test)
cm_viz.poof()


# In[ ]:


fig, ax = plt.subplots(figsize=(10,10))
roc_viz = ROCAUC(LR)
roc_viz.score(x_test, y_test)
roc_viz.poof()


# In[ ]:


fig, ax = plt.subplots(figsize=(10, 10))
cv = StratifiedKFold(12)
sizes = np.linspace(0.3, 1.0, 10)
lc_viz = LearningCurve(LR, cv=cv, train_sizes=sizes, scoring='f1_weighted', n_jobs=4, ax=ax)
lc_viz.fit(x, y)
lc_viz.poof()

