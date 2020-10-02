#!/usr/bin/env python
# coding: utf-8

# # Importing Required Libraries

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
import sys
import pickle
from sklearn import preprocessing
from time import time
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
# from sklearn.grid_search import GridSearchCV
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import xgboost
import seaborn as sns

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import sys
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

sys.path.append('/kaggle/input/enron-project/')
from feature_format import featureFormat
from feature_format import targetFeatureSplit

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # Code to convert new line characters in unix

# In[ ]:


original = "/kaggle/input/enron-project/final_project_dataset.pkl"
destination = "final_project_dataset_unix.pkl"

content = ''
outsize = 0
with open(original, 'rb') as infile:
    content = infile.read()
with open(destination, 'wb') as output:
    for line in content.splitlines():
        outsize += len(line) + 1
        output.write(line + str.encode('\n'))
# data_dict


# # Loading the file and Removing the "TOTAL" key###

# In[ ]:


# with open("/kaggle/input/enron-project/final_project_dataset.pkl", 'rb') as f:
#     data_dict = pickle.load(f)

data_dict = pickle.load(open("/kaggle/input/enron-project/final_project_dataset_unix.pkl", 'rb') )

data_dict.pop('TOTAL')
abc = featureFormat(data_dict, ['poi','salary','total_payments'])
# featureFormat()
print("The number of people in the dataset:",len(data_dict))
print(list(data_dict.keys())[0],"\n",data_dict[list(data_dict.keys())[0]])

for key in range(len(abc)):
    if abc[key][1]<1000000:
        if abc[key][0]==True:
            plt.scatter(abc[key][1],abc[key][2],color = 'b')
        else:
            plt.scatter(abc[key][1],abc[key][2],color = 'r')
# plt.scatter(abc[:][0],abc[:][1])

plt.ylabel('tot_payments')
plt.xlabel('salary')   
plt.show()
plt.figure(figsize=(20,10))
sns.heatmap(pd.DataFrame(data_dict).T.dropna(how = 'all').replace({'NaN':0}).drop(['other'],axis = 1).corr(),vmin=-1,cmap='coolwarm')


# # Plotting graphs to see dependence on various factors

# In[ ]:


# plt.figure(figsize=(20,6))
abc2 = featureFormat(data_dict,['poi','salary','bonus'])
abc3 = featureFormat(data_dict,['poi','salary','total_payments','deferral_payments'])
abc4 = featureFormat(data_dict,['poi','salary','total_payments','deferred_income'])
abc5 =  featureFormat(data_dict,['poi','from_this_person_to_poi','from_poi_to_this_person'])
fig,a =  plt.subplots(2,2,squeeze=False,figsize=(17,10))
a[0][1].set(ylim=(0, 20000000))
a[1][0].set(ylim=(0, 20000000))
a[1][1].set(xlim=(0,210), ylim=(0,320))
for key in range(len(abc2)):
    if abc2[key][0] == True:
         a[0][0].scatter(abc2[key][1],abc2[key][2],color = 'b')
    else:
        a[0][0].scatter(abc2[key][1],abc2[key][2],color = 'r')
x = np.arange(0,1000000,0.1)
# a[0][0].ylabel('bonus')
# a[0][0].xlabel('salary')  
a[0][0].plot(x,x**1.07,'b')

n = 0
m = 0
for key in range(len(abc3)):
    if abc3[key][0] == True:
        m+=1
        if abc3[key][3]==0:
             a[0][1].plot(abc3[key][1],abc3[key][2],'b^')
             n+=1
        else:
            a[0][1].plot(abc3[key][1],abc3[key][2],'bo')
    else:
        if abc3[key][3]==0:
            a[0][1].plot(abc3[key][1],abc3[key][2],'r^')
        else:
            a[0][1].plot(abc3[key][1],abc3[key][2],'ro')

mm  = 0
nn = 0
for key in range(len(abc4)):
    if abc4[key][0] == True:
        mm+=1
        if abc4[key][3]==0:
             a[1][0].plot(abc4[key][1],abc4[key][2],'b^')
             nn+=1
        else:
            a[1][0].plot(abc4[key][1],abc4[key][2],'bo')
    else:
        if abc4[key][3]==0:
            a[1][0].plot(abc4[key][1],abc4[key][2],'r^')
        else:
            a[1][0].plot(abc4[key][1],abc4[key][2],'ro')

for key in range(len(abc5)):
    if abc5[key][0] == True:
         a[1][1].scatter(abc5[key][1],abc5[key][2],color = 'b')
    else:
        a[1][1].scatter(abc5[key][1],abc5[key][2],color = 'r')

print(n," out of ",m," poi have deffereal payments equal to 0"," & \n",nn," out of ",mm," poi have deffered income equal to 0")
plt.show()


# # Introduing new features 

# In[ ]:


def dict_to_list(key,normalizer):
    new_list=[]

    for i in data_dict:
        if data_dict[i][key]=="NaN" or data_dict[i][normalizer]=="NaN":
            new_list.append(0.)
        elif data_dict[i][key]>=0:
            new_list.append(float(data_dict[i][key])/float(data_dict[i][normalizer]))
    return new_list

fraction_from_poi_email=dict_to_list("from_poi_to_this_person","to_messages")
fraction_to_poi_email=dict_to_list("from_this_person_to_poi","from_messages")
j = 0
for i in data_dict:
    data_dict[i]["fraction_from_poi_email"]=fraction_from_poi_email[j]
    data_dict[i]["fraction_to_poi_email"]=fraction_to_poi_email[j]
    j+=1


# In[ ]:


features_list = ['poi','shared_receipt_with_poi','fraction_from_poi_email','fraction_to_poi_email']
features_list2 = ['poi','shared_receipt_with_poi','fraction_from_poi_email','fraction_to_poi_email','deferral_payments']
data = featureFormat(data_dict, features_list2)
value , features = targetFeatureSplit(data)

for key in range(len(data)):
    if abc[key][0]==True:
        plt.scatter(data[key][2],data[key][3],color = 'b')
    else:
        plt.scatter(data[key][2],data[key][3],color = 'r')
# plt.scatter(abc[:][0],abc[:][1])

plt.ylabel('fraction_to_poi_email')
plt.xlabel('fraction_from_poi_email')   
plt.show()
X_train, X_test, Y_train, Y_test = train_test_split(features, value, test_size = 0.1)


# ### Using different algorithms to fit the data

# In[ ]:


from sklearn.model_selection import StratifiedKFold,RandomizedSearchCV

from sklearn.metrics import f1_score

clf = xgboost.XGBClassifier()
reg = LogisticRegression()
reg2 = svm.SVC()
reg3 = RandomForestClassifier(max_depth=10, criterion = 'entropy')
model = AdaBoostClassifier(n_estimators=100,base_estimator = reg3)
# reg3.fit(X_train,Y_train)
# print(accuracy_score(Y_test, model.predict(X_test)))
# model.predict(X_test)


# # **Using Stratified K Fold to check accuracy for ADAboost**

# ### It can be cleary seen that the model does well in terms of f1-score

# In[ ]:


import warnings
warnings.filterwarnings('ignore')

model.fit(X_train,Y_train)
skf = StratifiedKFold(n_splits = 8)
f1 = np.array(features)
v1 = np.array(value)
acc = []
for train_index, test_index in skf.split(f1, v1):
    X1_train, X1_test = f1[train_index], f1[test_index]
    Y1_train, Y1_test = v1[train_index], v1[test_index]
    model.fit(X1_train,Y1_train)
    acc.append(accuracy_score(Y1_test,model.predict(X1_test)))
    print('weighted f1-score:',float(classification_report(np.array(Y1_test),np.array(model.predict(X1_test)))[311:315]))
print(acc)


# # Parameter Optimization for XGBoost 
# ### And then using Stratified KFold to see accuracy

# In[ ]:


parameters = {
    'learning_rate' : [0.2 , 0.3 , 0.5 , 0.6],
    'gamma' : [0, 0.2, 0.5, 0.8],
    'max_depth' : [3, 4, 6, 8, 10],
    'min_child_weight' : [0.5, 1, 2, 4, 6],
}

rnd_search = RandomizedSearchCV(clf,param_distributions=parameters,cv = 8,n_jobs = -1,scoring = 'accuracy')
rnd_search.fit(f1, v1)
clf2 = rnd_search.best_estimator_


# In[ ]:


acc2 = []
i = 0
for train_index, test_index in skf.split(f1, v1):
    X1_train, X1_test = f1[train_index], f1[test_index]
    Y1_train, Y1_test = v1[train_index], v1[test_index]
    clf2.fit(X1_train,Y1_train)
    acc2.append(accuracy_score(Y1_test,clf2.predict(X1_test)))
    print('weighted f1-score:',float(classification_report(np.array(Y1_test),np.array(clf2.predict(X1_test)))[311:315]))
    
print(acc2)


# # Parameter Optimization For RandomForestClassifier

# ### The parameters like number of estimators and max_depth has been optimized according to data

# In[ ]:


param = {
    'n_estimators' : [80 , 100 , 120 , 150],
    'max_depth' : [3, 4, 6, 8, 10],
    'min_samples_split' : [2, 3]
}
rnd = RandomizedSearchCV(reg3,param_distributions=param,cv = 8,n_jobs = -1,scoring = 'f1')
rnd.fit(f1,v1)
reg3_ = rnd.best_estimator_

acc3 = []
for train_index, test_index in skf.split(f1, v1):
    X2_train, X2_test = f1[train_index], f1[test_index]
    Y2_train, Y2_test = v1[train_index], v1[test_index]
    reg3_.fit(X2_train,Y2_train)
    acc3.append(accuracy_score(Y2_test,reg3_.predict(X2_test)))
    print('weighted f1-score:',float(classification_report(np.array(Y2_test),np.array(reg3_.predict(X2_test)))[311:315]))
    
print(acc3)


# # Using SVM to predict poi

# In[ ]:


acc4 = []
for train_index, test_index in skf.split(f1, v1):
    X3_train, X3_test = f1[train_index], f1[test_index]
    Y3_train, Y3_test = v1[train_index], v1[test_index]
    reg2.fit(X3_train,Y3_train)
    acc2.append(accuracy_score(Y3_test,reg2.predict(X3_test)))
    print('weighted f1-score:',float(classification_report(np.array(Y3_test),np.array(reg2.predict(X3_test)))[311:315]))
    
print(acc3)


# # Outputting the data as a pickle file
# 
# ### As can be noticed after parameter optimization, XGBoost performs slightly better than ADAboost with Random Forest Classifier

# In[ ]:


pickle.dump(clf2, open("my_classifier.pkl", "wb") )
pickle.dump(data_dict, open("my_dataset.pkl", "wb") )
pickle.dump(features_list2, open("my_feature_list.pkl", "wb") )


# In[ ]:




