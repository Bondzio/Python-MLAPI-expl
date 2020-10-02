#!/usr/bin/env python
# coding: utf-8

# # IBM Attrition Dataset Analysis

# # Importing Libraries

# In[ ]:


#Call libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from statsmodels.graphics.mosaicplot import mosaic
import os


# # Reading data

# In[ ]:


#read data
ibm = pd.read_csv("../input/WA_Fn-UseC_-HR-Employee-Attrition.csv", header = 0)


# # Basic view of data

# In[ ]:


#top rows
ibm.head()


# # Analysis/plotting of data

# # 1. Basic analysis of Attrition

# In[ ]:


atr_cnt = ibm["Attrition"].value_counts()

sns.countplot(atr_cnt)
plt.show()


# # 2. Plot of Attrition Rate by age groups

# In[ ]:


#mosaic plot
ibm.Age.max() #Max age
ibm.Age.min() #Min age

ibm['cat_age'] = pd.cut(ibm['Age'], 3, labels=['young', 'middle', 'old']) #Create categorical column for age grouped by low/middle/high
ibm.head()

from statsmodels.graphics.mosaicplot import mosaic
plt.rcParams['font.size'] = 12.0
mosaic(ibm, ['cat_age', 'Attrition'])
plt.show()


# # 3. Plot of Attrition Rate by rate of pay/income - DailyRate, HourlyRate, MonthlyRate, MonthlyIncome

# In[ ]:


#barplot
fig,ax = plt.subplots(2,2, figsize=(10,10))                       # 'ax' has references to all the four axes
sns.boxplot(ibm['Attrition'], ibm['DailyRate'], ax = ax[0,0])  # Plot on 1st axes 
sns.boxplot(ibm['Attrition'], ibm['HourlyRate'], ax = ax[0,1])  # Plot on IInd axes
sns.boxplot(ibm['Attrition'], ibm['MonthlyRate'], ax = ax[1,0])       # Plot on IIIrd axes
sns.boxplot(ibm['Attrition'], ibm['MonthlyIncome'], ax = ax[1,1])       # Plot on IVth axes
plt.show()


# # 4. Plot of Attrition Rate Department wise

# In[ ]:


#crosstable
ibm_cc = pd.crosstab(index=ibm["Attrition"], 
                          columns=ibm["Department"])


ibm_cc.plot(kind="bar", 
                 figsize=(8,8),
                 stacked=True)
plt.show()


# # 5. Plot of Attrition by Gender

# In[ ]:


#two-way table
grouped = ibm.groupby(['Attrition','Gender'])
gr = grouped.size()

gr.plot( kind = "line",
figsize=(8,8))
plt.show()


# # 6. Plot of Attrition Rate by Job related factors - JobRole, JobLevel

# In[ ]:


#facet grid
g=sns.FacetGrid(ibm,row='JobRole',col='JobLevel',size=2.2,aspect=1.6)
g.map(plt.hist,'Attrition')
g.add_legend()
plt.show()


# # 7. Plot of Attrition Rate by Working hrs - OverTime, StandardHours

# In[ ]:


# transform overtime from categorical to numeric

number = LabelEncoder()
ibm['OverTime_num'] = number.fit_transform(ibm['OverTime'].astype('str'))

no = ibm[ibm['Attrition'] == 'No']
yes = ibm[ibm['Attrition'] == 'Yes']

fig,ax = plt.subplots(2,2, figsize=(10,10))  # 'ax' has references to all the four axes
sns.barplot(no['OverTime_num'], ax = ax[0,0])  # Plot on 1st axes 
sns.barplot(no['StandardHours'], ax = ax[0,1])  # Plot on IInd axes
sns.barplot(yes['OverTime_num'], ax = ax[1,0])       # Plot on IIIrd axes
sns.barplot(yes['StandardHours'], ax = ax[1,1])       # Plot on IVth axes
plt.show()


# # 8. Plot of Attrition Rate by Growth - PercentSalaryHike, PerformanceRating

# In[ ]:


#dist plot

no = ibm[ibm['Attrition'] == 'No']
yes = ibm[ibm['Attrition'] == 'Yes']


fig,ax = plt.subplots(2,2, figsize=(10,10))  # 'ax' has references to all the four axes
sns.distplot(no['PercentSalaryHike'], ax = ax[0,0])  # Plot on 1st axes 
sns.distplot(no['PerformanceRating'], ax = ax[0,1])  # Plot on IInd axes
sns.distplot(yes['PercentSalaryHike'], ax = ax[1,0])       # Plot on IIIrd axes
sns.distplot(yes['PerformanceRating'], ax = ax[1,1])       # Plot on IVth axes
plt.show()


# # 9. Plot of Attrition Rate Emp factors related - TotalWorkingYears, YearsInCurrentRole

# In[ ]:


#count plot

fig,ax = plt.subplots(2,2, figsize=(10,10))  # 'ax' has references to all the four axes
sns.countplot(no['TotalWorkingYears'], ax = ax[0,0])  # Plot on 1st axes 
sns.countplot(no['YearsInCurrentRole'], ax = ax[0,1])  # Plot on IInd axes
sns.countplot(yes['TotalWorkingYears'], ax = ax[1,0])       # Plot on IIIrd axes
sns.countplot(yes['YearsInCurrentRole'], ax = ax[1,1])       # Plot on IVth axes
plt.show()

