#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install plotly --upgrade')
get_ipython().system(' pip install chart_studio')
#import plotly
#plotly.__version__


# In[ ]:


import plotly
plotly.__version__


# In[ ]:


import chart_studio.plotly as py
from chart_studio.grid_objs import Grid, Column
import plotly.figure_factory as ff
import plotly.graph_objects as go

import pandas as pd
import time


# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
     
    for filename in filenames:
        
        print(os.path.join(dirname, filename))


# In[ ]:


df = pd.read_excel('/kaggle/input/world-development-indicators-world-bank/health Indicators WDI.xlsx')
df.head()


# In[ ]:


df.tail()


# In[ ]:


df.shape


# #### check the null values

# In[ ]:


df.isnull().sum()


# #### Drop the null values

# In[ ]:


df.dropna(inplace=True)


# In[ ]:


df.isnull().sum()


# In[ ]:


df.notnull().sum()


# #### Check the unique values of countries

# In[ ]:


cn = df['Country Name'].unique()
cn


# In[ ]:


df['Country Name'].value_counts()


# In[ ]:


df['Country Name'].count()


# In[ ]:


con = df['Continent'].unique()
con


# In[ ]:


year = df['Year'].value_counts()
year


# In[ ]:


df['Year'].unique()


# In[ ]:


temp = pd.crosstab([df['Year'],df["Population"]], df['Continent'])
temp


# In[ ]:


df.head(2)


# In[ ]:


import plotly.express as px


# In[ ]:


px.scatter(df, x="GDP per capita", y="Current health expenditure per capita",
           animation_frame="Year", animation_group="Country Name",
           size="Population", color="Continent", hover_name="Country Name",
           log_x=True, size_max=65, range_x=[100,100000], range_y=[25,90])


# In[ ]:


fig = px.bar(df, x="Continent", y="Population", color="Continent",
  animation_frame="Year", animation_group="Country Name", range_y=[0,4000000000])
fig.show()


# In[ ]:


df.rename(columns = {'Life expectancy at birth, total (years) ': 'Life Expectancy', 
                    'Government expenditure on education, total':'Exp on Edu',
                     'Domestic private health expenditure per capita' :'Private health exp',
                     'Domestic general government health expenditure per capita' :'gov health exp'
                    }, inplace = True)  


# In[ ]:


df.columns


# In[ ]:


df.head(2)


# In[ ]:


years =['1999', '2000', '2010', '2018']


# In[ ]:


# make list of continents
continents = []
for continent in df["Continent"]:
    if continent not in continents:
        continents.append(continent)
# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}


# In[ ]:


# fill in most of layout
fig_dict["layout"]["xaxis"] = {"range": [30, 85], "title": "Life Expectancy"}
fig_dict["layout"]["yaxis"] = {"title": "GDP per capita", "type": "log"}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["sliders"] = {
    "args": [
        "transition", {
            "duration": 400,
            "easing": "cubic-in-out"
        }
    ],
    "initialValue": "1999",
    "plotlycommand": "animate",
    "values": years,
    "visible": True
}
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}


# In[ ]:


df.columns


# In[ ]:


# make data
year = 1999
for continent in continents:
    dataset_by_year = df[df["Year"] == year]
    dataset_by_year_and_cont = dataset_by_year[
        df["Continent"] == continent]

    data_dict = {
        "x": list(dataset_by_year_and_cont["Life Expectancy"]),
        "y": list(dataset_by_year_and_cont["GDP per capita"]),
        "mode": "markers",
        "text": list(dataset_by_year_and_cont["Country Name"]),
        "marker": {
            "sizemode": "area",
            "sizeref": 200000,
            "size": list(dataset_by_year_and_cont["Population"])
        },
        "name": continent
    }
    fig_dict["data"].append(data_dict)

# make frames
for year in years:
    frame = {"data": [], "name": str(year)}
    for continent in continents:
        dataset_by_year = df[df["Year"] == int(year)]
        dataset_by_year_and_cont = dataset_by_year[
            dataset_by_year["Continent"] == continent]

        data_dict = {
            "x": list(dataset_by_year_and_cont["Life Expectancy"]),
            "y": list(dataset_by_year_and_cont["GDP per capita"]),
            "mode": "markers",
            "text": list(dataset_by_year_and_cont["Country Name"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 200000,
                "size": list(dataset_by_year_and_cont["Population"])
            },
            "name": continent
        }
        frame["data"].append(data_dict)

    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 10000}}
    ],
        "label": year,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)


fig_dict["layout"]["sliders"] = [sliders_dict]

fig = go.Figure(fig_dict)

fig.show()


# In[ ]:



fig = px.choropleth(df, locations="Code",
                    color="Life Expectancy", 
                    hover_name="Country Name", animation_frame=df["Year"],
                    color_continuous_scale=px.colors.sequential.Plasma)
fig.update_layout(transition = {'duration': 1000})
fig.show()


# In[ ]:



fig = px.choropleth(df, locations='Code',
                    color= 'Population',
                    hover_name='Country Name', labels={'GDP per capita':'GDP per capita'},
                    animation_frame=df["Year"],
                    color_continuous_scale=px.colors.sequential.Agsunset)
fig.update_layout(transition = {'duration': 10000})
fig.show()


# In[ ]:


df.head(2)


# In[ ]:


fig = px.choropleth(df, locations='Code',
                    color= 'GDP per capita',
                    hover_data=['Country Name','Continent','Exp on Edu'],
                    animation_frame=df["Year"],
                    color_continuous_scale=px.colors.sequential.thermal)
fig.update_layout(transition = {'duration': 10000})
fig.show()


# In[ ]:




