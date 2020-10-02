#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
get_ipython().run_line_magic('matplotlib', 'inline')


# ## EDA, Processing and Selection

# In[ ]:


df_org = pd.read_csv('/kaggle/input/summeranalytics2020/train.csv')
df = df_org.copy()


# In[ ]:


df.head()


# In[ ]:


df.shape


# In[ ]:


df.dtypes


# In[ ]:


df.describe()


# In[ ]:


df.info()


# In[ ]:


msno.bar(df)


# Great! No missing Values!

# Dropping up column ID!

# In[ ]:


no_use_cols = ['Id']
df.drop(no_use_cols, inplace=True, axis=1)


# In[ ]:


df.shape


# Dropping Duplicates in Data!

# In[ ]:


df.drop_duplicates(inplace=True)
df.shape


# In[ ]:


df.describe()


# In[ ]:


nominal_columns = df.select_dtypes(include=['object']).columns.tolist()
nominal_columns


# In[ ]:


cont_columns = ['Age','DistanceFromHome','EmployeeNumber','MonthlyIncome','NumCompaniesWorked', 'PercentSalaryHike','TotalWorkingYears',
                 'TrainingTimesLastYear', 'YearsAtCompany', 'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager']
ordinal_columns = ['EnvironmentSatisfaction','JobInvolvement','JobSatisfaction','Education','Behaviour','CommunicationSkill','PerformanceRating','StockOptionLevel']
target_column = ['Attrition']


# In[ ]:


len(nominal_columns)+len(cont_columns)+len(ordinal_columns)+len(target_column)


# In[ ]:


plt.figure(figsize=(10,10))
sns.heatmap(df[cont_columns].corr(), cmap="YlGnBu")


# In[ ]:


df[cont_columns].hist(figsize=(10,10))


# - Age has a normal Distribution
# - There are variables with exponential distribution.

# In[ ]:


sns.pairplot(df[cont_columns])


# In[ ]:


plt.figure(figsize=(10,10))
sns.heatmap(df[ordinal_columns].corr(), cmap="YlGnBu")


# Behaviour is constant!  
# Better drop it!

# In[ ]:


df.drop(['Behaviour'], inplace=True, axis = 1)
ordinal_columns.remove('Behaviour')


# In[ ]:


df.columns


# ### Let's see how does categorical variables actually affect attrition!

# In[ ]:


df_temp = pd.get_dummies(df, columns=['Attrition'])
for i in nominal_columns+ordinal_columns:
    m = df_temp.pivot_table(columns=i, values = ['Attrition_1','Attrition_0'], aggfunc=np.sum)
    m.loc['PercentAttrit'] = 0
    for a in m:
        m.loc['PercentAttrit'][a] = ((m[a][1])/(m[a][0]+m[a][1]))*100
    print(m)
    print("")


# Let's have some treat for eyes! Let's paint some Graphs.

# In[ ]:


plt.figure(figsize=(20,5))
total = float(len(df))
ax = sns.countplot(x = pd.cut(df.Age, bins = [0,26,32,36,40,np.inf], labels=[0,1,2,3,4]), hue = df['Attrition'])
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **We can infer that people in 20s, early 30s and above 40s are more likeyly to leave the job. Age is an important factor**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.BusinessTravel, hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.BusinessTravel, x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **Employees who have to travel frequently have higher attrition as compared to ones who travelrarely. In contrast, Non Travel employees have very low rate of attrition**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.DistanceFromHome)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.DistanceFromHome)


# **Employees who live far away from home have a higher rate of attrition.**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.EmployeeNumber)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.EmployeeNumber)


# **Attrition happens on evvery level here. Although there is slight difference in IQR.**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.EnvironmentSatisfaction, hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.EnvironmentSatisfaction, x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **There is higher attrition where there is low environment satisfaction. Attrition rate begins to decrease as we move towards high level of envrionment satisfaction. Alsmost similar at levels 3 and 4**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.JobSatisfaction, hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.JobSatisfaction, x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **Job Satisfaction distribution is almost identical to Environment Satisfaction**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.JobInvolvement, hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.JobInvolvement, x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **Trend is somewhat similar. Attrtion Rate decreases as scale moves towards right.**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.Gender, hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.Gender, x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **Females have slightly lesser Attrition Rate than males**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.MaritalStatus, hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.MaritalStatus, x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **Singles are more likely to leave job followed by Divorced. Married Employees are likely to stay**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.OverTime, hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.OverTime, x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **Employees who do overtime are more likely to leave.**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.NumCompaniesWorked)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.NumCompaniesWorked)


# **Employees who have jumped companies once are more likely to leave the job. Employees who jump companies alot are more like to leave.**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.PercentSalaryHike)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.PercentSalaryHike)


# **Distribution of Salary hike looks pretty much similar. On the higher side of hike, employees are likely to stay!**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.PerformanceRating, hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.PerformanceRating, x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **All employyes have performance rating of either 3 or 4. Attrition at both levels look failry similar.**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.StockOptionLevel, hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.StockOptionLevel, x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **Employees who own stocks are less likely to leave as compared to ones who don't have any**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.CommunicationSkill, hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.CommunicationSkill, x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **Distribution is fairly similar at all levels with slight difference.** 

# In[ ]:


plt.figure(figsize=(20,32))
plt.subplot(4,1,1)
ax = sns.countplot(x = df.JobRole, hue=df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(4,1,2)
ax = sns.countplot(x = df.Department, hue=df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(4,1,3)
ax = sns.countplot(x = df.Education, hue=df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(4,1,4)
ax = sns.countplot(x = df.EducationField, hue=df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# **Due to High Correlation among Department and JobRole, we can drop Department. Also, Education doesn't affect attrition rate significantly.**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.TotalWorkingYears)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.TotalWorkingYears)


# **Employees in initial years of their working life are more likely to leave.**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.YearsAtCompany)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.YearsAtCompany)


# **Employees in early years of company are more likely to leave**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.TrainingTimesLastYear)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.TrainingTimesLastYear)


# **Employees who have received lesser training tend to stay, compared to those who have received more training.**

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.YearsInCurrentRole)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.YearsInCurrentRole)


# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.YearsSinceLastPromotion)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.YearsSinceLastPromotion)


# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.YearsWithCurrManager)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.YearsWithCurrManager)


# ### Visualizing a few engineered features

# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df.StockOptionLevel.apply(lambda x: 0 if x == 0 else 1), hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = df.StockOptionLevel.apply(lambda x: 0 if x == 0 else 1), x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.TotalWorkingYears / df.Age)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.TotalWorkingYears / df.Age)


# **Observation from Profile: Employee number has unique values.! Strangeeee**

# In[ ]:


df.EducationField.unique()


# In[ ]:


df.JobRole.unique()


# In[ ]:


for ef in df.EducationField.unique():
    print(ef)
    print('='*50)
    print(df[df.EducationField == ef].JobRole.value_counts())
    print()


# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.YearsWithCurrManager / (df.YearsAtCompany + 1))
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.YearsWithCurrManager / (df.YearsAtCompany + 1))


# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.YearsInCurrentRole / (df.YearsAtCompany + 1))
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.YearsInCurrentRole / (df.YearsAtCompany + 1))


# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.Education / (df.Age + df.TotalWorkingYears))
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.Education / (df.Age + df.TotalWorkingYears))


# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = pd.cut(df.Age, bins = [0,27,45,np.inf], labels=['Young','Mid','Old']), hue = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(hue = pd.cut(df.Age, bins = [0,26,50,np.inf], labels=['Young','Mid','Old']), x = df.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# In[ ]:


df_temp = df.copy()
q_pays = dict()
for role in df.JobRole.unique():
    q_pays[role] =  df_temp[df_temp.JobRole == role].MonthlyIncome.quantile(0.4)

print(q_pays)
df_temp['paid_enough'] = df_temp.apply(lambda x: 'No' if x.MonthlyIncome < q_pays.get(x.JobRole) else 'Yes', axis = 1)

plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df_temp.paid_enough, hue = df_temp.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(x = df_temp.Attrition, hue = df_temp.paid_enough)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# In[ ]:


df_temp = df.copy()

def q25(x):
            return x.quantile(0.25)
def q50(x):
            return x.quantile(0.5)
def q75(x):
            return x.quantile(0.75)
    
def paid_enough(pay, qtiles):
    if pay <= qtiles[0]:
        return '25 or less'
    if pay <= qtiles[1]:
        return '25 to 50'
    if pay <= qtiles[2]:
        return '50-75'
    return '75 or above'


q_pays = dict()
for role in df.JobRole.unique():
    qtiles = [q25, q50, q75]
    q_pays[role] =  df_temp[df_temp.JobRole == role].MonthlyIncome.agg([q25, q50, q75]).to_list()

print(q_pays)
df_temp['paid_enough'] = df_temp.apply(lambda x: paid_enough(x.MonthlyIncome, q_pays[x.JobRole]), axis = 1)

plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
ax = sns.countplot(x = df_temp.paid_enough, hue = df_temp.Attrition)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")
plt.subplot(1,2,2)
ax = sns.countplot(x = df_temp.Attrition, hue = df_temp.paid_enough)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total),
            ha="center")


# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = (df.EnvironmentSatisfaction+df.JobSatisfaction+df.JobInvolvement) / 15)
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = (df.EnvironmentSatisfaction+df.JobSatisfaction+df.JobInvolvement) / 10)


# In[ ]:


plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
sns.boxplot(x = df.Attrition, y = df.YearsAtCompany/(df.PercentSalaryHike+1))
plt.subplot(1,2,2)
sns.violinplot(x = df.Attrition, y = df.YearsAtCompany/(df.PercentSalaryHike+1))


# ### Feature Selection

# In[ ]:


from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier


# In[ ]:


df_sel = df_org.copy()
no_use_cols = ['Id','Behaviour','Gender','Education', 'PerformanceRating', 'EmployeeNumber']
df_sel.drop(no_use_cols, inplace=True, axis=1)
df_sel.drop_duplicates(inplace=True)
df_sel = pd.get_dummies(df_sel, columns=df_sel.select_dtypes(include='object').columns.to_list())
X = df_sel.drop(['Attrition'], axis=1)
y = df_sel['Attrition']
rfe = RFE(RandomForestClassifier(), 20)
rfe.fit(X, y)
df_sel.drop(['Attrition'], axis=1).columns[rfe.get_support()]


# In[ ]:


df_sel = df_org.copy()
no_use_cols = ['Id','Behaviour','PerformanceRating','Gender','Education', 'TrainingTimesLastYear','PercentSalaryHike','Department', 'EmployeeNumber']
df_sel.drop(no_use_cols, inplace=True, axis=1)
df_sel.drop_duplicates(inplace=True)
df_sel = pd.get_dummies(df_sel, columns=df_sel.select_dtypes(include='object').columns.to_list())
X = df_sel.drop(['Attrition'], axis=1)
y = df_sel['Attrition']
rfe = RFE(RandomForestClassifier(), 20)
rfe.fit(X, y)
df_sel.drop(['Attrition'], axis=1).columns[rfe.get_support()]


# ### Feature Engineering and Profiling

# In[ ]:


df_mod = df_org.copy()
no_use_cols = ['Id',
               'Behaviour',
               'PerformanceRating',
               'Gender',
               'Education', 
               'Department',
               'EmployeeNumber']
df_mod.drop(no_use_cols, inplace=True, axis=1)
df_mod.drop_duplicates(inplace=True)

import pandas_profiling
profile = df_mod.profile_report(title='Employee_Attrition_Profile_Dataset')
profile.to_notebook_iframe()


# In[ ]:


df_mod = df_org.copy()
df_mod['OwnStocks'] = df_mod.StockOptionLevel.apply(lambda x: 0 if x == 0 else 1)
df_mod['PropWorkLife'] = df_mod.TotalWorkingYears / df_mod.Age
df_mod['PropExpComp'] = df_mod.NumCompaniesWorked/ (df_mod.TotalWorkingYears+1)
df_mod['AgeBar'] = pd.cut(df_mod.Age, bins = [0,27,45,np.inf], labels=['Young','Mid','Old']).astype('object')
df_mod['PropRoleComp'] = df_mod.YearsInCurrentRole / (df_mod.YearsAtCompany + 1)
q_pays = {
        'Laboratory Technician': 2705.0, 
        'Manufacturing Director': 5824.4000000000015, 
        'Sales Executive': 5675.8, 
        'Research Scientist': 2693.4, 
        'Sales Representative': 2325.8, 
        'Healthcare Representative': 6348.6, 
        'Research Director': 15014.600000000002, 
        'Human Resources': 2741.0, 
        'Manager': 16894.0
    }
df_mod['AboveQPay'] = df_mod.apply(lambda x: 'No' if x.MonthlyIncome < q_pays.get(x.JobRole) else 'Yes', axis = 1)
df_mod['WorkFactors'] = (df_mod.EnvironmentSatisfaction+df_mod.JobSatisfaction+df_mod.JobInvolvement) / 15

no_use_cols = [
                    'Id',
                    'Behaviour',
                    'PerformanceRating',
                    'Gender',
                    'Education', 
                    'Department',
                    'EmployeeNumber',
                    'PercentSalaryHike',
                    'YearsInCurrentRole',
                    'YearsSinceLastPromotion',
                    'YearsWithCurrManager',
                    'TrainingTimesLastYear',
                    'EducationField',
                    'StockOptionLevel',
                    'TotalWorkingYears',
                    'YearsAtCompany',
                    #'NumCompaniesWorked',
                    #'JobSatisfaction',
                    #'EnvironmentSatisfaction',
                    'Age',
                    #'MonthlyIncome',
                  ]
df_mod.drop(no_use_cols, inplace=True, axis=1)
df_mod.drop_duplicates(inplace=True)

import pandas_profiling
profile = df_mod.profile_report(title='Employee_Attrition_Profile_Dataset')
profile.to_notebook_iframe()


# ## Training

# In[ ]:


df = pd.read_csv('/kaggle/input/summeranalytics2020/train.csv')
dft = pd.read_csv('/kaggle/input/summeranalytics2020/test.csv')


# In[ ]:


def extract_feature(df_input):
    df = df_input.copy()
    df['OwnStocks'] = df.StockOptionLevel.apply(lambda x: 'No' if x == 0 else 'Yes')
    df['PropWorkLife'] = df.TotalWorkingYears / df.Age
    df['PropExpComp'] = df.NumCompaniesWorked / (df.TotalWorkingYears+1)
    df['PropRoleComp'] = df.YearsInCurrentRole / (df.YearsAtCompany + 1)
    df['AgeBar'] = pd.cut(df.Age, bins = [0,27,45,np.inf], labels=['Young','Mid','Old']).astype('object')
    q_pays = {
        'Laboratory Technician': 2705.0, 
        'Manufacturing Director': 5824.4000000000015, 
        'Sales Executive': 5675.8, 
        'Research Scientist': 2693.4, 
        'Sales Representative': 2325.8, 
        'Healthcare Representative': 6348.6, 
        'Research Director': 15014.600000000002, 
        'Human Resources': 2741.0, 
        'Manager': 16894.0
    }
    #df['AboveQPay'] = df.apply(lambda x: 'No' if x.MonthlyIncome < q_pays.get(x.JobRole) else 'Yes', axis = 1)
    #df['WorkFactors'] = (df.EnvironmentSatisfaction+df.JobSatisfaction+df.JobInvolvement) / 15
    cols_to_drop = [
                    'Id',
                    'Behaviour',
                    'PerformanceRating',
                    'Gender',
                    'Education', 
                    'Department',
                    'EmployeeNumber',
                    'PercentSalaryHike',
                    'YearsInCurrentRole',
                    'YearsSinceLastPromotion',
                    'YearsWithCurrManager',
                    'TrainingTimesLastYear',
                    'EducationField',
                    'StockOptionLevel',
                    'TotalWorkingYears',
                    'YearsAtCompany',
                    'NumCompaniesWorked',
                    'Age',
                    #'MonthlyIncome',
                    ]
    df.drop(cols_to_drop, inplace = True, axis = 1)
    print('Columns Dropped : {}'.format(cols_to_drop))
    print('Columns in DataFrame: {}'.format(df.columns.to_list()))
    return df


# In[ ]:


df_cleaned = extract_feature(df)
dft_cleaned = extract_feature(dft)


# In[ ]:


df_cleaned.drop_duplicates(inplace=True)


# In[ ]:


df_X = df_cleaned.drop(['Attrition'], axis = 1).copy()
df_y = df_cleaned[['Attrition']].copy()


# In[ ]:


nominal_type = list(df_X.select_dtypes(include='object').columns)
nominal_type


# In[ ]:


nominal_type_vals = dict()
for ot in nominal_type:
    nominal_type_vals[ot] = list(df_X[ot].unique())
print(nominal_type_vals)


# In[ ]:


numerical_type = list(df_X.select_dtypes(exclude='object').columns)
numerical_type


# In[ ]:


ordinal_type = list()
ordinal_columns_dataset = ['EnvironmentSatisfaction',
                           'JobInvolvement',
                           'JobSatisfaction',
                           'Education',
                           'Behaviour',
                           'CommunicationSkill',
                           'PerformanceRating',
                           'StockOptionLevel',
                          ]
for col in ordinal_columns_dataset:
    if col in numerical_type:
        numerical_type.remove(col)
        ordinal_type.append(col)
        
ordinal_type


# In[ ]:


final_cols = list(df_X.columns)
final_cols


# In[ ]:


numerical_index = list()
nominal_index = list()
ordinal_index = list()

for col in numerical_type:
    numerical_index.append(final_cols.index(col))
for col in nominal_type:
    nominal_index.append(final_cols.index(col))
for col in ordinal_type:
    ordinal_index.append(final_cols.index(col))

print('Numerical Columns')
for i,col in zip(numerical_index, numerical_type):
    print(i, col)
print('='*50)
print('Nominal Columns')
for i,col in zip(nominal_index, nominal_type):
    print(i, col)
print('='*50)
print('Ordinal Columns')
for i,col in zip(ordinal_index, ordinal_type):
    print(i, col)


# In[ ]:


df_X.describe()


# In[ ]:


X_train_full = df_X.copy()
y_train_full = df_y.copy()


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_val,y_train,y_val = train_test_split(df_X, df_y, test_size=0.20, random_state = 0, stratify=df_y)


# In[ ]:


from imblearn.over_sampling import SMOTENC
sampler = SMOTENC(categorical_features= nominal_index + ordinal_index, k_neighbors=3, random_state=0, sampling_strategy=0.7)
X_train, y_train = sampler.fit_resample(X_train, y_train)
X_train_full, y_train_full = sampler.fit_resample(X_train_full, y_train_full)


# In[ ]:


from catboost import CatBoostClassifier, Pool
from catboost import cv

cv_dataset = Pool(data=X_train,
                  label=y_train,
                  cat_features=nominal_index)


# In[ ]:


params = {"iterations": 200,
          "depth": 8,
          "learning_rate" : 0.06,
          "loss_function": "Logloss",
          "eval_metric":'AUC',
          "od_type" : "Iter",
          "od_wait" : 100,
          "l2_leaf_reg" : 20,
          "bagging_temperature":7,
          "bootstrap_type":"Bayesian",
          "random_strength": 10,
          "verbose": False
         }


# In[ ]:


scores = cv(cv_dataset,
            params,
            fold_count=5, 
            stratified=True,
            plot="True")


# In[ ]:


model = CatBoostClassifier(iterations=params['iterations'],
                           depth=params['depth'],
                           learning_rate=params['learning_rate'],
                           loss_function=params['loss_function'],
                           od_type = params['od_type'],
                           eval_metric =params['eval_metric'],
                           od_wait = params['od_wait'],
                           cat_features=nominal_index,
                           l2_leaf_reg = params['l2_leaf_reg'],
                           bagging_temperature = params["bagging_temperature"],
                           bootstrap_type = params["bootstrap_type"],
                           random_strength = params["random_strength"],
                           verbose=False
                          )
model.fit(X_train, y_train, eval_set=(X_val, y_val), plot=True)


# In[ ]:


model = CatBoostClassifier(iterations=params['iterations'],
                           depth=params['depth'],
                           learning_rate=params['learning_rate'],
                           loss_function=params['loss_function'],
                           od_type = params['od_type'],
                           eval_metric =params['eval_metric'],
                           od_wait = params['od_wait'],
                           cat_features=nominal_index,
                           l2_leaf_reg = params['l2_leaf_reg'],
                           bagging_temperature = params["bagging_temperature"],
                           bootstrap_type = params["bootstrap_type"],
                           random_strength = params["random_strength"],
                           verbose=False
                          )
model.fit(X_train_full, y_train_full)


# In[ ]:


X_test = dft_cleaned.copy()


# In[ ]:


def test_model_perf(model, X):
    predictions_df = pd.DataFrame(model.predict_proba(X),columns=['No_Attrition','Attrition'], index=range(1,471))
    predictions_df.No_Attrition = predictions_df.No_Attrition.apply(lambda x: np.around(x,7))
    predictions_df.Attrition = predictions_df.Attrition.apply(lambda x: np.around(x,7))
    predictions_df.index.name = 'Id'
    final_df = predictions_df[['Attrition']]
    return final_df


# In[ ]:


predictions_df = test_model_perf(model, X_test)
predictions_df.to_csv('submission.csv')

