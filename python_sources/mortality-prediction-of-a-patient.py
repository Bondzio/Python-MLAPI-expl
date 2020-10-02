#!/usr/bin/env python
# coding: utf-8

# The sample data contains the following attributes:
# 
# a) AGE: Age of the patient
# 
# b) SEX: Sex of the patient
# 
# c) CASTE NAME: Caste of the patient.
# 
# d) CATEGORY _CODE: Administrative data
# 
# e) CATEGORY NAME: Administrative data
# 
# f) SURGERY CODE: Administrative data
# 
# g) SURGERY: Name of the surgery operated.
# 
# h) DISTRICT_NAME: District of the patient
# 
# i) PREAUTH_DATE: Date of pre-authorization of the treatment
# 
# j) PREAUTH_AMT: Amount pre-authorized
# 
# k) CLAIM_DATE: Date of claim
# 
# l) CLAIM_AMOUNT: Amount claimed (post-treatment)
# 
# m) HOSP_NAME: Hospital Name
# 
# n) HOSP_TYPE: Type of hospital (Government or Private)
# 
# o) HOSP_DISTRICT: District where the hospital is located
# 
# p) SURGERY _ DATE: Date of surgery
# 
# q) DISCHARGE DATE: Date of discharge from the hospital post surgery
# 
# t) Mortality Y / N: If the patient died in the process
# 
# s) MORTALITY DATE: Date if dead
# 
# t) SRC_REGISTRATION: Administrative data
# 
# The target column is => 'Mortality Y / N'

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="ticks", color_codes=True)


# In[ ]:


df = pd.read_csv('../input/hospital_data.csv')
df.head()


# In[ ]:


df = df.drop('Unnamed: 0', axis=1)
df.shape


# In[ ]:


df.dtypes


# In[ ]:


def missing_values(df):
    missing_val = df.isnull().sum()
    missing_val_percent = missing_val * 100 / len(df)
    missing_val_table = pd.concat([missing_val, missing_val_percent], axis=1)
    missing_val_table = missing_val_table.rename(columns={0 : 'Missing Values', 1 : '% of Total Values'})
    return missing_val_table


# In[ ]:


missing_vals = missing_values(df)
missing_vals.sort_values(by=['% of Total Values'], ascending=False).head()


# In[ ]:


df = df.rename(columns={"Mortality Y / N": "Mortality"})


# In[ ]:


plt.figure(figsize=(8,6))
sns.countplot(x='Mortality', data=df, order= df['Mortality'].value_counts().index)
plt.title('Mortality count')
plt.show()


# So there is a problem of class imbalance we have to fix that later

# In[ ]:


df.loc[df['Mortality'] == 'NO', 'Mortality'] = 0
df.loc[df['Mortality'] == 'YES', 'Mortality'] = 1
df['Mortality'] = df['Mortality'].astype('int64')


# In[ ]:


# no. of unique vals in object type cols
df.select_dtypes('object').apply(pd.Series.nunique, axis=0)


# Now exploring each columns

# AGE & Sex

# In[ ]:


df.loc[(df['SEX'] == 'MALE') , 'SEX'] = 'Male'
df.loc[(df['SEX'] == 'FEMALE'), 'SEX'] = 'Female'
df.loc[(df['SEX'] == 'Male(Child)'), 'SEX'] = 'Boy'
df.loc[(df['SEX'] == 'Female(Child)'), 'SEX'] = 'Girl'


# In[ ]:


sns.catplot(x="SEX", y="AGE", hue="Mortality", kind="box", data=df)
plt.title('Age plot wrt Sex & Mortality')
plt.show()


# In[ ]:


# Using AGE col for plotting purpose since it will have the range of ages, the col will be dropped during training
df['Age'] = df['AGE']

df.loc[df['Age'] == 0, 'Age'] = 5
df.loc[(df['Age'] > 100), 'AGE'] = 100


# So a lot of ages has its value 0 for boy & girl and a Female has an age > 100, so we have to format the age.

# In[ ]:


df.loc[df['AGE'] <= 10, 'AGE'] = 10
df.loc[(df['AGE'] > 10) & (df['AGE'] <= 20), 'AGE'] = 20
df.loc[(df['AGE'] > 20) & (df['AGE'] <= 30), 'AGE'] = 30
df.loc[(df['AGE'] > 30) & (df['AGE'] <= 40), 'AGE'] = 40
df.loc[(df['AGE'] > 40) & (df['AGE'] <= 50), 'AGE'] = 50
df.loc[(df['AGE'] > 50) & (df['AGE'] <= 60), 'AGE'] = 60
df.loc[(df['AGE'] > 60) & (df['AGE'] <= 70), 'AGE'] = 70
df.loc[(df['AGE'] > 70) & (df['AGE'] <= 80), 'AGE'] = 80
df.loc[(df['AGE'] > 80) & (df['AGE'] <= 90), 'AGE'] = 90
df.loc[(df['AGE'] > 90), 'AGE'] = 100


# In[ ]:


plt.figure(figsize=(12, 6))
sns.countplot(x="AGE", data=df, order=df['AGE'].value_counts().index)
plt.title("AGE count")


# In[ ]:


temp_df = df.groupby(['Mortality', 'AGE'])['AGE'].count().unstack(['AGE'])
temp_df.head()


# In[ ]:


sns.catplot(x='AGE', col='Mortality', hue='SEX', data=df,order=df['AGE'].value_counts().index, kind='count', height=8, aspect=.7)


# AGE in range of [ages > 30 and ages <= 70] mortality with class 0 is more 

# In[ ]:


plt.figure(figsize=(12, 6))
sns.catplot(x="SEX", kind="count", data=df, order=df['SEX'].value_counts().index)
plt.title("SEX count")


# In[ ]:


temp_df = df.groupby(['Mortality', 'SEX'])['SEX'].count().unstack('Mortality')
temp_df.columns = ['0', '1']
temp_df = temp_df.sort_values(by='0', ascending=False)
temp_df.plot.bar(rot=0, figsize=(12,8))
plt.title('SEX vs Mortality plot')
plt.show()


# Death rate of male is greater than female

# In[ ]:


temp_df = df.groupby(['Mortality', 'AGE', 'SEX'])['SEX'].count().unstack(['Mortality']).reset_index()
temp_df.columns = ['AGE', 'SEX', '0', '1']
temp_df.sort_values(by='0', ascending=False).head()


# In[ ]:


sns.catplot(x='SEX', col='Mortality', hue='AGE', data=df, kind='count', height=8, aspect=.7)


# Males within age 31 and 60 have high deaths & Females with ages between 41 and 60 have high deaths

# PREAUTH_AMT

# In[ ]:


plt.figure(figsize=(6,4))
plt.scatter(range(df.shape[0]), np.sort(df['PREAUTH_AMT']))
plt.xlabel('Index')
plt.ylabel('PREAUTH_AMT')
plt.show()


# Fix that outlier

# In[ ]:


upper_limit = np.percentile(df['PREAUTH_AMT'], 99)
df.loc[(df['PREAUTH_AMT'] > upper_limit), 'PREAUTH_AMT'] = upper_limit


# In[ ]:


plt.figure(figsize=(12, 8))
sns.catplot(x="SEX", y="PREAUTH_AMT", hue="Mortality", kind="box", data=df)
plt.title('PREAUTH_AMT plot wrt Sex & Mortality')
plt.show()


# So preauthorization amount of female is maximum & also preauthorization amount of alive people are greater than dead ones 

# CLAIM_AMOUNT

# In[ ]:


plt.figure(figsize=(6,4))
plt.scatter(range(df.shape[0]), np.sort(df['CLAIM_AMOUNT']))
plt.xlabel('Index')
plt.ylabel('CLAIM_AMOUNT')
plt.show()


# In[ ]:


upper_limit = np.percentile(df['CLAIM_AMOUNT'], 99)
df.loc[(df['CLAIM_AMOUNT'] > upper_limit), 'CLAIM_AMOUNT'] = upper_limit


# In[ ]:


sns.catplot(x="SEX", y="CLAIM_AMOUNT", hue="Mortality", kind="box", data=df)
plt.title('CLAIM_AMOUNT plot wrt Sex & Mortality')
plt.show()


# Claimed amount of Boy with Mortality 1 or alive is maximum

# CASTE_NAME

# In[ ]:


temp_df = df.groupby(['Mortality', 'CASTE_NAME'])['CASTE_NAME'].count().unstack(['Mortality'])
temp_df.columns = ['0', '1']
temp_df = temp_df.sort_values(by='0', ascending=False)
temp_df.plot.bar(rot=0, figsize=(8, 8))
plt.title('CASTE_NAME vs Mortality plot')
plt.show()


# In[ ]:


sns.catplot(x='CASTE_NAME', col='Mortality', hue='AGE', data=df, kind='count', height=8, aspect=.7)


# In[ ]:


temp_df = df.groupby(['CASTE_NAME', 'AGE'])['CASTE_NAME'].count().unstack(['AGE'])
temp_df.plot.bar(rot=0, figsize=(25, 8))
plt.title('Ages with respect to diff caste groups')
plt.show()


# Caste BC with ages between 41 and 60 has more deaths

# CATEGORY_CODE

# In[ ]:


temp_df = df.groupby(['CATEGORY_CODE', 'Mortality'])['CATEGORY_CODE'].count().unstack(['Mortality'])
temp_df.columns = ['0', '1']
temp_df = temp_df.sort_values(by='0', ascending=False)
temp_df.plot.bar(rot=0, figsize=(25, 12))
plt.title('CATEGORY_CODE vs Mortality plot')
plt.show()


# M6, S12 & S15 category codes have higher deaths than others

# CATEGORY_NAME

# In[ ]:


temp_df = df.groupby(['CATEGORY_NAME', 'Mortality'])['CATEGORY_NAME'].count().unstack(['Mortality'])
temp_df.columns = ['0', '1']
temp_df = temp_df.sort_values(by='0', ascending=False)
temp_df.plot.bar(rot=90, figsize=(25, 12))
plt.title('CATEGORY_NAME vs Mortality plot')
plt.show()


# NEPHROLOGY, MEDICAL ONCOLOGY & POLY TRAUMA categories have higher deaths

# DISTRICT_NAME

# In[ ]:


temp_df = df.groupby(['DISTRICT_NAME', 'Mortality'])['DISTRICT_NAME'].count().unstack(['Mortality'])
temp_df.columns = ['0', '1']
temp_df = temp_df.sort_values(by='0', ascending=False)
temp_df.plot.bar(rot=0, figsize=(25, 12))
plt.title('DISTRICT_NAME vs Mortality plot')
plt.show()


# District 3 & 1 has higher deaths than others

# In[ ]:


df = df.drop(['DISTRICT_NAME'], axis=1)


# HOSP_TYPE

# In[ ]:


temp_df = df.groupby(['HOSP_TYPE', 'Mortality'])['HOSP_TYPE'].count().unstack(['Mortality'])
temp_df.columns = ['0', '1']
temp_df = temp_df.sort_values(by='0', ascending=False)
temp_df.plot.bar(rot=0, figsize=(8, 6))
plt.title('HOSP_TYPE vs Mortality plot')
plt.show()


# Hospital type C has greater deaths

# HOSP_DISTRICT

# In[ ]:


temp_df = df.groupby(['HOSP_DISTRICT', 'Mortality'])['HOSP_DISTRICT'].count().unstack(['Mortality'])
temp_df.columns = ['0', '1']
temp_df = temp_df.sort_values(by='0', ascending=False)
temp_df.plot.bar(rot=30, figsize=(12, 8))
plt.title('HOSP_DISTRICT vs Mortality plot')
plt.show()


# HOSP_DISTRICT 1, 2, 3 has almost same amount of deaths

# SRC_REGISTRATION

# In[ ]:


temp_df = df.groupby(['SRC_REGISTRATION', 'Mortality'])['SRC_REGISTRATION'].count().unstack(['Mortality'])
temp_df.columns = ['0', '1']
temp_df = temp_df.sort_values(by='0', ascending=False)
temp_df.plot.bar(rot=0, figsize=(8, 6))
plt.title('SRC_REGISTRATION vs Mortality plot')
plt.show()


# D SRC_REGISTRATION has excessively greater amount of deaths than any class

# Exploring datetime cols

# In[ ]:


df = df.drop(['MORTALITY_DATE'], axis=1)


# In[ ]:


df.loc[(df['DISCHARGE_DATE'].isnull()) , 'DISCHARGE_DATE'] = '0/0/0000 0:00'


# In[ ]:


df['PREAUTH_DATE'] = pd.to_datetime(df['PREAUTH_DATE'])
df['CLAIM_DATE'] = pd.to_datetime(df['CLAIM_DATE'])
df['SURGERY_DATE'] = pd.to_datetime(df['SURGERY_DATE'])
df['DISCHARGE_DATE'] = pd.to_datetime(df['DISCHARGE_DATE'], errors = 'coerce')

df['PREAUTH_Month'] = df['PREAUTH_DATE'].dt.month
df['PREAUTH_Year'] = df['PREAUTH_DATE'].dt.year

df['CLAIM_Month'] = df['CLAIM_DATE'].dt.month
df['CLAIM_Year'] = df['CLAIM_DATE'].dt.year

df['SURGERY_Month'] = df['SURGERY_DATE'].dt.month
df['SURGERY_YEAR'] = df['SURGERY_DATE'].dt.year

df['DISCHARGE_Month'] = df['DISCHARGE_DATE'].dt.month
df['DISCHARGE_YEAR'] = df['DISCHARGE_DATE'].dt.year


# Replace null vals with mean

# In[ ]:


df.loc[(df['DISCHARGE_YEAR'].isnull()) , 'DISCHARGE_YEAR'] = round(df['DISCHARGE_YEAR'].mean(), 0)
df.loc[(df['DISCHARGE_Month'].isnull()) , 'DISCHARGE_Month'] = round(df['DISCHARGE_Month'].mean(), 0)


# In[ ]:


df = df.drop(['PREAUTH_DATE', 'CLAIM_DATE', 'SURGERY_DATE', 'DISCHARGE_DATE'], axis=1)


# In[ ]:


pd.crosstab(df['SURGERY_YEAR'], df['Mortality']).T


# In[ ]:


temp_df = df.groupby(['Mortality', 'SURGERY_YEAR'])['SURGERY_YEAR'].count().unstack('SURGERY_YEAR')
temp_df = temp_df.T
temp_df.columns = ['0', '1']
temp_df = temp_df.sort_values(by='0', ascending=False)
temp_df.plot.bar(rot=0, figsize=(8,6))


# Most of the surgeries are done in 2017 and 2016, the deaths in these years are also greater than other years

# In[ ]:


plt.figure(figsize=(12, 6))
sns.countplot(x="SURGERY_Month", hue='Mortality', data=df, order= df['SURGERY_Month'].value_counts().index)
plt.title("Months of Surgery")


# In each month almost same no. of surgeries takes place

# In[ ]:


df = df.drop(['SURGERY_Month', 'CLAIM_Month', 'PREAUTH_Month', 'DISCHARGE_Month', 'AGE'], axis=1)


# In[ ]:


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

cat_cols = [col for col in df.columns if df[col].dtype == 'object']
for col in cat_cols:
    df[col] = le.fit_transform(df[col])


# In[ ]:


X = df.drop('Mortality', axis=1)
y = df['Mortality']


# In[ ]:


from sklearn.preprocessing import StandardScaler

X = StandardScaler().fit_transform(X)


# In[ ]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)


# Now we will have to fix the class imbalance on the training set[](http://)

# In[ ]:


sns.countplot(y_train)


# In[ ]:


from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=9)
X_train, y_train = smote.fit_sample(X_train, y_train)

sns.countplot(y_train)


# Class imbalance fixed!

# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

log_reg = LogisticRegression(C=1, random_state=17, solver='liblinear')

c_values = np.logspace(-2, 2, 20)

clf = GridSearchCV(estimator=log_reg, param_grid={'C': c_values}, scoring='roc_auc', n_jobs=1, cv=5, verbose=1)

clf.fit(X_train, y_train)
# clf.best_params_

y_pred = clf.predict(X_test)

print(accuracy_score(y_test, y_pred))


# In[ ]:


from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report 

conf_mat = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print('Confusion Matrix ==>')
print(conf_mat)
print('----------------------------------------------------------------------------------------')
print('Classification Report ==>')
print(report)


# In[ ]:


from sklearn.metrics import roc_curve, roc_auc_score

y_pred_proba = clf.predict_proba(X_test)[:, 1]

fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
auc = roc_auc_score(y_test, y_pred_proba)

plt.plot(fpr, tpr, label="auc="+str(auc))
plt.legend(loc=4)
plt.show()


# AUC score 1 represent perfect classifier and 0.5 represents bad classifier

# In[ ]:


map_class = {0: 'NO', 1: 'YES'}
temp_df = pd.DataFrame({'prediction': y_pred, 'original': y_test})
temp_df['prediction'] = temp_df['prediction'].map(map_class)
temp_df['original'] = temp_df['original'].map(map_class)
temp_df.head()

