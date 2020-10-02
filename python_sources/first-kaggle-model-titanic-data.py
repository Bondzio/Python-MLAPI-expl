#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:





# In[ ]:


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')

train.head()


# In[ ]:


test.head()


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier()

train.Sex = train.Sex.replace('male', 0)
train.Sex = train.Sex.replace('female', 1)

test.Sex = test.Sex.replace('male', 0)
test.Sex = test.Sex.replace('female', 1)



# In[ ]:





# In[ ]:


train[["Age", "Survived"]].groupby("Age").count().plot()


# In[ ]:


train[["Survived", "Age"]].groupby(["Age"]).mean().plot(),
train[["Survived", "Age"]].groupby(["Age"]).count().plot()


# In[ ]:


train.head()


# In[ ]:


corr = train.corr()
corr


# In[ ]:


import seaborn as sns
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True

)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'

)


# In[ ]:


test = test.fillna(0)

train.Fare = [int(x) for x in train.Fare]
test.Fare = [int(x) for x in test.Fare]

features = train[["Pclass", "Age", "Fare", "Sex"]]
features = features.fillna(0)
features.head()


# In[ ]:


bins = [0, 6, 50, 80]
train['Age_cut'] = pd.cut(train['Age'], bins)
train[['Age_cut', 'Survived']].groupby(['Age_cut'], as_index=False).mean().sort_values(by='Survived', ascending=False)
test['Age_cut'] = pd.cut(test['Age'], bins)


# In[ ]:


features.values.reshape(-1,1)


# In[ ]:


train.Survived.fillna('-')


# In[ ]:


train.Survived.values.reshape(-1,1)


# In[ ]:


rfc.fit(features, train.Survived)


# In[ ]:


test.Age_cut
train.Age_cut = train.Age_cut.replace(pd.Interval(left=0, right=6), int(0))
train.Age_cut = train.Age_cut.replace(pd.Interval(left=6, right=50), int(1))
train.Age_cut = train.Age_cut.replace(pd.Interval(left=50, right=80), int(2))

test.Age_cut = test.Age_cut.replace(pd.Interval(left=0, right=6), int(0))

test.Age_cut = test.Age_cut.replace(pd.Interval(left=6, right=50), int(1))
test.Age_cut = test.Age_cut.replace(pd.Interval(left=50, right=80), int(2))

train.Age_cut


# In[ ]:


train.Age_cut.fillna(1)
test.fillna(1)


# In[ ]:





# 

# In[ ]:


prediction = rfc.predict(test[["Pclass", "Age_cut", "Fare", "Sex"]])


# In[ ]:


my_prediction = pd.DataFrame(prediction, test.PassengerId, columns = ["Survived"])


# In[ ]:


#forest gave us 72%, let's try xboost
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(features)
test_features = test[["Pclass", "Age", "Fare", "Sex"]]
scaler.fit(test_features)


# In[ ]:


x = GradientBoostingClassifier()
x.fit(features, train.Survived)


# In[ ]:





# In[ ]:





# In[ ]:


from sklearn import model_selection,metrics
from sklearn.metrics import confusion_matrix
import xgboost
from xgboost import plot_importance
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.model_selection import GridSearchCV


# In[ ]:


train_x, valid_x, train_y, valid_y = model_selection.train_test_split(features, train.Survived,
                                                                    test_size=0.25,stratify=train.Survived,random_state=0)
xgboost_model = xgboost.XGBClassifier(objective='binary:logistic',learning_rate=0.1)
eval_set = [(train_x,train_y),(valid_x,valid_y)]
xgboost_model.fit(train_x,train_y,eval_metric=['error','logloss','auc'],eval_set=eval_set,verbose=True)
xgboost_model.score(train_x,train_y)
pred_y = xgboost_model.predict(valid_x)
metrics.accuracy_score(valid_y,pred_y)


# In[ ]:


prediction = xgboost_model.predict(test_features)


# In[ ]:


#prediction = x.predict(test_features)
my_prediction = pd.DataFrame(prediction, test.PassengerId, columns = ["Survived"])


# In[ ]:


my_prediction.to_csv("my_prediction.csv", index_label = ["PassengerId"])


# In[ ]:


#let's see how it's working now


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




