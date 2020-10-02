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


# *About
# Golden Globe Awards, any of the awards presented annually by the Hollywood Foreign Press Association (HFPA) in recognition of outstanding achievement in motion pictures and television during the previous year. Within the entertainment industry, the Golden Globes are considered second in importance both to the Academy Awards (for film) and to the Emmy Awards (for television), and the televised awards ceremony is a comparably lavish affair.*
# 
# **In this notebook, I have performed the basic data analysis on the Golden Globe Awards dataset and tried to identify following feartures and trends.**
# 
# 
# * Nominee who got most number of nominations?
# * Who got the most number of awards?
# * Which movie received the most number of awards?
# * Which director got most number of awards?
# * Which film/artist was nominated first during the year?
# * Total number of nominations done each year? what was the trend?
# * How many new categories were introduced over the period?

# Importing libraries

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt


# In[ ]:


df = pd.read_csv('/kaggle/input/golden-globe-awards/golden_globe_awards.csv')
df.head(3)


# Lets look at the data types and missing values before we start working on them.

# In[ ]:


missing_values = df.isnull().sum()
missing_values = pd.DataFrame(missing_values, columns=['Missing Values'])
column_data_types = df.dtypes
column_data_types  = pd.DataFrame(column_data_types, columns=['Data Types'])
missing_values.join(column_data_types)


# **Who got most number of nominations?**

# In[ ]:


#Who got most number of nominations
nomination_count = df["nominee"].value_counts()
print ("The most number of nominations got by: " + nomination_count.index[0])
print ("\nTop 5 candidates:")
print (nomination_count[:5].to_string())


# Who got most number of awards? 
# We need to check if the WIN column is True.

# In[ ]:


#Who got most number of awards
df_won = df[df["win"] == True]
won_count = df_won["nominee"].value_counts()
print ("The most number of awards got by:   " + won_count.index[0])
print ("\nTop 5 winners:")
print (won_count[:5].to_string())


# Which film got the most number of awards?

# In[ ]:


#Which film got the most number of awards
won_film_count = df_won["film"].value_counts()
print ("The most number of awards got by:  " + won_film_count.index[0])
print ("\nTop 5 films(including TV shows):")
print (won_film_count[:5].to_string())


# Which director got the most number of awards?

# In[ ]:


#Which director got the most number of awards
df_best_director = df_won[df_won["category"] == "Best Director - Motion Picture"]
best_director_count = df_best_director["nominee"].value_counts()
print ("The director who got the most number of awards:  " + best_director_count.index[0])
print ("\nTop 5 directors:")
print (best_director_count[:5].to_string())


# Which TV Show received the most number of awards?
# 
# Lets introduce new column PICTURE values TV Show or Movie. The value can be determined using two features i)CATEGORY and ii)FILM 
# 
# *As we already know, we have null values in FILM column. To keep things simple, lets make an assumption NaN is always considered as value Movie.*

# In[ ]:


series_picture = pd.Series(pd.np.where(df_won["film"].str.contains("TV", na = False), "TV Show",
                           pd.np.where(df_won["category"].str.contains("Television", na = False), "TV Show", "Movie")), name = "picture")
df_won = df_won.assign(picture = series_picture.values)
df_won.head(3)


# In[ ]:


#Which TV Show received the most number of awards
won_tv_show_count = df_won.loc[ df_won["picture"] == "TV Show", "film"].value_counts()
print ("The TV Show which got most number of awards: " + won_tv_show_count.index[0])
print ("\nTop 5 TV Shows:")
print (won_tv_show_count[:5].to_string())


# Which movie received the most number of awards?

# In[ ]:


#Which movie received the most number of awards
won_movie_count = df_won.loc[ df_won["picture"] == "Movie", "film"].value_counts()
print ("The Movie which got most number of awards: " + won_movie_count.index[0])
print ("\nTop 5 Movies:")
print (won_movie_count[:5].to_string())


# Which film/artist nominated first during the year?
# 
# *The nominee column has both film and actors.*
# *PS: I haved used to break to limit the output but you get the idea.*

# In[ ]:


#The film/artist was nominated first during the year
nominee_group = df.groupby('nominee')
for nominee, group_df in nominee_group:
    nominated_year = group_df['year_award'].min()
    print ('{} : {}'.format(nominee, nominated_year))
    break


# Nominations trends over the years

# In[ ]:


#Number of nominations done each year
fig1 = plt.figure()
subplot1 = fig1.add_subplot(1,1,1)

no_of_awards_each_year = df.groupby('year_award').size()
no_of_awards_each_year.plot(ax=subplot1, rot = 45)

subplot1.set_xlabel("Nominated Year")
subplot1.set_ylabel("Number of Nominations")
subplot1.locator_params(nbins=20, axis="x")
subplot1.set_title("Nominations trend over the years")
fig1.show()


# Categories trends over the years

# In[ ]:


#How many categories were introduced over the years
fig2 = plt.figure()
subplot2 = fig2.add_subplot(1,1,1)

no_of_categories_each_year = df.groupby(['category','year_award']).size().groupby('year_award').size()
no_of_categories_each_year.plot(ax=subplot2, rot = 45)

subplot2.set_xlabel("Nominated Year")
subplot2.set_ylabel("Number of Categories")
subplot2.locator_params(nbins=20, axis="x")
subplot2.set_title("Categories trend over the years")
fig2.show()

