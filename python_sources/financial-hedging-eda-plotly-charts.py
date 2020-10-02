#!/usr/bin/env python
# coding: utf-8

# <h1> Welcome to my Kernel </h1><br>
# I will do some explorations though the data of Financial Hedging just to better understand the pattern of variables
# <br>
# 
# *English is not my first language, so sorry for any mistake. *
# 
# <h3> Introduction to the data</h3> 

# <b>Background:</b>
# The underlying concept behind hedging strategies is simple, create a model, and make money doing it. The hardest part is finding the features that matter. For a more in-depth look at hedging strategies, I have attached one of my graduate papers to get you started.
#  <br>
# - <b>Mortgage-Backed Securities</b> <br>
# - <b>Geographic Business Investment</b> <br>
# - <b> Real Estate Analysis </b><br>
# 
# 
# <b>Statistical Fields:</b> <br>
# Note: All interpolated statistical data include Mean, Median, and Standard Deviation Statistics. For more information view the variable definitions document.
# 
# <b>Monthly Mortgage & Owner Costs: </b>Sum of mortgage payments, home equity loans, utilities, property taxes <br>
# <b>Monthly Owner Costs:</b> Sum of utilities, property taxes <br>
# <b>Gross Rent:</b> contract rent plus the estimated average monthly cost of utilities <br>
# <b>Household Income: </b>sum of the householder and all other individuals +15 years who reside in the household <br>
# <b>Family Income:</b> Sum of incomes of all members +15 years of age related to the householder.

# # <font color="red">If it were useful for you, please <b>UPVOTE</b> the kernel and give me your feedback =)</font>

# ## Importing Libraries

# In[ ]:


#Load the librarys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

import plotly.tools as tls
import plotly.offline as py
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
init_notebook_mode(connected=True)
import warnings

from scipy import stats

get_ipython().run_line_magic('matplotlib', 'inline')

# figure size in inches
rcParams['figure.figsize'] = 12,6


# ## Reading Dataset

# In[ ]:


df_features = pd.read_csv("../input/real_estate_db.csv", encoding='ISO-8859-1' )

del df_features['BLOCKID']
del df_features['UID'] 


# ## If you want to see how the data appears, and other informations, click in "Show Output" button

# In[ ]:


def resumetable(df):
    print(f"Dataset Shape: {df.shape}")
    summary = pd.DataFrame(df.dtypes,columns=['dtypes'])
    summary = summary.reset_index()
    summary['Name'] = summary['index']
    summary = summary[['Name','dtypes']]
    summary['Missing'] = df.isnull().sum().values    
    summary['Uniques'] = df.nunique().values
    summary['First Value'] = df.loc[0].values
    summary['Second Value'] = df.loc[1].values
    summary['Third Value'] = df.loc[2].values

    for name in summary['Name'].value_counts().index:
        summary.loc[summary['Name'] == name, 'Entropy'] = round(stats.entropy(df[name].value_counts(normalize=True), base=2),2) 

    return summary


# # Resuming our data

# ### First part of features 

# In[ ]:


#looking the shape of data
resumetable(df_features)[:43]


# ### Second part of features

# In[ ]:


#looking the shape of data
resumetable(df_features)[43:]


# ## Look head of our data

# In[ ]:


#Looking the data
df_features.head()


# # Type Feature
# - I ever need to define a feature to start. In general, I ever try to start by categoricals, so I choose "Type" feature.
# - Let's start by the distribution of each type in our data

# In[ ]:


percentual_types = round(df_features["type"].value_counts(), 2)

types = round(df_features["type"].value_counts() / len(df_features["type"]) * 100,2)

labels = list(types.index)
values = list(types.values)

trace1 = go.Pie(labels=labels, values=values, marker=dict(colors=['red']), text = percentual_types.values,)

layout = go.Layout(title='Distribuition of Types', legend=dict(orientation="h"));

fig = go.Figure(data=[trace1], layout=layout)
iplot(fig)


# 

# # Interactive 

# # I will introduce a interactive plot that will be possible use a dropdown to change to count of each categorical feature

# In[ ]:


state_count = df_features["state"].value_counts()
city_count = df_features.city.value_counts()
place_count = df_features.place.value_counts()
primary_count = df_features.primary.value_counts()


# In[ ]:


trace1 = go.Bar(x=state_count[:20].values[::-1],
                y=state_count[:20].index[::-1],
                orientation='h', visible=True,
                      name='Top 20 States',
                      marker=dict(
                          color=city_count[:20].values[::-1],
                          colorscale = 'Viridis',
                          reversescale = True
                      ))

trace2 = go.Bar(x=city_count[:20].values[::-1],
                      y=city_count[:20].index[::-1],
                      orientation = 'h', visible=False, 
                      name='TOP 20 Citys',
                      marker=dict(
                          color=city_count[:20].values[::-1],
                          colorscale = 'Viridis',
                          reversescale = True
                      ))

trace3 = go.Histogram(y=sorted(df_features['type'], reverse=True), histnorm='percent', orientation='h', visible=False, 
                      name='Type Count')

trace4 = go.Bar(x=place_count[:20].values[::-1],
                y=place_count[:20].index[::-1],
                orientation='h', visible=False, 
                name='Top 20 Place',
                marker=dict(
                    color=city_count[:20].values[::-1],
                    colorscale = 'Viridis',
                    reversescale = True
                      ))

data = [trace1, trace2, trace3, trace4]

updatemenus = list([
    dict(active=-1,
         x=-0.15,
         buttons=list([  
            dict(
                label = 'State Count',
                 method = 'update',
                 args = [{'visible': [True, False, False, False]}, 
                         {'title': 'TOP 20 State Count'}]),
             
             dict(
                  label = 'City Count',
                 visible=True,
                 method = 'update',
                 args = [{'visible': [False, True, False, False]},
                     {'title': 'TOP 20 City Count'}]),

            dict(
                 label = 'Type Count',
                 method = 'update',
                 args = [{'visible': [False, False, True, False]},
                     {'title': 'Type Counts'}]),

            dict(
                 label = 'Place Count',
                 method = 'update',
                 args = [{'visible': [False, False, False, True]},
                     {'title': ' Top 20 Place Count'}])
        ]),
    )
])


layout = dict(title='The count of the principal Categorical Features <br>(Select from Dropdown)', 
              showlegend=False,
              updatemenus=updatemenus)

fig = dict(data=data, layout=layout)

iplot(fig)


# In[ ]:


df_features['ALand_div_1M'] = np.log(df_features['ALand'] / 1000000)


# ## Some boxplots of City's

# In[ ]:



trace1  = go.Box(
    x=df_features[df_features.city.isin(city_count[:15].index.values)]['city'],
    y=df_features[df_features.city.isin(city_count[:15].index.values)]['rent_median'], 
    showlegend=False, visible=True
)
                        
trace2  = go.Box(
    x=df_features[df_features.city.isin(city_count[:15].index.values)]['city'],
    y=df_features[df_features.city.isin(city_count[:15].index.values)]['family_median'], 
    showlegend=False, visible=False
)
                
trace3 = go.Box(
    x=df_features[df_features.city.isin(city_count[:15].index.values)]['city'],
    y=df_features[df_features.city.isin(city_count[:15].index.values)]['hi_median'],
    showlegend=False, visible=False
)

trace4 = go.Box(
    x=df_features[df_features.city.isin(city_count[:15].index.values)]['city'],
    y=df_features[df_features.city.isin(city_count[:15].index.values)]['hc_mortgage_mean'],
    showlegend=False, visible=False
)

data = [trace1, trace2, trace3, trace4]

updatemenus = list([
    dict(active=-1,
         x=-0.15,
         buttons=list([  
             
            dict(
                label = 'City Rent Boxplot',
                 method = 'update',
                 args = [{'visible': [True, False, False, False]}, 
                     {'title': 'TOP 15 Citys - Rent Median'}]),
             
             dict(
                  label = 'City Family Boxplot',
                 method = 'update',
                 args = [{'visible': [False, True, False, False]},
                     {'title': 'TOP 15 Citys - Family Income Median'}]),

            dict(
                 label = 'City House Inc',
                 method = 'update',
                 args = [{'visible': [False, False, True, False]},
                     {'title': 'TOP 15 Citys - House income Median'}]),

            dict(
                 label =  'City HC Mortage',
                 method = 'update',
                 args = [{'visible': [False, False, False, True]},
                     {'title': 'TOP 15 Citys - Home Cost Mortage'}])
        ]),
    )
])

layout = dict(title='Citys BoxPlots of Medians <br>(Select metrics from Dropdown)', 
              showlegend=False,
              updatemenus=updatemenus)

fig = dict(data=data, layout=layout)

iplot(fig, filename='dropdown')


# ## Another Approach to visualization of this same data

# In[ ]:


city_count = df_features.city.value_counts()

#First plot
trace0 = go.Box(
    x=df_features[df_features.city.isin(city_count[:10].index.values)]['city'],
    y=df_features[df_features.city.isin(city_count[:10].index.values)]['rent_median'], 
    showlegend=False
)

#Second plot
trace1 = go.Box(
    x=df_features[df_features.city.isin(city_count[:10].index.values)]['city'],
    y=df_features[df_features.city.isin(city_count[:10].index.values)]['family_median'], 
    showlegend=False
)

#Second plot
trace2 = go.Box(
    x=df_features[df_features.city.isin(city_count[:10].index.values)]['city'],
    y=df_features[df_features.city.isin(city_count[:10].index.values)]['hc_mortgage_median'], 
    showlegend=False
)

#Third plot
trace3 = go.Histogram(
    x=df_features[df_features.city.isin(city_count[:20].index.values)]['city'], histnorm='percent',
    showlegend=False
)
#Third plot
trace4 = go.Histogram(
    x=np.log(df_features['family_median']).sample(5000), histnorm='percent', autobinx=True,
    showlegend=True, name='Family'
)

#Third plot
trace5 = go.Histogram(
    x=np.log(df_features['hc_mortgage_median']).sample(5000), histnorm='percent', autobinx=True,
    showlegend=True, name='HC mort'
)

#Third plot
trace6 = go.Histogram(
    x=np.log(df_features['rent_median']).sample(5000), histnorm='percent', autobinx=True,
    showlegend=True, name="Rent"
)

#Creating the grid
fig = tls.make_subplots(rows=2, cols=3, specs=[[{'colspan': 2}, None, {}], [{}, {}, {}]],
                          subplot_titles=("Citys Count",
                                          "Medians Distribuition", 
                                          "HC Morttage Median",
                                          "Family Median", 
                                          "Rent Median"))

#setting the figs
fig.append_trace(trace0, 2, 1)
fig.append_trace(trace1, 2, 3)
fig.append_trace(trace2, 2, 2)
fig.append_trace(trace3, 1, 1)
fig.append_trace(trace4, 1, 3)
fig.append_trace(trace5, 1, 3)
fig.append_trace(trace6, 1, 3)

fig['layout'].update(showlegend=True, title="Some Top Citys Distribuitions")

iplot(fig)


# - How can I set space between the plots and also how to invert the x axis labels

# # Taking a look in box plots of some of this values

# In[ ]:



#First plot
trace0 = go.Box(
    x=df_features[df_features.city.isin(city_count[:10].index.values)]['city'],
    y=df_features[df_features.city.isin(city_count[:10].index.values)]['rent_median'], 
    showlegend=False
)

#Second plot
trace1 = go.Box(
    x=df_features[df_features.city.isin(city_count[:10].index.values)]['city'],
    y=df_features[df_features.city.isin(city_count[:10].index.values)]['family_median'], 
    showlegend=False
)

#Second plot
trace2 = go.Box(
    x=df_features[df_features.city.isin(city_count[:10].index.values)]['city'],
    y=df_features[df_features.city.isin(city_count[:10].index.values)]['hc_mortgage_median'], 
    showlegend=False
)

#Third plot
trace3 = go.Histogram(
    x=df_features[df_features.city.isin(city_count[:20].index.values)]['city'], histnorm='percent',
    showlegend=False
)

#Creating the grid
fig = tls.make_subplots(rows=2, cols=3, specs=[[{'colspan': 3}, None, None], [{}, {}, {}]],
                          subplot_titles=("City Count",
                                          "Rent Median by City",
                                          "HC Morttage Median by City",
                                          "Family Median by City"
                                          ))
#setting the figs
fig.append_trace(trace0, 2, 1)
fig.append_trace(trace1, 2, 3)
fig.append_trace(trace2, 2, 2)
fig.append_trace(trace3, 1, 1)

fig['layout'].update(showlegend=True, title="Some City Distribuitions")
iplot(fig)


# ## State by some numerical features

# In[ ]:



#First plot
trace0 = go.Box(
    x=df_features[df_features.state.isin(state_count[:10].index.values)]['state'],
    y=df_features[df_features.state.isin(state_count[:10].index.values)]['hs_degree'],
    name="Top 10 States", showlegend=False
)

#Second plot
trace1 = go.Box(
    x=df_features[df_features.state.isin(state_count[:10].index.values)]['state'],
    y=df_features[df_features.state.isin(state_count[:10].index.values)]['family_median'],
    name="Top 15 Sucessful", showlegend=False
)

#Third plot
trace2 = go.Histogram(
    x=df_features[df_features.place.isin(place_count[:20].index.values)]['place'],
    histnorm='percent', name="Top 20 Place's", showlegend=False             
)

#Creating the grid
fig = tls.make_subplots(rows=2, cols=2, specs=[[{}, {}], [{'colspan': 2}, None]],
                          subplot_titles=('HS Degree Median TOP 10 States',
                                          'Family Median TOP 10 States', 
                                          "Top 20 Most Frequent Places"))

#setting the figs
fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace2, 2, 1)

fig['layout'].update(showlegend=True, title="Top Frequency States")

iplot(fig)


# In[ ]:





# ## Old Plots that might I will erase and continue developing graphs with markdown
# 

# In[ ]:


#First plot
trace0 = go.Box(
    x=df_features['type'],
    y=df_features['rent_median'], 
    showlegend=False
)

#Second plot
trace1 = go.Box(
    x=df_features['type'],
    y=df_features['family_median'], 
    showlegend=False
)

#Second plot
trace2 = go.Histogram(
    x=df_features['type'], histnorm="percent", 
    showlegend=False
)

trace3 = go.Scatter(
    x=df_features['rent_median'], 
    y=df_features['family_median'],
    showlegend=False,
    mode = 'markers'
)

#Creating the grid
fig = tls.make_subplots(rows=2, cols=3, specs=[[{}, {}, {}], [{'colspan': 3}, None, None]],
                          subplot_titles=("Rent Median by Type",
                                          "Type Count",
                                          "Family Median by Type", 
                                          "Rent Median x Family Median"))

#setting the figs
fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 3)
fig.append_trace(trace2, 1, 2)
fig.append_trace(trace3, 2, 1)

fig['layout'].update(showlegend=True, 
                     title="Some Type Distribuitions")

iplot(fig)


# Cool. 
# 

# ## First Look in State Feature

# In[ ]:



#First plot
trace0 = go.Box(
    x=df_features[df_features.state.isin(state_count[:10].index.values)]['state'],
    y=df_features[df_features.state.isin(state_count[:10].index.values)]['rent_median'],
    name="Top 10 States", showlegend=False
)

#Second plot
trace1 = go.Box(
    x=df_features[df_features.state.isin(state_count[:10].index.values)]['state'],
    y=df_features[df_features.state.isin(state_count[:10].index.values)]['hc_mortgage_median'],
    name="Top 15 Sucessful", showlegend=False
)

#Third plot
trace2 = go.Histogram(
    x=df_features[df_features.state.isin(state_count[:20].index.values)]['state'],
    histnorm='percent', name="Top 20 States's", showlegend=False             
)

#Creating the grid
fig = tls.make_subplots(rows=2, cols=2, specs=[[{}, {}], [{'colspan': 2}, None]],
                          subplot_titles=('Rent Median TOP 10 States',
                                          'Mortage Median TOP 10 States', 
                                          "Top 20 Most Frequent States"))

#setting the figs
fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace2, 2, 1)

fig['layout'].update(showlegend=True, title="Top Frequency States")

iplot(fig)


# <h1>Looking the distribuition of Numerical values </h1>

# In[ ]:


cat_feat = df_features.loc[:, df_features.dtypes == object].columns
num_feat = df_features.loc[:, df_features.dtypes != object].columns


# ## Please votes up my kernel and stay tuned in my kernel. 

# In[ ]:


female_male  = ['hs_degree', 'hs_degree_male', 'hs_degree_female', 'male_age_mean',
                'male_age_median', 'male_age_stdev', 'male_age_sample_weight',
                'male_age_samples', 'female_age_mean', 'female_age_median',
                'female_age_stdev', 'female_age_sample_weight', 'female_age_samples']


# In[ ]:




