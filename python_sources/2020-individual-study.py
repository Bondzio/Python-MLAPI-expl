#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.
import seaborn as sns
import matplotlib.pyplot as plt

import folium 
from folium import plugins
from folium import FeatureGroup, LayerControl, Map, Marker
# from folium.plugins import HeatMap

import json 
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

import datetime

import plotly.graph_objects as go
import plotly.express as px

from pyproj import Proj, transform


# In[ ]:


TimeGender = pd.read_csv('../input/coronavirusdataset/TimeGender.csv')
Case = pd.read_csv('../input/coronavirusdataset/Case.csv')
Region = pd.read_csv('../input/coronavirusdataset/Region.csv')
TimeProvince = pd.read_csv('../input/coronavirusdataset/TimeProvince.csv')
SearchTrend = pd.read_csv('../input/coronavirusdataset/SearchTrend.csv')
PatientRoute = pd.read_csv('../input/coronavirusdataset/PatientRoute.csv')
SeoulFloating = pd.read_csv('../input/coronavirusdataset/SeoulFloating.csv')
Time = pd.read_csv('../input/coronavirusdataset/Time.csv')
PatientInfo = pd.read_csv('../input/coronavirusdataset/PatientInfo.csv')
Weather = pd.read_csv('../input/coronavirusdataset/Weather.csv')
TimeAge = pd.read_csv('../input/coronavirusdataset/TimeAge.csv')
Policy = pd.read_csv('../input/coronavirusdataset/Policy.csv')


# # Trend of Contact_number of patients over age and gender

# In[ ]:


PatientInfo[pd.notna(PatientInfo['contact_number'])]
PatientRoute.merge(PatientInfo, on=['patient_id']).groupby(['patient_id']).count()
PatientInfo.groupby(['infected_by']).count().sort_values('patient_id', ascending=False).head(20).style.format("{:.0f}")


# PatientInfo['age'] = 2020 - PatientInfo['birth_year'].astype(int) + 1
PatientInfo['age'] = PatientInfo['age'].str.slice(0, -1).astype(float)
PatientInfo['age_group'] = PatientInfo['age'] // 10
PatientInfo['age_group'] = [str(a).replace('.','') for a in PatientInfo['age_group']]
PatientInfo['age_gender'] = PatientInfo['age_group'] + '_' + PatientInfo['sex']

PatientInfo[PatientInfo['contact_number'] == '-'] = np.nan
PatientInfo['contact_number'] = PatientInfo['contact_number'].astype(float)

fig = plt.gcf()
fig.set_size_inches(15, 5)

classes = np.sort(pd.unique(PatientInfo['age_gender'].dropna().values.ravel()))
boxplot = sns.boxplot(x="age_gender", y="contact_number", data=PatientInfo[PatientInfo['contact_number'] < 200], order = classes)
boxplot.set_xticklabels(boxplot.get_xticklabels(), rotation=45)
plt.title("Age vs Contact_number")
plt.show()

print(np.sort(pd.unique(PatientInfo['age_group'].dropna().values.ravel())))


# In[ ]:


PatientRoute['date'] = pd.to_datetime(PatientRoute['date'])


# In[ ]:


def return_total_distance(patient_id, symptom_date=datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')):
    total_distance = 0
    x = 0
    y = 0
    first = True
    for index,row in PatientRoute[PatientRoute['patient_id'] == patient_id].iterrows():
        prev_x = x
        prev_y = y
        x = row['longitude']
        y = row['latitude']            
        if (not first):
            total_distance += (((x - prev_x) * 88.74) ** 2 + ((y - prev_y) * 110) ** 2) ** 0.5
        first = False

            
    return total_distance
        
PatientInfo['total_distance'] = PatientInfo['patient_id'].map(return_total_distance)


# In[ ]:


def return_visit_count(patient_id, symptom=False):
    if symptom:
        symptom_date = datetime.datetime.strptime(PatientInfo[PatientInfo['patient_id'] == patient_id]['symptom_onset_date'].values[0], '%Y-%m-%d')
    else:
        symptom_date =datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')
    if (PatientRoute['patient_id'] == patient_id).any():
        return PatientRoute[(PatientRoute['patient_id'] == patient_id) & (PatientRoute['date'] >= symptom_date)].groupby(['latitude', 'longitude']).ngroups
    else:
        return np.nan
    
PatientInfo['visit_count'] = PatientInfo['patient_id'].map(return_visit_count)
PatientInfo


# # Trend of number of visited sites of patients over age and gender

# In[ ]:


fig = plt.gcf()

fig.set_size_inches(15, 5);
print(PatientInfo.loc[3127, 'visit_count'])
# classes = np.sort(pd.unique(PatientInfo['age_group'].dropna().values.ravel()))

df2 = PatientInfo[pd.notna(PatientInfo['visit_count'])].groupby('age_gender').mean();
df2.reset_index(inplace=True);
barplot = sns.barplot(x='age_gender', y='visit_count', data=df2);
barplot.set_xticklabels(barplot.get_xticklabels(), rotation=45)
plt.title('Age VS Number of visited sites')
plt.show()


# In[ ]:


def return_distance_symptom(patient_id, symptom=True):
    if symptom:
        try:
            symptom_date = datetime.datetime.strptime(PatientInfo[PatientInfo['patient_id'] == patient_id]['symptom_onset_date'].values[0], '%Y-%m-%d')
        except:
            return np.NaN
    else:
        symptom_date =datetime.datetime.strptime('2000-01-01', '%Y-%m-%d') 

    max_x = PatientRoute[
        (PatientRoute['patient_id'] == patient_id) & (PatientRoute['date'] > symptom_date)
    ]['longitude'].max()
    max_y = PatientRoute[
        (PatientRoute['patient_id'] == patient_id) & (PatientRoute['date'] > symptom_date)
    ]['latitude'].max()
    min_x = PatientRoute[
        (PatientRoute['patient_id'] == patient_id) & (PatientRoute['date'] > symptom_date)
    ]['longitude'].min()
    min_y = PatientRoute[
        (PatientRoute['patient_id'] == patient_id) & (PatientRoute['date'] > symptom_date)
    ]['latitude'].min()
    return (((max_x - min_x) * 88.74) ** 2 + ((max_y - min_y) * 110) ** 2) ** 0.5


# In[ ]:


def return_visit_count_symptom(patient_id, symptom=True):
    if symptom:
        try:
            symptom_date = datetime.datetime.strptime(PatientInfo[PatientInfo['patient_id'] == patient_id]['symptom_onset_date'].values[0], '%Y-%m-%d')
        except:
            return np.nan
    else:
        symptom_date =datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')
    # print(PatientRoute['date'] >= symptom_date)
    if (PatientRoute['patient_id'] == patient_id).any():
        return PatientRoute[(PatientRoute['patient_id'] == patient_id) & (PatientRoute['date'] >= symptom_date)].groupby(['latitude', 'longitude']).ngroups
    else:
        return np.nan


# In[ ]:


# PatientInfo_symptom = PatientInfo[pd.notna(PatientInfo['symptom_onset_date'])].copy(deep=True)
PatientInfo['distance_after_symptom'] = PatientInfo['patient_id'].map(return_distance_symptom)


# In[ ]:


PatientInfo['visit_count_after_symptom'] = PatientInfo['patient_id'].map(return_visit_count_symptom)


# In[ ]:


fig = plt.gcf()

fig.set_size_inches(20, 8);

# classes = np.sort(pd.unique(PatientInfo_symptom['age_gender'].dropna().values.ravel()));

df2 = PatientInfo[PatientInfo['distance_after_symptom'] > 0].groupby('age_group').mean();
df2.reset_index(inplace=True);
barplot = sns.barplot(x='age_group', y='distance_after_symptom', data=df2)
barplot.set_xticklabels(barplot.get_xticklabels(), rotation=45)
plt.title('Who move well after symptoms?')
plt.show()


# # Trend of number of visited sites after showing symptoms of patients over age and gender

# In[ ]:


fig = plt.gcf()

fig.set_size_inches(15, 5);

# classes = np.sort(pd.unique(PatientInfo_symptom['age_gender'].dropna().values.ravel()));

df2 = PatientInfo[pd.notna(PatientInfo['visit_count_after_symptom'])].groupby('age_gender').count();
df2.reset_index(inplace=True);
barplot = sns.barplot(x='age_gender', y='visit_count', data=df2)
barplot.set_xticklabels(barplot.get_xticklabels(), rotation=45)
plt.title('Age VS Number of visited sites (After showing symptom)')
plt.show()


# In[ ]:


fig = plt.gcf()

fig.set_size_inches(15, 5);

# classes = np.sort(pd.unique(PatientInfo_symptom['age_gender'].dropna().values.ravel()));

df2 = PatientInfo[pd.notna(PatientInfo['visit_count'])].groupby('infection_case').mean();
df2.reset_index(inplace=True);
barplot = sns.countplot(x='type', data=PatientRoute) # [~PatientRoute['type'].isin(['etc', 'hospital'])]
barplot.set_xticklabels(barplot.get_xticklabels(), rotation=45)
plt.title('Where is dangerous?')
plt.show()


# # The traveling distance of patients
# 
# https://news.joins.com/article/23739340
# 
# http://www.donga.com/news/article/all/20200409/100569089/1
# 
# Korea government launched a social distance campaign to prevent spread of COVID-19.
# Also, a lot of government including Europe pass the ordinance, which restricts movements.
# 
# We are sure that the social distancing and restriction of movements is effective for preventing COVID-19, but my question is 'Do people really keeps the guideline?'
# 
# In this part, I made some interpretations which show whether patients keep the social distancing or not.
# 
# 
# The ordinary method (usaully in leaderboard) :
# * Counting rows of patients' route data.
# 
# Problems
# * Visiting same place many times may be less critical because of limitation in contacted people.
# * It doesn't include data expressing distance.
# * (e.g. Visiting store in front the house VS visiting Busan)
# 
# 2 weeks ago, I made some visualizations which shows how many places the patient visited, but it also doesn't include data about moving distance.
# 
# Thus, I craeted another feature 'distance' which shows each patient's range of movement from patients' route data, and I visualize it in some ways.

# In[ ]:


# Return each patient's range of movement in killometers.
def return_distance(patient_id, symptom_date=datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')):
 
    max_x = PatientRoute[
        (PatientRoute['patient_id'] == patient_id) & (PatientRoute['date'] >= symptom_date)
    ]['longitude'].max()
    max_y = PatientRoute[
        (PatientRoute['patient_id'] == patient_id) & (PatientRoute['date'] >= symptom_date)
    ]['latitude'].max()
    min_x = PatientRoute[
        (PatientRoute['patient_id'] == patient_id) & (PatientRoute['date'] >= symptom_date)
    ]['longitude'].min()
    min_y = PatientRoute[
        (PatientRoute['patient_id'] == patient_id) & (PatientRoute['date'] >= symptom_date)
    ]['latitude'].min()
    return (((max_x - min_x) * 88.74) ** 2 + ((max_y - min_y) * 110) ** 2) ** 0.5

PatientInfo['distance'] = PatientInfo['patient_id'].map(return_distance)


# In[ ]:


# Distribution of the traveling range of each patient
plt.figure(figsize=(16, 6))
sns.set()
ax = sns.distplot(PatientInfo[(PatientInfo['distance'] > 0) & (PatientInfo['distance'] < 500)]['distance'],kde=False, bins=100)


# Many patients kept the social distancing well. But, some patients moved a lot even in this situation.
# 
# There might be some groups like people who keeps well, people who keeps little, people who ignore the guideline to go to travel of business trip. It can be further topic.
# 
# # The traveling range for each age group

# In[ ]:


sns.set()
plt.figure(figsize=(16, 6))

# To see the distribution easily, I dropped outliers which the traveling distance was over than 400 km.
fig = px.box(PatientInfo[PatientInfo['distance']<400], x="age_group", y="distance", points="all")
fig.update_xaxes(dtick=10)
fig.show()


# Like popular opinion, 20s patients usually moved for a long distance and have many outliers who covered a wide area.

# # The traveling distance of each patient in time series

# After pandemic, there were a lot of guidelines about social distancing and restriction of movements.
# 
# So, there would be some change in patients movement as time goes on.
# 
# To interpret patients' movement in time series,
# 1. Calculate distance between naighbor rows in patients' route data.
# 2. Sum distances for each patient and each week.
# 3. Average the traveling distance on each week and each age group.

# In[ ]:


# Calculate distance between naighbor rows in patients' route data.
prev_id = ""
PatientRoute['diff_distance'] = 0
for i, row in PatientRoute.iterrows():
    if prev_id == row['patient_id']:
        prev_x = PatientRoute.loc[i-1]['longitude']
        prev_y = PatientRoute.loc[i-1]['latitude']
        x = PatientRoute.loc[i]['longitude']
        y = PatientRoute.loc[i]['latitude']
        diff = (((x - prev_x) * 88.74) ** 2 + ((y - prev_y) * 110) ** 2) ** 0.5
        
        PatientRoute.loc[i, 'diff_distance'] = diff
    else:
        PatientRoute.loc[i, 'diff_distance'] = np.nan
    prev_id = row['patient_id']


# In[ ]:


Policy['start_week'] = pd.to_datetime(Policy['start_date']).dt.weekofyear

def mark_policy(fig):
    fig.update_layout(

        annotations=[
            dict(
                x=Policy[Policy['type'] == 'Alert'].iloc[1]['start_week'],
                y=1,
                xref="x",
                yref="y",
                text=f"Alert {Policy[Policy['type'] == 'Alert'].iloc[1]['detail']}",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40,
                bgcolor='white'
            ),
            dict(
                x=Policy[Policy['type'] == 'Alert'].iloc[2]['start_week'],
                y=1,
                xref="x",
                yref="y",
                text=f"Alert {Policy[Policy['type'] == 'Alert'].iloc[2]['detail']}",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-60,
                bgcolor='white'
            ),
            dict(
                x=Policy[Policy['type'] == 'Alert'].iloc[3]['start_week'],
                y=1,
                xref="x",
                yref="y",
                text=f"Alert {Policy[Policy['type'] == 'Alert'].iloc[3]['detail']}",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40,
                bgcolor='white'
            ),
            dict(
                x=Policy[Policy['type'] == 'Social'].iloc[0]['start_week'],
                y=1,
                xref="x",
                yref="y",
                text=f"{Policy[Policy['type'] == 'Social'].iloc[0]['gov_policy']}",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40,
                bgcolor='white'
            )
        ]
    )    


# In[ ]:


PatientRoute['week'] = PatientRoute['date'].dt.weekofyear


# In[ ]:


colors = px.colors.sequential.Plotly3

# Sum distances for each patient and each week.
# Average the traveling distance on each week and each age group.

df = PatientRoute[PatientRoute['diff_distance'].notna()]
new_df = df.merge(PatientInfo, on='patient_id')[
    ['week','age_group','patient_id','diff_distance']
].dropna().groupby(['week','age_group','patient_id']).sum().reset_index().groupby([
    'week','age_group'
]).mean().reset_index()
fig = px.line(new_df, x='week', y='diff_distance', color='age_group')
# fig.Layout(legend={'traceorder': 'normal'})

fig = go.Figure()
for i, age in enumerate(sorted(new_df['age_group'][new_df['age_group'].notna()].unique().tolist())):
    if age in ['00','10','90','nan']:
        continue
    cur_df = new_df[new_df['age_group'] == age]
    fig.add_trace(go.Scatter(x=cur_df['week'], y=cur_df['diff_distance'],
                        hoverinfo='all', hoverlabel=dict(bgcolor='white'),
                        mode='lines',
                        line=dict(width=2, color=colors[i]),
                        name=age))
mark_policy(fig)
    
fig.update_layout(title='Who moves a lot?',
        showlegend=True,
        xaxis=dict(
            range=[4, 16],
            ticksuffix=' week'),
        yaxis=dict(
            ticksuffix=' km'),
        )
fig.show()


# As time goes on, patients in all age group was deactivated.
# 
# Especially, When governments raised alert level and launched social distancing campaign, their movements was decreased.
# 
# In terms of age, dark traces means younger people. As seen, younger people like 20s~30s usually moved a longer distance than older.

# In[ ]:


cdf = new_df[~new_df['age_group'].isin(['00','10','90','nan'])].pivot('age_group','week','diff_distance')

data = [
    go.Contour(x=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
               y=['20','30','40','50','60','70','80'],
        z=cdf.values,
        colorscale='Jet',
    )
]

layout = go.Layout(
    title = "Who moves a lot?",
    yaxis = dict(range=[10,80], ticksuffix='s'),
    xaxis = dict(ticksuffix=' week'),
    xaxis_title="weeks",
    yaxis_title="age group",
)

fig = go.Figure(data=data, layout=layout)
fig.show()


# This is contour plot with same data. It also shows younger patients usually covered a wide area, so they would give a bad effect on spread of COVID-19.

# # The place most patients visited
# 
# In this part, I visualized where the patients usually visited.
# 
# Although there are already many visualizations about the place which most patients visited, there are some problems.
# 
# The ordinary method (usaully in leaderboard):
# - Just show absolute number of each type of place
# 
# Problem:
# - Hard to catch the changes with time varying
# - Too many hospital (Every patients would go hospital because of symptoms. And, it makes hard to analyze the other type of place)
# 
# 
# For these reasons, I classified the type of place to the large group which are 'medicine', 'transportation', 'life', 'entertainment', 'education', 'church'.
# 
# And, to visualize change for time and age, I normalized for each week and age group.
# 
# It was effective because the number of patients was so vary for time,and it makes hard to see the changes of type clearly.

# In[ ]:


PatientRoute['type'].unique()


# In[ ]:



def large_type(x):
    if x in ['academy', 'school', 'university']:
        return 'education'
    elif x in ['airport', 'public_transportation', 'gas_station']:
        return 'transportation'
    elif x in ['hospital', 'pharmacy']:
        return 'medicine'
    elif x in ['store', 'restaurant', 'beauty_salon', 'bank', 'bakery', 'real_estate_agency', 'posr_office', 'lodging']:
        return 'life'
    elif x in ['pc_cafe', 'bar', 'gym', 'cafe']:
        return 'entertainment'
    elif x in ['church']:
        return 'church'
    else:
        return 'etc'

PatientRoute['large_type'] = PatientRoute['type'].map(large_type)

type_by_time = PatientRoute.groupby(['week', 'large_type']).size().unstack().fillna(0)
# type_by_time = type_by_time.div(type_by_time.sum(axis=1), axis=0) * 100
type_by_time
type_by_time_age = []
df = PatientRoute.merge(PatientInfo, on='patient_id')
for age in ['20','30','40','50','60','70','80']:
    
    new_type_by_time = df[df['age_group'] == age].groupby(['week', 'large_type']).size().unstack().fillna(0)
    if 'education' not in new_type_by_time.columns:
        new_type_by_time['education'] = 0
    if 'entertainment' not in new_type_by_time.columns:
        new_type_by_time['entertainment'] = 0
    type_by_time_age.append(new_type_by_time)


# In[ ]:



colors = px.colors.qualitative.Light24
x = type_by_time.index.tolist()
categories = ['medicine', 'transportation', 'life', 'entertainment', 'education', 'church', 'etc']
fig = go.Figure()

for i, cat in enumerate(categories):
    fig.add_trace(go.Scatter(x=x, y=type_by_time[cat],
                        hoverinfo='x+y',
                        mode='lines',
                        line=dict(width=0.5, color=colors[i]),
                        name=cat,
                        stackgroup='one',
                        groupnorm='percent'))
for age, df in enumerate(type_by_time_age):
    for i, cat in enumerate(categories):
        fig.add_trace(go.Scatter(x=df.index.tolist(), y=df[cat],
                            hoverinfo='x+y',
                            mode='lines',
                            line=dict(width=0.5, color=colors[i]),
                            name=cat,
                            stackgroup=age,
                            groupnorm='percent',
                            visible=False))    

fig.update_layout(
    title='Where most patients visited?',
    showlegend=True,
    xaxis=dict(
        range=[4, 16],
        ticksuffix=' week'
    ),
    yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%'))
mark_policy(fig)

menus = []
for i, name in enumerate(['All', '20','30','40','50','60','70','80']):
    d = dict(label=name,
                     method="update",
                     args=[{"visible": [False]*i*7 + [True]*7 + [False]*(8-i-1)*7},
                           {"title": f"Where most patients visited? (Age: {name})"}])
    menus.append(d)

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=1,
            y=1.2,
            buttons=menus,
        )
    ],
    xaxis_title="weeks",
    yaxis_title="% in group of patients",
)

fig.show()


# I also marked some important policies for COVID-19.
# 
# As time goes on, the patients who move for entertainment or life, church was decreased. It was impressive since many patients keep the social distancing as well.
# 
# Also, the patients who visited educational place like school was comparatively less, and it means the policy to delay opening semester was effective.
# 
# The reason of increased percentage for 'transportation' would be homecoming of people who stayed abroad.
# 
# For 20s, the percenatage of less essential place like church, entertainment, life was impressively decreased after social distancing campaign.
# 
# Even for church, the older people usually went to the church even after raising alert level and social distancing campaign.
# 
# 
# 

# In[ ]:


PatientInfoRoute = PatientInfo.merge(PatientRoute, on="patient_id")

for group_name, group in PatientInfoRoute.groupby("patient_id"):
    x = 0
    y = 0
    for row_index, row in group.iterrows():
        if x == 0:
            x = row['longitude']
            y = row['latitude']
        PatientInfoRoute.loc[row_index, 'relative_x'] = PatientInfoRoute.loc[row_index, 'longitude'] - x
        PatientInfoRoute.loc[row_index, 'relative_y'] = PatientInfoRoute.loc[row_index, 'latitude'] - y


# In[ ]:


df = PatientInfoRoute.groupby('patient_id').filter(lambda x: x['relative_x'].count()>1)
df[df['patient_id']==1700000020]['date']


# In[ ]:


from ipywidgets import interact
f = go.FigureWidget()
# for group_name, group in PatientInfoRoute.groupby("patient_id"):
#     f.add_scatter(x=group['relative_x'], y=group['relative_y'], visible=False)

# steps = []
# for i in range(len(f.data)):
#     step = dict(
#         method="update",
#         args=[{"visible": [False] * len(f.data)},
#              {"title": "Slider switched to patient_id: "}],
#     )
#     step["args"][0]["visible"][i] = True
#     steps.append(step)

# sliders = [dict(
#     active=10,
#     currentvalue={"prefix": "patient_id: "},
#     steps=steps
# )]
# f.update_layout(sliders=sliders)
f.update_xaxes(range=[-1,1])
f.update_yaxes(range=[-1.3,1.3])
f.update_layout(width=400, height=400)

scatt = f.add_scatter()

@interact(patient_id=PatientInfoRoute.groupby('patient_id').filter(lambda x: x['relative_x'].count()>1)['patient_id'].unique())
def update(patient_id="1000000001"):
    with f.batch_update():
        f.data = []
        f.add_scatter(x=PatientInfoRoute[PatientInfoRoute['patient_id'] == patient_id]['relative_x'],
                    y= PatientInfoRoute[PatientInfoRoute['patient_id'] == patient_id]['relative_y'],
                     mode='lines+markers')
        x_max = PatientInfoRoute[PatientInfoRoute['patient_id'] == patient_id]['relative_x'].abs().max()
        y_max = PatientInfoRoute[PatientInfoRoute['patient_id'] == patient_id]['relative_y'].abs().max()
        f.update_xaxes(range=[-max(x_max,y_max), max(x_max,y_max)])
        f.update_yaxes(range=[-max(x_max,y_max), max(x_max,y_max)])
        
f

