import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import os
dataset = pd.read_csv("../input/heart.csv")
X = dataset.iloc[:,0:13].values
y = dataset.iloc[:,1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting K-NN to the Training set
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)


##Using multivariate regression predicting heart disease
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
dataset = pd.read_csv("../input/heart.csv")

# Any results you write to the current directory are saved as output.
X=dataset.iloc[:,0:13].values
y=dataset.iloc[:,13].values


#building the optimal model using backward elimination
import statsmodels.formula.api as sm
X=np.append(arr=np.ones((303,1)).astype(int),values=X,axis=1)
X_opt=X[:,[0, 1, 2, 3, 4, 5,6,7,8,9,10,11,12,13]]
regressor_OLS = sm.OLS(endog=y,exog=X_opt).fit()
regressor_OLS.summary()
X_opt=X[:,[0, 1, 3, 4, 5,6,7,8,9,10,11,12,13]]#removed cp
regressor_OLS = sm.OLS(endog=y,exog=X_opt).fit()
regressor_OLS.summary()

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)


#fiiting simple linear regression

from sklearn.linear_model import LinearRegression
regressor=LinearRegression()
regressor.fit(X_train,y_train)

#prediction
y_pred=regressor.predict(X_test)


#applying sigmoid 1 if y_pred>=0.5 else 0

for i in range(0,len(y_pred)):
    if y_pred[i]>=0.5:
        y_pred[i]=int(1)
    else:
        y_pred[i]=int(0)














