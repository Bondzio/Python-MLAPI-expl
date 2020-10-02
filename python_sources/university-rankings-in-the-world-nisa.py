#!/usr/bin/env python
# coding: utf-8

# # INTRODUCTION

# The Times Higher Education World University Ranking is widely regarded as one of the most influential and widely observed university measures, done in the United Kingdom in 2010.
# 
# In this tutorial, I am going to analyze the data and try to visuaize it with different kind of visualisation methods using plotly library.

# Parts of the notebook:

# 1. [Loading Data and Explanation of Features](#1)
# 1. [Line Charts](#2)
# 1. [Scatter Charts](#3)
# 1. [Bar Charts](#4)
# 1. [Pie Charts](#5)
# 1. [Bubble Charts](#6)
# 1. [Histogram](#7)
# 1. [Word Cloud](#8)
# 1. [Box Plot](#9)
# 1. [Scatter Plot Matrix](#10)
# 1. [Inset Plot](#11)
# 1. [3D Scatter Plot wiht Colorscaling](#12)
# 1. [Multiple Subplots](#13)

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# plotly
#import plotly.plotly as py
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected = True)
#from plotly.graph_objs as go

# word cloud library
from wordcloud import WordCloud

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# <a id = "1"></a>
# # 1.Load and Check Data

# In[ ]:


timesData = pd.read_csv("/kaggle/input/world-university-rankings/timesData.csv")


# ### Content of the data:
# * world_rank: world rank for the university. Contains rank ranges and equal ranks (eg. =94 and 201-250)
# * university_name: name of university
# * country: country of each university
# * teaching: university score for teaching (the learning environment)
# * international: university score international outlook (staff, students, research)
# * research: university score for research (volume, income and reputation)
# * citations: university score for citations (research influence)
# * income: university score for industry income (knowledge transfer)
# * total_score: total score for university, used to determine rank
# * num_students: number of students at the university
# * student_staff_ratio: ratio of students and staffs
# * international_students: ratio of international students
# * female_male_ratio: male and female ratio in universities
# * year: university ranks according to years

# In[ ]:


type(timesData)


# To get general idea from dataset we use "info()" function.

# In[ ]:


timesData.info()


# In[ ]:


timesData.head()


# <a id = "2"></a>
# # 2.Line Charts

# In[ ]:


timesData.head(100)


# I am going to visualize our data using plotly library.

# * mode -> which plot type we are gonna use.
# * name -> title of the plot.
# * marker -> color of the plot.
# * text -> information written on the plot.

# * layout -> title: name of the plot

# I am going to prepare my data frame:

# In[ ]:


first_100 = timesData.iloc[:100]


# In[ ]:


first_100


# In[ ]:


import plotly.graph_objs as go                 #importing graph objects as go 


# In[ ]:


trace1 = go.Scatter(x = first_100.world_rank, y = first_100.citations, mode = "lines", name = "citations", marker = dict(color = "rgba(238, 118, 33,1)"), text = first_100.university_name)


# In[ ]:


trace2 = go.Scatter(x = first_100.world_rank, y = first_100.teaching, mode = "lines+markers", name = "teaching", marker = dict(color = "rgba(139,0,139,0.8)"), text = first_100.university_name)


# In[ ]:


data = [trace1, trace2]


# In[ ]:


layout = dict(title = "Citation and Teaching vs World Rank of Top 100 Universities", xaxis = dict(title = "World Rank", ticklen = 5, zeroline = False))  # title :  label of x axis
                                                                                                                                                         # zeroline : showing zero line or not
                                                                                                                                                         # ticklen : length of x axis ticks           


# In[ ]:


iplot(dict(data = data, layout = layout))


# <a id = "3"></a>
# # 3.Scatter Plot

# I am going to compare citation and world rank of top 100 universities with 2014, 2015 and 2016 years.

# In[ ]:


first_100_2014 = timesData[timesData.year == 2014].iloc[:100]
first_100_2015 = timesData[timesData.year == 2015].iloc[:100]
first_100_2016 = timesData[timesData.year == 2016].iloc[:100]


# In[ ]:


plot1 = go.Scatter(x = first_100_2014.world_rank, y = first_100_2014.citations, mode = "markers", name ="2014", marker = dict(color = "rgba(0, 229, 238, 1)"), text = first_100_2014.university_name)
plot2 = go.Scatter(x = first_100_2015.world_rank, y = first_100_2015.citations, mode = "markers", name = "2015", marker = dict(color = "rgba(238, 58, 140, 1)"), text = first_100_2015.university_name)
plot3 = go.Scatter(x = first_100_2016.world_rank, y = first_100_2016.citations, mode = "markers", name ="2016", marker = dict(color = "rgba(102, 205, 0, 1)"), text = first_100_2016.university_name)


# In[ ]:


data = [plot1, plot2, plot3]


# In[ ]:


layout = dict(title = "Citation vs world rank of top 100 universities with 2014, 2015 and 2016 years", xaxis = dict(title = "World Rank", ticklen = 5, zeroline = False), yaxis = dict(title = "Citations", ticklen = 5, zeroline = False))


# In[ ]:


iplot(dict(data = data, layout = layout))


# <a id = "4"></a>
# # 4.Bar Plot

# I am going to compare citations and teaching of top 3 universities in 2014.

# In[ ]:


top_3_2014 = timesData[timesData.year == 2014].iloc[:3]


# In[ ]:


top_3_2014


# In[ ]:


plot1 = go.Bar(x = top_3_2014.university_name, y = top_3_2014.citations, name ="citations", marker = dict(color = "rgba(0, 229, 238, 1)", line=dict(color='rgb(0,0,0)',width=1.5)), text = top_3_2014.country)
plot2 = go.Bar(x = top_3_2014.university_name, y = top_3_2014.teaching, name = "teaching", marker = dict(color = "rgba(238, 58, 140, 1)", line=dict(color='rgb(0,0,0)',width=1.5)), text = top_3_2014.country)


# In[ ]:


data = [plot1, plot2]


# In[ ]:


layout = dict(title = " Citations And Teaching Of Top 3 Universities In 2014", xaxis = dict(title = "University Names", ticklen = 5, zeroline = False), yaxis = dict(title = "Ratio", ticklen = 5, zeroline = False))


# In[ ]:


iplot(dict(data = data, layout = layout))


# <a id = "5"></a>
# # 5.Pie Chart

# I am going to visualize students rate of top 7 universities in 2016.

# In[ ]:


timesData.head()


# In[ ]:


top_7_universities = timesData[timesData.year == 2016].iloc[:7]


# In[ ]:


top_7_universities


# In[ ]:


top_7_universities.info()


# As you can see "num_students" variable has a type object. We need to do it float64.

# In[ ]:


nums = []
for i in top_7_universities.num_students:
    a = float(i.replace(',','.'))
    nums.append(a)


# In[ ]:


nums


# In[ ]:


plot1 = {"values" : nums, "labels": top_7_universities.university_name, "hole" : 0.3, "type": "pie"}

layout = go.Layout({"title" : "Students Rate Of Top 7 Universities In 2016"})

iplot(dict(data = plot1, layout = layout))


# <a id = "6"></a>
# # 6.Bubble Chart

# I am going to visualize university world rank (first 20) vs teaching score with number of students (size) and international score (color) in 2016.

# In[ ]:


timesData.head()


# In[ ]:


top_20_2016 = timesData[timesData.year == 2016].iloc[:20]


# In[ ]:


nums1 = []
for i in top_20_2016.num_students:
    a = float(i.replace(',','.'))
    nums1.append(a)


# In[ ]:


nums2 = []
for i in top_20_2016.international:
    b = float(i)
    nums2.append(b)


# In[ ]:


nums2


# In[ ]:


plot1 = [{"x" : top_20_2016.world_rank, "y": top_20_2016.teaching, "mode": "markers", "marker": {"color": nums2, "size" : nums1, "showscale": True}}]

layout = go.Layout({"title" : " University World Rank (first 20) vs Teaching Score With Number Of Students (size) And International Score (color) In 2016"})

iplot(dict(data = plot1, layout = layout))


# <a id = "7"></a>
# # 7.Histogram

# I ama going to visualize students-staff ratio in 2011 and 2012 years.

# In[ ]:


student_2011 = timesData[timesData.year == 2011]
student_2012 = timesData[timesData.year == 2012]


# In[ ]:


plot1 = go.Histogram(x = student_2011.student_staff_ratio, name = "2011")
plot2 = go.Histogram(x = student_2012.student_staff_ratio, name = "2012")

layout = go.Layout(title = "students-staff ratio in 2011 and 2012 years", xaxis = dict(title = "Student Staff Ratio"), yaxis = dict(title = "Count"))

iplot(go.Figure(data = [plot1,plot2], layout = layout))


# <a id = "8"></a>
# # 8.Word Cloud

# I am going to visualize countries, which are mentioned most in 2011. 

# In[ ]:


from wordcloud import WordCloud


# In[ ]:


data_2011 = timesData.country[timesData.year == 2011]


# In[ ]:


plt.figure(figsize = (10,10))
word_cloud = WordCloud(background_color = "white", width = 512, height = 384). generate(" ".join(data_2011))
plt.imshow(word_cloud)
plt.axis("off") # for not visualizing x and y axis.

plt.show()


# <a id = "9"></a>
# # 9.Box Plot

# In[ ]:


data_2015_score = timesData.total_score[timesData.year == 2015]
data_2015_research = timesData.research[timesData.year == 2015]


# In[ ]:


import plotly.graph_objs as go 


# In[ ]:


plot1 = go.Box(y = data_2015_score, name = "total score of universities in 2015")
plot2 = go.Box(y = data_2015_research, name = "research of universities in 2015")

iplot(go.Figure(data = [plot1,plot2]))


# <a id = "10"></a>
# # 10.Scatter Matrix Plots

# In[ ]:


import plotly.figure_factory as ff


# In[ ]:


data_for_scatter = timesData[timesData.year == 2015]

data_2015_compare = data_for_scatter.loc[:,["research", "international", "total_score"]]


# In[ ]:


data_2015_compare


# In[ ]:


data_2015_compare["index"] = np.arange(1,len(data_2015_compare)+1)


# In[ ]:


data_2015_compare


# I added an index column

# In[ ]:


iplot(ff.create_scatterplotmatrix(data_2015_compare, diag = "box", index = "index", height=700, width=700))


# <a id = "11"></a>
# # 11.Inset Plot

# Two plots in one frame.

# I am going to compare teaching scores and incomes of the universities in 2015.

# In[ ]:


plot1 = go.Scatter(x = data_for_scatter.world_rank, y = data_for_scatter.teaching, name = "teaching")
plot2 = go.Scatter(x = data_for_scatter.world_rank, y = data_for_scatter.income, xaxis = "x2", yaxis = "y2", name ="income")

layout = go.Layout(title = "Income and Teaching vs World Rank of Universities", xaxis2 = dict(domain=[0.6, 0.95], anchor = 'y2'), yaxis2 = dict( domain=[0.6, 0.95], anchor='x2'))

iplot(go.Figure(data = [plot1, plot2], layout = layout))


# <a id = "12"></a>
# # 12. 3D Scatter Plot wiht Colorscaling

# In[ ]:


plot1 = go.Scatter3d(x = data_for_scatter.world_rank, y = data_for_scatter.research, z = data_for_scatter.citations, mode = "markers")

layout = go.Layout(title = "World Rank vs Research vs Citations") 

iplot(go.Figure(data = plot1, layout = layout))


# <a id = "13"></a>
# # 13.Multiple Subplots

# In[ ]:


trace1 = go.Scatter(x = data_for_scatter.world_rank, y = data_for_scatter.research, name = "research")
trace2 = go.Scatter(x = data_for_scatter.world_rank, y = data_for_scatter.citations, xaxis = "x2", yaxis = "y2", name = "citations")
trace3 = go.Scatter(x = data_for_scatter.world_rank, y = data_for_scatter.income, xaxis = "x3", yaxis = "y3", name = "income")
trace4 = go.Scatter(x = data_for_scatter.world_rank, y=data_for_scatter.total_score, xaxis = "x4", yaxis = "y4", name = "total_score")
data = [trace1, trace2, trace3, trace4]
layout = go.Layout(xaxis = dict(domain = [0, 0.45]), yaxis = dict(domain = [0, 0.45]), xaxis2 = dict(domain = [0.55, 1]), xaxis3 = dict(domain = [0, 0.45], anchor = "y3"), xaxis4 = dict(domain = [0.55, 1], anchor = "y4" ), yaxis2 = dict(domain = [0, 0.45], anchor = "x2"), yaxis3 = dict(domain=[0.55, 1]), yaxis4 = dict(domain = [0.55, 1], anchor = "x4"), 
title = "Research, citation, income and total score VS World Rank of Universities")
fig = go.Figure(data=data, layout=layout)
iplot(fig)

