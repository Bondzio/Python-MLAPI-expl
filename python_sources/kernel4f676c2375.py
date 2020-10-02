#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import pandas as pd
import seaborn as sns
import statsmodels.tsa.api as smt  
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn import metrics
import requests
import io
get_ipython().run_line_magic('matplotlib', 'inline')


df=pd.read_csv('../input/weatherAUS.csv')
df.shape


# In[ ]:


df.head()


# In[ ]:


total = df.isnull().sum().sort_values(ascending=False)
percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)


# In[ ]:


missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])


# In[ ]:


f, ax = plt.subplots(figsize=(15, 6))
plt.xticks(rotation='90')
sns.barplot(x=missing_data.index, y=missing_data['Percent'])
plt.xlabel('Features', fontsize=15)
plt.ylabel('Percent of missing values', fontsize=15)
plt.title('Percent missing data by feature', fontsize=15)
missing_data


# The above bar graph gives the missing value percentage for each features. so droping 'Sunshine','Evaporation','Cloud3pm','Cloud9am', Date and Location (since it is only for australia so not required).

# In[ ]:


df=df.drop(['Sunshine','Evaporation','Cloud3pm','Cloud9am'],axis=1)


# In[ ]:


df=df.drop(['Date','Location','RISK_MM'],axis=1)


# In[ ]:


df['RainTomorrow']=df['RainTomorrow'].map({'No':0,'Yes':1})


# In[ ]:


df['RainToday']=df['RainToday'].map({'No':0,'Yes':1})


# In[ ]:


df=df.dropna(how='any')  ## also able to fill nan values using mean,median.


# In[ ]:


df['WindDir9am']=df['WindDir9am'].map({'W':0, 'NNW':1, 'SE':2, 'ENE':3, 'SW':4, 'SSE':5, 'S':6, 'NE':7, 'SSW':8, 'N':9, 'WSW':10,
       'ESE':11, 'E':12, 'NW':13, 'WNW':14,
       'NNE':15
})


# In[ ]:


df['WindDir3pm']=df['WindDir3pm'].map({'WNW':0, 'WSW':1, 'E':2, 'NW':3, 'W':4, 'SSE':5, 'ESE':6, 'ENE':7, 'NNW':8, 'SSW':9,
       'SW':10, 'SE':11, 'N':12, 'S':13, 'NNE':14,
        'NE':15})


# In[ ]:


df['WindGustDir']=df['WindGustDir'].map({'W':0, 'WNW':1, 'WSW':2, 'NE':3, 'NNW':4, 'N':5, 'NNE':6, 'SW':7, 'ENE':8, 'SSE':9,
       'S':10, 'NW':11, 'SE':12, 'ESE':13, 
       'E':14, 'SSW':15})


# In[ ]:


df.head()


# In[ ]:


df.isnull().sum()


# BASE MODEL with logistic:

# In[ ]:


y=df['RainTomorrow']
X=df.drop('RainTomorrow',axis=1)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=20)


# In[ ]:


from statsmodels.tools import add_constant as add_constant
df_constant = add_constant(df)
df_constant.head()


# In[ ]:


cols=df_constant.columns[:-1]
model=sm.Logit(df.RainTomorrow,df_constant[cols])
result=model.fit()
result.summary()


# From the above base model it shows the pseudo r square as 0.331, by fadden r square it says that if pseudo r square is between 0.2 to 0.4 it is a good model and also LLR p value is less than 0.05 means the model is significant.

# In[ ]:


df['RainTomorrow'].value_counts(normalize=True)


# Since the target variable is highly imbalance. so balancing of the data is needed by using undersampling,oversampling and SMOTE and check for recall and AUC score.

# Starting with imbalancing and checking the AUC score and after that proceeding with balancing of data.

# In[ ]:


from sklearn.metrics import accuracy_score,roc_curve,roc_auc_score,confusion_matrix,classification_report


# In[ ]:


def imb_predict(algo,xtrain,ytrain,xtest,ytest):
    
    algo.fit(xtrain,ytrain)
    ypred=algo.predict(xtest)
    yprob=algo.predict_proba(xtest)[:,1]
    
    acc=accuracy_score(ytest,ypred)
    print('Accuracy Score: ',acc)
    
    con = confusion_matrix(ytest,ypred)
    print('Confusion matrix: \n',con)
    
    auc=roc_auc_score(ytest,yprob)
    print('AUC: ',auc)
    
    cr=classification_report(ytest,ypred)
    print('Classification report:\n ',cr)
    
    fpr,tpr,thresh=roc_curve(ytest,yprob)
    plt.plot(fpr,tpr,'b--')
    plt.plot(fpr,fpr,'r--')
    plt.show()  


# Logistic Regression

# In[ ]:


from sklearn.linear_model import LogisticRegression
lr=LogisticRegression(solver='liblinear')

imb_predict(lr,X_train,y_train,X_test,y_test)


# K-NN Classifier

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier  
knn = KNeighborsClassifier()
imb_predict(knn,X_train,y_train, X_test,y_test)


# Decision Tree Classifier

# In[ ]:


from sklearn.tree import DecisionTreeClassifier      
dtree=DecisionTreeClassifier(max_depth=5)
imb_predict(dtree,X_train,y_train, X_test,y_test)


# Random Forest Classifier

# In[ ]:


from sklearn.ensemble import RandomForestClassifier 
rf=RandomForestClassifier(n_estimators=20)
imb_predict(rf,X_train,y_train, X_test,y_test)


# Since the data is imbalance Accuracy is not a good metric. So Area under curve is good metric.

# Now performing undersampling

# In[ ]:


Xy_train=pd.concat([X_train,y_train],axis=1)                         ##unsersampling
Xy_train0=Xy_train[Xy_train['RainTomorrow']==0]
Xy_train1=Xy_train[Xy_train['RainTomorrow']==1]
len1=len(Xy_train1)
len0=len(Xy_train0)
Xy_train0_us=Xy_train0.sample(n=len1)
Xy_train_us=pd.concat([Xy_train1,Xy_train0_us],axis=0)

X_train_us=Xy_train_us.drop('RainTomorrow',axis=1)
y_train_us=Xy_train_us['RainTomorrow']


# > Logistic Regression

# In[ ]:


imb_predict(lr,X_train_us,y_train_us, X_test,y_test)


# KNN Classifier

# In[ ]:


imb_predict(knn,X_train_us,y_train_us, X_test,y_test) 


# Decision Tree Classifier

# In[ ]:


imb_predict(dtree,X_train_us,y_train_us, X_test,y_test) 


# Random Forest Classifier

# In[ ]:


imb_predict(rf,X_train_us,y_train_us, X_test,y_test) 


# Over sampling

# In[ ]:


Xy_train=pd.concat([X_train,y_train],axis=1)
Xy_train0=Xy_train[Xy_train['RainTomorrow']==0]                     ##oversampling
Xy_train1=Xy_train[Xy_train['RainTomorrow']==1]
len1=len(Xy_train1)
len0=len(Xy_train0)
Xy_train1_os=Xy_train1.sample(n=len0,replace=True)
Xy_train_os=pd.concat([Xy_train0,Xy_train1_os],axis=0)

X_train_os=Xy_train_os.drop('RainTomorrow',axis=1)
y_train_os=Xy_train_os['RainTomorrow']


# Logistic Regression

# In[ ]:


imb_predict(lr,X_train_os,y_train_os, X_test,y_test)


# KNN Classifier

# In[ ]:


imb_predict(knn,X_train_os,y_train_os, X_test,y_test)


# Decision Tree Classifier

# In[ ]:


imb_predict(dtree,X_train_os,y_train_os, X_test,y_test) 


# Random Forest Classifier

# In[ ]:


imb_predict(rf,X_train_os,y_train_os, X_test,y_test)  


# SMOTE

# In[ ]:


from imblearn.over_sampling import SMOTE
smote=SMOTE(ratio='minority')
X_train_sm,y_train_sm=smote.fit_sample(X_train,y_train)


# Logistic Regression

# In[ ]:


imb_predict(lr,X_train_sm,y_train_sm, X_test,y_test)    


# KNN Classifier

# In[ ]:


imb_predict(knn,X_train_sm,y_train_sm, X_test,y_test) 


# Decision Tree Classifier

# In[ ]:


imb_predict(dtree,X_train_sm,y_train_sm, X_test,y_test)


# Random Forest Classifier

# In[ ]:


imb_predict(rf,X_train_sm,y_train_sm, X_test,y_test) 


# Conclusion: From the above balancing techniques undersampling performs better comparing with recall. From all Logistic regression performs better with AUC score of 0.864.

# In the next version, with different techniques of filling missing values and applying PCA will be done.
