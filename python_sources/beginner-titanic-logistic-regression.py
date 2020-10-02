#!/usr/bin/env python
# coding: utf-8

# # Titanic Dataset
# 
# The goal of this notebook is try to predict the survival of passengers aboard the Titanic from their attributes.

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
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import missingno
sns.set_style('whitegrid')
sns.set_palette("deep")


# In[ ]:


gender_submission = pd.read_csv("../input/titanic/gender_submission.csv")
test = pd.read_csv("../input/titanic/test.csv")
train = pd.read_csv("../input/titanic/train.csv")


# # Section 1. Exploratory Data Analysis
# 
# How each person's attributes affect their survival rate will be explored.
# 
# Analysis will rely on the training dataset.

# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


#Types of data in each column
train.info()


# In[ ]:


#Overview of missing data within datasets
missingno.matrix(test,figsize = (10,3))
missingno.matrix(train,figsize = (10,3))


# In[ ]:


#Number of missing data
#Missing data exists in Age, Cabin and Embarked
#This will be dealt with in Section 2
train.isnull().sum()


# In[ ]:


plt.figure(figsize=(10,2))
ax = sns.countplot(y= 'Survived', data =train)
ax.set(xlabel = 'Count')


# In[ ]:


train['Survived'].value_counts()
pd.DataFrame(index=['Survived','Died'],data = [
    [342,"{0:.0f}%".format(342*100/891)],
    [549,"{0:.0f}%".format(549*100/891)]],
             columns=['Count','Percentage'])

#There more people who died than people who survived


# In[ ]:


sns.countplot(x='Survived',hue='Sex',data=train,palette = 'RdBu_r')
plt.title('Amount of Survivors by Gender')

#Relationship Detected
#Most of the goners where male while most of the survivors were female


# In[ ]:


sns.countplot(x='Survived',hue='Pclass',data=train)
plt.title("Amount of Survivors by Passenger Class")
#Relationship Detected
#3rd class passengers were most prevalent on the ship, and were also the class that perished the most


# In[ ]:


gr =train.groupby('Pclass')
for i in np.arange(1,4):
    globals()["c"+str(i)] = gr.get_group(i)

#c1 c2 c3 contain dataframes of Pclass 1 2 3 respectively

#There must be a better way to do this?
c1total = len(c1)
c2total = len(c2)
c3total = len(c3)

c1s = round(sum(c1['Survived']==1)*100/c1total,2)
c2s = round(sum(c2['Survived']==1)*100/c2total,2)
c3s = round(sum(c3['Survived']==1)*100/c3total,2)

survived_pclass =pd.DataFrame(data=[[100-c1s,100-c2s,100-c3s],[c1s,c2s,c3s]],index=['Dead','Survived'],columns=['Class 1','Class 2','Class 3'])


# In[ ]:


survived_pclass.plot(kind='bar')
plt.title("Percentage of Survivors per Passenger Class")


# In[ ]:


sns.countplot(hue='Survived',x='Pclass',data=train,palette = 'prism_r')
#Another viewing of the same data
#Colours accentuate death and survival


# In[ ]:


sns.distplot(train['Age'].dropna(),kde = False,hist_kws=dict(alpha=1))
plt.title("Age distribution of Titanic Passengers")


# In[ ]:


plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
ax = sns.distplot(train[train['Survived']==1]['Age'].dropna(),hist_kws=dict(alpha=0.7),color = 'green',bins = 30)
plt.title("Age Distribution of Survivors")
ax.set(xlabel='Age')


plt.subplot(1,2,2)
ax = sns.distplot(train[train['Survived']==0]['Age'].dropna(),hist_kws=dict(alpha=0.7),color = 'darkred',bins = 30)
plt.title("Age Distribution of Goners")
ax.set(xlabel='Age')


# In[ ]:


sns.scatterplot(y='Fare',x='Age',data=train,hue ='Survived',palette='prism_r')
plt.title("Fare and Age of passengers vs Survived")

#Most passengers with lower fare died, with the exception of younger passengers


# In[ ]:


plt.figure(figsize=(15,5))
#sns.countplot(x='Survived',hue='SibSp',data= train)
sns.countplot(hue='Survived',x='SibSp',data= train)


# In[ ]:


plt.figure(figsize=(15,5))
sns.countplot(x='Survived',hue='Parch',data= train)


# # 2. Data Cleaning

# In[ ]:


#Filling missing data for Age

plt.figure(figsize=(12,7))
sns.boxplot(x='Pclass',y='Age',hue = 'Sex',data=train)


# ### From the above boxplot, the average age of each passenger class is different
# #### With first class having the greatest average age and third class having the lowest average age
# Possibly because older people are more likely to be able to afford more expensive tickets?
# 
# There is also a slight difference in average age between the genders
# The missing fields in Age will be imputed with consideration of the passenger's class and gender

# In[ ]:


def age_imputer(cols):
    Age = cols[0]
    Pclass = cols[1]
    Sex = cols[2]
    
    if pd.isnull(Age):
        if Pclass ==1:
            if Sex == 'male':
                return train.groupby(['Sex','Pclass']).mean().loc['male']['Age'][1]
            elif Sex == 'female':
                return train.groupby(['Sex','Pclass']).mean().loc['female']['Age'][1]
        elif Pclass ==2:
            if Sex == 'male':
                return train.groupby(['Sex','Pclass']).mean().loc['male']['Age'][2]
            elif Sex == 'female':
                return train.groupby(['Sex','Pclass']).mean().loc['female']['Age'][2]
        elif Pclass ==3:
            if Sex == 'male':
                return train.groupby(['Sex','Pclass']).mean().loc['male']['Age'][3]
            elif Sex == 'female':
                return train.groupby(['Sex','Pclass']).mean().loc['female']['Age'][3]
            
    else:
        return Age


# In[ ]:


train['Age']=train[['Age','Pclass','Sex']].apply(age_imputer,axis = 1)
test['Age']=test[['Age','Pclass','Sex']].apply(age_imputer,axis = 1)


# In[ ]:


#Dealing with missing Embarked
train[train['Embarked'].isnull() == True]

#The passengers with missing Embarked boarded without any family
#Imputing values with the mode of Embarked.

train['Embarked'].fillna(train['Embarked'].mode()[0],inplace=True) #Embarked = S


# In[ ]:


#test has a missing value in Fare
test[test['Fare'].isnull()]
#Passenger is in the 3rd class and has no family boarded
#The imputed fare will be the average of the third class fare


# In[ ]:


test.isnull().sum()


# In[ ]:



test['Fare'].fillna(train[train['Pclass'] ==3]['Fare'].mean(),inplace = True)


# In[ ]:


print("\nTraining Set:\n")
print(train.isnull().sum())
print("\nTest Set:\n")
print(test.isnull().sum())
#Only missing value is Cabin, which might not be used


# # 3. Prediction

# ## Creating Dummy Variables

# In[ ]:


sex = pd.get_dummies(train['Sex'],drop_first=True) #Female is dropped (Baseline)
embark = pd.get_dummies(train['Embarked'],drop_first=True) #C is dropped (Baseline)
train = pd.concat([train,sex,embark],axis = 1)

sex = pd.get_dummies(test['Sex'],drop_first=True) #Female is dropped (Baseline)
embark = pd.get_dummies(test['Embarked'],drop_first=True) #C is dropped (Baseline)
test = pd.concat([test,sex,embark],axis = 1)


# ## Justifying Predictors to be used

# In[ ]:


train.drop(['PassengerId','Name','Ticket','Cabin','Sex','Embarked'],axis=1,inplace = True)
test.drop(['PassengerId','Name','Ticket','Cabin','Sex','Embarked'],axis=1,inplace =True)


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


X_train = train.drop(['Survived'],axis = 1)
y_train = train['Survived']


# # Building Logistic Regression Model

# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


# In[ ]:


log_model = LogisticRegression()


# In[ ]:


log_model.fit(X_train,y_train)


# In[ ]:


predictions = log_model.predict(test)


# In[ ]:


test = pd.read_csv("../input/titanic/test.csv")
predictions_df = pd.DataFrame(predictions,columns=['Survived'])


# In[ ]:


predictions_df.set_index(test['PassengerId'],inplace=True)


# In[ ]:


predictions_df


# In[ ]:


predictions_df.to_csv(r'predictions.csv')


