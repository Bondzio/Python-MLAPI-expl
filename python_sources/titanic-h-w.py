#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


train = pd.read_csv("../input/titanic/train.csv")
test = pd.read_csv("../input/titanic/test.csv")


# In[ ]:


train.info()


# In[ ]:


train.head()


# In[ ]:


#Drop Columns that has no relevance for Data Analysis Purposes
train_revized=train.drop(['PassengerId','Name','Ticket','Cabin'],axis=1)


# In[ ]:


train_revized.info()


# In[ ]:


train_revized_final=train_revized.drop(train_revized[train_revized.Embarked.isnull()].index)
train_revized_final.info()


# In[ ]:


train_revized_final.Age.fillna(train_revized_final.Age.mean(),inplace=True)


# In[ ]:


train_revized_final.info()


# In[ ]:


train_revized_final.info()


# In[ ]:


sns.pairplot(train_revized_final,hue='Pclass')


# In[ ]:


sns.distplot(train_revized_final.Age,kde=False);


# In[ ]:


train_revized_final.Age.hist()


# In[ ]:


pd.plotting.scatter_matrix(train_revized_final, alpha=0.5, figsize=(16, 16));


# In[ ]:


fig,(axis1,axis2) = plt.subplots(1,2,figsize=(18,6))

sns.barplot(x = 'Sex', y = 'Survived', order=['female','male'],data=train_revized_final, ax = axis1);
axis1.set_title('w.r.t Sex');

sns.barplot(x = 'Pclass', y = 'Survived', data=train_revized_final, ax = axis2);
axis2.set_title('w.r.t class');


# In[ ]:


deneme=train_revized_final[train_revized_final.Sex=='male']


# In[ ]:


deneme.Survived.mean()


# In[ ]:


fig,(axis1,axis2)=plt.subplots(1,2,figsize=(18,6))

sns.barplot('SibSp',y='Survived',data=train_revized_final,ax=axis1);
axis1.set_title('Survival Rate w.r.t Sibling & Spouses');

sns.barplot('Parch', y='Survived', data=train_revized_final,ax=axis2);
axis2.set_title('Survival rate w.r.t parents & Children');


# In[ ]:


fig,(axis3,axis4) = plt.subplots(1,2,figsize=(18,6))

sns.distplot(train_revized_final[train_revized_final['Survived']==0].Age,kde=False,ax=axis3);
axis3.set_title('Age dist for Not Survived');

sns.distplot(train_revized_final[train_revized_final['Survived']==1].Age,kde=False,ax=axis4);
axis4.set_title('Age dist for Survived');


# In[ ]:


fig,(axis1,axis2)=plt.subplots(1,2,figsize=(18,6));
sns.distplot(train_revized_final[train_revized_final['Survived']==0].Fare,kde=False,ax=axis1,color='orange',hist_kws={"alpha": 1});
sns.distplot(train_revized_final[train_revized_final['Survived']==1].Fare,kde=False,ax=axis2,color='orange',hist_kws={"alpha": 1});
axis1.set_title('did not survive');
axis2.set_title('survived');


# In[ ]:


print('Average Ticket Fare for those who did not survive is: ' + str(train_revized_final.groupby('Survived').Fare.mean().values[0]))
print('Average Ticket Fare for those who survived is: ' + str(train_revized_final.groupby('Survived').Fare.mean().values[1]))


# In[ ]:


train_revized_final.Fare.mean()


# In[ ]:


train_revized_final.groupby('Survived').Fare.mean()


# In[ ]:


correlation=train_revized_final.corr()
fig,axis1=plt.subplots(1,1,figsize=(8,8));
sns.heatmap(correlation,cmap=sns.diverging_palette(20, 220, n=200),ax=axis1);
axis1.set_title('Correlation Matrix');


# In[ ]:


fig, (axis1,axis2) =plt.subplots(1,2,figsize=(18,8));
sns.boxplot(y='Age', x='Pclass',data=train_revized_final,ax=axis1);
axis1.set_title('Age dist w.r.t Class');

sns.boxplot(y='Fare', x='Pclass',data=train_revized_final,ax=axis2);
axis2.set_title('Fare dist w.r.t Class');


# In[ ]:


from sklearn.preprocessing import OneHotEncoder
onehot_encoder = OneHotEncoder(sparse=False)


# In[ ]:


copy_df=train_revized_final.copy()
train_Embarked = copy_df["Embarked"].reshape(-1,1)
train_OneHotEncoded = onehot_encoder.fit_transform(train_Embarked)

