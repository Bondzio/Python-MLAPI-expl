#!/usr/bin/env python
# coding: utf-8

# Import relevant libraries

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


titanictrain = pd.read_csv("../input/train.csv")


# In[ ]:


titanictrain.head()


# First, we turn categorical variables to numerical and add them to our dataframe

# In[ ]:


sex = pd.get_dummies(titanictrain['Sex'],drop_first=True)
embark = pd.get_dummies(titanictrain['Embarked'],drop_first=True)


# In[ ]:


titanictrain.drop(['Sex','Embarked'],axis=1,inplace=True)
train = pd.concat([titanictrain,sex,embark],axis=1)


# In[ ]:


train.head()


# We define a funtion to grab only the title from the name column.
# We do this so we can impute age based on title, since different titles were used for children and adults (e.g. the honorific "Master" was used for young boys.

# In[ ]:


import re

def splitter(cols):
    return re.split('\, |\. ',cols)[1]


train['Name'] = train['Name'].apply(splitter)


# In[ ]:


train.head()


# In[ ]:


def age_imputation(cols):
    
    Age=cols[0]
    Name=cols[1]
    
    if pd.isnull(Age):
        if Name == 'Mr':
            return 32
        elif Name == 'Mrs':
            return 36
        elif Name == 'Miss':
            return 22
        elif Name == 'Master':
            return 5
        elif Name == 'Dr':
            return 42
    else:
        return Age


# In[ ]:


train['Age'] = train[['Age','Name']].apply(age_imputation,axis=1)


# We'll use a random forest classifier for this first attempt

# In[ ]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


from sklearn.model_selection import train_test_split


# We drop the Cabin column for now since it's missing too much data.

# In[ ]:


train.drop(['Name','Ticket','Cabin'],axis=1,inplace=True)


# In[ ]:


X = train.drop('Survived',axis=1)
y = train['Survived']


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)


# In[ ]:


rfc = RandomForestClassifier(n_estimators=200)


# In[ ]:


rfc.fit(X_train,y_train)


# In[ ]:


rfc_pred = rfc.predict(X_test)


# In[ ]:


from sklearn.metrics import classification_report, confusion_matrix


# In[ ]:


print(classification_report(rfc_pred,y_test))


# So we get a precision 82% abd a recall of 81%, which is not bad for a first attempt.
# We'll come back with more feature engineering.
