#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import warnings
warnings.filterwarnings('ignore')

import sys
import pandas
import numpy
import sklearn
import keras

import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
import numpy as np

# import the uci pima indians diabetes dataset
names = ['n_pregnant', 'glucose_concentration', 'blood_pressuer (mm Hg)', 'skin_thickness (mm)', 'serum_insulin (mu U/ml)',
        'BMI', 'pedigree_function', 'age', 'class']
df = pd.read_csv('../input/diabetes.csv', names = names)
df.info()


# In[ ]:


# import the uci pima indians diabetes dataset
df.columns = df.iloc[0].values
df.drop(0,inplace=True)
df.describe()


# In[ ]:


df.head()


# In[ ]:


df = df.reset_index()
df.drop('index',axis=1,inplace=True)
df.head()


# In[ ]:


for x in df.columns.tolist():
    df[x] = pd.to_numeric(df[x])


# In[ ]:


df.info()


# In[ ]:


plt.figure(figsize=(12,12))
sns.heatmap(df.corr(),annot=True,cmap='magma')


# In[ ]:


data = df
data.head()


# **Making predictions of zero values in each column**

# In[ ]:


gluc_0 = data[data['Glucose']==0]
gluc_0


# In[ ]:


blood_0 = data[data['BloodPressure']==0]
blood_0.head()


# In[ ]:


skin_0 = data[data['SkinThickness']==0]
skin_0.head()


# In[ ]:


serum_0 = data[data['Insulin']==0]
serum_0.head()


# In[ ]:


bmi_0 = data[data['BMI']==0]
bmi_0.head()


# In[ ]:


ped_0 = data[data['DiabetesPedigreeFunction']==0]
ped_0


# In[ ]:


age_0 = data[data['Age']==0]
age_0


# In[ ]:


'''cols = ['glucose_concentration','blood_pressuer (mm Hg)','skin_thickness (mm)','serum_insulin (mu U/ml)','BMI']
for col in cols:
    df[col].replace(0,np.NaN,inplace=True)

df.describe()'''


# In[ ]:


from sklearn.preprocessing import PolynomialFeatures
pf = PolynomialFeatures(degree=1)


# In[ ]:


X = data.loc[data['BloodPressure']!=0,['Glucose','Pregnancies','DiabetesPedigreeFunction','Age']]
y = data.loc[data['BloodPressure']!=0,'BloodPressure']
X_poly = pf.fit_transform(X)
X_poly.shape,y.shape


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X_poly,y,random_state=42)
for x in (X_train,X_test,y_train,y_test):
    print(x.shape)


# In[ ]:


from sklearn.linear_model import LinearRegression
lr = LinearRegression()

lr.fit(X_train,y_train)

preds = lr.predict(X_test)
from sklearn.metrics import mean_absolute_error,mean_squared_error
mean_absolute_error(y_test,preds),mean_squared_error(y_test,preds)


# In[ ]:


for i,j in zip(lr.predict(X_train),y_train.tolist()[:15]):
    print(j,'-->',i)


# In[ ]:


data.loc[blood_0.index,'BloodPressure'] = lr.predict(pf.transform(data.loc[blood_0.index,['Glucose','Pregnancies','DiabetesPedigreeFunction','Age']]))


# In[ ]:


data[(data['SkinThickness']==0) & (data['Glucose']==0)]


# In[ ]:


#pf = PolynomialFeatures(degree=3)
X = data.loc[data['BMI']!=0,['BloodPressure','Glucose','Pregnancies','DiabetesPedigreeFunction','Age']]
y = data.loc[data['BMI']!=0,'BMI']
'''X_poly = pf.fit_transform(X)'''
X.shape,y.shape


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=42)
for x in (X_train,X_test,y_train,y_test):
    print(x.shape)


# In[ ]:


lr = LinearRegression()

lr.fit(X_train,y_train)

preds = lr.predict(X_test)
from sklearn.metrics import mean_absolute_error,mean_squared_error
mean_absolute_error(y_test,preds),mean_squared_error(y_test,preds)


# In[ ]:


for i,j in zip(preds,y_test.tolist()[:15]):
    print(j,'-->',i)


# In[ ]:


mae_sum = 0
for p,t in zip(preds, y_test):
    mae_sum += abs(p - t)
mae = mae_sum / len(y_test)
mae


# In[ ]:


data.loc[bmi_0.index,'BMI'] = lr.predict(data.loc[bmi_0.index,['BloodPressure','Glucose','Pregnancies','DiabetesPedigreeFunction','Age']])

data.loc[bmi_0.index,'BMI']


# In[ ]:


pf = PolynomialFeatures(degree=2)
X = data.loc[data['SkinThickness']!=0,['BMI','BloodPressure','Glucose','Pregnancies','DiabetesPedigreeFunction','Age']]
y = data.loc[data['SkinThickness']!=0,'SkinThickness']
X_poly = pf.fit_transform(X)
X_poly.shape,y.shape


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X_poly,y,random_state=42)
for x in (X_train,X_test,y_train,y_test):
    print(x.shape)


# In[ ]:


lr = LinearRegression()

lr.fit(X_train,y_train)

preds = lr.predict(X_test)
from sklearn.metrics import mean_absolute_error,mean_squared_error
mean_absolute_error(y_test,preds),mean_squared_error(y_test,preds)


# In[ ]:


for i,j in zip(preds,y_test.tolist()[:15]):
    print(j,'-->',i)


# In[ ]:


data.loc[skin_0.index,'SkinThickness'] = lr.predict(pf.transform(data.loc[skin_0.index,['BMI','BloodPressure','Glucose','Pregnancies','DiabetesPedigreeFunction','Age']]))


# In[ ]:


data[data['Glucose']==0]


# In[ ]:


#pf = PolynomialFeatures(degree=3)
X = data.loc[data['Glucose']!=0,['SkinThickness','BMI','BloodPressure','Pregnancies','DiabetesPedigreeFunction','Age']]
y = data.loc[data['Glucose']!=0,'Glucose']
#X_poly = pf.fit_transform(X)
X.shape,y.shape


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=42)
for x in (X_train,X_test,y_train,y_test):
    print(x.shape)

lr = LinearRegression()

lr.fit(X_train,y_train)

preds = lr.predict(X_test)
from sklearn.metrics import mean_absolute_error,mean_squared_error
mean_absolute_error(y_test,preds),mean_squared_error(y_test,preds)


# In[ ]:


for i,j in zip(preds,y_test.tolist()[:15]):
    print(j,'-->',i)


# In[ ]:


data.loc[gluc_0.index,'Glucose'] = lr.predict(data.loc[gluc_0.index,['SkinThickness','BMI','BloodPressure','Pregnancies','DiabetesPedigreeFunction','Age']])


# In[ ]:


data[data['Glucose']==0]


# In[ ]:


#pf = PolynomialFeatures(degree=3)
X = data.loc[data['Insulin']!=0,['Glucose','SkinThickness','BMI','BloodPressure','Pregnancies','DiabetesPedigreeFunction','Age']]
y = data.loc[data['Insulin']!=0,'Insulin']
#X_poly = pf.fit_transform(X)
X.shape,y.shape


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=42)
for x in (X_train,X_test,y_train,y_test):
    print(x.shape)


# In[ ]:


lr = LinearRegression()

lr.fit(X_train,y_train)

preds = lr.predict(X_test)
from sklearn.metrics import mean_absolute_error,mean_squared_error
mean_absolute_error(y_test,preds),mean_squared_error(y_test,preds)


# In[ ]:


for i,j in zip(preds,y_test.tolist()[:15]):
    print(j,'-->',i)


# In[ ]:


data.loc[serum_0.index,'Insulin'] = lr.predict(data.loc[serum_0.index,['Glucose','SkinThickness','BMI','BloodPressure','Pregnancies','DiabetesPedigreeFunction','Age']])


# In[ ]:


X = data.iloc[:,:8]
y = data.iloc[:,8]
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler()
sc.fit(X)
X_sc = sc.transform(X)
print(X_sc.shape,y.shape)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X_sc,y)
for x in (X_train,X_test,y_train,y_test):
    print(x.shape)


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()

clf.fit(X_train,y_train)

preds = clf.predict(X_test)

from sklearn.metrics import confusion_matrix

confusion_matrix(y_true=y_test,y_pred=preds)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=1000)

clf.fit(X_train,y_train)

preds = clf.predict(X_test)

confusion_matrix(y_true=y_test,y_pred=preds)


# In[ ]:


confusion_matrix(y_true=y_train,y_pred=clf.predict(X_train))


# **Random forest with n_estimators=1000 results in overfitting**

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors=3)

clf.fit(X_train,y_train)

preds = clf.predict(X_test)

confusion_matrix(y_true=y_test,y_pred=preds)


# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = data.iloc[:,:8]
y = data.iloc[:,8]
print(X.shape,y.shape)

X_standardized = scaler.fit_transform(X)

data2 = pd.DataFrame(X_standardized)
data2.describe()


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X_standardized,y)
for x in (X_train,X_test,y_train,y_test):
    print(x.shape)


# In[ ]:


#df.dropna(inplace=True)
sns.pairplot(data,hue='Outcome',diag_kind='kde')


# In[ ]:


df.drop('BloodPressure',inplace=True,axis=1)

df.describe()


# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()


# In[ ]:


dataset = df.values
dataset.shape


# In[ ]:


X = dataset[:,:7]
y = dataset[:,7]
print(X.shape,y.shape)

X_standardized = scaler.fit_transform(X)

data = pd.DataFrame(X_standardized)
data.describe()


# In[ ]:


X_standardized.shape,y.shape


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X_standardized,y)
for x in (X_train,X_test,y_train,y_test):
    print(x.shape)


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()

clf.fit(X_train,y_train)

preds = clf.predict(X_test)

from sklearn.metrics import confusion_matrix

confusion_matrix(y_true=y_test,y_pred=preds)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100,max_depth=10)

clf.fit(X_train,y_train)

preds = clf.predict(X_test)

confusion_matrix(y_true=y_test,y_pred=preds)


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors=3)

clf.fit(X_train,y_train)

preds = clf.predict(X_test)

confusion_matrix(y_true=y_test,y_pred=preds)

