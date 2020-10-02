#!/usr/bin/env python
# coding: utf-8

# Machine learning is an application of artificial intelligence (AI) that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. Machine learning (ML) techniques allows us to obtain predictive, the dataset we are testing is pima-indian-diabetes with a dataset of 765 raw data with 8 data features and 1 data label we developed a method to achieve the best accuracy from the 5 methods we use with the stages of separation traning and testing the dataset, scaling features, parameters evaluation, confusion matrix and we get the accuracy of each method, and the results of the accuracy we get with these 5 methods Gradient-boasting is best with an accuracy score of 0.8, Decision Tree 0.72, Random Forest 0.72, next is Logistic Regression 0.7, and then followed by K-NN method with a score of 0.65

# In[ ]:


#import library

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import GridSearchCV 
#modeling parametes
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve

import os
print(os.listdir("../input"))


# In[ ]:


#read data
dataset = pd.read_csv("../input/pima-indians-diabetes-database/diabetes.csv")
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 8].values
print(dataset)



# In[ ]:


dataset.head()


# In[ ]:


dataset.info()


# In[ ]:


import itertools

columns=dataset.columns[:8]
plt.subplots(figsize=(18,15))
length=len(columns)
for i,j in itertools.zip_longest(columns,range(length)):
    plt.subplot((length/2),3,j+1)
    plt.subplots_adjust(wspace=0.2,hspace=0.5)
    dataset[i].hist(bins=20,edgecolor='black')
    plt.title(i)
plt.show()


# In[ ]:


data1 = dataset[dataset["Outcome"]==1]
columns = dataset.columns[:8]
plt.subplots(figsize=(18,15))
length =len(columns)
for i,j in itertools.zip_longest(columns,range(length)):
    plt.subplot((length/2),3,j+1)
    plt.subplots_adjust(wspace=0.2,hspace=0.5)
    plt.ylabel("Count")
    data1[i].hist(bins=20,edgecolor='black')
    plt.title(i)
plt.show()


# In[ ]:


print(dataset.groupby('Outcome').size())


# In[ ]:


import seaborn as sns
sns.countplot(dataset['Outcome'],label="Count")


# In[ ]:


sns.pairplot(data=dataset,hue='Outcome',diag_kind='kde')
plt.show()


# In[ ]:


# Splitting the dataset into the Training set and Test set
# Memisahkan dataset ke dalam set Pelatihan dan set Tes
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, 
                                                    random_state = 42)


# In[ ]:


X_train.shape


# In[ ]:


X_test.shape


# In[ ]:


y_train.shape


# In[ ]:


y_test.shape


# In[ ]:


#scalling feature
import seaborn as sns
# fig, (ax2) = plt.subplots(ncols=1, figsize=(6, 5))
# x = pd.DataFrame({
#     # Distribution with lower outliers
#     'x1': np.concatenate([np.random.normal(20, 1, 1000), np.random.normal(1, 1, 25)]),
#     # Distribution with higher outliers
#     'x2': np.concatenate([np.random.normal(30, 1, 1000), np.random.normal(50, 1, 25)]),
# })

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
#x
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
#y
# y_train = sc.fit_transform(y_train)
# y_test = sc.transform(y_test)


                                            
# scaled_df = pd.DataFrame(X_train,columns=['x1', 'x2','x3','x4','x5','x6','x7','x8'])
# ax2.set_title('testing')                                                                                        
# sns.kdeplot(scaled_df['x1'], ax=ax2)
# sns.kdeplot(scaled_df['x2'], ax=ax2)
# sns.kdeplot(scaled_df)
# plt.show
print('ini data x train',X_train)
print('ini data x train',X_test)


# In[ ]:


#gradient boasting method 

# Parameter evaluation with GSC validation
gbe = GradientBoostingClassifier(random_state=42)
parameters={'learning_rate': [0.05, 0.1, 0.5],
            'max_features': [0.5, 1],
            'max_depth': [3, 4, 5]
}
gridsearch=GridSearchCV(gbe, parameters, cv=100, scoring='roc_auc')
gridsearch.fit(X, y)
print(gridsearch.best_params_)
print(gridsearch.best_score_)


# In[ ]:


#gradient boasting method 

# Adjusting development threshold
gbi = GradientBoostingClassifier(learning_rate=0.05, max_depth=3,
                                 max_features=0.5,
                                 random_state=42)
X_train,X_test,y_train, y_test = train_test_split(X, y, random_state=42)
gbi.fit(X_train, y_train)
print("Accuracy on training set: {:.3f}".format(gbi.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(gbi.score(X_test, y_test)))


# In[ ]:


#gradient boasting method

# Storing the prediction
y_pred = gbi.predict_proba(X_test)[:,1]
print('y prediksi',y_pred)


# In[ ]:


#gradient boasting method

# Making the Confusion Matrix
from sklearn.metrics import classification_report, confusion_matrix
cm = confusion_matrix(y_test, y_pred.round())

import seaborn as sns
import matplotlib.pyplot as plt

f, ax = plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot = True, linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("Prediction(Ypred)")
plt.ylabel("Ytrue")
plt.show()

print('TN - True Negative {}'.format(cm[0,0]))
print('FP - False Positive {}'.format(cm[0,1]))
print('FN - False Negative {}'.format(cm[1,0]))
print('TP - True Positive {}'.format(cm[1,1]))
print('Accuracy Rate: {}'.format(np.divide(np.sum([cm[0,0],cm[1,1]]),np.sum(cm))))
print('Misclassification Rate: {}'.format(np.divide(np.sum([cm[0,1],cm[1,0]]),np.sum(cm))))


# In[ ]:


from sklearn.metrics import f1_score
# Plotting the predictions

plt.hist(y_pred,bins=10)
plt.xlim(0,1)
plt.xlabel("Predicted Proababilities")
plt.ylabel("Frequency")

round(roc_auc_score(y_test,y_pred),5)
print('akurasi model gradient bosting :',round(roc_auc_score(y_test,y_pred),5))


# In[ ]:


#gradient boasting

from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
# accuracy_score(y_test, y_pred.round(), normalize=True)
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred.round() ))
print()
print("Classification Report")
print(classification_report(y_test,y_pred.round()))
print('akurasi model gradient bosting :',round(roc_auc_score(y_test,y_pred),5))


# In[ ]:


GB = GradientBoostingClassifier()
GBscore = round(roc_auc_score(y_test,y_pred),5)
print (GBscore)


# In[ ]:


#decision Tree

# Parameter evaluation
treeclf = DecisionTreeClassifier(random_state=42)
parameters = {'max_depth': [6, 7, 8, 9],
              'min_samples_split': [2, 3, 4, 5,6],
              'max_features': [1, 2, 3, 4,5,6]
}
gridsearch=GridSearchCV(treeclf, parameters, cv=100, scoring='roc_auc')
gridsearch.fit(X,y)
print(gridsearch.best_params_)
print(gridsearch.best_score_)


# In[ ]:


#decision Tree

# Adjusting development threshold2
tree = DecisionTreeClassifier(max_depth = 6, 
                              max_features = 4, 
                              min_samples_split = 4, 
                              random_state=42)
X_train,X_test,y_train,y_test = train_test_split(X, y, random_state=42)
tree.fit(X_train, y_train)
print("Accuracy on training set: {:.3f}".format(tree.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(tree.score(X_test, y_test)))


# In[ ]:


#decision Tree

# Predicting the Test set results
y_pred = tree.predict(X_test)
# y_pred.shape
print('y predict', y_pred)


# In[ ]:


#decision Tree

# Making the Confusion Matrix
from sklearn.metrics import classification_report, confusion_matrix
cm = confusion_matrix(y_test, y_pred)

import seaborn as sns
import matplotlib.pyplot as plt

f, ax = plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot = True, linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("Prediction(Ypred)")
plt.ylabel("Ytrue")
plt.show()

print('TN - True Negative {}'.format(cm[0,0]))
print('FP - False Positive {}'.format(cm[0,1]))
print('FN - False Negative {}'.format(cm[1,0]))
print('TP - True Positive {}'.format(cm[1,1]))
print('Accuracy Rate: {}'.format(np.divide(np.sum([cm[0,0],cm[1,1]]),np.sum(cm))))
print('Misclassification Rate: {}'.format(np.divide(np.sum([cm[0,1],cm[1,0]]),np.sum(cm))))


# In[ ]:


#decision Tree

# Plotting the predictions
plt.hist(y_pred,bins=10)
plt.xlim(0,1)
plt.xlabel("Predicted Proababilities")
plt.ylabel("Frequency")

round(roc_auc_score(y_test,y_pred),5)


# In[ ]:


#decision tree
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print()
print("Classification Report")
print(classification_report(y_test, y_pred))
print('akurasi model decision tree :',round(roc_auc_score(y_test,y_pred),5))


# In[ ]:


DS = DecisionTreeClassifier()
DSscore = round(roc_auc_score(y_test,y_pred),5)
print (DSscore)


# In[ ]:


#K-NN model
# Parameter evaluation
knnclf = KNeighborsClassifier()
parameters={'n_neighbors': range(1, 20)}
gridsearch=GridSearchCV(knnclf, parameters, cv=100, scoring='roc_auc')
gridsearch.fit(X, y)
print('grid',gridsearch)


# In[ ]:


# plt.legend()
# plt.savefig('TESTINGS')
print(gridsearch.best_params_)
print(gridsearch.best_score_)


# In[ ]:


#K-NN model
# Fitting K-NN to the Training set
knnClassifier = KNeighborsClassifier(n_neighbors = 18)
knnClassifier.fit(X_train, y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'.format(knnClassifier.score(X_train, y_train)))
print('Accuracy of K-NN classifier on test set: {:.2f}'.format(knnClassifier.score(X_test, y_test)))


# In[ ]:


#K-NN
# Predicting the Test set results
y_pred = knnClassifier.predict(X_test)
print('y predict',y_pred)


# In[ ]:


#K-NN
# Making the Confusion Matrix
from sklearn.metrics import classification_report, confusion_matrix
cm = confusion_matrix(y_test, y_pred)

import seaborn as sns
import matplotlib.pyplot as plt

f, ax = plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot = True, linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("Prediction(Ypred)")
plt.ylabel("Ytrue")
plt.show()

print('TN - True Negative {}'.format(cm[0,0]))
print('FP - False Positive {}'.format(cm[0,1]))
print('FN - False Negative {}'.format(cm[1,0]))
print('TP - True Positive {}'.format(cm[1,1]))
print('Accuracy Rate: {}'.format(np.divide(np.sum([cm[0,0],cm[1,1]]),np.sum(cm))))
print('Misclassification Rate: {}'.format(np.divide(np.sum([cm[0,1],cm[1,0]]),np.sum(cm))))


# In[ ]:


# Plotting the predictions
plt.hist(y_pred,bins=10)
plt.xlim(0,1)
plt.xlabel("Predicted Proababilities")
plt.ylabel("Frequency")

round(roc_auc_score(y_test,y_pred),5)


# In[ ]:


from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print()
print("Classification Report")
print(classification_report(y_test, y_pred))
print('akurasi model K-NN:',round(roc_auc_score(y_test,y_pred),5))


# In[ ]:


KNN = KNeighborsClassifier()
KNNscore = round(roc_auc_score(y_test,y_pred),5)
print (KNNscore)


# In[ ]:


#Logistic Regresion
# Parameter evaluation
logclf = LogisticRegression(random_state=42)
parameters={'C': [1, 4, 10], 'penalty': ['l1', 'l2']}
gridsearch=GridSearchCV(logclf, parameters, cv=100, scoring='roc_auc')
gridsearch.fit(X, y)
print(gridsearch.best_params_)
print(gridsearch.best_score_)


# In[ ]:


#Logistic Regresion

# Adjusting development threshold
logreg_classifier = LogisticRegression(C = 1, penalty = 'l1')
X_train,X_test,y_train, y_test = train_test_split(X, y, random_state=42)
logreg_classifier.fit(X_train, y_train)
print("Training set score: {:.3f}".format(logreg_classifier.score(X_train, y_train)))
print("Test set score: {:.3f}".format(logreg_classifier.score(X_test, y_test)))


# In[ ]:


#Logistic Regresion

# Predicting the Test set results
y_pred = logreg_classifier.predict(X_test)
print('y predict',y_pred)


# In[ ]:


#Logistic Regresion

# Making the Confusion Matrix
from sklearn.metrics import classification_report, confusion_matrix
cm = confusion_matrix(y_test, y_pred)

import seaborn as sns
import matplotlib.pyplot as plt

f, ax = plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot = True, linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("Prediction(Ypred)")
plt.ylabel("Ytrue")
plt.show()

print('TN - True Negative {}'.format(cm[0,0]))
print('FP - False Positive {}'.format(cm[0,1]))
print('FN - False Negative {}'.format(cm[1,0]))
print('TP - True Positive {}'.format(cm[1,1]))
print('Accuracy Rate: {}'.format(np.divide(np.sum([cm[0,0],cm[1,1]]),np.sum(cm))))
print('Misclassification Rate: {}'.format(np.divide(np.sum([cm[0,1],cm[1,0]]),np.sum(cm))))


# In[ ]:


#Logistic Regresion

# Plotting the predictions
plt.hist(y_pred,bins=10)
plt.xlim(0,1)
plt.xlabel("Predicted Proababilities")
plt.ylabel("Frequency")

round(roc_auc_score(y_test,y_pred),5)


# In[ ]:


#Logistic Regresion

from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print()
print("Classification Report")
print(classification_report(y_test, y_pred))
print('akurasi model Logistic Regresion : ',round(roc_auc_score(y_test,y_pred),5))


# In[ ]:


LS = LogisticRegression()
LSscore = round(roc_auc_score(y_test,y_pred),5)
print (LSscore)


# In[ ]:


#Random Forest 

# Parameter evaluation
#evaluasi parameter
rfclf = RandomForestClassifier(random_state=42)
parameters={'n_estimators': [50, 100],
            'max_features': ['auto', 'sqrt', 'log2'],
            'max_depth' : [4,5,6,7],
            'criterion' :['gini', 'entropy']
}
gridsearch=GridSearchCV(rfclf, parameters, cv=50, scoring='roc_auc', n_jobs = -1)
gridsearch.fit(X, y)
print(gridsearch.best_params_)
print(gridsearch.best_score_)


# In[ ]:


#Random Forest 

#acuaration random forest
rf = RandomForestClassifier(n_estimators=100, criterion = 'gini', max_depth = 6, 
                            max_features = 'auto', random_state=0)
rf.fit(X_train, y_train)
print("Accuracy on training set: {:.3f}".format(rf.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(rf.score(X_test, y_test)))


# In[ ]:


#Random Forest 
# Predicting the Test set results
y_pred = rf.predict(X_test)
print('y predict', y_pred)


# In[ ]:


#random Forest

# Making the Confusion Matrix
from sklearn.metrics import classification_report, confusion_matrix
cm = confusion_matrix(y_test, y_pred)

import seaborn as sns
import matplotlib.pyplot as plt

f, ax = plt.subplots(figsize=(5,5))
sns.heatmap(cm,annot = True, linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("Prediction(Ypred)")
plt.ylabel("Ytrue")
plt.show()

print('T - True Negative {}'.format(cm[0,0]))
print('FP - False Positive {}'.format(cm[0,1]))
print('FN - False Negative {}'.format(cm[1,0]))
print('TP - True Positive {}'.format(cm[1,1]))
print('Accuracy Rate: {}'.format(np.divide(np.sum([cm[0,0],cm[1,1]]),np.sum(cm))))
print('Misclassification Rate: {}'.format(np.divide(np.sum([cm[0,1],cm[1,0]]),np.sum(cm))))


# In[ ]:


#Random Forest
# Plotting the predictions
plt.hist(y_pred,bins=10)
plt.xlim(0,1)
plt.xlabel("Predicted Proababilities")
plt.ylabel("Frequency")

round(roc_auc_score(y_test,y_pred),5)


# In[ ]:


from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print()
print("Classification Report")
print(classification_report(y_test, y_pred))
print('akurasi model Random Forest :',round(roc_auc_score(y_test,y_pred),5))


# In[ ]:


RF = RandomForestClassifier()
RFscore = round(roc_auc_score(y_test,y_pred),5)
print (RFscore)


# In[ ]:


# plotly
import plotly
from plotly.offline import init_notebook_mode, iplot
plotly.offline.init_notebook_mode(connected=True)
import plotly.offline as py
import plotly.graph_objs as go
import itertools
plt.style.use('fivethirtyeight')

scores=[GBscore,KNNscore,DSscore,LSscore,RFscore]
AlgorthmsName=["Gradient Boasting","K-NN","Decision Tree","Logistic Regresion","Random Forest"]
#create traces
trace1 = go.Scatter(
    x = AlgorthmsName,
    y= scores,
    name='Algortms Name',
    marker =dict(color='rgba(0,255,0,0.5)',
               line =dict(color='rgb(0,0,0)',width=2)),
                text=AlgorthmsName
)
data = [trace1]
layout = go.Layout(barmode = "group",
                  xaxis= dict(title= 'ML Algorithms',ticklen= 5,zeroline= False),
              yaxis= dict(title= 'Accuracy Scores',ticklen= 5,zeroline= False))
fig = go.Figure(data = data, layout = layout)
iplot(fig)

