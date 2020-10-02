#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np                # linear algebra
import pandas as pd               # data frames
import seaborn as sns             # visualizations
import matplotlib.pyplot as plt   # visualizations
import scipy.stats                # statistics
from sklearn.preprocessing import power_transform
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df = pd.read_csv("../input/train-modif/train_2.csv")
print(df.head())
print(df.info())
print(df.shape)


# In[ ]:


df_onehot=df.copy()
df_onehot=pd.get_dummies(df_onehot, columns=["Pclass","Sex"])
df_onehot=df_onehot.drop(columns=["Ticket", "Cabin", "Fare","Age","Title","Status", "Embarked"])
print(df_onehot.head())
print(df_onehot.info())
print(df_onehot.shape)


# In[ ]:


#Escalar datos numericos
df_scale = df_onehot.copy()
scaler = preprocessing.StandardScaler()
columns =df_onehot.columns[2:5]
df_scale[columns] = scaler.fit_transform(df_scale[columns])
df_scale.head()


# In[ ]:


# Create feature and target arrays
# Variables Explicativas
X = df_scale.iloc[:,2:10]
# Variable Respuesta
y = df_scale.iloc[:,1:2]
print(X.info())
print(X.shape)
print(y.info())
print(y.shape)


# In[ ]:


# Split into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=123, stratify=y)
print('X_train:', X_train.shape)
print('X_test:', X_test.shape)


# In[ ]:


# Seleccion of the model to run
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Prepare models
models = []
models.append(('LR', LogisticRegression(solver='lbfgs')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='scale')))
models

results = []
names = []
seed = 123
scoring = 'accuracy'
for name, model in models:
    kfold = model_selection.KFold(n_splits=5, random_state=seed)
    cv_results = model_selection.cross_val_score(model, X_train,y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)


# In[ ]:


plt.figure(figsize=(12,8))
sns.boxplot(x=names, y=results, palette="Set3")
plt.title("Models Accuracy")
plt.show()


# In[ ]:


# Import necessary modules
from scipy.stats import randint
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV

# Setup the parameters and distributions to sample from: param_dist
param_dist = {"max_depth": [3, None],
              "max_features": randint(1, 9),
              "min_samples_leaf": randint(1, 9),
              "criterion": ["gini", "entropy"]}

# Instantiate a Decision Tree classifier: tree
tree = DecisionTreeClassifier()

# Instantiate the Grid Search
tree_cv = RandomizedSearchCV(tree, param_dist, cv=5, scoring=scoring)

# Fit it to the data
tree_cv.fit(X_train, y_train)

# Print the tuned parameters and score
print("Tuned Decision Tree Parameters: {}".format(tree_cv.best_params_))
print("Best score is {}".format(tree_cv.best_score_))


# In[ ]:


from sklearn.model_selection import cross_val_score

# Fit it to the data with new hyper-parameters
new_tree = DecisionTreeClassifier(criterion = 'gini', max_depth = 3, 
                                  max_features = 7, min_samples_leaf = 3)
new_cv = cross_val_score(new_tree, X_train, y_train, cv=5, scoring=scoring)

# Merging the results with the old group of model to compare results
new_results = list(np.vstack((results, new_cv)))
names.append('CART_T')

plt.figure(figsize=(12,8))
sns.boxplot(x=names, y=new_results, palette="Set3")
plt.title("Models Accuracy")
plt.show()


# In[ ]:


from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# Instantiate the model
svm = SVC(gamma='scale')

# Fit the classifier to the training data
svm.fit(X_train, y_train)

# Predict the labels of the test data: y_pred
y_pred = svm.predict(X_test)

# Generate the confusion matrix and classification report
print(classification_report(y_test, y_pred))
sns.heatmap(confusion_matrix(y_test, y_pred),cbar=False,annot=True,fmt="d")


# In[ ]:


predict = pd.read_csv("../input/titanic-modif/test_2.csv")
pred_onehot=predict.copy()
pred_onehot=pd.get_dummies(pred_onehot, columns=["Pclass","Sex"])
pred_onehot=pred_onehot.drop(columns=["Ticket", "Cabin", "Fare","Age","Title", "Status", "Embarked"])
pred_onehot.info()
pred_scale = pred_onehot.copy()
scaler = preprocessing.StandardScaler()
columns =pred_onehot.columns[1:4]
pred_scale[columns] = scaler.fit_transform(pred_scale[columns])
#pred_scale.head()
#pred_scale.info()
#pred_scale.shape

X_predict = pred_scale.iloc[:,1:9]
X_predict.info()
y_predict=svm.predict(X_predict)
y_predict


# In[ ]:


#Generate Submission File

Titanic_Submission=pd.DataFrame({"PassengerId":predict.PassengerId, "Survived":y_predict})
Titanic_Submission.to_csv("Titanic_Submission.csv", index=False)
Titanic_Submission

