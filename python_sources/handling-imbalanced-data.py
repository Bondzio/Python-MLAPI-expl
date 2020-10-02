#!/usr/bin/env python
# coding: utf-8

# ***Please UpVote if you like the work!!!***

# The intention for the below code is just for us to get introduced to the techniques which can be used to handle the imbalanced data.
# 
# In my opinion, handling data to a complete 50 - 50 % is not a very good practice.
# 
# Handling of imbalanced data should only be limited to how this imbalance is represented in our population. If our sample data follows the same imbalance as that of population, then there is no need to handle imbalanced data. The only problem this imbalanced data could have is when our model is highly biased, it could lead us to predicting a biased result.
# 
# If we have build our model which is quite accurate(handled the bias and variace error well), the imbalance will not affect our model prediction.

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


df = pd.read_csv('../input/heart-patients/US_Heart_Patients.csv')
df = df.sample(frac = 1,random_state = 3)


# In[ ]:


df.head()


# In[ ]:


df['TenYearCHD'].value_counts()


# In[ ]:


df['TenYearCHD'].value_counts(normalize = True).plot(kind = 'bar')


# In[ ]:


ms = df.isnull().sum()
ms[ms > 0]


# In[ ]:


df = df.fillna(method = 'ffill')


# In[ ]:


y = df['TenYearCHD']
X = df.drop('TenYearCHD',axis = 1)


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3,random_state = 3)


# In[ ]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(solver='liblinear')


# In[ ]:


from sklearn.metrics import confusion_matrix,roc_auc_score,roc_curve,accuracy_score
def model_eval(algo,Xtrain,ytrain,Xtest,ytest):
    algo.fit(Xtrain,ytrain)
    y_train_ypred = algo.predict(Xtrain)
    y_train_prob = algo.predict_proba(Xtrain)[:,-1]

    print('Confusion matrix - Train : \n',confusion_matrix(ytrain,y_train_ypred))

    print('Overall accuracy : ',accuracy_score(ytrain,y_train_ypred))

    print('AUC - Train : ',roc_auc_score(ytrain,y_train_prob))
    print()

    #### TEST

    y_test_ypred = algo.predict(Xtest)
    y_test_prob = algo.predict_proba(Xtest)[:,-1]

    print('Confusion matrix - Test : \n',confusion_matrix(ytest,y_test_ypred))

    print('Overall accuracy - Test : ',accuracy_score(ytest,y_test_ypred))

    print('AUC - Test : ',roc_auc_score(ytest,y_test_prob))

    fpr,tpr,thresholds = roc_curve(ytest,y_test_prob)

    plt.plot(fpr,tpr)
    plt.plot(fpr,fpr)
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.show()


# In[ ]:


model_eval(lr,X_train,y_train,X_test,y_test)


# ### UNDERSAMPLING MAJORITY CLASS

# In[ ]:


Xy_train = pd.concat([X_train,y_train],axis = 1)

print('Before undersampling : \n',Xy_train['TenYearCHD'].value_counts())
print()

Xy_train_0 = Xy_train[Xy_train['TenYearCHD'] == 0]
Xy_train_1 = Xy_train[Xy_train['TenYearCHD'] == 1]

len_0 = len(Xy_train_0)
len_1 = len(Xy_train_1)

# Undersampling
Xy_train_0_us = Xy_train_0.sample(len_1,random_state = 3)

Xy_train_us = pd.concat([Xy_train_0_us,Xy_train_1])

print('After undersampling : \n',Xy_train_us['TenYearCHD'].value_counts())

y_train_us = Xy_train_us['TenYearCHD']
X_train_us = Xy_train_us.drop('TenYearCHD',axis = 1)


# In[ ]:


model_eval(lr,X_train_us,y_train_us,X_test,y_test)


# ### OVERSAMPLING MINORITY CLASS

# In[ ]:


Xy_train = pd.concat([X_train,y_train],axis = 1)

print('Before oversampling : \n',Xy_train['TenYearCHD'].value_counts())
print()

Xy_train_0 = Xy_train[Xy_train['TenYearCHD'] == 0]
Xy_train_1 = Xy_train[Xy_train['TenYearCHD'] == 1]

len_0 = len(Xy_train_0)
len_1 = len(Xy_train_1)

# OverSampling
Xy_train_1_os = Xy_train_1.sample(len_0,replace = True,random_state = 3)

Xy_train_os = pd.concat([Xy_train_1_os,Xy_train_0])

print('After oversampling : \n',Xy_train_os['TenYearCHD'].value_counts())

y_train_os = Xy_train_os['TenYearCHD']
X_train_os = Xy_train_os.drop('TenYearCHD',axis = 1)


# In[ ]:


model_eval(lr,X_train_os,y_train_os,X_test,y_test)


# In[ ]:


# !pip install imblearn


# ### Using SMOTE (Synthetic Minority Over-sampling Technique)

# In[ ]:


from imblearn.over_sampling import SMOTE
smote = SMOTE(sampling_strategy = 'minority',random_state = 3)

X_train_sm, y_train_sm = smote.fit_sample(X_train,y_train)


# In[ ]:


model_eval(lr,X_train_sm,y_train_sm,X_test,y_test)


# ***Please UpVote if you like the work!!!***
