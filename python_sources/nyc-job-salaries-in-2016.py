#!/usr/bin/env python
# coding: utf-8

# NYC Salaries Survey (in year 2016). Let's find out what Job categories were best paid. Don't get fustrated, that's my first Kernel, any comments are welcomme.  

# Easiest part import...

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


data = pd.read_csv('../input/jobpostings.csv')
data.head(1)


# In[ ]:


data.shape


# 3885 rows and 28 columns! Messy , manual worl with excel would take decades. Lenovo Intel(R) Core(TM) i5-8250U CPU 1.60 GHz, 8192 RAM and Pandas can process it fast.
# 

# In[ ]:


data.columns


# In[ ]:


data.info()


# There are 3884 job offers in 3884 rows. But 2 Job Categories has NuN values. Drop it, even they don't have statsistical matter.

# In[ ]:



data.dropna(subset=['Job Category'], inplace = True)
assert 1==1
data[['Job Category']].info()


# In[ ]:


data.describe()


# The main criterias in this survey we use are "Salary Range From" and "Salary Range To", only few of integers. In some positions minimum salary given is 0$ , that counts in the average(mean) and lowers it.
# 

# Its likely some offers are given per/hour but we estimate annual salaries. 
# So we need to do adjustments. Average  Salary From and To is expected to be greater than - 56048 $ and - 81294

# In[ ]:


a = data['Job Category']
b = data['Salary Range From']
c = data['Salary Range To']
data = pd.concat([a,b,c], axis=1)
data.index = np.arange(1, len(data)+1)
data.head(3)


# 35 $ per year, that's discreapancies, might be per/out , or  35000 $. Do the logical filtering Salary is geater than 1000 and iloc the names.
# 

# In[ ]:


pd.options.display.max_rows = 999
dt = data[(data['Salary Range From']>1000)]

print()
print("Maximum salary")
print(dt.max())

print()
print()
print("Minimum salary")
print(dt.min())
print()


dt = dt.groupby("Job Category").mean()
dt.reset_index(inplace=True)
dt.iloc[0:32, 0] = 'Administration & Human Resources'
dt.iloc[32:38, 0] = 'Building Operations & Maintenance'
dt.iloc[38:42, 0] = 'Clerical & Administrative Support'
dt.iloc[42:52, 0] = 'Communications & Intergovernmental Affairs'
dt.iloc[52:54, 0] = 'Community & Business Services'
dt.iloc[54:77, 0] = 'Constituent Services & Community Programs'
dt.iloc[77:90, 0] = 'Engineering, Architecture, & Planning'
dt.iloc[90:100, 0] = 'Finance, Accounting, & Procurement'
dt.iloc[100:114, 0] = 'Health'
dt.iloc[114:124, 0] = 'Legal Affairs'
dt.iloc[125:131, 0] = 'Legal Affairs'
dt.iloc[131:133, 0] = 'Public Safety, Inspections, & Enforcement'
dt.iloc[134:138, 0] = 'Technology, Data & Innovation'
dt = dt.groupby("Job Category").mean()

print()
print()
print("Salaries by Job categories - to max")
dt1 = dt.sort_values(by=['Salary Range To'], ascending=False)
dt1


# Top 3 best paid job categories: Enginering, IT, health and top 3 worst paid in : public safety, clerical & administrative support, maintenance & operations. I hope you are in one of those Top3(best paids). DATA ANALYTICS, thats on the number two.

# In[ ]:



dt1.plot.bar(stacked=True);


# Average salaries "From and To" in all categories varies about 24%. 

# In[ ]:



rep_plot = dt1.sort_values("Job Category").mean().plot(kind='bar')
rep_plot.set_xlabel("Job Category")
rep_plot.set_ylabel("Salary Range To")


# In[ ]:


pd.options.display.max_columns = 999
data2 = pd.read_csv('../input/jobpostings.csv')
data2.sort_values(by='Salary Range To', ascending=False).head(2)


# In[ ]:


pd.options.display.max_columns = 999
data2 = pd.read_csv('../input/jobpostings.csv')
data2.sort_values(by='Salary Range To', ascending=True).head(2)


# To conclude with. Minimum salary from maximum differs almost 9 times. Most of requirement for top 20 paid jobs are work experience 5-10(and above) years, preferably masters degree. For lowest paid jobs usualy there is no requirements. So salary depends on job categories, experience and education.

# In[ ]:




