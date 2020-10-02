#!/usr/bin/env python
# coding: utf-8

# # Covid 19 Death / Confirmed EDA

# I realized this EDA while being inspired by the 2 notebooks:
# 
# https://www.kaggle.com/imdevskp/covid-19-analysis-visualization-comparisons
# 
# https://www.kaggle.com/vanshjatana/analysis-and-prediction-on-coronavirus-italy
# 
# which proposes a method of in-depth analysis of the evolution of the virus.
# 
# I downloaded the data from the site:
# 
# https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
# 
# which updates the evolution of the epidemic every day in all the countries of the world

# # library

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from IPython.display import display
import tqdm
from IPython.core.display import HTML
import plotly.offline as py

sns.set(rc={'figure.figsize':(11.7,8.27)})

import warnings
warnings.filterwarnings('ignore')

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# # Dataset

# In[ ]:


Data = pd.read_excel('../input/covid19geographic/COVID-19-geographic-disbtribution-worldwide-2020-04-08.xlsx')


# In[ ]:


display(Data.head(5))
display(Data.describe())
print("Number of Country_Region: ", Data['countriesAndTerritories'].nunique())
print("Dates go from day", min(Data['dateRep']), "to day", max(Data['dateRep']), ", a total of", Data['dateRep'].nunique(), "days")
print("Number total of Deaths", Data['deaths'].sum())
print("Number total of Cases", Data['cases'].sum())


# # increased Cases / Deaths

# ## Global increase Cases / Deaths

# In[ ]:


fig = px.line(pd.melt(Data, id_vars=['dateRep'], value_vars=['cases', 'deaths']).groupby(['dateRep', 'variable']).sum().reset_index(),
              x='dateRep',  y="value", color = 'variable',
             title='Daily increase Death / Cases',
             labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count'},)
fig.update_layout(hovermode="x")
fig.show()


# ## Increased Cases for each Country

# In[ ]:


# sns.lineplot(x="dateRep", y="cases", hue="countriesAndTerritories", data=Data)

fig = px.line(Data, x="dateRep", y="cases", color='countriesAndTerritories', title='Daily increase Cases by Country',
             labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count'},)
fig.show()


# ## Increased Deaths for each Country

# In[ ]:


fig = px.line(Data, x="dateRep", y="deaths", color='countriesAndTerritories', title='Daily increase Deaths by Country',
             labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count'},)
fig.show()


# # Data Preprocess

# In[ ]:


Data.sort_values(by=['dateRep'], inplace = True)

Data['total_cases'] = Data['cases'].cumsum()
Data['total_deaths'] = Data['deaths'].cumsum()

Data['total_cases_ByCountry'] = Data.groupby(['countriesAndTerritories'])['cases'].cumsum()
Data['total_deaths_ByCountry'] = Data.groupby(['countriesAndTerritories'])['deaths'].cumsum()


display(Data.head())
display(Data.tail())


# # Expansion of Cases / Deaths

# ## Global Expansion of Cases / Deaths

# In[ ]:


fig = px.line(pd.melt(Data, id_vars=['dateRep'], value_vars=['total_cases', 'total_deaths']).groupby(['dateRep', 'variable']).max().reset_index(),
              x='dateRep',  y="value", color = 'variable',
             title='Cummulated Death / Cases',
              labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                      'cases_cumsum' : 'Cases', 
                      'deaths_cumsum': 'Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count'},)
fig.update_layout(hovermode="x")
fig.show()


# ## expanding Cases for each Country

# In[ ]:


fig = px.line(Data, x="dateRep", y="total_cases_ByCountry", color='countriesAndTerritories', title='Cummulated Cases by Country',
              labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                      'cases_cumsum' : 'Cases', 
                      'deaths_cumsum': 'Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count'},)
fig.show()


# ## expanding Deaths for each Country

# In[ ]:


fig = px.line(Data, x="dateRep", y="total_deaths_ByCountry", color='countriesAndTerritories', title='Cummulated Cases by Country',
              labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                      'cases_cumsum' : 'Cases', 
                      'deaths_cumsum': 'Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count'},)
fig.show()


# # Data Preprocess

# In[ ]:


Data['total_Cases_log10'] = np.log10(np.where(Data['total_cases']<=0 , 1, Data['total_cases']))
Data['total_Deaths_log10'] = np.log10(np.where(Data['total_deaths']<=0 , 1,Data['total_deaths']))

Data['total_Cases_ByCountry_log10'] = np.log10(np.where(Data['total_Cases_log10']<=0 , 1,Data['total_cases_ByCountry']))
Data['total_Death_ByCountry_log10'] = np.log10(np.where(Data['total_Deaths_log10']<=0 , 1,Data['total_deaths_ByCountry']))

display(Data.head())
display(Data.tail())


# # Log10 Expansion of Cases / Deaths

# I applied Log10 on the expenssion to reduce the significant differences in deaths and cases between the most affected and least affected countries.
# 
# This reduction will serve to better perceive the evolution of cases and deaths and to be able to find a possible relationship between them.

# ## Log10 Global Expansion of Cases / Deaths

# In[ ]:


fig = px.line(pd.melt(Data, id_vars=['dateRep'], value_vars=['total_Cases_log10', 'total_Deaths_log10']).groupby(['dateRep', 'variable']).max().reset_index(),
              x='dateRep',  y="value", color = 'variable',
             title='Log Cummulated Death / Cases World',
             labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                      'cases_cumsum' : 'Cases', 
                      'deaths_cumsum': 'Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count (Log10)'},)
fig.update_layout(hovermode="x")
fig.show()


# ## Log10 Expanding Cases for each Country

# In[ ]:


fig = px.line(Data, x="dateRep", y="total_Cases_ByCountry_log10", color='countriesAndTerritories', title='Log Cummulated Cases by Country',
             labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                      'cases_cumsum' : 'Cases', 
                      'deaths_cumsum': 'Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count (Log10)'},)
fig.show()


# ## Log10 Expanding Death for each Country

# In[ ]:


fig = px.line(Data, x="dateRep", y="total_Death_ByCountry_log10", color='countriesAndTerritories', title='Log Cummulated Deaths by Country',
              labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                      'cases_cumsum' : 'Cases', 
                      'deaths_cumsum': 'Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count (Log10)'},)
fig.show()


# # Total Cases / Deaths for each Country

# ## Total Cases for each Country

# In[ ]:


fig = px.pie(Data.groupby(['countriesAndTerritories']).max().reset_index(), values='total_cases_ByCountry', names='countriesAndTerritories', title='Total Cases by Country',
             labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                      'cases_cumsum' : 'Cases', 
                      'deaths_cumsum': 'Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count (Log10)'},)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()


# ## Total Deaths for each Country

# In[ ]:


fig = px.pie(Data.groupby(['countriesAndTerritories']).max().reset_index(), values='total_deaths_ByCountry', names='countriesAndTerritories', title='Total Deaths by Country',
            labels={'deaths_cumsum_ByCountry':'COVID 19 Total Deaths',
                      'cases_cumsum' : 'Cases', 
                      'deaths_cumsum': 'Deaths',
                     'variable' : 'Eolution',
                     'dateRep_usa': 'Date',
                     'dateRep': 'Date',
                     'countriesAndTerritories' : 'Country',
                     'countryterritoryCode': 'Country code',
                     'value' : 'Count (Log10)'},)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()


# # Current deaths / cases around the world

# ## Current cases around the world

# In[ ]:


country_geo = '../input/worldcountries/world-countries'

m = folium.Map(location=[40, 40], zoom_start=2)

folium.Choropleth(
    geo_data=country_geo,
    name='choropleth',
    data=Data.groupby(['countryterritoryCode']).max().reset_index(),
    columns=['countryterritoryCode', 'total_cases_ByCountry'],
    key_on='feature.id',
    fill_color='YlOrRd',
#     fill_opacity=0.7,
#     line_opacity=0.2,
    popup='cases_cumsum_ByCountry',
    nan_fill_color='white',
    legend_name='COVID 19 Total Cases'
).add_to(m)

folium.LayerControl().add_to(m)

display(m)


# ## Current deaths around the world

# In[ ]:


m = folium.Map(location=[40, 40], zoom_start=2)

folium.Choropleth(
    geo_data=country_geo,
    name='choropleth',
    data=Data.groupby(['countryterritoryCode']).max().reset_index(),
    columns=['countryterritoryCode', 'total_deaths_ByCountry'],
    key_on='feature.id',
    fill_color='YlOrRd',
#     fill_opacity=0.7,
#     line_opacity=0.2,
    nan_fill_color='white',
    legend_name='COVID 19 Total Deaths'
).add_to(m)

folium.LayerControl().add_to(m)

display(m)


# # Data Preprocess

# In[ ]:


def reindex_by_date(df):
    dates = pd.date_range(df.index.min(), df.index.max())
    return df.reindex(dates).bfill()

appended_data = []

for i in Data['countryterritoryCode'].unique():
    tmp = Data[Data['countryterritoryCode'] == i].groupby(['dateRep']).max().apply(reindex_by_date).reset_index().copy()
    appended_data.append(tmp)

Data_new = pd.concat(appended_data)
Data_new['dateRep_usa'] = Data_new['index'].dt.strftime('%m/%d/%Y')


# ## Deaths / cases ratio for each country

# In[ ]:


x = Data_new.groupby(['dateRep_usa', 'countryterritoryCode']).max().reset_index()['dateRep_usa'].max()

fig = px.scatter(Data_new.groupby(['dateRep_usa', 'countryterritoryCode']).max().reset_index()[
                (Data_new.groupby(['dateRep_usa', 'countryterritoryCode']).max().reset_index()['total_cases_ByCountry'] > 0)&
                (Data_new.groupby(['dateRep_usa', 'countryterritoryCode']).max().reset_index()['index'] == Data_new['index'].max())], 
                 x='total_cases_ByCountry', y='total_deaths_ByCountry', color='countryterritoryCode', size='total_Cases_ByCountry_log10', height=700,
                 text='countriesAndTerritories', log_x=True, log_y=True, title='Deaths vs Cases (Scale is in log10)',
                 labels={'cases_cumsum_ByCountry':'COVID 19 Total Cases',
                                  'dateRep_usa': 'Date',
                                  'countriesAndTerritories' : 'Country',
                                  'countryterritoryCode': 'Country code'},
                )
fig.update_traces(textposition='top center')
fig.update_layout(showlegend=False)
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()


# # Evolution of Deaths / Cases worldwide

# ## Evolution of Cases Worldwide

# In[ ]:


data_tmp1 = Data_new.groupby(['dateRep_usa', 'countryterritoryCode']).max().reset_index()[Data_new.groupby(['dateRep_usa', 'countryterritoryCode']).max().reset_index()['total_cases_ByCountry'] > 0].sort_values(by=['dateRep_usa'])
data_tmp2 = Data_new.groupby(['dateRep_usa', 'countryterritoryCode']).max().reset_index()[Data_new.groupby(['dateRep_usa', 'countryterritoryCode']).max().reset_index()['total_deaths_ByCountry'] > 0].sort_values(by=['dateRep_usa'])
data_tmp1['countriesAndTerritories2'] = data_tmp1['countriesAndTerritories'].str.replace('_', ' ')
data_tmp2['countriesAndTerritories2'] = data_tmp2['countriesAndTerritories'].str.replace('_', ' ')


max1 = Data.groupby(['countryterritoryCode', 'dateRep']).max().reset_index()['total_cases_ByCountry'].max()
max2 = Data.groupby(['countryterritoryCode', 'dateRep']).max().reset_index()['total_deaths_ByCountry'].max()


# In[ ]:


fig = px.choropleth(data_tmp1, locations="countriesAndTerritories2", locationmode='country names', 
                     color="total_cases_ByCountry", 
                     hover_name="countriesAndTerritories2",
                     hover_data = ['countriesAndTerritories','dateRep_usa'],
                     projection="mercator",
                     animation_frame="dateRep_usa",
                     color_continuous_scale='Sunsetdark',
                     range_color=[0,max1],
                     labels={'total_cases_ByCountry':'COVID 19 Total Cases',
                          'dateRep_usa': 'Date',
                          'countriesAndTerritories' : 'Country',
                          'countryterritoryCode': 'Country code'},
                     title='Evolution of Cases Worldwide',
                   width=1500, height=700,)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update(layout_coloraxis_showscale=True)
py.offline.iplot(fig)


# ## Evolution of deaths worldwide

# In[ ]:


fig = px.choropleth(data_tmp2, locations="countriesAndTerritories2", locationmode='country names', 
                     color="total_deaths_ByCountry", 
                     hover_name="countriesAndTerritories2",
                     hover_data = ['countriesAndTerritories','dateRep_usa'],
                     projection="mercator",
                     animation_frame="dateRep_usa",
                     color_continuous_scale='Sunsetdark',
                     range_color=[0,max2],
                     labels={'total_cases_ByCountry':'COVID 19 Total Cases',
                          'dateRep_usa': 'Date',
                          'countriesAndTerritories' : 'Country',
                          'countryterritoryCode': 'Country code'},
                     title='Evolution of deaths worldwide',
                   width=1500, height=700,)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update(layout_coloraxis_showscale=True)
py.offline.iplot(fig)


# https://app.flourish.studio/visualisation/1571387/edit

# In[ ]:


HTML('''<div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/1571387"><script src="https://public.flourish.studio/resources/embed.js"></script></div>''')


# <h1 style="color:red;"> ================= UPVOTE IF YOU ENJOY IT =) =================</h1> <br /> <br />
# 
# 
# 

# ![pic2.jpg](attachment:pic2.jpg)
