#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing Libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


ds = pd.read_csv('/kaggle/input/factors-affecting-campus-placement/Placement_Data_Full_Class.csv')
ds


# In[ ]:


ds.info()


# In[ ]:


ds.isnull().sum()


# Filling the null values

# In[ ]:


mean_salary = ds['salary'].mean()
ds.fillna({'salary' : mean_salary}, inplace=True)
ds.isnull().sum()


# ## **Converting string values into integar**

# In[ ]:


from sklearn.preprocessing import LabelEncoder

gender_n = LabelEncoder()
ssc_b_n = LabelEncoder()
hsc_b_n = LabelEncoder()
hsc_s_n = LabelEncoder()
degree_t_n = LabelEncoder()
workex_n = LabelEncoder()
specialisation_n = LabelEncoder()
status_n = LabelEncoder()

ds['gender_n'] = gender_n.fit_transform(ds['gender'])
ds['ssc_b_n'] = ssc_b_n.fit_transform(ds['ssc_b'])

ds['hsc_b_n'] = hsc_b_n.fit_transform(ds['hsc_b'])
ds['hsc_s_n'] = hsc_s_n.fit_transform(ds['hsc_s'])

ds['degree_t_n'] = degree_t_n.fit_transform(ds['degree_t'])
ds['workex_n'] = workex_n.fit_transform(ds['workex'])

ds['specialisation_n'] = specialisation_n.fit_transform(ds['specialisation'])
ds['status_n'] = status_n.fit_transform(ds['status'])


# Dropping unnecessary columns

# In[ ]:


ds.drop(['gender', 'ssc_b', 'hsc_b', 'hsc_s', 'degree_t', 'workex', 'specialisation', 'status','sl_no'], axis=1, inplace=True)
ds


# # Balancing dataset

# In[ ]:


ds['status_n'].value_counts()


# In[ ]:


ds_0 = ds[ds['status_n'] == 0]
ds_1 = ds[ds['status_n'] == 1]

ds_1 = ds_1.sample(ds_0.shape[0])

ds = ds_0.append(ds_1, ignore_index = True)
ds['status_n'].value_counts()


# # Feature Selection

# In[ ]:


x = ds.drop(['status_n'], axis=1)
y = ds['status_n']


# In[ ]:


from sklearn.feature_selection import SelectKBest, chi2
best_feature = SelectKBest(score_func= chi2, k = 'all')

fit = best_feature.fit(x,y)

ofscore = pd.DataFrame(fit.scores_)
ofcolumn = pd.DataFrame(x.columns)


# I select only that features that have feature_score atleast 1.0

# In[ ]:


feature_score = pd.concat([ofcolumn, ofscore], axis=1)
feature_score.columns = ['spec', 'score']
feature_score


# dropping unnecessary columns

# In[ ]:


x.drop(['mba_p','gender_n','ssc_b_n','hsc_b_n','hsc_s_n','degree_t_n'], axis=1, inplace=True)
x


# # Splitting data into train and test

# In[ ]:


from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.18)


# # Standardizing data

# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)


# # **Classifiers**

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier


# In[ ]:


rf = RandomForestClassifier()
rf.fit(x_train,y_train)
rf.score(x_test,y_test)


# In[ ]:


dt = DecisionTreeClassifier()
dt.fit(x_train,y_train)
dt.score(x_test,y_test)


# In[ ]:


kn = KNeighborsClassifier()
kn.fit(x_train,y_train)
kn.score(x_test,y_test)


# In[ ]:


svm = SVC()
svm.fit(x_train,y_train)
svm.score(x_test,y_test)


# In[ ]:


xg = XGBClassifier()
xg.fit(x_train,y_train)
xg.score(x_test,y_test)


# In[ ]:


nb = GaussianNB()
nb.fit(x_train,y_train)
nb.score(x_test,y_test)


# # Confusion Matrix

# In[ ]:


from sklearn.metrics import confusion_matrix, classification_report

y_pred = xg.predict(x_test)
cm = confusion_matrix(y_test,y_pred)
print('Confusion Matrix\n',cm)


# In[ ]:


plt.figure(figsize=(7,5))
sns.heatmap(cm,annot=True)
plt.xlabel('Predicted')
plt.ylabel('truth')


# **Classification Report**

# In[ ]:


print(classification_report(y_test,y_pred, target_names=['Class 0','Class 1']))

