#!/usr/bin/env python
# coding: utf-8

# 

# 

# In[ ]:


import pandas as pd #Pandas is a high level python library that allows us to manipulate datasets.
from sklearn.linear_model import LogisticRegression #in order to predict which passsenger will survive we 
#will need to build a model. ScikitLearn has a wide range of models freely availible. Here we are going 
#to use Logistic Regression. Simple to parametre.


# In[ ]:


#We import using padas the dataset
train=pd.read_csv("../input/train.csv",sep=',')
test=pd.read_csv("../input/test.csv",sep=',')


# In[ ]:


#We must index our Dataset.
#We will take the passenger Id columns in order to do so. 
#drop=True means the column does not bring any valuable information.
train.set_index('PassengerId',inplace=True,drop=True)
test.set_index('PassengerId',inplace=True,drop=True)


# 

# In[ ]:


train.sample(5)


# In[ ]:


test.head(5)


# 

# 

# In[ ]:


nullIndex=[]
nullCount=0
for i in range(1,len(train)+1):
    if train['Age'].isnull()[i]==True:
        nullIndex.append(i) #We collect passengerId to better fill the age column, but thats abnother story.
        nullCount+=1
print("There is : "+str(((nullCount/len(train))*100))[:5]+"% values missing")


# 

# In[ ]:


from scipy import median,mean
newAgeTrain=[train['Age'][i] for i in range(1,len(train)+1) if train['Age'].isnull()[i]==False]
newAgeTest=[test['Age'][i] for i in range(892,len(test)+892) if test['Age'].isnull()[i]==False]
Age=(len(train)*median(newAgeTrain)/(len(train)+len(test))+len(test)*median(newAgeTest)/(len(train)+len(test)))
Age


# In[ ]:


train['Age']=train['Age'].fillna(27.0)
test['Age']=test['Age'].fillna(27.0)


# 

# In[ ]:


del train['Name']
del train['Ticket']
del train['Embarked']
del train['Cabin']
del train['Sex']
del train['Fare']

del test['Name']
del test['Ticket']
del test['Embarked']
del test['Cabin']
del test['Sex']
del test['Fare']


# In[ ]:


train.tail(5)


# In[ ]:


test.head(5)


# 

# In[ ]:


target=train.Survived
del train['Survived']


# In[ ]:


#We import the logistic regression model :
LR=LogisticRegression()
#We train our model on the training dataset
LR.fit(train,target)
#We collect an arrow of predictions the size of the test dataset
predictions=LR.predict(test)
len(predictions)==len(test)


# In[ ]:


predictions


# In[ ]:


Resultat=pd.DataFrame()
index=[i for i in range(892,len(test)+892)]
Resultat['PassengerId']=index
Resultat['Survived']=predictions


# In[ ]:


Resultat.set_index('PassengerId',inplace=True,drop=True)


# In[ ]:


Resultat.to_csv('Titanic_01.csv')


# In[ ]:


Resultat.tail(10)


# In[ ]:





# In[ ]:




