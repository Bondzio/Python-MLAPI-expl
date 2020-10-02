#!/usr/bin/env python
# coding: utf-8

# # 2020 Democratic Primary Endorsements
# 
# **Remark** I have no domain knowledge, thus let me know if I am missing something useful or misusing/misunderstanding the data.
# 
# The goal of the notebook is to first analyze various statistics of endorsers which endorsed a candidate, and later do a less in depth analysis for the rest of endorsers in the list with no endorsee.
# 
# Just to recap how points are computed:
# * 10 points: *Former presidents*, *vice presidents* and *current national party leaders*
# * 8 points: *Governors*
# * 6 points: *U.S. senators*
# * 5 points: *Former presidential*, *vice-presidential nominees*, *former national party leaders* and *presidential candidates who have dropped out*
# * 3 points: *U.S. representatives* and *Mayors of large cities*
# * 2 points: *Officials in statewide elected offices* and *State legislative leaders*
# * 1 point: *Other Democratic National Committee members*
#     
# ### Table of Content
# * [Data Cleaning](#cleaning)
# * [Endorsee Analysis](#endorsee)
#     - [Endorsee Summary Table](#summarytable)
#     - [Endorsees Comparision](#comparison)
# * [Endorsers with no Endorsee](#noend)
# * [What's Next](#next)

# <a id="cleaning"></a>
# # Data Cleaning
# 
# Let's start by loading libraries and the dataset, deal with its missing values and clean columns.

# In[ ]:


import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
get_ipython().run_line_magic('matplotlib', 'inline')

import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import plotly.figure_factory as ff
from plotly import subplots
from plotly.subplots import make_subplots
init_notebook_mode(connected=True)

from datetime import date, datetime, timedelta
import time, re, os

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


def resumetable(df):
    print(f"Dataset Shape: {df.shape}")
    summary = pd.DataFrame(df.dtypes, columns=['dtypes'])
    summary = summary.reset_index()
    summary['Name'] = summary['index']
    summary = summary[['Name','dtypes']]
    summary['Missing'] = df.isnull().sum().values    
    summary['Uniques'] = df.nunique().values

    return summary

df = pd.read_csv('/kaggle/input/2020-democratic-primary-endorsements/endorsements-2020.csv')
df.head(10)


# Let's rename *endorser party* column which is spaced and check some initial statistics.

# In[ ]:


df.rename(columns={'endorser party': 'party'}, inplace=True)
resumetable(df)


# We can already see that each *Endorser* is unique in the dataframe, however most of them (~75%) do not have an *Endorsee*.
# Other columns with a high number of missing values are *city*, *body*, *order*, *district*, *date* and *source*.

# In[ ]:


percent_missing = np.round(df.isnull().sum() * 100 / len(df),2)
missing_value_df = pd.DataFrame({'column_name': df.columns,
                                 'percent_missing': percent_missing}).sort_values('percent_missing', ascending=False)


fig = go.Figure()
fig.add_trace(
        go.Bar(x=missing_value_df['column_name'],
               y=missing_value_df['percent_missing'],
               opacity=0.9,
               text=missing_value_df['percent_missing'],
               textposition='inside',
               marker={'color':'indianred'}
                   ))
fig.update_layout(
      title={'text': 'Percentage Missing by Column',
             'y':0.95, 'x':0.5,
            'xanchor': 'center', 'yanchor': 'top'},
      showlegend=False,
      xaxis_title_text='Columns',
      yaxis_title_text='Percentage',
      bargap=0.1
    )

fig.show()


# Let's drop the *city*, *body*, *order* and *district* column due to their high number of missing values - which I don't know how to fill.
# 
# Remark that only 24.75% of *endorsers* actually endorsed a candidate, those are the ones which has the triplets *date*, *endorsee* and *source*  columns populated. Otherwise all 3 columns are missing, in fact when plotting the missing values matrix, they correspond in the missing values index location. In the following plot, white corresponds to a missing value.

# In[ ]:


fig = go.Figure(
        go.Heatmap(
            z=df.isnull().astype(int),
            x=df.columns,
            y=df.index.values,
            colorscale='Greys',
            reversescale=True,
            showscale=False))

fig.update_layout(
    title={'text': 'Missing values Matrix',
             'y':0.95, 'x':0.5,
            'xanchor': 'center', 'yanchor': 'top'},
    xaxis=dict(tickangle=45, title='Columns'),
    yaxis=dict(range=[np.max(df.index.values), np.min(df.index.values)], title='Row Index'),
    )
fig.show()


# Checking this numerically we get what we espected:

# In[ ]:


df.drop(['city', 'body', 'order', 'district'], axis=1, inplace=True)
((df[['source', 'date', 'endorsee']].isnull()).astype(int).sum(axis=1)).value_counts()


# Let's do some preprocess for filling and/or mapping *source*, *endorsee* and *state* columns.

# In[ ]:


df.rename(columns={'source': 'raw_source'}, inplace=True)
df['raw_source'] = df.loc[:,'raw_source'].fillna('other')
df['source'] = 'other'

keys=['twitter', 'politico', 'youtube', '4president', 'cnn', 'apnews']

for k in keys:
    df['source'] =  np.where(df['raw_source'].str.contains(k), k,  df['source'])
    
df.drop('raw_source', axis=1, inplace=True)
df['endorsee'] = df.loc[:,'endorsee'].fillna('no_endorsee')
df['party'] = df.loc[:, 'party'].fillna('None')
resumetable(df)


# In[ ]:


state_to_s = {
 'Alabama': 'AL',
 'Alaska':'AK',
 'Arizona':'AZ',
 'Arkansas':'AR',
 'California':'CA',
 'Colorado':'CO',
 'Connecticut':'CT',
 'Delaware':'DE',
 'Florida':'FL',
 'Georgia':'GA',
 'Hawaii':'HI',
 'Idaho':'ID',
 'Illinois':'IL',
 'Indiana':'IN',
 'Iowa':'IA',
 'Kansas':'KS',
 'Kentucky':'KY',
 'Louisiana':'LA',
 'Maine':'ME',
 'Maryland':'MD',
 'Massachusetts':'MA',
 'Michigan':'MI',
 'Minnesota':'MN',
 'Mississippi':'MS',
 'Missouri':'MO',
 'Montana':'MT',
 'Nebraska':'NE',
 'Nevada':'NV',
 'New Hampshire':'NH',
 'New Jersey':'NJ',
 'New Mexico':'NM',
 'New York':'NY',
 'North Carolina' :'NC',
 'North Dakota':'ND',
 'Ohio':'OH',
 'Oklahoma':'OK',
 'Oregon':'OR',
 'Pennsylvania':'PA',
 'Rhode Island':'RI',
 'South Carolina':'SC',
 'South Dakota':'SD',
 'Tennessee':'TN',
 'Texas':'TX',
 'Utah':'UT',
 'Vermont':'VT',
 'Virginia':'VA',
 'Washington':'WA',
 'West Virginia':'WV',
 'Wisconsin':'WI',
 'Wyoming':'WY',
 'District of Columbia':'DC',
 'Marshall Islands':'MH'}

s_to_state = {}

for k,v in state_to_s.items():
    s_to_state[v]=k
    
df['full_state'] = df['state'].map(s_to_state)


# <a id="endorsee"></a>
# # Endorsee Analysis
# 
# Let's start to analyze and confront endorsees.

# In[ ]:


endorsee_df = df[df['endorsee']!='no_endorsee']
endorsee_df['endorsee'] = endorsee_df['endorsee'].str.split(' ').apply(lambda r: r[-1])
endorsee_df.head(10)


# In[ ]:


end_df = endorsee_df.groupby('endorsee').agg({'endorser': 'count', 'points': 'sum'})

end_df.rename(columns={'endorser': 'n_endorsements',
                       'points': 'tot_points'},
              inplace=True)

end_df['points_endorser_ratio'] = np.round(np.divide(end_df['tot_points'].to_numpy(), end_df['n_endorsements'].to_numpy()), 2)
end_df.reset_index(inplace=True)


# In[ ]:


fig = go.Figure()

fig.add_trace( 
        go.Scatter(
            x=end_df['n_endorsements'], 
            y=end_df['tot_points'],
            mode='markers+text',
            marker=dict(
                size=(end_df['points_endorser_ratio']+3)**2,
                color=end_df["points_endorser_ratio"],
                colorscale='geyser',
                opacity = 0.7),
            text=end_df['endorsee'],
            textposition='bottom right'
    ))

fig.update_layout(
        xaxis_type="log",
        yaxis_type="log",
        title={'text': 'Total Points per Number of Endorsers',
               'y':0.95, 'x':0.5,
               'xanchor': 'center', 'yanchor': 'top'},
        showlegend=False,
        xaxis_title_text='Number of Endorsers',
        yaxis_title_text='Total Points',
        updatemenus = list([
            dict(active=0,
                 buttons=list([
                    dict(label='Log Scale',
                         method='update',
                         args=[{'visible': True},
                               {'title': 'Log scale',
                                'xaxis': {'type': 'log'},
                                'yaxis': {'type': 'log'}}]),
                    dict(label='Log X',
                         method='update',
                         args=[{'visible': True},
                               {'title': 'Linear scale',
                                'xaxis': {'type': 'log'},
                                'yaxis': {'type': 'linear'}}]),
                    dict(label='Log Y',
                        method='update',
                       args=[{'visible': True},
                              {'title': 'Linear scale',
                               'xaxis': {'type': 'linear'},
                               'yaxis': {'type': 'log'}}]),
                    dict(label='Linear Scale',
                        method='update',
                       args=[{'visible': True},
                              {'title': 'Linear scale',
                               'xaxis': {'type': 'linear'},
                               'yaxis': {'type': 'linear'}}]),
                            ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=-0.2,
                xanchor="left",
                y=1.1,
                yanchor="top"
                )]),
        annotations=[
            go.layout.Annotation(text="Select Axis Scale", 
                                 x=-0.2, xref="paper", 
                                 y=1.13, yref="paper",
                                 align="left", showarrow=False),
        ])

fig.show()


# Both the size and the color of each Endorsee is proportional to his by his Points-to-Votes ratio.
# 
# We can see that Biden is quite far from the rest, having almost 3 times the number of votes and number of points of the "second" in the list.
# Using a linear scale is more clear that we have kind of 2 clusters, plus Biden on his own.
# 
# Finally, let's remark that Klobuchar has the highest Points-to-Votes ratio, followed by Bennet.

# <a id="summarytable"></a>
# ### Endorsee Table Summary
# 
# Let's create a chart summarizing, for each endorsee, the points received by *category*, *party*, *position*, *source* and *state*.

# In[ ]:


cols = ['category', 'source', 'position', 'party', 'state']
lc = len(cols)

d={}

for c in cols:
    tmp = endorsee_df.groupby(['endorsee', c]).agg({'points':'sum', 'endorser':'count'}).reset_index()
    tmp.rename(columns={'points': f'pt_by_{c}', 'endorser': f'votes_by_{c}'}, inplace=True)
    d[c] = tmp

cat_df = d['category']
source_df = d['source']
position_df = d['position']
party_df = d['party']
state_df = d['state']
state_df['full_state'] = state_df['state'].map(s_to_state)

buttons=[]
l=endorsee_df['endorsee'].nunique()
n_plots=5
colors = ['cadetblue', 'indianred',  'goldenrod']
pie_colors = [ 'mediumpurple', 'beige']


# In[ ]:


fig = make_subplots(
    rows=3, cols=2,
    specs=[[{'colspan':2}, None],
           [{}, {"type": "pie"}],
           [{}, {"type": 'pie'}]],
    subplot_titles=('Points by Endorser Category', 
                    'Points by Endorser Position', '% of Points by Endorser Party', 
                    'Number of Votes by Endorser Source', '% of Votes by Endorser State')
)


for i,e in enumerate(endorsee_df['endorsee'].unique()):
        
    visible = [False]*l*n_plots
    
    visible[i*lc:(i+1)*lc] = [True]*lc
        
    fig.add_trace(
            go.Bar(
                x=cat_df.loc[cat_df['endorsee']==e, 'category'],
                y=cat_df.loc[cat_df['endorsee']==e, 'pt_by_category'],
                text=cat_df.loc[cat_df['endorsee']==e, 'pt_by_category'],
                textposition='outside',
                opacity=0.9,
                marker={'color':colors[0],
                       'opacity':0.9},
                visible=False if i!=1 else True,
                showlegend=False),
        row=1, col=1)


    
    fig.add_trace(
            go.Bar(
                x=position_df.loc[position_df['endorsee']==e, 'position'],
                y=position_df.loc[position_df['endorsee']==e,'pt_by_position'],
                text=position_df.loc[position_df['endorsee']==e,'pt_by_position'],
                textposition='outside',
                opacity=0.9,
                marker={'color':colors[1],
                       'opacity':0.9},
                visible=False if i!=1 else True,
                showlegend=False),
        row=2, col=1)
    
    fig.add_trace(
            go.Pie(
                values=party_df.loc[party_df['endorsee']==e, 'pt_by_party'].to_numpy(),
                labels=party_df.loc[party_df['endorsee']==e, 'party'].to_numpy(),
                hole=0.4,
                visible=False if i!=1 else True,
                text=party_df.loc[party_df['endorsee']==e, 'party'],
                hoverinfo='label+percent+name',
                textinfo= 'percent+label',
                textposition = 'inside',
                showlegend=False,
                marker = dict(colors = plotly.colors.diverging.Geyser)),
        row=2, col=2)
    
    fig.add_trace(
            go.Bar(
                x=source_df.loc[source_df['endorsee']==e, 'source'],
                y=source_df.loc[source_df['endorsee']==e,'votes_by_source'],
                text=source_df.loc[source_df['endorsee']==e,'votes_by_source'],
                textposition='outside',
                opacity=0.9,
                marker={'color':colors[2],
                       'opacity':0.9},
                visible=False if i!=1 else True,
                showlegend=False
                       ),
        row=3, col=1)
    
    fig.add_trace(
            go.Pie(
                values=state_df.loc[state_df['endorsee']==e, 'votes_by_state'].to_numpy(),
                labels=state_df.loc[state_df['endorsee']==e, 'state'].to_numpy(),
                hole=0.4,
                visible=False if i!=1 else True,
                text=state_df.loc[state_df['endorsee']==e, 'full_state'],
                hoverinfo='label+percent+name',
                textinfo= 'percent+label',
                textposition = 'inside',
                showlegend=False,
                marker = dict(colors = plotly.colors.diverging.Geyser)),
        row=3, col=2)
    

    buttons.append(
        dict(label=e,
             method='update',
             args=[{'visible': visible},
                   #{'title': e}
                  ]))
    

fig.update_layout(
    title={'text': '<b> Endorsee Summary <b>', 'font':{'size':22},
            'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
    margin=dict(t=150),
    height=1350,
    xaxis1=dict(tickangle=45, tickvals=cat_df['category'].unique(), ticktext=cat_df['category'].unique()),
    yaxis1=dict(range=[0, np.max(cat_df['pt_by_category']+15)]),
    
    xaxis2=dict(tickangle=45, tickvals=position_df['position'].unique(), ticktext=position_df['position'].unique()),
    yaxis2=dict(range=[0, np.max(position_df['pt_by_position']+15)]),
    
    xaxis3=dict(tickangle=45, tickvals=source_df['source'].unique(), ticktext=source_df['source'].unique()), 
    yaxis3=dict(range=[0, np.max(source_df['votes_by_source']+15)]), 
    
    bargap=0.1,
    showlegend=True,
    updatemenus = list([
        dict(active=1,
             buttons=buttons,
             direction="down",
             pad={"r": 10, "t": 10},
             showactive=True,
             x=-0.15,
             xanchor="left",
             y=1.04,
             yanchor="top"
         )
     ]))

fig['layout']['annotations'] += go.layout.Annotation(text="Select Endorsee", 
                                                     x=-0.15, xref="paper", 
                                                     y=1.05, yref="paper",
                                                     align="left", showarrow=False),
    
    

fig.show()


# <a id="comparison"></a>
# 
# ### Endorsees Comparison
# 
# First and foremost, let's plot each Endosee cumulative points over time.

# In[ ]:


endorsee_df['date'] = pd.to_datetime(endorsee_df['date'])
e = endorsee_df.set_index('date')
pt_over_time = e.groupby("endorsee").resample('15D').agg({"endorser": np.size, "points": np.sum})
pt_over_time.reset_index(inplace=True)
pt_over_time['cum_points'] = pt_over_time.sort_values('date').groupby(by=['endorsee'])['points'].transform(lambda x: x.cumsum())
pt_over_time['cum_votes'] = pt_over_time.sort_values('date').groupby(by=['endorsee'])['endorser'].transform(lambda x: x.cumsum())


# In[ ]:


fig = go.Figure()

for i,e in enumerate(endorsee_df['endorsee'].unique()):
    
    fig.add_trace(
        go.Scatter(
            x=pt_over_time.loc[pt_over_time['endorsee']==e, 'date'],
            y=pt_over_time.loc[pt_over_time['endorsee']==e, 'cum_points'],
            name=e,
            mode ='markers+lines',
            showlegend=True)
        )
    
fig.update_layout(
    height=550,
    #width=800,
    title={'text': 'Total Points per over Time',
           'y':0.95, 'x':0.5,
           'xanchor': 'center', 'yanchor': 'top'},
    xaxis=dict(range=[date(2019,1,1), np.max(pt_over_time['date'])]),
    yaxis=dict(title='Points')
    )

fig.show()


# Now let's compare candidates using the *category*, *party*, *state* columns as source of points. 
# 
# The first plot shows each candidate points split among one of the possible column to select - this makes it easy to compare candidates points over the same value of the selected column.
# 
# On the other hand the bar plot quantifies the total amount of points, split by the above aggregation selected above. 

# In[ ]:


cols = ['category', 'party', 'state']
d={}

for c in cols:
    tmp = endorsee_df.groupby(['endorsee', c]).agg({'points':'sum', 'endorser':'count'}).reset_index()
    tmp.rename(columns={'points': f'pt_by_{c}', 'endorser': f'votes_by_{c}'}, inplace=True)
    d[c] = tmp
    
    
n_plots=2
l=len(cols)
buttons=[]

fig = make_subplots(
    rows=2, cols=1,
    specs=[[{}],
           [{}]],
    row_heights=[0.65, 0.35]
)


for i,c in enumerate(cols):

    visible = [False]*l*n_plots
    visible[i*n_plots:(i+1)*n_plots] = [True]*n_plots

    tmp = d[c]
    
    fig.add_trace( 
        go.Scatter(
            y=tmp[c],
            x=tmp['endorsee'],
            mode='markers+text',
            marker=dict(
                size=np.where(tmp[f'pt_by_{c}']<50, tmp[f'pt_by_{c}']+20, 60),
                color=tmp[f'votes_by_{c}'],
                colorscale='geyser',
                showscale=False,
                opacity = 0.7),
            text=tmp[f'pt_by_{c}'],
            visible=True if i==0 else False,
            textposition='middle center'),
        row=1, col=1)

    fig.add_trace(
        go.Bar(
            x=tmp['endorsee'],
            y=tmp[f'pt_by_{c}'],
            text=tmp[f'pt_by_{c}'],
            hoverinfo='all',
            textposition='inside',
            visible=True if i==0 else False,
            marker=dict(
                color=tmp[f'pt_by_{c}'],
                colorscale='geyser')),
        row=2, col=1)

    buttons.append(
        dict(label= ' '.join([s.capitalize() for s in c.split('_')]),
             method='update',
             args=[{'visible': visible},
                   {'title': {'text': 'Points by ' + [s.capitalize() for s in c.split("_")][-1],
                              'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                   #'yaxis1': {'title': f'Endorser {c.capitalize()}'},
                   #'yaxis2': {'title': f'Points by Endorser {c.capitalize()}'}
                   }]
            )
        )

    
fig.update_layout(
      height=1350,
      showlegend=False,
      xaxis1=dict(tickangle=45, title='Endorsee'),
      #yaxis1=dict(title='Endorsee Category'),
      xaxis2=dict(tickangle=45, title='Endorsee'),
      yaxis2=dict(title='Points', type='log'),
      updatemenus = list([
          dict(active=0,
             buttons=buttons,
             direction="right",
             pad={"r": 10, "t": 10},
             #showactive=True,
             x=0.15,
             xanchor="left",
             y=1.08,
             yanchor="top"
         )
     ]),
    annotations=[
        go.layout.Annotation(text="Select Aggregation", x=-0.12, xref="paper", y=1.06, yref="paper",
                             align="left", showarrow=False),
    ])
    

fig.show()


# Takeaways:
#  1. Category:
#      * Bloomberg has the highest points by majors endorsers.
#      * Warren has the highest points from statewide officeholders.
#      * Klobuchar is the only one with points coming from endorsement of past president or vicepresident.
#      * For every other category, Biden gets the highest score.
#  2. Party:
#      * All endorsers except 3 are Democrats.
#      * Booker is the only one endorsed by a Republican.
#  3. State:
#      * California is split between Biden and Harris
#      * Booker is strong in New Jersey, Harris is California, Klobuchar in Minnesota, Warren in Massachusetts.
#      * Biden has votes from 29 states, followed by Warren from 14, Sanders and Buttigieg from 13.

# <a id="noend"></a>
# # Endorsers with no Endorsee Analysis
# 
# Let's plot what's the "bivariate distribution" of Endorsers which did not endorse any candidate.

# In[ ]:


noend = df.loc[df['endorsee']=='no_endorsee']
noend.head(10)


# In[ ]:


from itertools import product 
cols = ['category', 'party', 'position', 'state']
col_pairs=[]
d={}
for i,c1 in enumerate(cols):
    for c2 in cols[i+1:]:
        col_pair=c1.capitalize() + '-' + c2.capitalize()
        tmp = noend.groupby([c1,c2]).agg({'points':'sum', 'endorser':'count'}).reset_index()
        tmp.rename(columns={'points': f'pt_by_{col_pair}', 'endorser': f'votes_by_{col_pair}'}, inplace=True)
        d[col_pair] = tmp
        col_pairs.append((c1,c2))


# In[ ]:


l=len(col_pairs)
buttons=[]

fig = go.Figure()

for j, (c1,c2) in enumerate(col_pairs):
    
    col_pair = c1.capitalize() + '-' + c2.capitalize()
    visible = [False]*l
    visible[j] = True

    tmp = d[col_pair]
    
    fig.add_trace( 
        go.Scatter(
            x=tmp[c1],
            y=tmp[c2],
            mode='markers+text',
            marker=dict(
                size=np.where(tmp[f'pt_by_{col_pair}']<50, tmp[f'pt_by_{col_pair}']+20, 60),
                color=tmp[f'votes_by_{col_pair}'],
                colorscale='geyser',
                showscale=False,
                opacity = 0.7),
            text=tmp[f'pt_by_{col_pair}'],
            visible=True if j==0 else False,
            textposition='middle center'))

    buttons.append(
        dict(label=col_pair,
             method='update',
             args=[{'visible': visible},
                   {'title': {'text': f'Votes by <b>{c1.capitalize()}<b> &  <b>{c2.capitalize()}<b>',
                              'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                   'xaxis': {'title': c1.capitalize(), 'tickangle': 45},
                   'yaxis': {'title': c2.capitalize()}
                   }]
            )
        )
  

    
fig.update_layout(
      margin=dict(l=120, t=200),
      height=1150,
      showlegend=False,
      title = {'text': f'Votes by <b>{col_pairs[0][0].capitalize()}<b> &  <b>{col_pairs[0][1].capitalize()}<b>',
                              'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
      xaxis={'title': col_pairs[0][0].capitalize(), 'tickangle':45},
      yaxis={'title': col_pairs[0][1].capitalize()},
      updatemenus = [
          go.layout.Updatemenu(
             active=0,
             buttons=buttons,
             direction="down",
             pad={"r": 10, "t": 10},
             #showactive=True,
             x=0,
             xanchor="left",
             y=1.1,
             yanchor="top"
         )
     ],
    annotations=[
        go.layout.Annotation(text="Select Columns", x=0.02, xref="paper", y=1.12, yref="paper",
                             align="left", showarrow=False),
    ])
    

fig.show()


# <a id="next"></a>
# ### Where to go from here?
# 
# As I mentioned at the beginning I have no domain knowledge, I think it is possible to cluster values in the *position* columns, and maybe also *state* based on some understanding of their political situation.
# 
# Another interesting analysis would be to confront *endorsers* behaviour with respect to 2016 Democratic Primary Endorsements data.
# 
# As always, any feedback is more than welcomed :)
