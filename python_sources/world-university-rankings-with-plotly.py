#!/usr/bin/env python
# coding: utf-8

# # INTRODUCTION
# 

# * In this notebook is to learn plotly library. Thank DATAI for guiding.

# Content:
# 
# 1.[Loading Data and Explanation of Features](#1)
# 
# 2.[Line Charts](#2)
# 
# 3.[Scatter Charts](#3)
# 
# 4.[Bar Charts](#4)
# 
# 5.[Pie Charts](#5)
# 
# 6.[Bubble Charts](#6)
# 
# 7.[Histogram](#7)
# 
# 8 [Word Cloud](#8)
# 
# 9.[Box Plots](#9)
# 
# 10.[Scatterplot Matrix](#10)
# 
# 11.[Inset Plots](#11)
# 
# 12.[3D Scatter Plot with Colorscaling](#12)
# 
# 13.[Multiple Subplots](#13)

# In[ ]:


#pip install plotly==3.10.0


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

#numpy
import numpy as np # linear algebra

#pandas
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# plotly
# import plotly.plotly as py
from plotly.offline import init_notebook_mode, iplot, plot
import plotly as py
init_notebook_mode(connected=True)
import plotly.graph_objs as go


#import chart_studio.plotly as py
#from plotly.offline import init_notebook_mode, iplot
#init_notebook_mode(connected=True)



#worldcloud library
from wordcloud import WordCloud

#matplotlib
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


timesData=pd.read_csv("/kaggle/input/world-university-rankings/timesData.csv")


# <a id="1"></a>
# 
# ## 1.Loading Data and Explanation of Features
# 
# TimesData includes 14 features. If you want to find features, you can use below code:
#  
# 

# In[ ]:


timesData.columns.unique()


# In[ ]:


timesData.info()


# In[ ]:


timesData.head()


# <a id="2"></a>
# 
# ## 2. Line Charts

# In[ ]:



#reminding for iloc

# Single selections using iloc and DataFrame
# Rows:
    #data.iloc[0] # first row of data frame (value1) 
    #data.iloc[1] # second row of data frame (value2)
    #data.iloc[-1] # last row of data frame (value3)
# Columns:
    #data.iloc[:,0] # first column of data frame (first_name)
    #data.iloc[:,1] # second column of data frame (last_name)
    #data.iloc[:,-1] # last column of data frame (id)



# Multiple row and column selections using iloc and DataFrame
    #data.iloc[0:5] # first five rows of dataframe
    #data.iloc[:, 0:2] # first two columns of data frame with all rows
    #data.iloc[[0,3,6,24], [0,5,6]] # 1st, 4th, 7th, 25th row + 1st 6th 7th columns
    #data.iloc[0:5, 5:8] # first 5 rows and 5th, 6th, 7th columns of data frame


# In[ ]:


df=timesData.iloc[:100,:]

import plotly.graph_objs as go

trace1=go.Scatter(
                x=df.world_rank,
                y=df.citations,
                mode="lines",
                name="citations",
                marker=dict(color='rgba(16,112,2,0.8)'),
                text=df.university_name)

trace2=go.Scatter(
                x=df.world_rank,
                y=df.citations,
                mode="lines+markers",
                name="teaching",
                marker=dict(color='rgba(80,26,80,0.8)'),
                text=df.university_name)
    
data=[trace1,trace2]

layout=dict(title='Citation and Teaching vs World Rank of Top 100 Universities',
            xaxis=dict(title='World Rank', ticklen=5, zeroline=False))

fig=dict(data=data, layout=layout)
iplot(fig)


# <a id="3"></a>
# 
# ## Scatter Charts

# In[ ]:


timesData.head(15)


# In[ ]:


#data frames

df2014=timesData[timesData.year==2014].iloc[:100,:]
df2015=timesData[timesData.year==2015].iloc[:100,:]
df2016=timesData[timesData.year==2016].iloc[:100,:]

#for graph
import plotly.graph_objs as go

#
trace1=go.Scatter(
                x=df2014.world_rank,
                y=df2014.citations,
                mode="markers", #->type of plot like marker, line or line + markers
                name="2014",
                marker=dict(color='rgba(255,128,255,0.8)'), #-> marker is used with dictionary
                text=df2014.university_name
                )
trace2=go.Scatter(
                x=df2015.world_rank,
                y=df2015.citations,
                mode="markers", #->type of plot like marker, line or line + markers
                name="2015",
                marker=dict(color='rgba(255,128,2,0.8)'),#-> marker is used with dictionary
                text=df2015.university_name
                )
trace3=go.Scatter(
                x=df2016.world_rank,
                y=df2016.citations,
                mode="markers", #->type of plot like marker, line or line + markers
                name="2016",
                marker=dict(color='rgba(0,128,200,0.8)'), #-> marker is used with dictionary
                text=df2016.university_name
                )

data=[trace1,trace2,trace3]

layout=dict(title='Citation vs world rank of top 100 universities with 2014, 2015 and 2016 years',
            xaxis=dict(title="World Rank", ticklen=5, zeroline=False), # dictionary
            yaxis=dict(title="Citation", ticklen=5, zeroline=False)  # dictionary
           )

fig=dict(data=data, layout=layout) #-> data and layout

iplot(fig) #-> for plots, fig is created by data and layout and iplot shows fig


# <a id="4"></a>
# 
# ## Bar Charts
# 
# First Bar Charts Example: citations and teaching of top 3 universities in 2014 (style1)

# In[ ]:


#data frames

df2014= timesData[timesData.year==2014].iloc[:3,:]
df2014


# In[ ]:


#data frames
df2014=timesData[timesData.year==2014].iloc[:3,:]

#for graph
import plotly.graph_objs as go

#create trace1 
trace1=go.Bar(
           x=df2014.university_name,
           y=df2014.citations,
           name="citations",
           marker=dict(color='rgba(255,174,255,0.5)',
           line=dict(color='rgba(0,0,0)', width=1.5)),
           text=df2014.country)

trace2=go.Bar(
           x=df2014.university_name,
           y=df2014.citations,
           name="teaching",
           marker=dict(color='rgba(32,174,128,0.5)',
           line=dict(color='rgba(0,0,0)', width=1.5)),
           text=df2014.country)

data=[trace1,trace2]
layout=go.Layout(barmode="group")
fig=go.Figure(data=data,layout=layout)
iplot(fig)


# Second Bar Charts Example: citations and teaching of top 3 universities in 2014 (style2)

# In[ ]:


#data frames
df2014=timesData[timesData.year==2014].iloc[:3,:]


#for graph
import plotly.graph_objs as go

x=df2014.university_name

trace1={
    'x':x,
    'y':df2014.citations,
    'name':'citation',
    'type':'bar'
};

trace2={
    'x':x,
    'y':df2014.teaching,
    'name':'teaching',
    'type':'bar'
};
data=[trace1,trace2]


layout={
    'xaxis':{'title':'Top 3 Universities'},
    'barmode':'relative',
    'title':'citations and teaching of top 3 universities in 2014'
};

fig=go.Figure(data=data, layout=layout)
iplot(fig)





# Third Bar Charts Example: Horizontal bar charts. (style3) 
# Citation vs income for universities

# In[ ]:


# import graph objects as "go" and import tools
import plotly.graph_objs as go
from plotly import tools
import matplotlib.pyplot as plt
# prepare data frames
df2016 = timesData[timesData.year == 2016].iloc[:7,:]

y_saving = [each for each in df2016.research]
y_net_worth  = [float(each) for each in df2016.income]
x_saving = [each for each in df2016.university_name]
x_net_worth  = [each for each in df2016.university_name]

trace0 = go.Bar(
                x=y_saving,
                y=x_saving,
                marker=dict(color='rgba(171, 50, 96, 0.6)',line=dict(color='rgba(171, 50, 96, 1.0)',width=1)),
                name='research',
                orientation='h',
)
trace1 = go.Scatter(
                x=y_net_worth,
                y=x_net_worth,
                mode='lines+markers',
                line=dict(color='rgb(63, 72, 204)'),
                name='income',
)
layout = dict(
                title='Citations and income',
                yaxis=dict(showticklabels=True,domain=[0, 0.85]),
                yaxis2=dict(showline=True,showticklabels=False,linecolor='rgba(102, 102, 102, 0.8)',linewidth=2,domain=[0, 0.85]),
                xaxis=dict(zeroline=False,showline=False,showticklabels=True,showgrid=True,domain=[0, 0.42]),
                xaxis2=dict(zeroline=False,showline=False,showticklabels=True,showgrid=True,domain=[0.47, 1],side='top',dtick=25),
                legend=dict(x=0.029,y=1.038,font=dict(size=10) ),
                margin=dict(l=200, r=20,t=70,b=70),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
)
annotations = []
y_s = np.round(y_saving, decimals=2)
y_nw = np.rint(y_net_worth)
# Adding labels
for ydn, yd, xd in zip(y_nw, y_s, x_saving):
    # labeling the scatter savings
    annotations.append(dict(xref='x2', yref='y2', y=xd, x=ydn - 4,text='{:,}'.format(ydn),font=dict(family='Arial', size=12,color='rgb(63, 72, 204)'),showarrow=False))
    # labeling the bar net worth
    annotations.append(dict(xref='x1', yref='y1', y=xd, x=yd + 3,text=str(yd),font=dict(family='Arial', size=12,color='rgb(171, 50, 96)'),showarrow=False))

layout['annotations'] = annotations

# Creating two subplots
fig = tools.make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                          shared_yaxes=False, vertical_spacing=0.001)

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)

fig['layout'].update(layout)
iplot(fig)


# <a id="5"></a>
# 
# ## Pie Charts

# In[ ]:


df2016.columns.unique()


# In[ ]:


df2016.head()


# In[ ]:


df2016=timesData[timesData.year==2016].iloc[:7,:]

pie1=df2016.num_students

pie1_list=[float(each.replace(',','.')) for each in df2016.num_students]

labels=df2016.university_name
fig={
    "data":[
        {
            "values":pie1_list,
            "labels":labels,
            "domain":{"x":[0,.5]},
            "name":"Number Of Students Rates",
            "hoverinfo":"label+percent+name",
            "hole":.3,
            "type":"pie"
         },],
     "layout": {
        "title":"Universities Number of Students rates",
        "annotations": [
            { "font": { "size": 20},
              "showarrow": False,
              "text": "Number of Students",
                "x": 0.20,
                "y": 1
            },
        ]
    }
}
iplot(fig)


# <a id="6"></a>
# 
# ## Bubble Charts
# 
# University world rank (first 20) vs teaching score with number of students(size) and international score (color) in 2016

# In[ ]:


df2016.head(10)


# In[ ]:


df2016.info()


# In[ ]:


df2016=timesData[timesData.year==2016].iloc[:20,:]

num_students_size=[float(each.replace(',','.')) for each in df2016.num_students]

international_color=[float(each) for each in df2016.international]

data=[
    {
        'y':df2016.teaching,
        'x':df2016.world_rank,
        'mode':'markers',
        'marker':{
            'color':international_color,
            'size':num_students_size,
            'showscale':True
        },
        "text":df2016.university_name
    }
]
iplot(data)


# <a id='7'></a>
# 
# ## Histogram
# 
# Lets look at histogram of students-staff ratio in 2011 and 2012 years.

# In[ ]:


timesData.head()


# In[ ]:


x2011=timesData.student_staff_ratio[timesData.year==2011]
x2012=timesData.student_staff_ratio[timesData.year==2012]

trace1=go.Histogram(
    x=x2011,
    opacity=0.75,
    name="2011",
    marker=dict(color='rgba(171,50,60,0.6)'))

trace2=go.Histogram(
x=x2012,
    opacity=0.75,
    name="2012",
    marker=dict(color='rgba(90,63,12,10)'))

data=[trace1,trace2]

layout=go.Layout(barmode='overlay',
                title=' students-staff ratio in 2011 and 2012',
                   xaxis=dict(title='students-staff ratio'),
                   yaxis=dict( title='Count'),
)
fig = go.Figure(data=data, layout=layout)
iplot(fig)


# <a id='8'></a>
# 
# ## Word Cloud
# 
# It is not a py plot but learning is good for visulation.
# 
# Word cloud library that I imported at the beginning of kernel

# In[ ]:


x2011=timesData.country[timesData.year==2011]
plt.subplots(figsize=(8,8))
wordcloud= WordCloud(
                    background_color='white',
                    width=512,
                    height=384).generate("".join(x2011))

plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('graph.png')
    
plt.show()


# In[ ]:


#while studying you can check your data frames. So you can see output and you learn easily
#x2011


# <a id="9"></a>
# 
# ## Box Plots

# In[ ]:


x2015=timesData[timesData.year==2015]

trace0=go.Box(
              y=x2015.total_score,
              name='total score of universities in 2015',
              marker = dict(
              color='rgb(12,128,129)',
        
    )
)

trace1=go.Box(
             y=x2015.research,
             name='research of universities in 2015',
             marker=dict(
             color='rgb(12,128,128)',
    )
)

data=[trace0,trace1]
iplot(data)


# <a id="10"></a>
# 
# ## Scatterplot Matrix

# In[ ]:


# import figure factory
import plotly.figure_factory as ff
# prepare data
dataframe = timesData[timesData.year == 2015]
data2015 = dataframe.loc[:,["research","international", "total_score"]]
data2015["index"] = np.arange(1,len(data2015)+1)
# scatter matrix
fig = ff.create_scatterplotmatrix(data2015, diag='box', index='index',colormap='Portland',
                                  colormap_type='cat',
                                  height=700, width=700)
iplot(fig)


# In[ ]:


#data2015


# <a id="11"></a>
# 
#  ## Inset Plots

# In[ ]:


# first line plot
trace1 = go.Scatter(
    x=dataframe.world_rank,
    y=dataframe.teaching,
    name = "teaching",
    marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
)
# second line plot
trace2 = go.Scatter(
    x=dataframe.world_rank,
    y=dataframe.income,
    xaxis='x2',
    yaxis='y2',
    name = "income",
    marker = dict(color = 'rgba(160, 112, 20, 0.8)'),
)
data = [trace1, trace2]
layout = go.Layout(
    xaxis2=dict(
        domain=[0.6, 0.95],
        anchor='y2',        
    ),
    yaxis2=dict(
        domain=[0.6, 0.95],
        anchor='x2',
    ),
    title = 'Income and Teaching vs World Rank of Universities'

)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# <a id="12"></a>
# 
# ## 3D Scatter Plot with Colorscaling

# In[ ]:


# create trace 1 that is 3d scatter
trace1 = go.Scatter3d(
    x=dataframe.world_rank,
    y=dataframe.research,
    z=dataframe.citations,
    mode='markers',
    marker=dict(
        size=10,
        color='rgb(0,0,0)',                # set color to an array/list of desired values      
    )
)

data = [trace1]
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0  
    )
    
)
fig = go.Figure(data=data, layout=layout)
iplot(fig)


# <a id="13"></a>
# 
# ## Multiple Subplots

# In[ ]:


trace1 = go.Scatter(
    x=dataframe.world_rank,
    y=dataframe.research,
    name = "research"
)
trace2 = go.Scatter(
    x=dataframe.world_rank,
    y=dataframe.citations,
    xaxis='x2',
    yaxis='y2',
    name = "citations"
)
trace3 = go.Scatter(
    x=dataframe.world_rank,
    y=dataframe.income,
    xaxis='x3',
    yaxis='y3',
    name = "income"
)
trace4 = go.Scatter(
    x=dataframe.world_rank,
    y=dataframe.total_score,
    xaxis='x4',
    yaxis='y4',
    name = "total_score"
)
data = [trace1, trace2, trace3, trace4]
layout = go.Layout(
    xaxis=dict(
        domain=[0, 0.45]
    ),
    yaxis=dict(
        domain=[0, 0.45]
    ),
    xaxis2=dict(
        domain=[0.55, 1]
    ),
    xaxis3=dict(
        domain=[0, 0.45],
        anchor='y3'
    ),
    xaxis4=dict(
        domain=[0.55, 1],
        anchor='y4'
    ),
    yaxis2=dict(
        domain=[0, 0.45],
        anchor='x2'
    ),
    yaxis3=dict(
        domain=[0.55, 1]
    ),
    yaxis4=dict(
        domain=[0.55, 1],
        anchor='x4'
    ),
    title = 'Research, citation, income and total score VS World Rank of Universities'
)
fig = go.Figure(data=data, layout=layout)
iplot(fig)


# Conclusion
# 
# Thanks for you upvotes
