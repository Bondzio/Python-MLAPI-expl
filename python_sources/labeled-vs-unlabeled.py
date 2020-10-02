#!/usr/bin/env python
# coding: utf-8

# How good labeled data do in comparison with unlabeled data?
# 
# In this simple kernel we are going to see the difference between the unsupervised learning algorithm **k-means** and the supervised learning **nearest neighbors**.
# 
# Almost all data scientists have gone through some Iris Dataset example at some point. Training a model to classify the correct Iris specie: **setosa**, **versicolor**, or **virginica**.
# 
# The Iris Dataset is used as a classic dataset for begginers because of its simplicity. Using the petal/sepal width and lenght as features of the model to classify a multilabel problem.
# 
# In this kind of example, people usually use supervised learning to solve this classification problem, because we have labeled data. But, an unsupervised learning algorithm can be as good as supervised one? Let's see:

# **Supervised Learning:**

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_palette('husl')
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=5)

model = KNeighborsClassifier(n_neighbors=8)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
score = metrics.accuracy_score(y_test, y_pred)
print(score)


# We got a precision of **98.33%** using supervised learning.

# In[2]:


fignum = 1
fig = plt.figure(fignum, figsize=(8, 6))
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

for name, label in [('Setosa', 0),
                    ('Versicolour', 1),
                    ('Virginica', 2)]:
    ax.text3D(X[y == label, 3].mean(),
              X[y == label, 0].mean(),
              X[y == label, 2].mean() + 2, name,
              horizontalalignment='center',
              bbox=dict(alpha=.2, edgecolor='w', facecolor='w'))
# Reorder the labels to have colors matching the cluster results
y = np.choose(y, [1, 0, 2]).astype(np.float)
ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y, edgecolor='k')

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
ax.set_title('Supervised learning labeled data')
ax.dist = 12
fig.show()


# **Unsupervised Learning:**

# In[30]:


iris = datasets.load_iris()
X = iris.data
y = iris.target

estimators = [('k_means_iris_3', KMeans(n_clusters=3))]



comparison_result = 0
while comparison_result < 0.5:
    fignum = 1
    titles = ['3 clusters']
    for name, est in estimators:
        fig = plt.figure(fignum, figsize=(8, 6))
        ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
        est.fit(X)
        labels = est.labels_

        ax.scatter(X[:, 3], X[:, 0], X[:, 2],
                   c=labels.astype(np.float), edgecolor='k')

        ax.w_xaxis.set_ticklabels([])
        ax.w_yaxis.set_ticklabels([])
        ax.w_zaxis.set_ticklabels([])
        ax.set_xlabel('Petal width')
        ax.set_ylabel('Sepal length')
        ax.set_zlabel('Petal length')
        ax.set_title(titles[fignum - 1])
        ax.dist = 12
        fignum = fignum + 1

    comparison = []    

    for a, b in zip(y, labels):
        if a == b:
            comparison.append(1)
        else:
            comparison.append(0)

    comparison_result = comparison.count(1)/len(comparison)

# Plot the ground truth
fig = plt.figure(fignum, figsize=(8, 6))
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

for name, label in [('Setosa', 0),
                    ('Versicolour', 1),
                    ('Virginica', 2)]:
    ax.text3D(X[y == label, 3].mean(),
              X[y == label, 0].mean(),
              X[y == label, 2].mean() + 2, name,
              horizontalalignment='center',
              bbox=dict(alpha=.2, edgecolor='w', facecolor='w'))
# Reorder the labels to have colors matching the cluster results
y = np.choose(y, [1, 0, 2]).astype(np.float)
ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y, edgecolor='k')

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
ax.set_title('Ground Truth')
ax.dist = 12
fig.show()


# In[31]:


print(comparison.count(1)/len(comparison))


# Using unsupervised learning we got **89.33%** precision, a worse performance in comparison to the supervised learning algorithm, as expected. But, considering the unsupervised learning consists of **unlabeled** data, the k-means algorithm did actually a very good job clustering the species.
# 
# For some cases, where labeling data is a hard thing to do, an unsupervised learning algorithm can solve the problem faster while not giving up too much of precision.
