#!/usr/bin/env python
# coding: utf-8

# # Credit Card Fraud Prediction (Imbalanced Class)

# # 1. Import Libraries

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='white', context='notebook', palette='deep')

import warnings
warnings.filterwarnings("ignore")

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold
from collections import Counter

from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier


# # 2. Load and Check Data

# ## 2.1 Load Data

# In[ ]:


data = pd.read_csv('/kaggle/input/creditcardfraud/creditcard.csv')
data.head()


# In[ ]:


print(data.shape)


# In[ ]:


data.describe().round(decimals=2)


# In[ ]:


features = data.columns.values


# ## 2.2 Outlier Detection

# In[ ]:


def detect_outliers(df,n,features):
    outlier_indices = []
    
    for col in features:
        Q1 = np.percentile(df[col], 25)
        Q3 = np.percentile(df[col],75)
        IQR = Q3 - Q1
        outlier_step = 1.5 * IQR
        outlier_list_col = df[(df[col] < Q1 - outlier_step) | (df[col] > Q3 + outlier_step )].index
        outlier_indices.extend(outlier_list_col)
        
    outlier_indices = Counter(outlier_indices)        
    multiple_outliers = list( k for k, v in outlier_indices.items() if v > n )
    
    return multiple_outliers 


# In[ ]:


# Potential outlier
# Select observations containing more than 4 outliers
data.loc[detect_outliers(data, 4, features)]


# ## 2.3 Check for null and missing values

# In[ ]:


data = data.fillna(np.nan)
data.isnull().sum()


# > ## Notes :
# - Outlier is detected
# - No missing value

# # 3. Exploratory Data Analysis

# ## 3.1 Numerical Analysis

# In[ ]:


# Correlation matrix
plt.figure(figsize=(20, 15))
sns.heatmap(data.corr(), annot=True, fmt=".2f", cmap="coolwarm")


# In[ ]:


data.corr()['Class'].sort_values(ascending=False)


# In[ ]:


def most_corr(param, n):
    class_corr = data.corr()[param].sort_values(ascending=False)
    list_class = []
    for i in features:
        if(np.abs(class_corr[i]) >= n):
           list_class.append(i)
    return list_class


# In[ ]:


most_corr('Class', 0.1) # Select features with correlation higher than 0.1 (positive correlation) or lower than -0.1 (negative correlation)


# In[ ]:


# Plot skew
fig = plt.figure(figsize=(12,18))
for i in range(len(features)):
    fig.add_subplot(8,4,i+1)
    sns.distplot(data[features[i]], kde_kws={'bw': 0.1})
    plt.title('Skew : %.2f' % data[features[i]].skew())
    
plt.tight_layout()
plt.show()


# In[ ]:


# Univariate analysis - boxplot
fig = plt.figure(figsize=(12,18))
for i in range(len(features)):
    fig.add_subplot(8,4,i+1)
    sns.boxplot(y=data[features[i]])
    
plt.tight_layout()
plt.show()


# In[ ]:


# Bivariate analysis - boxplot
fig = plt.figure(figsize=(12,18))
for i in range(len(features)):
    fig.add_subplot(8,4,i+1)
    sns.boxplot(y=data[features[i]], x=data['Class'])
    
plt.tight_layout()
plt.show()


# In[ ]:


attributes_select = ['V1', 'V3', 'V4', 'V7', 'V10', 'V11', 'V12', 'V14', 'V16', 'V17', 'V18']
data.loc[detect_outliers(data, 4, attributes_select)]['Class'].value_counts()


# ## 3.2 Categorical Analysis

# In[ ]:


# Count Class values
data['Class'].value_counts()


# > ## Notes :
# - Likely have correlation 'V1', 'V3', 'V4', 'V7', 'V10', 'V11', 'V12', 'V14', 'V16', 'V17', 'V18'
# - No need to reduce skewness
# - Imbalaced 'Class' data, must be handled
# - No need to drop outliers due to most of value 1 Class are in outlier

# # 4. Feature Selection

# In[ ]:


attributes = ['V1', 'V3', 'V4', 'V7', 'V10', 'V11', 'V12', 'V14', 'V16', 'V17', 'V18', 'Class']
dataset = data[attributes]


# # 5. Build Model

# ## 5.1 Preparation

# In[ ]:


from sklearn.model_selection import train_test_split

train, test = train_test_split(dataset, test_size=0.2)


# In[ ]:


train['Class'].value_counts()


# In[ ]:


test['Class'].value_counts()


# In[ ]:


X_train = train.drop(['Class'], axis = 1)
Y_train = train['Class']

X_test = test.drop(['Class'], axis = 1)
Y_test = test['Class']


# ## 5.2 Cross Validation Model

# In[ ]:


kfold = StratifiedKFold(n_splits=10)

# Modeling step Test differents algorithms 
random_state = 2
classifiers = []
algorithm = ["DecisionTree","AdaBoost",
             "ExtraTrees", "LogisticRegression"]

classifiers.append(DecisionTreeClassifier(random_state=random_state))
classifiers.append(AdaBoostClassifier(DecisionTreeClassifier(random_state=random_state),random_state=random_state,learning_rate=0.1))
classifiers.append(ExtraTreesClassifier(random_state=random_state))
classifiers.append(LogisticRegression(random_state = random_state))

cv_results = []
for classifier in classifiers :
    cv_results.append(cross_val_score(classifier, X_train, y = Y_train, scoring = "accuracy", cv = kfold, n_jobs=4))
    

cv_means = []
cv_std = []
for cv_result in cv_results:
    cv_means.append(cv_result.mean())
    cv_std.append(cv_result.std())

cv_res = pd.DataFrame({
        "CrossValMeans":cv_means,
        "CrossValerrors": cv_std,
        "Algorithm": algorithm
        })


# In[ ]:


# Plot score of cross validation models
g = sns.barplot("CrossValMeans","Algorithm", data = cv_res, palette="Set3",orient = "h",**{'xerr':cv_std})
g.set_xlabel("Mean Accuracy")
g = g.set_title("Cross validation scores")


# In[ ]:


cv_res


# > Notes
# - It seems the accuracy of the model is quite similar, but let's look at hyperparameter tuning with class weight and confusion matrix

# ## 5.3 Hyperparameter Tuning

# In[ ]:


from sklearn.metrics import plot_confusion_matrix


# In[ ]:


# Decision Tree
DTC = DecisionTreeClassifier(random_state=random_state)


# Search grid for optimal parameters
ex_param_grid = {
    'class_weight': ['balanced', {0:1,1:10}, {0:1,1:100}, {0:0.5, 1:289}]
}


gsDTC = GridSearchCV(DTC, param_grid = ex_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)

gsDTC.fit(X_train,Y_train)

DTC_best = gsDTC.best_estimator_

# Best score
gsDTC.best_score_

# Plot Confusion Matrix
plot_confusion_matrix(DTC_best, X_test, Y_test)


# In[ ]:


DTC_best


# In[ ]:


# Extra Trees Classifier
ETC = ExtraTreesClassifier(random_state=random_state)


# Search grid for optimal parameters
ex_param_grid = {
    'class_weight': ['balanced', {0:1,1:10}, {0:1,1:100}, {0:0.5, 1:289}]
}


gsETC = GridSearchCV(ETC, param_grid = ex_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)

gsETC.fit(X_train,Y_train)

ETC_best = gsETC.best_estimator_

# Best score
gsETC.best_score_

# Plot Confusion Matrix
plot_confusion_matrix(ETC_best, X_test, Y_test)


# In[ ]:


ETC_best


# In[ ]:


# LogisticRegression
LRC = LogisticRegression()


# Search grid for optimal parameters
ex_param_grid = {
    'C': [0.001, 0.01, 0.1, 1],
    'class_weight': ['balanced', {0:1,1:10}, {0:1,1:100}, {0:0.5, 1:289}]
}


gsLRC = GridSearchCV(LRC, param_grid = ex_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)

gsLRC.fit(X_train,Y_train)

LRC_best = gsLRC.best_estimator_

# Best score
gsLRC.best_score_

# Plot Confusion Matrix
plot_confusion_matrix(LRC_best, X_test, Y_test)


# In[ ]:


LRC_best


# In[ ]:


# Ada Boost Classifier
ADB = AdaBoostClassifier(DecisionTreeClassifier(random_state=random_state, class_weight={0: 1, 1: 10}),random_state=random_state)


# Search grid for optimal parameters
ex_param_grid = {
    'learning_rate': [0.001, 0.01, 0.1]
}


gsADB = GridSearchCV(ADB, param_grid = ex_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)

gsADB.fit(X_train,Y_train)

ADB_best = gsADB.best_estimator_

# Best score
gsADB.best_score_

# Plot Confusion Matrix
plot_confusion_matrix(ADB_best, X_test, Y_test)


# > Notes
# - Decision Tree and Ada Boost Classifier give similar result due to Ada Boost uses Decision Tree as Base estimators

# # Final

# ### The best model is Extratress classifier with lowest false negative and positive
