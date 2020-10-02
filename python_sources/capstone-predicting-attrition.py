#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


df=pd.read_csv("../input/HR_Employee_Attrition_Data.csv")


# In[ ]:


df.head()


# # Checking Nulls

# In[ ]:


df.isnull().any()


# In[ ]:


df.shape


# In[ ]:


df.describe()


# # Taking the numeric Colums for analysis

# In[ ]:


df_n=df.select_dtypes(include=['number'])


# In[ ]:


df_n.head()


# # Finding outliers

# In[ ]:


fig,axes =plt.subplots(6,5, figsize=(20, 30))
ax=axes.ravel()
i=0

for column in df_n.columns:
    sns.boxplot(data=df_n[column],ax=ax[i])
    ax[i].set_xlabel(list(df_n.columns)[i])
    i +=1
plt.show()  


# In[ ]:


#MonthlyIncome,NunCompaniesWorked,StockOptionLevel,TotalWorkingYears,TrainingTimesLastYear,YearsAtCompany,YearsInCurrentRole,
#YearsSinceLastPromotion,YearsWithCurrManager


# # Checking Correlation

# In[ ]:


df_n.corr()


# In[ ]:


df_n.StandardHours.value_counts()


# # Removing Constat or Zero variance Columns

# In[ ]:


df.drop(["StandardHours","EmployeeCount"],axis=1,inplace=True)


# In[ ]:


df_n=df.select_dtypes(include=['number'])


# In[ ]:


df_n.corr()


# In[ ]:


f, ax = plt.subplots(figsize=(10, 8))
corr = df_n.corr()
sns.heatmap(corr,
            mask=np.zeros_like(corr, dtype=np.bool), 
            cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax)


# In[ ]:


f, ax = plt.subplots(figsize=(20, 16))
corr = df_n.corr()
sns.heatmap(corr, annot=True,fmt='.2f',mask=np.zeros_like(corr, dtype=np.bool), 
            cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax)


# # Columns at correlation

# In[ ]:


df_n.MonthlyIncome.corr(df_n.JobLevel) #Checking Correlatio b/w two columns


# # Correlated Columns

# In[ ]:


# 1)MonthlyIncome:JobLevel
# 2)PerformanceRating:PercentSalaryHike,
# 3)MonthlyIncome:TotalWorkingYears
# 4)YearsAtCompany:YearsInCurrentRole
# 5)YearsAtCompany:YearsWithCurrManager


# # Removing Correlated columns

# In[ ]:


df_new=df.drop(["JobLevel","TotalWorkingYears","PerformanceRating","YearsInCurrentRole","YearsWithCurrManager"],axis=1)


# In[ ]:


df_n=df_new.select_dtypes(include=['number'])


# In[ ]:


df_n.head()


# # Finding Categorical Variable

# In[ ]:


df.describe(include='object')


# In[ ]:


df_object=df.select_dtypes(include=['object'])


# In[ ]:


df_object.head()


# # Dropping Dependant Variable

# In[ ]:


df_object.drop("Attrition",axis=1,inplace=True)


# In[ ]:


df_object.head()


# In[ ]:


df_object_FU=df_object


# # Getting Dummies or Hot encoding for Categorical Variable

# In[ ]:


list(df_object_FU.columns)


# In[ ]:


for column in list(df_object.columns):

    df_tmp=pd.get_dummies(df_object[column])
    df_object=pd.concat([df_object,df_tmp], axis=1)
    


# In[ ]:


df_object.head()


# In[ ]:


df_object.drop(list(df_object_FU.columns),axis=1,inplace=True)


# In[ ]:


df_object.head()


# In[ ]:


df_C=pd.concat([df_n,df_object],axis=1)


# In[ ]:


df_C.head()


# # Feature Selection

# In[ ]:


X=df_C.values


# In[ ]:



y=df.Attrition.values


# # Train Test Split

# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


# In[ ]:


X_test_FutureUse=X_test


# # Standardization & Scaling of Features

# In[ ]:


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_test = sc.fit_transform(X_test)
X_train=sc.fit_transform(X_train)


# # Logistic Regression

# In[ ]:


from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(X_train,y_train)


# # Prediction

# In[ ]:


y_pred=logreg.predict(X_test)


# In[ ]:


y_pred


# # Accuracy Calculation

# In[ ]:


from sklearn import metrics
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Accuracy:","\n",metrics.confusion_matrix(y_test, y_pred))
print("Classification Report:","\n",metrics.classification_report(y_test, y_pred))


# # Applying SVM

# In[ ]:


from sklearn.svm import SVC
svc=SVC() #Default hyperparameters
svc.fit(X_train,y_train)
y_pred=svc.predict(X_test)


# In[ ]:


print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Accuracy:","\n",metrics.confusion_matrix(y_test, y_pred))
print("Classification Report:","\n",metrics.classification_report(y_test, y_pred))

