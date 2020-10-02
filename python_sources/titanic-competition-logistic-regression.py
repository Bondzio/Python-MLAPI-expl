#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# **Dataset exploration**

# In[ ]:


train_df = pd.read_csv('../input/titanic/train.csv')
test_df = pd.read_csv('../input/titanic/test.csv')
train_df.head()


# In[ ]:


data_train = train_df.drop(['Name', 'Ticket', 'Cabin'], axis=1)
data_test = test_df.drop(['Name', 'Ticket', 'Cabin'], axis=1)
data_train.head()


# In[ ]:


print(data_train.info(), data_test.info())


# **Data cleaning**

# In[ ]:


data_train.Age = data_train['Age'].fillna(data_train['Age'].median())
data_test.Age = data_test['Age'].fillna(data_test['Age'].median())
data_train.Embarked = data_train['Embarked'].fillna('S')
data_test.Fare = data_test['Fare'].fillna(data_test['Fare'].median())


# In[ ]:


data_train.info(), data_test.info()


# In[ ]:


categorical_cols = [cname for cname in data_train.columns if
                    len(data_train[cname].unique()) <= 10 and
                    data_train[cname].dtype == 'object'
                   ]
numerical_cols = [cname for cname in data_train.columns if
                    data_train[cname].dtype in ['int64', 'float64']
                 ]


# In[ ]:


embarked_categorical = {category: index for index, category in enumerate(data_train.Embarked.astype('category').cat.categories)}
sex_categorical = {category: index for index, category in enumerate(data_train.Sex.astype('category').cat.categories)}

data_train.Embarked = data_train['Embarked'].map(embarked_categorical)
data_test.Embarked = data_test['Embarked'].map(embarked_categorical)

data_train.Sex = data_train['Sex'].map(sex_categorical)
data_test.Sex = data_test['Sex'].map(sex_categorical)


# **Training**

# In[ ]:


data_train.columns


# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(data_train.drop(['PassengerId', 'Survived'], axis=1), data_train['Survived'], test_size=0.2)


# In[ ]:


model = LogisticRegression()
model.fit(X_train, Y_train)


# In[ ]:


# Good accuracy!!!
y_pred = model.predict(X_test)
print('Accuracy Score:', str(accuracy_score(Y_test, y_pred)*100) + '%')


# **Prediction**

# In[ ]:


X_for_real_prediction = data_test.drop('PassengerId', axis=1)
X_for_real_prediction


# In[ ]:


real_predictions = model.predict(X_for_real_prediction)
real_predictions


# In[ ]:


output = pd.DataFrame({'PassengerId':data_test.PassengerId,'Survived':real_predictions})
output


# In[ ]:


output.to_csv('my_titanic_submission.csv', index=False)
print('All ready')


# In[ ]:




