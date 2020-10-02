#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


import os
os.listdir("../input")


# In[ ]:


train=pd.read_csv("../input/train1/train1.csv")


# In[ ]:


test = pd.read_csv("../input/test-1/test1.csv")


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


train.sample()


# In[ ]:


train.describe()


# In[ ]:


test.describe()


# In[ ]:


train_original = train.copy()
test_original = test.copy()


# In[ ]:


train.columns


# In[ ]:


test.columns


# In[ ]:


train.dtypes


# In[ ]:


train.shape ,  test.shape


# In[ ]:


dataset = pd.concat([train,test])


# In[ ]:


dataset.shape


# In[ ]:


train['Loan_Status'].value_counts()


# In[ ]:


train['Loan_Status'].value_counts().plot.bar(title = 'Loan_Status')


# In[ ]:


train['Gender'].value_counts()


# In[ ]:


train['Gender'].value_counts(normalize ='True').plot.bar(title = 'Gender')


# In[ ]:


train['Married'].value_counts(normalize ='True').plot.bar(title = 'Married')


# In[ ]:


train['Dependents'].value_counts().plot.bar(title = 'Dependents')


# In[ ]:


train['Property_Area'].value_counts(normalize=True).plot.bar(title='Property_Area')


# In[ ]:


sns.distplot(train['ApplicantIncome'])


# In[ ]:


plt.figure(1)
plt.subplot(121)
sns.distplot(train['CoapplicantIncome'])

plt.subplot(122)
train['CoapplicantIncome'].plot.box(figsize=(16,5))

plt.show()


# In[ ]:


train.boxplot(column='ApplicantIncome', 
              by = 'Education')


# In[ ]:


train.isnull().sum()


# In[ ]:


train['LoanAmount'].fillna(train['LoanAmount'].mean(), inplace=True)
train['Self_Employed'].fillna('No',inplace=True)
train['Gender'].fillna(train['Gender'].mode()[0], inplace=True)
train['Married'].fillna(train['Married'].mode()[0], inplace=True)
train['Dependents'].fillna(train['Dependents'].mode()[0], inplace=True)
train['Loan_Amount_Term'].fillna(train['Loan_Amount_Term'].mode()[0], inplace=True)
train['Credit_History'].fillna(train['Credit_History'].mode()[0], inplace=True)  


# In[ ]:


train['income'] = train['ApplicantIncome'] + train['CoapplicantIncome']
train.drop(['ApplicantIncome','CoapplicantIncome'],axis =1,inplace = True)


# In[ ]:


from sklearn.preprocessing import LabelEncoder
var_mod = ['Gender','Married','Dependents','Education','Self_Employed','Property_Area','Loan_Status']
le = LabelEncoder()
for i in var_mod:
    train[i] = le.fit_transform(train[i])
train.dtypes 


# In[ ]:


train.head()


# In[ ]:


train['Loan_Amount_Term'].value_counts()


# In[ ]:


train['Loan_Amount_Term'].fillna(train['Loan_Amount_Term'].mode()[0],inplace=True)


# In[ ]:


train['LoanAmount'].fillna(train['LoanAmount'].median(),inplace=True)


# In[ ]:


train.isnull().sum()


# In[ ]:


Credit_History=pd.crosstab(train['Credit_History'],train['Loan_Status'])
Property_Area=pd.crosstab(train['Property_Area'],train['Loan_Status'])
my_colors = 'ygbkymc'  #yellow, green, blue, black
Credit_History.div(Credit_History.sum(1).astype(float), axis=0).plot(kind="bar",color=my_colors, stacked=True, figsize=(4,4))
plt.show()

Property_Area.div(Property_Area.sum(1).astype(float), axis=0).plot(kind="bar",color=my_colors, stacked=True)
plt.show()


# In[ ]:


test.isnull().sum()


# In[ ]:


test['LoanAmount'].fillna(test['LoanAmount'].median(), inplace=True)
test['Self_Employed'].fillna(test['Self_Employed'].mode()[0], inplace=True)
test['Gender'].fillna(test['Gender'].mode()[0], inplace=True)
test['Dependents'].fillna(test['Dependents'].mode()[0], inplace=True)
test['Loan_Amount_Term'].fillna(test['Loan_Amount_Term'].mode()[0], inplace=True)
test['Credit_History'].fillna(test['Credit_History'].mode()[0], inplace=True)  


# In[ ]:


test['income'] = test['ApplicantIncome'] + test['CoapplicantIncome']
test.drop(['ApplicantIncome','CoapplicantIncome'],axis =1,inplace = True)


# In[ ]:


from sklearn.preprocessing import LabelEncoder
var_mod = ['Gender','Married','Dependents','Education','Self_Employed','Property_Area']
le = LabelEncoder()
for i in var_mod:
    test[i] = le.fit_transform(test[i])
test.dtypes  


# In[ ]:


test.head()


# In[ ]:


train['LoanAmount_log'] = np.log(train['LoanAmount'])
train['LoanAmount_log'].hist(bins=20)
test['LoanAmount_log'] = np.log(test['LoanAmount'])


# In[ ]:


matrix = train.corr()
f, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(matrix, vmax=.8, square=True, cmap="Greens");


# In[ ]:


train=train.drop('Loan_ID', axis =1)


# In[ ]:


X = train.drop('Loan_Status',1)
y = train.Loan_Status


# In[ ]:


test=test.drop('Loan_ID', axis =1)


# In[ ]:


import warnings
warnings.filterwarnings('ignore')


# In[ ]:


from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


# In[ ]:


from sklearn.metrics import accuracy_score


# In[ ]:


x_train, x_cv, y_train, y_cv = train_test_split(X,y, test_size =0.3)


# In[ ]:


model = LogisticRegression()
model.fit(x_train, y_train)


# In[ ]:


pred_cv = model.predict(x_cv)


# In[ ]:


accuracy_score(y_cv,pred_cv)


# In[ ]:


pred_test = model.predict(test)


# In[ ]:


submission=pd.read_csv("../input/submission/Submission.csv")


# In[ ]:


submission['Loan_Status']=pred_test
submission['Loan_ID']=test_original['Loan_ID']


# In[ ]:


submission['Loan_Status'].replace(0, 'N',inplace=True)
submission['Loan_Status'].replace(1, 'Y',inplace=True)


# In[ ]:


from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


# In[ ]:


i=1
kf =KFold(n_splits=3, shuffle=True, random_state=0)
for train_index,test_index in kf.split(X,y):
    print('\n{} of kfold {}'.format(i,kf.n_splits))
    xtr,xvl = X.loc[train_index],X.loc[test_index]
    ytr,yvl = y[train_index],y[test_index]
    model = LogisticRegression(random_state=1)
    model.fit(xtr, ytr)
    pred_test = model.predict(xvl)
    score = accuracy_score(yvl,pred_test)
    print('accuracy_score',score)
    i+=1
pred_test = model.predict(test)
pred=model.predict_proba(xvl)[:,1]


# In[ ]:


submission['Loan_Status']=pred_test
submission['Loan_ID']=test_original['Loan_ID']


# In[ ]:


submission['Loan_Status'].replace(0, 'N',inplace=True)
submission['Loan_Status'].replace(1, 'Y',inplace=True)


# In[ ]:


pd.DataFrame(submission, columns=['Loan_ID','Loan_Status']).to_csv('Logistic.csv')


# In[ ]:


from sklearn import tree


# In[ ]:


i=1
kf = KFold(n_splits=3,random_state=1,shuffle=True)
for train_index,test_index in kf.split(X,y):
    print('\n{} of kfold {}'.format(i,kf.n_splits))
    xtr,xvl = X.loc[train_index],X.loc[test_index]
    ytr,yvl = y[train_index],y[test_index]
    
    model = tree.DecisionTreeClassifier(random_state=1)
    model.fit(xtr, ytr)
    pred_test = model.predict(xvl)
    score = accuracy_score(yvl,pred_test)
    print('accuracy_score',score)
    i+=1
pred_test = model.predict(test)


# In[ ]:


submission['Loan_Status']=pred_test            # filling Loan_Status with predictions
submission['Loan_ID']=test_original['Loan_ID'] # filling Loan_ID with test Loan_ID


# In[ ]:


# replacing 0 and 1 with N and Y
submission['Loan_Status'].replace(0, 'N',inplace=True)
submission['Loan_Status'].replace(1, 'Y',inplace=True)


# In[ ]:


# Converting submission file to .csv format
pd.DataFrame(submission, columns=['Loan_ID','Loan_Status']).to_csv('Decision Tree.csv')


# In[ ]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


i=1
kf = KFold(n_splits=3,random_state=1,shuffle=True)
for train_index,test_index in kf.split(X,y):
    print('\n{} of kfold {}'.format(i,kf.n_splits))
    xtr,xvl = X.loc[train_index],X.loc[test_index]
    ytr,yvl = y[train_index],y[test_index]
    
    model = RandomForestClassifier(random_state=1, max_depth=10)
    model.fit(xtr, ytr)
    pred_test = model.predict(xvl)
    score = accuracy_score(yvl,pred_test)
    print('accuracy_score',score)
    i+=1
pred_test = model.predict(test)


# In[ ]:


abc=[]
classifiers=['Linear Svm','Radial Svm','Logistic Regression','KNN','Decision Tree']
models=[svm.SVC(kernel='linear'),svm.SVC(kernel='rbf'),LogisticRegression(),KNeighborsClassifier(n_neighbors=3),DecisionTreeClassifier()]
for i in models:
    model = i
    model.fit(x_train,y_train)
    prediction=model.predict(x_cv)
    abc.append(metrics.accuracy_score(prediction,y_cv))
models_dataframe=pd.DataFrame(abc,index=classifiers)   
models_dataframe.columns=['Accuracy']
models_dataframe


# In[ ]:


importances=pd.Series(model.feature_importances_, index=X.columns)
importances.plot(kind='barh', figsize=(12,8))


# In[ ]:




