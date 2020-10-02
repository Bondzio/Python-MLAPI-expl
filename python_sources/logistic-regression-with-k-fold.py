#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold


# In[ ]:


dftrain=pd.read_csv('../input/train.csv')
dftest=pd.read_csv("../input/test.csv")


# In[ ]:


dftrain.info()


# In[ ]:


dftrain.describe()


# In[ ]:


dftest.describe()


# In[ ]:


dftrain['Age']=dftrain['Age'].fillna(dftrain['Age'].median())
dftest['Age']=dftest['Age'].fillna(dftest['Age'].median())
dftest['Fare']=dftest['Fare'].fillna(dftest['Fare'].median())


# In[ ]:


dftrain.loc[dftrain['Sex']=='male','Sex']=0
dftrain.loc[dftrain['Sex']=='female','Sex']=1
dftest.loc[dftest['Sex']=='male','Sex']=0
dftest.loc[dftest['Sex']=='female','Sex']=1


# In[ ]:


#titanic.Embarked.unique()
#titanic.Embarked.value_counts()


# In[ ]:


"""titanic['Embarked']=titanic.Embarked.fillna('S')
titanic.loc[titanic['Embarked']=='S','Embarked']=0
titanic.loc[titanic['Embarked']=='C','Embarked']=1
titanic.loc[titanic['Embarked']=='Q','Embarked']=2
#titanic.descibe()"""


# In[ ]:


#dftrain.set_index(['PassengerId'],inplace=True)
#dftest.set_index(['PassengerId'],inplace=True)


# In[ ]:


"""alg=LinearRegression()
kf=KFold(titanic.shape[0],n_folds=3,random_state=1)
listfold=list(kf)
print(kf)"""
alg=LogisticRegression()
kf=KFold(dftrain.shape[0],n_folds=3,random_state=1)
listfold=list(kf)
print(kf)


# In[ ]:


train,test=listfold[0]
dftrain.describe()


# In[ ]:


print(len(train))
len(test)


# In[ ]:


dftrain.columns


# In[ ]:


pradicator=['PassengerId','Pclass', 'Sex', 'Age', 'SibSp','Parch', 'Fare']
pradication=[]


# In[ ]:


for train,test in kf:
    train_data=dftrain[pradicator].iloc[train]
    train_prad=dftrain['Survived'].iloc[train]
    alg.fit(train_data,train_prad)
    test_prad=alg.predict(dftrain[pradicator].iloc[test])
    pradication.append(test_prad)


# In[ ]:


len(pradication)


# In[ ]:


import numpy as np


# In[ ]:


pradication=np.concatenate(pradication,axis=0)


# In[ ]:


pradication[pradication>0.5]=1
pradication[pradication<=0.5]=0


# In[ ]:


accuracy=sum(pradication==dftrain['Survived'])/len(pradication)
accuracy


# In[ ]:


X_train=dftrain[pradicator]
y=dftrain['Survived']
X_test=dftest[pradicator]
alg.fit(X_train,y)
prediction = alg.predict(X_test)
ids=dftest['PassengerId']
dfprediction=pd.DataFrame( { 'PassengerId': ids,'Survived': prediction})
#dfPrediction = pd.DataFrame(data=prediction,index = dftest.index.values,columns=['Survived'])
print(dfprediction)
output = dfprediction.to_csv('submission.csv', index=False)



# In[ ]:





# In[ ]:




