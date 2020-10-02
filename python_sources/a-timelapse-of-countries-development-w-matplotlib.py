#!/usr/bin/env python
# coding: utf-8

# In a TED talk titled *"The best stats you've ever seen"* he gave in 2006, Hans Rosling showed the audience how we can use statistics to debunk misconceptions about the world.  
# His talk can be seen [here](https://www.ted.com/talks/hans_rosling_shows_the_best_stats_you_ve_ever_seen). It's only 20 minutes long and if you haven't seen it yet, you really should.  
# In this post, I am going to use matplotlib to replicate the animation he shows at the beginning of his talk. It shows the evolution of the fertility rate and the life expectancy of countries over the years. Hans Rosling built this animation when, after testing his students on global health, he realized that they still thought that the world was divided in two: 
# - the western world: low fertility rate and high life expectancy
# - the third world: high fertilit rate and low life expectancy
# 
# There will be some differences between the original visualization and the one I am going to build:
# - more data. The talk was made in 2006 with data from 1962 to 2003. I will use data from 1960 to 2016.
# - regions. The original visualization has five regions. I will keep the regions from the source data (i.e. seven regions).
# - colors. I can't ge the exact colors of the regions. I'll use my own color mapping.

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import Image, display
get_ipython().run_line_magic('matplotlib', 'notebook')


# ## Prepare the data
# First, I load the data in separate dataframes

# In[ ]:


country = pd.read_csv('../input/world-telecommunications-data/Metadata_Country_API_IT.CEL.SETS.P2_DS2_en_csv_v2.csv')
population = pd.read_csv('../input/world-bank-data-1960-to-2016/country_population.csv')
fertility_rate = pd.read_csv('../input/world-bank-data-1960-to-2016/fertility_rate.csv')
life_expectancy = pd.read_csv('../input/world-bank-data-1960-to-2016/life_expectancy.csv')


# Then some preprocessing is needed.   
# For each dataset, I remove the countries that have missing values. Some of them have too many years with out data (all years in some cases).

# In[ ]:


def preprocess_df(df, value_name):
    """ remove missing values and put years in one column
    
    Parameters
    ----------
    df: dataframe
        the data that needs to be preprocessed

    value_name: string
        the name of the column that will contain the year's data

    Return
    ------
    preprocessed dataframe
    """
    years = [str(y) for y in range(1960, 2017)]
    
    # remove useless columns
    df.drop(['Country Name', 'Indicator Name', 'Indicator Code'], axis=1, inplace=True)

    # remove countries with missing value
    df.dropna(axis=0, inplace=True)

    # melt the dataframe to have years in one columns
    df = pd.melt(df,
                 id_vars='Country Code',
                 value_vars=years,
                 var_name='Year',
                 value_name=value_name)

    return df

country = country[['Country Code', 'Region']]
population = preprocess_df(population, 'Population')
fertility_rate = preprocess_df(fertility_rate, 'Fertility Rate')
life_expectancy = preprocess_df(life_expectancy, 'Life Expectancy')


# Now that the data has been cleaned up, I can merge all the datasets into one dataframe I will use to build the animation.

# In[ ]:


# Merge the data into one dataframe
df = pd.merge(country, population, how='left', on='Country Code')
df = pd.merge(df, life_expectancy, how='left', on=['Country Code', 'Year'])
df = pd.merge(df, fertility_rate, how='left', on=['Country Code', 'Year'])

# Remove remaining lines with missing values
# They will appear if a country is in one dataset but not in another one
df.dropna(axis=0, inplace=True)


# ## Build the animation 

# In[ ]:


# get a list of the years. I will create one frame per year.
years = df['Year'].unique().tolist()

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(df['Fertility Rate'].min() - .3,
            df['Fertility Rate'].max() + .3)
ax.set_ylim(df['Life Expectancy'].min() - 2,
            df['Life Expectancy'].max() + 2)

# set the regions' colors
colors = {
    'Latin America & Caribbean': '#2CA02C',
    'South Asia': '#8C564B',
    'Sub-Saharan Africa': '#E377C2',
    'Europe & Central Asia': '#FF7F0E',
    'Middle East & North Africa': '#D62728',
    'East Asia & Pacific': '#1F77B4',
    'North America': '#9467BD'
}

# create one scatterplot per region
# I need to do like this to have all the regions 
# showing up in the legend
scats = []
groups = df.groupby('Region')
for name, grp in groups:
    scat = ax.scatter([], [],
                    marker='o',
                    color=colors[name],
                    label=name,
                    edgecolor='silver',
                    alpha=.6)
    scats.append(scat)

# add the year in the middle of the scatter plot
# for now, the text is empty (''). Il will be filled 
# in each frame
year_label = ax.text(4.5, 50, '', va='center', ha='center', alpha=.1,
                    size=32, fontdict={'weight': 'bold'})

# decorate the visualization
ax.spines['bottom'].set_color('silver')
ax.spines['top'].set_color('silver')
ax.spines['right'].set_color('silver')
ax.spines['left'].set_color('silver')
ax.tick_params(
    labelcolor='silver',
    color='silver'
)
ax.set_xlabel('Fertility Rate', color='silver')
ax.set_ylabel('Life Expectancy', color='silver')
ax.legend(loc=1, fontsize=7)

# set the initial state
def init():
    for scat in scats:
        scat.set_offsets([])
    return scats,

# function that will update the figure with new data
def update(year):
    # I need to update all scatterplots one by one
    # and return a list of updated plots
    for scat, (name, data) in zip(scats, groups):
        # get the data for the current year
        sample = data[data['Year'] == year]
        # set the x and y values 
        scat.set_offsets(sample[['Fertility Rate', 'Life Expectancy']])
        # update the size of the markers with the population
        # of the current year
        scat.set_sizes(np.sqrt(sample['Population'] / 10000) * 5)
        year_label.set_text(year)
    return scats,

# generate the animation
ani = animation.FuncAnimation(fig, update, init_func=init,
                            frames=years,
                            interval=200,
                            repeat=True)

plt.show()


# In[ ]:


# save the animation as an animated gif file
ani.save('best_stat_anim.gif', dpi=80, writer='imagemagick')


# In[ ]:


display(Image(url='best_stat_anim.gif'))


# In[ ]:




