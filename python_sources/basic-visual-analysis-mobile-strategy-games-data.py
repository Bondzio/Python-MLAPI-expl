#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='whitegrid')


# In[ ]:


game_data=pd.read_csv('../input/17k-apple-app-store-strategy-games/appstore_games.csv', parse_dates=True)
game_data.head()


# In[ ]:


game_data.isnull().sum() #number of missing values in each column


# In[ ]:


game_data.drop(['URL','Icon URL'], axis=1, inplace=True) #removing less-informative columns
game_data['Size']=game_data.Size/(1024**2)  #converting game-sizes to MB
game_data.head()


# In[ ]:


game_data.dtypes


# In[ ]:


game_data.columns


# # A. In Numbers... 

# In[ ]:


game_data.describe() #summary statistics for numerical columns


# In[ ]:


categorical_cols=[x for x in game_data.columns if game_data[x].dtype=='object']
game_data[categorical_cols].describe()  #summary statistics for categorical columns


# In[ ]:


game_data.Name.value_counts() # count/frequency of game names


# Some game names appeared twice, but this is most likely due to repetition, since the number of unique names is equal to the number of unique game IDs. 

# In[ ]:


game_data.Name.nunique()==game_data.ID.nunique() #checking if game names are unique


# In[ ]:


#Getting Developers with most games
game_data.groupby(['Developer']).ID.count().nlargest(20)


# In[ ]:


#Getting Developers' overall average rating accross all games
print(game_data.groupby('Developer')['Average User Rating'].mean().nlargest(615))
print('\nOver 600 Developers had the maximum average rating (5.0), which is great.\n')

print(game_data.groupby('Developer')['Average User Rating'].mean().nsmallest(5))
print('\nThe lowest overall average rating was 1.0')


# Some Subtitles appear more than once when game name & ID change. This could mean that a Developer listed as having multiple games could really have just one, with changes to the name and ID. See below example.

# In[ ]:


game_data.groupby(['Subtitle']).get_group('"90\'s Digital Pet - Tamagotchi"')


# # B. Some Graphics..

# ## Prices

# In[ ]:


print('{:.2f}% of the games are free.'.format(game_data[game_data.Price==0].Price.count()/len(game_data)*100))
print('{:,} ({:.2f}%) of the games have in-app Purchases.'.format(game_data['In-app Purchases'].notna().sum(),
                                                                  game_data['In-app Purchases'].notna().sum()/len(game_data)*100))

plt.figure(figsize=(10,6))
sns.distplot(game_data.Price.dropna())
plt.title('Distribution of Prices', fontweight='bold',fontsize=18, pad=20)


# In[ ]:


plt.figure(figsize=(10,6))
sns.boxplot(y=game_data.Price)
plt.title('Boxplot of Game Prices', fontweight='bold',fontsize=18, pad=20)


# So many of the games are free (price=0) that the boxplot is just a thin strip at zero, with the other prices appearing as outliers. Perhaps the violin plot below will shed more light.

# In[ ]:


plt.figure(figsize=(10,6))
sns.violinplot(y=game_data.Price.clip(0,10)) # limiting to games costing less than 10$
plt.title('Violin plot of Game Prices',fontweight='bold',fontsize=18, pad=20)


# In[ ]:


plt.figure(figsize=(10,6))
sns.regplot(x=game_data['Average User Rating'], y=game_data.Price.clip(0,60))
plt.title('Relationship between Price and Average Rating', fontweight='bold',fontsize=18, pad=20)


# There's a very weak negative correlation between price and average rating (limit price values to range [0,5] to see it better), which would imply that costlier games would receive lower ratings. But there are so many values and outliers that contradict this.

# ## Game Size

# In[ ]:


print('The largest game was < {} >, and the smallest was < {} >, with sizes {:,.2f}MB and {:.2f}MB respectively'.format(game_data.Name.iloc[game_data.Size.idxmax()],game_data.Name.iloc[game_data.Size.idxmin()],game_data.Size.max(), game_data.Size.min()))
plt.figure(figsize=(10,6))
sns.boxplot(y=game_data.Size)
plt.title('Boxplot of Game Sizes')

plt.figure(figsize=(10,6))
sns.distplot(game_data.Size.dropna())
plt.title('Distribution of Game Sizes', fontweight='bold',fontsize=18, pad=20)
plt.xlabel('Size in MB')


# In[ ]:


plt.figure(figsize=(10,10))
sns.regplot(x=game_data['Average User Rating'],y=game_data['Size'])
plt.title('Relationship between Game Size and Average User Rating', fontweight='bold',fontsize=18, pad=20)


# There appears to a be positive correlation between the two: accounting for the scale, larger games would likely yield higher ratings. But it is rather weak, as most of the values fall well clear of the regression line, and games of almost all sizes have had a 4.5 rating.

# ## User Ratings

# In[ ]:


plt.figure(figsize=(10,6))
print(game_data['Average User Rating'].value_counts())
sns.countplot(game_data['Average User Rating'], color='orangered')
plt.title('Count of Average Ratings', fontweight='bold',fontsize=18, pad=20)


# In[ ]:


plt.figure(figsize=(10,6))
ratings=game_data[['Average User Rating','User Rating Count']].dropna()
sns.barplot(x=ratings['Average User Rating'], y=ratings['User Rating Count'], palette='Blues')
plt.title('Count of User Ratings responsible for each each Average-Rating', fontweight='bold',fontsize=18, pad=20)


# ## Age Ratings

# In[ ]:


plt.figure(figsize=(10,6))
print(game_data['Age Rating'].value_counts())
sns.countplot(game_data['Age Rating'], color='teal')


# A very large proportion of the games can be played by kids, who are often the most likely to play games. Lower age ratings also maximize the target audience, which is another plus.

# ## Genres

# In[ ]:


plt.figure(figsize=(10,6))
game_data[game_data['Primary Genre'] != 'Games']['Primary Genre'].value_counts().plot(kind='bar')
plt.title('Primary Genres of Games - other than just "Games"', fontweight='bold',fontsize=18, pad=20)
plt.ylabel('Count')


# ## Language

# In[ ]:


#Getting list of all languages listen in all apps
language_list=' '.join([x for x in game_data.Languages.dropna().values]).replace(',','').split()
languages=pd.Series(language_list)
print('Total number of different languages: {}'.format(languages.nunique()))
languages.value_counts()


# In[ ]:


plt.figure(figsize=(9,26))
sns.countplot(y=languages, order=languages.value_counts().index)
plt.title('Count of Games offering Language', fontweight='bold',fontsize=18, pad=20)

