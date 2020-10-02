#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


titanic_train = pd.read_csv('/kaggle/input/titanic/train.csv')
titanic_test = pd.read_csv('/kaggle/input/titanic/test.csv')
y_test = pd.read_csv('/kaggle/input/titanic/gender_submission.csv')


# In[ ]:


titanic_train


# In[ ]:


def data_drop(data_file, drop_column):
    data_file.drop([drop_column], axis = 1, inplace = True)
    return data_file


# In[ ]:


def data_assign_new_sex_feature(data, past_value, first_item, second_item):
    data.Sex = [first_item if each == past_value else second_item for each in data.Sex]
    return data


# In[ ]:


def normalize_all_columns(data):
    x = (data - np.min(data)) / (np.max(data) - np.min(data))
    return x


# In[ ]:


def find_best_knn_model(max_range_knn_model, x_train, y_train, x_test, y_test):
    score_list = []
    for each in range (1, max_range_knn_model):
        knn = KNeighborsClassifier(n_neighbors=each)
        knn.fit(x_train, y_train)
        score_list.append(knn.score(x_test, y_test))
    
    best_model_accuracy = np.argmax(score_list)
    
    return best_model_accuracy + 1


# In[ ]:


titanic_train_after_first_drop = data_drop(titanic_train, "Name")


# In[ ]:


titanic_train_after_first_drop


# In[ ]:


titanic_train_after_second_drop = data_drop(titanic_train_after_first_drop, "PassengerId")


# In[ ]:


titanic_train_after_second_drop


# In[ ]:


titanic_train_after_third_drop = data_drop(titanic_train_after_second_drop, "Ticket")


# In[ ]:


titanic_train_after_third_drop


# In[ ]:


titanic_train_after_fourth_drop = data_drop(titanic_train_after_third_drop, "Cabin")


# In[ ]:


titanic_train_after_fourth_drop


# In[ ]:


titanic_train_after_fifth_drop = data_drop(titanic_train_after_fourth_drop, "Embarked")


# In[ ]:


titanic_train_after_fifth_drop


# In[ ]:


data = titanic_train_after_fifth_drop
data


# In[ ]:


data = data_assign_new_sex_feature(data, "male", 1, 0)
data


# In[ ]:


y_train = data.Survived.values
y_train


# In[ ]:


x_train = data_drop(data, "Survived")
x_train


# In[ ]:


x_train = data.fillna(data.mean())
x_train


# In[ ]:


x_train = normalize_all_columns(x_train)
x_train


# In[ ]:


titanic_test_after_first_drop = data_drop(titanic_test, "Name")
titanic_test_after_first_drop


# In[ ]:


titanic_test_after_second_drop = data_drop(titanic_test_after_first_drop, "PassengerId")


# In[ ]:


titanic_test_after_third_drop = data_drop(titanic_test_after_second_drop, "Ticket")


# In[ ]:


titanic_test_after_fourth_drop = data_drop(titanic_test_after_third_drop, "Cabin")


# In[ ]:


titanic_test_after_fifth_drop = data_drop(titanic_test_after_fourth_drop, "Embarked")


# In[ ]:


data_test = titanic_test_after_fifth_drop
data_test


# In[ ]:


data_test = data_assign_new_sex_feature(data_test, "male", 1, 0)
data_test


# In[ ]:


x_test = data_test.fillna(data_test.mean())
x_test


# In[ ]:


x_test = normalize_all_columns(x_test)
x_test


# In[ ]:


y_test = data_drop(y_test, "PassengerId")
y_test


# In[ ]:


k_value = find_best_knn_model(20, x_train, y_train, x_test, y_test)
print(k_value)
knn = KNeighborsClassifier(n_neighbors= k_value)
knn.fit(x_train, y_train)
prediction = knn.predict(x_test)
print(prediction)
accuracy_score = knn.score(x_test, y_test)
print(accuracy_score)
print("For KNN method, Accuration of data is %{}".format(accuracy_score * 100))


# In[ ]:


lr = LogisticRegression()
lr.fit(x_train, y_train)
prediction = lr.predict(x_test)
print(prediction)
accuracy_score = lr.score(x_test, y_test)
print("For Linearregression method, Accuration of data is %{}".format(accuracy_score * 100))


# In[ ]:





# In[ ]:




