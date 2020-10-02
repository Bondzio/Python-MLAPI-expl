#!/usr/bin/env python
# coding: utf-8

# **Objectives** : 
# display the sum of awards by country, given to directors + discover chloropleth maps
# 
# **Sources & methodology** : Awards scrapped from imdb for 90 000 directors (30 000 directors actually have at least one award). Then I use the majoritary language of their filmography as a proxy nationality, which causes a few issues, mainly that is projects all english (resp. french) speaking directors to USA (resp. France). Also a director may change nationality over time. Last but not least, there are a few issues of data quality on tmdb.org on languages but overall nothing game breaking. It mostly succeed in showing anglo-saxon hegemony, then with a cluster of french, italian, german and japanese movie directors (not surprising)

# In[ ]:


import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Load misc files & join them
df_awards = pd.read_csv("../input/350-000-movies-from-themoviedborg/220k_awards_by_directors.csv", sep=",")
df_language = pd.read_csv("../input/350-000-movies-from-themoviedborg/MostCommonLanguageByDirector.csv", sep=",",encoding="utf-8")
df_lantocou = pd.read_csv("../input/350-000-movies-from-themoviedborg/language to country.csv", sep=";",encoding="utf-8")
df_language.rename(columns={"original_language": "Language"},inplace=True)
df = pd.merge(df_awards, df_language, on='director_name').drop("nb",axis=1)
df=df.merge(df_lantocou,on="Language")

#Assign weights for outcome for final scoring
di = {'Won': 2, 'Nominated': 1,'2nd place':1,'3rd place':1}
df=df.replace({"outcome": di})


# In[ ]:


#Display "countries w/ most awards"
df_disp = df.loc[:, ('Country','outcome')].groupby('Country').sum()
df_disp.reset_index(inplace=True)
df_disp.sort_values(by="outcome",ascending=False,inplace=True)
df_disp[:10]


# USA dpo

# In[ ]:


# Show distribution of awards except excluding top scorer (usually US + country of origin of award)
plt.hist(df_disp[df_disp['outcome']<120]['outcome'])
plt.xlabel("Award scoring")
plt.ylabel("# of countries")
plt.title("Distribution of countries by award total scoring (excluding USA)")
plt.show()


# In[ ]:


#Add countries with no awards
df_countries = pd.read_csv('../input/list-of-all-countries-iso-codes/2014_world_gdp_with_codes.csv')
df_countries.rename(columns={"CODE": "Country"},inplace=True)
df_disp=df_disp.merge(df_countries,on="Country",how="outer")
df_disp.fillna(0,inplace=True)


# # Create Chloropleth map with plotly

# In[ ]:


import plotly.offline as py
py.init_notebook_mode()
import pandas as pd

data = [ dict(
        type = 'choropleth',
    locations = df_disp['Country'],
    z = df_disp['outcome'],
        colorscale = [[0,"red"],[1,"white"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 1
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = 'Score=',
            title = 'Awards density by country'),
      ) ]

layout = dict(
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False)

