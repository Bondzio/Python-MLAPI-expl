#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#data analysis 
import numpy as np
import pandas as pd
import os


# In[ ]:


#plotting
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


#sklearn modeling libraries
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier 
from sklearn.ensemble import GradientBoostingClassifier
from xgboost.sklearn import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier


# In[ ]:


#pre-processing - scaling
from sklearn.preprocessing import StandardScaler as ss
#data splitting
from sklearn.model_selection import train_test_split


# In[ ]:


#dimensionality reduction using decomposition
from sklearn.decomposition import PCA


# In[ ]:


#performance measures
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.metrics import auc, roc_curve


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


#data-set processing and analysing
os.chdir("../input")
#pd.options.display.max_columns = 200
data = pd.read_csv("data.csv")


# In[ ]:


data.shape


# In[ ]:


data.head


# In[ ]:


data.tail


# In[ ]:


#null value checking
data.isnull()


# In[ ]:


data.isnull().sum


# In[ ]:


data.isnull().sum(axis = 1)


# In[ ]:


#total number of null values
data.isnull().values.sum()


# In[ ]:


data.drop(['id', 'Unnamed: 32'], axis=1)


# In[ ]:


data.shape


# In[ ]:


data.columns.values


# In[ ]:


#predictor
X = data.loc[:, 'radius_mean': 'fractal_dimension_worst']


# In[ ]:


X


# In[ ]:


y = data['diagnosis']
di = {'M': 1, 'B': 0}
y = y.map(di)


# In[ ]:


y


# In[ ]:


#scaling
scale = ss()
X = scale.fit_transform(X)
X.shape


# In[ ]:


#pca
pca = PCA()
X_pca = pca.fit_transform(X)
X_pca.shape


# In[ ]:


pca.explained_variance_ratio_


# In[ ]:


pca.explained_variance_ratio_.cumsum()


# In[ ]:


X = X_pca[:,:10] #out 10 values 95% Variance


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size = 0.2,
                                                    shuffle = True
                                                    )


# In[ ]:


X_train.shape


# In[ ]:


X_test.shape


# In[ ]:


#default classifiers
dt = DecisionTreeClassifier()
rf = RandomForestClassifier(n_estimators=100)
xg = XGBClassifier(learning_rate=0.5,
                   reg_alpha= 5,
                   reg_lambda= 0.1
                   )
knn = KNeighborsClassifier()
gbm = GradientBoostingClassifier()
et = ExtraTreesClassifier(n_estimators=100)


# In[ ]:


#train data 
dt1 = dt.fit(X_train,y_train)
rf1 = rf.fit(X_train,y_train)
xg1 = xg.fit(X_train,y_train)
gbm1 = gbm.fit(X_train,y_train)
et1 = et.fit(X_train,y_train)
knn1 = knn.fit(X_train,y_train)


# In[ ]:


#Make predictions
y_pred_dt = dt1.predict(X_test)
y_pred_rf = rf1.predict(X_test)
y_pred_et = et1.predict(X_test)
y_pred_gbm = gbm1.predict(X_test)
y_pred_xg = xg1.predict(X_test)
y_pred_knn = knn1.predict(X_test)


# In[ ]:


#Get probability values
y_pred_dt_prob = dt1.predict_proba(X_test)
y_pred_rf_prob = rf1.predict_proba(X_test)
y_pred_et_prob = et1.predict_proba(X_test)
y_pred_gbm_prob = gbm1.predict_proba(X_test)
y_pred_xg_prob = xg1.predict_proba(X_test)
y_pred_knn_prob = knn1.predict_proba(X_test)


# In[ ]:


#Accuracy Score of Decision Tree Classifier
accuracy_score(y_test,y_pred_dt)


# In[ ]:


#Accuracy Score of Random Forest Classifier
accuracy_score(y_test,y_pred_rf)


# In[ ]:


#Accuracy Score of Extra Trees Classifier
accuracy_score(y_test,y_pred_et)


# In[ ]:


#Accuracy Score of Gradient Boosting Machine Classifier
accuracy_score(y_test,y_pred_gbm)


# In[ ]:


#Accuracy Score of XG Boost Classifier
accuracy_score(y_test,y_pred_xg)


# In[ ]:


#Accuracy Score of KNeighbors Classifier
accuracy_score(y_test,y_pred_knn)


# In[ ]:


#Confusion matrix
confusion_matrix(y_test,y_pred_dt)


# In[ ]:


confusion_matrix(y_test,y_pred_rf)


# In[ ]:


confusion_matrix(y_test,y_pred_et)


# In[ ]:


confusion_matrix(y_test,y_pred_gbm)


# In[ ]:


confusion_matrix(y_test,y_pred_xg)


# In[ ]:


confusion_matrix(y_test,y_pred_knn)


# In[ ]:


# Determine and print the Precision, Recall & F-score values
p_dt,r_dt,f_dt,_ = precision_recall_fscore_support(y_test,y_pred_dt)
print(" Precision, Recall and F-Score values of Decision Tree Classifier are ", p_dt,r_dt,f_dt)
p_rf,r_rf,f_rf,_ = precision_recall_fscore_support(y_test,y_pred_rf)
print(" Precision, Recall and F-Score values of Random Forest Classifier are ", p_rf,r_rf,f_rf)
p_et,r_et,f_et,_ = precision_recall_fscore_support(y_test,y_pred_et)
print(" Precision, Recall and F-Score values of Extra Trees Classifier are ", p_et,r_et,f_et)
p_gbm,r_gbm,f_gbm,_ = precision_recall_fscore_support(y_test,y_pred_gbm)
print(" Precision, Recall and F-Score values of Gradient Boosting Machine Classifier are ", p_gbm,r_gbm,f_gbm)
p_xg,r_xg,f_xg,_ = precision_recall_fscore_support(y_test,y_pred_xg)
print(" Precision, Recall and F-Score values of XG Boost Classifier are ", p_xg,r_xg,f_xg)
p_knn,r_knn,f_knn,_ = precision_recall_fscore_support(y_test,y_pred_knn)
print(" Precision, Recall and F-Score values of KNeighbors Classifier are ", p_knn,r_knn,f_knn)


# In[ ]:


# Plotting Graph

Classifier_models = [(dt, "decisiontree"), (rf, "randomForest"), (et, "extratrees"), (gbm, "gradientboost"), (xg,"xgboost"), (knn,"Kneighbors")]

#  Plotting the ROC curve


fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111)

# Connecting diagonals and specifying Labels,Title

ax.plot([0, 1], [0, 1], ls="--")
ax.set_title('ROC curve for models')
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')


# Setting x,y axes limits

ax.set_xlim([0.0, 1.0])

ax.set_ylim([0.0, 1.0])

AUC = []
for clf,name in Classifier_models:
    clf.fit(X_train,y_train)
    y_pred_prob = clf.predict_proba(X_test)
    fpr, tpr, thresholds = roc_curve(y_test,
                                     y_pred_prob[: , 1],
                                     pos_label= 1
                                     )
    AUC.append((auc(fpr,tpr)))
    ax.plot(fpr, tpr, label = name)

ax.legend(loc="lower right")
plt.show()


# In[ ]:


print("The AUC values for DT Classifier, RF Classifier, ET Classifier, GBM Classifier, XG Boost Classifier, KNeighbors Classifier respectively are :",AUC)


# In[ ]:


print(" Gradient Boost Classifier model has the best performance")


# In[ ]:


print("Observation made from plot : The slower the increase in False Positive Rate from 0, the larger is the Area Under Curve")


# In[ ]:




