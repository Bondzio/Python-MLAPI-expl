#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing the libraries
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from pandas.plotting import scatter_matrix
from sklearn.feature_selection import RFE
from sklearn import model_selection
import matplotlib.pyplot as plt
from sklearn.svm import SVC
import seaborn as sns
import pandas as pd
import numpy as np


# In[ ]:


# Importing the dataset  
dataset = pd.read_csv('../input/Admission_Predict.csv', sep=',')


# In[ ]:


dataset.info()


# We don't need the Searial number feature. 

# In[ ]:


dataset = dataset.drop(["Serial No."], axis=1)


# In[ ]:


print(dataset.columns)


# There's an extra space for the column "Chance of Admit". Let's get rid of it.

# In[ ]:


dataset.rename(columns = {'Chance of Admit ':'Chance of Admit'}, inplace = True)


# In[ ]:


dataset.describe()


# In[ ]:


dataset.head()


# # Visualize data

# ### Box and whisker plots

# In[ ]:


dataset.plot(kind='box', subplots=True, layout=(4,3), figsize=(80, 80), sharex=False, sharey=False)
plt.show()


# ### Histograms

# In[ ]:


dataset.hist(figsize=(20, 20))
plt.show()


# ### Scatter plot matrix

# In[ ]:


sm = scatter_matrix(dataset, alpha=0.2, figsize=(20, 20), diagonal='kde')

# Change label rotation
[s.xaxis.label.set_rotation(45) for s in sm.reshape(-1)]
[s.yaxis.label.set_rotation(0) for s in sm.reshape(-1)]

# May need to offset label when rotating to prevent overlap of figure
[s.get_yaxis().set_label_coords(-0.3,0.5) for s in sm.reshape(-1)]

# Hide all ticks
[s.set_xticks(()) for s in sm.reshape(-1)]
[s.set_yticks(()) for s in sm.reshape(-1)]

plt.show()


# ### Heat map

# We can display a heat map to see the corelation between features.

# In[ ]:


correlation = dataset.corr()
plt.figure(figsize=(14, 12))
heatmap = sns.heatmap(correlation, annot=True, linewidths=0, vmin=-1, cmap="RdBu_r")


# ### Dataframe for specific features

# * TOEFL Score and GRE Score

# In[ ]:


# Create a new dataframe containing only TOEFL Score and GRE Score columns to visualize their co-relations
toefl_gre = dataset[['TOEFL Score', 'GRE Score']]

# Initialize a joint-grid with the dataframe, using seaborn library
gridA = sns.JointGrid(x="GRE Score", y="TOEFL Score", data=toefl_gre, height=6)

# Draws a regression plot in the grid 
gridA = gridA.plot_joint(sns.regplot, scatter_kws={"s": 10})

# Draws a distribution plot in the same grid
gridA = gridA.plot_marginals(sns.distplot)


# * CGPA and Chance of Admit

# In[ ]:


cgpa_admit = dataset[['CGPA', 'Chance of Admit']]
gridB = sns.JointGrid(x="Chance of Admit", y="CGPA", data=cgpa_admit, height=6)
gridB = gridB.plot_joint(sns.regplot, scatter_kws={"s": 10})
gridB = gridB.plot_marginals(sns.distplot)


# * CGPA and GRE Score

# In[ ]:


cgpa_gre = dataset[['CGPA', 'GRE Score']]
gridB = sns.JointGrid(x="GRE Score", y="CGPA", data=cgpa_gre, height=6)
gridB = gridB.plot_joint(sns.regplot, scatter_kws={"s": 10})
gridB = gridB.plot_marginals(sns.distplot)


# * CGPA and TOEFL Score

# In[ ]:


cgpa_toefl = dataset[['CGPA', 'TOEFL Score']]
gridB = sns.JointGrid(x="TOEFL Score", y="CGPA", data=cgpa_toefl, height=6)
gridB = gridB.plot_joint(sns.regplot, scatter_kws={"s": 10})
gridB = gridB.plot_marginals(sns.distplot)


# ### Visualize relationships with bar plots

# In[ ]:


fig, axs = plt.subplots(ncols=1,figsize=(10,6))
sns.barplot(x='TOEFL Score', y='CGPA', data=cgpa_toefl, ax=axs)
plt.title('TOEFL Score VS CGPA')

plt.tight_layout()
plt.show()
plt.gcf().clear()


# In[ ]:


fig, axs = plt.subplots(ncols=1,figsize=(20,12))
sns.barplot(x='CGPA', y='Chance of Admit', data=cgpa_admit, ax=axs)
plt.title('CGPA VS Chance of Admit')

plt.tight_layout()
plt.show()
plt.gcf().clear()


# When CGPA increase, Chance of Admit also increase.

# # Training the models

# ## Data Preparation

# Here, we choosed to apply some transforms to convert our regression problem into a classification problem.

# The chances of admission are given with two decimal places. We are therefore sure not to have a value like "0.499". The data can therefore be separated so that up to 0.49 (less than 50%) the result is "Rejected" and from 0.50 to 1, it is "Accepted".

# In[ ]:


# Defining the splits for categories. 0 to 0.49 will be "Rejected" result, 0.5 to 1 will be "Accepted"
bins = [0,0.49,1]


admission_labels=["Rejected", "Accepted"]
dataset['admission_categorical'] = pd.cut(dataset['Chance of Admit'], bins=bins, labels=admission_labels, include_lowest=True)

display(dataset.head(n=20))

# Split the data into features and target label
admission_raw = dataset['admission_categorical']
features_raw = dataset.drop(['Chance of Admit', 'admission_categorical'], axis = 1)


# ## Splitting the data

# In[ ]:


# Import train_test_split
from sklearn.model_selection import train_test_split

# Split the 'features' and 'income' data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features_raw, 
                                                    admission_raw, 
                                                    test_size = 0.2, 
                                                    random_state = 0)

# Show the results of the split
print("Training set contains {} elements.".format(X_train.shape[0]))
print("Test set contains {} elements.".format(X_test.shape[0]))


# ## K-fold cross validation

# The algorithms we'll be using are : 
# * Logistic regression
# * Decision tree
# * Random forest
# * K-Nearest Neighbors (K-NN)
# * Naive bayes
# * Support Vector Machine (SVM)

# In[ ]:


# 10-fold cross validation
# Test options and evaluation metric
seed = 7
# Using metric accuracy to measure performance
scoring = 'accuracy' 

# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression(solver='saga', multi_class='ovr')))
models.append(('DT', DecisionTreeClassifier(criterion = 'entropy', random_state = 0)))
models.append(('RF', RandomForestClassifier(n_estimators = 100, criterion = 'entropy', random_state = 0)))
models.append(('KNN', KNeighborsClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))

# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = model_selection.KFold(n_splits=10, random_state=seed)
	cv_results = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)


# In[ ]:


# Compare Algorithms
fig = plt.figure("Algorithms comparison")
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()


# ## Predictions

# ### Random Forest

# In[ ]:


# Make predictions on validation dataset
classifier = RandomForestClassifier(n_estimators = 100, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
print(accuracy_score(y_test, y_pred))
print("###")
print(confusion_matrix(y_test,  y_pred))
print("###")
print(classification_report(y_test,  y_pred))


# ### SVM

# In[ ]:


# Make predictions on validation dataset
classifier = SVC(gamma='auto')
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
print(accuracy_score(y_test, y_pred))
print("####")
print(confusion_matrix(y_test,  y_pred))
print("###")
print(classification_report(y_test,  y_pred))


# ### KNN

# In[ ]:


# Make predictions on validation dataset
classifier = KNeighborsClassifier()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
print(accuracy_score(y_test, y_pred))
print("###")
print(confusion_matrix(y_test,  y_pred))
print("###")
print(classification_report(y_test,  y_pred))


# In[ ]:


# Confusion matrix
labels = ['Rejected', 'Accepted']
cm = confusion_matrix(y_test, y_pred, labels)
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(cm)
plt.title('Confusion matrix of the KNN classifier')
fig.colorbar(cax)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()


# # Save model

# In[ ]:


from sklearn.externals import joblib
joblib.dump(classifier, 'knn_admission.joblib')

