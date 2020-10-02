#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn import tree
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
data = pd.read_csv("../input/data.csv",header=0)
# Any results you write to the current directory are saved as output.
print(data.columns)
print(data.shape)


# This data contains 569 rows and 33 columns. As you can see, the last **Unnamed: 32** column is meaningless to us. So we need to drop it, along with the **id** column which are of no use for prediction.
# 

# In[ ]:


data.drop(['Unnamed: 32', 'id'], axis=1, inplace=True)
print(data.columns)  # To check if columns are dropped


# The first column is nothing but the label values that we want to predict. It has 2 classes of labels : M = malignant, B = benign. So we will predict using classification techniques of sklearn.

# In[ ]:


print(data['diagnosis'].value_counts())


# Let's define a function to predict the accuracy and use that function on different models. I am going to use **train_test_split** function that conveniently splits the data into train and test data respectively. It produces four kinds of data:
# X_train & y_train are training samples and labels.
# X_test & y_test are testing samples and labels.
# Then we will set the **test_size** to 0.3 to make use of 30% of data for testing. We will fit the model on training data and later calculate its score with the testing data.

# In[ ]:


def accuracy_predictor(model, data):
    train = data.drop('diagnosis', axis=1)
    label = data['diagnosis']
    X_train, X_test, y_train, y_test = train_test_split(train,
                                                        label,
                                                        test_size=0.3,
                                                        random_state=0)
    clf = model.fit(X_train, y_train)
    print("Using all features %f" % clf.score(X_test, y_test))


# Lets test our function using support vector classifier.

# In[ ]:


clf = svm.SVC(kernel='linear', C=1)
accuracy_predictor(clf, data)


# By all features, I mean that we are using all the columns for prediction even if they are highly correlated. To make it more optimized, we will see how much different columns are correlated to each other, and make use of only useful features.

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
# I will make use of all features which are labelled as *.mean 
features_mean = ['radius_mean', 'texture_mean', 'perimeter_mean',
                 'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean',
                 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean']
corr = data[features_mean].corr()
plt.figure(figsize=(8,8))
sns.heatmap(corr, cbar = True,  square = True, annot=True, fmt= '.2f',annot_kws={'size': 8},
           xticklabels= features_mean, yticklabels= features_mean,
           cmap= 'coolwarm') 
plt.show()


# This heatmap shows how highly radius, parameter and area are related. Additionally, concavity, concave points and compactness are related. So lets choose any one from each and the remaining ones and make changes in our function. 

# In[ ]:


def accuracy_predictor(model, data):
    train = data.drop('diagnosis', axis=1)
    label = data['diagnosis']
    X_train, X_test, y_train, y_test = train_test_split(train,
                                                        label,
                                                        test_size=0.3,
                                                        random_state=0)
    clf = model.fit(X_train, y_train)
    print("Using all features %f" % clf.score(X_test, y_test))
    unique_mean_features = ['radius_mean', 'texture_mean', 'smoothness_mean',
                            'compactness_mean', 'symmetry_mean',
                            'fractal_dimension_mean']
    new_train = data[unique_mean_features]
    X_train, X_test, y_train, y_test = train_test_split(new_train,
                                                        label,
                                                        test_size=0.3,
                                                        random_state=0)
    clf = model.fit(X_train, y_train)
    print("With independent mean features: %f" % clf.score(X_test, y_test))


# Lets try again on SVM.

# In[ ]:


clf = svm.SVC(kernel='linear', C=1)
accuracy_predictor(clf, data)


# Now I will make use of different classification model i.e. Decision Trees.

# In[ ]:


clf = tree.DecisionTreeClassifier()
accuracy_predictor(clf, data)


# Decision Trees here are giving less score than SVMs, so obviously SVMs seem better. Lets try k Nearest Neighbors now.
# In the model for kNN, we can use different algorithms like 'auto', 'ball_tree', 'kd_tree' or 'brute'. You can study which one to use and why from http://scikit-learn.org/stable/modules/neighbors.html
# Let us set neighbors of 5 for our prediction.

# In[ ]:


knn = KNeighborsClassifier(n_neighbors=5,
                           algorithm='ball_tree'
                          )
accuracy_predictor(knn, data)


# Score is lower than SVMs. So you will say SVM wins. But if you notice, there is **n_neighbors** which is actually playing the game here. So we will try the prediction score taking different values for k.

# In[ ]:


for neighbor in range(3, 20):
    print("Iteration %d" % neighbor)
    knn = KNeighborsClassifier(n_neighbors=neighbor,
                               algorithm='ball_tree'
                               )
    accuracy_predictor(knn, data)


# You can see now how much score changes when we change the number of neighbors used. 
# Conclusions:
# 
# 1) Using all features, k = 10 seems to optimize the prediction giving 96.49% score.
# 
# 2) Using only uniques mean features, k = 9 gives 90.64%
# 
# I will make simple curve to show how scores vary with this parameter k.

# In[ ]:


from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

x = range(3, 20)
# y1 and y2 are scores when using all features and unique features respectively.
# I made slight changes in the function and appended the scores in two lists.
# I am not posting that basic code.
y1 = [0.9181286549707602, 0.9298245614035088, 0.9473684210526315, 0.9473684210526315, 0.9532163742690059, 0.9532163742690059,
      0.9590643274853801, 0.9649122807017544, 0.9649122807017544, 0.9649122807017544,
      0.9649122807017544, 0.9649122807017544, 0.9649122807017544, 0.9649122807017544,
      0.9649122807017544, 0.9649122807017544, 0.9649122807017544]
y2 = [0.8421052631578947,
      0.8596491228070176, 0.8771929824561403, 0.8830409356725146, 0.8888888888888888,
      0.9005847953216374, 0.9064327485380117, 0.8888888888888888, 0.8947368421052632,
      0.8947368421052632, 0.8947368421052632, 0.9005847953216374, 0.8947368421052632,
      0.8947368421052632, 0.9005847953216374, 0.9005847953216374, 0.9064327485380117]
f1 = interp1d(x, y1, kind='cubic')
f2 = interp1d(x, y2, kind='cubic')
plt.plot(x, f1(x), '-', x, f2(x), '--')
plt.legend(['all features', 'unique mean features'], loc='best')
plt.show()


# Now you can easily see from here which k value gives highest score, without manually looking the ouput. This process is nothing but hyper-parameter optimization. 
# 
# Hyper-parameters are parameters that are not directly learnt within estimators. In scikit-learn they are passed as arguments to the constructor of the estimator classes.
# Here k is that parameter.
# 
# You can use different values for different model classes to understand which value gives the best possible score.
# You can try the above function on different classification algorithms too and test which model can be used best on this data.
# 
# 
# 
# 
