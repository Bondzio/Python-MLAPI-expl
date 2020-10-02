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
import matplotlib.pyplot as plt
import seaborn as sns

# Any results you write to the current directory are saved as output.


# In[ ]:


train=pd.read_csv('../input/train_LZdllcl.csv')
test=pd.read_csv('../input/test_2umaH9m.csv')
sample=pd.read_csv('../input/sample_submission_M0L0uXE.csv')


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


sample.head()


# In[ ]:


train.shape
#test.shape


# In[ ]:


train.describe()


# In[ ]:


test.describe()


# what i have seen so far  is we have some missing values of previous_year_rating so fill the missing values with mean.

# In[ ]:


train['previous_year_rating']=train['previous_year_rating'].fillna(train['previous_year_rating'].mean())


# In[ ]:


test['previous_year_rating']=test['previous_year_rating'].fillna(train['previous_year_rating'].mean())


# In[ ]:


train.describe()
#test.describe()


# In[ ]:


train['not_promoted']=1-train['is_promoted']


# In[ ]:


train.groupby('gender').agg('sum')[['is_promoted','not_promoted']].plot(kind='bar',figsize=(25,12),color=['g','r'],stacked=True)


# In[ ]:


train.groupby('gender').agg('mean')[['is_promoted','not_promoted']].plot(kind='bar',figsize=(25,12),color=['g','r'])


# it is observed that most people are not promoted

# In[ ]:


fig = plt.figure(figsize=(25, 7))
sns.violinplot(x='education', y='age', 
               hue='is_promoted', data=train, 
               split=True,
               palette={0: "r", 1: "g"}
              );


# In[ ]:


#from sklearn.preprocessing import LabelEncoder, OneHotEncoder
#labelencoder_X = LabelEncoder()
#train.iloc[:,3] = labelencoder_X.fit_tranform(train.iloc[:,3])


# In[ ]:


figure = plt.figure(figsize=(25,7))
plt.hist([train[train['is_promoted']==1]['length_of_service'],train[train['is_promoted']==0]['length_of_service']],stacked=True,color = ['g','r'],
        bins=50,label = ['is_promoted','not_promoted'])
plt.xlabel('length_of_service')
plt.ylabel('no of employee')
plt.legend();


# In[ ]:


figure = plt.figure(figsize=(25, 7))
plt.hist([train[train['is_promoted'] == 1]['age'], train[train['is_promoted'] == 0]['age']], 
         stacked=True, color = ['g','r'],
         bins = 50, label = ['is_promoted','not_promoted'])
plt.xlabel('age')
plt.ylabel('number of employees')
plt.legend();


# In[ ]:


figure = plt.figure(figsize=(25, 7))
plt.hist([train[train['is_promoted'] == 1]['previous_year_rating'], train[train['is_promoted'] == 0]['previous_year_rating']], 
         stacked=True, color = ['g','r'],
         bins = 50, label = ['is_promoted','not_promoted'])
plt.xlabel('previous year rating')
plt.ylabel('number of employees')
plt.legend();


# In[ ]:


figure = plt.figure(figsize=(25, 7))
plt.hist([train[train['is_promoted'] == 1]['no_of_trainings'], train[train['is_promoted'] == 0]['no_of_trainings']], 
         stacked=True, color = ['g','r'],
         bins = 50, label = ['is_promoted','not_promoted'])
plt.xlabel('no of training')
plt.ylabel('number of employees')
plt.legend();


# In[ ]:


figure=plt.figure(figsize=(25,7))
plt.hist([train[train['is_promoted']==1]['KPIs_met >80%'],train[train['is_promoted'] == 0]['KPIs_met >80%']],stacked=True,
         color = ['g','r'])
plt.xlabel('KP1')
plt.ylabel('no of employee')
plt.legend();


# In[ ]:


figure=plt.figure(figsize=(25,7))
plt.hist([train[train['is_promoted']==1]['length_of_service'],train[train['is_promoted'] == 0]['length_of_service']],stacked=True,
         color = ['g','r'])
plt.xlabel('length_of_service')
plt.ylabel('no of employee')
plt.legend();


# In[ ]:


figure=plt.figure(figsize=(25,7))
plt.hist([train[train['is_promoted']==1]['awards_won?'],train[train['is_promoted'] == 0]['awards_won?']],stacked=True,
         color = ['g','r'])
plt.xlabel('awards_won')
plt.ylabel('no of employee')
plt.legend();


# In[ ]:


figure=plt.figure(figsize=(25,7))
plt.hist([train[train['is_promoted']==1]['avg_training_score'],train[train['is_promoted'] == 0]['avg_training_score']],stacked=True,
         color = ['g','r'])
plt.xlabel('avg_training_score')
plt.ylabel('no of employee')
plt.legend();


# here we can say that people who have 95% or more avg_training_score  must have be promoted

# In[ ]:


train['region'].describe()


# #**Feature Engineering**

# In[ ]:


def get_combined_data():
    train=pd.read_csv('../input/train_LZdllcl.csv')
    test=pd.read_csv('../input/test_2umaH9m.csv')
    targets=train.is_promoted
    train.drop(['is_promoted'],1,inplace=True)
    #train.shape
    combined = train.append(test)
    combined.reset_index(inplace=True)
    return combined


# In[ ]:


combined=get_combined_data()


# In[ ]:


combined.head()


# In[ ]:


combined.describe()


# In[ ]:


combined['previous_year_rating']=combined['previous_year_rating'].fillna(combined['previous_year_rating'].mean())


# In[ ]:


combined.describe()


# In[ ]:


df=pd.get_dummies(combined['gender'])
df.head()


# In[ ]:


combined=pd.concat([combined,df],axis=1)


# In[ ]:


combined.head()


# In[ ]:


combined=combined.drop('gender',axis=1)
combined.head()


# In[ ]:


df=pd.get_dummies(combined['education'])
df.head()


# In[ ]:


combined=pd.concat([combined,df],axis=1)


# In[ ]:


combined=combined.drop('education',axis=1)


# In[ ]:


df=pd.get_dummies(combined['department'])
combined=pd.concat([combined,df],axis=1)

combined.head()


# In[ ]:


combined=combined.drop('department',axis=1)


# In[ ]:


combined.head()


# In[ ]:


df=pd.get_dummies(combined['recruitment_channel'])
combined = pd.concat([combined,df],axis=1)
combined=combined.drop('recruitment_channel',axis=1)
combined.head()


# In[ ]:


#df=pd.get_dummies(combined['region'])
#combined = pd.concat([combined,df],axis=1)
combined = combined.drop('region',axis=1)
combined.head()


# In[ ]:


combined['age']=pd.qcut(combined['age'],8,labels=['age1','age2','age3','age4','age5','age6','age7','age8'])
combined=pd.concat([combined,pd.get_dummies(combined['age'])],axis=1)
combined.head()


# In[ ]:


combined=combined.drop('age',axis=1)


# In[ ]:


combined.head()


# In[ ]:


combined['avg_training_score']=pd.qcut(combined['avg_training_score'],12,labels=['avg_training_score1','avg_training_score2','avg_training_score3','avg_training_score4',
                                                                                'avg_training_score5','avg_training_score6','avg_training_score7','avg_training_score8','avg_training_score9',
                                                                                'avg_training_score10','avg_training_score11','avg_training_score12'])


# In[ ]:


combined=pd.concat([combined,pd.get_dummies(combined['avg_training_score'])],axis=1)
combined.head()


# In[ ]:


combined=combined.drop('avg_training_score',axis=1)
combined.head()


# In[ ]:


combined.shape


# In[ ]:


#combined['length_of_service']=pd.qcut(combined['length_of_service'],34,labels=['length_of_service1','length_of_service2','length_of_service3','length_of_service4',
 ##                                                                            'length_of_service9','length_of_service10','length_of_service11','length_of_service12',
   #                                                                           'length_of_service13','length_of_service14','length_of_service15','length_of_service16',
    #                                                                          'length_of_service17','length_of_service18','length_of_service19','length_of_service20',
     #                                                                         'length_of_service21','length_of_service22','length_of_service23','length_of_service24',
      #                                                                        'length_of_service25','length_of_service26','length_of_service27','length_of_service28',
       #                                                                       'length_of_service29','length_of_service30','length_of_service31','length_of_service32',
        #                                                                     'length_of_service33','length_of_service34'],duplicates='drop')
#combined=pd.concat([combined,pd.get_dummies(combined['length_of_service'])],axis=1)
#combined.head()


# In[ ]:


x_train=combined.iloc[:54808]
y_train=pd.DataFrame(train['is_promoted'])
y_train.shape


# In[ ]:


from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier


# In[ ]:


x_test=combined.iloc[54808:]


# In[ ]:


x_test.shape


# In[ ]:


from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(x_train,y_train,test_size=0.3)


# In[ ]:


#clfd=XGBClassifier()
#clfd.fit(x_train,y_train)
clfd=RandomForestClassifier()
clfd.fit(X_train,Y_train)


# In[ ]:


features = pd.DataFrame()
features['feature'] = x_train.columns
features['importance'] = clfd.feature_importances_
features.sort_values(by=['importance'], ascending=True, inplace=True)
features.set_index('feature', inplace=True)


# In[ ]:


features.plot(kind='barh',figsize=(150,150))
plt.legend()


# In[ ]:


print(features.sort_values(by=['importance']))


# In[ ]:


#combined.drop(['region_18','region_34','region_9','region_33','region_33','region_'])


# In[ ]:


predict=clfd.predict(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix,classification_report


# In[ ]:


print(confusion_matrix(Y_test,predict))
print(classification_report(Y_test,predict))


# In[ ]:


#from sklearn.model_selection import StratifiedKFold
#skf = StratifiedKFold(n_splits=5, random_state=None)
# X is the feature set and y is the target
#for train_index, test_index in skf.split(x_train,y_train): 
    #print("Train:", train_index, "Validation:", test_index) 
   # X_train, X_test = x_train[train_index], x_train[test_index] 
   # y_train, y_test = y_train[train_index], y_train[test_index]


# In[ ]:


predict1=clfd.predict(x_test)


# In[ ]:


sample['is_promoted']=pd.DataFrame(predict1)


# In[ ]:


sample.head()


# In[ ]:


sample.to_csv('submission.csv',index=False)


# In[ ]:




