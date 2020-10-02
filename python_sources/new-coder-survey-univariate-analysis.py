#!/usr/bin/env python
# coding: utf-8

# # 2016 New Coder Survey - Univariate Analysis
# 
# This is my first notebook for this data set, and covers only univariate analysis. To see multivariate exploratory analysis, please check my other notebook: [link](https://www.kaggle.com/narimiran/d/freecodecamp/2016-new-coder-survey-/exploratory-visualizations).
# 
# If you have any suggestions, critiques, etc. - please write them below in the comments, I would love to hear them. Thank you!

# # Imports and Settings

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams["axes.labelsize"] = 13
plt.rcParams["axes.labelweight"] = 'bold'
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
sns.set_style('whitegrid')


# # Loading and Overview

# In[ ]:


df = pd.read_csv('../input/2016-FCC-New-Coders-Survey-Data.csv', low_memory=False)
df.head()


# In[ ]:


df.shape


# In[ ]:


df.info()


# Univariate analysis will be separated in several parts, each having similar topics grouped together (Demographic, Education, Jobs and Employment).

# # Demographic

# ## Age

# In[ ]:


ax = df.Age.hist(bins=30)
_ = (ax.set_title('Age distribution'),
     ax.set_xlabel('Age'),
     ax.set_ylabel('Number of coders'))

age_median = df.Age.median()

_ = (ax.axvline(age_median, color='black', linewidth=2), 
     ax.text(age_median-0.5, 70, 
             'median = {:.0f} years'.format(age_median), 
             rotation=90, fontsize=13, fontweight='bold',
             horizontalalignment='right', verticalalignment='bottom'))


# It seems there are some very young (less than 16 years old) people, and few 60+ people. Let's explore that a bit:

# In[ ]:


print("The youngest coder: \t{:.0f} years old\n"
      "The oldest coder: \t{:.0f} years old".format(df.Age.min(), df.Age.max()))


# In[ ]:


df.Age[df.Age < 16].value_counts(sort=False)


# In[ ]:


df.Age[df.Age > 60].value_counts(sort=False)


# ## Gender

# In[ ]:


gender = df.Gender.value_counts(ascending=True)

ax = gender.plot(kind='barh', width=0.7)
_ = (ax.set_title('Gender Distribution'),
     ax.set_xlabel('Number of coders'))


# ## Marital Status

# In[ ]:


marital = df.MaritalStatus.value_counts(ascending=True)
ax = marital.plot(kind='barh', figsize=(7,5), width=0.7)

_ = (ax.set_title('Marital Status'),
     ax.set_xlabel('Number of coders'),
    )


# ## Children

# In[ ]:


ax = df.HasChildren.value_counts(sort=False).plot(kind='barh')
_ = (ax.set_title('Do Coders Have Children?'),
     ax.set_xlabel('Number of coders'),
     ax.set_yticklabels(["don't have children", 'have children'], rotation=90)
    )


# It would seem like majority of coders have children, but only 1/4 of the coders answered the question.
# 
# How many children do they have?

# In[ ]:


ax = df.ChildrenNumber.hist(bins=18)

_ = (ax.set_title('Number Of Children'),
     ax.set_xlabel('Children'),
     ax.set_ylabel('Number of coders'),
    )


# ## Financially Supporting

# In[ ]:


support = df.FinanciallySupporting.value_counts(sort=False)
ax = support.plot(kind='barh')

_ = (ax.set_title('Financially Supporting Dependants'),
     ax.set_xlabel('Number of coders'),
     ax.set_yticklabels(["not supporting", 'supporting'], rotation=90)
    )


# ## City Population

# In[ ]:


city = df.CityPopulation.value_counts(sort=True, ascending=True)

ax = city.plot(kind='bar', rot=0, width=0.6)
_ = (ax.set_title('City Population'), 
     ax.set_xlabel('City Size'), 
     ax.set_ylabel('Number of coders'))


# ## Country

# In[ ]:


citizen = df.CountryCitizen.value_counts(ascending=True)[-30:]

ax = citizen.plot(kind='barh', figsize=(7,12), width=0.7, logx=True)
_ = (ax.set_title('Top 30 Countries by Citizens'), 
     ax.set_xlabel('Number of coders (log)'))


# In[ ]:


living = df.CountryLive.value_counts(ascending=True)[-30:]

ax = living.plot(kind='barh', figsize=(7,12), logx=True, width=0.7)
_ = (ax.set_title('Top 30 Countries by Place of Living'), 
     ax.set_xlabel('Number of coders (log)'))


# ## Language

# In[ ]:


language = df.LanguageAtHome.value_counts(ascending=True)[-30:]
ax = language.plot(kind='barh', logx=True, width=0.7, figsize=(8,12))
_ = (ax.set_title('Top 30 Languages'), 
     ax.set_xlabel('Number of coders (log)'))


# ## Ethnic Minority

# In[ ]:


ax = df.IsEthnicMinority.value_counts(sort=False).plot(kind='barh')

_ = (ax.set_title('Are Coders an Ethnic Minority'),
     ax.set_xlabel('Number of coders'),
     ax.set_yticklabels(["not a minority", 'minority'], rotation=90)
    )


# # Education

# ## School Degree

# In[ ]:


ax = df.SchoolDegree.value_counts(ascending=True).plot(kind='barh', figsize=(7,8), width=0.6)

_ = (ax.set_title('Highest School Degree'), 
     ax.set_xlabel('Number of coders'),    
    )


# ## School Major

# In[ ]:


major = df.SchoolMajor.value_counts(ascending=True)[-30:]

ax = major.plot(kind='barh', figsize=(7,12), width=0.7)
_ = (ax.set_title('Top 30 University Majors'), 
     ax.set_xlabel('Number of coders'))


# ## Hours Learning

# In[ ]:


ax = df.HoursLearning.hist(bins=25)

_ = (ax.set_title('Hours Spent Learning'),
     ax.set_xlabel('Hours per week'),
     ax.set_ylabel('Number of coders'),
     ax.set_xticks(np.linspace(0, 100, 11))
    )

hours_median = df.HoursLearning.median()

_ = (ax.axvline(hours_median, color='black', linewidth=2), 
     ax.text(hours_median, 60, 
             'median = {:.0f} hours'.format(hours_median), 
             rotation=90, fontsize=13, fontweight='bold', 
             horizontalalignment='right', verticalalignment='bottom')
    )


# ## Money For Learning

# In[ ]:


ax = df.MoneyForLearning.hist(bins=30, log=True)
_ = (ax.set_title('Money Spent on Learning'),
     ax.set_xlabel('Money in US$'),
     ax.set_ylabel('Number of coders (log)'),
    )


# A large majority (the above histogram has a logarithmic y-axis) of coders spent low amount of money on learning. Let's explore the group with $1000 or less:

# In[ ]:


low_money = df.MoneyForLearning[df.MoneyForLearning <= 1000]

ax = low_money.hist(bins=20)
_ = (ax.set_title('Money Spent on Learning\n'
                  '(Coders With $1000 or Less)'),
     ax.set_xlabel('Money in US$'),
     ax.set_ylabel('Number of coders'),
     ax.set_xticks(np.linspace(0, 1000, 11))
    )


# About half of all coders have little or no money for learning.

# ## Months Programming

# In[ ]:


ax = df.MonthsProgramming.hist(bins=20, log=True)
_ = (ax.set_title('Months of Programming Experience'),
     ax.set_xlabel('Months of experience'),
     ax.set_ylabel('Number of coders (log)'))

months_median = df.MonthsProgramming.median()

_ = (ax.axvline(months_median, color='black', linewidth=2), 
     ax.text(months_median+6, 2, 
             'median = {:.0f} months'.format(months_median), 
             rotation=90, fontsize=13, fontweight='bold', 
             horizontalalignment='left', verticalalignment='bottom')
    )


# Very skewed distribution (the above histogram has a logarithmic y-axis), so we'll divide coders in two groups: one with 1 year of the experience or less, and other more experienced (we'll limit the max experience to 30 years, so we don't show outliers).

# In[ ]:


newbies = df.MonthsProgramming[df.MonthsProgramming <= 12]
oldies = df.MonthsProgramming[(df.MonthsProgramming > 12) & (df.MonthsProgramming <= 360)]


# In[ ]:


ax = newbies.hist(bins=12)
_ = (ax.set_title('Months of programming experience\n'
                  '(coders with 1 year of experience or less)'),
     ax.set_xlabel('Months of experience'),
     ax.set_ylabel('Number of coders'),
     ax.set_xticks(np.linspace(0, 12, 13)),
    )


# In[ ]:


ax = oldies.hist(bins=15)
_ = (ax.set_title('Months of programming experience\n'
                  '(coders with 1 year of experience or more)'),
     ax.set_xlabel('Months of experience'),
     ax.set_ylabel('Number of coders'),
     ax.set_xticks(np.linspace(0, 360, 16)),
     ax.set_xlim((13, 360)),
    )


# # Jobs and Employment

# ## Employment Status

# In[ ]:


employment = df.EmploymentStatus.value_counts(ascending=True)

ax = employment.plot(kind='barh', figsize=(7,6), width=0.7)
_ = (ax.set_title('Employment Status'),
     ax.set_xlabel('Number of coders'))


# ## Software Developers

# In[ ]:


devs = df.IsSoftwareDev.value_counts(sort=False)

ax = devs.plot(kind='barh')
_ = (ax.set_title('Are Coders Already Software Developers?'),
     ax.set_xlabel('Number of coders'),
     ax.set_yticklabels(["not a developer", 'developer'], rotation=90)
    )


# ## Employment Field

# In[ ]:


field = df.EmploymentField.value_counts(ascending=True)

ax = field.plot(kind='barh', figsize=(7,10), width=0.7)
_ = (ax.set_title('Employment Field'),
     ax.set_xlabel('Number of coders'),
    )


# ## Under Employment

# In[ ]:


under = df.IsUnderEmployed.value_counts(sort=False)

ax = under.plot(kind='barh')
_ = (ax.set_title('Are Coders Under-Employed?'),
     ax.set_xlabel('Number of coders'),
     ax.set_yticklabels(["not under-employed", 'under-employed'], rotation=90)
    )


# ## Debt

# In[ ]:


ax = df.HasDebt.value_counts(sort=False).plot(kind='barh')
_ = (ax.set_title('Do Coders Have a Debt?'),
     ax.set_xlabel('Number of coders'),
     ax.set_yticklabels(["don't have a debt", 'have a debt'], rotation=90)
    )


# ## Income

# In[ ]:


ax = df.Income.hist(bins=25)
_ = (ax.set_title('Income Last Year'),
     ax.set_xlabel('Income in US$'),
     ax.set_ylabel('Number of coders'),
     ax.set_xticks(np.linspace(0, 200000, 9))
    )

income_median = df.Income.median()

_ = (ax.axvline(income_median, color='black', linewidth=2), 
     ax.text(income_median-1000, 40, 
             'median = ${:.0f}'.format(income_median), 
             rotation=90, fontsize=13, fontweight='bold', 
             horizontalalignment='right', verticalalignment='bottom')
    )


# ## Expected Earning

# In[ ]:


ax = df.ExpectedEarning.hist(bins=25)
_ = (ax.set_title('Expected Earning'),
     ax.set_xlabel('Salary in US$'),
     ax.set_ylabel('Number of coders'),
     ax.set_xticks(np.linspace(0, 200000, 9)))

expected_median = df.ExpectedEarning.median()

_ = (ax.axvline(expected_median, color='black', linewidth=2), 
     ax.text(expected_median-1000, 40, 
             'median = ${:.0f}'.format(expected_median), 
             rotation=90, fontsize=13, fontweight='bold', 
             horizontalalignment='right', verticalalignment='bottom'))


# ## Job Applying Time

# In[ ]:


ax = df.JobApplyWhen.value_counts(ascending=True).plot(kind='barh', figsize=(8,5), width=0.6)
_ = (ax.set_title('When Will They Apply For a Job?'),
     ax.set_xlabel('Number of coders'),
    )


# ## Job Preference

# In[ ]:


ax = df.JobPref.value_counts(ascending=True).plot(kind='barh', figsize=(8,5), width=0.6)
_ = (ax.set_title('Job Preference'),
     ax.set_xlabel('Number of coders'),
    )


# ## Job Role Interest

# In[ ]:


ax = df.JobRoleInterest.value_counts(ascending=True).plot(kind='barh', figsize=(8,6), width=0.7)
_ = (ax.set_title('Job Role Interest'),
     ax.set_xlabel('Number of coders'),
    )


# ## Job Location

# In[ ]:


ax = df.JobWherePref.value_counts(ascending=True).plot(kind='barh', figsize=(8,4))
_ = (ax.set_title('Where Would They Like To Work?'),
     ax.set_xlabel('Number of coders'),
    )


# ## Job Relocation

# In[ ]:


ax = df.JobRelocateYesNo.value_counts(sort=False).plot(kind='barh')

_ = (ax.set_title('Would They Relocate For a Job?'),
     ax.set_xlabel('Number of coders'),
     ax.set_yticklabels(["would not relocate", 'would relocate'], rotation=90)
    )


# It looks like majority would be willing to relocate, but only 1/3 of the coders answered this question.
