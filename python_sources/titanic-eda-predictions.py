#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math


# ## Train Data 

# In[ ]:


train_data = pd.read_csv('/kaggle/input/titanic/train.csv')
train_data.head()


# In[ ]:


train_data.shape


# In[ ]:


train_data.isnull().sum()


# In[ ]:


train_data[train_data.Embarked.isnull()]


# In[ ]:


#Dropping rows with Embarked as null
train_data = train_data[~train_data.Embarked.isnull()]
train_data.shape


# In[ ]:


#Imputing the mean age for missing values 
val = train_data.Age.mean()
train_data['Age'] = train_data.Age.apply(lambda x : val if math.isnan(x) else x)


# In[ ]:


train_data.Survived.value_counts().plot.pie(autopct='%0.2f%%')
plt.show()


# In[ ]:


train_data.Pclass.value_counts().plot.pie(autopct='%0.2f%%')
plt.show()


# In[ ]:


train_data.Sex.value_counts().plot.pie(autopct='%0.2f%%')
plt.show()


# In[ ]:


train_data.Embarked.value_counts().plot.pie(autopct='%0.2f%%')
plt.show()


# In[ ]:


sns.distplot(train_data.Age)
plt.show()


# In[ ]:


sns.distplot(train_data.Fare)
plt.show()


# In[ ]:


sns.countplot(data = train_data, x = 'Pclass',  hue = 'Survived')
plt.show()


# In[ ]:


sns.countplot(data = train_data, x = 'Sex',  hue = 'Survived')
plt.show()


# ## Test Data

# In[ ]:


test_data = pd.read_csv('/kaggle/input/titanic/test.csv')
test_data.shape


# In[ ]:


test_data.isnull().sum()


# In[ ]:


#Imputing the mean age for missing values 
val = test_data.Age.mean()
test_data['Age'] = test_data.Age.apply(lambda x : val if math.isnan(x) else x)


# In[ ]:


test_data[test_data.Fare.isnull()]


# In[ ]:


#Imputing the Fare value
val = test_data.groupby('Pclass').Fare.mean()
test_data.loc[test_data.PassengerId == 1044, 'Fare'] = val[3]
test_data[test_data.PassengerId == 1044]


# ## Model Training 

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV


# In[ ]:


train_data.columns


# In[ ]:


def creatingDummyVariables(df, columns) :
    # Creating a dummy variable for some of the categorical variables and dropping the first one.
    dummy1 = pd.get_dummies(df[columns], drop_first=True)
    
    # Adding the results to the master dataframe
    df1 = pd.concat([df, dummy1], axis=1)
    
    #Dropping the initial column
    df1.drop(columns, axis = 1, inplace = True)
    
    return df1


# In[ ]:


def createModelDF(df, col) :
    model_df = df[col]
    model_df = creatingDummyVariables(model_df, ['Sex','Embarked'])
    return model_df


# In[ ]:


model_train_data = createModelDF(train_data,['Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked'])


# In[ ]:


x_train = model_train_data.drop('Survived',1)
y_train = model_train_data['Survived']


# In[ ]:


dt_basic = DecisionTreeClassifier(max_depth=10)
dt_basic.fit(x_train,y_train)


# In[ ]:


# Create a Parameter grid
param_grid = {
    'max_depth' : range(5,20,5),
    'min_samples_leaf' : range(50,210,50),
    'min_samples_split' : range(50,210,50),
    'criterion' : ['gini','entropy'] 
}


# In[ ]:


n_folds = 5


# In[ ]:


dtree = DecisionTreeClassifier()
grid = GridSearchCV(dtree, param_grid, cv = n_folds, n_jobs = -1,return_train_score=True)


# In[ ]:


grid.fit(x_train,y_train)


# In[ ]:


cv_result = pd.DataFrame(grid.cv_results_)
cv_result.head()


# In[ ]:


grid.best_params_


# In[ ]:


grid.best_score_


# In[ ]:


best_grid = grid.best_estimator_
best_grid


# In[ ]:


best_grid.fit(x_train,y_train)


# In[ ]:


x_test = createModelDF(test_data,['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked'])


# In[ ]:


y_test = best_grid.predict(x_test)


# In[ ]:


predictions = pd.DataFrame({'PassengerId' : test_data.PassengerId,
                    'Survived' : y_test
                   })
predictions.to_csv('predictions.csv',index = False)
print('Test predictions stored in csv file')

