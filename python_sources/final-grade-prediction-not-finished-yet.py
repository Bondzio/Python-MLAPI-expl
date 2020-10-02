#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv("/kaggle/input/student-alcohol-consumption/student-mat.csv")


# In[ ]:


data.head()


# In[ ]:


sns.countplot(x = data.G3)
plt.show()


# In[ ]:


plt.figure(figsize = (14,14))
sns.heatmap(data.corr(),annot = True)
plt.show()


# Effective: medu-fedu-failures-age-traveltime  
# age-abseces  
# traveltime/failrules-walc/dalc  

# In[ ]:


data.columns


# In[ ]:


data.sex=[1 if i == "M" else 0 for i in data.sex]


# In[ ]:


data.famsize=[1 if i == "GT3" else 0 for i in data.famsize]


# In[ ]:


data.address=[1 if i == "U" else 0 for i in data.address]


# In[ ]:


data.internet=[1 if i == "yes" else 0 for i in data.internet]


# In[ ]:


data.romantic=[1 if i == "yes" else 0 for i in data.romantic]


# In[ ]:


data.Pstatus=[1 if i == "A" else 0 for i in data.Pstatus]


# In[ ]:


data.schoolsup=[1 if i == "yes" else 0 for i in data.schoolsup]


# In[ ]:


data.famsup=[1 if i == "yes" else 0 for i in data.famsup]


# In[ ]:


data.paid=[1 if i == "yes" else 0 for i in data.paid]


# In[ ]:


data.activities=[1 if i == "yes" else 0 for i in data.activities]


# In[ ]:


data.nursery=[1 if i == "yes" else 0 for i in data.nursery]


# In[ ]:


data.higher=[1 if i == "yes" else 0 for i in data.higher]


# In[ ]:


data.school=[1 if i == "yes" else 0 for i in data.school]


# In[ ]:


data = pd.get_dummies(data,columns = ["famsize"])


# In[ ]:


data = pd.get_dummies(data,columns = ["Mjob"])


# In[ ]:


data = pd.get_dummies(data,columns = ["Fjob"])


# In[ ]:


data = pd.get_dummies(data,columns = ["reason"])


# In[ ]:


data = pd.get_dummies(data,columns = ["guardian"])


# In[ ]:


#data = pd.get_dummies(data,columns = ["traveltime"])
#data = pd.get_dummies(data,columns = ["famrel"])
#data = pd.get_dummies(data,columns = ["studytime"])
#data = pd.get_dummies(data,columns = ["failures"])
#data = pd.get_dummies(data,columns = ["freetime"])
#data = pd.get_dummies(data,columns = ["goout"])
#data = pd.get_dummies(data,columns = ["Dalc"])
#data = pd.get_dummies(data,columns = ["Walc"])
#data = pd.get_dummies(data,columns = ["health"])
#data = pd.get_dummies(data,columns = ["Medu"])
#data = pd.get_dummies(data,columns = ["Fedu"])


# In[ ]:


data.absences = (data.absences-data.absences.min())/(data.absences.max()-data.absences.min())
data.age = (data.age-data.age.min())/(data.age.max()-data.age.min())
data.Fedu = (data.Fedu-data.Fedu.min())/(data.Fedu.max()-data.Fedu.min())
data.Medu = (data.Medu-data.Medu.min())/(data.Medu.max()-data.Medu.min())
data.health = (data.health-data.health.min())/(data.health.max()-data.health.min())
data.traveltime = (data.traveltime-data.traveltime.min())/(data.traveltime.max()-data.traveltime.min())
data.famrel = (data.famrel-data.famrel.min())/(data.famrel.max()-data.famrel.min())
data.studytime = (data.studytime-data.studytime.min())/(data.studytime.max()-data.studytime.min())
data.failures = (data.failures-data.failures.min())/(data.failures.max()-data.failures.min())
data.freetime = (data.freetime-data.freetime.min())/(data.freetime.max()-data.freetime.min())
data.goout = (data.goout-data.goout.min())/(data.goout.max()-data.goout.min())
data.Dalc = (data.Dalc-data.Dalc.min())/(data.Dalc.max()-data.Dalc.min())
data.Walc = (data.Walc-data.Walc.min())/(data.Walc.max()-data.Walc.min())


# In[ ]:


data.drop(labels="G1",axis = 1,inplace = True)


# In[ ]:


data.drop(labels="G2",axis = 1,inplace = True)


# In[ ]:


data.columns


# In[ ]:


data.G3


# In[ ]:


data.G3=[1 if i > 9  else 0 for i in data.G3]


# In[ ]:


data.G3


# In[ ]:


y = data["G3"].values
x=data.drop(["G3"],axis=1)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.3,random_state = 31)


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
neig = np.arange(1, 25)
train_accuracy = []
test_accuracy = []
for i, k in enumerate(neig):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(x_train,y_train)
    train_accuracy.append(knn.score(x_train, y_train))
    test_accuracy.append(knn.score(x_test, y_test))
print("Best accuracy is {} with K = {}".format(np.max(test_accuracy),1+test_accuracy.index(np.max(test_accuracy))))


# In[ ]:


from sklearn.svm import SVC
svclassifier = SVC(kernel='linear')
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
svclassifier.score(x_test,y_test)


# In[ ]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(x_train,y_train)
print(lr.score(x_test,y_test)*100)


# In[ ]:


y_pred = lr.predict(x_test)
y_true = y_test
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_true,y_pred)
f, ax = plt.subplots(figsize=(8,8))
sns.heatmap(cm,annot = True,linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.title("Confision Matrix")
plt.show()


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rt=RandomForestClassifier(n_estimators=38,random_state=1)
rt.fit(x_train,y_train)

print("score: ",rt.score(x_test,y_test)) 


# In[ ]:


score_list2=[]
for i in range(1,50):
    rt2=RandomForestClassifier(n_estimators=i,random_state=1)
    rt2.fit(x_train,y_train)
    score_list2.append(rt2.score(x_test,y_test))

plt.figure(figsize=(12,8))
plt.plot(range(1,50),score_list2)
plt.xlabel("Esimator values")
plt.ylabel("Acuuracy")
plt.show()


# # Best accuracy is 72% for now 
# # If I play heads or tails, I get more accurate results
# ## But i will improve
# 

# In[ ]:




