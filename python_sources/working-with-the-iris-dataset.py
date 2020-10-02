#!/usr/bin/env python
# coding: utf-8

# # **Working with the Iris Species Dataset**
# 
# This is my first notebook on Kaggle and will mainly serve as a way to practice some Machine Learning concepts and exploratory data analysis on a dataset I find particularly interesting. As this is my first notebook, I would appreciate any feedback available!

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#This will just make the notebook easier to read down the line
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# In[ ]:


#Read in the iris dataset and drop the redundant Id column
iris = pd.read_csv('../input/Iris.csv').drop('Id',axis=1)


# In[ ]:


#Check the top of the dataframe
iris.head(5)


# In[ ]:


#More information about the data
iris.info()


# # Exploratory Data Analysis

# In[ ]:


#We'll start off with a pairplot differentiated by species
sns.pairplot(data=iris, hue='Species', palette='inferno')


# In[ ]:


#Let's try looking at the data columns
plt.figure(figsize=(15,10))
plt.subplot(2,2,1)
sns.violinplot(x='Species', y='SepalLengthCm', data=iris, palette='plasma')
plt.subplot(2,2,2)
sns.violinplot(x='Species', y='SepalWidthCm', data=iris, palette='plasma')
plt.subplot(2,2,3)
sns.violinplot(x='Species', y='PetalLengthCm', data=iris, palette='plasma')
plt.subplot(2,2,4)
sns.violinplot(x='Species', y='PetalWidthCm', data=iris, palette='plasma')


# In[ ]:


sns.heatmap(iris.corr(), annot=True, cmap='coolwarm')


# It appears petal length and petal width are the most correlated, followed by sepal length and petal length

# In[ ]:


#Let's see those two plots
plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
sns.scatterplot(x='PetalLengthCm', y='PetalWidthCm', data=iris, hue='Species', palette='inferno')
plt.title('Petal Length vs Petal Width')
plt.subplot(1,2,2)
sns.scatterplot(x='PetalLengthCm', y='SepalLengthCm', data=iris, hue='Species', palette='inferno')
plt.title('Petal Length vs Sepal Length')


# It appears the Setosa species is the most separable, so let's look at that by itself

# In[ ]:


#Make a new dataframe for setosa
setosa = iris[iris['Species']=='Iris-setosa']


# In[ ]:


#Let's see sepal and petal kdeplots for the setosas
plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
sns.kdeplot(setosa['SepalWidthCm'], setosa['SepalLengthCm'], cmap="viridis", shade=True, shade_lowest=False)
plt.title('Setosa Sepal Width vs Sepal Length')
plt.subplot(1,2,2)
sns.kdeplot(setosa['PetalWidthCm'], setosa['PetalLengthCm'], cmap="viridis", shade=True, shade_lowest=False)
plt.title('Setosa Petal Width vs Petal Length')


# # Now on to the Machine Learning part
# First, the train test split

# In[ ]:


from sklearn.model_selection import train_test_split


# We could do a train test split on all the columns of the iris dataframe, but because of the relatively small size of the dataset, we would likely end up getting very high and very similar values for precision and recall (as we will see later). While this is good for a model, it may be more interesting to first predict the species just using the petal information or just using the sepal information to see larger differences between our models

# In[ ]:


#Let's break our train test split into one for petals and one for sepals
X_petal = iris[['PetalLengthCm', 'PetalWidthCm']]
X_sepal = iris[['SepalLengthCm', 'SepalWidthCm']]
y = iris['Species']
X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(X_petal, y, test_size=0.30)
X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_sepal, y, test_size=0.30)


# ## First we'll try Logistic Regression

# In[ ]:


from sklearn.linear_model import LogisticRegression


# In[ ]:


#We'll make the model and fit it to the training data
logmodel_p = LogisticRegression()
logmodel_s = LogisticRegression()
logmodel_p.fit(X_train_p,y_train_p)
logmodel_s.fit(X_train_s,y_train_s)


# In[ ]:


#Now for our predictions
pred_p = logmodel_p.predict(X_test_p)
pred_s = logmodel_s.predict(X_test_s)


# In[ ]:


from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, r2_score


# In[ ]:


#Here is our classification report and confusion matrix for the Logistic Regression model for petals
print(classification_report(y_test_p, pred_p))
print(confusion_matrix(y_test_p, pred_p))


# In[ ]:


#Here is our classification report and confusion matrix for the Logistic Regression model for sepals
print(classification_report(y_test_s, pred_s))
print(confusion_matrix(y_test_s, pred_s))


# In[ ]:


#Print accuracy scores
print('Using Logistic Regression:')
print('The accuracy using Petal information is ' + str(accuracy_score(y_test_p, pred_p)))
print('The accuracy using Sepal information is ' + str(accuracy_score(y_test_s, pred_s)))


# ## Next we'll try K Nearest Neighbors

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier


# We could try various values for n_neighbors to minimize our error, but for simplicity we will just choose n=3

# In[ ]:


#We'll make the model and fit it to the training data using our n neighbors
knn_p = KNeighborsClassifier(n_neighbors=3)
knn_s = KNeighborsClassifier(n_neighbors=3)
knn_p.fit(X_train_p,y_train_p)
knn_s.fit(X_train_s,y_train_s)
pred_p = knn_p.predict(X_test_p)
pred_s = knn_s.predict(X_test_s)


# In[ ]:


#Here is our classification report and confusion matrix for the KNN n=3 model for petals
print(classification_report(y_test_p, pred_p))
print(confusion_matrix(y_test_p, pred_p))


# In[ ]:


#Here is our classification report and confusion matrix for the KNN n=3 model for sepals
print(classification_report(y_test_s, pred_s))
print(confusion_matrix(y_test_s, pred_s))


# In[ ]:


#Print accuracy scores
print('Using KNN:')
print('The accuracy using Petal information is ' + str(accuracy_score(y_test_p, pred_p)))
print('The accuracy using Sepal information is ' + str(accuracy_score(y_test_s, pred_s)))


# ## Next, Decision Trees

# In[ ]:


from sklearn.tree import DecisionTreeClassifier


# In[ ]:


#We'll make the model and fit it to the training data
dtree_p = DecisionTreeClassifier()
dtree_s = DecisionTreeClassifier()
dtree_p.fit(X_train_p,y_train_p)
dtree_s.fit(X_train_s,y_train_s)
pred_p = dtree_p.predict(X_test_p)
pred_s = dtree_s.predict(X_test_s)


# In[ ]:


#Here is our classification report and confusion matrix for the Decision Tree model for petals
print(classification_report(y_test_p, pred_p))
print(confusion_matrix(y_test_p, pred_p))


# In[ ]:


#Here is our classification report and confusion matrix for the Decision Tree model for sepals
print(classification_report(y_test_s, pred_s))
print(confusion_matrix(y_test_s, pred_s))


# In[ ]:


#Print accuracy scores
print('Using a Decision Tree:')
print('The accuracy using Petal information is ' + str(accuracy_score(y_test_p, pred_p)))
print('The accuracy using Sepal information is ' + str(accuracy_score(y_test_s, pred_s)))


# ## Next, expanding to a Random Forest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


#We'll make the model and fit it to the training data using 100 estimators
rfc_p = RandomForestClassifier(n_estimators=100)
rfc_s = RandomForestClassifier(n_estimators=100)
rfc_p.fit(X_train_p, y_train_p)
rfc_s.fit(X_train_s, y_train_s)
pred_p = rfc_p.predict(X_test_p)
pred_s = rfc_s.predict(X_test_s)


# In[ ]:


#Here is our classification report and confusion matrix for the Random Forest model for petals
print(classification_report(y_test_p, pred_p))
print(confusion_matrix(y_test_p, pred_p))


# In[ ]:


#Here is our classification report and confusion matrix for the Random Forest model for sepals
print(classification_report(y_test_s, pred_s))
print(confusion_matrix(y_test_s, pred_s))


# In[ ]:


#Print accuracy scores
print('Using a Random Forest:')
print('The accuracy using Petal information is ' + str(accuracy_score(y_test_p, pred_p)))
print('The accuracy using Sepal information is ' + str(accuracy_score(y_test_s, pred_s)))


# ## Finally, let's use a Support Vector Machine

# In[ ]:


from sklearn.svm import SVC


# In[ ]:


#We'll make the model and fit it to the training data
svc_model_p = SVC()
svc_model_s = SVC()
svc_model_p.fit(X_train_p,y_train_p)
svc_model_s.fit(X_train_s,y_train_s)
pred_p = svc_model_p.predict(X_test_p)
pred_s = svc_model_s.predict(X_test_s)


# In[ ]:


#Here is our classification report and confusion matrix for the SVM model for petals
print(classification_report(y_test_p, pred_p))
print(confusion_matrix(y_test_p, pred_p))


# In[ ]:


#Here is our classification report and confusion matrix for the SVM model for sepals
print(classification_report(y_test_s, pred_s))
print(confusion_matrix(y_test_s, pred_s))


# In[ ]:


#Print accuracy scores
print('Using SVM:')
print('The accuracy using Petal information is ' + str(accuracy_score(y_test_p, pred_p)))
print('The accuracy using Sepal information is ' + str(accuracy_score(y_test_s, pred_s)))


# ## Overall
# It appears that overall it is best to use petal information to predict iris species, rather than sepal data to get a more accurate model

# # Putting it all together
# 
# Now instead of just using either petal data or sepal data, we will use them both to predict the iris species

# In[ ]:


#Another train test split
X = iris.drop('Species', axis=1)
y = iris['Species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)


# ## Logistic Regression

# In[ ]:


#We'll make the model and fit it to the training data
logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)
pred = logmodel.predict(X_test)


# In[ ]:


#Here is our classification report and confusion matrix for the Logistic Regression model
print(classification_report(y_test, pred))
print(confusion_matrix(y_test, pred))


# In[ ]:


#Print accuracy scores
print('Using Logistic Regression:')
print('The accuracy is ' + str(accuracy_score(y_test, pred)))


# ## K Nearest Neighbors
# 
# Similar to earlier, instead of testing different values of n_neighbors to minimize our error, we will just use n=3 for simplicity

# In[ ]:


#We will use n=3
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train,y_train)
pred = knn.predict(X_test)


# In[ ]:


#Here is our classification report and confusion matrix for the KNN n=3 model
print(classification_report(y_test, pred))
print(confusion_matrix(y_test, pred))


# In[ ]:


#Print accuracy scores
print('Using KNN:')
print('The accuracy is ' + str(accuracy_score(y_test, pred)))


# ## Decision Tree

# In[ ]:


#We'll make the model and fit it to the training data
dtree = DecisionTreeClassifier()
dtree.fit(X_train,y_train)
pred = dtree.predict(X_test)


# In[ ]:


#Here is our classification report and confusion matrix for the Decision Tree model
print(classification_report(y_test, pred))
print(confusion_matrix(y_test, pred))


# In[ ]:


#Print accuracy scores
print('Using a Decision Tree:')
print('The accuracy is ' + str(accuracy_score(y_test, pred)))


# ## Random Forest

# In[ ]:


#We'll make the model and fit it to the training data using 100 estimators
rfc = RandomForestClassifier(n_estimators=100)
rfc.fit(X_train, y_train)
pred = rfc.predict(X_test)


# In[ ]:


#Here is our classification report and confusion matrix for the Random Forest model
print(classification_report(y_test, pred))
print(confusion_matrix(y_test, pred))


# In[ ]:


#Print accuracy scores
print('Using a Random Forest:')
print('The accuracy is ' + str(accuracy_score(y_test, pred)))


# ## SVM

# In[ ]:


#We'll make the model and fit it to the training data
svc_model = SVC()
svc_model.fit(X_train,y_train)
pred = svc_model.predict(X_test)


# In[ ]:


#Here is our classification report and confusion matrix for the SVM model
print(classification_report(y_test, pred))
print(confusion_matrix(y_test, pred))


# In[ ]:


#Print accuracy scores
print('Using SVM:')
print('The accuracy is ' + str(accuracy_score(y_test, pred)))


# # Overall
# 
# It appears that using both the petal data and the sepal data together to build our models resulted in equal and better accuracy than the models trained above that used either but not both. Please give me feedback on what you think!

# In[ ]:




