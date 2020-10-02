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


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes = True)
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


dataset = pd.read_csv('../input/pimaindiansdiabetescsv/pima-indians-diabetes.csv',header = None)


# In[ ]:


dataset.head()


# In[ ]:


columns = ['preg','plas','pres','skin','test','mass','pedi','age','class']


# In[ ]:


dataset.columns = columns


# In[ ]:


dataset.head()


# ### EDA

# In[ ]:


dataset.info()


# In[ ]:


dataset.describe().T


# In[ ]:


dataset[dataset['plas'] == 0].shape


# In[ ]:


dataset[dataset['pres'] == 0].shape


# In[ ]:


dataset[dataset['skin'] == 0].shape


# In[ ]:


dataset[dataset['test'] == 0].shape


# In[ ]:


dataset[dataset['mass'] == 0].shape


# In[ ]:


dataset[['plas','pres','skin','test','mass']].median()


# In[ ]:


dataset[['plas','pres','skin','test','mass']] = dataset[['plas','pres','skin','test','mass']].apply(lambda x: x.replace(0,x.median()))


# In[ ]:


dataset.head()


# In[ ]:


dataset.iloc[:,:-1] = dataset.iloc[:,:-1].astype('float64')


# In[ ]:


dataset.dtypes


# In[ ]:


dataset.describe().T


# In[ ]:


dataset.corr()['class'].plot(kind = 'bar')
plt.show()


# In[ ]:


plt.figure(figsize=(12,6))
sns.heatmap(dataset.corr(),annot = True)


# In[ ]:


dataset['class'].value_counts()


# In[ ]:


sns.pairplot(dataset,hue = 'class')


# In[ ]:


X = dataset.iloc[:,:-1]
y = dataset.iloc[:,-1]


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y,stratify = y,test_size= 0.3,random_state=42)


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier,BaggingClassifier


# In[ ]:


from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier


# In[ ]:


dtree = DecisionTreeClassifier(criterion = 'gini',max_depth = 5)
dtree.fit(X_train,y_train)
print('Training Score : ',dtree.score(X_train,y_train))
print('Testing Score : ',dtree.score(X_test,y_test))
y_pred = dtree.predict(X_test)
y_pred_prob = dtree.predict_proba(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix,classification_report
print('<--------Confusion Matrix-------->\n',confusion_matrix(y_test,y_pred))
print('<--------Classification Report-------->\n',classification_report(y_test,y_pred))


# In[ ]:


rf = RandomForestClassifier(n_estimators=10,max_features=4, random_state=42)
rf.fit(X_train,y_train)
print('Training Score : ',rf.score(X_train,y_train))
print('Testing Score : ',rf.score(X_test,y_test))
y_pred = rf.predict(X_test)
y_pred_prob = rf.predict_proba(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix,classification_report
print('<--------Confusion Matrix-------->\n',confusion_matrix(y_test,y_pred))
print('<--------Classification Report-------->\n',classification_report(y_test,y_pred))


# In[ ]:


dtree_1 = DecisionTreeClassifier()


# In[ ]:


dtree_1.fit(X_train,y_train)


# In[ ]:


abc = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=1),n_estimators=100)
abc.fit(X_train,y_train)
print('Training Score : ',abc.score(X_train,y_train))
print('Testing Score : ',abc.score(X_test,y_test))
y_pred = abc.predict(X_test)
y_pred_prob = abc.predict_proba(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix,classification_report
print('<--------Confusion Matrix-------->\n',confusion_matrix(y_test,y_pred))
print('<--------Classification Report-------->\n',classification_report(y_test,y_pred))



# In[ ]:


gb = GradientBoostingClassifier(learning_rate=0.05,n_estimators=50,max_depth=3)
gb.fit(X_train,y_train)
print('Training Score : ',gb.score(X_train,y_train))
print('Testing Score : ',gb.score(X_test,y_test))
y_pred = gb.predict(X_test)
y_pred_prob = gb.predict_proba(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix,classification_report
print('<--------Confusion Matrix-------->\n',confusion_matrix(y_test,y_pred))
print('<--------Classification Report-------->\n',classification_report(y_test,y_pred))



# In[ ]:


xgb = XGBClassifier()
xgb.fit(X_train,y_train)
print('Training Score : ',xgb.score(X_train,y_train))
print('Testing Score : ',xgb.score(X_test,y_test))
y_pred = xgb.predict(X_test)
y_pred_prob = xgb.predict_proba(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix,classification_report
print('<--------Confusion Matrix-------->\n',confusion_matrix(y_test,y_pred))
print('<--------Classification Report-------->\n',classification_report(y_test,y_pred))



# In[ ]:


lgbm = LGBMClassifier(max_depth=3,
    learning_rate=0.1,
    n_estimators=50,)
lgbm.fit(X_train,y_train)
print('Training Score : ',lgbm.score(X_train,y_train))
print('Testing Score : ',lgbm.score(X_test,y_test))
y_pred = lgbm.predict(X_test)
y_pred_prob = lgbm.predict_proba(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix,classification_report
print('<--------Confusion Matrix-------->\n',confusion_matrix(y_test,y_pred))
print('<--------Classification Report-------->\n',classification_report(y_test,y_pred))



# In[ ]:


cat = CatBoostClassifier(iterations=100,learning_rate=0.1)
cat.fit(X_train,y_train,plot = True)
print('Training Score : ',cat.score(X_train,y_train))
print('Testing Score : ',cat.score(X_test,y_test))
y_pred = cat.predict(X_test)
y_pred_prob = cat.predict_proba(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix,classification_report
print('<--------Confusion Matrix-------->\n',confusion_matrix(y_test,y_pred))
print('<--------Classification Report-------->\n',classification_report(y_test,y_pred))



# In[ ]:


from sklearn.model_selection import cross_val_score


# In[ ]:


cvs = cross_val_score(estimator=cat,X=X_train,y=y_train,scoring = 'accuracy',n_jobs = -1,verbose = 100,cv = 10)


# In[ ]:


cvs


# In[ ]:


cvs.mean()


# In[ ]:




