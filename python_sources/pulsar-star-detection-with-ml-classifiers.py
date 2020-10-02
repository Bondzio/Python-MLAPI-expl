#!/usr/bin/env python
# coding: utf-8

# # Contents
# 

# 1. Introduction
# 2. Read and Overview Data
# 3. Data Preparation
# 4. Logistic Regression
# 5. KNN
# 6. SVM
# 7. Recision Tree
# 8. Random Forrest
# 9. Naive Bayes
# 10. Compare Scores
# 11. Conclusion

# # 1. Introduction
# 
# In this kernel we will do the determination of pulsar star according to the Predicting a Pulsar Star dataset. We will use mechine learning classifiers while determining. These classifiers are Logistic Regression, KNN, SVM, Naive Bayes, Decision Tree and Random Forrest. Finally we will compare them according to scores and Confusion Matrix

# # 2. Read and Overview Data
# 

# * Modules

# In[75]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.plotly as py
from plotly.offline import init_notebook_mode,iplot
init_notebook_mode(connected = True)
import plotly.graph_objs as go

from sklearn.metrics import confusion_matrix
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# * Read dataset with pandas

# In[76]:


data = pd.read_csv("../input/pulsar_stars.csv")


# * first 5 component of data

# In[77]:


data.head() #using pandas head function for first 5 component


# In[78]:


# information about dataset
data.info()


# everything looks fine

# # 3. Data Preparation

# * Choose x and y values for machine learning algorithms
# * y values are binary result
# * x values are features

# In[79]:


y = data.target_class # target class chosen as y values
x_data = data.drop(["target_class"],axis = 1) 
x = (x_data - np.min(x_data))/(np.max(x_data)-np.min(x_data)).values # normalization x values


# In[80]:



f,ax = plt.subplots(figsize=(7,7))

sns.heatmap(x.corr(),annot = True ,linewidths = .4,ax = ax)


# * Then we will x and y values split as test and train with sklearn module

# In[81]:


from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 42) #20% test and 80% train
# 


# * Transactions complated we can start the algorithms

# # 4. Logistic Regression 

# In[82]:


# implement lr with sklearn
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression()

lr.fit(x_train,y_train)

form = lr.score(x_test,y_test)*100
print("Random Forrest accuracy : {0:.2f}%".format(form))


# In[96]:


from sklearn.metrics import confusion_matrix
# Calculation of counfusion matrix
y_pred = lr.predict(x_test)
y_true = y_test
cm = confusion_matrix(y_true,y_pred)
# and plotting
f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm,annot = True,linewidths=.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# # 5.  KNN

# In[84]:


from sklearn.neighbors import KNeighborsClassifier
# implement knn with sklearn
knn = KNeighborsClassifier(n_neighbors=9)
knn.fit(x_train,y_train)

form = knn.score(x_test,y_test)*100
print("KNN accuracy : {0:.2f}%".format(form))


# In[85]:


# Calculation of counfusion matrix
y_pred = knn.predict(x_test)
y_true = y_test
cm = confusion_matrix(y_true,y_pred)
# and plotting
f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm,annot = True,linewidths=.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# # 6. SVM

# In[86]:


from sklearn.svm import SVC
# implement svm with sklearn
ssvm = SVC(random_state=42)
ssvm.fit(x_train,y_train)
form = ssvm.score(x_test,y_test)*100
print("SVM Accuracy : {0:.2f}%".format(form))


# In[87]:


# Calculation of counfusion matrix
y_pred = ssvm.predict(x_test)
y_true = y_test
cm = confusion_matrix(y_true,y_pred)
# and plotting
f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm,annot = True,linewidths=.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# # 7. Decision Tree 

# In[88]:


from sklearn.tree import DecisionTreeClassifier
# implement decision tree with sklearn
dt = DecisionTreeClassifier()
dt.fit(x_train,y_train)
form = dt.score(x_test,y_test)*100
print("Decision Tree Accuracy : {0:.2f}%".format(form))


# In[89]:


# Calculation of counfusion matrix
y_pred = dt.predict(x_test)
y_true = y_test
cm = confusion_matrix(y_true,y_pred)
# and plotting
f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm,annot = True,linewidths=.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# # 8. Random Forest  

# In[90]:


from sklearn.ensemble import RandomForestClassifier
# implement random forest with sklearn
rf = RandomForestClassifier(n_estimators=200,random_state=42)
rf.fit(x_train,y_train)
form = rf.score(x_test,y_test)*100
print("Random Forrest accuracy : {0:.2f}%".format(form))


# In[91]:


# Calculation of counfusion matrix
y_pred = rf.predict(x_test)
y_true = y_test
cm = confusion_matrix(y_true,y_pred)
# and plotting
f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm,annot = True,linewidths=.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# # 9. Naive Bayes 

# In[92]:


from sklearn.naive_bayes import GaussianNB
# implement naive bayes with sklearn
nb = GaussianNB()
nb.fit(x_train,y_train)
form = nb.score(x_test,y_test)*100
print("Naive Bayes accuracy : {0:.2f}%".format(form))


# In[93]:


# Calculation of counfusion matrix
y_pred = nb.predict(x_test)
y_true = y_test
cm = confusion_matrix(y_true,y_pred)
# and plotting
f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(cm,annot = True,linewidths=.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# # 10. Compare Scores

# * We will compare scores with pie chard
# * Use piechard because see the accuracy rate between each other

# In[94]:


#score list and name list created
scores = [lr.score(x_test,y_test)*100,ssvm.score(x_test,y_test)*100,knn.score(x_test,y_test)*100,
    dt.score(x_test,y_test)*100,rf.score(x_test,y_test)*100,nb.score(x_test,y_test)*100]
names = ["Logistic Regression","SVM","KNN","Decision Tree","Random Forest","Naive Bayes"]


# In[95]:


fig = {
  "data": [
    {
      "values": scores,
      "labels": names,
      "domain": {"x": [0, .5]},
      "name": "Score Rates",
      "hoverinfo":"label+percent+name",
      "hole": .3,
      "type": "pie"
    },],
  "layout": {
        "title":"Classifier Algorithms Score Rates",
        "annotations": [
            { "font": { "size": 20},
              "showarrow": False,
              "text": "Classifier Rates",
                "x": 0.20,
                "y": 1
            },
        ]
    }
}
iplot(fig)


# # 11. Conclusion
# * Classifications applied to data
# * Score values obtained and compared
# * According to this data, the most efficient result was KNN classification

# In[ ]:





# In[ ]:




