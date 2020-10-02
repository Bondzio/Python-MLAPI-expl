#!/usr/bin/env python
# coding: utf-8

# Classification models on Iris dataset with Python (first exercise).

# In[ ]:


#Importing the packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_absolute_error


# **Introduction**
# 
# The data set consists of 50 samples from each of three species of Iris (Iris setosa, Iris virginica and Iris versicolor). Four features were measured from each sample: the length and the width of the sepals and petals, in centimeters.
# (source: Wikipedia)

# **Getting Data**

# In[ ]:


dataset = pd.read_csv('../input/irisdataset/iris.csv')


# ##**Understanding a dataset**

# In[ ]:


dataset.head() #first five rows


# In[ ]:


dataset.shape #dimension of dataset


# In[ ]:


dataset.dtypes #type of every variable


# In[ ]:


dataset['variety']=dataset['variety'].astype('category') 


# In[ ]:


dataset.isnull().sum() #how many misssing values we have


# In[ ]:


dataset.info()


# In[ ]:


dataset.variety.value_counts() #frequency by category of dependent variable


# In[ ]:


dataset.describe() #basic statistics


# This dataset has 150 observations and 5 variables.
# We have here 4 numerical features: sepal length, sepal width, petal length and petal width. Variety is a dependent variable with three categories, each of them have a 50 observations.
# We don't have to worry about missing data.
# 

# ##**Visualization**

# In[ ]:


#Boxplots for each independent variable
dataset.plot(kind='box')


# In[ ]:


#Box plots by variety category
dataset.boxplot(by="variety",figsize=(10,10))


# In[ ]:


#Histograms for every numerical variable:
dataset.hist(figsize=(10,5))
plt.show()


# In[ ]:


#Plots by category
sns.pairplot(dataset,hue="variety")


# ##**Classification models**
# 1. Decision Tree
# 2. Random Forest
# 3. K-Nearest Neighbours
# 4. Support Vector Machine
# 5. Naive Bayes

# Trying a few different models on train and test dataset:

# In[ ]:


#Preparing data to the split
X = dataset.iloc[:,:4]
y = dataset.variety

#Splitting the dataset into the train and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 5)
print("X_train:",X_train.shape,
      '\n',"X_test:",X_test.shape,
      '\n',"y_train:",y_train.shape,
      '\n',"y_test:",y_test.shape)


# In[ ]:


#Decision Tree
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
from sklearn.metrics import accuracy_score
print('Accuracy is:',accuracy_score(y_pred,y_test))
pd.concat([X_test, y_test, pd.Series(y_pred, name='predicted', index=X_test.index)], 
          ignore_index=False, axis=1)


# In[ ]:


pd.crosstab(y_test, y_pred, rownames=['variety'], colnames=['predicted'])


# In[ ]:


#Random Forest
model = RandomForestClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
from sklearn.metrics import accuracy_score
print('Accuracy is:',accuracy_score(y_pred,y_test))
pd.concat([X_test, y_test, pd.Series(y_pred, name='predicted', index=X_test.index)], 
          ignore_index=False, axis=1)


# In[ ]:


pd.crosstab(y_test, y_pred, rownames=['variety'], colnames=['predicted'])


# In[ ]:


#K-Nearest Neighbours
model2 = KNeighborsClassifier(n_neighbors=2)
model2.fit(X_train, y_train)
y_pred = model2.predict(X_test)
print('Accuracy is:',accuracy_score(y_pred,y_test))
pd.concat([X_test, y_test, pd.Series(y_pred, name='predicted', index=X_test.index)], 
          ignore_index=False, axis=1)


# In[ ]:


pd.crosstab(y_test, y_pred, rownames=['variety'], colnames=['predicted'])


# In[ ]:


#How many neighbors we need?
scores = []
for n in range(1,15):
    model = KNeighborsClassifier(n_neighbors=n)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    scores.append(accuracy_score(y_pred,y_test))
    
plt.plot(range(1,15), scores)
plt.xlabel('Number of neighbors')
plt.ylabel('Accuracy')
plt.show()


# In[ ]:


#Let's try one more time with 8 neighbors
model3 = KNeighborsClassifier(n_neighbors=8)
model3.fit(X_train, y_train)
y_pred = model3.predict(X_test)
print('Accuracy is:',accuracy_score(y_pred,y_test))
pd.concat([X_test, y_test, pd.Series(y_pred, name='predicted', index=X_test.index)], 
          ignore_index=False, axis=1)


# In[ ]:


pd.crosstab(y_test, y_pred, rownames=['variety'], colnames=['predicted'])


# In[ ]:


#Support Vector Machine
from sklearn.svm import SVC
model5=SVC()
model5.fit(X_train, y_train)
y_pred = model5.predict(X_test)
print('Accuracy is:',accuracy_score(y_pred,y_test))
pd.concat([X_test, y_test, pd.Series(y_pred, name='predicted', index=X_test.index)], 
          ignore_index=False, axis=1)


# In[ ]:


pd.crosstab(y_test, y_pred, rownames=['variety'], colnames=['predicted'])


# In[ ]:


#Naive Bayes
from sklearn.naive_bayes import GaussianNB
model6 = GaussianNB()
model6.fit(X_train, y_train)
y_pred = model6.predict(X_test)
print('Accuracy is:',accuracy_score(y_pred,y_test))
pd.concat([X_test, y_test, pd.Series(y_pred, name='predicted', index=X_test.index)], 
          ignore_index=False, axis=1)


# In[ ]:


pd.crosstab(y_test, y_pred, rownames=['variety'], colnames=['predicted'])

