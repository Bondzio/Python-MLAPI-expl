#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


get_ipython().system('pip install numpy')


# In[ ]:


train = pd.read_csv("../input/titanic/train.csv")
train.head()


# In[ ]:


test = pd.read_csv("../input/titanic/test.csv")
test.head()


# In[ ]:


train.info()


# In[ ]:


test.info()


# In[ ]:


all = pd.concat([train, test], sort = False)
all.info()


# In[ ]:


#Fill Missing numbers with median
all['Age'] = all['Age'].fillna(value=all['Age'].median())
all['Fare'] = all['Fare'].fillna(value=all['Fare'].median())


# In[ ]:


all.info()


# In[ ]:


sns.catplot(x = 'Embarked', kind = 'count', data = all) #or all['Embarked'].value_counts()


# In[ ]:


all['Embarked'] = all['Embarked'].fillna('S')
all.info()


# ****Extra Features:

# In[ ]:


#Age
all.loc[ all['Age'] <= 16, 'Age'] = 0
all.loc[(all['Age'] > 16) & (all['Age'] <= 32), 'Age'] = 1
all.loc[(all['Age'] > 32) & (all['Age'] <= 48), 'Age'] = 2
all.loc[(all['Age'] > 48) & (all['Age'] <= 64), 'Age'] = 3
all.loc[ all['Age'] > 64, 'Age'] = 4 


# In[ ]:


#Title
import re
def get_title(name):
    title_search = re.search(' ([A-Za-z]+\.)', name)
    
    if title_search:
        return title_search.group(1)
    return ""


# In[ ]:


all['Title'] = all['Name'].apply(get_title)
all['Title'].value_counts()


# In[ ]:


all['Title'] = all['Title'].replace(['Capt.', 'Dr.', 'Major.', 'Rev.'], 'Officer.')
all['Title'] = all['Title'].replace(['Lady.', 'Countess.', 'Don.', 'Sir.', 'Jonkheer.', 'Dona.'], 'Royal.')
all['Title'] = all['Title'].replace(['Mlle.', 'Ms.'], 'Miss.')
all['Title'] = all['Title'].replace(['Mme.'], 'Mrs.')
all['Title'].value_counts()


# In[ ]:


#Cabin
all['Cabin'] = all['Cabin'].fillna('Missing')
all['Cabin'] = all['Cabin'].str[0]
all['Cabin'].value_counts()


# In[ ]:


#Family Size & Alone 
all['Family_Size'] = all['SibSp'] + all['Parch'] + 1
all['IsAlone'] = 0
all.loc[all['Family_Size']==1, 'IsAlone'] = 1
all.head()


# In[ ]:


#Drop unwanted variables
all_1 = all.drop(['Name', 'Ticket'], axis = 1)
all_1.head()


# In[ ]:


all_dummies = pd.get_dummies(all_1, drop_first = True)
all_dummies.head()


# In[ ]:


all_train = all_dummies[all_dummies['Survived'].notna()]
all_train.info()


# In[ ]:


all_test = all_dummies[all_dummies['Survived'].isna()]
all_test.info()


# ****Train/Test Split

# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(all_train.drop(['PassengerId','Survived'],axis=1), 
                                                    all_train['Survived'], test_size=0.30, 
                                                    random_state=101)


# ### Build Random Forest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


RF_model = RandomForestClassifier()


# In[ ]:


from sklearn.model_selection import GridSearchCV


# In[ ]:


#Using max_depth, criterion will suffice for DT Models, rest all will remain constant 
parameters = {'n_estimators' : (10,30,50,70,90,100)
              , 'criterion' : ('gini', 'entropy')
              , 'max_depth' : (3,5,7,9,10)
              , 'max_features' : ('auto', 'sqrt')
              , 'min_samples_split' : (2,4,6)
              #, 'min_weight_fraction_leaf' : (0.0,0.1,0.2,0.3)
             }


# In[ ]:


RF_grid  = GridSearchCV(RandomForestClassifier(n_jobs = -1, oob_score= False), param_grid = parameters, cv = 3, verbose = True)


# In[ ]:


RF_grid_model = RF_grid.fit(X_train, y_train)


# In[ ]:


RF_grid_model.best_estimator_


# In[ ]:


RF_model = RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight=None,
                       criterion='entropy', max_depth=3, max_features='sqrt',
                       max_leaf_nodes=None, max_samples=None,
                       min_impurity_decrease=0.0, min_impurity_split=None,
                       min_samples_leaf=1, min_samples_split=4,
                       min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=-1,
                       oob_score=False, random_state=None, verbose=0,
                       warm_start=False)


# In[ ]:


RF_model.fit(X_train, y_train)


# In[ ]:


predictions = RF_model.predict(X_test)
predictions


# ****Check Accuracy

# In[ ]:


print(f'Test : {RF_model.score(X_test, y_test):.3f}')
print(f'Train : {RF_model.score(X_train, y_train):.3f}')
      


# ****Final Predictions

# In[ ]:


all_test.head()


# In[ ]:


TestForPred = all_test.drop(['PassengerId', 'Survived'], axis = 1)


# In[ ]:


TestForPred.info()


# In[ ]:


t_pred = RF_model.predict(TestForPred).astype(int)


# In[ ]:


PassengerId = all_test['PassengerId']


# In[ ]:


RF_Sub = pd.DataFrame({'PassengerId': PassengerId, 'Survived':t_pred })
RF_Sub.head()


# In[ ]:


RF_Sub.to_csv("RF_Class_Submission.csv", index = False)


# In[ ]:




