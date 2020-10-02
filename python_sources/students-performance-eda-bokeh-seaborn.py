#!/usr/bin/env python
# coding: utf-8

# **Students performance - visualisation with Bokeh**
# 
# In this kernel we are goinf to perform exploratory data analysis using bokeh library for visualisation. Bokeh is an interactive visualisation library which can be used wth various programming languages. Here we will use Python.
# 
# First let's load standard library to create database from .csv file - Pandas - and a visualisation library seaborn.
# Later in this kernel I will import appropraite components from bokeh library to create interactive plots.

# In[ ]:


import pandas as pd
import seaborn as sns
import matplotlib as plt


# Creating a pandas dataframe from .csv file..

# In[ ]:


data = pd.read_csv("../input/StudentsPerformance.csv")


# Looking at the first few rows for the visual inspection.

# In[ ]:


data.head()


# Everything seems fine so no it's time to check a shape and bersic statistics of the database.

# In[ ]:


data.shape


# In[ ]:


data.describe()


# Let's see what are the levels of parental education.

# In[ ]:


data["parental level of education"].unique().tolist()


# Lunch types

# In[ ]:


data["lunch"].unique().tolist()


# Test preparation course

# In[ ]:


data["test preparation course"].unique().tolist()


# There are couple of categorical variables that divide our students in many subgroups. Let's look at the boxplots to see how the variation looks between them before plotting the stratified scatterplots.

# In[ ]:


ax1 = sns.catplot(x="parental level of education", y="math score", hue="gender",data=data, palette="deep", col="test preparation course", kind="box",height=5, aspect=1)
ax1.fig.subplots_adjust(top=0.9)
ax1.fig.suptitle('MATH', fontsize=16)
ax1.set_xticklabels(rotation=90)

ax2 = sns.catplot(x="parental level of education", y="reading score", hue="gender",data=data, palette="deep", col="test preparation course", kind="box",height=5, aspect=1)
ax2.set_xticklabels(rotation=90)
ax2.fig.subplots_adjust(top=0.9)
ax2.fig.suptitle('READING', fontsize=16)

ax3 = sns.catplot(x="parental level of education", y="writing score", hue="gender",data=data, palette="deep", col="test preparation course", kind="box",height=5, aspect=1)
ax3.set_xticklabels(rotation=90)
ax3.fig.subplots_adjust(top=0.9)
ax3.fig.suptitle('WRITING', fontsize=16)


# **Creating visualisations with Bokeh**
# 
# I will hide the input code for clarity and aesthetics of kernel because sometimes in Bokeh there is a relatively big chunk of python code.
# 
# Scatter plot of the exam results description:
# * Color will indicate gender.
# * Hovering over the point will revela parental education level and lunch type.

# In[ ]:


# bokeh packages
from bokeh.io import output_file, show, output_notebook, push_notebook
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,CategoricalColorMapper
from bokeh.layouts import row, column
output_notebook()

import warnings
warnings.filterwarnings("ignore")


# In[ ]:


#creating data source for thescatter plot
source = ColumnDataSource(data={
    "gender": data.loc[:,"gender"],
    "math" : data.loc[:,"math score"],
    "lunch" : data.loc[:,"lunch"],
    "parents" : data.loc[:,"parental level of education"],
    "reading" : data.loc[:,"reading score"],
    "writing" : data.loc[:,"writing score"]
})

factors = list(data.gender.unique())
colors = ["red","green"]

mapper = CategoricalColorMapper(factors = factors,palette = colors)
hover = HoverTool(tooltips = [("Parents education","@parents"),("Lunch","@lunch")])

p1 = figure(x_axis_label="math score", y_axis_label="reading score", tools=[hover,"crosshair","pan","box_zoom"])
p1.circle("math", "reading", source=source, color = {"field":"gender","transform":mapper},hover_color ="red")

p2 = figure(x_axis_label="writing score", y_axis_label="reading score", tools=[hover,"crosshair","pan","box_zoom"])
p2.circle("writing", "reading", source=source, color = {"field":"gender","transform":mapper},hover_color ="red")

layout = column(p1, p2)
show(layout,notebook_handle=True)


# Parental education level pie chart

# In[ ]:


# creating data for the graph
x = {
    "bachelor's degree": sum(data["parental level of education"]=="bachelor's degree"),
    "some college": sum(data["parental level of education"]=="some college"),
    "master's degree": sum(data["parental level of education"]=="master's degree"),
    "associate's degree": sum(data["parental level of education"]=="associate's degree"),
    "high school": sum(data["parental level of education"]=="high school"),
    "some high school": sum(data["parental level of education"]=="high school")
}
print(x)


# In[ ]:


from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum

data1 = pd.Series(x).reset_index(name='value').rename(columns={'index':'education'})
data1['angle'] = data1['value']/data1['value'].sum() * 2*pi
data1['color'] = Category20c[len(x)]

p = figure(plot_height=350, title="Parental level of education", toolbar_location=None,
           tools="hover", tooltips="@education: @value", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='education', source=data1)

p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None
show(p)

