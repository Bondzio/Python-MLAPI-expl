#!/usr/bin/env python
# coding: utf-8

# ## Import DataSet

# In[ ]:


import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib . pyplot as plt
sns.set_style('darkgrid')
flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
sns.set_palette(flatui)
import cufflinks as cf
cf.go_offline()


# In[ ]:


data = pd.read_csv("../input/heart-disease-uci/heart.csv")


# In[ ]:


data.head()


# In[ ]:


data.info()


# In[ ]:


data.nunique()


# In[ ]:


data.dtypes.unique()


# In[ ]:


data.columns


# In[ ]:


data.index


# In[ ]:


sum(data.isnull().sum())


# In[ ]:


data.describe()


# ## EDA 

# In[ ]:


sns.pairplot(data[['age','thalach','trestbps','oldpeak','chol']])


# In[ ]:


plt.figure(figsize=(10,6))
sns.heatmap(data.corr(),annot=True,cmap='viridis')


# observations: from the above chol is poorly correlated to the target variable, which might not be very useful to our prediction.

# In[ ]:


sns.countplot(data['target'])


# In[ ]:


sns.countplot(data['fbs'])


# In[ ]:


sns.barplot(x='slope',y='age',data=data,hue='sex')


# In[ ]:


d = sns.FacetGrid(data=data,col='target',row='cp')
d.map(sns.barplot,'slope','thalach')


# observations: when cp is 0 target is 1 and slop is 2 thalanch has no value same with cp 2 target 0 ,cp 3 and target 0 slope 2 thalanch has no value

# In[ ]:


sns.kdeplot(data['thalach'])


# In[ ]:


sns.kdeplot(data['trestbps'])


# In[ ]:


sns.scatterplot(data['trestbps'],data['thalach'])


# In[ ]:


sns.scatterplot(data['trestbps'],data['age'])


# In[ ]:


sns.boxplot(data['trestbps'])


# In[ ]:


sns.boxplot(data['chol'])


# In[ ]:


IQR = data.trestbps.quantile(0.75) - data.trestbps.quantile(0.25)

Lower_fence = data.trestbps.quantile(0.25) - (IQR * 1.5)
Upper_fence = data.trestbps.quantile(0.75) + (IQR * 1.5)

Upper_fence, Lower_fence, IQR


# In[ ]:


data.query('trestbps >170 or trestbps < 90')


# In[ ]:


IQR = data.chol.quantile(0.75) - data.chol.quantile(0.25)

Lower_fence = data.chol.quantile(0.25) - (IQR * 1.5)
Upper_fence = data.chol.quantile(0.75) + (IQR * 1.5)

Upper_fence, Lower_fence, IQR


# In[ ]:


data.query('chol >369.75 or chol < 115.75')


# In[ ]:


sns.boxplot(x=data['cp'],y = data['thalach'])


# In[ ]:


sns.boxplot(x=data['ca'],y=data['age'])


# ## Model Training

# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X = data.drop('target',axis=1)
y = data['target']


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split( X.values, y.values, test_size=0.2, random_state=42)


# In[ ]:


from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression


# In[ ]:


param = {"C":np.logspace(-3,3,7),"penalty":["l1","l2"]}
logistic =LogisticRegression()


# In[ ]:


model = GridSearchCV(logistic,param,cv=10,refit=True,verbose=3)


# In[ ]:


model.fit(X_train,y_train)


# In[ ]:


y_pred = model.predict(X_test)


# In[ ]:


from sklearn.metrics import classification_report,confusion_matrix


# In[ ]:


print(classification_report(y_test,y_pred))


# In[ ]:


sns.heatmap(confusion_matrix(y_test,y_pred),annot=True,fmt='g')


# ## Evaluators

# In[ ]:


def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
    n_jobs=None, train_sizes=np.linspace(.1, 1.0, 10)):
    """Plots the learning curve of a regression or classfication model using their defualt metrics accuracy or r2_score"""
    plt.figure()
    plt.title(title)
    plt.xlabel("Training Accuracy")
    plt.ylabel("Score")

    train_sizes, train_scores, test_scores = learning_curve(
    estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)

    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.grid()
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
    train_scores_mean + train_scores_std, alpha=0.1,
    color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
    test_scores_mean + test_scores_std, alpha=0.1, color="g")

    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
    label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
    label="Cross-validation score")
    plt.legend(loc="best")
    return plt


# In[ ]:


def Probability_fpr_tpr(estimator,X,y):
    """Returns the false postive rate and true postive rate"""
    probab = estimator.predict_proba(X)[:,1]
    [fpr,tpr,thr] = roc_curve(y, probab)
    return fpr,tpr,thr


def Plot_Roc_Curve(train_fpr,train_tpr,thr1,test_fpr,test_tpr,thr2):
    """Used to plot Roc Curve For Training and Test Set to Check Overfitting in model"""
    plt.figure(figsize=(11,6))
    plt.plot(train_fpr, train_tpr, color = 'coral', label = "Train ROC curve area: "+str(auc(train_fpr, train_tpr)))
    plt.plot(test_fpr, test_tpr, color = 'g', label = "Test ROC curve area: "+str(auc(test_fpr, test_tpr)))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (1 - specificity)', fontsize=12)
    plt.ylabel('True Positive Rate (sensitivty)', fontsize=12)
    plt.title('Receiver operating characteristic (ROC) curve')
    plt.legend(loc="lower right")
    plt.show()
    
    idx = np.min(np.where(train_tpr>0.95))
    print("Train-Set:")
    print("Using a threshold of %.3f " % thr1[idx] + "guarantees a sensitivity of %.3f " % train_tpr[idx]+
    "and a specificity of %.3f" % (1-train_fpr[idx]) +
    ", i.e. a false positive rate of %.2f%%." % (np.array(train_fpr[idx])*100))
    print("Test-Set:")
    idx = np.min(np.where(test_tpr>0.95))
    print("Using a threshold of %.3f " % thr2[idx] + "guarantees a sensitivity of %.3f " % test_tpr[idx]+
    "and a specificity of %.3f" % (1-test_fpr[idx]) +
    ", i.e. a false positive rate of %.2f%%." % (np.array(test_fpr[idx])*100))
    
    print("\n")
    if abs(auc(train_fpr, train_tpr) - auc(test_fpr, test_tpr))*100 > 4.5:
        print("........................................This model is overfitting........................................")
    elif abs(auc(train_fpr, train_tpr) - auc(test_fpr, test_tpr))*100 <= 4.5:
        print("........................................this model is a good fit........................................")
    elif abs(auc(train_fpr, train_tpr) - auc(test_fpr, test_tpr))*100 < 0.1:
        print("........................................this model is Underfitting........................................")    
    else:
        print("unknown fit")


# ### Acuracy Learning Curve

# In[ ]:


from sklearn.metrics import roc_auc_score,roc_curve,auc
from sklearn.model_selection import learning_curve,ShuffleSplit


# In[ ]:


X = data.drop('target',axis=1).values
y = data['target'].values
title = "Learning Curve"
cv = ShuffleSplit(n_splits=100,test_size=0.2,random_state=42)


# In[ ]:


plot_learning_curve(model.best_estimator_,title,X,y,cv=cv)


# ### Roc Curve

# In[ ]:


train_fpr,train_tpr,thr1 = Probability_fpr_tpr(model,X_train,y_train)
test_fpr,test_tpr,thr2 = Probability_fpr_tpr(model,X_test,y_test)


# In[ ]:


Plot_Roc_Curve(train_fpr,train_tpr,thr1,test_fpr,test_tpr,thr2)


# In[ ]:




