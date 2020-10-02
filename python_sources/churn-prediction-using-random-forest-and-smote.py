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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
ax,figsize=(16,10)
 
# Any results you write to the current directory are saved as output.


# In[ ]:


data=pd.read_csv('../input/WA_Fn-UseC_-Telco-Customer-Churn.csv')


# In[ ]:


data.head(20)


# In[ ]:


#create a copy of the data frame
df1=data.copy()


# In[ ]:


df1['TotalCharges']=pd.to_numeric(df1['TotalCharges'], errors='coerce')


# In[ ]:


df1.isnull().sum()


# In[ ]:


#there are missing values present in the dataset and imputing them with the median of values
df1['TotalCharges'] = df1['TotalCharges'] .fillna((df1['TotalCharges'] .median()))


#  we can see there are only 16% of the senior citizens and the rest are younger people

# In[ ]:


#senior citizes vs the churn rate
import matplotlib.ticker as mtick # For specifying the axes tick format 
ax = (df1['SeniorCitizen'].value_counts()*100.0 /len(df1)).plot.pie(autopct='%.1f%%', labels = ['No', 'Yes'],figsize =(5,5), fontsize = 12 )                                                                           
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_ylabel('Senior Citizens',fontsize = 12)
ax.set_title('% of Senior Citizens', fontsize = 12)


# In[ ]:


def kdeplot(feature):
    plt.figure(figsize=(9, 4.5))
    plt.title("KDE for {}".format(feature))
    ax0 = sns.kdeplot(df1[df1['Churn'] == "No"][feature], color= 'navy', label= 'Churn: No')
    ax1 = sns.kdeplot(df1[df1['Churn'] == "Yes"][feature], color= 'orange', label= 'Churn: Yes')
kdeplot('tenure')
kdeplot('MonthlyCharges')
kdeplot('TotalCharges')


# we can see that from the graph that there is higher people with people without churn has the higher churn rate

# From the above graph we can infer that
# 1. For the first graph i.e  we can see that there is higher churn for the recently joined customers
# 2. For the second graph i.e  we can see there is higher churn rate for the people whoe monthly charges are between 800-1200
# 3. For the third graph i.e for the we can see that higher churn rate for the people for popele whose total charges are between 2000-6000

# In[ ]:


# g=sns.PairGrid(df1[['MonthlyCharges','TotalCharges','tenure']],hue='Churn')
g = sns.PairGrid(df1[['MonthlyCharges','TotalCharges','tenure']])
g = g.map(plt.scatter)


# **3.categorical variables**
# #Gender and age distribtuion

# In[ ]:


ax=sns.countplot(x='SeniorCitizen',hue='Churn',data=df1)
ax.set_ylabel('seniorCitizen')
ax.set_xlabel('Churn')
ax.set_title('Senior Citizen vs Churn')


# In[ ]:


g = sns.FacetGrid(df1, row='SeniorCitizen', col="gender", hue="Churn", height=3.5)
g.map(plt.scatter, "tenure", "MonthlyCharges", alpha=0.6)
g.add_legend();


# In[ ]:


#3.2 Dependants and their partners
ax1=sns.countplot(x='Dependents',hue='Churn',data=df1)
ax1.set_ylabel('Dependents')
ax1.set_xlabel('Churn')
ax1.set_title('Dependents vs Churn')


# In[ ]:


ax2=sns.countplot(x='Partner',hue='Churn',data=df1)
ax2.set_ylabel('Partner')
ax2.set_xlabel('Churn')
ax2.set_title('Partner vs Churn')


# **3.3. Phone and internet services**

# In[ ]:


plt.figure(figsize=(9,4.5))
ax3=sns.countplot(x='MultipleLines',data=df1)


# In[ ]:


#least chekc how these will effect the monthly charges
sns.boxplot(x='MultipleLines',y='MonthlyCharges',hue='Churn',data=df1,palette="Set2")


# In[ ]:


#intrenet Servies
plt.figure(figsize=(9,4.5))
ax4=sns.countplot(x='InternetService',hue='Churn',data=df1)


# In[ ]:


sns.boxplot(x='InternetService',y='MonthlyCharges',hue='Churn',data=df1,palette="Set2")


# In[ ]:


# we can observe that there is higher churn rate fot the Fiber optic and higher the monthly charges there is more ie. greater than 80 like to have more churn


# In[ ]:


#lets observe about the payments
plt.figure(figsize=(9, 4.5))
ax5=sns.countplot(x="PaymentMethod",hue='Churn',data=df1)


# We can observe a very high churn for the customers who have mead electronic check payment method

# In[ ]:


#payment vs contract
g = sns.FacetGrid(data=df1, col="PaperlessBilling",hue='Churn',height=4, aspect=.9)
ax = g.map(sns.countplot, "Contract",palette = "Blues_d", order= ['Month-to-month', 'One year', 'Two year'])


# In[ ]:


sns.boxplot(x='Contract',y='MonthlyCharges',hue='Churn',data=df1,palette="Set2")


# In[ ]:


ax=sns.boxplot(x="MonthlyCharges",y="PaymentMethod", hue="Churn",data=df1,orient='h',palette="Set1")
ax.legend(loc='upper right')


# In[ ]:


#drop the CustomerID
df1.drop(['customerID'],axis=1,inplace=True)


# In[ ]:


import seaborn as sns
plt.figure(figsize=(15,8))
corr=df1.corr()
sns.heatmap(corr,annot=True)


# In[ ]:


df1=pd.get_dummies(df1, columns=['gender','SeniorCitizen','Partner','Dependents','PhoneService','MultipleLines','InternetService','OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies','Contract','PaperlessBilling','PaymentMethod'])


# In[ ]:


#there are some redundant features which are to be removed from the model
df1=df1.drop(columns=[
'OnlineSecurity_No','TechSupport_No','OnlineBackup_No','gender_Female','PaperlessBilling_No',
    'MultipleLines_No','StreamingMovies_No','Partner_No','Dependents_No','SeniorCitizen_1',
    'StreamingTV_No','PhoneService_No','PhoneService_Yes','MultipleLines_No phone service',
    'TechSupport_No internet service','StreamingTV_No internet service',
    'OnlineSecurity_No internet service','OnlineBackup_No internet service',
    'StreamingMovies_No internet service','DeviceProtection_No internet service',
    'InternetService_No'],axis=1)


# In[ ]:


from sklearn.model_selection import train_test_split
y=df1['Churn']
X=df1.drop(['Churn'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns =X_train.columns


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
m1= RandomForestClassifier(n_estimators=50, min_samples_leaf=3, max_features=0.7, n_jobs=-1, oob_score=True)
m1.fit(X_train,y_train)
m1.score(X_test,y_test)


# In[ ]:


feature_importances = pd.DataFrame(m1.feature_importances_,
                                   index = X_train.columns,
                                    columns=['importance']).sort_values('importance',ascending=False)
feature_importances


# In[ ]:


#apply the smote to overcome the problem of data imbalance
from imblearn.over_sampling import SMOTE


# In[ ]:


os = SMOTE(random_state=41)

os_data_X,os_data_y=os.fit_sample(X_train,y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns )
os_data_y= pd.DataFrame(data=os_data_y,columns=["Churn"])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of yes in oversampled data",len(os_data_y[os_data_y["Churn"]=='Yes']))
print("No.of No transcation",len(os_data_y[os_data_y["Churn"]=='No']))
print("Proportion of churn yes data in oversampled data is ",len(os_data_y[os_data_y["Churn"]=='Yes'])/len(os_data_X))
print("Proportion of no data in oversampled data is ",len(os_data_y[os_data_y["Churn"]=='No'])/len(os_data_X))


# In[ ]:


from sklearn.model_selection import train_test_split
y=os_data_y
X=os_data_X
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns =X_train.columns


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=50, min_samples_leaf=3, max_features=0.5, n_jobs=-1, oob_score=True)
clf.fit(X_train,y_train)


# In[ ]:


clf.score(X_test,y_test)


# we can observe that there is an increase of 5% accuracy from 80 to 86% because of the smote sampling that is followed above

# In[ ]:


feature_importances = pd.DataFrame(clf.feature_importances_,
                                   index = X_train.columns,
                                    columns=['importance']).sort_values('importance',ascending=False)
feature_importances

