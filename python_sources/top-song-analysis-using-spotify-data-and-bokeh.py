#!/usr/bin/env python
# coding: utf-8

# # Top-Song Analysis using Spotify data
# 

# In[ ]:


import numpy as np 
from ipywidgets import interact
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure
import pandas as pd 
import matplotlib.pyplot as plt
import os
output_notebook()


# 
# # Exploring the data
# ### According to the source's description: 
# "This dataset contains the daily ranking of the 200 most listened songs in 53 countries from 2017 and 2018 by Spotify users. It contains more than 2 million rows, which comprises 6629 artists, 18598 songs for a total count of one hundred five billion streams count."

# ### Use pd.read_csv('filepath') to read the .csv file. 

# In[ ]:


spotify_data = pd.read_csv("../input/data.csv") 


#  This function returns a pandas dataframe. We can see the first rows of the file with the head() function

# In[ ]:


spotify_data.head()


# In[ ]:


print("DataFrame's columns: ", spotify_data.columns)
print("DataFrame's shape: ", spotify_data.shape)
print("Countries :", spotify_data['Region'].unique()) 

# Notice in the list of countries, that "global" is also an option


# ## Now let's see which was the most streamed song on a single day
# 
# * For that we can use the function np.where() 
# 
# 

# In[ ]:


index = np.where(spotify_data["Streams"] == max(spotify_data['Streams']))  # Find the index with the maximum value for 'Streams'
print(spotify_data['Track Name'][index[0][0]])                             # Print the Track Name using the first entry of index
print(spotify_data['Date'][index[0][0]])                                   # Print the Date with the most streams
print(spotify_data['Region'][index[0][0]])


# According to Wikipedia this song was released January 12, 2017, which means that it took more than 5 months for
# it to reach its global maximum peak of streams-on-a-single-day on Spotify.
# 
# ### Using this time only the dataframe we can show the top songs (global) on that date

# In[ ]:


Region = spotify_data['Region'] == 'global'
Date   = spotify_data['Date']=='2017-01-12'  # yy-mm-dd
spotify_data[Region & Date].head()


# # Tracks which made it at least to the top 10 globally
# # Position through time in different regions

# In[ ]:


Region_global = spotify_data['Region'] == 'global'
Region_other = spotify_data['Region'] == 'fr'
Position = spotify_data['Position'] <= 10
Top_10_Tracks_Global = spotify_data[Region_global & Position]['Track Name'].drop_duplicates().reset_index(drop=True)


Name   = spotify_data['Track Name'] == Top_10_Tracks_Global[1]
Global_Position = spotify_data[Region_global & Name]['Position'].reset_index(drop=True)
Local_Position = spotify_data[Region_other & Name]['Position'].reset_index(drop=True)

x_1 = list(range(0,len(Global_Position)))
y_1 = list(Global_Position[:])
x_2 = list(range(0,len(Local_Position)))
y_2 = list(Local_Position[:])

fig_2 = figure(title="", plot_height=400,plot_width=700) 
fig_2.xaxis.axis_label = 'Time in Days'
fig_2.yaxis.axis_label = 'Position'
inp_multi=fig_2.multi_line([x_1, x_2], [y_1, y_2], color=["navy", "green"], alpha=[0.8, 0.8], line_width=2,legend='Global')
fig_2.legend.location = "top_left"


# In[ ]:


def update_name_and_region(trackName,region):
    Name = spotify_data['Track Name'] == trackName
    Region = spotify_data['Region'] == 'global'
    Region_local = spotify_data['Region'] == region
    Global_Position = spotify_data[Region & Name]['Position'].reset_index(drop=True)
    Local_Position = spotify_data[Region_local & Name]['Position'].reset_index(drop=True)
    inp_multi.data_source.data['xs'][0] = list(range(0,len(Global_Position[:])))
    inp_multi.data_source.data['ys'][0] = list(Global_Position[:])
    inp_multi.data_source.data['xs'][1] = list(range(0,len(Local_Position[:])))
    inp_multi.data_source.data['ys'][1] = list(Local_Position[:])
    fig_2.title.text = trackName + ' (Global Position and Local Position; Region: ' + region + ')'
    show(fig_2,notebook_handle=True)
    push_notebook()
    


# In[ ]:


interact(update_name_and_region, trackName=Top_10_Tracks_Global[:],region= spotify_data['Region'].unique());


# # Total days on the number one spot

# In[ ]:


song_names    = list()
days_in_top_1 = list()
Position = spotify_data['Position'] <= 1
Region   = spotify_data['Region'] == 'global'
Top_1_Tracks_Global = spotify_data[Region & Position]['Track Name'].drop_duplicates().reset_index(drop=True)


for n in range(len(Top_1_Tracks_Global)):
    song_names.append(str(Top_1_Tracks_Global[n]))
    Name     = spotify_data['Track Name'] == song_names[n]
    days_in_top_1.append(len(spotify_data[Region & Position & Name]))

    
top_1_fig = figure(x_range=song_names, plot_height=550,plot_width=800, title="Days in spot No. 1",
                   y_axis_label = 'Total days' ,toolbar_location=None, tools="")

top_1_fig.vbar(x=song_names, top=days_in_top_1, width=0.9)
top_1_fig.xgrid.grid_line_color = None
top_1_fig.y_range.start = 0
top_1_fig.xaxis.major_label_orientation = 1
#top_1_fig.y_axis_label = 'Days in spot Number 1'
show(top_1_fig)
type(top_1_fig.xaxis)


# ### For the given timespan the number one spot (global) was pretty much dominated by only 3 different songs :
# - Shape of You
# - Despacito
# - rockstar
