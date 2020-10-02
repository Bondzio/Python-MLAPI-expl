#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Load in libraries

import warnings
warnings.filterwarnings('ignore')
import os

#libraries for handling data
import pandas as pd
import numpy as np
import math
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
from sklearn.preprocessing import MinMaxScaler
mmscaler = MinMaxScaler()
from sklearn.preprocessing import RobustScaler
rscaler = RobustScaler()
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error
import datetime
from datetime import datetime, time

#libraries for data visualization
import matplotlib as mpl
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pylab as pylab
import seaborn as sns

#libaries for modelling
# Regression Modelling Algorithms
import statsmodels.api as sm
#from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor , GradientBoostingRegressor


# In[ ]:


groups = pd.read_csv('../input/groups.csv')
group_memberships = pd.read_csv('../input/group_memberships.csv')
school_memberships = pd.read_csv('../input/school_memberships.csv')
tags = pd.read_csv('../input/tags.csv')
answers = pd.read_csv('../input/answers.csv')
emails = pd.read_csv('../input/emails.csv')
comments = pd.read_csv('../input/comments.csv')
questions = pd.read_csv('../input/questions.csv')
matches = pd.read_csv('../input/matches.csv')
professionals = pd.read_csv('../input/professionals.csv')
students = pd.read_csv('../input/students.csv')
tag_questions = pd.read_csv('../input/tag_questions.csv')
tag_users =pd.read_csv('../input/tag_users.csv')


# In[ ]:


def get_meta_info_about_columns_and_tables(df_arr, df_name_arr):
    tables = []
    columns = []
    for df, name in zip(df_arr, df_name_arr):
        columns.extend(df.columns.values)
        tables.extend([name] * len(df.columns))
    return pd.DataFrame({'table': tables, 'column': columns})


# In[ ]:


tables_columns_info = get_meta_info_about_columns_and_tables(
    [
        professionals,
        tag_users,
        students,
        tag_questions,
        groups,
        emails,
        group_memberships,
        answers,
        comments,
        matches,
        tags,
        questions,
        school_memberships
    ],
    [
        'professionals',
        'tag_users',
        'students',
        'tag_questions',
        'groups',
        'emails',
        'group_memberships',
        'answers',
        'comments',
        'matches',
        'tags',
        'questions',
        'school_memberships'
    ]
)


# In[ ]:


tables_columns_info.head(10)


# In[ ]:


tables_columns_info[tables_columns_info.column.str.contains('group')]


# In[ ]:


professionals['professionals_date_joined'] = pd.to_datetime(professionals['professionals_date_joined'], errors='coerce')
students['students_date_joined'] = pd.to_datetime(students['students_date_joined'], errors='coerce')
emails.emails_date_sent = pd.to_datetime(emails.emails_date_sent, errors='coerce')
answers.answers_date_added = pd.to_datetime(answers.answers_date_added , errors='coerce')
comments.comments_date_added = pd.to_datetime(comments.comments_date_added, errors='coerce')
questions.questions_date_added = pd.to_datetime(questions.questions_date_added, errors = 'coerce')


# In[ ]:





# In[ ]:


groups.head(3)


# In[ ]:


groups.info()


# In[ ]:


groups.isnull().sum()


# In[ ]:


answers.head()


# Students

# In[ ]:


students.head(3)


# In[ ]:


students.info()


# In[ ]:


students.isnull().sum()


# Top 10 student locations

# In[ ]:


students.students_location.nunique()


# In[ ]:


students_locations_top = students.students_location.value_counts().sort_values(ascending = False).head(10)


# In[ ]:


students_locations_top


# In[ ]:


students_locations_top.plot.bar()


# groups

# In[ ]:


groups.columns


# In[ ]:


groups.groups_group_type.unique()


# In[ ]:


groups.groups_group_type.nunique()


# In[ ]:


groups.groups_group_type.value_counts()


# In[ ]:


#groups.groups_group_type.value_counts().sort_values(ascending=True).plot.pie(title='Group Types')
groups.groups_group_type.value_counts().sort_values(ascending=True).plot(kind='pie',autopct='%1.1f%%', title='Group Types')
plt.xlabel('')
plt.ylabel('')


# In[ ]:


#groups.groups_group_type.value_counts().sort_values(ascending=True).plot.barh(title='Group Types')
groups.groups_group_type.value_counts().sort_values(ascending=True).plot(kind='barh', title='horizoneal bar graph')
plt.xlabel('counts')
plt.ylabel('group types')


# In[ ]:


#groups.groups_group_type.value_counts().plot.bar()
#groups.groups_group_type.value_counts().sort_values(ascending=True).plot.bar(title='group types')
groups.groups_group_type.value_counts().sort_values(ascending=True).plot(kind='bar', title='group types', figsize=(5, 5))


# In[ ]:


temp = groups.groups_group_type.value_counts()
temp = temp.reset_index()


# In[ ]:


temp.head()


# In[ ]:


sns.barplot(x="groups_group_type", y='index', data=temp, color="cyan")


# In[ ]:


emails.head()


# In[ ]:


emails.columns


# In[ ]:


emails.emails_frequency_level.unique()


# In[ ]:


professionals.head()


# In[ ]:


professionals.professionals_location.nunique()


# In[ ]:


professionals_location_top = professionals.professionals_location.value_counts().sort_values(ascending=True).head(10)
professionals_location_top


# In[ ]:


professionals_location_topChart = professionals_location_top.plot.pie(autopct='%1.0f%%')
plt.xlabel('')
plt.ylabel('')


# In[ ]:


students.head()


# In[ ]:


students.students_id.count()


# In[ ]:


students.students_date_joined.isnull().sum()


# In[ ]:


students['students_date_joined_year'] = students['students_date_joined'].dt.year
students['students_date_joined_month'] = students.students_date_joined.dt.month
students['students_date_joined_day'] = students.students_date_joined.dt.day


# In[ ]:


students_count =students['students_id'].groupby(students['students_date_joined_year']).count()
students_count


# In[ ]:


students_count.plot.line()


# In[ ]:


school_memberships.head()


# In[ ]:


school_memberships.school_memberships_school_id.nunique()


# In[ ]:


questions.head()


# In[ ]:


questions.quest_added_year = questions.questions_date_added.dt.year


# In[ ]:


questions.questions_id.groupby(questions.quest_added_year).count().plot(kind='bar')


# cumulated number of questions per year

# In[ ]:


np.cumsum(questions.questions_id.groupby(questions.quest_added_year).count()).plot(kind='bar')


# # Merging data sets

# In[ ]:


df = pd.merge(questions, answers, how='left', left_on='questions_id', right_on='answers_question_id')
df = pd.merge(df, tag_questions, how ='left', left_on='questions_id', right_on='tag_questions_question_id')
df = pd.merge(df, tags, how='left', left_on='tag_questions_tag_id', right_on='tags_tag_id')
df = pd.merge(df, group_memberships, how='left', left_on='answers_author_id', right_on='group_memberships_user_id')
df = pd.merge(df, groups,how='left', left_on='group_memberships_group_id', right_on='groups_id')


# In[ ]:


df.head().transpose()


# In[ ]:


df.questions_date_added = pd.to_datetime(df.questions_date_added, errors='coerce')
df.quest_added_date = df.questions_date_added.dt.date


# In[ ]:


g1 =df.questions_id.groupby(df.quest_added_date).count()
g1.plot()


# In[ ]:


df.tags_tag_name.nunique()


# In[ ]:


top_tags = df.questions_id.groupby(df.tags_tag_name).count().sort_values(ascending=False).head(10)


# In[ ]:


top_tags.plot.bar()


# See how long it takes the questions to be answered

# In[ ]:


df['duration_answers'] = (pd.to_datetime(df.answers_date_added) - pd.to_datetime(df.questions_date_added) ).dt.days


# In[ ]:


df.duration_answers.describe()


# In[ ]:


df.duration_answers.groupby(df.groups_group_type).describe()


# In[ ]:


sns.distplot(df.duration_answers.dropna())


# In[ ]:


sns.kdeplot(df.duration_answers.dropna(), shade=True, color='r')


# In[ ]:


sns.kdeplot(df.duration_answers.dropna()[df.tags_tag_name=='college'], label='college', shade=False)
sns.kdeplot(df.duration_answers.dropna()[df.tags_tag_name=='career'], label='career', shade=False)
sns.kdeplot(df.duration_answers.dropna()[df.tags_tag_name=='engineering'], label='engineering', shade=False)


# In[ ]:


sns.kdeplot(df.duration_answers.dropna()[df.groups_group_type=='competition'], label='competition')
#sns.kdeplot(df.duration_answers.dropna()[df.groups_group_type=='youth program'], label='youth program')
sns.kdeplot(df.duration_answers.dropna()[df.groups_group_type=='mentorship program'], label='mentorship program')


# In[ ]:


df.duration_answers.groupby(df.groups_group_type).mean()


# In[ ]:




