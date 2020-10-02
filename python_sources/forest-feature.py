#!/usr/bin/env python
# coding: utf-8

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


train_data = pd.read_csv("../input/learn-together/train.csv", index_col='Id')
train_data.sample(5)


# In[ ]:


test_data = pd.read_csv("../input/learn-together/test.csv", index_col='Id')
test_data.shape


# In[ ]:


soils = [
    [7, 15, 8, 14, 16, 17,
     19, 20, 21, 23], 
    [3, 4, 5, 10, 11, 13],   
    [6, 12],   
    [2, 9, 18, 26],      
    [1, 24, 25, 27, 28, 29, 30,
     31, 32, 33, 34, 36, 37, 38, 
     39, 40, 22, 35], ]


# In[ ]:


soil_dict = dict()
for index, values in enumerate(soils):
    for v in values:
        soil_dict[v] = index


# In[ ]:


family= [[1], [2,6,7, 8, 9, 15, 26], [3, 4, 5], [10, 11, 13], [12],[14], 
         [16, 17, 19], [18], [20, 21, 23], [22, 24, 25, 27, 28, 31, 38], 
         [29, 30], [32, 33], [34, 39, 40], [35, 36, 37]]


# In[ ]:


family_dict = dict()
for index, values in enumerate(family):
    for v in values:
        family_dict[v] = index


# In[ ]:


def family(df, family_dict=family_dict):
    df['family'] =  sum(i * df['Soil_Type'+ str(i)] for i in range(1, 41))
    df['family'] = df['family'].map(family_dict) 
    df['Rocky'] =  sum(i * df['Soil_Type'+ str(i)] for i in range(1, 41))
    df['Rocky'] = df['Rocky'].map(soil_dict) 
    return df


# In[ ]:


train = family(train_data)


# In[ ]:


test= family(test_data)


# In[ ]:


test.shape


# In[ ]:


train.shape


# In[ ]:


train.columns


# In[ ]:


def interaction(series1, series2):
    interactions = (series1).astype(str) + "_" + series2.astype(str)
    labels, uniques = pd.factorize(interactions)
    return labels
    


# In[ ]:



y= train['Cover_Type']
train= train.drop(['Cover_Type'], axis= 1)


# In[ ]:


total= pd.concat([train, test], keys= ['train', 'test'])


# In[ ]:


total['aspect_slope']= interaction(total.Aspect, total.Slope)


# In[ ]:


total['horizontal_vertical']= interaction(total['Horizontal_Distance_To_Hydrology'], total['Vertical_Distance_To_Hydrology'])


# In[ ]:


total['hydrology_fire']= interaction(total['Horizontal_Distance_To_Hydrology'], total['Horizontal_Distance_To_Fire_Points'])


# In[ ]:


total['9am_Noon']= interaction(total['Hillshade_9am'], total['Hillshade_Noon'])


# In[ ]:


total['3pm_Noon']= interaction(total['Hillshade_3pm'], total['Hillshade_Noon'])


# In[ ]:


total['9am_3pm']= interaction(total['Hillshade_9am'], total['Hillshade_3pm'])


# In[ ]:


listk= ['Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
       'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
       'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
       'Horizontal_Distance_To_Fire_Points']


# In[ ]:


from sklearn.preprocessing import LabelEncoder


# In[ ]:


for col in listk:
    label_enc = LabelEncoder()
    total[col+'new'] = label_enc.fit_transform(total[col].astype(str))


# In[ ]:


#total['elevationbin']= pd.cut(total['Elevation'], 8)


# In[ ]:


train= total.loc['train']


# In[ ]:


test= total.loc['test']


# In[ ]:


test.shape


# In[ ]:


train.shape


# In[ ]:


#def number(df):
    #for col in listk:
        #label_enc = LabelEncoder()
        #df[col+'new'] = label_enc.fit_transform(df[col].astype(str))
        
        #return df
    
    


# In[ ]:


#train= number(train)


# In[ ]:


#test= number(test)


# In[ ]:


#test


# In[ ]:


train.columns


# Finding important variables using permutation method.

# In[ ]:


from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score


# In[ ]:


#train= train.fillna(method= 'ffill')


# In[ ]:


train.isnull().sum()[train.isnull().sum() > 0]


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:



plt.hist('Horizontal_Distance_To_Roadways', data= train)
plt.show()


# In[ ]:


plt.hist('Horizontal_Distance_To_Roadways', data= test)
plt.show()


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(train, y, test_size = 0.2, random_state = 21)


# In[ ]:


classifier = RandomForestClassifier(max_depth=3, n_estimators=650)
classifier.fit(X_train, y_train)


# In[ ]:


import eli5
from eli5.sklearn import PermutationImportance


# In[ ]:


perm = PermutationImportance(classifier, random_state=1).fit(X_test, y_test)
eli5.show_weights(perm, feature_names = X_test.columns.tolist())


# In[ ]:


from sklearn.metrics import f1_score
y_pred = classifier.predict(X_test)
f1_score(y_test, y_pred, average='macro')  

f1_score(y_test, y_pred, average='micro')  

f1_score(y_test, y_pred, average='weighted')  

f1_score(y_test, y_pred, average=None)


# In[ ]:


plt.hist('Elevation', data= train)
plt.show()


# In[ ]:


plt.hist('Elevation', data= test)
plt.show()


# In[ ]:


total['elevationbin']= pd.cut(total['Elevation'], 8, labels= ['best', 'very good', 'good', 'not good', 'medium', 'bad', 'very bad', 'worst'])


# In[ ]:


label_enc = LabelEncoder()
total['elevationnumber'] = label_enc.fit_transform(total['elevationbin'])


# In[ ]:


pd.get_dummies(train, prefix_sep='_', drop_first=True)


# In[ ]:


train= total.loc['train']
test= total.loc['test']


# In[ ]:


train= pd.get_dummies(train, prefix_sep='_', drop_first=True)


# In[ ]:


test= pd.get_dummies(test, prefix_sep='_', drop_first=True)


# In[ ]:


train.head()


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(train, y, test_size = 0.2, random_state = 21)


# In[ ]:


classifier = RandomForestClassifier(max_depth=None, n_estimators=1000, min_samples_split=2, max_features="sqrt", n_jobs=-1)
classifier.fit(X_train, y_train)


# In[ ]:


perm = PermutationImportance(classifier, random_state=1).fit(X_test, y_test)
eli5.show_weights(perm, feature_names = X_test.columns.tolist())


# In[ ]:


from sklearn.metrics import f1_score
y_pred = classifier.predict(X_test)
f1_score(y_test, y_pred, average='macro')  

f1_score(y_test, y_pred, average='micro')  

f1_score(y_test, y_pred, average='weighted')  

f1_score(y_test, y_pred, average=None)


# In[ ]:


from sklearn import model_selection 
from sklearn.ensemble import BaggingClassifier 
from sklearn.tree import DecisionTreeClassifier 


# In[ ]:


kfold = model_selection.KFold(n_splits = 3, 
                       random_state = 10) 
  
# initialize the base classifier 
base_cls = DecisionTreeClassifier() 
  
# no. of base classifier 
num_trees = 500
  
# bagging classifier 
model = BaggingClassifier(base_estimator = base_cls, n_estimators = num_trees, 
                                      random_state = 10) 
  
results = model_selection.cross_val_score(model, X_train, y_train, cv = kfold) 
print("accuracy :") 
print(results.mean()) 


# In[ ]:


from sklearn.metrics import f1_score
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
f1_score(y_test, y_pred, average='macro')  

f1_score(y_test, y_pred, average='micro')  

f1_score(y_test, y_pred, average='weighted')  

f1_score(y_test, y_pred, average=None)


# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier


# In[ ]:


from sklearn.model_selection import cross_val_score


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier


# In[ ]:


clf1 = DecisionTreeClassifier()
clf2 = RandomForestClassifier(max_depth=None, n_estimators=1000, min_samples_split=2, max_features="sqrt", n_jobs=-1)


eclf = VotingClassifier(estimators=[('dt', clf1), ('rf', clf2)], voting='soft', weights=[1, 2])

for clf, label in zip([clf1, clf2, eclf], ['decision tree', 'Random Forest', 'Ensemble']):
    scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))


# In[ ]:


eclf.fit(X_train, y_train)
y_pred = eclf.predict(X_test)
f1_score(y_test, y_pred, average='macro')  

f1_score(y_test, y_pred, average='micro')  

f1_score(y_test, y_pred, average='weighted')  

f1_score(y_test, y_pred, average=None)


# In[ ]:


classifier = RandomForestClassifier(max_depth=None, n_estimators=1000, min_samples_split=2, max_features="sqrt", n_jobs=-1)
classifier.fit(train, y)


# In[ ]:


rfc_predict = classifier.predict(test)


# In[ ]:


submission= pd.read_csv('../input/learn-together/sample_submission.csv', index_col= 'Id')
submission['Cover_Type']= list(rfc_predict)
submission['Cover_Type'].value_counts()


# In[ ]:


submission.to_csv('submission.csv')

