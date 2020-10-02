#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


# In[ ]:


import plotly.graph_objects as go


# In[ ]:


plt.style.use('fivethirtyeight')


# In[ ]:


df = pd.read_csv('../input/udemy-courses/udemy_courses.csv')


# In[ ]:


df.head(2)


# In[ ]:


df.is_paid = df.is_paid.astype(int)


# In[ ]:


df.info(memory_usage='deep')


# In[ ]:


# df[df['is_paid'] == 'https://www.udemy.com/learnguitartoworship/']


# In[ ]:


# df.set_index('course_id').reset_index()
# df.drop([2066],inplace=True)


# ## Course Type is Paid or Free 

# In[ ]:


labels = ['Paid', 'Free']
# df['is_paid'] = df['is_paid'].str.lower()
size = df['is_paid'].value_counts()
print(size)
explode = [0, 0.05]

plt.rcParams['figure.figsize'] = (6, 6)
plt.pie(size, explode = explode, labels = labels, shadow = False, autopct = '%.2f%%')
plt.title('Analysis of Course Type', fontsize = 16)
plt.axis('off')
plt.legend()
plt.show()


# ## Course Subject Type

# In[ ]:


labels = ['Web Development', 'Business Finance', 'Musical Instruments', 'Graphic Design']
size = df['subject'].value_counts()
print(size)
explode = [0.01, 0.02,0.03,0.04]

plt.rcParams['figure.figsize'] = (9, 9)
plt.pie(size, explode = explode, labels = labels, shadow = False, autopct = '%.2f%%')
plt.title('Analysis of Course Subjects', fontsize = 14)
# plt.axis('off')
plt.legend()
plt.show()


# ## Number of Lectures by Course Type (Free/Paid)

# In[ ]:


coures_free_lectures = df[df['is_paid'] == False]['num_lectures'].sum()
coures_paid_lectures = df[df['is_paid'] == True]['num_lectures'].sum()
plt.rcParams['figure.figsize'] = (10.0, 5.0)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=["Free", "Paid"],
    y=[coures_free_lectures, coures_paid_lectures],
    width=[0.3, 0.3]
))
# Change the bar mode
fig.update_layout(title="Number of Lectures by Course Type (Free/ Paid)")
fig.show()


# #### Number of Lectures in Paid Course are more than Free Courses.

# ## Course type by courses

# In[ ]:


plt.rcParams['figure.figsize'] = (10.0, 5.0)
ax = sns.countplot(x="subject", hue="is_paid", data=df)


# In[ ]:


max_subs = df[['course_title', 'num_subscribers', 'num_reviews', 'price', 'is_paid', 'subject', 'num_lectures']]


# In[ ]:


top_10 = max_subs.sort_values(by='num_subscribers', ascending=False).head(10)


# In[ ]:


fig = go.Figure(data=[
    go.Bar(name='Subscribers', x=top_10['course_title'], y=top_10['num_subscribers'],text=top_10['num_subscribers'],textposition='auto'),
    go.Bar(name='Reviews', x=top_10['course_title'], y=top_10['num_reviews'],text=top_10['num_reviews'],textposition='auto')
])

# Change the bar mode
fig.update_layout(barmode='group',xaxis_tickangle=-40,title="Top 10 courses subscribers and reviews")
fig.show()


# ## Top 10 courses

# In[ ]:


fig = go.Figure(data=[
    go.Bar(name='Subscribers', x=top_10['num_subscribers'], y=top_10['course_title'], orientation='h'),
])
fig.update_layout(title="Top 10 courses")
fig.show()


# In[ ]:


import plotly.express as px

fig = px.bar(max_subs.head(10), x='course_title', y='num_subscribers',
             hover_data=['num_subscribers'], color='num_subscribers',
             labels={'pop':'Top 10 courses'}, height=600)
fig.show()


# ## Top 10 Free Courses

# In[ ]:


top_10_free = max_subs[max_subs.is_paid == False]
top_10_free = top_10_free.sort_values(by='num_subscribers', ascending=False)
top_10_free


# In[ ]:


fig = px.bar(top_10_free.head(10), x='num_subscribers', y='course_title', width=890, height=400, orientation='h')
fig.update_layout(title="Top 10 Free courses", xaxis_title="Subscribers",yaxis_title="Course ")
fig.update_yaxes(automargin=True)

fig.show()


# In[ ]:


labels = ['Web Development', 'Business Finance', 'Musical Instruments', 'Graphic Design']
size = top_10_free['subject'].value_counts()
print(size)
explode = [0.01, 0.02,0.03,0.04]

plt.rcParams['figure.figsize'] = (9, 9)
plt.pie(size, explode = explode, labels = labels, shadow = False, autopct = '%.2f%%')
plt.title('Analysis of % Subjects in Free Course', fontsize = 14)
plt.legend()
plt.show()


# #### Web Development courses are most popular in free courses

# ## Top 10 Paid Course

# In[ ]:


top_10_paid = max_subs[max_subs.is_paid == True]
top_10_paid = top_10_paid.sort_values(by='num_subscribers', ascending=False)
top_10_paid


# In[ ]:


fig = px.bar(top_10_paid.head(10), x='num_subscribers', y='course_title', width=890, height=400, orientation='h')
fig.update_layout(title="Top 10 Paid courses", xaxis_title="Subscribers",yaxis_title="Course ")
fig.update_yaxes(automargin=True)
fig.show()


# In[ ]:


labels = ['Business Finance', 'Web Development', 'Musical Instruments', 'Graphic Design']
size = top_10_paid['subject'].value_counts()
print(size)
explode = [0.01, 0.02,0.03,0.04]

plt.rcParams['figure.figsize'] = (9, 9)
plt.pie(size, explode = explode, labels = labels, shadow = False, autopct = '%.2f%%')
plt.title('Analysis % Of Subjects in Paid Course', fontsize = 14)
plt.legend()
plt.show()


# #### Business Finance and Web Development courses are most popular in Paid courses.

# In[ ]:


import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (7, 5)

plt.subplot(1, 1, 1)
sns.set(style = 'whitegrid')
sns.distplot(df['num_subscribers'])
plt.title('Distribution of num_lectures', fontsize = 16)
plt.xlabel('Range of num of lectures')
plt.ylabel('Count')


# In[ ]:


plt.rcParams['figure.figsize'] = (7, 5)

plt.subplot(1, 1, 1)
sns.set(style = 'whitegrid')
sns.distplot(df['price'])
plt.title('Distribution of price', fontsize = 16)
plt.xlabel('Range of price')
plt.ylabel('Count')

