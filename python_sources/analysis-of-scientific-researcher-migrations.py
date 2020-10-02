#!/usr/bin/env python
# coding: utf-8

# # Plotting immigration maps of countries
# In this notebook I will use the data from the Scientific Researcher Migrations dataset and additional geographical data from the Counties geographic coordinates dataset in order to plot a map describing the scientist immigration from and to a certain country.

# In[ ]:



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib.pyplot as plt # plotting
from mpl_toolkits.basemap import Basemap # map plotting
import seaborn as sbs # pretty plotting
import matplotlib as mpl # plotting settings

mpl.rcParams['figure.figsize'] = (10,10)


# In[ ]:


df = pd.read_csv("../input/scientist-migrations/ORCID_migrations_2016_12_16_by_person.csv", index_col="orcid_id")
df.head()


# Lets check out who has the most registered sceintists:

# In[ ]:


most = df.groupby("earliest_country").count().sort_values(by="has_migrated", ascending=False).head(20)
most["earliest_country"] = most.index
plt.title("Number of scientists originating in a given country", fontsize=20)
sbs.barplot(x="earliest_country", y="has_migrated", data=most)
plt.ylabel('# Scientists', fontsize=10)
plt.xlabel('Country code', fontsize=10)


# And let us check out which country draws the most scientists in 2016:

# In[ ]:


most = df.groupby("country_2016").count().sort_values(by="has_migrated", ascending=False).head(20)
most["country_2016"] = most.index
plt.title("Number of scientists working in a given country in 2016", fontsize=20)
sbs.barplot(x="country_2016", y="has_migrated", data=most)
plt.ylabel('# Scientists', fontsize=10)
plt.xlabel('Country code', fontsize=10)


# We create a matrix from the rows which has both an earliest_country value and a country_2016 value. The matrix at index (i,j) will store the number of scientists from country i working in country j in 2016.
# 
# We will also create a data set from this matrix.

# In[ ]:


migrators = df[["earliest_country","country_2016"]].dropna(axis=0,how="any")
countries = set(migrators["country_2016"].unique()) | set(migrators["earliest_country"].unique())
countries = sorted(countries)
migration_matrix = np.zeros((len(countries), len(countries)), dtype=int)
for index, row in migrators.iterrows():
    src_index = countries.index(row["earliest_country"])
    dst_index = countries.index(row["country_2016"])
    migration_matrix[src_index,dst_index] += 1
df_migrations = pd.DataFrame(migration_matrix, index=countries, columns=countries)
stayed = migration_matrix.trace()


# In[ ]:


df_migrations.describe()[["US","RU","CN"]]


# The transposed dataset will show the reverse process.

# In[ ]:


df_migrations.transpose().describe()[["US","RU","CN"]]


# The countries losing the most scientists:

# In[ ]:


incoming_minus_outgoing = df_migrations.sum(axis=0) - df_migrations.sum(axis=1)
most = np.abs(incoming_minus_outgoing.sort_values().head(10))
plt.title("Scientist loss per country")
most.plot.bar()


# The countries losing the most scientists:

# In[ ]:


incoming_minus_outgoing = df_migrations.sum(axis=0) - df_migrations.sum(axis=1)
most = np.abs(incoming_minus_outgoing.sort_values(ascending=False).head(10))
plt.title("Scientist gain per country")
most.plot.bar()


# Lets load the country geo locations:

# In[ ]:


countries_df = pd.read_csv("../input/counties-geographic-coordinates/countries.csv", index_col="country")
countries_df = countries_df[countries_df.index != "UM"]
countries_df.head()


# This function will draw a simple line between two countries, with the width of the line depending on immegration size, and the color on immegration direction.

# In[ ]:


def draw_country_line(c1,c2,min_delta, brush_factor, neg_color='r', pos_color='b'):
    if c2 not in countries_df.index:
        return
    delta = df_migrations[c1][c2] - df_migrations[c2][c1]
    if abs(delta) < min_delta:
        return
    x = (countries_df["longitude"][c1],countries_df["longitude"][c2])
    y = (countries_df["latitude"][c1],countries_df["latitude"][c2])
    color = pos_color if delta > 0 else neg_color
    worldmap.plot(x,y,latlon=True,linewidth=delta*brush_factor,color=color)


# Lets see the lines without directions on the whole world

# In[ ]:


plt.figure(figsize=(20,10))
worldmap = Basemap()
worldmap.drawcoastlines()
worldmap.drawcountries()
worldmap.fillcontinents()
for i,c1 in enumerate(countries):
    for c2 in countries[i+1:]:
        draw_country_line(c1,c2,100,0.001,'g','g')
plt.title("Immigration Map")
plt.show()


# This function plots a map for a specific country, Lets use it on Israel!

# In[ ]:


def plot_country_immigration_map(c1,min_delta, brush_factor):
    plt.figure(figsize=(20,10))
    worldmap = Basemap()
    worldmap.drawcoastlines()
    worldmap.drawcountries()
    worldmap.fillcontinents()
    for c2 in countries:
        draw_country_line(c1,c2, min_delta, brush_factor)
    plt.title(countries_df["name"][c1] + " Immigration Map")
    plt.show()
    
plot_country_immigration_map("IL",1,0.2)


# Well seems like we get we lose a lot of scientists to the USA and the EU, but we also accept a lot of scientists from India and Russia.
# 
# How does it look for other countries ?

# In[ ]:


plot_country_immigration_map("US", 1, 0.005)


# In[ ]:


plot_country_immigration_map("CN", 1, 0.005)


# Man... China has to work on it's scienctist retention...

# In[ ]:


plot_country_immigration_map("GB", 1, 0.01)


# In[ ]:


plot_country_immigration_map("IN", 1, 0.01)

