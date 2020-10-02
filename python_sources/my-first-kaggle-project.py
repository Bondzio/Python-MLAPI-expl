# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import keras


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

#import os
#print(os.listdir("../input"))
train_data = pd.read_csv("../input/train.csv")
test_data = pd.read_csv("../input/test.csv")

print(train_data.head())
# Any results you write to the current directory are saved as output.

y = train_data['label']
x = train_data.drop('label',axis=1)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.23,random_state=44)
model1 = RandomForestClassifier(random_state=45)
model1.fit(x_train,y_train)
model2 = GaussianNB()
model2.fit(x_train,y_train)

print(model1.score(x_test,y_test))
print(model2.score(x_test,y_test))
print('adsdsd')



