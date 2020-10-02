#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import warnings


# plotly
# import plotly.plotly as py

from plotly.offline import init_notebook_mode, iplot, plot
import plotly as py
init_notebook_mode(connected=True)
import plotly.graph_objs as go

# word cloud library
from wordcloud import WordCloud

# matplotlib
import matplotlib.pyplot as plt
# Input data files are available in the "../input/" directory.
# For example, running
warnings.filterwarnings('ignore')


# ### Before you read, please upvote if you find helpful

# # India has the fastest growing Data Science community !

# ## Almost 25 % of respondents were from India followed by USA with 15 %

# In[ ]:


# Reading data

mcr_2019 = pd.read_csv('/kaggle/input/kaggle-survey-2019/multiple_choice_responses.csv')


# In[ ]:


columns = list(mcr_2019.columns)
countries = pd.DataFrame(mcr_2019['Q3'].value_counts().reset_index())
countries=countries.rename({'index':'country', 'Q3':'entries'}, axis=1)

import plotly.express as px  # Be sure to import express
fig = px.choropleth(countries,
                    locations='country',  # DataFrame column with locations
                    color='entries',  # DataFrame column with color values
                    locationmode = 'country names', # Set to plot
                    color_continuous_scale='viridis')
fig.update_layout(
    title_text = '2019 Kaggle survey respondents per country')

fig.show()  # Output the plot to the screen


# ## Why so many respondents from India

# ## Lets analyse data of India

# In[ ]:


pop_age = pd.DataFrame(mcr_2019[mcr_2019['Q3']=='India']['Q1'].value_counts().reset_index())
pop_age = pop_age.rename({'index':'Age','Q1':'count'}, axis=1)


# In[ ]:



fig = px.bar(pop_age, x = 'Age', y = 'count', title= 'Age wise users in India')
fig.show();


# ## Most people are in age 18-21 and 76 percent people are below age 30

# # gender distribution

# In[ ]:


pop_male_age =  pd.DataFrame(mcr_2019[np.logical_and(mcr_2019['Q3']=='India' , mcr_2019['Q2']=='Male')]['Q1'].value_counts().reset_index())
pop_male_age = pop_male_age.rename({'index' : 'Age', 'Q1' : 'number'}, axis = 1)
pop_female_age =  pd.DataFrame(mcr_2019[np.logical_and(mcr_2019['Q3']=='India' , mcr_2019['Q2']=='Female')]['Q1'].value_counts().reset_index())
pop_female_age = pop_female_age.rename({'index' : 'Age', 'Q1' : 'number'}, axis = 1)


# In[ ]:


ages = ['18-21', '22-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-49', '60-69', '70+']

import plotly.graph_objs as go
# create trace1 
trace1 = go.Bar(
                x = pop_male_age.Age,
                y = pop_male_age.number,
                name = "male",
                marker = dict(color = 'rgba(25, 100, 255, 0.6)',
                             line=dict(color='rgb(0,0,0)',width=1.5)),
                )
# create trace2 
trace2 = go.Bar(
                x = pop_female_age.Age,
                y = pop_female_age.number,
                name = "female",
                marker = dict(color = 'rgba(255, 174, 255, 0.9)',
                              line=dict(color='rgb(0,0,0)',width=1.5)),
                )
data = [trace1, trace2]
layout = go.Layout(barmode = "group")
fig = go.Figure(data = data, layout = layout)
iplot(fig)


# ## There are less females as compared to males

# In[ ]:


pie1_list = np.array(mcr_2019[mcr_2019['Q3']=='India']['Q2'].value_counts()[:2])
labels = ['Male','Female']
# figure
fig = {
  "data": [
    {
      "values": pie1_list,
      "labels": labels,
      "domain": {"x": [0, .5]},
      "name": "Number Of Students Rates",
      "hoverinfo":"label+percent+name",
      "hole": .3,
      "type": "pie"
    },],
  "layout": {
        "title":"Gender Ratio in India",
        "annotations": [
            { "font": { "size": 20},
              "showarrow": False,
              "text": "Number of people",
                "x": 0.50,
                "y": 1
            },
        ]
    }
}
iplot(fig)


# # Degree types

# In[ ]:


pie1_list = np.array(mcr_2019[mcr_2019['Q3']=='India']['Q4'].value_counts()[:4])
labels = ['Bachelors','Masters','Doctoral','Professional']
# figure
fig = {
  "data": [
    {
      "values": pie1_list,
      "labels": labels,
      "domain": {"x": [0, .5]},
      "hoverinfo":"label+percent+name",
      "hole": .3,
      "type": "pie"
    },],
  "layout": {
        "title":"Degree types",
        "annotations": [
            { "font": { "size": 20},
              "showarrow": False,
              "text": "",
                "x": 0.50,
                "y": 1
            },
        ]
    }
}
iplot(fig)


# ## Majorly peope have a Bachelor's degree followed by Master's

# # job type

# In[ ]:


pie1_list = [1531, 765, 720, 350, 283]
labels = ['Student', 'Data Scientist', 'Software Eng.','Data Analyst', 'Not Employed']
# figure
fig = {
  "data": [
    {
      "values": pie1_list,
      "labels": labels,
      "domain": {"x": [0, .5]},
      "hoverinfo":"label+percent+name",
      "hole": .3,
      "type": "pie"
    },],
  "layout": {
        "title":"Job types",
        "annotations": [
            { "font": { "size": 20},
              "showarrow": False,
              "text": "Percent of people",
                "x": 0.50,
                "y": 1
            },
        ]
    }
}
iplot(fig)


# ## Most of people are Students who are interested in Data Science/ Machine Learning.
# ## India has 35% youth, Data Science seems to provide a promising career choice

# In[ ]:


empl = mcr_2019[mcr_2019['Q3']=='India'][['Q1','Q5']]
empl = pd.DataFrame(empl.groupby('Q1')['Q5'].value_counts())


# In[ ]:


Stud = []
DataSc = []
SE = []
DataAn = []
NE = []

for i in ages[:6]:
    Stud.append(empl[np.logical_and(empl.index.get_level_values(0)==i, empl.index.get_level_values(1)=='Student')].Q5[0])
    DataSc.append(empl[np.logical_and(empl.index.get_level_values(0)==i, empl.index.get_level_values(1)=='Data Scientist')].Q5[0])
    SE.append(empl[np.logical_and(empl.index.get_level_values(0)==i, empl.index.get_level_values(1)=='Software Engineer')].Q5[0])
    DataAn.append(empl[np.logical_and(empl.index.get_level_values(0)==i, empl.index.get_level_values(1)=='Data Analyst')].Q5[0])
    NE.append(empl[np.logical_and(empl.index.get_level_values(0)==i, empl.index.get_level_values(1)=='Not employed')].Q5[0])


# In[ ]:


import plotly.graph_objects as go

x=ages
fig = go.Figure(go.Bar(x=x, y=Stud, name='Students',marker = dict(color = 'rgba(25, 25, 255, 0.8)')))
fig.add_trace(go.Bar(x=x, y=DataSc, name='Data Scientists',marker = dict(color = 'rgba(25, 255, 25, 0.8)')))
fig.add_trace(go.Bar(x=x, y=SE, name='Software Eng.',marker = dict(color = 'rgba(25, 0, 25, 0.8)')))
fig.add_trace(go.Bar(x=x, y=DataAn, name='Data Analysts',marker = dict(color = 'rgba(255, 10, 25, 0.8)')))
fig.add_trace(go.Bar(x=x, y=NE, name='Not Employed',marker = dict(color = 'rgba(25, 100, 25, 0.8)')))

fig.update_layout(barmode='stack')
fig.show()


# ## We can see majority of people are students between age 18-21 
# ## There are more Data Scientists as compared to other job types , it is obvious as this is kaggle survey
# ## There is also a group of people unemployed in almost each age group, these may be people looking for career transition to Data Science

# # Company sizes

# In[ ]:


pie1_list = list(mcr_2019[mcr_2019['Q3']=='India']['Q6'].value_counts().values)
labels = list(mcr_2019[mcr_2019['Q3']=='India']['Q6'].value_counts().index)
# figure
fig = {
  "data": [
    {
      "values": pie1_list,
      "labels": labels,
      "domain": {"x": [0, .5]},
      "hoverinfo":"label+percent+name",
      "hole": .3,
      "type": "pie"
    },],
  "layout": {
        "title":"",
        "annotations": [
            { "font": { "size": 20},
              "showarrow": False,
              "text": "Company Size",
                "x": 0.50,
                "y": 1
            },
        ]
    }
}
iplot(fig)


# ## There are 40% people work in company of size less than 249 which must be startups

# In[ ]:


country_ind = mcr_2019[mcr_2019['Q3']=='India']


# In[ ]:


ages = ages[0:8]


# In[ ]:


small=[]
small_mid=[]
mid = []
large_mid = []
large = []

for i in ages:
    small.append(country_ind[country_ind['Q1']==i]['Q6'].value_counts().values[0])        
for i in ages:
    small_mid.append(country_ind[country_ind['Q1']==i]['Q6'].value_counts().values[1])
for i in ages:
    mid.append(country_ind[country_ind['Q1']==i]['Q6'].value_counts().values[2])
for i in ages:
    large_mid.append(country_ind[country_ind['Q1']==i]['Q6'].value_counts().values[3])
for i in ages:
    large.append(country_ind[country_ind['Q1']==i]['Q6'].value_counts().values[4])


# In[ ]:


import plotly.graph_objects as go

x=ages
fig = go.Figure(go.Bar(y=x, x=small, name='0 - 49',marker = dict(color = 'rgba(255, 25, 255, 0.8)'),orientation='h'))
fig.add_trace(go.Bar(y=x, x=small_mid, name='> 10k',marker = dict(color = 'rgba(25, 255, 25, 0.8)'),orientation='h'))
fig.add_trace(go.Bar(y=x, x=mid, name='50 - 249',marker = dict(color = 'rgba(25, 0, 25, 0.8)'),orientation='h'))
fig.add_trace(go.Bar(y=x, x=large_mid, name='250 - 999',marker = dict(color = 'rgba(255, 10, 25, 0.8)'),orientation='h'))
fig.add_trace(go.Bar(y=x, x=large, name='1k - 10k',marker = dict(color = 'rgba(25, 100, 25, 0.8)'),orientation='h'))

fig.update_layout(barmode='stack')
fig.show()


# ## people with age 18-21 are mostly students so in this age group we find less working professionals, if not students then are working for a startup
# ## Age 24-29 has most employees and either they work for startup or for a large company
# ## Generally we find most people working in companies with less people.

# # Favourite references =

# In[ ]:


mcr_2019 = country_ind

twitter = mcr_2019['Q12_Part_1'].value_counts().values[0]
hacker_news = mcr_2019['Q12_Part_2'].value_counts().values[0]
reddit = mcr_2019['Q12_Part_3'].value_counts().values[0]
kagle = mcr_2019['Q12_Part_4'].value_counts().values[0]
fastai = mcr_2019['Q12_Part_5'].value_counts().values[0]
youtube = mcr_2019['Q12_Part_6'].value_counts().values[0]
podcasts = mcr_2019['Q12_Part_7'].value_counts().values[0]
blogs = mcr_2019['Q12_Part_8'].value_counts().values[0]
journals = mcr_2019['Q12_Part_9'].value_counts().values[0]
slack = mcr_2019['Q12_Part_10'].value_counts().values[0]

pie1_list = [twitter, hacker_news, reddit, kagle, fastai, youtube, podcasts, blogs, journals, slack]
labels = ['twitter', 'hacker_news', 'reddit', 'kaggle', 'fastai', 'youtube', 'podcasts', 'blogs', 'journals', 'slack'] 

import plotly.graph_objects as go

labels = labels
values = pie1_list

fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.show()
print("References used:")


# ## Kaggle is mostly used for references, followed by Blogs and Youtube

# ## Lets see references for students as they contribute most

# In[ ]:


Ind_Stu = country_ind[country_ind['Q5']=='Student']


# In[ ]:


twitter = Ind_Stu['Q12_Part_1'].value_counts().values[0]
hacker_news = Ind_Stu['Q12_Part_2'].value_counts().values[0]
reddit = Ind_Stu['Q12_Part_3'].value_counts().values[0]
kagle = Ind_Stu['Q12_Part_4'].value_counts().values[0]
fastai = Ind_Stu['Q12_Part_5'].value_counts().values[0]
youtube = Ind_Stu['Q12_Part_6'].value_counts().values[0]
podcasts = Ind_Stu['Q12_Part_7'].value_counts().values[0]
blogs = Ind_Stu['Q12_Part_8'].value_counts().values[0]
journals = Ind_Stu['Q12_Part_9'].value_counts().values[0]
slack = Ind_Stu['Q12_Part_10'].value_counts().values[0]

pie1_list = [twitter, hacker_news, reddit, kagle, fastai, youtube, podcasts, blogs, journals, slack]
labels = ['twitter', 'hacker_news', 'reddit', 'kaggle', 'fastai', 'youtube', 'podcasts', 'blogs', 'journals', 'slack'] 



colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen','silver','red','Purple','blue','green','darkblue']

fig = go.Figure(data=[go.Pie(labels= labels,
                             values=pie1_list)])
fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2),), title='References used by students', titlefont_size=20)
fig.show()


# ## Stats not differ much for students

# # Courses prefered

# In[ ]:


Udacity = Ind_Stu['Q13_Part_1'].value_counts().values[0]
coursera = Ind_Stu['Q13_Part_2'].value_counts().values[0]
edX = Ind_Stu['Q13_Part_3'].value_counts().values[0]
Datacamp = Ind_Stu['Q13_Part_4'].value_counts().values[0]
Dataquest = Ind_Stu['Q13_Part_5'].value_counts().values[0]
Kaggle = Ind_Stu['Q13_Part_6'].value_counts().values[0]
Fastai = Ind_Stu['Q13_Part_7'].value_counts().values[0]
Udemy = Ind_Stu['Q13_Part_8'].value_counts().values[0]
Linkedin = Ind_Stu['Q13_Part_9'].value_counts().values[0]
University_degree = Ind_Stu['Q13_Part_10'].value_counts().values[0]

pie1_list = [Udacity, coursera, edX, Datacamp, Dataquest, Kaggle, Fastai, Udemy, Linkedin, University_degree]
labels = ['Udacity', 'coursera', 'edX', 'Datacamp', 'Dataquest', 'Kaggle', 'Fastai', 'Udemy', 'Linkedin', 'University_degree'] 



colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen','silver','red','Purple','blue','green','darkblue']

fig = go.Figure(data=[go.Pie(labels= labels,
                             values=pie1_list)])
fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)), title = 'Courses prefered by Indian Students', titlefont_size = 20)
fig.show()


# ## Coursera is mostly used followed by Udemy
# ## Everyone must have seen Andrew NG's machine learning Course

# # IDE used

# In[ ]:


jupyter = Ind_Stu['Q16_Part_1'].value_counts().values[0]
r_studio = Ind_Stu['Q16_Part_2'].value_counts().values[0]
pycharm = Ind_Stu['Q16_Part_3'].value_counts().values[0]
atom = Ind_Stu['Q16_Part_4'].value_counts().values[0]
matlab = Ind_Stu['Q16_Part_5'].value_counts().values[0]
vs_code = Ind_Stu['Q16_Part_6'].value_counts().values[0]
spyder = Ind_Stu['Q16_Part_7'].value_counts().values[0]
notepad = Ind_Stu['Q16_Part_9'].value_counts().values[0]
sublime = Ind_Stu['Q16_Part_10'].value_counts().values[0]


# In[ ]:



ide = pd.DataFrame(data = np.array([jupyter, spyder, vs_code, sublime, pycharm, r_studio, atom ,matlab,notepad]),)
ide['names'] = ['jupyter', 'spyder', 'vs_code', 'sublime', 'pycharm','r_studio','atom','matlab','notepad']
ide = ide.rename(columns = {0:'ide_usage'})


# In[ ]:


fig = px.bar(ide, x = 'names', y = 'ide_usage', )
fig.show();


# ## There are mostly Data Scientists in the survey so Jupyter Notebook is the obviuos choice

# ## Lets see which group of people uses Online notebook's like kaggle and colab more

# In[ ]:


#country_ind[country_ind['Q17_Part_1'].isnull() + country_ind['Q17_Part_2'].isnull() + country_ind['Q17_Part_3'].isnull() + country_ind['Q17_Part_4'].isnull() + country_ind['Q17_Part_5'].isnull() + country_ind['Q17_Part_6'].isnull() + country_ind['Q17_Part_7'].isnull() + country_ind['Q17_Part_8'].isnull() + country_ind['Q17_Part_9'].isnull() + country_ind['Q17_Part_10'].isnull() + country_ind['Q17_Part_11'].isnull() + country_ind['Q17_Part_12'].isnull()]['Q5'].value_counts()
values = country_ind[~country_ind['Q17_Part_1'].isnull() + ~country_ind['Q17_Part_2'].isnull() + ~country_ind['Q17_Part_3'].isnull() + ~country_ind['Q17_Part_4'].isnull() + ~country_ind['Q17_Part_5'].isnull() + ~country_ind['Q17_Part_6'].isnull() + ~country_ind['Q17_Part_7'].isnull() + ~country_ind['Q17_Part_8'].isnull() + ~country_ind['Q17_Part_9'].isnull() + ~country_ind['Q17_Part_10'].isnull() + ~country_ind['Q17_Part_11'].isnull() + ~country_ind['Q17_Part_12'].isnull()]['Q5'].value_counts().values
labels = list(country_ind[~country_ind['Q17_Part_1'].isnull() + ~country_ind['Q17_Part_2'].isnull() + ~country_ind['Q17_Part_3'].isnull() + ~country_ind['Q17_Part_4'].isnull() + ~country_ind['Q17_Part_5'].isnull() + ~country_ind['Q17_Part_6'].isnull() + ~country_ind['Q17_Part_7'].isnull() + ~country_ind['Q17_Part_8'].isnull() + ~country_ind['Q17_Part_9'].isnull() + ~country_ind['Q17_Part_10'].isnull() + ~country_ind['Q17_Part_11'].isnull() + ~country_ind['Q17_Part_12'].isnull()]['Q5'].value_counts().index)


# In[ ]:


fig = go.Figure([go.Bar(x = labels, y = values)])
fig.show();


# ## As we expected Students uses these services more , this is also the reason most of students are able to learn and practice Machine learning since students cant afford high end specifications.

# In[ ]:


kaggle = Ind_Stu['Q17_Part_1'].value_counts().values[0]
colab = Ind_Stu['Q17_Part_2'].value_counts().values[0]
microsoft_azure = Ind_Stu['Q17_Part_3'].value_counts().values[0]
gcp = Ind_Stu['Q17_Part_4'].value_counts().values[0]
paperspace = Ind_Stu['Q17_Part_5'].value_counts().values[0]
floyd_hub = Ind_Stu['Q17_Part_6'].value_counts().values[0]
binder = Ind_Stu['Q17_Part_7'].value_counts().values[0]
ibm_watson = Ind_Stu['Q17_Part_8'].value_counts().values[0]
code_ocean = Ind_Stu['Q17_Part_9'].value_counts().values[0]
aws = Ind_Stu['Q17_Part_10'].value_counts().values[0]

pie1_list = [kaggle, colab, microsoft_azure, gcp, paperspace, floyd_hub, binder, ibm_watson, code_ocean, aws]
labels = ['kaggle', 'colab', 'microsoft_azure', 'gcp', 'paperspace', 'floyd_hub', 'binder/jupyter hub', 'ibm_watson', 'code_ocean', 'aws']


#colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen','silver','red','Purple','blue','green','darkblue']

fig = go.Figure(data=[go.Pie(labels= labels,
                             values=pie1_list)])
fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig.show()


# ## Students use kaggle and colab more than any other notebook

# ## Lets see which programming language is used mostly

# In[ ]:


python = country_ind['Q18_Part_1'].value_counts().values[0]
r = country_ind['Q18_Part_2'].value_counts().values[0]
sql = country_ind['Q18_Part_3'].value_counts().values[0]
c = country_ind['Q18_Part_4'].value_counts().values[0]
cpp = country_ind['Q18_Part_5'].value_counts().values[0]
java = country_ind['Q18_Part_6'].value_counts().values[0]
javascript = country_ind['Q18_Part_7'].value_counts().values[0]
typescript = country_ind['Q18_Part_8'].value_counts().values[0]
bash = country_ind['Q18_Part_9'].value_counts().values[0]
matlab = country_ind['Q18_Part_10'].value_counts().values[0]

labels = ['python','sql','r','cpp','c','java','javascript','matlab','bash','typescript']
values = [python, sql, r, cpp, c, java, javascript, matlab, bash, typescript]


fig = go.Figure([go.Bar(x = labels, y = values)])
fig.show();


# ## Python is the most used language followed by sql and R 
# ## Lets see which language is used more in specific job types

# In[ ]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

labels = ['Student', 'Software Engineer', 'Data Scientist', 'Manager', 'Data Analyst']
specs = [[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]]

fig = make_subplots(rows=2, cols=2, specs=specs)

fig.add_trace(go.Pie(labels=labels, values=[1072, 426, 546, 90, 207], name='python',title='Python',
                     ), 1, 1)
fig.add_trace(go.Pie(labels=labels, values=[200, 68, 218, 42, 90], name='SQL', title = 'SQL',
                     ), 1, 2)
fig.add_trace(go.Pie(labels=labels, values=[320, 222, 281, 52, 139], name='R', title = 'R',
                     ), 2, 1)
fig.add_trace(go.Pie(labels=labels, values=[230, 168, 62, 30, 10], name='java', title = 'JAVA',
                     ), 2, 2)


# ## R, Python, SQL is mostly used by students and data scientists
# ## JAVA is mostly used by students and Software Engineers

# # Mostly used data visualisations library

# In[ ]:


ggplot = country_ind['Q20_Part_1'].value_counts().values[0]
matplotlib = country_ind['Q20_Part_2'].value_counts().values[0]
altair = country_ind['Q20_Part_3'].value_counts().values[0]
shiny = country_ind['Q20_Part_4'].value_counts().values[0]
d3js = country_ind['Q20_Part_5'].value_counts().values[0]
plotly = country_ind['Q20_Part_6'].value_counts().values[0]
bokeh = country_ind['Q20_Part_7'].value_counts().values[0]
seaborn = country_ind['Q20_Part_8'].value_counts().values[0]

pie1_list = [ggplot, matplotlib, altair, shiny, d3js, plotly, bokeh, seaborn]
labels = ['ggplot', 'matplotlib', 'altair', 'shiny', 'd3js', 'plotly', 'bokeh', 'seaborn'] 



colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen','silver','red','Purple','blue','green','darkblue']

fig = go.Figure(data=[go.Pie(labels= labels,
                             values=pie1_list)])
fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig.show()


# ## Matplotlib and seaborn are mostly used for data visualisations

# # Use of cpu, gpu and tpu's

# In[ ]:


cpu = country_ind['Q21_Part_1'].value_counts().values[0]
gpu = country_ind['Q21_Part_2'].value_counts().values[0]
tpu = country_ind['Q21_Part_3'].value_counts().values[0]


colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen','silver','red','Purple','blue','green','darkblue']

fig = go.Figure(data=[go.Pie(labels= ['cpu','gpu','tpu'],
                             values=[cpu, gpu, tpu])])
fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig.show()


# ## Use of cpu, gpu is common but Tpu is hardly used

# # Years of experience in using machine learning

# In[ ]:


fig = go.Figure([go.Bar(x = list(country_ind['Q23'].value_counts().index), y = country_ind['Q23'].value_counts().values)])
fig.show();


# ## Almost 83 % people have less than two years of experience, these are majorly students 

# # Mostly used Machine learning algorithms

# In[ ]:


Regression = country_ind['Q24_Part_1'].value_counts().values[0]
Decision_trees = country_ind['Q24_Part_2'].value_counts().values[0]
xgboost = country_ind['Q24_Part_3'].value_counts().values[0]
Naive_bayes = country_ind['Q24_Part_4'].value_counts().values[0]
Neural_network = country_ind['Q24_Part_6'].value_counts().values[0]
Cnn = country_ind['Q24_Part_7'].value_counts().values[0]
Gans = country_ind['Q24_Part_8'].value_counts().values[0]
Rnn = country_ind['Q24_Part_9'].value_counts().values[0]
Transformer_network = country_ind['Q24_Part_10'].value_counts().values[0]

data = [Regression, Decision_trees, Cnn, xgboost, Naive_bayes, Rnn, Neural_network, Gans, Transformer_network]
labels = ['Regression', 'Decision_trees','Cnn', 'xgboost', 'Naive_bayes', 'Rnn', 'Neural_network', 'Gans', 'Transformer_network']

fig = go.Figure([go.Bar(x = labels, y = data)], )
fig.update_traces(marker=dict(color= '#00F000',line=dict(color='#000000', width=2)))
fig.show();


# ## Linear Regression and logistic Regression are mostly used followed by trees and CNN's

# # Mostly used cloud services

# In[ ]:


gcp = country_ind['Q29_Part_1'].value_counts().values[0]
aws = country_ind['Q29_Part_2'].value_counts().values[0]
azure = country_ind['Q29_Part_3'].value_counts().values[0]
ibm = country_ind['Q29_Part_4'].value_counts().values[0]
alibaba = country_ind['Q29_Part_5'].value_counts().values[0]
salesforce = country_ind['Q29_Part_6'].value_counts().values[0]
oracle = country_ind['Q29_Part_7'].value_counts().values[0]
sap = country_ind['Q29_Part_8'].value_counts().values[0]


colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen','silver','red','Purple','blue','green','darkblue']

fig = go.Figure(data=[go.Pie(labels= ['gcp', 'aws', 'azure', 'ibm', 'alibaba', 'salesforce', 'oracle', 'sap'],
                             values=[gcp, aws, azure, ibm, alibaba, salesforce, oracle, sap])])
fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig.show()


# ## AWS is mostly used followed by GCP and azure

# # CONCLUSION
# <ul>
#     
# ## <li>India has huge youth population, Data Science / Machine Learning seems to be a good career choice</li>
# 
# ## <li>References are easily available on kaggle/ youtube</li>
# 
# ## <li>Online courses on coursera and udemy are helpful</li>
# 
# ## <li>Kaggle and Google colab provide online resources which has helped students a lot</li>
# 
# ## <li>There are many startups being launched in India Since last few years and mostly are trying to incorporate Machine learning </li>
# 
# ## <li>Cloud services such as AWS and GCP provide 1 year free service and easy solutions</li>
# </ul>
