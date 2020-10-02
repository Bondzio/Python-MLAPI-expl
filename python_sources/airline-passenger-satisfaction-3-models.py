#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[ ]:


data_train = pd.read_csv('/kaggle/input/airline-passenger-satisfaction/train.csv')
data_test = pd.read_csv('/kaggle/input/airline-passenger-satisfaction/test.csv')


# ### Data analysis ###

# In[ ]:


data_train.info()


# And look at type of every column.
# 
# Machine learning models require all input and output variables to be numeric.
# 
# Because our data contains categorical data, we must transform it to numbers before we will fit and evaluate a model.
# 
# We have next categorical data:
# - Gender
# - Customer Type
# - Type of Travel
# - Class
# 
# For these columns to use method of Pandas get_dummies.
# 
# For categorical column 'satisfaction' to use LabelEncoder from sklearn:
# 
# * neutral or dissatisfied = 0
# * satisfied = 1

# In[ ]:


from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
data_train['satisfaction'] = labelencoder.fit_transform(data_train['satisfaction'])
data_test['satisfaction'] = labelencoder.fit_transform(data_test['satisfaction'])


# In[ ]:


'How many people satisfacted by Airline:'
data_train.groupby('Gender')[['satisfaction']].sum()
'How many people participated in the study:'
data_train.groupby('Gender')[['satisfaction']].count()
'Percentage of satisfacted people :'
data_train.groupby('Gender')[['satisfaction']].sum()/ data_train.groupby('Gender')[['satisfaction']].count()


# So, people`s satisfaction do not depend from gender.

# In[ ]:


'Satisfaction of people depending on the class:'
data_train.groupby('Class')[['satisfaction']].sum()
'How many people participated in the study:'
data_train.groupby('Class')[['satisfaction']].count()
'Percentage of satisfacted people depending from the class:'
data_train.groupby('Class')[['satisfaction']].sum()/ data_train.groupby('Class')[['satisfaction']].count()


# We can see that satisfaction depend from class: Business class promotes to satisfaction and not if eco class.

# In[ ]:


'Percentage of satisfacted people depending from the type of travel:'
data_train.groupby('Type of Travel')[['satisfaction']].sum()/ data_train.groupby('Type of Travel')[['satisfaction']].count()


# Business travel also promotes to satisfaction.

# In[ ]:


data_dummies=pd.get_dummies(data_train, columns=["Gender","Customer Type","Type of Travel","Class"],drop_first=True)


# In[ ]:


data_test=pd.get_dummies(data_test, columns=["Gender","Customer Type","Type of Travel","Class"],drop_first=True)


# In[ ]:


fig, ax = plt.subplots(figsize=(14,14))
sns.heatmap(data_dummies.corr(), annot=True, square=True, cbar=False, ax=ax, linewidths=0.25);


# In[ ]:


X_train = data_dummies.drop(columns=['Arrival Delay in Minutes', 'Unnamed: 0', 'id', 'satisfaction'])
X_test = data_test.drop(columns=['Arrival Delay in Minutes', 'Unnamed: 0', 'id', 'satisfaction'])


# As we can see there is correlation: 'Departure Delay in Minutes', 'Arrival Delay in Minutes'.
# Drop from data column 'Arrival Delay in Minutes'.
# Also columns 'Unnamed: 0', 'id' don`t have useful information - drop them too.

# In[ ]:


y_train = data_dummies['satisfaction']
y_test = data_test['satisfaction']


# In[ ]:


X_train.isnull().sum()


# Our data haven`t 'Null'.

# <div class="alert alert-block alert-warning">
# Create one more data without outliers and will be train models on 2 data with a choice of the best.
# </div>

# In[ ]:


data_outliers = []
for col in X_train.columns:    
        Q_min = X_train[col].quantile(0.01)
        Q_max = X_train[col].quantile(0.99)
        idx = ((X_train[col] < Q_min) | (X_train[col] > Q_max))
        data_outliers.append(X_train[idx])

data_outliers = pd.concat(data_outliers)
data_cleared = X_train.drop(data_outliers.index.unique())
y_cleared = y_train.drop(data_outliers.index.unique())


# ## Train models ##

# In[ ]:


from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve


# In[ ]:


from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from numpy import mean
from sklearn.model_selection import GridSearchCV


# In[ ]:


def models_result(model, X_test, y_test):
    labels = model.predict(X_test)
    matrix = confusion_matrix(y_test, labels)
    sns.heatmap(matrix.T, square=True, annot=True, fmt='d', cbar=False)
    plt.xlabel('true label')
    plt.ylabel('predicted label');
    
    logit_roc_auc = roc_auc_score(y_test, labels)
    fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test)[:,1])
    plt.figure()
    plt.plot(fpr, tpr, label='(area = %0.2f)' % logit_roc_auc)
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.legend(loc="lower right")
    plt.savefig('Log_ROC')
    plt.show();
    
    print(classification_report(y_test, labels))


# ### RandomForestClassifier ###

# In this model, we will select hyperparameters for the best result. Then the already selected hyperparameters will be substituted.
# 
# We will iterate over different values for parameters:
# - max_features
# - n_estimators

# In[ ]:


from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
n_estimators = [50, 75, 100]
max_features = ['sqrt', 'log2']
grid = dict(n_estimators=n_estimators,max_features=max_features)
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_search_RandomForestClassifier = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring='accuracy',error_score=0)
model_RandomForestClassifier = grid_search_RandomForestClassifier.fit(X_train, y_train)

print("Best: %f using %s" % (model_RandomForestClassifier.best_score_, model_RandomForestClassifier.best_params_))


# In[ ]:


means = model_RandomForestClassifier.cv_results_['mean_test_score']
stds = model_RandomForestClassifier.cv_results_['std_test_score']
params = model_RandomForestClassifier.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))


# And to use RandomForestClassifier we need choose hyperparameters: max_features = log2, n_estimators = 100

# In[ ]:


model_RandomForestClassifier_cleared = grid_search_RandomForestClassifier.fit(data_cleared, y_cleared)
print("Result: %f" % (model_RandomForestClassifier_cleared.best_score_))


# In[ ]:


models_result(model_RandomForestClassifier, X_test, y_test)


# ### BaggingClassifier ###

# In[ ]:


from sklearn.ensemble import BaggingClassifier

model = BaggingClassifier(random_state=28)
n_estimators = [40]
grid = dict(n_estimators=n_estimators)
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_search_BaggingClassifier = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring='accuracy',error_score=0)
model_BaggingClassifier = grid_search_BaggingClassifier.fit(X_train, y_train)

print("Result: %f" % (model_BaggingClassifier.best_score_))


# In[ ]:


model_BaggingClassifier_cleared = grid_search_BaggingClassifier.fit(data_cleared, y_cleared)
print("Result: %f" % (model_BaggingClassifier_cleared.best_score_))


# In[ ]:


models_result(model_BaggingClassifier, X_test, y_test)


# ### AdaBoostClassifier ###

# In[ ]:


ABC = AdaBoostClassifier(DecisionTreeClassifier(max_depth=3),
                        learning_rate = 1.1,
                        random_state=42)

n_estimators = [75]
grid = dict(n_estimators=n_estimators)
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_search_ABC = GridSearchCV(estimator=ABC, param_grid=grid, n_jobs=-1, cv=cv, scoring='accuracy',error_score=0)
model_ABC = grid_search_ABC.fit(X_train, y_train)

print("Result: %f" % (model_ABC.best_score_))


# In[ ]:


model_ABC_cleared = grid_search_ABC.fit(data_cleared, y_cleared)
print("Result: %f" % (model_ABC_cleared.best_score_))


# In[ ]:


models_result(model_ABC, X_test, y_test)


# We use 3 models:
# 
# - RandomForestClassifier
# - BaggingClassifier
# - AdaBoostClassifier( with DecisionTreeClassifier)
# 
# The best result gave a model with using RandomForestClassifier = 96,23% accuracy.

# <div class="alert alert-block alert-success">
#     
# Thanks to:
# 
# author of this dataset;
#     
# https://machinelearningmastery.com/
#         
# ### Happy coding ###
# </div>
