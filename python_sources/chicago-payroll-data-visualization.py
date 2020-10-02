#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Read data into a dataframe
chi_payroll=pd.read_csv('../input/Current_Employee_Names__Salaries__and_Position_Titles.csv')
print('First two rows')
print(chi_payroll.head(2))
print('===========')
print('Column Names')
print(chi_payroll.columns)
print('===========')
print('Data rows & columns')
print(chi_payroll.shape)
print('===========')
print('Count, mean etc of numerical value')
print(chi_payroll.describe())
print('===========')


# In[ ]:


#Finding out Null values in the data
print(chi_payroll.isnull().sum().sort_values(ascending=False))


# Hourly Rate and Typical hours can be null for Full time employees. we will need to further investigate Annual salary

# In[ ]:



print(chi_payroll['Hourly Rate'].isnull().groupby(chi_payroll['Full or Part-Time']).sum())
print(chi_payroll['Typical Hours'].isnull().groupby(chi_payroll['Full or Part-Time']).sum())


# As we suspected Hourly Rate & Typical hours are null for full time employees we can impute them with 0. We will need to take a look at part time employees having these fields 0.

# In[ ]:


chi_payroll['Currency'],chi_payroll['Hourly Rate']=chi_payroll['Hourly Rate'].str.split('$',1).str
chi_payroll[['Hourly Rate']]=chi_payroll[['Hourly Rate']].astype(float)
chi_payroll['CurrencySalary'],chi_payroll['Annual Salary']=chi_payroll['Annual Salary'].str.split('$',1).str
chi_payroll[['Annual Salary']]=chi_payroll[['Annual Salary']].astype(float)
print(chi_payroll['Annual Salary'].dtype)


# In[ ]:



print(chi_payroll.loc[(chi_payroll['Full or Part-Time'] == 'P') & (chi_payroll['Hourly Rate'].isnull())])


# I am assuming that since the employees are getting an Annual salary they are marked as part time by mistake. I will change the value to Full time and then impute Hourly Rate & Typical Hours to 0. 

# In[ ]:


chi_payroll['Full or Part-Time'] = np.where(chi_payroll['Hourly Rate'].isnull(),'F','P')
#print(chi_payroll['Hourly Rate'].isnull().groupby(chi_payroll['Full or Part-Time']).sum())
#print(chi_payroll['Typical Hours'].isnull().groupby(chi_payroll['Full or Part-Time']).sum())


# In[ ]:


#Changing the Hourly Rate & Typical Hours to 0
chi_payroll['Hourly Rate'].fillna(0,inplace=True)
chi_payroll['Typical Hours'].fillna(0,inplace=True)
#print(chi_payroll['Hourly Rate'].isnull().groupby(chi_payroll['Full or Part-Time']).sum())
#print(chi_payroll['Typical Hours'].isnull().groupby(chi_payroll['Full or Part-Time']).sum())


# Now checking if annual salary is null for part time employees, and chaging it to 0

# In[ ]:


print(chi_payroll['Annual Salary'].isnull().groupby(chi_payroll['Full or Part-Time']).sum())


# In[ ]:


chi_payroll['Annual Salary'].fillna(0,inplace=True)
print(chi_payroll.isnull().sum().sort_values(ascending=False))


# Now the data doesnot contain any null value. Let's encode the categorical variables and find relation ship among them

# In[ ]:





# In[ ]:


#Visualising the salary for part time employees

#pd.to_numeric(chi_payroll['Hourly Rate_int'])


f1=plt.figure()
sns.countplot('Typical Hours',data=chi_payroll,hue='Full or Part-Time')
f2=plt.figure()
#b=sns.stripplot(x='Typical Hours',y='Hourly Rate',data=chi_payroll,jitter=True,size=8)

sns.stripplot(x='Typical Hours',y='Hourly Rate',data=chi_payroll,jitter=True,size=8)
#print((chi_payroll['Hourly Rate']))
#b.set_ylim(min(chi_payroll['Hourly Rate']),max(chi_payroll['Hourly Rate']))


# In[ ]:



#print(chi_payroll['Hourly Rate_int'].dtype)
#print(chi_payroll['Typical Hours'].dtype)

sns.violinplot(x='Typical Hours',y='Hourly Rate',data=chi_payroll)


# 
# Visualizing employee departments and salary 

# In[ ]:




#grid = sns.FacetGrid(chi_payroll, row='Department', size=2.2, aspect=1.6)
#grid.map(plt.bar, 'Typical Hours','Hourly Rate')#,palette='deep')
#grid.add_legend()
g = sns.factorplot(x="Department", y="Hourly Rate",col="Typical Hours",data=chi_payroll, kind="box",        col_wrap=2,size=10, aspect=.7)


# In[ ]:


f1=plt.figure()
g = sns.factorplot(x="Hourly Rate",y="Typical Hours",hue='Department',data=chi_payroll, kind="violin")


# In[ ]:


f2=plt.figure()
f2.set_size_inches(20, 10)
g = sns.violinplot(y='Annual Salary',x='Department',data=chi_payroll)
plt.xticks(rotation=45)


# In[ ]:


f2=plt.figure()
f2.set_size_inches(20, 10)
g = sns.boxplot(y='Annual Salary',x='Department',data=chi_payroll)
plt.xticks(rotation=45)


# I will compute average annual salary in each department to clarify  which departments are paid more in general

# In[ ]:


f2=plt.figure()
#f2.set_size_inches(20, 10)
Annualsalary_group=chi_payroll.groupby('Department',as_index=False)['Annual Salary'].mean()
#print(Annualsalary_group)
Annualsalary_group.plot(y='Annual Salary',x='Department',kind='bar',figsize=(25,10))
plt.xticks(fontsize=20)
#tick.label.set_fontsize(14) 
plt.show()


# In[ ]:


f2=plt.figure()
#f2.set_size_inches(20, 10)
HRate_group=chi_payroll.groupby('Department',as_index=False)['Hourly Rate'].max()
HRate_group.plot(y='Hourly Rate',x='Department',kind='bar',figsize=(20,10))
plt.xticks(fontsize=20)
plt.show()


# It seems like COPA,IT and buildings have the highest average annual salary whereas Health department pays contractors the maximum amount of houry rate. It is interesting to note that IT, COPA and Buildings department do not hire contractors.
# Now let's analyse the relationship of annual salary & Job Title

# In[ ]:


#f2=plt.figure()
#f2.set_size_inches(20, 10)
#Annualsalary_title_group=chi_payroll.groupby('Job Titles',as_index=False)['Annual Salary'].mean()
#print(Annualsalary_group)
#Annualsalary_title_group.plot(x='Annual Salary',y='Job Titles',kind='bar',figsize=(25,25))
#plt.xticks(fontsize=20)
#tick.label.set_fontsize(14) 
#plt.show()

