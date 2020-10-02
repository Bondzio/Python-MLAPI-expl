#!/usr/bin/env python
# coding: utf-8

# * Problem statement* 
# 
# 
#   Given the data on the forest cover type can be analyzed to predict what type of forest or tree will arise
#   in a specific area.
#  
#  

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn import ensemble
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas_profiling

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib
matplotlib.__version__


# In[ ]:


data_train=pd.read_csv('/kaggle/input/learn-together/train.csv')
data_test=pd.read_csv('/kaggle/input/learn-together/test.csv')


# In[ ]:


print("train data:",data_train.shape, "test data:",data_test.shape)


# In[ ]:


profile = data_train.profile_report(title='Pandas Profiling Report')


# In[ ]:


profile


# *  Above Profile shows all the details about the data.

# * Below boxplots are for only numeric columns to check the outliers

# In[ ]:


for column in data_train.iloc[:,1:11]:
    plt.figure()
    data_train.boxplot([column],sym='k.')


# * By looking at the boxplots .It clearly shows there are outliers in the data.Except for Elevation and Aspect.

# In[ ]:


data_train.iloc[:, 2:11].hist(figsize=(16, 12), bins=50)


# Above plots depict the spread of data 

# In[ ]:


def r(x):
    if x + 180 > 360:
        return x - 180
    else:
        return x + 180


# In[ ]:


data_train['Aspect2'] = data_train.Aspect.map(r)
data_test['Aspect2'] = data_test.Aspect.map(r)


# Angle of the Aspect
# 

# In[ ]:


data_train['Highwater']=data_train.Vertical_Distance_To_Hydrology < 0
data_test['Highwater'] = data_test.Vertical_Distance_To_Hydrology < 0


# Depth of the hydrology or water

# In[ ]:


def plotc(c1, c2):
    fig = plt.figure(figsize=(16, 8))
    sel = np.array(list(data_train.Cover_Type.values))

    plt.scatter(c1, c2, c=sel, cmap=plt.cm.jet,s=100)
    plt.xlabel(c1.name)
    plt.ylabel(c2.name)
    plt.show()


# In[ ]:


plotc(data_train.Elevation, data_train.Vertical_Distance_To_Hydrology)


# Above plot clearly shows there are observations of vertical distance to hydrology which are negative.

# In[ ]:


plotc(data_train.Elevation-data_train.Vertical_Distance_To_Hydrology, data_train.Vertical_Distance_To_Hydrology)


# In[ ]:


data_train['EVDtH'] = data_train.Elevation - data_train.Vertical_Distance_To_Hydrology
data_test['EVDtH'] = data_test.Elevation - data_test.Vertical_Distance_To_Hydrology


# In[ ]:


data_train['EHDtH'] = data_train.Elevation - data_train.Horizontal_Distance_To_Hydrology * 0.2
data_test['EHDtH'] = data_test.Elevation - data_test.Horizontal_Distance_To_Hydrology * 0.2


# * Below calculation is to calculate the distance of the hydrology ,the formaula used is hypotenuse = sqrt(a2+b2).

# In[ ]:


data_train['Distance_to_Hydrology'] = (data_train['Horizontal_Distance_To_Hydrology'] ** 2 + data_train[
    'Vertical_Distance_To_Hydrology'] ** 2) ** 0.5
data_test['Distance_to_Hydrology'] = (data_test['Horizontal_Distance_To_Hydrology'] ** 2 + data_test[
    'Vertical_Distance_To_Hydrology'] ** 2) ** 0.5


# * Below calculations are to calculate the distance between the hydrology and fire points,hydrology and 
#   road ways,fire points and road ways
# 

# In[ ]:


data_train['Hydro_Fire_1'] = data_train['Horizontal_Distance_To_Hydrology'] + data_train['Horizontal_Distance_To_Fire_Points']
data_test['Hydro_Fire_1'] = data_test['Horizontal_Distance_To_Hydrology'] + data_test['Horizontal_Distance_To_Fire_Points']

data_train['Hydro_Fire_2'] = abs(data_train['Horizontal_Distance_To_Hydrology'] - data_train['Horizontal_Distance_To_Fire_Points'])
data_test['Hydro_Fire_2'] = abs(data_test['Horizontal_Distance_To_Hydrology'] - data_test['Horizontal_Distance_To_Fire_Points'])

data_train['Hydro_Road_1'] = abs(data_train['Horizontal_Distance_To_Hydrology'] + data_train['Horizontal_Distance_To_Roadways'])
data_test['Hydro_Road_1'] = abs(data_test['Horizontal_Distance_To_Hydrology'] + data_test['Horizontal_Distance_To_Roadways'])

data_train['Hydro_Road_2'] = abs(data_train['Horizontal_Distance_To_Hydrology'] - data_train['Horizontal_Distance_To_Roadways'])
data_test['Hydro_Road_2'] = abs(data_test['Horizontal_Distance_To_Hydrology'] - data_test['Horizontal_Distance_To_Roadways'])

data_train['Fire_Road_1'] = abs(data_train['Horizontal_Distance_To_Fire_Points'] + data_train['Horizontal_Distance_To_Roadways'])
data_test['Fire_Road_1'] = abs(data_test['Horizontal_Distance_To_Fire_Points'] + data_test['Horizontal_Distance_To_Roadways'])

data_train['Fire_Road_2'] = abs(data_train['Horizontal_Distance_To_Fire_Points'] - data_train['Horizontal_Distance_To_Roadways'])
data_test['Fire_Road_2'] = abs(data_test['Horizontal_Distance_To_Fire_Points'] - data_test['Horizontal_Distance_To_Roadways'])


# In[ ]:


feature_cols = [col for col in data_train.columns if col not in ['Cover_Type', 'Id']]


# In[ ]:


features = data_train[feature_cols]
features_test = data_test[feature_cols]
target = data_train['Cover_Type']
test_ids = data_test['Id']


# In[ ]:


from bayes_opt import BayesianOptimization
from sklearn.model_selection import train_test_split


# In[ ]:


X_train,X_test,y_train,y_test =train_test_split(features,target,test_size=0.3,random_state=0,stratify=target)


# In[ ]:


#Bayesian optimization
def bayesian_optimization(dataset, function, parameters):
   X_train, y_train, X_test, y_test = dataset
   n_iterations = 5
   gp_params = {"alpha": 1e-4}

   BO = BayesianOptimization(function, parameters)
   BO.maximize(n_iter=n_iterations, **gp_params)

   return BO.max


# In[ ]:


def rfc_optimization(cv_splits):
    def function(n_estimators, max_depth, min_samples_split):
        return cross_val_score(
               RandomForestClassifier(
                   n_estimators=int(max(n_estimators,0)),                                                               
                   max_depth=int(max(max_depth,1)),
                   min_samples_split=int(max(min_samples_split,2)), 
                   n_jobs=-1, 
                   random_state=42,   
                   class_weight="balanced"),  
               X=X_train, 
               y=y_train, 
               cv=cv_splits,
               #scoring="roc_auc",
               n_jobs=-1).mean()

    parameters = {"n_estimators": (10, 1000),
                  "max_depth": (1, 150),
                  "min_samples_split": (2, 10)}
    
    return function, parameters


# In[ ]:


def train(X_train, y_train, X_test, y_test, function, parameters):
    dataset = (X_train, y_train, X_test, y_test)
    cv_splits = 4
    
    best_solution = bayesian_optimization(dataset, function, parameters)      
    params = best_solution["params"]

    model = RandomForestClassifier(
             n_estimators=int(max(params["n_estimators"], 0)),
             max_depth=int(max(params["max_depth"], 1)),
             min_samples_split=int(max(params["min_samples_split"], 2)), 
             n_jobs=-1, 
             random_state=42,   
             class_weight="balanced")

    model.fit(X_train, y_train)
    
    return model


# In[ ]:


function,parameters = rfc_optimization(4)


# In[ ]:


from sklearn.model_selection import cross_val_score

from sklearn.ensemble import RandomForestClassifier


# In[ ]:


classifier = train(X_train, y_train, X_test, y_test, function, parameters)


# In[ ]:


y_pred = classifier.predict(X_test)
from sklearn.metrics import confusion_matrix,accuracy_score
cm = confusion_matrix(y_test, y_pred)
accuracy_score=accuracy_score(y_test,y_pred )
accuracy_score


# In[ ]:


test_pred=classifier.predict(features_test)


# In[ ]:


sel = np.array(list(data_train.Cover_Type.values))
sel1=np.unique(sel)
data_train.groupby('Cover_Type').count()[['Id']].plot.pie(subplots=True,radius = 2, autopct = '%1.1f%%')
plt.legend(sel1,loc='upper center')
plt.title("Cover Type distributions")
plt.show()


# In[ ]:


output = pd.DataFrame({'Id':data_test.Id, 
                       'Cover_Type': test_pred})


# In[ ]:


sel = np.array(list(output.Cover_Type.values))
sel1=np.unique(sel)
output.groupby('Cover_Type').count()[['Id']].plot.pie(subplots=True,radius = 2, autopct = '%1.1f%%')
plt.legend(sel1,loc='upper center')
plt.title("Cover Type distributions")
plt.show()


# In[ ]:


output.to_csv('submission.csv', index=False)


# *  References
# 
# * [https://douglas-fraser.com/forest_cover_management.pdf]
# * Feature Engineering
# * [https://github.com/jaustinrdi/kaggle/blob/master/kaggle_forest/guschin_example.py#L64]
# 
# More to enhance......................
