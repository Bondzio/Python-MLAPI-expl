# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.

# Importing the dataset
dataset = pd.read_csv('../input/breastCancer.csv')
#correlatedFeatures = find_correlation(dataset,0.9,True)
#dataset = dataset.drop(correlatedFeatures, axis=1)
dataset.head()

X = dataset.iloc[:, 2:-1].values
y = dataset.iloc[:, 1].values

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
y = le.fit_transform(y)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state =0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

clf = SVC(kernel = 'rbf', random_state = 0,C=10,gamma=0.01)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

ac = accuracy_score(y_test, y_pred)
print("%s : %f %%" % ('SVM:', ac*100))

from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
cm = confusion_matrix(y_test, y_pred)
print(cm)
