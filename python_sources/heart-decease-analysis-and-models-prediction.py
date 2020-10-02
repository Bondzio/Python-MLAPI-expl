#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


#Data Visualization
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import cufflinks as cf
import plotly.offline
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)


get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')

#Machine Learning 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

#Spliting the Data
from sklearn.model_selection import train_test_split

#Standard Scaler
from sklearn.preprocessing import StandardScaler

#Model Prediction
from sklearn.metrics import classification_report,confusion_matrix,roc_curve,auc
from sklearn.model_selection import cross_val_score


# **Data Processing**

# In[ ]:


data = pd.read_csv("/kaggle/input/heart-disease-uci/heart.csv")
data.head()


# In[ ]:


data.info()


# In[ ]:


data.describe()


# Checking for Null Values

# In[ ]:


data.isna().any()


# # **Feature Selection**

# In[ ]:


sns.pairplot(data=data)


# In[ ]:


#get correlations of each features in dataset
corrmat = data.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
#plot heat map
g=sns.heatmap(data[top_corr_features].corr(),annot=True,cmap="RdYlGn")


# # **Data Visualization**

# In[ ]:


data.hist(figsize=(20,20))


# **Checking Dataset is a Balanced Dataset or Imbalanced Dataset**

# In[ ]:


sns.countplot(x='target',data=data, palette = "coolwarm_r")


# Data looks like 40 60 propotion. So i am treating it as Balanced Data set.

# In[ ]:


pd.set_option('display.max_rows',None)
print(data.age)


# In[ ]:


print("Min Age:",data.age.min(),", Max Age:",data.age.max())


# In[ ]:


fig = px.pie(data, values='target', names='age', title='Total no of targets based on Age')
fig.update_traces(textposition='inside')
fig.show()


# In[ ]:


data["Male"]=data[data["sex"]==1]["age"]
data["Female"]=data[data["sex"]==0]["age"]
data[["Male","Female"]].iplot(kind="histogram", bins=20, theme="white", title="Heart Patient Ages based on sex",
         xTitle='Ages', yTitle='Count')


# In[ ]:


desease_sex = data[data['target']==1]['sex'].value_counts()
not_desease_sex= data[data['target']==0]['sex'].value_counts()
df1 = pd.DataFrame([desease_sex,not_desease_sex])
df1.index = ['Diagnose','Not Diagnose']
df1.iplot(kind='bar',barmode='stack', title='Diagnose or Not with heart desease by the Sex')


# In[ ]:


sns.countplot(x='cp',data=data, palette = "coolwarm_r")


# Side by Side Graphs for Age,Chest Pain Type,Maximum Heart Rate Achieved with Respect to Target

# In[ ]:


pd.crosstab(data.age,data.target).plot(kind="bar",figsize=(20,6))
plt.title('Heart Disease Frequency for Ages')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()


# In[ ]:


pd.crosstab(data.cp,data.target).plot(kind="bar",figsize=(15,6))
plt.title('Heart Disease Frequency for Chest Pain Type')
plt.xlabel('Chest Pain Type')
plt.ylabel('Frequency')
plt.show()


# In[ ]:


pd.crosstab(data.thalach,data.target).plot(kind="bar",figsize=(20,6))
plt.title('Heart Disease Frequency for Maximum Heart Rate Achieved')
plt.xlabel('Maximum Heart Rate Achieved')
plt.ylabel('Frequency')
plt.show()


# # **Model Processing**

# In[ ]:


df = pd.get_dummies(data, columns = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'])


# In[ ]:


standardScaler = StandardScaler()
columns_to_scale = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
df[columns_to_scale] = standardScaler.fit_transform(df[columns_to_scale])


# In[ ]:


df.head()


# Droping the Extra Coulmns and creating the Predictors 

# In[ ]:


y = df['target']
X = df.drop(['target','Male','Female'], axis = 1)


# In[ ]:


y.head()


# In[ ]:


#ROC Curve
def rocCurve(model):
    y_prob = model.predict_proba(X_test)[:,1]
    fpr, tpr, thr = roc_curve(y_test, y_prob)
    lw = 2
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, 
          color='darkorange', 
          lw=lw, 
          label="Curve Area = %0.3f" % auc(fpr, tpr))
    plt.plot([0, 1], [0, 1], color='green', 
                 lw=lw, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic Plot')
    plt.legend(loc="lower right")
    plt.show()


# # **KNN Model**

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.30)


# In[ ]:


accuracy_rate = []
for k in range(1,21):
    knn_classifier = KNeighborsClassifier(n_neighbors = k)
    knn_accuracy_score=cross_val_score(knn_classifier,X,y,cv=10)
    accuracy_rate.append(round(knn_accuracy_score.mean()*100,2))


# In[ ]:


print(accuracy_rate)


# In[ ]:


error_rate = []
for k in range(1,21):
    knn_classifier = KNeighborsClassifier(n_neighbors = k)
    knn_error_score=cross_val_score(knn_classifier,X,y,cv=10)
    error_rate.append(round(1- knn_error_score.mean(),2))


# In[ ]:


print(error_rate)


# In[ ]:


plt.figure(figsize=(10,6))
#plt.plot(range(1,21),error_rate,color='blue', linestyle='dashed', marker='o',
         #markerfacecolor='red', markersize=10)
plt.plot(range(1,21),accuracy_rate,color='blue', linestyle='dashed', marker='o',
         markerfacecolor='red', markersize=10)
plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')


# In[ ]:


plt.figure(figsize=(20,6))
plt.plot([k for k in range(1, 21)], accuracy_rate, color = 'blue', linestyle='dashed', marker='o',markerfacecolor='red')
for i in range(1,21):
    plt.text(i, accuracy_rate[i-1], (i, accuracy_rate[i-1]))
plt.xticks([i for i in range(1, 21)])
plt.xlabel('Number of Neighbors (K)')
plt.ylabel('Scores')
plt.title('K Neighbors Classifier scores for different K values')


# From above plot we can see the accuracy of score is good when k value is 10, 9, 12. So we can choose any value from these three values to calculate the Score for KNN Model.

# In[ ]:


knn = KNeighborsClassifier(n_neighbors=1)

knn.fit(X_train,y_train)
knn_pred = knn.predict(X_test)

print('K=1')
print(classification_report(y_test,knn_pred))


# In[ ]:


plt.figure(figsize=(5, 5))
sns.heatmap(confusion_matrix(y_test,knn_pred), square=True, 
                    cmap="Greens",
                    annot=True, 
                    cbar=False, 
                    xticklabels=["Haven't Disease", "Have Disease"], 
                    yticklabels=["Haven't Disease","Have Disease"])
plt.title("Confusion Matrix With K =1")
plt.xlabel('Predicted Values')
plt.ylabel('True Values');
plt.show();


# In[ ]:


# NOW WITH K=10
knn_classifier = KNeighborsClassifier(n_neighbors=12)
knn_score=cross_val_score(knn_classifier,X,y,cv=10)

knn_classifier.fit(X_train,y_train)
knn_y_pred = knn_classifier.predict(X_test)

print('K=10')
print(classification_report(y_test,knn_y_pred))


# In[ ]:


plt.figure(figsize=(5, 5))
sns.heatmap(confusion_matrix(y_test,knn_y_pred), square=True, 
                    cmap="Purples",
                    annot=True, 
                    cbar=False, 
                    xticklabels=["Haven't Disease", "Have Disease"], 
                    yticklabels=["Haven't Disease","Have Disease"])
plt.title("Confusion Matrix With K =10")
plt.xlabel('Predicted Values')
plt.ylabel('True Values');
plt.show();


# In[ ]:


knn_accuracy_score= round(knn_score.mean()*100,2)
knn_accuracy_score


# In[ ]:


#ROC Curve
rocCurve(knn_classifier)


# # **RandomForestClassifier**

# In[ ]:


randomforest_classifier= RandomForestClassifier(n_estimators=10,random_state=1)
rdm_score=cross_val_score(randomforest_classifier,X,y,cv=10)


# In[ ]:


rdm_accuracy = round(rdm_score.mean()*100,2)
rdm_accuracy


# In[ ]:


randomforest_classifier.fit(X_train,y_train)
rfc_y_pred = randomforest_classifier.predict(X_test)
print(classification_report(y_test,rfc_y_pred))


# In[ ]:


plt.figure(figsize=(5, 5))
sns.heatmap(confusion_matrix(y_test,rdf_y_pred), square=True, 
                    cmap="Oranges",
                    annot=True, 
                    cbar=False, 
                    xticklabels=["Haven't Disease", "Have Disease"], 
                    yticklabels=["Haven't Disease","Have Disease"])
plt.title("Random Forrest Confusion Matrix")
plt.xlabel('Predicted Values')
plt.ylabel('True Values');
plt.show();


# In[ ]:


rocCurve(randomforest_classifier)


# # **SVC**

# In[ ]:


from sklearn.svm import SVC
svc = SVC(C=5, probability=True)
score_svc = cross_val_score(svc,X,y,cv=10)


# In[ ]:


svc_accuracy = round(score_svc.mean()*100,2)
svc_accuracy


# In[ ]:


svc.fit(X_train,y_train)
svc_y_pred = svc.predict(X_test)
print(classification_report(y_test,svc_y_pred))


# In[ ]:


plt.figure(figsize=(5, 5))
sns.heatmap(confusion_matrix(y_test,svc_y_pred), square=True, 
                    cmap="Pastel1",
                    annot=True, 
                    cbar=False, 
                    xticklabels=["Haven't Disease", "Have Disease"], 
                    yticklabels=["Haven't Disease","Have Disease"])
plt.title("SVC Confusion Matrix")
plt.xlabel('Predicted Values')
plt.ylabel('True Values');
plt.show();


# In[ ]:


#ROC Curve
rocCurve(svc)


# In[ ]:


decisiontree_classifier = DecisionTreeClassifier(random_state=0)
dtc_score=cross_val_score(decisiontree_classifier,X,y,cv=10)


# In[ ]:


dtc_accuracy = round(dtc_score.mean()*100,2)
dtc_accuracy


# In[ ]:


decisiontree_classifier.fit(X_train,y_train)
dtc_y_pred = decisiontree_classifier.predict(X_test)
print(classification_report(y_test,dtc_y_pred))


# In[ ]:


plt.figure(figsize=(5, 5))
sns.heatmap(confusion_matrix(y_test,dtc_y_pred), square=True, 
                    cmap="BuGn",
                    annot=True, 
                    cbar=False, 
                    xticklabels=["Haven't Disease", "Have Disease"], 
                    yticklabels=["Haven't Disease","Have Disease"])
plt.title("Decision Tree Confusion Matrix")
plt.xlabel('Predicted Values')
plt.ylabel('True Values');
plt.show();


# In[ ]:


#ROC Curve
rocCurve(decisiontree_classifier)


# In[ ]:


names=["KNN","Random Forest","Decesion Tree","SVC"]
accs =[knn_accuracy_score,rdm_accuracy,dtc_accuracy,svc_accuracy]
sns.set_style("whitegrid")
plt.figure(figsize=(8,6))
plt.ylabel("Accuracy")
plt.xlabel("Algorithms")
sns.barplot(x=names, y=accs)
plt.show()

