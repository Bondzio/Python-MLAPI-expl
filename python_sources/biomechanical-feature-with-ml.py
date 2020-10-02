#!/usr/bin/env python
# coding: utf-8

# # Explanation

# In this kernel I compared classification methos which are consist of KNN,Logistic regression ,SVM,Naive Bayes,Desicion tree, Random Forest algorithms.

# # Contents

# ### 1) Data manipulation

# ### 2) Normalization

# ### 3) Visualization

# ### 4) Preprocessing

# ### 5) Classification Algorithms

# ### 6) Results and Conclusion

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# # 1) Data Manipulation

# In[ ]:


data = pd.read_csv("../input/column_2C_weka.csv")


# In[ ]:


data.head()


# In[ ]:


data.info()


# In[ ]:


A = data[data["class"] == 'Abnormal']
N = data[data["class"] == 'Normal']


# In[ ]:


A.drop(["class"],axis = 1,inplace = True)
N.drop(["class"],axis = 1,inplace = True)


# # 2) Normalization

# In[ ]:


A = (A-np.min(A))/(np.max(A)-np.min(A))
N = (N-np.min(N))/(np.max(N)-np.min(N))


# # 3) Visualize data

# In[ ]:


plt.scatter(A.pelvic_incidence ,A["pelvic_tilt numeric"] , color = 'red')
plt.scatter(N.pelvic_incidence ,N["pelvic_tilt numeric"] , color = 'green')
plt.xlabel("pelvic tilt")
plt.ylabel("pelvic incidence")
plt.show()


# In[ ]:


sns.countplot(x = "class", data = data)
data["class"].value_counts()


# # 4) Preprocessing 

# In[ ]:


data["class"].replace(["Normal","Abnormal"],[1,0],inplace = True)


# In[ ]:


y = data["class"].values
x_data = data.drop(["class"],axis = 1)
x = (x_data-np.min(x_data))/(np.max(x_data)-np.min(x_data))


# In[ ]:


from sklearn.model_selection import train_test_split 
x_train,x_test,y_train, y_test = train_test_split(x,y,test_size = 0.33 ,random_state = 42)


# In[ ]:


x_list =[]
y_list =[]


# # 5) Classification Algorithms

# ## Logistic_regression (1)

# In[ ]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(x_train,y_train)
prediction = lr.predict(x_test)
print("Logistic regression score :",lr.score(x_test,y_test))
x_list.append("Logistic regression")
y_list.append(lr.score(x_test,y_test))


# ## KNN Classification (2)

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
kn =KNeighborsClassifier(n_neighbors=4)
kn.fit(x_train,y_train)
print("Knn classification score :",kn.score(x_test,y_test))
score=[]
for i in range(1,20):
    kn2 = KNeighborsClassifier(n_neighbors=i)
    kn2.fit(x_train,y_train)
    score.append(kn2.score(x_test,y_test))
plt.plot(score)
x_list.append("Knn classification")
y_list.append(kn.score(x_test,y_test))


# ## Support vector machine classification (SVM) (3)

# In[ ]:


from sklearn.svm import SVC
svm =SVC(random_state=1)
svm.fit(x_train,y_train)
print("svm score : ",svm.score(x_test,y_test))
x_list.append("SVM")
y_list.append(svm.score(x_test,y_test))


# ## Naive Bayes Classification (4)

# In[ ]:


from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(x_train,y_train)
print("Naive bayes score : ",nb.score(x_test,y_test))
x_list.append("Naive Bayes Classification")
y_list.append(nb.score(x_test,y_test))


# ## Desicion tree algorithm (5)

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier()
dt.fit(x_train,y_train)
print("desicion tree score : ",dt.score(x_test,y_test))
x_list.append("Desicion tree")
y_list.append(dt.score(x_test,y_test))


# ## Random forest algorithm (6)

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=50 , random_state=1)
rf.fit(x_train,y_train)
print("random forest score : ",rf.score(x_test,y_test))
x_list.append("Random forest")
y_list.append(rf.score(x_test,y_test))


# ### Evaluating  Models

# In[ ]:


y_true = y_test
y_pred = rf.predict(x_test)


# In[ ]:


from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_true,y_pred)

f,ax = plt.subplots(figsize =(5,5))
sns.heatmap(cm,annot=True,linewidths =0.5,linecolor = "red",fmt = ".0f",ax = ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# ## 6) Results

# In[ ]:


scores = zip(x_list,y_list)
mapped =list(scores)
df = pd.DataFrame(mapped,columns =["label","result"])
df


# In[ ]:


new_df = df["result"].sort_values(ascending = False).index.values
sorted_df = df.reindex(new_df)


# In[ ]:


sorted_df


# In[ ]:


# plot figure
plt.figure(figsize = (10,6))
plt.plot(sorted_df.label,sorted_df.result)
plt.xlabel("Score")
plt.ylabel("Algorithms")
plt.xticks(rotation = 90)
plt.show()


# # 7) Conclusion
# Desicion tree algorithm gives the highest results among the classification methods
