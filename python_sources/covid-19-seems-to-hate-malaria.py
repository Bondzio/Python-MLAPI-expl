#!/usr/bin/env python
# coding: utf-8

# # COVID-19 Seems to Hate Malaria.

# COronaVIrus Disease 2019 (COVID-19) was first reported in December 2019, and has now engulfed and locked down the entire world.
# 
# Malaria is an old and life threatening pathogenic disease, which still exits in spite of aggressive efforts.
# 
# This notebook compares the known numbers of cases of and deaths due to Covid-19 to the known numbers of deaths due to malaria.
# 
# The notebook finds that while malaria is present almost everywhere and Covid-19 is entering almost everywhere, the overall presence of Covid-19 is less noticeable in regions known for malaria.
# 
# It is as if Covid-19 seems to hate malaria.
# 
# Based on this finding, I am inclined to speculate that people who have had some malaria medicine (such as [quinine](https://en.wikipedia.org/wiki/Quinine)) and regions which have had spray of some mosquito killer (such as [DDT](https://en.wikipedia.org/wiki/DDT)) are less likely to get Covid-19.

# ### Packages and Files Used

# In[ ]:


from __future__ import print_function
import os
import pandas as pd
import datetime as dt
import json
import plotly.express as px
from urllib.request import urlopen
from IPython.core.display import display, HTML


# In[ ]:


zfic = '../input/covid19-and-malaria/Covid_World_Daily.csv'
zfim = '../input/covid19-and-malaria/Malaria_World.csv'
zfip = '../input/covid19-and-malaria/Population_World.csv'
zurl = 'https://raw.githubusercontent.com/jupyter-widgets/ipyleaflet/master/examples/countries.geo.json'


# ### Covid-19 Dataframe
# 
# Prepare dataframes of Covid-19 cases and deaths, keep relevant columns, and add cumulative sums.

# In[ ]:


dfc1 = pd.read_csv(zfic, encoding='latin-1')
# dfc1.head(1)
dfc2 = dfc1[['countryterritoryCode','countriesAndTerritories','popData2018','dateRep','cases','deaths']]
dfc2 = dfc2.groupby(by=['countryterritoryCode','countriesAndTerritories','popData2018','dateRep']
                   ).sum().groupby(level=[0]).cumsum()
dfc2 = dfc2.reset_index()
# dfc2.head(1)
dfc2.columns = ['Code','Name','Population','Date','Covid_C','Covid_D']
dfc2.head(1)


# In[ ]:


dfc3 = dfc2[['Date']].groupby(by=['Date']).count()
dfc3 = dfc3.reset_index()
dfc3['Date'] = pd.to_datetime(dfc3['Date'])
dfc3 = dfc3.sort_values(by=['Date'], ascending=False)
dfc3.head(2)


# ### Malaria Dataframe
# 
# Prepare a dataframe of malaria deaths and population, merge them, and keep relevant columns.

# In[ ]:


dfm1 = pd.read_csv(zfim, encoding='latin-1')
# dfm1.head(1)
dfp1 = pd.read_csv(zfip, encoding='latin-1')
# dfp1.head(1)
dfm1 = pd.merge(dfm1, dfp1, on='Code', how='left', indicator=False)
# dfm1.head(1)
dfm1 = dfm1[['Code','Country_x','Population_2020','Deaths_2010']]
dfm1.columns = ['Code','Name','Population','Malaria_D']
dfm1 = dfm1.dropna()
dfm1.head(1)


# ### Correlation of Covid-19 and Malaria (Deaths per Million Population)
# 
# Merge covid-19 and malaria dataframes, and evaluate correlation between covid and malaria.

# In[ ]:


def pickOne(arr):
    b = "0"
    for c in arr:
        if str(c) > str(b):
            b = c
    return str(b)

def perPop(j,k):
    return int(1000000 * float(j) / float(k))


# In[ ]:


dfcm1 = pd.merge(dfc2, dfm1, on=['Code'], how='outer', indicator=False)
dfcm1 = dfcm1.fillna(0)
# dfcm1.head(1)

dfcm1['Name'] = dfcm1.apply(lambda x: pickOne([x.Name_x, x.Name_y]), axis=1)
dfcm1['Population'] = dfcm1.apply(lambda x: pickOne([x.Population_x, x.Population_y]), axis=1)
dfcm1['Covid_CP'] = dfcm1.apply(lambda x: perPop(x.Covid_C, x.Population), axis=1)
dfcm1['Covid_DP'] = dfcm1.apply(lambda x: perPop(x.Covid_D, x.Population), axis=1)
dfcm1['Malaria_DP'] = dfcm1.apply(lambda x: perPop(x.Malaria_D, x.Population), axis=1)

dfcm1['aCfMf'] = dfcm1.apply(lambda x: (x.Covid_DP<1) & (x.Malaria_DP<11), axis=1)
dfcm1['aCfMt'] = dfcm1.apply(lambda x: (x.Covid_DP<1) & (x.Malaria_DP>10), axis=1)
dfcm1['aCtMf'] = dfcm1.apply(lambda x: (x.Covid_DP>0) & (x.Malaria_DP<11), axis=1)
dfcm1['aCtMt'] = dfcm1.apply(lambda x: (x.Covid_DP>0) & (x.Malaria_DP>10), axis=1)

dfcm1 = dfcm1[['Code','Name','Date','Covid_C','Covid_D','Malaria_D',
               'Covid_CP','Covid_DP','Malaria_DP','aCfMf','aCfMt','aCtMf','aCtMt']]
dfcm1 = dfcm1.sort_values(by=['Malaria_D'], ascending=False)
dfcm1.head(1)


# In[ ]:


dfcm2 = dfcm1[['Date','aCfMf','aCfMt','aCtMf','aCtMt','Covid_D','Malaria_D']].groupby(['Date']).sum()
dfcm2 = dfcm2.reset_index()
dfcm2 = dfcm2.iloc[1:]
dfcm2['Date'] = pd.to_datetime(dfcm2['Date'])
dfcm2 = dfcm2.sort_values(by=['Date'], ascending=False)
dfcm2.head(1)


# In[ ]:


dfcm2['CfMf'] = dfcm2.apply(lambda x: int(100 * x.aCfMf / (x.aCfMf + x.aCfMt + x.aCtMf + x.aCtMt)), axis=1)
dfcm2['CfMt'] = dfcm2.apply(lambda x: int(100 * x.aCfMt / (x.aCfMf + x.aCfMt + x.aCtMf + x.aCtMt)), axis=1)
dfcm2['CtMf'] = dfcm2.apply(lambda x: int(100 * x.aCtMf / (x.aCfMf + x.aCfMt + x.aCtMf + x.aCtMt)), axis=1)
dfcm2['CtMt'] = dfcm2.apply(lambda x: int(100 - x.CfMf - x.CfMt - x.CtMf), axis=1)
dfcm3 = dfcm2[['Date','CfMf','CfMt','CtMf','CtMt']]
dfcm3.head(1)


# ### Plot the Correlation as a Colored Table

# In[ ]:


a = ["","","",""]
b = ["","","",""]
for i in range(4):      
    try:
        v = dfcm3.iloc[1,i+1]
    except:
        v = 0
    try:
        w = dfcm3.iloc[90,i+1]
    except:
        w = 0
    a[i] = "<td style='background-color:rgb("
    a[i] = a[i] + str(int(255)) +","
    a[i] = a[i] + str(int(255-v)) +","
    a[i] = a[i] + str(int(255-2*v))
    a[i] = a[i] + ")'>" + str(v) + "</td>"
    b[i] = "<td style='background-color:rgb("
    b[i] = b[i] + str(int(255)) +","
    b[i] = b[i] + str(int(255-w)) +","
    b[i] = b[i] + str(int(255-2*w))
    b[i] = b[i] + ")'>" + str(w) + "</td>"    
    
zhtm = "<html><body>"
zhtm = zhtm + "<table><col width='500'><col width='500'>"
zhtm = zhtm + "<tr><td>"
zhtm = zhtm + "<table><col width='200'><col width='150'><col width='150'>"
zhtm = zhtm + "<tr><td><h2>" + str(dfcm3.iloc[1,0])[:10] + "</h2></td><th >No_Covid</th><th>With_Covid</th></tr>"
zhtm = zhtm + "<tr><th>No_Malaria</th>" + a[0] + a[2] + "</tr>"
zhtm = zhtm + "<tr><th>With_Malaria</th>" + a[1] + a[3] + "</tr></table>"
zhtm = zhtm + "</td><td>"
zhtm = zhtm + "<table><col width='200'><col width='150'><col width='150'>"
zhtm = zhtm + "<tr><td><h2>" + str(dfcm3.iloc[90,0])[:10] + "</h2></td><th >No_Covid</th><th>With_Covid</th></tr>"
zhtm = zhtm + "<tr><th>No_Malaria</th>" + b[0] + b[2] + "</tr>"
zhtm = zhtm + "<tr><th>With_Malaria</th>" + b[1] + b[3] + "</tr></table>"
zhtm = zhtm + "</tr></table>"
zhtm = zhtm + "</body></html>"
    
display(HTML(zhtm))


# ### Plot Data on the World Map
# 
# - Load an available geo-jason file for the world.
# - Prepare a dataframe of malaria deaths for alls ids (as included in the geo-jason), and map it on the world map.
# - Prepare a dataframe of covid-19 deaths for all ids for a beginning date, and map it on the world map.
# - Prepare a dataframe of covid-19 deaths for all ids for a later date, and map it on the world map.

# In[ ]:


with urlopen(zurl) as resp:
    zjso = json.loads(resp.read().decode('utf-8'))
    
zids = []
for zloc in zjso['features']:
    zids.append([zloc['id']])
zids = pd.DataFrame(data=zids, columns=['Code'])
# zids.head(3)

maps = ["","",""]
dats = ['2019','2020-01-31','2020-03-31']
labs = ["Malaria deaths per million up to 2019", "Covid-19 cases per million up to 2020-01-31", "Covid-19 cases per million up to 2020-03-31"]


# In[ ]:


dfm2 = dfm1
dfm2['Malaria_DP'] = dfm2.apply(lambda x: perPop(x.Malaria_D, x.Population), axis=1)
dfm2 = pd.merge(zids, dfm1[['Code','Malaria_DP']], on=['Code'], how='left', indicator=False)
dfm2 = dfm2.fillna(0)

for i in [0]:
    
    maps[i] = px.choropleth_mapbox(dfm2,
                                   geojson=zjso,
                                   locations='Code',
                                   color='Malaria_DP',
                                   color_continuous_scale="OrRd",
                                   range_color=(0,12),
                                   mapbox_style="carto-positron",
                                   zoom=1,
                                   center = {"lat":0,"lon":0},
                                   opacity=0.5,
                                   labels={'Malaria_DP':'Malaria'})
    
    maps[i].update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# In[ ]:


dfc4 = dfc2[['Date','Code','Population','Covid_C']]
dfc4['Date'] = pd.to_datetime(dfc4['Date'])
dfc4['Covid_CP'] = dfc4.apply(lambda x: perPop(x.Covid_C, x.Population), axis=1)

for i in [1,2]:
    
    dfc5 = dfc4.loc[dfc4['Date']==dats[i], ['Code','Covid_CP']]
    dfc5['Covid_CP'] = dfc5['Covid_CP'].astype(float)
    dfc6 = pd.merge(zids, dfc5[['Code','Covid_CP']], on=['Code'], how='left', indicator=False)
    dfc6 = dfc6.fillna(0)
    
    maps[i] = px.choropleth_mapbox(dfc6,
                                   geojson=zjso,
                                   locations='Code',
                                   color='Covid_CP',
                                   color_continuous_scale="OrRd",
                                   range_color=(0,12),
                                   mapbox_style="carto-positron",
                                   zoom=1,
                                   center = {"lat":0,"lon":0},
                                   opacity=0.5,
                                   labels={'Covid_CP':'Covid-19'})
    
    maps[i].update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# In[ ]:


print(labs[0])


# In[ ]:


maps[0]


# In[ ]:


print(labs[1])


# In[ ]:


maps[1]


# In[ ]:


print(labs[2])


# In[ ]:


maps[2]


# ### Conclusion

# - In January 2020, there was almsot no region with both malaria and Covid-19.
# - In later period, there are a regions with both malaria and Covid-19.
# - In later period, the number of regions with both malaria and Covid-19 is not significant.
# - This implies that while malaria is present almost everywhere and Covid-19 is entering almost everywhere, the overall presence of Covid-19 is less noticeable in regions known for malaria.
# - Based on this finding, I am inclined to speculate that people who have had some malaria medicine (such as [quinine](https://en.wikipedia.org/wiki/Quinine)) and regions which have had spray of some mosquito killer (such as [DDT](https://en.wikipedia.org/wiki/DDT)) are less likely to get Covid-19.

# ### References

# GovCDC: https://www.cdc.gov/coronavirus/2019-nCoV/index.html
# 
# GovWHOCovid: https://www.who.int/health-topics/coronavirus
# 
# GovWHOMalaria: https://www.who.int/news-room/fact-sheets/detail/malaria
# 
# EduHarvard: https://dataverse.harvard.edu/file.xhtml
# 
# EduStanford: https://library.stanford.edu/research/stanford-geospatial-center
# 
# OrgWikiCovid: https://en.wikipedia.org/wiki/Coronavirus_disease_2019
# 
# OrgWikiMalaria: https://en.wikipedia.org/wiki/Malaria
# 
# OrgHopkinsM: https://www.hopkinsmedicine.org/coronavirus/
# 
# OrgNPR: https://www.npr.org/sections/goatsandsoda/2020/01/23/798632253/map-confirmed-cases-of-wuhan-coronavirus
# 
# OrgEndMal: https://endmalaria.org/about-malaria/key-facts
# 
# InfoWorldoM: https://www.worldometers.info/coronavirus/#countries
# 
# ComNaturalE: https://www.naturalearthdata.com/
