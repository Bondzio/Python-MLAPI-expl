#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import StratifiedShuffleSplit

train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')


# In[ ]:


def encode(train, test):
    le = LabelEncoder().fit(train.species) 
    labels = le.transform(train.species)           # encode species strings
    classes = list(le.classes_)                    # save column names for submission
    test_ids = test.id                             # save test ids for submission
    
    train = train.drop(['species', 'id'], axis=1)  
    test = test.drop(['id'], axis=1)
    
    return train, labels, test, test_ids, classes

train, labels, test, test_ids, classes = encode(train, test)


# In[ ]:


sss = StratifiedShuffleSplit(labels, 10, test_size=0.2, random_state=23)

for train_index, test_index in sss:
    X_train, X_test = train.values[train_index], train.values[test_index]
    y_train, y_test = labels[train_index], labels[test_index]


# In[ ]:


from sklearn.metrics import accuracy_score, log_loss
from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(alpha=1e-4, hidden_layer_sizes=(100, 100, 100), random_state=1)
clf.fit(X_train, y_train)
    
train_predictions = clf.predict(X_test)
acc = accuracy_score(y_test, train_predictions)
print("Accuracy: {:.4%}".format(acc))
    
train_predictions = clf.predict_proba(X_test)
ll = log_loss(y_test, train_predictions)
print("Log Loss: {}".format(ll))


# In[ ]:


test_predictions = clf.predict_proba(test)

submission1 = pd.DataFrame(test_predictions, columns=classes)
submission1.insert(0, 'id', test_ids)
submission1.reset_index()
#submission1 = submission1.drop(submission1.columns[0], axis=1)
submission1.to_csv('submission1.csv')
submission1.tail()

