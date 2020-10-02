#!/usr/bin/env python
# coding: utf-8

# Read the file which contains IBM employee data along with Attrition indicator, explore the data by creating plots and see if there is correlation between the independent variables ( age, distance from home, no# of years of service) has any effect on Attrition.
# Call libraries

# In[3]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os


# In[4]:


empatt = pd.read_csv("../input/WA_Fn-UseC_-HR-Employee-Attrition.csv")
empatt.head()


# In[5]:


# lets plot the data and look at it, ex: find the Age distribution of ppl in the dataset
sns.distplot(empatt['Age'], color = 'red')
plt.show()


# In[6]:


# Display multiple distribution plots.
fig,ax = plt.subplots(3,3, figsize=(10,10))
sns.distplot(empatt['YearsAtCompany'], ax = ax[0,0], color = 'cyan')   
sns.distplot(empatt['YearsInCurrentRole'], ax = ax[0,1],color = 'cyan')
sns.distplot(empatt['YearsSinceLastPromotion'], ax = ax[0,2],color = 'cyan')   
sns.distplot(empatt['YearsWithCurrManager'], ax = ax[1,0], color = 'cyan')
sns.distplot(empatt['TotalWorkingYears'], ax = ax[1,1], color = 'cyan')  
sns.distplot(empatt['TrainingTimesLastYear'], ax = ax[1,2], color = 'cyan')  
sns.distplot(empatt['WorkLifeBalance'], ax = ax[2,0], color = 'cyan')  
sns.distplot(empatt['DistanceFromHome'], ax = ax[2,1], color = 'cyan')  
sns.distplot(empatt['RelationshipSatisfaction'], ax = ax[2,2], color = 'cyan')  
plt.show()


# In[7]:


sns.countplot(empatt['Attrition'])
plt.show()


# In[8]:


#Bar plot of Job Satisfaction with respect to distance from home according to gender
#Estimator used is median
from numpy import median
sns.barplot(x='Attrition', y='MonthlyIncome', hue= 'Gender',data=empatt, estimator=median)
plt.show()


# In[9]:


# Box Plot
f,ax = plt.subplots(figsize=(15,10))
sns.boxplot(x='JobSatisfaction', y='MonthlyIncome', data=empatt, hue='JobLevel',palette='Set3')
plt.legend(loc='best')
plt.show()


# In[10]:


## Joint scatter plot
sns.jointplot(empatt.Age,empatt.MonthlyIncome, kind = "scatter")   
plt.show()


# In[98]:


g = sns.FacetGrid(empatt, col="JobSatisfaction", row="Gender")
g.map(sns.kdeplot, "MonthlyIncome", "YearsInCurrentRole")
plt.show()


# In[11]:


# Pair Plots
data1 = ['Attrition','Age','MonthlyIncome','DistanceFromHome']
sns.pairplot(empatt[data1], kind="reg", diag_kind = "kde" , hue = 'Attrition' )
plt.show()


# In[15]:


data2 = ['Gender', 'HourlyRate','DailyRate','MonthlyRate','PercentSalaryHike']
sns.pairplot(empatt[data2], kind="reg", diag_kind = "kde" , hue = 'Gender' )
plt.show()


# In[16]:


#Plot a correlation map for all numeric variables
f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(empatt.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()


# View the attrition based on different variables...

# In[17]:


total_records= len(empatt)
columns = ["Gender","MaritalStatus","WorkLifeBalance","EnvironmentSatisfaction","JobSatisfaction",
           "JobLevel","BusinessTravel","Department"]

j=0
for i in columns:
    j +=1
    plt.subplot(4,2,j)
    ax1 = sns.countplot(data=empatt,x= i,hue="Attrition")
    if(j==8 or j== 7):
        plt.xticks( rotation=90)
    for p in ax1.patches:
        height = p.get_height()
        ax1.text(p.get_x()+p.get_width()/2.,
                height + 3,
                '{:1.2f}'.format(height/total_records,0),
                ha="center",rotation=0) 

# Custom the subplot layout
plt.subplots_adjust(bottom=-0.9, top=2)
plt.show()


# In[ ]:




