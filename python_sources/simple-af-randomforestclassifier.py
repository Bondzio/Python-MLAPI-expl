#!/usr/bin/env python
# coding: utf-8

# This is my first Jupyter Notebook in which I show how I used RandomForestClassifier to make submission for[ Titanic Competition](https://www.kaggle.com/c/titanic).
# 
# First of all, we need to import necesery libraries and our data:

# In[ ]:


import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

#for splitting given data and checking our results without making submission:
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import recall_score

#for optimizing parameters of our RandomForestClassifier:
from sklearn.model_selection import GridSearchCV

train_data = pd.read_csv("../input/train.csv")


# Then we should do some preprocession and delete irrelevant data(some of which is not totally irrelevant, I just don't know how to process it yet ;P)

# In[ ]:


#X - labels and y - features
X = train_data.drop(["Survived", "Name", "Ticket", "Cabin", "Embarked"], axis=1)
X = X.replace(["male", "female"], [1, 0])
X = X.fillna(X.Age.mean())

y = train_data["Survived"]


# And split it in to be able to make intermediate evaluation of our classifier

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=11)

clf = RandomForestClassifier(max_depth=5, n_estimators=40)
#created classifier with most optimized parameters found by GridSearch

clf.fit(X_train, y_train)

pred = clf.predict(X_test)

print("accuracy: ", accuracy_score(y_test, pred))
print("f1_score: ", f1_score(y_test, pred))
print("precision: ", average_precision_score(y_test, pred))
print("recall: ", recall_score(y_test, pred))


# Fitting our classifier on whole training set

# In[ ]:


test_data = pd.read_csv("../input/test.csv")

test_data = test_data.drop(["Name", "Ticket", "Cabin", "Embarked"], axis=1)
test_data = test_data.replace(["male", "female"], [1, 0])
test_data = test_data.fillna(X.Age.mean())

clf.fit(X, y)


# Predicting test_data labels and making submission

# In[ ]:


PassengerId = test_data['PassengerId']

predictions = clf.predict(test_data)
pd.DataFrame({ "PassengerId": PassengerId, "Survived": predictions }).to_csv("submission.csv", index=False)

