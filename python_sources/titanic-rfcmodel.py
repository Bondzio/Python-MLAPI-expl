#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


train_set = pd.read_csv('/kaggle/input/titanic/train.csv')
test_set = pd.read_csv('/kaggle/input/titanic/test.csv')
Gender_Sub = pd.read_csv('/kaggle/input/titanic/gender_submission.csv')


# In[ ]:


train_set.head(20)


# In[ ]:


train_set.shape


# In[ ]:


test_set.shape


# In[ ]:


test_set.head()


# Now, Checking for the null values in the given data.

# In[ ]:


train_null = train_set.isna().sum(0)
test_null =  test_set.isna().sum(0)
pd.concat([train_null,test_null],axis=1, sort = False, keys = ['train_null', 'test_null'])


# Acc. to Gender_Submission file, all women survived and all men died. So, let's check for our train_set data whether it applies. 

# In[ ]:


women_survived = train_set.loc[train_set.Sex=='female']["Survived"]
women_survived_percentage = sum(women_survived)/len(women_survived)
print("Female Survied % : ",women_survived_percentage)


# In[ ]:


#lets find out how many men survived in the similar way
men_survived = train_set.loc[train_set.Sex=='male']["Survived"]
men_survived_percentage  = sum(men_survived)/len(men_survived)
print("Male Survived % : ",men_survived_percentage)


# Lets check with building Random Forest Model

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
Y = train_set["Survived"]
columns = ["Pclass", "Sex", "SibSp", "Parch"]
X = pd.get_dummies(train_set[columns])
X1 = pd.get_dummies(test_set[columns])


#Building a RF Classifier Model

model = RandomForestClassifier(n_estimators = 50,max_depth = 5,random_state=1)
model.fit(X,Y)

#Predictions on Test Data Set(test_set)

Predictions = model.predict(X1)


output = pd.DataFrame({'PassengerId' : test_set.PassengerId,'Survived' : Predictions})
output.to_csv('my_submission.csv', index=False)

