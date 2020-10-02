#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # Linear algebra
import pandas as pd # Data processing.

import seaborn as sns # Visualizing (Heat Map)
import matplotlib.pyplot as plt # Visualizing

from sklearn.metrics import confusion_matrix # Comparing

import warnings # For ignore warnings
warnings.filterwarnings("ignore")


# In[ ]:


data = pd.read_csv("../input/data.csv")


# Preparing Data

# In[ ]:


data.drop(["id","Unnamed: 32"],axis = 1, inplace = True)
data.diagnosis = [1 if each == "M" else 0 for each in data.diagnosis]

y = data.diagnosis
x_data = data.drop(["diagnosis"],axis = 1)

x = (x_data - np.min(x_data))/(np.max(x_data)-np.min(x_data)) # Normalize data

compare = []


# Train - Test Split

# In[ ]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.15,random_state = 42)


# # Algorithms
# - K-Nearest Neighbour (KNN) Classification
# - Logistic Regression Classification
# - Naive Bayes Classification
# - Random Forest Classification
# - Suppor Vector Machine (SVM) Classification
# - Decision Tree Classification

# In[ ]:


y_true = y_test


# ## K-Nearest Neighbour (KNN) Classification

# **Firstly, Let's find optimal k value**

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
scores = []
for i in range(1,len(x_test)):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(x_train,y_train)
    scores.append(knn.score(x_test,y_test))
k_value = scores.index(max(scores))+1
print("Optimal n_neighbors values is :", k_value)
# We write max(scores)+1 because normally counting starts from 0 in software but scores list is starting with 1


# Prepare Model

# In[ ]:


knn2 = KNeighborsClassifier(n_neighbors=k_value)
knn2.fit(x_train,y_train) # Fit data
y_predict = knn2.predict(x_test)

cm = confusion_matrix(y_true,y_predict)


# Visualizaiton

# In[ ]:


f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm, annot = True, linewidths = 1, linecolor = "red", fmt = ".0f", ax = ax)
plt.xlabel("Predicted")
plt.ylabel("Real")
plt.show()

knn_correct = cm[1][1] + cm[0][0]
knn_accuracy = knn.score(x_test,y_test)
print("Number of Correct :",knn_correct)
print("KNN accuracy", knn_accuracy)
compare.append(["KNN",knn_correct,knn_accuracy])


# ## Logistic Regression Classification

# Prepare Model

# In[ ]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(x_train,y_train)

y_predict = lr.predict(x_test)

cm = confusion_matrix(y_true,y_predict)


# Visualization

# In[ ]:


f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm, annot = True, linewidths = 1, linecolor = "red", fmt = ".0f", ax = ax)
plt.xlabel("Predicted")
plt.ylabel("Real")
plt.show()

lr_correct = cm[1][1] + cm[0][0]
lr_accuracy = lr.score(x_test,y_test)
print("Number of Correct :",lr_correct)
print("LR accuracy", lr_accuracy)
compare.append(["LR",lr_correct,lr_accuracy])


# ## Naive Bayes Classification

# In[ ]:


from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(x_train,y_train)
y_predict = nb.predict(x_test)

cm = confusion_matrix(y_true,y_predict)


# Visualization

# In[ ]:


f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm, annot = True, linewidths = 1, linecolor = "red", fmt = ".0f", ax = ax)
plt.xlabel("Predicted")
plt.ylabel("Real")
plt.show()

nb_correct = cm[1][1] + cm[0][0]
nb_accuracy = nb.score(x_test,y_test)
print("Number of Correct :",nb_correct)
print("NB accuracy", nb_accuracy)
compare.append(["NB",nb_correct,nb_accuracy])


# ## Random Forest Classification

# **Firstly, Let's find optimal n_estimators value**

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
scores = []
for i in range(1,10):
    rf = RandomForestClassifier(n_estimators = i,random_state = 42)
    rf.fit(x_train,y_train)
    scores.append(rf.score(x_test,y_test))
optimal_n = scores.index(max(scores))+1
print("Optimal n_estimator :", optimal_n)


# Prepare Model

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rf2 = RandomForestClassifier(n_estimators = 8,random_state = 42)
rf2.fit(x_train,y_train)
y_predict = rf2.predict(x_test)

cm = confusion_matrix(y_true,y_predict)


# Visualizing

# In[ ]:


f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm, annot = True, linewidths = 1, linecolor = "red", fmt = ".0f", ax = ax)
plt.xlabel("Predicted")
plt.ylabel("Real")
plt.show()

rf_correct = cm[1][1] + cm[0][0]
rf_accuracy = nb.score(x_test,y_test)
print("Number of Correct :",rf_correct)
print("RF accuracy", rf_accuracy)
compare.append(["RF",rf_correct,rf_accuracy])


# ## Suppor Vector Machine (SVM) Classification

# Prepare Model

# In[ ]:


from sklearn.svm import SVC
svm = SVC(random_state = 42)
svm.fit(x_train,y_train)
y_predict = svm.predict(x_test)

cm = confusion_matrix(y_true,y_predict)


# Visualizing

# In[ ]:


f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm, annot = True, linewidths = 1, linecolor = "red", fmt = ".0f", ax = ax)
plt.xlabel("Predicted")
plt.ylabel("Real")
plt.show()

svm_correct = cm[1][1] + cm[0][0]
svm_accuracy = svm.score(x_test,y_test)
print("Number of Correct :",svm_correct)
print("SVM accuracy", svm_accuracy)
compare.append(["SVM",svm_correct,svm_accuracy])


# ## Decision Tree Classification

# Prepare Mode

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier()
dt.fit(x_train,y_train)
y_predict = dt.predict(x_test)

cm = confusion_matrix(y_true,y_predict)


# Visualize

# In[ ]:


f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm, annot = True, linewidths = 1, linecolor = "red", fmt = ".0f", ax = ax)
plt.xlabel("Predicted")
plt.ylabel("Real")
plt.show()

dt_correct = cm[1][1] + cm[0][0]
dt_accuracy = dt.score(x_test,y_test)
print("Number of Correct :",dt_correct)
print("DT accuracy", dt_accuracy)
compare.append(["DT",dt_correct,dt_accuracy])


# ## Compare

# - K-Nearest Neighbour (KNN) Classification -> KNN
# - Logistic Regression Classification -> LR
# - Naive Bayes Classification -> NB
# - Random Forest Classification -> RF
# - Suppor Vector Machine (SVM) Classification -> SVM
# - Decision Tree Classification -> DT

# In[ ]:


accuracy = []
correct = []
index = []
for i in compare:
    accuracy.append(i[2])
    correct.append(i[1])
    index.append(i[0])
data = {"Correct":correct,"Accuracy":accuracy}

pd.options.display.float_format = '{:,.3f}'.format # We write this code cause of to show 3 digits after the comma
df = pd.DataFrame(data,index = index)
df


# In[ ]:


sns.lineplot(index,correct,color = "red")
plt.xlabel("Algorithms")
plt.ylabel("Number of Correct")
plt.show()


# In[ ]:


sns.lineplot(index,accuracy,color = "blue")
plt.xlabel("Algorithms")
plt.ylabel("Accuracy")
plt.show()


# ## Result

# - **When we look at this comparison, we see that,the most suitable model is Linear Regression. but this does not indicate that it is the best classification algorithm. Since all classification algorithms have different mathematical background, we get different results in different datasets.**
