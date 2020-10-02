#!/usr/bin/env python
# coding: utf-8

# **Plotting pivot tables and exploring data**
# --------------------------------------------

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
from matplotlib import style
import seaborn as sns
sns.set(style='ticks', palette='RdBu')
#sns.set(style='ticks', palette='Set2')
import pandas as pd
import numpy as np
import time
import datetime 
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
pd.options.display.max_colwidth = 1000
from time import gmtime, strftime
Time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
import timeit
start = timeit.default_timer()
pd.options.display.max_rows = 100

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))
df=pd.read_csv("../input/HR_comma_sep.csv")

# Any results you write to the current directory are saved as output.


# First we can simply describe the variables, and look at their means/standard deviations, and normal quintiles. 

# In[ ]:


df.columns = ['satisfaction_level', 
                  'last_evaluation', 
                  'number_project',
                  'average_montly_hours', 
                  'time_spend_company', 
                  'Work_accident', 
                  'left',
                  'promotion_last_5years', 
                  'department', 
                  'salary']
df.describe().T


# In[ ]:


df['dept_index'] = df['department']

department_groups = {'sales': 1, 
                     'marketing': 2, 
                     'product_mng': 3, 
                     'technical': 4, 
                     'IT': 5, 
                     'RandD': 6, 
                     'accounting': 7, 
                     'hr': 8, 
                     'support': 8, 
                     'management': 9 
                    }
df['dept_index'] = df.department.map(department_groups)
salary_groups = {'low': 0, 'medium': 1, 'high': 2}
df['salary_index']=df['salary']
df.salary_index = df.salary.map(salary_groups)

#
df.columns


# Then we can plot a few pivot tables to look at the data and colormap them according to the values. 

# In[ ]:


df_jobtype = pd.pivot_table(df,
                        values = ['satisfaction_level', 'last_evaluation'],
                        index = ['department'],
                        columns = [],aggfunc=[np.mean], 
                        margins=True).fillna('')

cm = sns.light_palette("green", as_cmap=True)
df_jobtype.style.background_gradient(cmap=cm)


# In[ ]:


df_jobtype_salary = pd.pivot_table(df,
                        values = ['satisfaction_level', 'last_evaluation'],
                        index = ['department', 'salary'],
                        columns = [],aggfunc=[np.mean], 
                        margins=True).fillna('')
cm = sns.light_palette("green", as_cmap=True)
df_jobtype_salary.style.background_gradient(cmap=cm)


# In[ ]:


df_jobtype_salary_prom = pd.pivot_table(df,
                        values = ['satisfaction_level', 'last_evaluation'],
                        index = ['department','promotion_last_5years', 'salary'],
                        columns = [],aggfunc=[np.mean], 
                        margins=True).fillna('')

cm = sns.light_palette("green", as_cmap=True)
df_jobtype_salary_prom.style.background_gradient(cmap=cm)


# In[ ]:


df_jobtype_prom = pd.pivot_table(df,
                        values = ['satisfaction_level', 'last_evaluation'],
                        index = ['department','promotion_last_5years'],
                        columns = [],aggfunc=[np.mean], 
                        margins=True).fillna('')

cm = sns.light_palette("green", as_cmap=True)
df_jobtype_prom.style.background_gradient(cmap=cm)


# In[ ]:


df_jobtype_salary_time = pd.pivot_table(df,
                        values = ['satisfaction_level', 'last_evaluation'],
                        index = ['department','time_spend_company', 'salary'],
                        columns = [],aggfunc=[np.mean], 
                        margins=True).fillna('')
cm = sns.light_palette("green", as_cmap=True)
df_jobtype_salary_time.style.background_gradient(cmap=cm)


# We can now plot various plots and start seeing some trends in the data. 

# In[ ]:


for i in set(df['department']):
    aa= df[df['department'].isin([i])]
    g = sns.factorplot(x='time_spend_company', y="satisfaction_level",data=aa, 
                   saturation=1, kind="box", col = 'left', row = 'department',
                   ci=None, aspect=1, linewidth=1) 


# In[ ]:


for i in set(df['department']):
    aa= df[df['department'].isin([i])]
    g = sns.factorplot(x='time_spend_company', y="satisfaction_level",data=aa, 
                   saturation=1, kind="box", col = 'salary', row='department', 
                   ci=None, aspect=1, linewidth=1) 


# In[ ]:


for i in set(df['department']):
    aa= df[df['department'].isin([i])]
    g = sns.factorplot(x='left', y="satisfaction_level",data=aa, 
                   saturation=1, kind="box", col = 'salary',row='department', 
                   ci=None, aspect=1, linewidth=1) 


# We can now check how the various variables are correlated, and derive conclusions out of them. 

# In[ ]:


variable_correlations = df.corr()
variable_correlations


# In[ ]:


def heat_map(corrs_mat):
    sns.set(style="white")
    f, ax = plt.subplots(figsize=(11, 9))
    mask = np.zeros_like(corrs_mat, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True 
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corrs_mat, mask=mask, cmap=cmap, ax=ax)


# In[ ]:


heat_map(variable_correlations)


# This shows a very high correlation between number of projects and average monthly hours. Therefore we should plot projects done vs various departments and their salaries. 

# In[ ]:


df_left = df[df['left']==1]
reduced_variable_correlations = df_left.corr()
reduced_variable_correlations
heat_map(reduced_variable_correlations)


# This shows a very high correlation between number of projects and average monthly hours. Therefore we should plot projects done vs various departments and their salaries. 

# In[ ]:


for i in set(df['department']):
    aa= df[df['department'].isin([i])]
    g = sns.factorplot(x='number_project', y="satisfaction_level",data=aa, 
                   saturation=1, kind="box", col = 'salary', row='department', 
                   ci=None, aspect=1, linewidth=1) 


# It is now somewhat apparent that the sweet spot for number of projects done should be between 3 and 5. If employees don't get to work on any projects, they are not satisfied, and if they have to work on too many projects, they are again not satisfied. In fact, overworking them reduces the satisfaction very significantly. 

# In[ ]:


for i in set(df['department']):
    aa= df[df['department'].isin([i])]
    g = sns.factorplot(x='number_project', y="average_montly_hours",data=aa, 
                   saturation=1, kind="box", col = 'left', row='department', 
                   ci=None, aspect=1, linewidth=1) 


# It seems that average monthly hours is a significant factor. The employees that left, were working a significantly more number of hours on an average compared to those who stayed. 

# In[ ]:


for i in set(df['department']):
    aa= df[df['department'].isin([i])]
    g = sns.factorplot(x='number_project', y="average_montly_hours",data=aa, 
                   saturation=1, kind="box", col = 'promotion_last_5years', row='department', 
                   ci=None, aspect=1, linewidth=1) 


# In[ ]:


df_small = df[['satisfaction_level', 
                   'last_evaluation', 
                   'number_project',
                   'average_montly_hours', 
                   'time_spend_company']]
sns.pairplot(df_small, hue="number_project")


# We can derive the same conclusions out of the pair plot as well. Wherever clusters exist, those clusters indicate a high correlation.  For example ~ those employees with very low satisfaction levels have very high number of hours, more than 5 projects, and because of this they have to spend a lot more hours than the normal. Although their last evaluations are high, the employees are not satisfied. 

# In[ ]:


#g = sns.PairGrid(df_small, diag_sharey=False)
#g.map_lower(sns.kdeplot, cmap="Blues_d")
#g.map_upper(plt.scatter)
#g.map_diag(sns.kdeplot, lw=3)


# In[ ]:


df=pd.read_csv("../input/HR_comma_sep.csv")
df.columns = ['satisfaction_level', 
                  'last_evaluation', 
                  'number_project',
                  'average_montly_hours', 
                  'time_spend_company', 
                  'Work_accident', 
                  'left',
                  'promotion_last_5years', 
                  'department', 
                  'salary']
mod_df = df 


# In[ ]:


df.columns


# In[ ]:


from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import RFECV, SelectKBest

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier

classifiers = [('RandomForestClassifierG', RandomForestClassifier(n_jobs=-1, criterion='gini')),
               ('RandomForestClassifierE', RandomForestClassifier(n_jobs=-1, criterion='entropy')),
               ('AdaBoostClassifier', AdaBoostClassifier()),
               ('ExtraTreesClassifier', ExtraTreesClassifier(n_jobs=-1)),
               ('KNeighborsClassifier', KNeighborsClassifier(n_jobs=-1)),
               ('DecisionTreeClassifier', DecisionTreeClassifier()),
               ('ExtraTreeClassifier', ExtraTreeClassifier()),
               ('LogisticRegression', LogisticRegression()),
               ('GaussianNB', GaussianNB()),
               ('BernoulliNB', BernoulliNB())
              ]
allscores = []



salary_groups = {'low': 0, 'medium': 1, 'high': 2}

department_groups = {'sales': 1, 
                     'marketing': 2, 
                     'product_mng': 3, 
                     'technical': 4, 
                     'IT': 5, 
                     'RandD': 6, 
                     'accounting': 7, 
                     'hr': 8, 
                     'support': 9, 
                     'management': 10 
                    }
mod_df.salary = mod_df.salary.map(salary_groups)

mod_df['deptgrps'] = mod_df.department.map(department_groups)

for dept in mod_df.department.unique():
    mod_df['dept_'+dept] = (mod_df.department == dept).astype(int)
mod_df = mod_df.drop('department', axis=1)

x, Y = mod_df.drop('left', axis=1), mod_df['left']
for name, classifier in classifiers:
    scores = []
    for i in range(3): # three runs
        roc = cross_val_score(classifier, x, Y, scoring='roc_auc', cv=20)
        scores.extend(list(roc))
    scores = np.array(scores)
    print(name, scores.mean())
    new_data = [(name, score) for score in scores]
    allscores.extend(new_data)


# In[ ]:


temp = pd.DataFrame(allscores, columns=['classifier', 'score'])
sns.factorplot(x='classifier', 
               y="score",data=temp, 
               saturation=1, 
               kind="bar", 
               ci=None, 
               aspect=1, 
               linewidth=1) 
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)


# In[ ]:


temp = pd.DataFrame(allscores, columns=['classifier', 'score'])
#sns.violinplot('classifier', 'score', data=temp, inner=None, linewidth=0.3)
sns.factorplot(x='classifier', 
               y="score",
               data=temp, 
               saturation=1, 
               kind="box", 
               ci=None, 
               aspect=1, 
               linewidth=1)     
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)


# In[ ]:


df.columns


# In[ ]:


x, Y = mod_df.drop('left', axis=1), mod_df['left']

for name, classifier in classifiers:
    scores = []
    for i in range(3): # three runs
        roc = cross_val_score(classifier, x, Y, scoring='roc_auc', cv=20)
        scores.extend(list(roc))
    scores = np.array(scores)
    print(name, scores.mean())
    new_data = [(name, score) for score in scores]
    allscores.extend(new_data)


# In[ ]:


reduced_variable_correlations = mod_df.corr()
reduced_variable_correlations
heat_map(reduced_variable_correlations)


# In[ ]:


mod_df_left = mod_df[mod_df['left']==1]
reduced_variable_correlations = mod_df_left.corr()
reduced_variable_correlations
heat_map(reduced_variable_correlations)


# We can see now, that by splitting things into various departments, one can see that the things are not common at all places. Some departments need more work on one aspect over the other. 

# In[ ]:


x, Y = mod_df.drop('promotion_last_5years', axis=1), mod_df['promotion_last_5years']
for name, classifier in classifiers:
    scores = []
    for i in range(3): # three runs
        roc = cross_val_score(classifier, x, Y, scoring='roc_auc', cv=20)
        scores.extend(list(roc))
    scores = np.array(scores)
    print(name, scores.mean())
    new_data = [(name, score) for score in scores]
    allscores.extend(new_data)


# In[ ]:


temp = pd.DataFrame(allscores, columns=['classifier', 'score'])
#sns.violinplot('classifier', 'score', data=temp, inner=None, linewidth=0.3)
sns.factorplot(x='classifier', 
               y="score",
               data=temp, 
               saturation=1, 
               kind="box", 
               ci=None, 
               aspect=1, 
               linewidth=1)     
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)


# In[ ]:




