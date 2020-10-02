#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


train_dataset=pd.read_csv("/kaggle/input/titanic/train.csv")


# In[ ]:


sns.heatmap(train_dataset.isnull(),cmap="viridis")


# In[ ]:


len(train_dataset[train_dataset['Cabin'].isnull()])/len(train_dataset['Cabin'])


# In[ ]:


# 77.1% of data missing
# lets drop this column
train_dataset.drop("Cabin",axis=1,inplace=True)


# In[ ]:


len(train_dataset[train_dataset['Age'].isnull()])/len(train_dataset['Age'])


# In[ ]:


train_dataset.head()


# In[ ]:


train_dataset.drop(['Ticket','PassengerId','Name'],axis=1,inplace=True)


# In[ ]:


train_dataset.isna().sum()


# In[ ]:


sns.barplot(x=train_dataset['Pclass'], y=train_dataset['Age'], palette="deep")


# In[ ]:


sns.barplot(x=train_dataset['Pclass'], y=train_dataset['Age'], palette="deep")


# In[ ]:


print(train_dataset[train_dataset['Pclass']==3]["Age"].mean())
print(train_dataset[train_dataset['Pclass']==2]["Age"].mean())
print(train_dataset[train_dataset['Pclass']==1]["Age"].mean())


# In[ ]:


def compute_age(cols):
    Age=cols[0]
    Pclass=cols[1]
    if pd.isnull(Age)==False:
        return Age
    elif Pclass==3:
        return 25.1406
    elif Pclass==2:
        return 29.8776
    else:
        return 38.23344


# In[ ]:


train_dataset["Age"]=train_dataset[['Age','Pclass']].apply(compute_age,axis=1)


# In[ ]:


sns.countplot(x='Embarked',data=train_dataset)


# In[ ]:


def setEmbakedC(col):
    emb=col[0]
    if pd.isnull(emb):
        return 'S'
    return emb

train_dataset['Embarked']=train_dataset[['Embarked']].apply(setEmbakedC,axis=1)


# In[ ]:


train_dataset.isna().sum()


# In[ ]:


sex=pd.get_dummies(train_dataset['Sex'],drop_first=True)
embark=pd.get_dummies(train_dataset['Embarked'],drop_first=True)
train_dataset=pd.concat([train_dataset,sex,embark],axis=1)
train_dataset.head()


# In[ ]:


train_dataset.drop(['Sex','Embarked'],axis=1,inplace=True)


# In[ ]:


train_dataset.head()


# In[ ]:


train_dataset[train_dataset['FamilySize']==train_dataset['FamilySize'].max()]


# In[ ]:


train_dataset['FamilySize']=train_dataset['SibSp']+train_dataset['Parch']


# In[ ]:


train_dataset.drop(['SibSp','Parch'],axis=1,inplace=True)


# In[ ]:


train_dataset['Fare']=(train_dataset['Fare']-train_dataset['Fare'].mean())/train_dataset['Fare'].std()


# In[ ]:


train_dataset['Age']=(train_dataset['Age']-train_dataset['Age'].mean())/train_dataset['Age'].std()
#train_dataset['Parch']=(train_dataset['Parch']-train_dataset['Parch'].mean())/train_dataset['Parch'].std()
train_dataset['Pclass']=(train_dataset['Pclass']-train_dataset['Pclass'].mean())/train_dataset['Pclass'].std()
#train_dataset['SibSp']=(train_dataset['SibSp']-train_dataset['SibSp'].mean())/train_dataset['SibSp'].std()


# In[ ]:


train_dataset.head()


# In[ ]:


train_dataset['FamilySize']=(train_dataset['FamilySize']-train_dataset['FamilySize'].mean())/train_dataset['FamilySize'].std()


# In[ ]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(train_dataset.drop('Survived',axis=1), train_dataset['Survived'])
y_predicted=lr.predict(train_dataset.drop('Survived',axis=1))


# In[ ]:


from sklearn.metrics import confusion_matrix
confusion_matrix(train_dataset['Survived'], y_predicted)


# In[ ]:


test_data=pd.read_csv("/kaggle/input/titanic/test.csv")


# In[ ]:


test_data.drop(['Cabin','Name','Ticket'],axis=1,inplace=True)


# In[ ]:


test_data.head()


# In[ ]:


train_dataset.head()


# In[ ]:


test_data.isna().sum()


# In[ ]:





# In[ ]:


test_data["Age"]=test_data[['Age','Pclass']].apply(compute_age,axis=1)


# In[ ]:


train_dup=pd.read_csv("/kaggle/input/titanic/train.csv")
train_dup['Fare'].mean()


# In[ ]:


def computeFareIfNull(col):
    fare=col[0]
    if pd.isnull(fare)==False:
        return fare
    else:
        return 32.2042


# In[ ]:


test_data["Fare"]=test_data[['Fare']].apply(computeFareIfNull,axis=1)


# In[ ]:


test_data.head()


# In[ ]:


train_dataset.head()


# In[ ]:


sex=pd.get_dummies(test_data['Sex'],drop_first=True)
embark=pd.get_dummies(test_data['Embarked'],drop_first=True)
test_data=pd.concat([test_data,sex,embark],axis=1)
test_data.head()


# In[ ]:


test_data.drop(['Sex','Embarked'],axis=1,inplace=True)


# In[ ]:


test_data.head()
test_data['FamilySize']=test_data['SibSp']+test_data['Parch']


# In[ ]:


test_data.head()


# In[ ]:


test_data.drop(['SibSp','Parch'],axis=1,inplace=True)


# In[ ]:


y_test_prd=lr.predict(test_data.drop('PassengerId',axis=1))


# In[ ]:


sbu=pd.read_csv(  "/kaggle/input/titanic/gender_submission.csv")


# In[ ]:


sbu


# In[ ]:


frame = { 'Survived': y_test_prd}
mdl_result = pd.DataFrame(frame) 


# In[ ]:


result=pd.concat([test_data["PassengerId"],mdl_result],axis=1)
result.head()


# In[ ]:


result.to_csv('my_submission.csv', index=False)

