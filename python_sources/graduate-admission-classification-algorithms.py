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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
import keras
from keras.models import Sequential  
from keras.layers.core import Dense
from xgboost import XGBClassifier

from sklearn.metrics import roc_curve,confusion_matrix,precision_score,recall_score,classification_report

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# Find the Exploratory Analysis and the Regression approach of this dataset [here](https://www.kaggle.com/kenil020/graduate-admission-eda-and-regression/notebook)
# .Now we will look at the Classification approach to the dataset.

# # **Classification**

# Preparing the dataset i.e. Converting the continuous variable Chance of Admit into a discrete variable.

# In[ ]:


dataset = pd.read_csv('../input/Admission_Predict_Ver1.1.csv')
dataset.head()


# Considering the Acceptance Rate of the college is 20%. We would take the Chance of Admit at the 20th percentile as our threshold. Taking 20% because that is what i got when i looked for the college admission rate on google.

# In[ ]:


dataset.sort_values(by = 'Chance of Admit ',ascending = False).head(int(20/100*len(dataset)))[99:]
# 20% is 100 students according to our data.


# So lets say we take our threshold as 0.80 for the dataset.

# In[ ]:


dataset['Admit'] = dataset['Chance of Admit '].apply(lambda x: 1 if x >= 0.80 else 0 )
dataset.head() # Required Dataset


# Let us now remove the columns that are not required and then rename few columns

# In[ ]:


dataset.drop(['Serial No.','Chance of Admit '],axis = 1,inplace = True)
dataset.columns = ['GRE','TOEFL','University Rating','SOP','LOR','CGPA','Research','Admit']
dataset.head()


# Lets dive straight into it with our first classification model.

# Before that we would look at the correlation matrix

# In[ ]:


corr_matrix = dataset.corr()
plt.rcParams['figure.figsize'] = 15,10
sns.heatmap(corr_matrix,annot = True)


# Let us now split the dataset into train and test for our Classification models.

# In[ ]:


X = dataset.iloc[:,:-1].values
Y = dataset.iloc[:,7].values
train_X,test_X,train_Y,test_Y = train_test_split(X,Y,test_size = 0.2,random_state = 27)
test_Y


# Some metrics we will look at to check the accuracy.
# 1. Precision = TP /(TP + FP)
# 2. Recall = TP/(TP + FN)
# 3. Classification Report. Tells us about the Precision, Recall and F1 score.
# 3. Confusion Matrix
# 4. Accuracy of correct prediction = (TP  + TN)/(TP + FP + TN + FN)
# 5. ROC Curve

# ## **Logistic Regression**

# ### ***Training the Model***

# In[ ]:


model_logistic = LogisticRegression(random_state = 0)
model_logistic.fit(train_X,train_Y)


# ### ***Predicting the Outcome***

# In[ ]:


pred_logistic = model_logistic.predict(test_X)


# ### ***Checking for Accuracy***

# In[ ]:


#Precision
print("Precision Score : ",precision_score(test_Y,pred_logistic))

#Recall
print("Recall Score : ",recall_score(test_Y,pred_logistic))

#Confusion Matrix
cm_logistic = confusion_matrix(test_Y,pred_logistic)

#Classification Report
print("Classification Report: ")
print(classification_report(test_Y,pred_logistic))
#Accuracy
print("Accuracy for Test: ",(cm_logistic[0,0] + cm_logistic[1,1])/
      (cm_logistic[0,0] + cm_logistic[1,1] + cm_logistic[0,1] + cm_logistic[1,0]))

plt.rcParams['figure.figsize'] = 10,10
sns.heatmap(cm_logistic,annot = True)
plt.title('Test Dataset')
plt.ylabel('Actual')
plt.xlabel('Predicted')

pred_logistic_train = model_logistic.predict(train_X)
cm = confusion_matrix(train_Y,pred_logistic_train)
print("Accuracy for Train: ",(cm[0,0] + cm[1,1])/(cm[0,0] + cm[1,1] + cm[0,1] + cm[1,0]))

#ROC Curve
plt.figure()
plt.rcParams['figure.figsize'] = 7,7
fpr,tpr,threshold = roc_curve(test_Y,pred_logistic)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.xlabel('FPR',fontsize = 20)
plt.ylabel('TPR',fontsize = 20)
plt.title('ROC Curve',fontsize = 20)
plt.show()


# So we get an accuracy of around 0.91 i.e. we are able to make correct predictions 91 times out of 100.

# ## ***Support Vector Classification - Linear Kernel***

# ### ***Training the model***

# In[ ]:


model_svc_linear = SVC(kernel = 'linear',random_state = 0 , C = 1)
model_svc_linear.fit(train_X,train_Y)


# ### ***Predicting the Outcome***

# In[ ]:


pred_svc_linear = model_svc_linear.predict(test_X)


# ### ***Checking for Accuracy***

# In[ ]:


#Precision
print("Precision Score : ",precision_score(test_Y,pred_svc_linear))

#Recall
print("Recall Score : ",recall_score(test_Y,pred_svc_linear))

#Confusion Matrix
cm_svc_linear = confusion_matrix(test_Y,pred_svc_linear)

#Classification Report
print("Classification Report: ")
print(classification_report(test_Y,pred_svc_linear))
#Accuracy
print("Accuracy for Test: ",(cm_svc_linear[0,0] + cm_svc_linear[1,1])/
      (cm_svc_linear[0,0] + cm_svc_linear[1,1] + cm_svc_linear[0,1] + cm_svc_linear[1,0]))

plt.rcParams['figure.figsize'] = 10,10
sns.heatmap(cm_svc_linear,annot = True)
plt.title('Test Dataset')
plt.ylabel('Actual')
plt.xlabel('Predicted')


pred_svc_linear_train = model_svc_linear.predict(train_X)
cm = confusion_matrix(train_Y,pred_svc_linear_train)
print("Accuracy for Train: ",(cm[0,0] + cm[1,1])/(cm[0,0] + cm[1,1] + cm[0,1] + cm[1,0]))

#ROC Curve
plt.figure()
plt.rcParams['figure.figsize'] = 7,7
fpr,tpr,threshold = roc_curve(test_Y,pred_svc_linear)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.xlabel('FPR',fontsize = 20)
plt.ylabel('TPR',fontsize = 20)
plt.title('ROC Curve',fontsize = 20)
plt.show()


# As we can see we have slightly improved the accuracy as compared to the Logistic Regression Model on both the testing and the training dataset.

# ## ***Support Vector Classification - Gaussian Kernel***

# ### ***Training the Dataset***

# In[ ]:


model_svc_rbf = SVC(kernel = 'rbf',random_state = 0 , C = 100, gamma = 0.01)
model_svc_rbf.fit(train_X,train_Y)


# ### ***Predicting the Outcome***

# In[ ]:


pred_svc_rbf = model_svc_rbf.predict(test_X)


# ### ***Checking the Accuracy***

# In[ ]:


#Precision
print("Precision Score : ",precision_score(test_Y,pred_svc_rbf))

#Recall
print("Recall Score : ",recall_score(test_Y,pred_svc_rbf))

#Confusion Matrix
cm_svc_rbf = confusion_matrix(test_Y,pred_svc_rbf)

#Classification Report
print("Classification Report: ")
print(classification_report(test_Y,pred_svc_rbf))
#Accuracy
print("Accuracy for Test: ",(cm_svc_rbf[0,0] + cm_svc_rbf[1,1])/
      (cm_svc_rbf[0,0] + cm_svc_rbf[1,1] + cm_svc_rbf[0,1] + cm_svc_rbf[1,0]))

plt.rcParams['figure.figsize'] = 10,10
sns.heatmap(cm,annot = True)
plt.title('Test Dataset')
plt.ylabel('Actual')
plt.xlabel('Predicted')


pred_svc_rbf_train = model_svc_rbf.predict(train_X)
cm = confusion_matrix(train_Y,pred_svc_rbf_train)
print("Accuracy for Train: ",(cm[0,0] + cm[1,1])/(cm[0,0] + cm[1,1] + cm[0,1] + cm[1,0]))

#ROC Curve
plt.figure()
plt.rcParams['figure.figsize'] = 7,7
fpr,tpr,threshold = roc_curve(test_Y,pred_svc_rbf)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.xlabel('FPR',fontsize = 20)
plt.ylabel('TPR',fontsize = 20)
plt.title('ROC Curve',fontsize = 20)
plt.show()


# As you can see we have almost narrowed it down on the 100% accuracy for the dataset.

# ## ***Decision Tree Classification***

# ### ***Training the Dataset***
# 

# In[ ]:


model_dtree = DecisionTreeClassifier(criterion = 'entropy',random_state = 0,max_features = 5,max_depth = 11
                                    ,min_samples_split = 5)
model_dtree.fit(train_X,train_Y)


# ### ***Predicing the Outcome***

# In[ ]:


pred_dtree = model_dtree.predict(test_X)


# ### ***Checking for Accuracy***

# In[ ]:


#Precision
print("Precision Score : ",precision_score(test_Y,pred_dtree))

#Recall
print("Recall Score : ",recall_score(test_Y,pred_dtree))

#Confusion Matrix
cm_dtree = confusion_matrix(test_Y,pred_dtree)

#Classification Report
print("Classification Report: ")
print(classification_report(test_Y,pred_dtree))
#Accuracy
print("Accuracy for Test: ",(cm_dtree[0,0] + cm_dtree[1,1])/
      (cm_dtree[0,0] + cm_dtree[1,1] + cm_dtree[0,1] + cm_dtree[1,0]))

plt.rcParams['figure.figsize'] = 10,10
sns.heatmap(cm_dtree,annot = True)
plt.title('Test Dataset')
plt.ylabel('Actual')
plt.xlabel('Predicted')

pred_dtree_train = model_dtree.predict(train_X)
cm = confusion_matrix(train_Y,pred_dtree_train)
print("Accuracy for Train: ",(cm[0,0] + cm[1,1])/(cm[0,0] + cm[1,1] + cm[0,1] + cm[1,0]))

#ROC Curve
plt.figure()
plt.rcParams['figure.figsize'] = 7,7
fpr,tpr,threshold = roc_curve(test_Y,pred_dtree)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.xlabel('FPR',fontsize = 20)
plt.ylabel('TPR',fontsize = 20)
plt.title('ROC Curve',fontsize = 20)
plt.show()


# We can see that the Accuracy for train and test are nearby, but the difference might suggest that we are overfitting the dataset.

# ## **Random Forest Classification**

# ### ***Training the Dataset***

# In[ ]:


model_rforest = RandomForestClassifier(n_estimators = 500,random_state = 0,max_depth = 5
                                      ,max_features = 5,min_samples_split = 10, 
                                       criterion = 'entropy')
model_rforest.fit(train_X,train_Y)


# ### ***Predicting the Outcome***

# In[ ]:


pred_rforest = model_rforest.predict(test_X)


# ### ***Checking for Accuracy***

# In[ ]:


#Precision
print("Precision Score : ",precision_score(test_Y,pred_rforest))

#Recall
print("Recall Score : ",recall_score(test_Y,pred_rforest))

#Confusion Matrix
cm_rforest = confusion_matrix(test_Y,pred_rforest)

#Classification Report
print("Classification Report: ")
print(classification_report(test_Y,pred_rforest))
#Accuracy
print("Accuracy for Test: ",(cm_rforest[0,0] + cm_rforest[1,1])/
      (cm_rforest[0,0] + cm_rforest[1,1] + cm_rforest[0,1] + cm_rforest[1,0]))

plt.rcParams['figure.figsize'] = 10,10
sns.heatmap(cm_rforest,annot = True)
plt.title('Test Dataset')
plt.ylabel('Actual')
plt.xlabel('Predicted')

pred_rforest_train = model_rforest.predict(train_X)
cm = confusion_matrix(train_Y,pred_rforest_train)
print("Accuracy for Train: ",(cm[0,0] + cm[1,1])/(cm[0,0] + cm[1,1] + cm[0,1] + cm[1,0]))

#ROC Curve
plt.figure()
plt.rcParams['figure.figsize'] = 7,7
fpr,tpr,threshold = roc_curve(test_Y,pred_rforest)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.xlabel('FPR',fontsize = 20)
plt.ylabel('TPR',fontsize = 20)
plt.title('ROC Curve',fontsize = 20)
plt.show()


# ## **Naive Bayes Classifier**

# ### ***Training the Dataset***

# In[ ]:


model_nb = GaussianNB()
model_nb.fit(train_X,train_Y)


# ### ***Predicting the Outcomes***

# In[ ]:


pred_nb = model_nb.predict(test_X)


# ### ***Checking for Accuracy***

# In[ ]:


#Precision
print("Precision Score : ",precision_score(test_Y,pred_nb))

#Recall
print("Recall Score : ",recall_score(test_Y,pred_nb))

#Confusion Matrix
cm_nb = confusion_matrix(test_Y,pred_nb)

#Classification Report
print("Classification Report: ")
print(classification_report(test_Y,pred_nb))
#Accuracy
print("Accuracy for Test: ",(cm_nb[0,0] + cm_nb[1,1])/
      (cm_nb[0,0] + cm_nb[1,1] + cm_nb[0,1] + cm_nb[1,0]))

plt.rcParams['figure.figsize'] = 7,7
sns.heatmap(cm_nb,annot = True)
plt.title('Test Dataset')
plt.ylabel('Actual')
plt.xlabel('Predicted')

pred_nb_train = model_nb.predict(train_X)
cm = confusion_matrix(train_Y,pred_nb_train)
print("Accuracy for Train: ",(cm[0,0] + cm[1,1])/(cm[0,0] + cm[1,1] + cm[0,1] + cm[1,0]))

#ROC Curve
plt.figure()
plt.rcParams['figure.figsize'] = 10,10
fpr,tpr,threshold = roc_curve(test_Y,pred_nb)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.xlabel('FPR',fontsize = 20)
plt.ylabel('TPR',fontsize = 20)
plt.title('ROC Curve',fontsize = 20)
plt.show()


# ## **K Nearest Neighbors**

# ### ***Training the Dataset***

# In[ ]:


model_knn = KNeighborsClassifier(n_neighbors= 5,metric = 'minkowski',p = 2)
model_knn.fit(train_X,train_Y)


# ### ***Predicting the Outcome***

# In[ ]:


pred_knn = model_knn.predict(test_X)


# ### ***Checking for Accuracy***

# In[ ]:


#Precision
print("Precision Score : ",precision_score(test_Y,pred_knn))

#Recall
print("Recall Score : ",recall_score(test_Y,pred_knn))

#Confusion Matrix
cm_knn = confusion_matrix(test_Y,pred_knn)

#Classification Report
print("Classification Report: ")
print(classification_report(test_Y,pred_knn))
#Accuracy
print("Accuracy for Test: ",(cm_knn[0,0] + cm_knn[1,1])/
      (cm_knn[0,0] + cm_knn[1,1] + cm_knn[0,1] + cm_knn[1,0]))

plt.rcParams['figure.figsize'] = 7,7
sns.heatmap(cm_knn,annot = True)
plt.title('Test Dataset')
plt.ylabel('Actual')
plt.xlabel('Predicted')

pred_knn_train = model_nb.predict(train_X)
cm = confusion_matrix(train_Y,pred_knn_train)
print("Accuracy for Train: ",(cm[0,0] + cm[1,1])/(cm[0,0] + cm[1,1] + cm[0,1] + cm[1,0]))

#ROC Curve
plt.figure()
plt.rcParams['figure.figsize'] = 10,10
fpr,tpr,threshold = roc_curve(test_Y,pred_knn)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.xlabel('FPR',fontsize = 20)
plt.ylabel('TPR',fontsize = 20)
plt.title('ROC Curve',fontsize = 20)
plt.show()


# ## **Principal Component Classification**

# ### ***Finding the Principal Component***

# In[ ]:


pca = PCA(n_components = None)
train_X_pca = pca.fit_transform(train_X)
test_X_pca = pca.fit(test_X)
explained_variance = pca.explained_variance_ratio_


# In[ ]:


for x in explained_variance:
    print(round(x,2))


# As we can the variance explained by the first two components is enough and the other components can be ignored. Now using this components to create the new logistic regression model

# ### ***Training the Dataset***

# In[ ]:


pca = PCA(n_components = 2)
train_X_pca = pca.fit_transform(train_X)
test_X_pca = pca.transform(test_X)
model_pca = LogisticRegression()
model_pca.fit(train_X_pca,train_Y)


# ### ***Predicting the Outcome***

# In[ ]:


pred_pca = model_pca.predict(test_X_pca)


# ### ***Checking the Accuracy***

# In[ ]:


#Precision
print("Precision Score : ",precision_score(test_Y,pred_pca))

#Recall
print("Recall Score : ",recall_score(test_Y,pred_pca))

#Confusion Matrix
cm_pca = confusion_matrix(test_Y,pred_pca)

#Classification Report
print("Classification Report: ")
print(classification_report(test_Y,pred_pca))
#Accuracy
print("Accuracy for Test: ",(cm_pca[0,0] + cm_pca[1,1])/
      (cm_pca[0,0] + cm_pca[1,1] + cm_pca[0,1] + cm_pca[1,0]))

plt.rcParams['figure.figsize'] = 10,10
sns.heatmap(cm_pca,annot = True)
plt.title('Test Dataset')
plt.ylabel('Actual')
plt.xlabel('Predicted')

pred_pca_train = model_pca.predict(train_X_pca)
cm = confusion_matrix(train_Y,pred_pca_train)
print("Accuracy for Train: ",(cm[0,0] + cm[1,1])/(cm[0,0] + cm[1,1] + cm[0,1] + cm[1,0]))

#ROC Curve
plt.figure()
plt.rcParams['figure.figsize'] = 7,7
fpr,tpr,threshold = roc_curve(test_Y,pred_pca)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.xlabel('FPR',fontsize = 20)
plt.ylabel('TPR',fontsize = 20)
plt.title('ROC Curve',fontsize = 20)
plt.show()


# Though most of the variance is explained by first two parameters, we see that the model does not give great output on the test dataset.

# ## **Artifical Neural Network**

# ### ***Training the Dataset***

# In[ ]:


model_ann = Sequential()
# Input Layer and First Hidden Layer
model_ann.add(Dense(output_dim = 6,init = 'uniform',activation = 'relu',input_dim = 7))

#Second Hidden Layer
model_ann.add(Dense(output_dim = 6,init = 'uniform',activation = 'relu'))

#Final Layer
model_ann.add(Dense(output_dim = 1,init = 'uniform',activation = 'sigmoid'))

#Compiling ANN
model_ann.compile(optimizer = 'adam', loss = 'binary_crossentropy',metrics = ['accuracy'])

model_ann.fit(train_X,train_Y,batch_size = 5,nb_epoch = 100)


# ### ***Predicting the Outcome***

# In[ ]:


pred_ann = model_ann.predict(test_X)
pred_ann = (pred_ann > 0.5)


# ### ***Checking for Accuracy***

# In[ ]:


#Precision
print("Precision Score : ",precision_score(test_Y,pred_ann))

#Recall
print("Recall Score : ",recall_score(test_Y,pred_ann))

#Confusion Matrix
cm_ann = confusion_matrix(test_Y,pred_ann)

#Classification Report
print("Classification Report: ")
print(classification_report(test_Y,pred_ann))
#Accuracy
print("Accuracy for Test: ",(cm_ann[0,0] + cm_ann[1,1])/
      (cm_ann[0,0] + cm_ann[1,1] + cm_ann[0,1] + cm_ann[1,0]))

plt.rcParams['figure.figsize'] = 10,10
sns.heatmap(cm_ann,annot = True)
plt.title('Test Dataset')
plt.ylabel('Actual')
plt.xlabel('Predicted')

pred_ann_train = model_ann.predict(train_X)
cm = confusion_matrix(train_Y,pred_ann_train > 0.5)
print("Accuracy for Train: ",(cm[0,0] + cm[1,1])/(cm[0,0] + cm[1,1] + cm[0,1] + cm[1,0]))

#ROC Curve
plt.figure()
plt.rcParams['figure.figsize'] = 7,7
fpr,tpr,threshold = roc_curve(test_Y,pred_ann)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.xlabel('FPR',fontsize = 20)
plt.ylabel('TPR',fontsize = 20)
plt.title('ROC Curve',fontsize = 20)
plt.show()


# ## **XGBoost Classifier**

# ### ***Training the Dataset***

# In[ ]:


model_xgb = XGBClassifier(max_depth = 5,learning_rate = 0.05,n_estimators = 500,nthread = -1)
model_xgb.fit(train_X,train_Y)


# ### ***Predicting the Outcome***

# In[ ]:


pred_xgb = model_xgb.predict(test_X)


# ### ***Checking for Accuracy***

# In[ ]:


#Precision
print("Precision Score : ",precision_score(test_Y,pred_xgb))

#Recall
print("Recall Score : ",recall_score(test_Y,pred_xgb))

#Confusion Matrix
cm_xgb = confusion_matrix(test_Y,pred_xgb)

#Classification Report
print("Classification Report: ")
print(classification_report(test_Y,pred_xgb))
#Accuracy
print("Accuracy for Test: ",(cm_xgb[0,0] + cm_xgb[1,1])/
      (cm_xgb[0,0] + cm_xgb[1,1] + cm_xgb[0,1] + cm_xgb[1,0]))

plt.rcParams['figure.figsize'] = 10,10
sns.heatmap(cm_xgb,annot = True)
plt.title('Test Dataset')
plt.ylabel('Actual')
plt.xlabel('Predicted')

pred_xgb_train = model_xgb.predict(train_X)
cm = confusion_matrix(train_Y,pred_xgb_train > 0.5)
print("Accuracy for Train: ",(cm[0,0] + cm[1,1])/(cm[0,0] + cm[1,1] + cm[0,1] + cm[1,0]))

#ROC Curve
plt.figure()
plt.rcParams['figure.figsize'] = 7,7
fpr,tpr,threshold = roc_curve(test_Y,pred_xgb)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr, tpr, marker='.')
plt.xlabel('FPR',fontsize = 20)
plt.ylabel('TPR',fontsize = 20)
plt.title('ROC Curve',fontsize = 20)
plt.show()


# This sums up all the model that i wanted to train. Now lets look at thei performance
# 

# In[ ]:


index = ['LogisticRegression','SupportVectorClassifier(Linear)','SupportVectorClassifier(Gaussian)',
        'DecisionTree','RandomForest','PrincipalComponent','NaiveBayes','KNearestNeighbors',
        'AritficialNeuralNetwork','XGBoost']

data = [[precision_score(test_Y,pred_logistic),recall_score(test_Y,pred_logistic),
         (cm_logistic[0,0] + cm_logistic[1,1])/(cm_logistic[0,0]+cm_logistic[0,1]+cm_logistic[1,0]+cm_logistic[1,1])],
        [precision_score(test_Y,pred_svc_linear),recall_score(test_Y,pred_svc_linear),
         (cm_svc_linear[0,0] + cm_svc_linear[1,1])/(cm_svc_linear[0,0]+cm_svc_linear[0,1]+cm_svc_linear[1,0]+cm_svc_linear[1,1])],
        [precision_score(test_Y,pred_svc_rbf),recall_score(test_Y,pred_svc_rbf),
         (cm_svc_rbf[0,0] + cm_svc_rbf[1,1])/(cm_svc_rbf[0,0]+cm_svc_rbf[0,1]+cm_svc_rbf[1,0]+cm_svc_rbf[1,1])],
        [precision_score(test_Y,pred_dtree),recall_score(test_Y,pred_dtree),
         (cm_dtree[0,0] + cm_dtree[1,1])/(cm_dtree[0,0]+cm_dtree[0,1]+cm_dtree[1,0]+cm_dtree[1,1])],
        [precision_score(test_Y,pred_rforest),recall_score(test_Y,pred_rforest),
         (cm_rforest[0,0] + cm_rforest[1,1])/(cm_rforest[0,0]+cm_rforest[0,1]+cm_rforest[1,0]+cm_rforest[1,1])],
        [precision_score(test_Y,pred_pca),recall_score(test_Y,pred_pca),
         (cm_pca[0,0] + cm_pca[1,1])/(cm_pca[0,0]+cm_pca[0,1]+cm_pca[1,0]+cm_pca[1,1])],
        [precision_score(test_Y,pred_nb),recall_score(test_Y,pred_nb),
         (cm_nb[0,0] + cm_nb[1,1])/(cm_nb[0,0]+cm_nb[0,1]+cm_nb[1,0]+cm_nb[1,1])],
        [precision_score(test_Y,pred_knn),recall_score(test_Y,pred_knn),
         (cm_knn[0,0] + cm_knn[1,1])/(cm_knn[0,0]+cm_knn[0,1]+cm_knn[1,0]+cm_knn[1,1])],
        [precision_score(test_Y,pred_ann),recall_score(test_Y,pred_ann),
         (cm_ann[0,0] + cm_ann[1,1])/(cm_ann[0,0]+cm_ann[0,1]+cm_ann[1,0]+cm_ann[1,1])],
        [precision_score(test_Y,pred_xgb),recall_score(test_Y,pred_xgb),
         (cm_xgb[0,0] + cm_xgb[1,1])/(cm_xgb[0,0]+cm_xgb[0,1]+cm_xgb[1,0]+cm_xgb[1,1])]]

accuracy = pd.DataFrame(data = data,index = index,columns = ['Precision','Recall','Accuracy'])
accuracy.sort_values(by = ['Accuracy','Precision','Recall'],ascending = False)

