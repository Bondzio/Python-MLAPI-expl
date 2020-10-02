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

# Any results you write to the current directory are saved as output.


# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
print(os.listdir("../input"))


# In[ ]:


empl_df = pd.read_csv("../input/HR-Employee-Attrition.csv")


# In[ ]:


empl_df.head()


# In[ ]:


empl_df.info()


# In[ ]:


empl_df.isna().sum()


# In[ ]:


empl_df.BusinessTravel.unique()


# In[ ]:


empl_df.Department.unique()


# 

# In[ ]:


empl_df.EducationField.unique()


# In[ ]:


empl_df.JobRole.unique()


# In[ ]:


empl_df.columns


# In[ ]:


cols_to_Encode = ["BusinessTravel","Department","EducationField","JobRole","MaritalStatus","Over18","OverTime"]
numeric_cols = ["Attrition", "Gender","Age","DailyRate","DistanceFromHome","Education","EmployeeCount","EmployeeNumber","EnvironmentSatisfaction","HourlyRate",
                "JobInvolvement","JobLevel","JobSatisfaction","MonthlyIncome","MonthlyRate","NumCompaniesWorked","PercentSalaryHike",
               "PerformanceRating","RelationshipSatisfaction","StandardHours","StockOptionLevel","TotalWorkingYears","TrainingTimesLastYear"
                ,"WorkLifeBalance","YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion","YearsWithCurrManager"]


# 

# In[ ]:


#Other way
# cat_col = emp_atr.select_dtypes(exclude=np.number).columns
# num_col = emp_atr.select_dtypes(include=np.number).columns


# 

# In[ ]:


empl_df['Attrition'] = empl_df['Attrition'].apply(lambda x: 1 if x=="Yes" else 0)
empl_df['Attrition'].value_counts()


# In[ ]:


empl_df['Gender'] = empl_df['Gender'].apply(lambda x: 1 if x=="Male" else 0)
empl_df['Gender'].value_counts()


# In[ ]:


print(cols_to_Encode)


# In[ ]:


print(numeric_cols)


# In[ ]:


encoded_cols = pd.get_dummies(empl_df[cols_to_Encode])


# In[ ]:


df_final = pd.concat([encoded_cols,empl_df[numeric_cols]], axis = 1)


# In[ ]:


df_final.head()


# In[ ]:


df_final.shape


# In[ ]:


empl_df.corr()


# In[ ]:


df_final.corr()


# In[ ]:


df_final.cov()


# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics


# In[ ]:


X=df_final.drop(columns=['Attrition'])
Y=df_final['Attrition']


# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
logreg = LogisticRegression()
logreg.fit(X_train, Y_train)


# In[ ]:


train_Pred = logreg.predict(X_train)


# In[ ]:


metrics.confusion_matrix(Y_train,train_Pred)


# In[ ]:


metrics.accuracy_score(Y_train,train_Pred)


# In[ ]:


test_Pred = logreg.predict(X_test)


# In[ ]:


metrics.confusion_matrix(Y_test,test_Pred)


# In[ ]:


from sklearn.metrics import classification_report
print(classification_report(Y_test, test_Pred))


# In[ ]:


metrics.accuracy_score(Y_test,test_Pred)

