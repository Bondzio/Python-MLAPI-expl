#!/usr/bin/env python
# coding: utf-8

# Import/Clean Data
# -----------------

# In[ ]:


import numpy as np
import pandas as pd

import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode()

police_data = pd.read_csv('../input/clean_data.csv', usecols=[0, 4, 5, 6, 7, 9])
police_data = police_data.rename(
    columns={'person':'name', 'cause_short':'cause'})
police_data['date'] = pd.to_datetime(police_data['date'])
police_data['state'] = police_data['state'].str.strip()
police_data['cause'] = police_data['cause'].str.title()
# assignment of federal police officers to District of Columbia
police_data['state'] = police_data['state'].str.replace('US', 'DC')
# exclusion of police dogs from data
police_data = police_data[police_data['canine'] == False]
police_data = police_data[['date', 'year', 'name', 'state', 'cause']]

us_states = np.asarray(['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',                     'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI',                     'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY',                     'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT',                     'WA', 'WI', 'WV', 'WY'])

# police officer deaths in US states only, territories excluded (21,809 rows)
police_datausa = police_data[police_data['state'].isin(us_states)]


# Police Deaths by Year
# ---------------------

# In[ ]:


# police officer deaths per year
police_peryear = np.asarray(police_datausa.groupby('year').year.count())
# police deaths in 2016 estimated, data published in July 2016
police_peryear[-1] = police_peryear[-1] * 2

police_years = np.asarray(police_datausa.year.unique())

trace = [go.Scatter(
    x = police_years,
    y = police_peryear,
    mode = 'lines',
    connectgaps = True,
    name = 'Police Officers',
    line = dict(
        color = ('rgb(1, 97, 156)'),
        width = 3
        ) )]

layout = go.Layout(
    title = 'Police Officer Deaths by Year in United States (1791-2016)',
    xaxis = dict(
        showline = True,
        showgrid = False,
        autotick = True,
        showticklabels = True
    ),
    yaxis = dict(
        range = [0, 315],
        showgrid = False,
        zeroline = False,
        showline = False,
        showticklabels = False
    ) )

figure = dict(data=trace, layout=layout)
iplot(figure)


# Police Deaths by Cause
# -------------------------------

# In[ ]:


# categories of police officer death causes
cause_vehcol = ['Automobile Accident', 'Motorcycle Accident', 'Vehicle Pursuit',
                'Aircraft Accident', 'Train Accident', 'Bicycle Accident',
                'Boating Accident']
cause_vehasl = ['Vehicular Assault', 'Struck By Vehicle', 'Struck By Streetcar',
                'Struck By Train']
cause_medical = ['Heart Attack', 'Duty Related Illness', 'Heat Exhaustion']
cause_accident = ['Accidental', 'Gunfire (Accidental)', 'Training Accident', 'Fall',
                 'Structure Collapse']
cause_terror = ['Terrorist Attack', '9/11 Related Illness', 'Explosion', 'Bomb']

cause_categories = []

for death in police_datausa['cause'].values:
    if death == 'Gunfire':
        cause_categories.append('Firearm')
    elif death in cause_vehcol:
        cause_categories.append('Vehicle (Collision)')
    elif death in cause_vehasl:
        cause_categories.append('Vehicle (Assault)')
    elif death in cause_medical:
        cause_categories.append('Medical Condition')
    elif death in cause_accident:
        cause_categories.append('Accident')
    elif death == 'Assault':
        cause_categories.append('Assault')
    elif death == 'Stabbed':
        cause_categories.append('Knife')
    elif death == 'Drowned':
        cause_categories.append('Water')
    elif death in cause_terror:
        cause_categories.append('Terrorism')
    elif death == 'Electrocuted':
        cause_categories.append('Electricity')
    elif death == 'Animal Related':
        cause_categories.append('Animal')
    elif death == 'Fire':
        cause_categories.append('Fire')
    elif death in ['Weather/Natural Disaster', 'Exposure']:
        cause_categories.append('Weather')
    elif death in ['Exposure to Toxins', 'Poisoned']:
        cause_categories.append('Poison')
    else:
        cause_categories.append('Unknown')

pd.options.mode.chained_assignment = None
police_datausa['category'] = cause_categories

# police officer deaths by cause
police_percause = np.asarray(police_datausa.groupby('category').category.count())
police_percause.sort()
police_percause = np.delete(police_percause, [0])

police_causes = ['Poison', 'Weather', 'Fire', 'Animal', 'Electricity', 'Terrorism',
                 'Water', 'Knife', 'Assault', 'Accident', 'Medical Condition',
                 'Vehicle (Assault)', 'Vehicle (Collision)', 'Firearm']

trace = [go.Bar(
            x = police_percause,
            y = police_causes,
            orientation = 'h',
            marker = dict(
                color = 'rgb(1, 97, 156)')
)]

layout = go.Layout(
    title = 'Police Officer Deaths by Cause in United States (1791-2016)',
    xaxis = dict(
        showgrid = False,
        autotick = True,
        showticklabels = False
    ),
    autosize = False,
    margin = dict(
        autoexpand = False,
        l = 125,
        r = 40,
        b = 80,
        pad = 5
    ),
    annotations = [
        dict(x = x, y = y,
             text = str(x),
             xanchor = 'left',
             yanchor = 'middle',
             showarrow = False
        ) for x, y in zip(police_percause, police_causes)]
)

figure = dict(data=trace, layout=layout)
iplot(figure)


# Police Deaths by Cause (Past 50 Years)
# ------------------------------------------

# In[ ]:


# police officer deaths by cause per year
police_total = police_peryear[150:]
police_gun = np.asarray(police_datausa[(police_datausa.year > 1964) & (
    police_datausa.category == 'Firearm')].groupby('year').year.count())
police_vehcol = np.asarray(police_datausa[(police_datausa.year > 1964) & (
    police_datausa.category == 'Vehicle (Collision)')].groupby('year').year.count())
police_vehasl = np.asarray(police_datausa[(police_datausa.year > 1964) & (
    police_datausa.category == 'Vehicle (Assault)')].groupby('year').year.count())

police_gun = np.round(np.divide(police_gun, police_total) * 100, 1)
police_gun = np.delete(police_gun, [51])
police_vehcol = np.round(np.divide(police_vehcol, police_total) * 100, 1)
police_vehcol = np.delete(police_vehcol, [51])
police_vehasl = np.round(np.divide(police_vehasl, police_total) * 100, 1)
police_vehasl = np.delete(police_vehasl, [51])

labels = ['Firearm', 'Vehicle (Collision)', 'Vehicle (Assault)']
colors = ['rgb(1, 97, 156)', 'rgb(192, 35, 36)', 'rgb(97, 156, 1)']

x_data = police_years[150:201]
y_data = np.asarray([police_gun, police_vehcol, police_vehasl])

traces = []

for i in range(0, 3):
    traces.append(go.Scatter(
        x = x_data,
        y = y_data[i],
        mode = 'lines',
        name = labels[i],
        line = dict(color = colors[i], width = 3),
        connectgaps = True
    ))
    traces.append(go.Scatter(
        x = [x_data[0], x_data[50]],
        y = [y_data[i][0], y_data[i][50]],
        mode = 'markers',
        name = labels[i],
        marker = dict(color = colors[i], size = 7)
    ))

layout = go.Layout(
    title = 'Police Deaths by Cause in United States (1965-2015)',
    showlegend = False,
    xaxis = dict(
        showline = True,
        showgrid = False,
        autotick = True,
        showticklabels = True
    ),
    yaxis = dict(
        showgrid = False,
        zeroline = False,
        showline = False,
        showticklabels = False
    ),
    margin = dict(
        autoexpand = False,
        l = 125,
        r = 40,
        b = 80
    ))

annotations = []

for y_trace, label in zip(y_data, labels):
    annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                  xanchor='right', yanchor='middle',
                                  text=label + ' {}%'.format(y_trace[0]),
                                  showarrow=False))
    annotations.append(dict(xref='paper', x=0.95, y=y_trace[50],
                                  xanchor='left', yanchor='middle',
                                  text='{}%'.format(y_trace[50]),
                                  showarrow=False))

layout['annotations'] = annotations

figure = dict(data=traces, layout=layout)
iplot(figure)


# Police Deaths by State
# ----------------------

# In[ ]:


# police officer deaths per state
police_perstate = np.asarray(police_datausa.groupby('state').state.count())

police_scale = [[0, 'rgb(229, 239, 245)'],[1, 'rgb(1, 97, 156)']]

data = [ dict(
        type = 'choropleth',
        colorscale = police_scale,
        autocolorscale = False,
        showscale = False,
        locations = us_states,
        z = police_perstate,
        locationmode = 'USA-states',
        marker = dict(
            line = dict(
                color = 'rgb(255, 255, 255)',
                width = 2
            ) ),
        ) ]

layout = dict(
        title = 'Police Officer Deaths by State in United States (1791-2016)',
        geo = dict(
            scope = 'usa',
            projection = dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)',
            countrycolor = 'rgb(255, 255, 255)')
             )

figure = dict(data=data, layout=layout)
iplot(figure)


# Police Deaths per Capita
# ------------------------

# In[ ]:


# state population estimates for July 2015 from US Census Bureau
# www.census.gov/popest/data/state/totals/2015/tables/NST-EST2015-01.csv
state_population = np.asarray([738432, 4858979, 2978204, 6828065, 39144818, 5456574,                               3590886, 672228, 945934, 20271272, 10214860, 1431603,                               3123899, 1654930, 12859995, 6619680, 2911641, 4425092,                               4670724, 6794422, 6006401, 1329328, 9922576, 5489594,                               6083672, 2992333, 1032949, 10042802, 756927, 1896190,                               1330608, 8958013, 2085109, 2890845, 19795791, 11613423,                               3911338, 4028977, 12802503, 1056298, 4896146, 858469,                               6600299, 27469114, 2995919, 8382993, 626042, 7170351,                               5771337, 1844128, 586107])

# police officer deaths per 100,000 people in state
police_percapita = police_perstate / state_population * 100000
# District of Columbia outlier (1 law enforcement death per 500 people) adjusted
police_percapita[7] = police_percapita[7] / 10

data = [ dict(
        type = 'choropleth',
        colorscale = police_scale,
        autocolorscale = False,
        showscale = False,
        locations = us_states,
        z = police_percapita,
        locationmode = 'USA-states',
        marker = dict(
            line = dict(
                color = 'rgb(255, 255, 255)',
                width = 2
            ) ),
        ) ]

layout = dict(
        title = 'Police Officer Deaths per 100,000 People in United States (1791-2016)',
        geo = dict(
            scope = 'usa',
            projection = dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)',
            countrycolor = 'rgb(255, 255, 255)')
             )

figure = dict(data=data, layout=layout)
iplot(figure)


# Police Deaths per Capita (Past 50 Years)
# -----------------------------------

# In[ ]:


# police officer deaths per 100,000 people in state, limited to past 50 years
police_perstate50 = np.asarray(police_datausa[police_datausa.year > 1964].groupby('state')
                               .state.count())
police_percapita50 = police_perstate50 / state_population * 100000
# District of Columbia outlier (1 law enforcement death per 1,250 people) adjusted
police_percapita50[7] = police_percapita50[7] / 15

data = [ dict(
        type = 'choropleth',
        colorscale = police_scale,
        autocolorscale = False,
        showscale = False,
        locations = us_states,
        z = police_percapita50,
        locationmode = 'USA-states',
        marker = dict(
            line = dict(
                color = 'rgb(255, 255, 255)',
                width = 2
            ) ),
        ) ]

layout = dict(
        title = 'Police Officer Deaths per 100,000 People in United States (1965-2016)',
        geo = dict(
            scope = 'usa',
            projection = dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)',
            countrycolor = 'rgb(255, 255, 255)')
             )

figure = dict(data=data, layout=layout)
iplot(figure)


# In[ ]:




