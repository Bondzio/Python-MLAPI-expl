#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


df=pd.read_csv("../input/titanic/train.csv")
test=pd.read_csv("../input/titanic/test.csv")
df.head()


# In[ ]:


df.drop("Name",axis=1,inplace=True)
df.drop("Ticket",axis=1,inplace=True)
df.drop(["Fare"],axis=1,inplace=True)


# In[ ]:


df.head()


# In[ ]:


df.isna().sum()


# In[ ]:


df["Cabin"].fillna(str(df["Cabin"].mode().values[0]),inplace=True)


# In[ ]:


df["Cabin"]=df["Cabin"].apply(lambda x:str(x).replace(' ','')if ' ' in str(x) else str(x))


# In[ ]:


df["Deck"] = df["Cabin"].str.slice(0,1)


# In[ ]:


df.drop(["Cabin"],axis=1,inplace=True)


# In[ ]:


def impute_median(series):
    return series.fillna(series.median())


# In[ ]:


df.Age=df.Age.transform(impute_median)


# In[ ]:


df.isnull().sum()


# In[ ]:


df["Embarked"]=df["Embarked"].fillna("S")


# In[ ]:


df.isnull().sum()


# In[ ]:


df['Is_Married'] = np.where(df['SibSp']==1, 1, 0)
df.head()


# In[ ]:


df["Family_Size"]=df.SibSp+df.Parch
df.head()


# In[ ]:


df['Elderly'] = np.where(df['Age']>=50, 1, 0)


# In[ ]:


df.head()


# In[ ]:


df.dtypes


# In[ ]:


from sklearn.preprocessing import LabelEncoder
labelEncoder_Y=LabelEncoder()
df.iloc[:,3]=labelEncoder_Y.fit_transform(df.iloc[:,3].values)
df.iloc[:,7]=labelEncoder_Y.fit_transform(df.iloc[:,7].values)
df.iloc[:,8]=labelEncoder_Y.fit_transform(df.iloc[:,8].values)


# In[ ]:


df.dtypes


# In[ ]:


df.Sex.value_counts()


# In[ ]:


sns.countplot(df.Sex,label="count")
plt.show()


# In[ ]:


df.Survived.value_counts()


# In[ ]:


sns.countplot(df.Survived,label="count")
plt.show()


# In[ ]:


sns.pairplot(df.iloc[:,1:12],hue="Survived")
plt.show()


# In[ ]:


df.iloc[:,1:12].corr()


# In[ ]:


plt.figure(figsize=(10,10))
sns.heatmap(df.iloc[:,1:12].corr(), annot=True,fmt=".0%")
plt.show()


# In[ ]:


test.head()


# In[ ]:


test['Is_Married'] = np.where(test['SibSp']==1, 1, 0)
test.head()


# In[ ]:


test["Family_Size"]=test.SibSp+test.Parch
test.head()


# In[ ]:


test['Elderly'] = np.where(test['Age']>=50, 1, 0)
test.head()


# In[ ]:


test.drop("Name",axis=1,inplace=True)
test.drop("Ticket",axis=1,inplace=True)
test.drop("Fare",axis=1,inplace=True)


# In[ ]:


test.isnull().sum()


# In[ ]:


test.Age=test.Age.transform(impute_median)


# In[ ]:


test["Cabin"].fillna(str(test["Cabin"].mode().values[0]),inplace=True)


# In[ ]:


test["Cabin"]=test["Cabin"].apply(lambda x:str(x).replace(' ','')if ' ' in str(x) else str(x))


# In[ ]:


test["Deck"] = test["Cabin"].str.slice(0,1)


# In[ ]:


test.drop(["Cabin"],axis=1,inplace=True)


# In[ ]:


test.dtypes


# In[ ]:


from sklearn.preprocessing import LabelEncoder
labelEncoder_Y=LabelEncoder()
test.iloc[:,2]=labelEncoder_Y.fit_transform(test.iloc[:,2].values)
test.iloc[:,6]=labelEncoder_Y.fit_transform(test.iloc[:,6].values)
test.iloc[:,10]=labelEncoder_Y.fit_transform(test.iloc[:,10].values)


# In[ ]:


test.head()


# In[ ]:


x=df.iloc[:,2:12].values
y=df.iloc[:,1].values.reshape(-1,1)
x_test  = test.drop("PassengerId",axis=1).copy()


# In[ ]:



from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test=train_test_split(x,y,test_size=0.469,random_state=42)


# In[ ]:


from sklearn.preprocessing import StandardScaler

sc=StandardScaler()
x_train=sc.fit_transform(x_train)
x_test=sc.fit_transform(x_test)


# In[ ]:


x_train.shape


# In[ ]:


x_test.shape


# In[ ]:


y_train.shape


# In[ ]:


y_test.shape


# In[ ]:


def models(x_train,y_train):
  
  from sklearn.linear_model import LogisticRegression
  log=LogisticRegression(random_state=42)
  log.fit(x_train,y_train)
  
 
  from sklearn.tree import DecisionTreeClassifier
  tree=DecisionTreeClassifier(criterion='entropy',random_state=0)
  tree.fit(x_train,y_train)
  
  
  from sklearn.ensemble import RandomForestClassifier
  forest = RandomForestClassifier(n_estimators=15,criterion="entropy",random_state=0)
  forest.fit(x_train,y_train)

  print("[0]Logistic Regression Training Accuracy:",log.score(x_train,y_train))
  print("[1]Decision Tree Classifier Training Accuracy:",tree.score(x_train,y_train))
  print("[2]Random Forest Classifier Training Accuracy:",forest.score(x_train,y_train))
  
  return log,tree,forest


# In[ ]:


model = models(x_train,y_train)


# In[ ]:


from sklearn.metrics import confusion_matrix


for i in range(len(model)):
  print("Model ", i)
  cm =confusion_matrix(y_test,model[i].predict(x_test))

  TP=cm[0][0]
  TN=cm[1][1]
  FN=cm[1][0]
  FP=cm[0][1]

  print(cm)
  print("Testing Accuracy = ", (TP+TN) / (TP+TN+FN+FP))
  print()


# In[ ]:


from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

for i in range(len(model) ):
  print("Model ",i)
  print( classification_report(y_test,model[i].predict(x_test)))
  print( accuracy_score(y_test,model[i].predict(x_test)))
  print()


# In[ ]:


pred=model[0].predict(x_test)
print(pred)


# In[ ]:


PassengerId = test['PassengerId']
submission = pd.DataFrame({ 'PassengerId': PassengerId,
                            'Survived': pred })
submission.to_csv(r'submission.csv',index=False)


# In[ ]:


from IPython.display import FileLink
FileLink(r'submission.csv')


# <a href="./submission.csv"> Download File </a>
