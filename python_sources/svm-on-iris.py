# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn import svm
from sklearn import metrics

# Any results you write to the current directory are saved as output.
data = pd.read_csv("../input/Iris.csv")

data = data.drop('Id',axis=1)

train,test = train_test_split(data,test_size = 0.1)

train_X = train[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']]
train_Y = train.Species

test_X = test[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']]
test_Y = test.Species

model = svm.SVC()
model.fit(train_X,train_Y)

prediction = model.predict(test_X)

accuracy = metrics.accuracy_score(prediction,test_Y)

print('The accuracy is ',accuracy)