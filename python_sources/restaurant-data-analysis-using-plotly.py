#!/usr/bin/env python
# coding: utf-8

# # Exploring Restaurant Data using Plotly

# In this notebook, my aim is to generate insights out of Restaurant data made available by one of the most popular websites for Foodies, Zomato. We would be using Plotly for vizualizing data in a interactive form. This kernel can act as a tutorial for folks seeking to learn Plotly for data vizualization.
# 

# # About Plotly

# Plotly is one of the finest data visualization tools available built on top of visualization library D3.js, HTML and CSS. It is created using Python and the Django framework.  One can choose to create interactive data visualizations online or use the libraries that plotly offers to create these visualizations in the language/ tool of choice. It is compatible with a number of languages/ tools: R, Python, MATLAB, Perl, Julia, Arduino. 

# This kernel also uses Plotly Express, which is a wrapper around Plotly and helps generate interactive graphs using minimalistic code.

# ## Importing necassary modules 

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from wordcloud import WordCloud
#Imports required for Plotly
import plotly.graph_objs as go
import plotly.offline as py
import plotly.figure_factory as ff
from plotly import tools
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True) #This is important 
import plotly_express as px
#Plotly Imports Ends
import warnings
warnings.filterwarnings('ignore')
import os
print(os.listdir("../input"))


# 
# ### Reading the dataset

# In[ ]:


rest_data=pd.read_csv('../input/zomato.csv')
print('We have a total of {0} restaurants in the data set'.format(rest_data.shape[0]))


# In[ ]:


#vizualizing the first 5 observations
rest_data.head()


# ## Performing data cleansing activities

# The URL's of the restaurants and it's phone numbers won't be much useful in our analysis. Also, as far as the location/address is concerned, we have 3 columns signifying the same macro level detail of the address, viz. complete address, suburb etc. Thus, Keeping just the location (Suburb) makes more sense for our analysis.
# 
# Concludingly, Dropping the URL, phone number, physical address and location column.

# In[ ]:


del rest_data['url']
del rest_data['address']
del rest_data['phone']
del rest_data['location']


# Renaming some columns for better interpretability 

# In[ ]:


rest_data.rename(columns={'listed_in(city)': 'Suburb','listed_in(type)': 'restaurant_type'}, inplace=True)


# ## viewing the dataset info after the above cleanup operations

# In[ ]:


rest_data.info()


# We can see that there are some missing values in Votes, which means that not enough paeople have given their ratings for that particular restaurant, thus a consolidated rating is not available. Replacing all the null values in votes with 'Newly Opened'.

# In[ ]:


rest_data.rate = rest_data.rate.replace(np.nan, 'Newly Opened')


# # Let's start with the Data Vizualization exercise

# Before that, a quick reference guide (cheat sheet) to plotly can be found [here](https://www.kaggle.com/learn-forum/98361).
# 
# This is a handy guide to quick code snippets for every type of plotly charts used in this kernel.

# The feature that I find most lucrative about Plotly is it's interactivity. These plots are as good as the one's generated by some popular Business Intellegence tools like Tableau which costs hundreds of dollars in individual licences.

# * ## Total number of Restaurants in each Suburban locality of the city

# In[ ]:


trace1 = go.Bar(
                x = rest_data.Suburb.value_counts().keys(),
                y = rest_data.Suburb.value_counts(),
                name = "Suburb",
#                 marker = dict(
#                          colorscale='Jet',
#                          showscale=True),
                text = rest_data.Suburb)
data1 = [trace1]
layout = go.Layout(title = 'Restaurant Distribution by Suburb', 
                   barmode = "group", 
                   yaxis=dict(title= 'Number of Restaurants'))
fig = go.Figure(data = data1, layout = layout)
py.offline.iplot(fig, filename = 'basic-line')


# The above graph shows that BTM has the maximum number of restaurants in the city followed by Koramangala (all blocks) and Jayanagar.

# ## Distribution of Restaurant by restaurant-types.

# In[ ]:


trace1 = go.Bar(
                x = rest_data['restaurant_type'].value_counts().keys(),
                y = rest_data['restaurant_type'].value_counts(),
                name = "restaurant_type",
#                 marker = dict(
#                          colorscale='Jet',
#                          showscale=True),
                text = rest_data['restaurant_type'])
data1 = [trace1]
layout = go.Layout(title = 'Restaurant Distribution by Type', 
                   barmode = "group", 
                   yaxis=dict(title= 'Number of Restaurants'))
fig = go.Figure(data = data1, layout = layout)
py.offline.iplot(fig, filename = 'basic-line')


# It can observed that the Restaurants providing home delivery of food are in maximum number across the city (almost to the tune of 25000), followed by Dine-out restaurants and dessert parlours.

# ## Distribution of Restaurant by SubCategories

# In[ ]:


trace1 = go.Bar(
                x = rest_data['rest_type'].value_counts().head(15).keys(),
                y = rest_data['rest_type'].value_counts().head(15),
                name = "rest_type",
#                 marker = dict(
#                          colorscale='Jet',
#                          showscale=True),
                text = rest_data['rest_type'])
data1 = [trace1]
layout = go.Layout(title = 'Restaurant Distribution by Sub-Categories', 
                   barmode = "group", 
                   yaxis=dict(title= 'Number of Restaurants'))
fig = go.Figure(data = data1, layout = layout)
py.offline.iplot(fig, filename = 'basic-line')


# In the above graph, we can see that there are almost 20,000 restaurants serving quick bites in the city. At the second position, we have casual dining options (10,330 restaurants) followed by cafe's.

# ## How many restaurants accept online orders on Zomato?

# In[ ]:


x = rest_data['online_order'].value_counts()
trace = go.Pie(labels = x.index, values = x)
layout = go.Layout(title = "Online Order")
fig = go.Figure(data=[trace], layout = layout)
py.iplot(fig, filename='pie_OnlineOrder')


# ## How many of them allow advance booking of tables?

# In[ ]:


x = rest_data['book_table'].value_counts()
trace = go.Pie(labels = x.index, values = x)
layout = go.Layout(title = "Book Table")
fig = go.Figure(data=[trace], layout = layout)
py.iplot(fig, filename='pie_bookTable')


# ## Restaurant ratings v/s Cost for two (hover over each data point for more details)

# In[ ]:


trace = go.Scatter(y = rest_data['approx_cost(for two people)'], text = rest_data['name'], mode = 'markers', x = rest_data['rate'].apply(
                    lambda x: x.split('/')[0])
                   )
data1 = [trace]
layout = go.Layout(title='Cost v/s Ratings', xaxis = dict(title='Restaurant Rating'), yaxis = dict(title='Cost for two'))
fig = go.Figure(data = data1 , layout = layout)
py.iplot(fig, filename='pie_bookTable')


# From the above plot, it can be observed that the "cost of two persons" increases for restaurants having ratings greater than 4. Also, one can hover over each data point which signifies individual restaurant.

# ### Some more data cleansing steps

# In[ ]:


#Removing the '/5' suffix from restaurant ratings.
#Also removing comma from "approx cost for two people" which is amount in Indian Rupees.
rest_data['rate'] = rest_data['rate'].apply(lambda x: (x.split('/')[0]))
rest_data['approx_cost(for two people)'] = rest_data['approx_cost(for two people)'].str.replace(',','').astype(float)


# ## What is the approx cost for two people for different cuisines?

# In[ ]:


px.scatter(rest_data, x="cuisines", y="approx_cost(for two people)")


# In[ ]:


rest_data['approx_cost(for two people)'].dropna(inplace=True)


# ## Restaurant Rating Distribution for each Suburban area.
# Hover over individual data points for restaurant details.

# In[ ]:


#Commented this since kaggle was behaving weirdly at the time of committing the kernel with this cell
#px.scatter(rest_data, x="Suburb", y="rate", hover_name='name')
# trace = go.Scatter(y = rest_data['rate'], text = rest_data['name'], mode = 'markers', x = rest_data['Suburb'])
                   
# data1 = [trace]
# layout = go.Layout(title='Rating Distribution for each Suburban area', xaxis = dict(title='Suburb'), yaxis = dict(title='Rating'))
# fig = go.Figure(data = data1 , layout = layout)
# py.iplot(fig, filename='pie_bookTable')


# # Dishes liked by Banagloreans 

# In[ ]:


c1 = ''.join(str(rest_data['dish_liked'].values))
from wordcloud import WordCloud
plt.figure(figsize=(10,10))
wordcloud = WordCloud(max_font_size=None, background_color='white', collocations=False,
                      width=1500, height=1500).generate(c1)
plt.imshow(wordcloud)
plt.axis("off")


# ## Popular cuisines in the city

# In[ ]:


c2 = ''.join(str(rest_data['cuisines'].values))
from wordcloud import WordCloud
plt.figure(figsize=(10,7))
wordcloud = WordCloud(max_font_size=None, background_color='white', collocations=False,
                      width=1000, height=1000).generate(c2)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")


# # Largest Restaurant Chains across the City

# In[ ]:


chain = rest_data['name'].value_counts().head(25).to_frame()
chain['Restaurant Names'] = chain.index
chain.rename(columns={'name':'Count'}, inplace=True)


# In[ ]:


px.bar(chain, x = 'Restaurant Names', y = 'Count')


# Cafe Coffee Day is the largest chain of restaurant in the city. (P.S. Cafe coffee day is Indian version of Starbucks :p )

# # Most popular restaurant-types in each Suburb

# In[ ]:


df_1=rest_data.groupby(['Suburb','rest_type']).agg('count')
data=df_1.sort_values(['name'],ascending=False).groupby(['Suburb'],
                as_index=False).apply(lambda x : x.sort_values(by="name",ascending=False).head(5))['name'].reset_index().rename(columns={'name':'count'})


# In[ ]:


rest_data.groupby(['Suburb','rest_type']).agg('count').sort_values(['name'],ascending=False).groupby('Suburb').head(1).name


# As we can see, quick bites is the most popular restaurant type for each suburb across the City, Let's also explore the most poplular restaurants in quick bites.

# In[ ]:


quick_bite = rest_data[rest_data['rest_type'] == 'Quick Bites'].name.value_counts().head(20).to_frame()
quick_bite['Restaurant Name'] = quick_bite.index
quick_bite.rename(columns={'name':'Count'}, inplace=True)
px.bar(quick_bite, x='Restaurant Name', y='Count')


# Five star chicken, Domino's Pizza and Mcdonalds are dominating the 'quick bites' market.

# # Top 10 Cuisines

# In[ ]:


cuisines = rest_data['cuisines'].value_counts().head(10).to_frame()
cuisines['Cuisine names'] = cuisines.index
px.bar(cuisines, x="Cuisine names", y="cuisines")


# As seen in the word cloud, the above graph tells the same story that North indian restaurants are highest in numbers across the city(almost 3k) followed by those serving chinese and South indian cuisines. Also there are significant number of Biryani outlets in the city. (Biryani is made with Indian spices, rice, meat (chicken, goat, beef, lamb, prawn, or fish), vegetables or eggs.)

# <img src="https://en.wikipedia.org/wiki/Biryani#/media/File:India_food.jpg" width="800px">

# ## This is a work in progress. More to come :)

# ### Please consider upvoting if you think this kernel is worth it :)
