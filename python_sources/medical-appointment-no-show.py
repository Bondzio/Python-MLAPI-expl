#!/usr/bin/env python
# coding: utf-8

# # import libraries

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,accuracy_score,roc_curve,roc_auc_score,classification_report
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sms
from sklearn.preprocessing import StandardScaler,LabelEncoder


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


# In[ ]:


from imblearn.under_sampling import NearMiss
from imblearn.over_sampling import SMOTE
import statsmodels.api as sms
import warnings
warnings.filterwarnings("ignore")


# # load datasets

# In[ ]:


medical = pd.read_csv('../input/noshowappointments/KaggleV2-May-2016.csv',parse_dates=['ScheduledDay','AppointmentDay'])
medical.head()


# In[ ]:


medical.info()


# # data cleaning

# In[ ]:


medical['appoint_gap_days'] = medical['ScheduledDay'].dt.day - medical['AppointmentDay'].dt.day


# In[ ]:


medical[medical.appoint_gap_days < 0]['appoint_gap_days'].values


# In[ ]:


collist = medical[medical.appoint_gap_days < 0].index
collist


# In[ ]:


medical.loc[collist,'appoint_gap_days'] = 0


# In[ ]:


medical['appoint_month'] = medical['ScheduledDay'].dt.month


# In[ ]:


medical['No-show'].value_counts()


# In[ ]:


medical['No-show'] = medical['No-show'].map({'Yes':1,'No':0})


# # Encoding

# In[ ]:


le = LabelEncoder()


# In[ ]:


medical['Gender'] = le.fit_transform(medical['Gender'])


# In[ ]:


medical['Neighbourhood'] = le.fit_transform(medical['Neighbourhood'])


# # Scaling

# In[ ]:


sc = StandardScaler()


# In[ ]:


scaledData = pd.DataFrame(sc.fit_transform(medical.drop(['AppointmentID','ScheduledDay','AppointmentDay','No-show'],axis=1)),columns=medical.drop(['AppointmentID','ScheduledDay','AppointmentDay','No-show'],axis=1).columns)
scaledData.head()


# # Train test split

# In[ ]:


x = scaledData.drop(['PatientId','Gender'],axis=1)
y = medical['No-show']


# In[ ]:


xtrain,xtest,ytrain,ytest = train_test_split(x,y,random_state=32)


# # Apply model

# In[ ]:


lor = LogisticRegression()
dt = DecisionTreeClassifier(criterion = 'gini', max_depth= 2, max_features= 'auto')
rf = RandomForestClassifier(bootstrap= True, criterion='gini', max_depth= 2, max_features= 'auto')
knn = KNeighborsClassifier()
nb =GaussianNB()
#svm = SVC()


# In[ ]:


mobj = [lor,dt,rf,knn,nb]
mname = ['LogisticRegression','DecisionTreeClassifier','RandomForestClassifier','KNeighborsClassifier','GaussianNB']


# In[ ]:


for obj,name in zip(mobj,mname):
    obj.fit(xtrain,ytrain)
    ypred = obj.predict(xtest)
    print('\n***',name,'*** \n')
    print('accuracy_score \n',accuracy_score(ytest,ypred))
    print('confusion_matrix \n',confusion_matrix(ytest,ypred))
    print('classification_report \n',classification_report(ytest,ypred))


# # Parameter Tuning

# In[ ]:


param_dt = {
    'max_depth': [2, 3, 4],
    'max_features': ['auto', 'sqrt', 'log2'],
    'criterion': ['gini', 'entropy']
}
param_rf = {
    'max_depth': [2, 3, 4],
    'bootstrap': [True, False],
    'max_features': ['auto', 'sqrt', 'log2', None],
    'criterion': ['gini', 'entropy']
}
param_knn = {'n_neighbors':list(range(1,12)),
          'leaf_size':[1,2,3,5],
          'weights':['uniform', 'distance'],
             'p' : [1,2,3]
}
# params_svm = {'C': [3,4,5,6,7,8,9,10,11,12], 
#           'kernel': ['linear', 'poly', 'rbf', 'sigmoid']}


# In[ ]:


olist = [dt,rf]
plist = [param_dt,param_rf]
nlist = ['Decision','Random']


# In[ ]:


for o,p,n in zip(olist,plist,nlist):
    print('\n***',n)
    grid = GridSearchCV(o, cv = 5,param_grid=p, n_jobs = 3)
    grid.fit(x,y)
    print(grid.best_params_)


# In[ ]:


# gridk = GridSearchCV(knn, cv = 3,param_grid=param_knn, n_jobs = 3)
# gridk.fit(x,y)
# print(grid.best_params_)


# # Up sampling

# In[ ]:


sm = SMOTE()


# In[ ]:


ovx,ovy = sm.fit_sample(x,y)


# In[ ]:


xtrain,xtest,ytrain,ytest = train_test_split(ovx,ovy,random_state=32)


# In[ ]:


for obj,name in zip(mobj,mname):
    obj.fit(xtrain,ytrain)
    ypred = obj.predict(xtest)
    print('\n***',name,'*** \n')
    print('accuracy_score \n',accuracy_score(ytest,ypred))
#     print('confusion_matrix \n',confusion_matrix(ytest,ypred))
#     print('classification_report \n',classification_report(ytest,ypred))


# # Down sampling

# In[ ]:


nm = NearMiss()


# In[ ]:


unx,uny = nm.fit_sample(x,y)


# In[ ]:


xtrain,xtest,ytrain,ytest = train_test_split(unx,uny,random_state=32)


# In[ ]:


for obj,name in zip(mobj,mname):
    obj.fit(xtrain,ytrain)
    ypred = obj.predict(xtest)
    print('\n***',name,'*** \n')
    print('accuracy_score \n',accuracy_score(ytest,ypred))
    print('confusion_matrix \n',confusion_matrix(ytest,ypred))
    print('classification_report \n',classification_report(ytest,ypred))


# In[ ]:


plt.figure(figsize=(12,10))
sns.heatmap(medical.corr(),annot=True)


# In[ ]:


model = sms.Logit(y,x).fit()
model.summary()


# In[ ]:




