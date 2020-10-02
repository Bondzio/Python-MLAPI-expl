# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.
import matplotlib.pyplot as plt


# Importing the dataset
dataset = pd.read_csv('../input/mushrooms.csv')
X = dataset.iloc[:, 1:].values
y = dataset.iloc[:, 0].values


# Encoding categorical (nonnumerical) data into numbers ***ALWAYS OMIT ONE DUMMY VAR***
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
for i in range(0,22):
    labelencoder_X = LabelEncoder()
    X[:, i] = labelencoder_X.fit_transform(X[:, i])
labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)
# This makes Spain=2 > Germany=1 > France=0, but we can't say a country is greater than another
# instead we make dummy encoding: three columns for each country with 1 or 0 as the value
onehotencoder= OneHotEncoder(categorical_features = [0,1,2,4,8,10,11,12,13,14,16,17,18,19,20,21])
X = onehotencoder.fit_transform(X).toarray()

# take care of missing data by inputting the mean of the column in the blank
#from sklearn.preprocessing import Imputer
#imputer = Imputer(missing_values = "NaN", strategy = "mean", axis = 0)
#imputer = imputer.fit(X[:, :])
#X[:, :] = imputer.transform(X[:, :])


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)


# Apply Kernel PCA
# This part has two steps: kernel step maps data to higher dimension where it is linearly separable
# PCA part takes this linearly separable data and maps it to a 2D space
from sklearn.decomposition import KernelPCA
kpca = KernelPCA(n_components = 2, kernel = 'linear')
X_train = kpca.fit_transform(X_train)
X_test = kpca.transform(X_test)


# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# Fitting Random Forest classifier to the Training set
# Create your Random Forest classifier here
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=10, random_state=0, criterion='entropy')
classifier.fit(X_train, y_train)


# Predicting the Test set results
y_pred = classifier.predict(X_test)


# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)


# Applying K-fold Cross Validation APPLY TO ALL THE DATA, NOT JUST TRAINING DATA THIS WILL BIAS IT
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=classifier, X=X, y=y, cv=20)
# if working with a lot of data, you can set n_jobs to -1
print('average accuracy of classifier with cross-validation: {}'.format(accuracies.mean()))
print('standard deviation of accuracies with cross-validation: {}'.format(accuracies.std()))


# Visualising the Training set results
from matplotlib.colors import ListedColormap
X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Random Forest (Training set)')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()


# Visualising the Test set results
from matplotlib.colors import ListedColormap
X_set, y_set = X_test, y_test  
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Random Forest (Test set)')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()