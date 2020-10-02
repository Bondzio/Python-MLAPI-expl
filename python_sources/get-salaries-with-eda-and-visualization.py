#!/usr/bin/env python
# coding: utf-8

# # Graduation according to region and university?
# 
# 

# ***Suad Emre UMAR - 27.09.2018***

# ## Table of Contents
# ***
# * [1. Introduction](#c) <br>
# * [2. Importing dataset and data preprocessing](#importing_dataset_and_data_preprocessing) <br>
#    * [2.1. Importing essential libraries](#importing_essential_libraries) <br>
#    * [2.2. Importing datasets](#importing_datasets) <br>
#    * [2.3. Summarize the datasets](#Summarize_the_dataset) <br>
#    * [2.4. Data preprocessing](#data_preprocessing) <br>
#        * [2.4.1. Change of Data's columns](change_data's_columns)<br>
#        * [2.4.2. Change of Data columns types](change_data_types)<br>
# * [3. Data Visualization](#data_visualization) <br>
#    * [3.1. Salary According to Undergraduate Major](#major) <br>
#    * [3.2. Salary According to School Type](#school_type) <br>
#    * [3.3. Salary According to Region](#region) <br>  
# ***

# ## 1. Introduction
# <a id="c"></a>
# 
# The <a href="https://www.kaggle.com/wsj/college-salaries">Where it Pays to Attend College</a> dataset is not new -While students choose university and department, they wonder how much they will pay after graduation. therefore we will find answers to some questions in this data.
# 

# ## 2. Importing dataset and data preprocessing
# <a id="importing_dataset_and_data_preprocessing"></a>
# 

# ### 2.1. Importing essential libraries
# <a id="importing_essential_libraries"></a>

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import random as rnd
import plotly.plotly as py
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
import plotly.graph_objs as go
import matplotlib.gridspec as gridspec
from sklearn.preprocessing import StandardScaler
from numpy import genfromtxt
from scipy.stats import multivariate_normal
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score , average_precision_score
from sklearn.metrics import precision_score, precision_recall_curve
import re
from sklearn.metrics import confusion_matrix
from wordcloud import WordCloud
from collections import Counter 
get_ipython().run_line_magic('matplotlib', 'inline')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# ### 2.2. Importing datasets
# <a id="importing_datasets"></a>

# In[ ]:


major=pd.read_csv('../input/degrees-that-pay-back.csv',encoding="windows-1252")
collage=pd.read_csv('../input/salaries-by-college-type.csv',encoding="windows-1252")
region=pd.read_csv('../input/salaries-by-region.csv',encoding="windows-1252") 


# ### 2.3.Summarize the datasets
# <a id="Summarize_the_dataset"></a>

# In[ ]:


major.info() 


# In[ ]:


major.isnull().sum()


# In[ ]:


major.head() 


# In[ ]:


collage.info() 


# In[ ]:


collage.isnull().sum()


# In[ ]:


collage.head() 


# In[ ]:


region.info() 


# In[ ]:


region.isnull().sum()


# In[ ]:


region.head() 


# <b>NOTE:</b> We have got two problems:First, there is a missing data in dataset so dataset are incomplete. Secondly, there is space in columns and columns' types are object so we need to remove the spaces in the columns and change the values of the columns

# ### 2.4. Data preprocessing
# <a id="data_preprocessing"></a>

# #### 2.4.1. Change of Data's columns
# <a id="change_data's_columns"></a>

# <b>NOTE:</b>There aremany ways but i will show you 2 of them. First we can remove the spaces and write small. Secondly, we can renaming the columns. Let's look both of them.

# In[ ]:


#First we can remove the space and write all columns small.
#major.columns=[each.lower() for each in major.columns]
#major.columns=[each.split()[0]+"_"+each.split()[1] if (len(each.split())>1) else each for each in major.columns] 


# In[ ]:


#second way
major_columns = {
    "Undergraduate Major" : "major",
    "Starting Median Salary" : "start",
    "Mid-Career Median Salary" : "mid_p50",
    "Percent change from Starting to Mid-Career Salary" : "increase",
    "Mid-Career 10th Percentile Salary" : "mid_p10",
    "Mid-Career 25th Percentile Salary" : "mid_p25",
    "Mid-Career 75th Percentile Salary" : "mid_p75",
    "Mid-Career 90th Percentile Salary" : "mid_p90"
}

major.rename(columns=major_columns, inplace=True)

collage_columns = {
    "School Name" : "name",
    "School Type" : "type",
    "Starting Median Salary" : "start",
    "Mid-Career Median Salary" : "mid_p50",
    "Mid-Career 10th Percentile Salary" : "mid_p10",
    "Mid-Career 25th Percentile Salary" : "mid_p25",
    "Mid-Career 75th Percentile Salary" : "mid_p75",
    "Mid-Career 90th Percentile Salary" : "mid_p90"
}

collage.rename(columns=collage_columns, inplace=True)

region_columns = {
    "School Name" : "name",
    "Region" : "region",
    "Starting Median Salary" : "start",
    "Mid-Career Median Salary" : "mid_p50",
    "Mid-Career 10th Percentile Salary" : "mid_p10",
    "Mid-Career 25th Percentile Salary" : "mid_p25",
    "Mid-Career 75th Percentile Salary" : "mid_p75",
    "Mid-Career 90th Percentile Salary" : "mid_p90"
}

region.rename(columns=region_columns, inplace=True) 


# #### 2.4.1. Change of Data columns types
# <a id="(change_data_types"></a>

# <b>NOTE:</b>  We are changing type of columns which is including money variables

# In[ ]:


def change_to_num(money):
    if type(money)== str and money[0] == '$':
        a = money[1:].replace(',','')
        return float(a)
    else:
        return money
type(change_to_num('$234,54.00')) 


# In[ ]:


major=major.applymap(change_to_num) 
collage=collage.applymap(change_to_num) 
region=region.applymap(change_to_num) 


# In[ ]:


major.info() 


# ## 3. Data Visualization 
# <a id="data_visualization"></a>

# ### 3.1.Salary According to Undergraduate Major
# <a id="major">

# In[ ]:


Feature = major['major'].value_counts().index
plt.subplots(figsize=(10,8))
wordcloud = WordCloud(
                        background_color = 'black',
                        width=512,
                        height=384
                        ).generate(" ".join(Feature))
plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('graph.png')
plt.show() 


# <b>NOTE:</b> The most department is 'Engineering' in the university.

# <b>Question:</b> Which undergraduate majors get the highest income at the start of their career?

# In[ ]:


major.sort_values('start',ascending=False)
sns.barplot(y='major', x='start', data=major.sort_values('start',ascending=False))
fig = plt.gcf() 
fig.set_size_inches(15,20)  


# <b>NOTE:</b>  Physician Assistants get the highest income at the start of their career.

# In[ ]:


Feature = major['major']
weightage = major['start']
total = major['mid_p50']
percent=major['increase']
mid_pos=(major['start'] + major['mid_p50']) / 2
weightage = np.array(weightage)
Feature = np.array(Feature)
total = np.array(total)
percent = np.array(percent)
mid_pos = np.array(mid_pos)

idx = weightage.argsort()
Feature, total,percent,mid_pos,weightage = [np.take(x, idx) for x in [Feature, total,percent,mid_pos,weightage]]


s = 1 
size=[] 
for i,cn in enumerate(weightage):
    s=s+1
    size.append(s) 
    


# In[ ]:


fig, ax = plt.subplots(figsize=(8,16))

ax.scatter(total,size,marker="o",color="lightBlue",s=size,linewidths=10)
ax.scatter(weightage,size,marker="o",color="lightGreen",s=size,linewidths=10)
ax.set_xlabel('Median Salary')
ax.set_ylabel('Undergraduate Major')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.grid() 
for i, txt in enumerate(Feature):
    ax.annotate(txt, (110000,size[i]),fontsize=12,rotation=0,color='Brown')
    ax.annotate('.',xy=(total[i],size[i]), xytext=(weightage[i],size[i]),
               arrowprops=dict(facecolor='LightGreen',shrink=0.06),
               )
for i, pct in enumerate(percent):
    ax.annotate(pct,(mid_pos[i],size[i]),fontsize=12,rotation=0,color='Brown')
    
ax.annotate('Start',(35000,52),fontsize=14,rotation=0,color='Green')
ax.annotate('Median Salary',(35000,53),fontsize=14,rotation=0,color='Blue')
ax.annotate('.',xy=(110000, 52.5), xytext=(68000, 52.5),
           arrowprops=dict(facecolor='LightGreen',shrink=0.06),)
ax.annotate('Percent increase in the salary', (70000,53), fontsize=14,rotation=0,color='Brown'); 


# In[ ]:


df = major.sort_values('increase',ascending=False).iloc[:25,:] 
#Creating trace1
trace1 = go.Scatter(
                    x=df.increase,
                    y=df.mid_p50,
                    mode= "lines",
                    name= "Median of salary", 
                    marker = dict(color = 'rgba(16,112,2,0.8)'),
                    text= df.major)

#Creating trace2
trace2 = go.Scatter(
                     x=df.increase,
                    y=df.start,
                    mode= "lines+markers",
                    name= "start salary",
                    marker = dict(color = 'rgba(16,112,2,0.8)'),
                    text= df.major)
data=[trace1,trace2]
layout = dict(title= 'Start and Top of salary vs Increase of top 25 major',
             xaxis=dict(title='Percent change from Starting to Mid-Career Salary',ticklen=5,zeroline=False)
             )
fig = dict(data=data, layout=layout)
iplot(fig) 


# In[ ]:


sns.barplot(y='major', x='increase', data=major.sort_values('increase',ascending=False).head(20))
fig = plt.gcf() 
fig.set_size_inches(10,8) 


# In[ ]:


df = major.sort_values('mid_p90',ascending=False).iloc[:7,:] 
trace1 = go.Bar(
                x=df.major,
                y=df.mid_p90,
                name="Long-term salary",
                marker = dict(color= 'rgba(225, 174, 225, 0.5)',
                            line=dict(color='rgb(0,0,0)',width=1.5)),
                text=df.major)

trace2 = go.Bar( 
                x=df.major,
                y=df.mid_p50,
                name="Median salary",
                marker = dict(color= 'rgba(225, 225, 128, 0.5)',
                            line=dict(color='rgb(0,0,0)',width=1.5)),
                text=df.major)
data = [trace1,trace2]
layout = go.Layout(barmode = "group") 
fig = go.Figure(data=data , layout=layout)
iplot(fig) 


# <b>RESULT:</b> 
# * Physician Assistants start their career noticeably with the best salary. 
# * In the middle of the career, Chemical Engineers and then Computer Engineers get the best salary. 
# * In the long term, Economists have the salary advanteges who earns the best salary when compared to others.
# * Mathematicians and Philosophers have the most increase in their salary during their career.
# * As a result of analyzes we have made, different jobs have different advantages in their career opportunuties when start salary, long term salary and increase in salary percentage compared.

# ### 3.2. Salary According to School Type 
# <a id="school_type"></a>

# <b>Question:</b> From which school when you graduate, you get the highest income ?

# In[ ]:


collage.groupby('type').mean().plot(kind='bar',figsize=(10,7)) 
plt.show() 


# <b> NOTE: </b> According to graph which type of school gets salaries when start,10percent,1st quarter, median,3rd quarter and long-term of your career

# In[ ]:


fig, ax = plt.subplots(figsize=(15,10), ncols=3, nrows=1)

y_title_margin = 1.0 

ax[0].set_title("Starting Salary", y = y_title_margin)
ax[1].set_title("Mid-career Salary", y = y_title_margin)
ax[2].set_title("3rd quarter Salary", y = y_title_margin)

ax[0].set_xticklabels(collage['type'], rotation='vertical', fontsize='large')
ax[1].set_xticklabels(collage['type'], rotation='vertical', fontsize='large')
ax[2].set_xticklabels(collage['type'], rotation='vertical', fontsize='large')
ax[0].set_ylim(35000,250000)
ax[1].set_ylim(35000,250000)
ax[2].set_ylim(35000,250000)

sns.boxplot(x='type',y='start', data=collage,ax=ax[0]) 
sns.boxplot(x='type',y='mid_p50', data=collage,ax=ax[1])
sns.boxplot(x='type',y='mid_p75', data=collage,ax=ax[2])

plt.tight_layout() 


# <b> NOTE: There isn't noticeable difference between Engineering and lvg League in start salary. However there is a big differencebetween them in 3rd quarter of your career's salary  </b> 

# In[ ]:


Ivy_league = collage[collage.type == "Ivy League"]

trace0 = go.Box(
                y=Ivy_league.mid_p50,
                name='Median salary of Ivy League',
                marker = dict(
                    color = 'rgb(12, 12, 140)',
                )
        )

trace1 = go.Box(
                y=Ivy_league.mid_p75,
                name='3rd Quarter salary of Ivy League',
                marker = dict(
                    color = 'rgb(12, 120, 140)',
                )
        )
data = [trace0, trace1]
iplot(data) 


# In[ ]:


Feature = []
school = []
med_sal = []
v_features = collage['type'].value_counts().index 
for i, cn in enumerate(v_features):
    Feature.append(str(cn))
    filtered = collage[(collage['type']==str(cn))]
    temp = filtered[filtered['mid_p50'] == filtered['mid_p50'].max()]['name'].values  
    temp1 = temp[0]
    tempval = filtered['mid_p50'].max()
    school.append(temp1)
    med_sal.append(tempval) 
    
f,ax = plt.subplots(figsize=(15,7))
g = sns.barplot( y = Feature,
               x = med_sal,
               palette = "GnBu_d")
plt.title("Top collages from each School type provide highest salary in median career")

for i, v in enumerate(school): 
    ax.text(.5, i, v,fontsize=16,color='white',weight='bold')
fig=plt.gcf()
plt.show() 


# <b> NOTE: </b> Of the people whose school type is Lvy League, the ones whose salary is highest in the mids of theirs careers are graduates from Dartmounth Collage.

# *<b> RESULT: </b> 
# * When graduates from different school types compared, there isn't important differences in terms of start salary. The exception is that, graduates from Lvy League start their career with the highest salary than any others.
# * There is a noticable differences who is graduates from Lvy League,  medium and 3rd quarter of salary career with the highest salary than any others.

# ### 3.3. Salary According to Region 
# <a id="region"></a>

# <b>Question:</b> In which region graduation you will higher earn money?

# In[ ]:


Feature = []
school  = []
Med_sal = []
v_features = region['region'].value_counts().index
for i, cn in enumerate(v_features):
     Feature.append(str(cn)) 
     filtered = region[(region['region']==str(cn))]
     temp = filtered[filtered['mid_p50'] == filtered['mid_p50'].max()]['name'].values
     temp1 = temp[0]
     tempval = filtered['mid_p50'].max()
     school.append(temp1)
     Med_sal.append(tempval)

f, ax = plt.subplots(figsize=(15, 7)) 
g = sns.barplot( y = Feature,
            x = Med_sal,
                palette="GnBu_d")
plt.title("Median of Career Top colleges from each region ensuring highest pay")

for i, v in enumerate(school): 
    ax.text(.5, i, v,fontsize=16,color='white',weight='bold')
fig=plt.gcf()
plt.show() 


# In[ ]:


Feature = []
school  = []
Med_sal = []
v_features = region['region'].value_counts().index
for i, cn in enumerate(v_features):
     Feature.append(str(cn)) 
     filtered = region[(region['region']==str(cn))]
     temp = filtered[filtered['mid_p75'] == filtered['mid_p75'].max()]['name'].values
     temp1 = temp[0]
     tempval = filtered['mid_p75'].max()
     school.append(temp1)
     Med_sal.append(tempval)

f, ax = plt.subplots(figsize=(15, 7)) 
g = sns.barplot( y = Feature,
            x = Med_sal,
                palette="GnBu_d")
plt.title("3rd Quarter of Career Top colleges from each region ensuring highest pay")

for i, v in enumerate(school): 
    ax.text(.5, i, v,fontsize=16,color='white',weight='bold')
fig=plt.gcf()
plt.show() 


# In[ ]:


region.groupby('region').mean().plot(kind='bar',figsize=(10,7)) 
plt.show() 


# <b> RESULT: </b> The people who is working in northeastern,they get more salaries every period of their careers.

# <b>NOTE:</b>  The comments are important for improving.
