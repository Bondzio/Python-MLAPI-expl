#!/usr/bin/env python
# coding: utf-8

# ![](https://blog.socialcops.com/wp-content/uploads/2016/07/OG-MachineLearning-Python-Titanic-Kaggle.png)

# # Titanic EDA & Prediction 

# ![](data:image/jpeg;base64,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)

# ## So According to me, if you are newbie in DS, then you should start take part in titanic competition, dataset is very challenging, so this kernels is based on my opinion regarding dataset, so now you can enjoy EDA & Prediction

# In[ ]:


import numpy as np 
import pandas as pd 

import os
print(os.listdir("../input"))


# In[ ]:


dataset = pd.read_csv('../input/train.csv')


# In[ ]:


dataset.head()


# # So we need to first study of our data
# 
# ## 1 - PassengerId - Column does not depend on survive   
# ## 2 - Pclacss - it's needed for prediction      [--Select--]
# ## 4 - Name - it's not useful for our prediction
# ## 5 - Sex - Male/ Female depends on survived because female always get a first chance   [--Select--]
# ## 6 - Age - Age depends on survivde  [--Select--]
# ## 7 - SibSp - Having siblings/spouse depends on survived  [--Select--]
# ## 8 - Parch - Number of childs depends on survived  [--Select--]
# ## 9 - Ticket - Ticket not create impact on survived
# ## 10 - Fare - Fare create impact om survived because who have a costly tickets ,that person have more chance to get first in lifeboat  [--Select--]
# ## 11 - Cabin - Cabin have more null values and its not create any impact on survived
# ## 12 - Embarked - it's create impact on survived  [--Select--]

# In[ ]:


##Let's create funcition for barplot
def bar_chart(feature):
    survived = dataset[dataset['Survived']==1][feature].value_counts()
    dead = dataset[dataset['Survived']==0][feature].value_counts()
    df = pd.DataFrame([survived,dead])
    df.index = ['Survived','Dead']
    df.plot(kind='bar',stacked=True, figsize=(15,7))
    
bar_chart('Sex')


# In[ ]:


##Now let's see a barplot of Pclass
bar_chart('Pclass')


# In[ ]:


##Let's see for SibSp
bar_chart('SibSp')


# In[ ]:


##Let's see for Parch
bar_chart('Parch')


# In[ ]:


##Let's plot the Embarked
bar_chart('Embarked')


# In[ ]:


##Now let's make a list of our features matrix list
features= [ 'Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']
##Let's devide in X and Y
x = dataset[features]
y = dataset['Survived']


# In[ ]:


x.isnull().sum()


# In[ ]:


##Now fill the null values
x['Age'] = x['Age'].fillna(x['Age'].median())
x['Embarked']= x['Embarked'].fillna(x['Embarked'].value_counts().index[0])


# In[ ]:


###Now let's enocde categorical values 
from sklearn.preprocessing import LabelEncoder
LE = LabelEncoder()
x['Sex'] = LE.fit_transform(x['Sex'])
x['Embarked'] = LE.fit_transform(x['Embarked'])


# In[ ]:


##Now everything is ok 
##Now let's Split the Data
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.1,random_state =0)


# In[ ]:


##Now we fit our model
from xgboost import XGBClassifier
classifier = XGBClassifier(colsample_bylevel= 0.9,
                    colsample_bytree = 0.8, 
                    gamma=0.99,
                    max_depth= 5,
                    min_child_weight= 1,
                    n_estimators= 10,
                    nthread= 4,
                    random_state= 2,
                    silent= True)
classifier.fit(x_train,y_train)
classifier.score(x_test,y_test)


# In[ ]:


##Now take the test data for prediction
test_data = pd.read_csv('../input/test.csv')
test_x = test_data[features]


# In[ ]:


##Let's fill values
test_x['Age'] = test_x['Age'].fillna(test_x['Age'].median())
test_x['Fare'] = test_x['Fare'].fillna(test_x['Fare'].median())


# In[ ]:


##Let's enocde categorical values
test_x['Sex'] = LE.fit_transform(test_x['Sex'])
test_x['Embarked'] = LE.fit_transform(test_x['Embarked'])


# In[ ]:


##Now we predict the values
prediction = classifier.predict(test_x)


# In[ ]:


##Now according to rules we have to store a prediction in csv file
output = pd.DataFrame({'PassengerId': test_data.PassengerId,'Survived': prediction})
output.to_csv('submission.csv', index=False)
output.head()
##Submission.csv is a file which we have to submit in a competition


# # Upvote my kernel if you like it:), and share your opinion and suggestions in commentbox
