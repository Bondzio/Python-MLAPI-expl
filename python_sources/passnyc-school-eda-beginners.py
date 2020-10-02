#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#invite people for the Kaggle party
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')

# Put this when it's called
from sklearn.model_selection import train_test_split
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression

import os
print(os.listdir("../input"))


# In[ ]:


school = pd.read_csv('../input/2016 School Explorer.csv')


# In[ ]:


school.head()


# In[ ]:


school.shape


# In[ ]:


pd.Series(school.columns)


# ## Correlation Matrix (heatmap style)

# In[ ]:


#correlation matrix
corrmat = school.corr()
f, ax = plt.subplots(figsize=(24, 18))
sns.heatmap(corrmat, vmax=.8, square=True);


# That's really a 'hot'map, divided into 2 bright sections.
# Section 1 has Grade 3 to Grade 5 variables whereas Section 2 has Grade 6 to Grade 8 variables.
# 
# But why?
# Hypothesis: There are 2 school categories, one having Grade 3 to Grade 5 facilities, other having Grade 6 to Grade 8 facilities.

# In[ ]:


school[['Grades','SED Code']].groupby(by='Grades').count().sort_values(by='SED Code',ascending=False)


# # Missing Data

# In[ ]:


total = school.isnull().sum().sort_values(ascending=False)
percent = (school.isnull().sum()/school.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(25)


# In[ ]:


#Analysing Top 3 columns with most missing values
missing_col = ['Other Location Code in LCGMS', 'Adjusted Grade', 'New?']
t1 = school[[missing_col[0],'SED Code']].groupby(by=missing_col[0]).count()
t2 = school[[missing_col[1],'SED Code']].groupby(by=missing_col[1]).count()
t3 = school[[missing_col[2],'SED Code']].groupby(by=missing_col[2]).count()
pd.concat([t1,t2,t3])


# In[ ]:


#Since the values (other than Null) are not useful, it is better to drop these 3 columns
school = school.drop(missing_col, axis=1)


# In[ ]:


#Let's find and drop some more columns which are not useful (at least for now)
school.head(2)
drop_list = ['School Name', 'Address (Full)', 'Grades'] #dropping Grades becasue 'Grades Low' and 'Grades High' columns provide sufficient information
school = school.drop(drop_list, axis=1)


# In[ ]:


#Now we should do some basic categorical univariate exploration
countplot_list = ['District', 'City', 'Zip', 'Community School?']
school[['District', 'City', 'Zip']].groupby(by=['District','City']).count()


# In[ ]:


sns.countplot(school['Community School?'])


# In[ ]:


#simplifying further by dropping these analyzed features, at least for now
school = school.drop(['District', 'City', 'Zip', 'Location Code'], axis=1) #Not dropping 'Community School?' and dropping one other 'Location Code' feature


# In[ ]:


# missing value treatment
total = school.isnull().sum().sort_values(ascending=False)
percent = (school.isnull().sum()/school.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(20)


# In[ ]:


school.describe()


# ## Lattitude Longitude Analysis

# In[ ]:


# sns.lmplot( x="Latitude", y="Longitude", data=school, fit_reg=False, hue='City', legend=True, size=10)


# ### Children Races Analysis - Univariate Distribution

# In[ ]:


# Pre-process : Remove % sign and convert object-type into float-type
race_cols = ['Percent Asian','Percent Black','Percent Hispanic','Percent White']
school[race_cols] = school[race_cols].replace({'\%': ''}, regex=True)


# #### Total % should be 100 in ideal case, let's see the distribution of 'Sum% of all races for each school'

# In[ ]:


school[race_cols].sum(axis=1).sort_values(ascending=False).plot(kind='hist')


# In[ ]:


for col in race_cols:
    school[col] = school[col].astype('float64')


# In[ ]:


plt.figure(figsize=(20,5))
sns.distplot(school[race_cols[0]] , color="red", label="Asian", hist=False)
sns.distplot(school[race_cols[1]] , color="green", label="Black", hist=False)
sns.distplot(school[race_cols[2]] , color="yellow", label="Hispanic", hist=False)
sns.distplot(school[race_cols[3]] , color="magenta", label="White", hist=False)


# In[ ]:


# Skewness
skew_values = stats.skew(school[race_cols], nan_policy = 'omit')
pd.concat([pd.DataFrame(list(race_cols), columns=['Features']), 
           pd.DataFrame(list(skew_values), columns=['Skewness degree'])], axis = 1)


# ### There is more weight on the right tail in case of 'Asian', 'ELL' and White. 
# Hypothesis: There is a racial discrimination against Black and Hispanic race children

# In[ ]:


### Schools Rating Analysis - Univariate Categorical
rating_cols = ['Rigorous Instruction Rating', 'Collaborative Teachers Rating', 'Supportive Environment Rating', 'Effective School Leadership Rating',
               'Strong Family-Community Ties Rating', 'Trust Rating', 'Student Achievement Rating']
rating_df = school[rating_cols]
rating_group = pd.Series()
for i in rating_cols:
    rating_group = pd.concat([rating_group, rating_df[i].value_counts(dropna = False)], axis=1, join='outer')
rating_group = rating_group.drop(0, axis=1)
rating_tags = ['Exceeding Target', 'Meeting Target', 'Approaching Target', 'Not Meeting Target']
rating_group = rating_group.reindex(rating_tags)


# In[ ]:


rating_grp = rating_group.reset_index()
ax = rating_grp.plot(x='index', kind='bar')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


# It would be interesting to compare the individual as well as total rating points against 'races'
# 
# For that, first compare 'Target Achievement Effectiveness' vs. Race

# In[ ]:


col_list = rating_cols + race_cols
df = school[col_list]
df.head(2)


# In[ ]:


# We have to normalize the percent aggregates for each race. E.g.::
df.iloc[:,[0,7,8,9,10]].groupby(by='Rigorous Instruction Rating', axis=0).sum().apply(lambda x:100*x / float(x.sum())).reset_index()


# In[ ]:


def barplot_race(i, title):
    df.iloc[:,[i,7,8,9,10]].groupby(by=title, axis=0).sum().apply(lambda x:100*x / float(x.sum())).reset_index().plot(x=title, kind='bar')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xticks(rotation=20)
    plt.show()
for i,col in enumerate(rating_cols):
    barplot_race(i,col)


# In[ ]:




