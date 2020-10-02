#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


DfTrain = pd.read_csv('/kaggle/input/titanic/train.csv')
DfTest = pd.read_csv('/kaggle/input/titanic/test.csv')


# In[ ]:


DfTrain.shape


# In[ ]:


DfTrain.info()


# In[ ]:


DfTrain.head()


# In[ ]:


DfTest.shape


# In[ ]:


DfTest.head()


# In[ ]:


DfTrain.corr()


# In[ ]:


import random as rnd
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


DfTrain.describe()


# In[ ]:


# for categorical features
DfTrain.describe(include=['O'])


# In[ ]:


DfTrain[['Pclass','Survived']].groupby(['Pclass'],as_index = False).mean().sort_values(by= 'Survived')


# In[ ]:


DfTrain[['Sex','Survived']].groupby(['Sex'],as_index = False).mean().sort_values(by= 'Survived')


# In[ ]:


DfTrain[['SibSp','Survived']].groupby(['SibSp'],as_index = False).mean().sort_values(by= 'Survived',ascending=False)


# In[ ]:


DfTrain[['Parch','Survived']].groupby(['Parch'],as_index = False).mean().sort_values(by= 'Survived')


# In[ ]:


graph = sns.FacetGrid(DfTrain,col='Survived')
graph.map(plt.hist,'Age',bins=20)


# In[ ]:


import warnings
warnings.filterwarnings('ignore')


# In[ ]:


graph = sns.FacetGrid(DfTrain, col='Survived', row='Pclass', size=2.2, aspect=1.6)
graph.map(plt.hist, 'Age', alpha=.5, bins=20)
graph.add_legend();


# In[ ]:


graphs = sns.FacetGrid(DfTrain ,row ='Embarked', size = 3, aspect=2 )
graphs.map(sns.pointplot, 'Pclass', 'Survived', 'Sex' , palette='deep' ,markers=["o", "x"],linestyles=["-", "--"])
graphs.add_legend()


# In[ ]:


graph = sns.FacetGrid(DfTrain, row='Embarked', col='Survived', size=2, aspect=1.5)
graph.map(sns.barplot, 'Sex', 'Fare', alpha=.5)
graph.add_legend()


# In[ ]:


FullData = [DfTrain, DfTest]


# In[ ]:


print("---Before---")
print("Train Data : {}".format(DfTrain.shape))
print("Test Data : {}".format(DfTest.shape))
print("Full Data : {}".format(FullData[0].shape))
print("Full Data : {}".format(FullData[1].shape))

DfTrain = DfTrain.drop(['Ticket','Cabin'], axis=1)
DfTest = DfTest.drop(['Ticket','Cabin'], axis=1)
FullData = [DfTrain, DfTest]


# In[ ]:


print("---After Preprocessing---")
print("Train Data : {}".format(DfTrain.shape))
print("Test Data : {}".format(DfTest.shape))
print("Full Data : {}".format(FullData[0].shape))
print("Full Data : {}".format(FullData[1].shape))


# In[ ]:


FullData[0].head()


# In[ ]:


#Name Titles count
for dataset in FullData:
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)


# In[ ]:


pd.crosstab(DfTrain['Title'], DfTrain['Sex'])


# In[ ]:


for dataset in FullData:
    dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')

    dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')
    
DfTrain[['Title', 'Survived']].groupby(['Title'], as_index=False).mean()


# In[ ]:


titles = {"Mrs" : 1,"Miss" : 2, "Master" : 3 ,"Mr" : 4, "Rare" : 5}

for dataset in FullData:
    dataset['Title'] = dataset['Title'].map(titles)
    dataset['Title'] = dataset['Title'].fillna(0)
    
DfTrain.head(10)


# In[ ]:


DfTrain = DfTrain.drop(['Name','PassengerId'],axis=1)
DfTest = DfTest.drop(['Name'], axis =1)
FullData = [DfTrain,DfTest]


# In[ ]:


print(DfTrain.shape)
print(DfTest.shape)


# In[ ]:


for dataset in FullData:
    dataset['Sex'] = dataset['Sex'].map({'male':0,'female':1})
    
DfTrain.head(10)
#Male -> 0
#Female -> 1


# In[ ]:


#checking what Age and which Gender were class

graph = sns.FacetGrid(DfTrain,row = 'Pclass',col = 'Sex', size = 2,aspect = 1.5 )
graph.map(plt.hist , 'Age', bins =20 , color= 'g')
graph.add_legend()


# In[ ]:


DfTrain['AgeBar'] = pd.cut(DfTrain['Age'],5 ) #slice the age range to 5 bins
DfTrain[['AgeBar','Survived']].groupby(['AgeBar'], as_index=False).mean().sort_values(by='AgeBar')


# In[ ]:


DfTrain.head() #Extra Age bar and change Age column to ordinal


# In[ ]:


for dataset in FullData:
    dataset.loc[ dataset['Age'] <= 16 ,'Age'] = 0
    dataset.loc[ (dataset['Age'] >= 16) & (dataset['Age'] <=32), 'Age'] = 1
    dataset.loc[ (dataset['Age'] >= 32) & (dataset['Age'] <=48), 'Age'] = 2
    dataset.loc[ (dataset['Age'] >=48) & (dataset['Age'] <=64) ,'Age'] = 3
    dataset.loc[ dataset['Age'] >= 64 ,'Age'] 


# In[ ]:


DfTrain = DfTrain.drop(['AgeBar'] , axis = 1)
FullData = [DfTrain,DfTest]


# In[ ]:


DfTrain.head()


# In[ ]:


for dataset in FullData:
    dataset['Family'] = dataset['SibSp'] + dataset['Parch'] + 1

DfTrain[['Family','Survived']].groupby(['Family'] , as_index = False).mean().sort_values(by = 'Survived', ascending=False) 


# In[ ]:


for dataset in FullData:
    dataset['withOutFamily'] = 0
    dataset.loc[dataset['Family']==1 ,'withOutFamily'] = 1
    
DfTrain[['withOutFamily','Survived']].groupby(['withOutFamily'] ,as_index=False).mean()


# In[ ]:


DfTrain = DfTrain.drop(['Parch', 'SibSp', 'Family'], axis=1)
DfTest = DfTest.drop(['Parch', 'SibSp', 'Family'], axis=1)
FullData = [DfTrain,DfTest]

DfTrain.head(10)


# In[ ]:


#DfTrain = DfTrain.drop(['Age*Class'], axis=1)
#DfTest = DfTest.drop(['Age*Class'], axis=1)
#FullData = [DfTrain,DfTest]

#DfTrain.head(10)


# In[ ]:


guess_ages = np.zeros((2,3))
guess_ages


# In[ ]:


for dataset in FullData:
    for i in range(0, 2):
        for j in range(0, 3):
            guess_df = dataset[(dataset['Sex'] == i) & (dataset['Pclass'] == j+1)]['Age'].dropna()
            age_guess = guess_df.median()
            guess_ages[i,j] = int( age_guess/0.5 + 0.5 ) * 0.5
            
    for i in range(0, 2):
        for j in range(0, 3):
            dataset.loc[ (dataset.Age.isnull()) & (dataset.Sex == i) & (dataset.Pclass == j+1),'Age'] = guess_ages[i,j]
    dataset['Age'] = dataset['Age'].astype(int)

DfTrain.head(10)


# In[ ]:


for dataset in FullData:
    dataset['AgeWithClass'] = dataset.Age * dataset.Pclass

DfTrain.loc[:, ['AgeWithClass', 'Age', 'Pclass']].head(10)


# In[ ]:


freq_port = DfTrain['Embarked'].isna().sum()
freq_port


# In[ ]:


EmbarkedNA = DfTrain.Embarked.dropna().mode()[0]
EmbarkedNA


# In[ ]:


for dataset in FullData:
    dataset['Embarked'] = dataset['Embarked'].fillna(EmbarkedNA)
    
DfTrain[['Embarked', 'Survived']].groupby(['Embarked'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[ ]:


for dataset in FullData:
    dataset['Embarked'] = dataset['Embarked'].map({'S':0,'C':1,'Q':2}).astype(int)
    
DfTrain.head()


# In[ ]:


#from sklearn.preprocessing import MinMaxScaler
#scaler = MinMaxScaler()
DfTest['Fare'].fillna(DfTest['Fare'].dropna().median(), inplace=True)
DfTest.head()


# In[ ]:


#FullData['Fare'] = FullData['Fare'].astype(int).apply(lambda x: MinMaxScaler().fit_transform(x))
#DfTrain['Fare'].dtype
DfTrain['FareRange'] = pd.qcut(DfTrain['Fare'], 4)
DfTrain[['FareRange', 'Survived']].groupby(['FareRange'], as_index=False).mean().sort_values(by='FareRange', ascending=True)


# In[ ]:


for dataset in FullData:
    dataset.loc[ dataset['Fare'] <= 7.91, 'Fare'] = 0
    dataset.loc[(dataset['Fare'] > 7.91) & (dataset['Fare'] <= 14.454), 'Fare'] = 1
    dataset.loc[(dataset['Fare'] > 14.454) & (dataset['Fare'] <= 31), 'Fare']   = 2
    dataset.loc[ dataset['Fare'] > 31, 'Fare'] = 3
    dataset['Fare'] = dataset['Fare'].astype(int)

DfTrain = DfTrain.drop(['FareRange'], axis=1)
combine = [DfTrain, DfTest]
    
DfTrain.head()


# In[ ]:


X_train = DfTrain.drop("Survived", axis=1)
Y_train = DfTrain["Survived"]
X_test  = DfTest.drop("PassengerId", axis=1).copy()
X_train.shape, Y_train.shape, X_test.shape


# In[ ]:


#Model
from sklearn.linear_model import LogisticRegression
log = LogisticRegression()
log.fit(X_train,Y_train)
prediction = log.predict(X_test)
perfmce = round(log.score(X_train,Y_train) * 100,2)
print("Accuracy with Logistic Regression : {}".format(perfmce))


# In[ ]:


from sklearn.svm import SVC
svc = SVC()
svc.fit(X_train, Y_train)
Y_pred = svc.predict(X_test)
SVMperfmce = round(svc.score(X_train, Y_train) * 100, 2)
print("Accuracy with Support Vector : {}".format(SVMperfmce))


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

rd = RandomForestClassifier(n_estimators=30)
rd.fit(X_train, Y_train)
Y_pred = rd.predict(X_test)
rd.score(X_train, Y_train)
RdForestperfmce = round(rd.score(X_train, Y_train) * 100, 2)
print("Accuracy with Random Forest : {}".format(RdForestperfmce))


# In[ ]:


submission = pd.DataFrame({
        "PassengerId": DfTest["PassengerId"],
        "Survived": Y_pred
    }) 


# In[ ]:


filename = 'submission.csv'
submission.to_csv(filename,index=False)
print('Saved file: ' + filename)

