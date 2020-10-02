#!/usr/bin/env python
# coding: utf-8

#  ## Marvel V/s DC

# <img src="http://getwallpapers.com/wallpaper/full/f/6/7/133994.jpg" width="800px">

# > We are already familiar with the fact that how much popularity the Comic Books are getting these days. Marvel and DC have a huge fan base in all the countries around the world. The recent releases prove that super hero genre in movies is never going to fade, instead the Box office collection of these movies are breaking some of the oldest records. Avengers Infinity Wars broke the record of Star Wars which is considered to be the most popular movie in The United States of America. It is not all movies like Black Panther(Marvel) coming with a full cast of Black Americans now stand in the Top 10 most earning movies till date around the world, Wonder Woman(DC), a movie with a female lead did wonders in the Box Office. All the release from Marvel and DC have been loved by the audiences world wide and accepted whole heartedly. Since, the popularity of Marvel and DC is a concern related to World Entertainment. I am very curious to investigate the data and find some interesting results.

# In[ ]:


get_ipython().system('pip install pywaffle')


# In[ ]:



# for some basic operations
import numpy as np 
import pandas as pd 
import random
from collections import Counter

# for visualizations
import matplotlib.pyplot as plt
import seaborn as sns
from pywaffle import Waffle
from pandas import plotting
from pandas.plotting import parallel_coordinates

# for interactive visualizations
import plotly.offline as py
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
from plotly import tools
init_notebook_mode(connected = True)
import plotly.figure_factory as ff

# for providing path
import os
print(os.listdir("../input"))


# **Reading the DC data**

# In[ ]:


# reading the data for dc

dc = pd.read_csv('../input/dc-wikia-data.csv')

# checking the head of the data
dc.head()


# **Reading the Marvel Data**

# In[ ]:


# reading the marvel data

marvel = pd.read_csv('../input/marvel-wikia-data.csv')

# checking the head of the data
marvel.head()


# ## Data Visualization

# In[ ]:


# imputing missing values

dc['ID'] = dc['ID'].fillna(dc['ID'].mode()[0])
dc['ALIGN'] = dc['ALIGN'].fillna(dc['ALIGN'].mode()[0])
dc['EYE'].fillna(dc['EYE'].mode()[0], inplace = True)
dc['HAIR'].fillna(dc['HAIR'].mode()[0], inplace = True)
dc['SEX'].fillna(dc['SEX'].mode()[0], inplace = True)
dc['ALIVE'].fillna(dc['ALIVE'].mode()[0], inplace = True)
dc['APPEARANCES'].fillna(dc['APPEARANCES'].mode()[0], inplace = True)
dc['FIRST APPEARANCE'].fillna(dc['FIRST APPEARANCE'].mode()[0], inplace = True)
dc['YEAR'].fillna(dc['YEAR'].mode()[0], inplace = True)

marvel['ID'] = marvel['ID'].fillna(marvel['ID'].mode()[0])
marvel['ALIGN'] = marvel['ALIGN'].fillna(marvel['ALIGN'].mode()[0])
marvel['EYE'].fillna(marvel['EYE'].mode()[0], inplace = True)
marvel['HAIR'].fillna(marvel['HAIR'].mode()[0], inplace = True)
marvel['SEX'].fillna(marvel['SEX'].mode()[0], inplace = True)
marvel['ALIVE'].fillna(marvel['ALIVE'].mode()[0], inplace = True)
marvel['APPEARANCES'].fillna(marvel['APPEARANCES'].mode()[0], inplace = True)
marvel['FIRST APPEARANCE'].fillna(marvel['FIRST APPEARANCE'].mode()[0], inplace = True)
marvel['Year'].fillna(marvel['Year'].mode()[0], inplace = True)


# * By looking at the above bubble plot, we can say that people do not like bad characters much that is the reason why they have very low appearances in comparison to good characters.
# 
# * The Good characters have highest appearances in comparison to others.

# In[ ]:



plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

plt.subplot(2, 1, 1)
sns.violinplot(dc['ID'], dc['YEAR'], hue = dc['ALIGN'], palette = 'PuRd')
plt.xlabel(' ')
plt.title('DC', fontsize = 30)

plt.subplot(2, 1, 2)
sns.violinplot(marvel['ID'], marvel['Year'], hue = marvel['ALIGN'], palette = 'copper')
plt.title('MARVEL', fontsize = 30)

plt.show()


# In[ ]:



plt.rcParams['figure.figsize'] = (20, 8)
plt.style.use('fivethirtyeight')

dc['APPEARANCES'].fillna(0, inplace = True)
marvel['APPEARANCES'].fillna(0, inplace = True)

import warnings
warnings.filterwarnings('ignore')

plt.subplot(1, 2, 1)
sns.kdeplot(dc['APPEARANCES'], color = 'green')
plt.title('DC')

plt.subplot(1, 2, 2)
sns.kdeplot(marvel['APPEARANCES'], color = 'skyblue')
plt.title('Marvel')

plt.suptitle('Appearances comparison vs DC and Marvel', fontsize = 20)
plt.show()


# > From the above two plots made for visualizing the no. of appearances for  different superheroes in Marvel and DC one thing is clear that on an average the Marvel Superheroes have a larger fan base. AS the maximum no. of appearances for DC is about 3000 whereas the maximum no. of appearances for marvel heroes is about 4000 which is very high or we can say 25% higher than DC's.

# In[ ]:



trace1 = go.Histogram(
         x = dc['ID'],
         name = 'DC',
         opacity = 0.75,
         marker = dict(
               color = 'rgb(52, 85, 159, 0.6)'
         )
)
trace2 = go.Histogram(
          x = marvel['ID'],
          name = 'Marvel',
          opacity = 0.75,
          marker = dict(
                 color = 'rgb(84, 52, 15, 0.6)'
          )
)
data = [trace1, trace2]

layout = go.Layout(
    barmode = 'group',
    title = 'Comparison of Identities')

fig = go.Figure(data = data, layout = layout)
py.iplot(fig)


# > By looking at the above Bar plot for comparison of Identities of superheroes in Marvel and DC, It is clearly visible that Marvel has around 6275 Secrect Identies, 4528 Public Identies, No Identity Unknown, 1788 No dual Identity, and 15 Known to Authorities Identity whereas Dc has 2408 Secret Identies, 2466 Public Identities, 9 Identities unknown, 0 Non-dual identities, and known to authorities identities.
# 
# >Overall Marvel has almost double the identies in comparision to DC. Marvel has more diverse identites in Comparison to DC. Marvel has no identities unknown which is great whereas DC has 9 identities unknown. Marvel also has Non-dual identites and identities known to authorization committies.

# In[ ]:


# create trace 1 that is 3d scatter

trace1 = go.Scatter3d(
    x = dc['APPEARANCES'],
    y = dc['YEAR'],
    z = dc['ALIVE'],
    name = 'DC',
    mode='markers',
    marker=dict(
        size=10,
        color = 'rgb(58,56,72)',                # set color to an array/list of desired values      
    )
)

trace2 = go.Scatter3d(
    x = marvel['APPEARANCES'],
    y = marvel['Year'],
    z = marvel['ALIVE'],
    name = 'Marvel',
    mode = 'markers',
    marker = dict(
         size = 10,
         color = 'rgb(217, 2, 8)'
    )
)

data = [trace1, trace2]

layout = go.Layout(
    title = 'Character vs Gender vs Alive or not',
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0  
    )
    
)
fig = go.Figure(data=data, layout=layout)
iplot(fig)


# In[ ]:



trace = go.Box(
            x = dc['ALIGN'],
            y = dc['APPEARANCES'],
            name = 'DC',
            marker = dict(
                  color = 'rgb(145, 65, 75)')
)
                   

trace2 = go.Box(
            x = marvel['ALIGN'],
            y = marvel['APPEARANCES'],
            name = 'Marvel',
            marker = dict(
                   color = 'rgb(2, 15, 85)'),

              )

data = [trace, trace2]

layout = go.Layout(
    boxmode = 'group',
    title = 'Character vs Appearances')

fig = go.Figure(data = data, layout = layout)
py.iplot(fig)


# > By looking at the above graph, we can conclude that Marvel has more number of good and neutral characters in their comics, whereas DC has more number of reformed criminals in their comics. although they have similar number of bad charaters in their comics.

# In[ ]:



hair_dc = dc['HAIR'].value_counts()
hair_marvel = marvel['HAIR'].value_counts()

trace = go.Bar(
             x = hair_dc.index,
             y = hair_dc.values,
             name = 'DC',
             marker = dict(
                  color = 'rgb(56, 54, 36)'
             )
)
trace2 = go.Bar(
            x = hair_marvel.index,
            y = hair_marvel.values,
            name = 'Marvel',
            marker = dict(
                  color = 'rgb(78, 03, 45)'
            )
)

data = [trace, trace2]

layout = go.Layout(
             barmode = 'relative',
              title = 'Different Hair Colors of SuperHeroes')

fig = go.Figure(data = data, layout = layout)
py.iplot(fig)


# > Very Interesting the marvel and dc comics have equal no. of characters with all the different categories of hair color mentioned above.

# In[ ]:



hair_dc = dc['EYE'].value_counts()
hair_marvel = marvel['EYE'].value_counts()

trace = go.Bar(
             x = hair_dc.index,
             y = hair_dc.values,
             name = 'DC',
             marker = dict(
                  color = 'rgb(35, 25, 20)'
             )
)
trace2 = go.Bar(
            x = hair_marvel.index,
            y = hair_marvel.values,
            name = 'Marvel',
            marker = dict(
                  color = 'rgb(15, 25, 45)'
            )
)

data = [trace, trace2]

layout = go.Layout(
             barmode = 'relative',
              title = 'Different Eye Colors of SuperHeroes')

fig = go.Figure(data = data, layout = layout)
py.iplot(fig)


# In[ ]:



gsm_dc = dc['GSM'].value_counts()
gsm_marvel = marvel['GSM'].value_counts()

label_dc = gsm_dc.index
size_dc = gsm_dc.values

label_marvel = gsm_marvel.index
size_marvel = gsm_marvel.values

colors = ['aqua', 'gold']

trace = go.Pie(
         labels = label_dc, values = size_dc, marker = dict(colors = colors), name = 'DC', hole = 0.3)
colors2 = ['pink', 'lightblue']

trace2 = go.Pie(labels = label_marvel, values = size_marvel, marker = dict(colors = colors2), name = 'Marvel', hole = 0.3)

data = [trace]
data2 = [trace2]

layout1 = go.Layout(
           title = 'Sexual Minority Groups in DC')
layout2 = go.Layout(
           title = 'Sexual Minority Groups in Marvel'  )

fig = go.Figure(data = data, layout = layout1)
fig2 = go.Figure(data = data2, layout = layout2)
py.iplot(fig)
py.iplot(fig2)


# In[ ]:



align_dc = dc['ALIGN'].value_counts()
align_marvel = marvel['ALIGN'].value_counts()

trace1 = go.Bar(
            x = align_dc.index,
            y = align_dc.values,
            name = 'DC',
            marker = dict(
                 color = 'rgb(78, 6, 2)'
            )
)
trace2 = go.Bar(
             x = align_marvel.index,
             y = align_marvel.values,
             name = 'Marvel',
             marker = dict(
                  color = 'rgb(05, 35, 20)'
             )
)
data = [trace1, trace2]

layout = go.Layout(
           barmode = 'group',
           title = 'Alignment of Characters')

fig = go.Figure(data = data, layout = layout)
py.iplot(fig, filename = 'Alignment')


# In[ ]:



sex_count_dc = dc['SEX'].value_counts()
sex_count_marvel = marvel['SEX'].value_counts()

trace1 = go.Bar(
    x = sex_count_dc.index,
    y = sex_count_dc.values,
    name = 'DC',
    marker = dict(
        color = 'rgb(26,01,98)'
    )
)

trace2 = go.Bar(
     x = sex_count_marvel.index,
     y = sex_count_marvel.values,
     name = 'Marvel',
     marker = dict(
       color = 'rgb(104, 105, 120)' 
     )
)
data = [trace1, trace2]

layout = go.Layout(
            barmode = 'stack',
            title = 'Comparison of Gender in DC and Marvel')

fig = go.Figure(data = data, layout = layout)
py.iplot(fig, filename = 'Gender')


# In[ ]:



import warnings
warnings.filterwarnings('ignore')

# Prepare Data
df = dc.iloc[:200,:].groupby('SEX').size().reset_index(name='counts')
n_categories = df.shape[0]
colors = [plt.cm.inferno_r(i/float(n_categories)) for i in range(n_categories)]

# Draw Plot and Decorate
fig = plt.figure(
    FigureClass=Waffle,
    values = df['counts'],
    labels = ['Female','Male'],
    legend = {'loc': 'upper left'},
    title = {'label': 'Gender Gap in DC', 'fontsize': 20},    
    rows=7,
    colors=['pink','lightgreen'],
    figsize = (20, 5)
)


# In[ ]:



import warnings
warnings.filterwarnings('ignore')

# Prepare Data
df = marvel.iloc[:200,:].groupby('SEX').size().reset_index(name='counts')
n_categories = df.shape[0]
colors = [plt.cm.inferno_r(i/float(n_categories)) for i in range(n_categories)]

# Draw Plot and Decorate
fig = plt.figure(
    FigureClass=Waffle,
    values = df['counts'],
    labels = ['Genderfluid','Male','Female','Agender'],
    legend = {'loc': 'upper left'},
    title = {'label': 'Gender Gap in Marvel', 'fontsize': 20},    
    rows=7,
    colors=['yellow','blue', 'lightblue','orange'],
    figsize = (20, 5)
)


# In[ ]:



# Plot
plt.figure(figsize=(20, 10), dpi= 80)

plt.subplot(1, 2, 1)
parallel_coordinates(dc[['APPEARANCES','YEAR', 'SEX']], 'SEX',  colormap='Dark2')

# Lighten borders
plt.gca().spines["top"].set_alpha(0)
plt.gca().spines["bottom"].set_alpha(.3)
plt.gca().spines["right"].set_alpha(0)
plt.gca().spines["left"].set_alpha(.3)

plt.title('DC', fontsize = 20)
plt.grid(alpha=0.3)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(1, 2, 2)
parallel_coordinates(marvel[['APPEARANCES','Year', 'SEX']], 'SEX',  colormap='Dark2')

# Lighten borders
plt.gca().spines["top"].set_alpha(0)
plt.gca().spines["bottom"].set_alpha(.3)
plt.gca().spines["right"].set_alpha(0)
plt.gca().spines["left"].set_alpha(.3)

plt.title('Marvel', fontsize = 20)
plt.grid(alpha=0.3)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.suptitle('Parallel Coordinates For Appearances vs Gender', fontsize = 20)
plt.show()


# ## Top 15 Characters from Marvel

# In[ ]:


# Inspired from https://www.kaggle.com/piyush1912/dc-vs-marvel-comics 

marvel['comics'] = 'Marvel'
marvel = marvel.truncate(before=-1, after=15)
import networkx as nx
marvel = nx.from_pandas_edgelist(marvel, source='comics', target='name', edge_attr=True,)


# <img src="https://i.pinimg.com/originals/29/df/17/29df176d0b0c352444204446a5b1c3f6.gif" width="300px">
# 

# In[ ]:




import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize']  = (15, 15)
plt.style.use('fivethirtyeight')
plt.suptitle('Most Popular Characters of Marvel', fontsize = 30)

pos = nx.spring_layout(marvel)

# drawing nodes
nx.draw_networkx_nodes(marvel, pos, node_size = 1200, node_color = 'pink')

# drawing edges
nx.draw_networkx_edges(marvel, pos, width = 6, alpha = 0.1, edge_color = 'brown')

# labels
nx.draw_networkx_labels(marvel, pos, font_size = 20, font_family = 'sans-serif')

plt.grid()
plt.axis('off')
plt.show()


# **The Top Characters from the Marvel Universe are Iron Man,  Captain America, Hulk, Spiderman, Wolverine, Mathew Murdock, Benjamin Grimm, Reed Richards, Jonathan Storm, Scott Summers etc.**
# 
# **Mostly The Popular Characters include the heroes from Avengers, but there is no female in the Top 15 Most Popularr Character in the Marvel universe.**

# ## Top 15 Characters from DC

# In[ ]:



dc['comics']= 'DC'
dc= dc.truncate(before=-1, after=15)

import networkx as nx
dc = nx.from_pandas_edgelist(dc, source='comics', target='name', edge_attr=True,)


# 
# <img src="https://media1.tenor.com/images/de7249ce3d32f166b2dc466eae96b439/tenor.gif?itemid=5274502" width="400px">
# 

# In[ ]:



import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize']  = (15, 15)
plt.style.use('fivethirtyeight')
plt.suptitle('Most Popular Characters of DC', fontsize = 30)

pos = nx.spring_layout(dc)

# drawing nodes
nx.draw_networkx_nodes(dc, pos, node_size = 1200, node_color = 'orange')

# drawing edges
nx.draw_networkx_edges(dc, pos, width = 6, alpha = 0.1, edge_color = 'black')

# labels
nx.draw_networkx_labels(dc, pos, font_size = 20, font_family = 'sans-serif')

plt.grid()
plt.axis('off')
plt.show()


# **The Top Characters from DC are Wonder Woman, Superman, Aquaman, Alan Scott, Green Lantern, Batman, Flash, Alfred pennyworth, Gordon, Richard Grayson, Dinah Laurel Lance, Barbara Gordon, Jaosn Garrick, Timothy Drake. **
# 
# 
# **One Important finding is that there are so many characters from New Earth. There is a female character also in the list of Top 15 Most Popular Characters in the DC Universe whereas there no female character in the Marvel Universe.**
