#!/usr/bin/env python
# coding: utf-8

# 1. Import the csv dataset from https://www.kaggle.com/uciml/adult-census-income

# In[ ]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder


# In[ ]:


adult = pd.read_csv("../input/adult-census-income/adult.csv", sep = ',', names = ['age', 'workclass', 'fnIwgt', 'education', 'education.num', 'marital.status', 'occupation', 'relationship', 'race', 'sex', 'capital.gain', 'capital.loss', 'hours.per.week', 'native.country', 'income'])


# In[ ]:


adult.shape


# In[ ]:


adult.head()


# In[ ]:


adult.tail()


# In[ ]:


adult.describe()


# In[ ]:


n_records = adult.shape[0]
n_greater_50k = adult[adult['income'] == '>50K']. shape[0]
n_at_most_50k = adult[adult['income'] == '<=50K']. shape[0]
greater_percent = (n_greater_50k / n_records) * 100
print("Total number of records: {}".format(n_records))
print("Individuals making more that $50,000: {}".format(n_greater_50k))
print("Individuals making at most $50,000: {}".format(n_at_most_50k))
print("Percentage of individuals making more than $50,00: {}".format(greater_percent))


# In[ ]:


le = LabelEncoder()


# In[ ]:


for col in adult.columns:
    if adult[col].dtypes == 'object':
        adult[col] = le.fit_transform(adult[col])


# In[ ]:


adult.head()


# In[ ]:


dataset = pd.read_csv("../input/adult-census-income/adult.csv")
#removing '?' containing rows
dataset = dataset[(dataset != '?').all(axis=1)]
#label the income objects as 0 and 1
dataset['income'] = dataset['income'].map({'<=50K': 0, '>50K': 1})

sns.catplot( x = 'education.num', y = 'income',data = dataset,kind = 'bar',height = 6)
plt.show()


# In[ ]:


#explore which country do most people belong
plt.figure(figsize=(38,14))
sns.countplot(x='native.country',data=dataset)
plt.show()


# In[ ]:


#marital.status vs income
sns.factorplot(x='marital.status',y='income',data=dataset,kind='bar',height=8)
plt.show()


# In[ ]:


#relationship vs income
sns.factorplot(x='relationship',y='income',data=dataset,kind='bar',size=7)
plt.show()


# In[ ]:


for column in dataset:
    enc=LabelEncoder()
    if dataset.dtypes[column]==np.object:
         dataset[column]=enc.fit_transform(dataset[column])


# In[ ]:


plt.figure(figsize=(14,10))
sns.heatmap(adult.corr(),annot=True,fmt='.2f')
plt.show()


# In[ ]:


from sklearn.preprocessing import LabelEncoder


# In[ ]:


le = LabelEncoder()


# In[ ]:


for col in adult.columns:
    if adult[col].dtypes == 'object':
        adult[col] = le.fit_transform(adult[col])


# In[ ]:


adult.head()


# In[ ]:


X = adult[['age', 'workclass', 'fnIwgt', 'education', 'education.num', 'marital.status', 'occupation', 'relationship', 'race', 'sex', 'capital.gain', 'capital.loss', 'hours.per.week', 'native.country', 'income']]


# In[ ]:


Y = adult.income


# In[ ]:


x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.30, random_state = 42)


# In[ ]:


model = []


# In[ ]:


model.append(("LR", LogisticRegression()))
model.append(("LDA", LinearDiscriminantAnalysis()))
model.append(("KNN", KNeighborsClassifier()))
model.append(("CART", DecisionTreeClassifier()))
model.append(("NB", GaussianNB()))


# In[ ]:


result = []


# In[ ]:


names = []


# In[ ]:


from sklearn import model_selection


# In[ ]:


for name, models in model:
    kfold = model_selection.KFold(n_splits = 10, random_state = 7)
    cv_result = model_selection.cross_val_score(models, x_train, y_train, cv = kfold, scoring = "accuracy")
    result.append(cv_result)
    names.append(name)
    msg = "%s,%f,(%f)" % (name, cv_result.mean(), cv_result.std())
    print(msg)


# ##
# LR,0.999912,(0.000175)
# ##
# LDA,0.789541,(0.006553)
# ##
# KNN,0.752116,(0.011613)
# ##
# CART,0.999956,(0.000132)
# ##
# NB,0.985960,(0.003249)

# In[ ]:




