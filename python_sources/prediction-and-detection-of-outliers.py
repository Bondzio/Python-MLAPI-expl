#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing the libraries

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # data visualisation (2-D)
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns # data visualisation (3-D)
plt.style.use('seaborn') # set style for graph
import warnings 
warnings.filterwarnings('ignore') # ignore all types of warnings

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


# Loading the red wine dataset
wine = pd.read_csv('../input/red-wine-quality-cortez-et-al-2009/winequality-red.csv')


# In[ ]:


display(wine.head(), wine.shape)


# In[ ]:


wine.info()


# In[ ]:


# data doesn't contain any null value 


# In[ ]:


wine.describe()


# In[ ]:


# its look like our data contains some outliers in most of the features, let's take a look at them


# In[ ]:


# lets check the correlation of the features
wine.corr()


# In[ ]:


plt.figure(figsize = (10, 8))
sns.heatmap(wine.corr(), square = True, cmap = 'Blues')


# In[ ]:


# its looks like features are not strongly correlated to each other
# lets do some visualisation to detect the outliers in the data


# In[ ]:


plt.figure(figsize = (10, 6))
sns.set_context('talk')
sns.boxplot(wine['quality'], wine['free sulfur dioxide'], data = wine)


# In[ ]:


# free sulphur dioxide contains some extreme values in the dataset


# In[ ]:


plt.figure(figsize = (10, 8))
sns.boxplot(wine['quality'], wine['citric acid'], data = wine)


# In[ ]:


# citric acid only contains 2 extremes in it which is avoidable for now


# In[ ]:


plt.figure(figsize = (10, 8))
sns.boxplot(wine['quality'], wine['total sulfur dioxide'], data = wine)


# In[ ]:


# total sulphur dioxide containes some outliers and we have to remove them


# In[ ]:


plt.figure(figsize = (10, 8))
sns.boxplot(wine['quality'], wine['sulphates'], data = wine)


# In[ ]:


# sulphates also contains so many outliers


# In[ ]:


plt.figure(figsize = (10, 8))
sns.boxplot(wine['quality'], wine['residual sugar'], data = wine)


# In[ ]:


# residual sugar contains outliers too


# Detection and Removal of Outliers in dataset

# In[ ]:


outliers = []  # list to store outliers value

# method for detecting the outliers using interquantilerange technique 
def detect_outliers(data): 
    quantile1, quantile3 = np.percentile(data, [25, 75])  # create two quantiles for 25% and 75%
    iqr_val = quantile3 - quantile1                       # interquantilerange value
    lower_bound_value = quantile1 - (1.5 * iqr_val)       # lower limit of the data, anything greater are not outliers
    upper_bound_value = quantile3 + (1.5 * iqr_val)       # upper limit of the data, anything less are not outliers
    
    for i in data:
        if lower_bound_value < i < upper_bound_value:     # if data[value] is greater than lbv and less than ubv than it is not considered as an outlier
            pass
        else:
            outliers.append(i)
            
    return lower_bound_value, upper_bound_value           # return lower bound and upper bound value for the data


# In[ ]:


# fwith the help of boxplot visualisation we can notice that the outliers are only present through the upper bound value so we only check ubv


# In[ ]:


# detection of outliers from residual sugar
detect_outliers(wine['residual sugar'])


# In[ ]:


wine = wine.drop(wine[wine['residual sugar'] > 3.65].index) # drop values which contains outliers


# In[ ]:


# detection of outliers from sulphates
detect_outliers(wine['sulphates'])


# In[ ]:


wine = wine.drop(wine[wine['sulphates'] > 0.99].index)


# In[ ]:


# detection of outliers from free sulphur dioxide
detect_outliers(wine['free sulfur dioxide'])


# In[ ]:


wine = wine.drop(wine[wine['free sulfur dioxide'] > 40.5].index)


# In[ ]:


# detect outliers from total sulphur dioxide
detect_outliers(wine['total sulfur dioxide'])


# In[ ]:


wine = wine.drop(wine[wine['total sulfur dioxide'] > 112].index)


# In[ ]:


# outliers are removed from the dataset. now do some preprocessing on data


# In[ ]:


# lets change the wine quality in only two categories 'bad' and 'good' it makes it easier for classification


# In[ ]:


wine['quality'] = pd.cut(wine['quality'], bins = [0, 6, 8], labels = ['bad', 'good'])


# In[ ]:


wine['quality']


# In[ ]:


# lets do labelencoding on wine quality to make it '0' and '1'
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

wine['quality'] = le.fit_transform(wine['quality'])


# In[ ]:


# split the dataset into featurees and label
X = wine.drop(['quality'], axis = 1)
y = wine['quality']


# In[ ]:


# split the dataset into training and testing set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)


# In[ ]:


# lets take a look at the labels
sns.countplot(y)


# In[ ]:


#  it is clearly seen here that their is an imbalance in the dataset, 1's are very few as compared to 0's


# In[ ]:


# lets make the dataset balance by using over sampling 
from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state = 42, ratio = 0.9)
X_train, y_train = sm.fit_sample(X_train, y_train)


# In[ ]:


# lets normalize data 
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# In[ ]:


# Building classification model using randomForestClassiifier
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)


# In[ ]:


predictions = clf.predict(X_test)  # predictions generated by our model


# In[ ]:


from sklearn.metrics import confusion_matrix, classification_report
print(classification_report(y_test, predictions))


# In[ ]:


# we have get an accuracy of 92 % 
# lets check cross validation score for our predictions
from sklearn.model_selection import cross_val_score
scores = cross_val_score(clf, X_train, y_train, cv = 10)
scores.mean()


# In[ ]:


# cross validation mean is 91


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators = 90, criterion = 'gini', max_features = 'auto')
clf.fit(X_train, y_train)# lets use gridsearchcv to parameter tuning 
from sklearn.model_selection import GridSearchCV
param = {
    'n_estimators' : [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200],
    'criterion' : ['gini', 'entropy'],
    'max_features' : ['auto', 'sqrt', 'log2']
} 

grid_search = GridSearchCV(estimator = clf,
                          param_grid = param,
                          scoring = 'f1',
                          cv = 'warn',
                          n_jobs = -1)

grid_search = grid_search.fit(X_train, y_train)

print(f'best score : {grid_search.best_score_}')
print(f'best parameters : {grid_search.best_params_}')


# In[ ]:


# lets make changes in parameters in RandomForestClassifier


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators = 60, criterion = 'gini', max_features = 'log2')
clf.fit(X_train, y_train)


# In[ ]:


predictions_update = clf.predict(X_test)


# In[ ]:


from sklearn.metrics import classification_report
print(classification_report(y_test, predictions_update))


# In[ ]:


# Great ! we got an accuracy of 94


# In[ ]:


from sklearn.model_selection import cross_val_score
scores = cross_val_score(clf, X_train, y_train, cv = 10)
scores.mean()


# In[ ]:


# Great! we got a score of 93


# In[ ]:


# hope you like ths notebook
# thank you

