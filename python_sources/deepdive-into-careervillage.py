#!/usr/bin/env python
# coding: utf-8

# ![Career Village](https://www.careervillage.org/static/img/careervillage-logo.png)

# ### Data Science for good: CareerVillage.org
# 
# Careervillage.org is a nonprofit which crowdsources career advice for underserved youth. Their mission statement speaks for itself:
# > Our mission is to democratize access to the career advice and guidance underserved youth need to create professional goals and understand their personal paths to those goals. We exist first and foremost to level the playing field. <br/>
# 
# Their main goal is building a platform which crowd sources career advice from their over 15k professional members to give insights into different career options and also relevant career advice to youths who need it most, to inspire and motivate them. <br/>
# 
# 
# Check out their [blog](https://medium.com/@careervillage) for more details.
# 
# 

# <h2>Problem statement: </h2>
# 
# Develop a method to recommend relevant questions to the professionals who are most likely to answer them. With solutions being evaluated based on
# 
# **Performance**: How well does the solution match professionals to the questions they would be motivated to answer? 
# 
# **Easy to implement**: The CareerVillage.org team wants to put the winning submissions to work, quickly. 
# 
# **Extensibility:** In the future, CareerVillage.org aims to add more data features and to accommodate new objectives which should be possible with the suggested solutions. 

# <h2>About the dataset </h2>
# Along with google.org, CarrerVillage.org has released years worth of data from their website including emails sent out to professionals, the questions, answers and comments exchanged, the professions, locations and school details of the student and professional members. 
# 
# Data is for years 2012 though 2019 Feb. It has been provided in 13 csvs which are listed below with a short description of the csvs.

# In[ ]:


import os
from os.path import join
import warnings
import calendar

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

sns.set_style('whitegrid')
sns.set_context("paper", font_scale=1.5)
init_notebook_mode(connected=True)
plt.rcParams.update({'font.size': 12})

warnings.filterwarnings('ignore')


# In[ ]:


purple_colors = sns.color_palette("Purples")


# In[ ]:


input_path = '../input'


# In[ ]:


csv_names = sorted(os.listdir(input_path))
csv_descriptions = ['Answers text with question id', 'All comments with parent details (Q or A)', 
                'Emails sent to the subscribers with mail frequency and question details',
                'Which group does a member belong to', 'Mapping from group id to name',
                'Mapping from email to questions', 'Details of professionals who joined with location and date',
                'Questions with time it was asked and student ID',
               'Which school does a member belong to',
               'Details of students who joined with location and date',
               'Tag ID to question mapping', 'Tag ID to user mapping',
               'Tag ID to tag name mapping']

for i, (a,b) in enumerate(zip(csv_names, csv_descriptions)):
    print('{:>2}. {:>25}  :  {}'.format(i+1,a,b)) 


# Next, we'll start the analysis by loading the csvs, merging the csvs where applicable and looking into the relevant details in the respective csvs. We also try and find out which of the fields appear relevant to predicting a relevant recepient for a given question during the below analysis. 
# 
# We analyse the data in the following order:
# * [Questions](#1)
# * [Professionals](#2)
# * [Emails and matches](#3)
# * [ETA in answer](#4)
# * [Answers](#5)
# * [Comments](#6)
# * [Tags](#7)

# In[ ]:


# Loading the csvs

df_tags = pd.read_csv(join(input_path,'tags.csv'))
df_tag_users = pd.read_csv(join(input_path,'tag_users.csv'))
df_tag_questions = pd.read_csv(join(input_path,'tag_questions.csv'))

df_students = pd.read_csv(join(input_path,'students.csv'))
df_professionals = pd.read_csv(join(input_path,'professionals.csv'))

df_emails = pd.read_csv(join(input_path,'emails.csv'))
df_matches = pd.read_csv(join(input_path,'matches.csv'))

df_questions = pd.read_csv(join(input_path, 'questions.csv'))
df_answers = pd.read_csv(join(input_path, 'answers.csv'))

df_comments = pd.read_csv(join(input_path, 'comments.csv'))


# <h3><a id="1"> Questions dataset </a> </h3>
# ![Questions](https://knowyourteam.com/blog/wp-content/uploads/2018/12/bf28e-1y32gotcrvncb8ot3jctsea.png)
#  
# A total of 23931 questions have been asked over the years (Sep 2011 to Jan 2019). We look at the numbers year by year, month by month and also monthly average. 

# In[ ]:


num_of_questions = len(set(df_questions['questions_id']))
print('Total Number Of Questions : {}'.format(num_of_questions))


# ## Time Distribution Of Number Of Questions were asked

# In[ ]:


df_questions['questions_date_added'] = pd.to_datetime(df_questions['questions_date_added'])
df_questions_copy = df_questions.set_index(keys='questions_date_added')


# In[ ]:


df_questions_yearly_distibution = df_questions_copy['questions_id'].groupby([df_questions_copy.index.year]).count()
df_questions_month_distibution = df_questions_copy['questions_id'].groupby([df_questions_copy.index.month]).count()

df_questions_copy['month_year'] = df_questions_copy.index.to_period('M').astype('str')
df_questions_monthly_distibution = df_questions_copy[['month_year', 'questions_id']].groupby(by='month_year').count()


# In[ ]:


fig = plt.figure(figsize=(16, 12))
ax1 = plt.subplot2grid((2, 2), (0, 0))
ax2 = plt.subplot2grid((2, 2), (0, 1))
ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

ax1.set_xlabel('Years')
ax2.set_xlabel('Month Number')
ax3.set_xlabel('Month (MM-YYYY)')

ax1.set_ylabel('No. Of Questions Asked')
ax2.set_ylabel('Average No. Of Questions for each month')
ax3.set_ylabel('No. Of Questions Asked')

ax1.set_title('Questions asked per year')
ax2.set_title('Average questions asked per month')
ax3.set_title('Questions month over month')

ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)

x_ = df_questions_month_distibution.index.values 
sns.barplot(df_questions_yearly_distibution.index.values, 
            df_questions_yearly_distibution.values, 
            color=purple_colors[-2], 
            ax=ax1)
ax1.axhline(0, color="k", clip_on=False)
sns.barplot([calendar.month_name[m ] for m in x_], 
            df_questions_month_distibution.values, 
            color=purple_colors[-2], 
            ax=ax2)
ax2.axhline(0, color="k", clip_on=False)
sns.barplot(df_questions_monthly_distibution.index.values, 
            df_questions_monthly_distibution.values.ravel(), 
            color=purple_colors[-2], 
            ax=ax3)
ax3.axhline(0, color="k", clip_on=False)

fig.tight_layout()


# As can be seen from the above plot, questions peak around May of each year (which matches the college joining time) and also that they peaked in 2016 - showing growing popularity of the platform around 2016.

# <h3><a id="2"> Professionals </a> </h3>
# ![Professionals](http://m.professionalsinteract.com/images/Professionals2.jpg)
# 
# A total of 28k professionals are on the platform with their professions and areas of expertise as diverse as showcased in the image :)
# We look at the distributions of the industries these professionals belong to, locations and joining dates.

# In[ ]:


TOP_NUM = 30


# In[ ]:


num_of_professionals = len(set(df_professionals['professionals_id']))
print('Total Number Of Professionals : {}'.format(num_of_professionals))


# ## Distribution of professionals by industry and  location

# In[ ]:


df_professionals['professionals_industry'] = df_professionals[~pd.isnull(df_professionals['professionals_industry'])]['professionals_industry'].astype(str)
df_professionals_industry = df_professionals['professionals_industry'].value_counts().sort_values(ascending=False)

df_professionals['professionals_location'] = df_professionals[~pd.isnull(df_professionals['professionals_location'])]['professionals_location'].astype(str)
df_professionals_location = df_professionals['professionals_location'].value_counts().sort_values(ascending=False)


# In[ ]:


fig, ax = plt.subplots(1, 2, figsize=(25, 9))
sns.barplot(df_professionals_industry.index.values[:TOP_NUM], 
            df_professionals_industry.values[:TOP_NUM], 
            color=purple_colors[-2], 
            ax=ax[0])

sns.barplot(df_professionals_location.index.values[:TOP_NUM], 
            df_professionals_location.values[:TOP_NUM], 
            color=purple_colors[-2], 
            ax=ax[1])

ax[0].set_title('Professionals by industry')
ax[1].set_title('Professionals by location')

ax[0].set_ylabel('Count')
ax[1].set_ylabel('Count')

ax[0].set_xlabel('Industry')
ax[1].set_xlabel('Location')

ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=90, fontsize=15);
ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=90, fontsize=15);

ax[0].axhline(0, color="k", clip_on=False)
ax[1].axhline(0, color="k", clip_on=False)


# ## Time Distribution Of Number Of Professionals who joined

# In[ ]:


df_professionals['professionals_date_joined'] = pd.to_datetime(df_professionals['professionals_date_joined'])
df_professionals_copy = df_professionals.set_index(keys='professionals_date_joined')


# In[ ]:


df_professionals_yearly_distibution = df_professionals_copy['professionals_id'].groupby([df_professionals_copy.index.year]).count()
df_professionals_month_distibution = df_professionals_copy['professionals_id'].groupby([df_professionals_copy.index.month]).count()

df_professionals_copy['month_year'] = df_professionals_copy.index.to_period('M').astype('str')
df_professionals_monthly_distibution = df_professionals_copy[['month_year', 'professionals_id']].groupby(by='month_year').count()

x = df_professionals_month_distibution.index.values


# In[ ]:


fig = plt.figure(figsize=(16, 12))
ax1 = plt.subplot2grid((2, 2), (0, 0))
ax2 = plt.subplot2grid((2, 2), (0, 1))
ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

ax1.set_xlabel('Years')
ax2.set_xlabel('Month Number')
ax3.set_xlabel('Month (MM-YYYY)')

ax1.set_ylabel('No. Of Professionals Joined')
ax2.set_ylabel('No. Of Professionals Joined')
ax3.set_ylabel('No. Of Professionals Joined')

ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90)

sns.barplot(df_professionals_yearly_distibution.index.values, 
            df_professionals_yearly_distibution.values, 
            color=purple_colors[-2], 
            ax=ax1)
ax1.axhline(0, color="k", clip_on=False)
sns.barplot([calendar.month_name[m] for m in x], 
            df_professionals_month_distibution.values, 
            color=purple_colors[-2], 
            ax=ax2)
ax2.axhline(0, color="k", clip_on=False)
sns.barplot(df_professionals_monthly_distibution.index.values, 
            df_professionals_monthly_distibution.values.ravel(), 
            color=purple_colors[-2], 
            ax=ax3);
ax3.axhline(0, color="k", clip_on=False)

fig.suptitle('Distribution of professionals joining over time');

fig.tight_layout(pad=3.5)


# The growing popularity of the platform and the increasing number of professionals joining in are evident from the yearwise distribution of number of professionals joining in.

# <h3><a id="3"> E mails and matches </a> </h3>
# ![Emails](https://maxcdn.icons8.com/app/uploads/2016/10/mail.png)

# In[ ]:


df_email_matches = df_emails.merge(df_matches, left_on='emails_id', right_on='matches_email_id', how='outer')
df_email_matches = df_email_matches.drop('matches_email_id', axis=1)
df_email_matches = df_email_matches.rename({'emails_id' : 'email_id'}, axis=1)


# In[ ]:


fig, ax = plt.subplots(1, 1, figsize=(9, 9))

sns.countplot(x='emails_frequency_level', data=df_emails, ax=ax, color=purple_colors[-2]);
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
ax.set_xlabel('Email notification Frequency');
ax.set_title('Subscribers count by frequency')
ax.axhline(0, color="k", clip_on=False)


# ### Number of questions per email
# Below we show the number of questions per email sent to subscribers with different subscription frequencies. 
# 

# In[ ]:


df_question_count_in_email = df_email_matches.groupby(['email_id', 'emails_frequency_level']).count()['matches_question_id']
df_question_count_in_email = df_question_count_in_email.swaplevel(1, 0)


# In[ ]:


print('Immediate mailing subscription: \n')
print(df_question_count_in_email.xs('email_notification_immediate').value_counts()[:5])


# In[ ]:


print('Daily mailing subscription: \n')
print(df_question_count_in_email.xs('email_notification_daily').value_counts()[:5])


# In[ ]:


print('Weekly mailing subscription: \n')
print(df_question_count_in_email.xs('email_notification_weekly').value_counts()[:5])


# Observations:
# *     19 questions sent to weekly subscribers
# *     3 questions sent to daily subscribers
# *     1 question sent to immediate subscribers

# In[ ]:


fig, ax = plt.subplots(1, 1, figsize=(16, 9))
df_matches_count = df_email_matches.groupby('matches_question_id').count()['email_id']
sns.distplot(df_matches_count.values, kde=False, norm_hist=False, color=purple_colors[-2])
ax.set_title('Distribution of # recepients receiving a question')
ax.set_xlabel('# recepients')
ax.set_ylabel('# questions')


# <h3><a id="4"> ETA in answering </a> </h3>
# ![](https://images.freeimages.com/images/small-previews/38e/pocket-watch-3-1419880.jpg)

# In[ ]:


df_question_sent = df_matches.groupby('matches_question_id', as_index=False).count()
df_question_sent = df_question_sent.rename({'matches_email_id' : 'member_in_emails'}, axis=1)


# In[ ]:


df_questions['questions_title_length'] = df_questions['questions_title'].apply(len)
df_questions['questions_body_length'] = df_questions['questions_body'].apply(len)

df_questions = df_questions.merge(df_question_sent, left_on='questions_id', 
                                  right_on='matches_question_id', how='left')
df_questions = df_questions.drop(['matches_question_id'], axis=1)

df_questions['questions_date_added'] = pd.to_datetime(df_questions['questions_date_added'])
df_answers['answers_date_added'] = pd.to_datetime(df_answers['answers_date_added'])


# In[ ]:


df_questions_indexed = df_questions.set_index(keys='questions_date_added')
df_answers_indexed = df_answers.set_index(keys='answers_date_added')

df_answers_indexed = df_answers_indexed.drop_duplicates(subset='answers_question_id', keep='first')
df_questions_yearly_distibution = df_questions_indexed['questions_id'].groupby([df_questions_indexed.index.year]).count()
df_answers_yearly_distibution = df_answers_indexed['answers_question_id'].groupby([df_answers_indexed.index.year]).count()


# In[ ]:


plt.figure(figsize=[16,6])
plt.plot(df_questions_yearly_distibution.values, color='orange')
plt.plot(df_answers_yearly_distibution.values, color='blue')
plt.xticks(range(len(df_questions_yearly_distibution.index.values)), df_questions_yearly_distibution.index.values);
plt.title("Number of questions asked and questions answered over years");
plt.xlabel("Years");
plt.ylabel("Number of questions");
plt.legend(['Questions asked','Questions answered'], loc=0);


# In[ ]:


df_questions_answers = df_questions.merge(df_answers, left_on='questions_id', right_on='answers_question_id', how='inner')
df_questions_answers_copy = df_questions_answers[['questions_id', 'questions_date_added', 'answers_date_added', 
                                                  'questions_title_length', 'questions_body_length', 'member_in_emails']]

df_questions_answers_copy['time_to_answer'] = df_questions_answers_copy['answers_date_added'] - df_questions_answers_copy['questions_date_added']
df_questions_answers_copy['time_to_answer_in_days'] = df_questions_answers_copy['time_to_answer'].dt.days
plt.figure(figsize=[16,6])
plt.hist(df_questions_answers_copy['time_to_answer_in_days'].values, bins=100, color=purple_colors[-2]);
plt.xlabel('Days')
plt.title('Time to answer in days');


# In[ ]:


plt.figure(figsize=[12,8])
sns.distplot(df_questions_answers_copy['questions_title_length'], kde=False, norm_hist=False, color=purple_colors[-2])
plt.title('Distribution of title length for questions');


# In[ ]:


plt.figure(figsize=[12,8])
sns.distplot(df_questions_answers_copy[df_questions_answers_copy['questions_body_length']<1000]['questions_body_length'], kde=False, norm_hist=False, bins=50, color=purple_colors[-2])
plt.title('Distribution of body length for questions');


# In[ ]:


df_questions_answers_copy[['questions_title_length', 'questions_body_length', 'time_to_answer_in_days']].corr()


# In[ ]:


df_questions_answers_copy_1 = df_questions_answers_copy[df_questions_answers_copy['questions_body_length'] < 1000]

plt.figure(figsize=[6,6])
plt.scatter(df_questions_answers_copy_1['questions_body_length'], df_questions_answers_copy_1['time_to_answer_in_days'], alpha=0.5, color=purple_colors[-3])
plt.title('Scatter plot of question body length vs time to answer');
plt.xlabel('Questions body length');
plt.ylabel('Time to answer in days');


# As can be seen, there is very little correlation between the length of questions body and the time it takes to answer the question in days.

# In[ ]:


df_questions_answers_copy[['member_in_emails', 'time_to_answer_in_days']].corr()


# <h3><a id="5"> Answers </a> </h3>
# <img src="https://www.coronainsights.com/wp-content/uploads/2014/12/Question-Answer.jpg" alt="Drawing" style="width: 500px;"/>

# In[ ]:


num_of_answers = len(set(df_answers['answers_id']))
print('Total Number Of answers : {}'.format(num_of_answers))

num_of_questions = len(set(df_answers['answers_question_id']))
print('Total Number Of Questions answered : {}'.format(num_of_questions))


# In[ ]:


df_tag_question = df_tag_questions.merge(right=df_tags, how="left", left_on="tag_questions_tag_id", right_on="tags_tag_id")
mapping = dict(df_tag_question[['tag_questions_question_id', 'tags_tag_name']].values)
df_answer = df_answers.copy()
df_answer['tag_name'] = df_answers.answers_question_id.map(mapping)


# In[ ]:


df_answers_tags = df_answer.tag_name.value_counts().sort_values(ascending=True).tail(30).sort_values(ascending=False)
plt.figure(figsize=[20,8])
ax = sns.barplot(x = df_answers_tags.index.values, y= df_answers_tags.values, color=purple_colors[-2])
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
# df_answers_tags.plot.barh(figsize=(10, 8),  width=1)
plt.title("Top 50 Question tags for the answers", fontsize=15)
plt.ylabel('Number of Answers', fontsize=15)
plt.xlabel('Question tags', fontsize=15)
plt.show()


# Length of answer body

# In[ ]:



df_answer['answers_length'] = df_answer['answers_body'].apply(lambda x: len(str(x).split()))

plt.figure(figsize=[9,6])
sns.distplot(df_answer['answers_length'], kde=False, norm_hist=False, color=purple_colors[-2])
plt.title('Distribution of length for answer bodies');


# ## Number of Answers for Questions

# In[ ]:


number_answers_for_question = df_answers['answers_question_id'].value_counts(ascending=True).values

plt.figure(figsize=[12,8])
sns.distplot(number_answers_for_question, kde=False, norm_hist=False, color=purple_colors[-2])
plt.title('Distribution of number of answers for question');
plt.xlabel('# answers')


# <h3><a id="6"> Comments </a> </h3>
# <img src="http://thirdrock.com.au/wp-content/uploads/2018/04/comment1.jpg" alt="Drawing" style="width: 500px;"/>
# <!--![](http://thirdrock.com.au/wp-content/uploads/2018/04/comment1.jpg) .element height="10%" width="10%" -->

# In[ ]:


print('There are {} total comments'.format(df_comments.shape[0]))
print('Comments by {} unique authors'.format(np.unique(df_comments['comments_author_id']).shape[0]))


# In[ ]:


df_comments['is_author_prof'] = df_comments['comments_author_id'].isin(list(df_professionals['professionals_id']))
df_comments['is_author_student'] = df_comments['comments_author_id'].isin(list(df_students['students_id']))
df_comments['is_author_other_user'] = np.logical_not(np.logical_or(df_comments['is_author_prof'], df_comments['is_author_student']))

print('Number of comments by professionals: {}'.format(sum(df_comments['is_author_prof'])))
print('Number of comments by students: {}'.format(sum(df_comments['is_author_student'])))
print('Number of comments by other users: {}'.format(sum(df_comments['is_author_other_user'])))


# In[ ]:


df_comments['is_parent_question'] = df_comments['comments_parent_content_id'].isin(list(df_questions['questions_id']))
df_comments['is_parent_answer'] = df_comments['comments_parent_content_id'].isin(list(df_answers['answers_id']))

print('Number of comments on questions: {}'.format(sum(df_comments['is_parent_question'])))
print('Number of comments on answers: {}'.format(sum(df_comments['is_parent_answer'])))


# In[ ]:


comments_body = df_comments['comments_body']


# In[ ]:


def f(txt):
    return len(str(txt).split(" "))
    
df_comments['comments_body_len'] = df_comments['comments_body'].apply(f)

plt.figure(figsize=[12,8])
sns.distplot(df_comments['comments_body_len'], kde=False, norm_hist=False, color=purple_colors[-2])
plt.title('Distribution of length for comment bodies');


# In[ ]:


has_thank_index = ['thank' in str(a).lower() for a in comments_body]
print("Number of comments with string 'thank': "+str(sum(has_thank_index)))
has_thank_comments = df_comments[has_thank_index]
has_thank_comments['comments_body'].head()


# In[ ]:


has_html_index = ['<html>' in str(a).lower() for a in comments_body]
print("Number of comments with string '<html>': "+str(sum(has_html_index)))
has_html_comments = df_comments[has_html_index]
has_html_comments['comments_body'].head()


# In[ ]:


short_thank_you_comments_index = np.logical_and(df_comments['comments_body_len']<10, has_thank_index)
short_thank_you_comments = df_comments[short_thank_you_comments_index]
print("Number of short comments with string 'thank' in them: {}".format(short_thank_you_comments.shape[0]))
short_thank_you_comments['comments_body'].tail()


# In[ ]:


long_comments_index = np.logical_not(short_thank_you_comments_index)
long_comments = df_comments[long_comments_index]
print("Number of long comments to be analysed further: {}".format(long_comments.shape[0]))
long_comments['comments_body'].head()


# <h3><a id="7"> Tags </a> </h3>
# ![](https://cdn-images-1.medium.com/max/1600/1*xgoysqs1OfNCYXlLYZZtuw.jpeg)

# In[ ]:


num_unique_users = len(np.unique(df_tag_users[['tag_users_user_id']])) 
num_unique_tags = df_tags.shape[0]

print('There are {} unique tags'.format(num_unique_tags))
print('In all {} tags have been given to {} unique users'.format(df_tag_users.shape[0], num_unique_users))


# In[ ]:


df_count_tags_per_user = df_tag_users.groupby('tag_users_user_id').count()


# In[ ]:


data = [go.Histogram(x=df_count_tags_per_user.values[:,0], nbinsx=90, 
                     marker=dict(color='rgb({}, {}, {})'.format(*list(map(int, tuple([z * 255 for z in purple_colors[-2]]))))), 
                     opacity=0.75)]
layout = go.Layout(
    title='Distribution of tags per user',
    xaxis=dict(
        title='# tags'
    ),
    yaxis=dict(
        title='# Users'
    )
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# In[ ]:


df_count_tags_per_user.values.shape


#  Most common tags

# In[ ]:


df_count = df_tag_users.groupby('tag_users_tag_id').count()
df_count = df_count.sort_values(by='tag_users_user_id').reset_index()
df_count = df_count.rename({'tag_users_user_id':'count'}, axis=1)
df_tags_users_merged = df_count.merge(df_tags, right_on='tags_tag_id', left_on='tag_users_tag_id')
df_tags_users_merged = df_tags_users_merged.drop(['tags_tag_id', 'tag_users_tag_id'], axis=1)
df_tags_users_merged.sort_values(by='count', ascending=False).head(20)
df_tags_users_merged_sorted = df_tags_users_merged.sort_values(by='count', ascending=False)

data = [go.Bar(
            y=df_tags_users_merged_sorted['count'][:TOP_NUM],
            x=df_tags_users_merged_sorted['tags_tag_name'][:TOP_NUM], 
            marker=dict(color='rgb({}, {}, {})'.format(*list(map(int, tuple([z * 255 for z in purple_colors[-2]]))))),
            opacity=0.75
)]

layout = dict(
    width = 800,
    height = 550,
    title = '30 most common tags overall',
    xaxis = dict(
         tickangle=315,tickfont = dict(size=13,  color='grey'),
    ),
    yaxis = go.layout.YAxis(
        title = '# Users',
        automargin = True,
        titlefont = dict(size=17, color='grey')
    ),
    margin=dict(b=130)
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# In[ ]:


all_tagged_users = set(df_tag_users['tag_users_user_id'])
student_users = set(df_students['students_id']) 
professional_users = set(df_professionals['professionals_id'])

tagged_students = all_tagged_users.intersection(student_users)
tagged_professionals = all_tagged_users.intersection(professional_users)
print('Of the {} tagged users, {} are students and {} are professionals'.format(len(all_tagged_users),
                                                                               len(tagged_students),
                                                                               len(tagged_professionals)))


# In[ ]:


df_student_users = df_tag_users.merge(df_students, left_on='tag_users_user_id', right_on='students_id')
df_student_users = df_student_users.drop('tag_users_user_id', axis=1)
df_student_users.shape
df_professional_users = df_tag_users.merge(df_professionals, left_on='tag_users_user_id', right_on='professionals_id')
df_professional_users = df_professional_users.drop('tag_users_user_id', axis=1)
df_professional_users.shape
print('In all {} tags have been given to  {} to students and {} to professionals'.format(df_tag_users.shape[0], 
                                                                 df_student_users.shape[0], 
                                                                 df_professional_users.shape[0]))


# Top 20 student based tags

# In[ ]:


df_count = df_student_users[['students_id', 'tag_users_tag_id']].groupby('tag_users_tag_id').count()
df_count = df_count.sort_values(by='students_id').reset_index()
df_count = df_count.rename({'students_id':'count'}, axis=1)
df_tags_users_merged = df_count.merge(df_tags, right_on='tags_tag_id', left_on='tag_users_tag_id')
df_tags_users_merged = df_tags_users_merged.drop([ 'tags_tag_id', 'tag_users_tag_id'], axis=1)
df_tags_users_merged_sorted = df_tags_users_merged.sort_values(by='count', ascending=False)

data = [go.Bar(
            y=df_tags_users_merged_sorted['count'][:30],
            x=df_tags_users_merged_sorted['tags_tag_name'][:30],
            marker=dict(color='rgb({}, {}, {})'.format(*list(map(int, tuple([z * 255 for z in purple_colors[-2]]))))),
            opacity=0.75
            
)]

layout = dict(
    width = 800,
    height = 550,
    title = '30 most common tags for students',
    xaxis = dict(
         tickangle=315,tickfont = dict(size=13,  color='grey'),
    ),
    yaxis = go.layout.YAxis(
        title = '# Users',
        automargin = True,
        titlefont = dict(size=17, color='grey')
    ),
    margin=dict(b=100)
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# Top 20 professionals tags

# In[ ]:


df_count = df_professional_users[['professionals_id', 'tag_users_tag_id']].groupby('tag_users_tag_id').count()
df_count = df_count.sort_values(by='professionals_id').reset_index()
df_count = df_count.rename({'professionals_id':'count'}, axis=1)
df_tags_users_merged = df_count.merge(df_tags, right_on='tags_tag_id', left_on='tag_users_tag_id')
df_tags_users_merged = df_tags_users_merged.drop(['tags_tag_id', 'tag_users_tag_id'], axis=1)
df_tags_users_merged_sorted = df_tags_users_merged.sort_values(by='count', ascending=False)

data = [go.Bar(
            y=df_tags_users_merged_sorted['count'][:30],
            x=df_tags_users_merged_sorted['tags_tag_name'][:30],
            marker=dict(color='rgb({}, {}, {})'.format(*list(map(int, tuple([z * 255 for z in purple_colors[-2]]))))),
            opacity=0.75
            
)]

layout = dict(
    width = 800,
    height = 550,
    title = '30 most common tags for professionals',
    xaxis = dict(
         tickangle=315,tickfont = dict(size=13,  color='grey'),
    ),
    yaxis = go.layout.YAxis(
        title = '# Users',
        automargin = True,
        titlefont = dict(size=17, color='grey')
    ),
    margin=dict(b=130)
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# Top tags in questions

# In[ ]:


df_tag_questions.head()
df_tags_users_merged = df_tag_questions.merge(df_tags, left_on='tag_questions_tag_id', right_on='tags_tag_id')
df_tags_users_merged = df_tags_users_merged.drop(['tag_questions_tag_id'], axis=1)
df_tags_users_merged = df_tags_users_merged.groupby(['tags_tag_name']).count()
df_tags_users_merged = df_tags_users_merged.drop('tags_tag_id', axis=1).reset_index()
df_tags_users_merged_sorted = df_tags_users_merged.sort_values(by='tag_questions_question_id', ascending=False)
data = [go.Pie(
            values=df_tags_users_merged_sorted['tag_questions_question_id'][:30],
            labels=df_tags_users_merged_sorted['tags_tag_name'][:30],
            #marker=dict(color='rgb({}, {}, {})'.format(*list(map(int, tuple([z * 255 for z in purple_colors[-2]]))))),
            #opacity=0.75
)]

layout = dict(
    width = 1000,
    height = 800,
    title = 'Most common 30 tags',
    xaxis = dict(
        title = '# Users'
    ),
    yaxis = go.layout.YAxis(
        automargin = True,
        titlefont = dict(size=30),
        tickfont = dict(size=13),

    )
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# More exciting stuff coming soon. Stay tuned! :)

# <img src="https://4.bp.blogspot.com/-OIAJ2gnXHA8/Vyh32uGTMtI/AAAAAAAACEQ/8ihj8MTQ9BcjpJGCzgmQBFa4_bXJzBzEQCLcB/s1600/Comments.gif" alt="Drawing" style="width: 500px;"/>

# In[ ]:




