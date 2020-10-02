#!/usr/bin/env python
# coding: utf-8

# ![](https://www.publicdomainpictures.net/pictures/110000/velka/classroom.jpg)
# 
# # DonorsChoose: Matching donors to causes
# 
# DonorsChoose is a US charity set up to raise funds for public school projects. They have partnered with Google.org and Kaggle in a drive to find a better solution for matching donors to particular projects in an attempt to motivate the donor to gift.
# 
# This kernel explores the data and tries to find the key indicators that suggest what kind of donors connect with what kind of project. My train of thought throughout revolves around the idea that to connect donors to projects via data science, we need information about both the potential donor and the project. This data set gives a good chunk of info about the projects, but not so much on the donors. What we do have, however, is:
# 
# - Their city and state
# - Whether they are a teacher involved in the project
# - Other projects they have donated too
# 
# I will therefore dig into these features and see if they lead to any strong donation indicators.
# 
# ## Table of contents
# 
# 1. Data loading
# 2. Geographical relationships - do people donate locally?
#     1. Donation destination Sankey
#     2. Heatmapping donation sources
#     3. Visualising in-state donor preference
#     4. California in-state donations
#     5. Out of state donations 
#     6. Differences between in-state and out-of-state donations
#         1. Word clouds
#         2. School percentage of free lunches
#         3. School metro type
#         4. Time series of donation types
# 3. Frequent donators - do they donate to the same kinds of project?
#     1. PCA of project info
#     2. Examining distances by donor in the project feature space
#     3. Example of a suggested project

# In[ ]:


import os
import gc
import glob
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA, KernelPCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import pairwise_distances_argmin_min, pairwise_distances
import warnings
from wordcloud import WordCloud, STOPWORDS
import random
warnings.filterwarnings('ignore')
py.init_notebook_mode(connected=True)
get_ipython().run_line_magic('matplotlib', 'inline')


# ## 1. Data loading
# 
# The data is provided in several files, so let's load them into their own dataframes and take a look. I can then merge them on the ID columns to concatenate the data as I need it as we go.

# In[ ]:


in_path = os.path.join(os.path.pardir, 'input')
in_files = glob.glob(os.path.join(in_path, '*.csv'))
print('Input files found:\n\t{}'.format('\n\t'.join(in_files)))


# In[ ]:


def describe_df(df, df_name):
    id_cols = df.columns[df.columns.str.contains('ID')]
    n_rows, n_cols = df.shape[0], df.shape[1]
    print('{:10} dataframe has {:8} rows, {:2} columns an ID keys: {}'          .format(df_name, str(n_rows), str(n_cols), ', '.join(id_cols)))

sample_size = None

donations_df = pd.read_csv('../input/Donations.csv', nrows=sample_size)
describe_df(donations_df, 'Donations')

donors_df = pd.read_csv('../input/Donors.csv', nrows=sample_size)
describe_df(donors_df, 'Donors')

projects_df = pd.read_csv('../input/Projects.csv', nrows=sample_size)
describe_df(projects_df, 'Projects')

resources_df = pd.read_csv('../input/Resources.csv', nrows=sample_size)
describe_df(resources_df, 'Resources')

schools_df = pd.read_csv('../input/Schools.csv', nrows=sample_size)
describe_df(schools_df, 'Schools')

teachers_df = pd.read_csv('../input/Teachers.csv', nrows=sample_size)
describe_df(teachers_df, 'Teachers')


# ## 2. Geographical relationships
# 
# The first relationship I would like to explore is that of the donor's location to the projects location. The hypothesis here might be that people connect better to projects nearby.
# 
# To do this, I'll need to connect donors to schools to get the right data.

# In[ ]:


donors_schools_df = donations_df.merge(donors_df, left_on='Donor ID', right_on='Donor ID')

donors_schools_df = donors_schools_df.merge(projects_df[['Project ID', 'School ID']], 
                                            left_on='Project ID', right_on='Project ID')

donors_schools_df = donors_schools_df.merge(schools_df, left_on='School ID', right_on='School ID')

donors_schools_df.head(3)


# ### 2.1 Donations destination Sankey
# 
# Before we go into detail on where the donations are headed, lets get a top level view of where the donations from the highest donating states are going.
# 
# Firstly, choose the top *n* states for donations:

# In[ ]:


top_n = 10  # How many to look at
top_donor_states = donors_schools_df.groupby('Donor State')['Donation Amount'].sum().sort_values(ascending=False)
top_donor_states.drop('other', inplace=True)  # Don't plot other, not interesting for now
top_donor_states = top_donor_states[:top_n]
fig, ax = plt.subplots(1, 1, figsize=[10, 5])
sns.barplot(y=top_donor_states.index, x=top_donor_states, ax=ax, palette=sns.color_palette('GnBu_d', top_n))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)  
ax.set_xlabel('Total Donation Amount ($)')
plt.show()


# Now lets use a Sankey plot to see where these donations usually go - **Note** I am going to restrict the minimum sum of inter-state donations to $250k for this plot, just so it doesn't get too messy.

# In[ ]:


# Limit data to include only those states that contain both donors and schools
school_states = donors_schools_df['School State'].unique()
donor_states = donors_schools_df['Donor State'].unique()
states_to_keep_mask = [x in school_states for x in donor_states]
states = donor_states[states_to_keep_mask]
donors_schools_df = donors_schools_df[donors_schools_df['School State'].isin(states)]
donors_schools_df = donors_schools_df[donors_schools_df['Donor State'].isin(states)]

# Pivot, summing the donations
pivot = donors_schools_df.pivot_table(columns='School State',
                                      index='Donor State', 
                                      values='Donation Amount', 
                                      aggfunc='sum',
                                      fill_value=0)

# Separate the top n donors
top_n_pivot = pivot.loc[top_donor_states.index, :]

# Remove any states that none of them donate too
top_n_pivot = top_n_pivot.loc[:, top_n_pivot.sum() > 0]

# Unpivot
donation_paths = top_n_pivot.reset_index().melt(id_vars='Donor State')
donation_paths = donation_paths[donation_paths['value'] > 250000]  # Only significant amounts

# Encode state names to integers for the Sankey
donor_encoder, school_encoder = LabelEncoder(), LabelEncoder()
donation_paths['Encoded Donor State'] = donor_encoder.fit_transform(donation_paths['Donor State'])
donation_paths['Encoded School State'] = school_encoder.fit_transform(donation_paths['School State'])    + len(donation_paths['Encoded Donor State'].unique())


# In[ ]:


# Create a state to color dictionary
all_states = np.unique(np.array(donation_paths['School State'].unique().tolist() + donation_paths['Donor State'].unique().tolist()))
plotly_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

states_finished = False
state_colors = []
i = 0
while not states_finished:
    
    state_colors.append(plotly_colors[i]) 
    
    if len(state_colors) >= len(all_states):
        states_finished = True
        
    i += 1
    if i >= len(plotly_colors):
        i = 0
        
color_dict = dict(zip(all_states, state_colors))


# In[ ]:


snky_labels = donor_encoder.classes_.tolist()  + school_encoder.classes_.tolist()
colors = []
for state in snky_labels:
    colors.append(color_dict[state])

data = dict(
    type='sankey',
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(
        color = "black",
        width = 0.5
      ),
      label = snky_labels,
      color = colors,
    ),
    link = dict(
      source = donation_paths['Encoded Donor State'],
      target = donation_paths['Encoded School State'],
      value = donation_paths['value'],
  ))

layout =  dict(
    title = "Donation Destination Sankey",
    autosize=False,
    width=800,
    height=750,

    font = dict(
      size = 10
    )
)

fig = dict(data=[data], layout=layout)
py.iplot(fig, validate=False)


# Great! So, the left hand nodes are all the donor states and the right are the school states. The thickness of the flows represents the donation sum passing to the school state - so California, New York and Texas are the widest as per the above bar chart.
# 
# So we can start to see here that donor's have a strong preference for donating to in-state schools - lets look into this a bit further.

# ### 2.2 Heatmapping donation sources

# In[ ]:


# Scale pivot plot by the funds that state receives
sum_state_funds = donors_schools_df.groupby('School State')['Donation Amount'].sum()
pivot = pivot / sum_state_funds.transpose()


# In[ ]:


fig, ax = plt.subplots(1, 1, figsize=[17, 10])
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(data=pivot, square=True, cmap=cmap, center=0,
            linewidths=.5, cbar=True, ax=ax)
ax.set_title('Heatmap of funding ratios from donor states to school states')
plt.show()


# Awesome, so we can see here by the strong diagonal present that most donors like to donate in-state. Also interesting are the horizontal lines across California and New York, suggesting those are the states where donors are more likely to donate elsewhere.
# 
# However, this may be skewed by teacher donations as they are highly likely to reside in the same state. Let's see if non-teacher donations follows a similar trend.

# In[ ]:


donors_schools_df = donors_schools_df[donors_schools_df['Donor Is Teacher'] == 'No']
pivot2 = donors_schools_df.pivot_table(columns='School State',
                                      index='Donor State', 
                                      values='Donation Amount', 
                                      aggfunc='sum',
                                      fill_value=0)

# Scale again by the funds that state receives
sum_state_funds = donors_schools_df.groupby('School State')['Donation Amount'].sum()
pivot2 = pivot2 / sum_state_funds.transpose()

fig, ax = plt.subplots(1, 1, figsize=[17, 10])
cmap = sns.diverging_palette(220, 270, as_cmap=True)
sns.heatmap(data=pivot2, square=True, cmap=cmap, center=0,
            linewidths=.5, cbar=True, ax=ax)
ax.set_title('Heatmap of funding ratios from donor states to school states - teacher donations excluded')
plt.show()


# OK, so in-state donor preference is definitely still a thing even when teacher donations are excluded. This probably isn't news to DonorsChoose, but what might be helpful is if we can quantify the strength of this preference by state. 
# 
# To do this, I'll take the diagonal values and plot them on a Plotly chloropeth. I have to give a big shoud out to sban here for their `state_to_code` dict in the fantastic kernel [here](https://www.kaggle.com/shivamb/deep-eda-interactive-maps-donorschoose) that allowed me to map the state names to the Plotly codes:

# ### 2.3 Visualising in-state donor preference

# In[ ]:


instate_pref = pd.DataFrame({'Donor State': pivot2.index, 'Preference': np.diagonal(pivot2)})
state_to_code = {'District of Columbia' : 'dc','Mississippi': 'MS', 'Oklahoma': 'OK', 'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR', 'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA', 'Idaho': 'ID', 'Wyoming': 'WY', 'Tennessee': 'TN', 'Arizona': 'AZ', 'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT', 'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT', 'California': 'CA', 'Massachusetts': 'MA', 'West Virginia': 'WV', 'South Carolina': 'SC', 'New Hampshire': 'NH', 'Wisconsin': 'WI', 'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND', 'Pennsylvania': 'PA', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY', 'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH', 'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD', 'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA', 'North Carolina': 'NC', 'New York': 'NY', 'Texas': 'TX', 'Nevada': 'NV', 'Maine': 'ME'}
instate_pref['State Code'] = instate_pref['Donor State'].map(state_to_code)


# In[ ]:


scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = instate_pref['State Code'],
        z = instate_pref['Preference'].astype(float),
        locationmode = 'USA-states',
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "In-state donation ratio")
        ) ]

layout = dict(
        title = 'Donor in-state preference by state',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig = dict( data=data, layout=layout )
py.iplot( fig, filename='d3-cloropleth-map' )


# We can infer from this plot that donors in Wyoming and South Dakota are the most likely to donate further afield, whilst Californians donate in-state most often. 
# 
# This is handy information for considering which projects might motivate a particular donor and suggests that most of the time it is likely to be something in-state.

# ### 2.4 California in-state donations
# 
# So it looks like most donations are in-state, but we also have information on what city the schools are donors are in. Let's take California, the biggest donor, and see how donations move between cities - again excluding those made by teachers.
# 
# Again, to keep the Sankey readable, only take the top few cities for donations and the minium sum of inter city donations is above $15000.

# In[ ]:


cali_df = donors_schools_df[(donors_schools_df['School State'] == 'California') &
                            (donors_schools_df['Donor State'] == 'California') &
                            (donors_schools_df['Donor Is Teacher'] == 'No')]
top_cities = cali_df.groupby('Donor City')['Donation Amount'].sum().sort_values(ascending=False)[:top_n]
fig, ax = plt.subplots(1, 1, figsize=[10, 5])
sns.barplot(y=top_cities.index, x=top_cities, ax=ax, palette=sns.color_palette('husl', top_n))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)  
ax.set_xlabel('Total Donation Amount ($)')
plt.show()


# In[ ]:


# Pivot, summing the donations
cali_df = cali_df[cali_df['Donor City'].isin(top_cities.index)]
city_pivot = cali_df.pivot_table(columns='School City',
                                      index='Donor City', 
                                      values='Donation Amount', 
                                      aggfunc='sum',
                                      fill_value=0)

# Unpivot
city_paths = city_pivot.reset_index().melt(id_vars='Donor City')
city_paths = city_paths[city_paths['value'] > 15000]  # Only significant amounts

# Encode state names to integers for the Sankey
donor_encoder_c, school_encoder_c = LabelEncoder(), LabelEncoder()
city_paths['Encoded Donor City'] = donor_encoder_c.fit_transform(city_paths['Donor City'])
city_paths['Encoded School City'] = school_encoder_c.fit_transform(city_paths['School City'])    + len(city_paths['Encoded Donor City'].unique())


# In[ ]:


# Create a state to color dictionary
all_cities = np.unique(np.array(city_paths['School City'].unique().tolist() + city_paths['Donor City'].unique().tolist()))

cities_finished = False
city_colors = []
i = 0
while not cities_finished:
    
    city_colors.append(plotly_colors[i]) 
    
    if len(city_colors) >= len(all_cities):
        cities_finished = True
        
    i += 1
    if i >= len(plotly_colors):
        i = 0
        
color_dict = dict(zip(all_cities, city_colors))


# In[ ]:


snky_labels = donor_encoder_c.classes_.tolist()  + school_encoder_c.classes_.tolist()
colors = []
for city in snky_labels:
    colors.append(color_dict[city])


data = dict(
    type='sankey',
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(
        color = "black",
        width = 0.5
      ),
      label = donor_encoder_c.classes_.tolist()  + school_encoder_c.classes_.tolist(),
      color = colors
    ),
    link = dict(
      source = city_paths['Encoded Donor City'],
      target = city_paths['Encoded School City'],
      value = city_paths['value'],
  ))

layout =  dict(
    title = "Inter-city donations (excl. teacher donations) in California",
    autosize=False,
    width=800,
    height=750,

    font = dict(
      size = 10
    )
)

fig = dict(data=[data], layout=layout)
py.iplot(fig, validate=False)


# So it looks as though the trend goes down to city level too, at least for California. Most donations stay within the city of the donor with the exception of Corte Madera.

# ### 2.5 Out of state donations
# 
# On the other hand, it might ge interesting to see which states have the most donors willing to donate out of state - and in particular to which states they are most likely to donate to.

# In[ ]:


state_lat_lon = {
    'Alabama': [32.806671,-86.791130],
    'Alaska': [61.370716,-152.404419],
    'Arizona': [33.729759,-111.431221],
    'Arkansas': [34.969704,-92.373123],
    'California': [36.116203,-119.681564],
    'Colorado': [39.059811,-105.311104],
    'Connecticut': [41.597782,-72.755371],
    'Delaware': [39.318523,-75.507141],
    'District of Columbia': [38.897438,-77.026817],
    'Florida': [27.766279,-81.686783],
    'Georgia': [33.040619,-83.643074],
    'Hawaii': [21.094318,-157.498337],
    'Idaho': [44.240459,-114.478828],
    'Illinois': [40.349457,-88.986137],
    'Indiana': [39.849426,-86.258278],
    'Iowa': [42.011539,-93.210526],
    'Kansas': [38.526600,-96.726486],
    'Kentucky': [37.668140,-84.670067],
    'Louisiana': [31.169546,-91.867805],
    'Maine': [44.693947,-69.381927],
    'Maryland': [39.063946,-76.802101],
    'Massachusetts': [42.230171,-71.530106],
    'Michigan': [43.326618,-84.536095],
    'Minnesota': [45.694454,-93.900192],
    'Mississippi': [32.741646,-89.678696],
    'Missouri': [38.456085,-92.288368],
    'Montana': [46.921925,-110.454353],
    'Nebraska': [41.125370,-98.268082],
    'Nevada': [38.313515, -117.055374],
    'New Hampshire': [43.452492,-71.563896],
    'New Jersey': [40.298904,-74.521011],
    'New Mexico': [34.840515,-106.248482],
    'New York': [42.165726,-74.948051],
    'North Carolina': [35.630066,-79.806419],
    'North Dakota': [47.528912,-99.784012],
    'Ohio': [40.388783,-82.764915],
    'Oklahoma': [35.565342,-96.928917],
    'Oregon': [44.572021,-122.070938],
    'Pennsylvania': [40.590752,-77.209755],
    'Rhode Island': [41.680893,-71.511780],
    'South Carolina': [33.856892,-80.945007],
    'South Dakota': [44.299782,-99.438828],
    'Tennessee': [35.747845,-86.692345],
    'Texas': [31.054487,-97.563461],
    'Utah': [40.150032,-111.862434],
    'Vermont': [44.045876,-72.710686],
    'Virginia': [37.769337,-78.169968],
    'Washington': [47.400902,-121.490494],
    'West Virginia': [38.491226,-80.954453],
    'Wisconsin': [44.268543,-89.616508],
    'Wyoming': [42.755966,-107.302490]
}


# In[ ]:


flight_paths = []
for i in pivot2.index:
    
    for j in pivot2.columns:
        
        # Only plot if significant
        if (pivot2.loc[i, j] > 0.05) * (i != j):
               
            flight_paths.append(
                dict(
                    type = 'scattergeo',
                    locationmode = 'USA-states',                           
                    lon = [state_lat_lon[i][1], state_lat_lon[j][1]],
                    lat = [state_lat_lon[i][0], state_lat_lon[j][0]],
                    mode = 'lines',
                    line = dict(
                        width = 10 * pivot2.loc[i, j],
                        color = 'blue',                        
                    ),
                    text = '{:.2f}% of {}\'s donations come from {}'.format(100 * pivot2.loc[i, j], j, i),
                )
            )
    
layout = dict(
        title = 'Strongest out of state donation patterns (hover for details)',
        showlegend = False, 
        geo = dict(
            scope='usa',
            #projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            #subunitcolor = "rgb(217, 217, 217)",
            #countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )
    
fig = dict(data=flight_paths, layout=layout)
py.iplot(fig)


# Interesting! Again we can see the donating power of California and New York. Although most of their donations are in-state, the absolute values are so high that they still contribute significantly to other states. The other hub is Texas, which donats quite a lot to surrounding states.
# 
# The most striking relationship here is California to Wyoming: Wyoming schools received roughly 40% of their donations from Californian donors.

# In[ ]:


# Clean up
del pivot, pivot2, city_pivot, teachers_df, schools_df, donors_df
gc.collect()


# ### 2.6 Differences between in-state and out-of-state donations
# 
# Are there any significant differences in the kinds of donations that are made out of state? This may help us understand what motivates someone to donate out-of-state. 
# 
# A good place to start might just be to visualise word clouds of the project descriptions.

# In[ ]:


donors_schools_df = donors_schools_df.merge(projects_df, left_on='Project ID', right_on='Project ID')
donors_schools_df['In State Flag'] = donors_schools_df['Donor State'] == donors_schools_df['School State']

def green_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return 'hsl({:d}, 80%, {:d}%)'.format(random.randint(85, 140), random.randint(60, 80))

def red_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return 'hsl({:d}, 80%, {:d}%)'.format(random.randint(0, 35), random.randint(60, 80))

fig, (ax, ax1) = plt.subplots(1, 2, figsize=[15, 7])

# In state descriptions
stopwords = set(STOPWORDS)
wc = WordCloud(width=500, height=400, stopwords=stopwords, collocations=True)
wc.generate(' '.join(donors_schools_df.loc[donors_schools_df['In State Flag'] == 1, 'Project Title'].astype(str)))
ax.imshow(wc.recolor(color_func=green_color_func), interpolation="bilinear")
ax.axis('off')
ax.set_title('In-state descriptions')

# Out of state descriptions
wc = WordCloud(width=500, height=400, stopwords=stopwords, collocations=True)
wc.generate(' '.join(donors_schools_df.loc[donors_schools_df['In State Flag'] == 0, 'Project Title'].astype(str)))
ax1.imshow(wc.recolor(color_func=red_color_func), interpolation="bilinear")
ax1.axis('off')
ax1.set_title('Out-of-state descriptions')

plt.show()


# Not a huge amount of difference other than greater variation in the in-state words likely a result of their being more donations there. Lets look at some other features for a difference.

# #### 2.6.2 School percentage of free lunches
# 
# Lets look at the differences in the amount of free lunches in the in-state schools and out-of-state schools, assuming that this is a rough proxy for the affluence of the school.**

# In[ ]:


fig, ax = plt.subplots(1, 1, figsize=[10, 6])
sns.kdeplot(donors_schools_df.loc[donors_schools_df['In State Flag'] == 1, 'School Percentage Free Lunch'], shade=True, label='In-state')
sns.kdeplot(donors_schools_df.loc[donors_schools_df['In State Flag'] == 0, 'School Percentage Free Lunch'], shade=True, label='Out-of-state')
ax.get_yaxis().set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False) 
ax.spines['left'].set_visible(False) 
ax.set_xlabel('School percentage free lunch (%)')
ax.legend(frameon=False)
plt.show()


# The out-of-state donations appear to have a higher peak at >80% free lunch, which suggests that out-of-state donations might be motivated by the recipient school being in special need of charitable help.
# 
# #### 2.6.3 School metro type
# 
# Another difference might be in metro types of the schools - following the above point you maight expect that out-of-state donations go to inner-city schools where affluence can sometimes be lower.

# In[ ]:


instate_types = donors_schools_df[donors_schools_df['In State Flag'] == 1].groupby('School Metro Type')['Donation Amount'].sum().reset_index()
instate_types['Donation Amount'] = instate_types['Donation Amount'] / instate_types['Donation Amount'].sum()  # Normalise
instate_types['instate'] = 'In-state'
outstate_types = donors_schools_df[donors_schools_df['In State Flag'] == 0].groupby('School Metro Type')['Donation Amount'].sum().reset_index()
outstate_types['Donation Amount'] = outstate_types['Donation Amount'] / outstate_types['Donation Amount'].sum()
outstate_types['instate'] = 'Out-of-state'
types = instate_types.append(outstate_types)

fig, ax = plt.subplots(1, 1, figsize=[10, 6])
sns.barplot(x=types['School Metro Type'], y=types['Donation Amount'], hue=types['instate'], palette=sns.color_palette('Blues', 2))

ax.set_ylabel('Donation Amount Proportion')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False) 
ax.set_xlabel('School Metro Types')
ax.legend(frameon=False)
plt.show()


# And that idea doesn't really seem to be the case. In fact, it seems that rural schools are more popular out-of-state at the expense of suburban ones.
# 
# Therefore, if we were to suggest an out-of-state donation to a donor, it may be better to suggest a lower affluence, rural school.

# > #### 2.6.4 Time series of donation types
# 
# Has one or the other become more popular over time?

# In[ ]:


donors_schools_df['Donation Received Date'] = pd.to_datetime(donors_schools_df['Donation Received Date'], infer_datetime_format=True)
donors_schools_df['Donation Received Month'] = donors_schools_df['Donation Received Date'].dt.to_period('M')
monthly_donations = donors_schools_df.groupby(['Donation Received Month', 'In State Flag'])['Donation Amount'].sum().reset_index()

fig, ax = plt.subplots(1, 1, figsize=[12, 5])
monthly_donations[monthly_donations['In State Flag'] == 1].plot(x='Donation Received Month', y='Donation Amount', ax=ax, label='In-state', color='C0')
ax.tick_params(axis='y', labelcolor='C0')
ax.set_ylabel('Total in-state donations ($)')

ax1 = ax.twinx()
monthly_donations[monthly_donations['In State Flag'] == 0].plot(x='Donation Received Month', y='Donation Amount', ax=ax1, label='Out-of-state', color='C1')
ax1.tick_params(axis='y', labelcolor='C1')
ax1.set_ylabel('Total out-of-state donations ($)')

for a in [ax, ax1]:
    a.spines['top'].set_visible(False)
    a.set_xlabel('')

lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax1.get_legend_handles_labels()
ax.legend_.remove()
ax1.legend(lines + lines2, labels + labels2, loc=0, frameon=False)
#ax.legend(frameon=False)
ax.grid(linestyle='--', color='lightgrey')
plt.show()


# Hmm not really, both trends are essentially the same. They experience both the same irregular peaks and the same underlying growth.

# In[ ]:


del donors_schools_df


# ## 3. Frequent Donators
# 
# I could be interesting to look at those donators who have donated several times and see how similar the causes are. Lets see what the distribution of the numbers of donation per donor looks like.

# In[ ]:


donor_projects = projects_df.merge(donations_df, left_on='Project ID', right_on='Project ID')
donor_frequency = donor_projects.groupby('Donor ID')['Project ID'].nunique()


# In[ ]:


fig, (ax, ax1) = plt.subplots(1, 2, figsize=[15, 5])
sns.distplot(donor_frequency, ax=ax)
ax.set_title('Distribution of no. of donations')
sns.kdeplot(donor_frequency, ax=ax1)
ax1.set_title('KDE plot of no. of donations')
for a in [ax, ax1]:
    a.set_xlabel('No. of donations')
plt.show()


# ![](http://)Understandably, it is heavily right-skewed with most donors only donating a handful of times but with a few tail observations donating thousands of times. Let's look at some counts to get a better understanding so we can choose which group to have a look at patterns for.

# In[ ]:


donations = [1, 2, 3, 4, 5, 10, 20]
for d in donations:
    donor_perc = 100 * sum(donor_frequency > d) / len(donor_frequency)
    print('{:4.2f}% of donors donated to more than {} project(s).'.format(donor_perc, d))


# So the majority of people only donate once, reducing the pool of data we have for this section. Ideally, I would want to look at people who have donated to >5 projects to get a good sense of any patterns, but that limits the data available a lot. Lets look at >3 for now.

# In[ ]:


frequent_donors = donor_frequency[donor_frequency > 3]
frequent_donors = frequent_donors.index.tolist()
donor_projects = donor_projects[donor_projects['Donor ID'].isin(frequent_donors)].sort_values(by='Donor ID')


# ### 3.1 PCA of project info
# 
# To measure how similar different projects are so that I can test the hypothesis that donors donate to similar projects, I am going to use PCA to reduce the feature space to a smaller number of dimensions with high variance.
# 
# I chose PCA over T-SNE as although there are a lot of categorical features, I want the distance between the points to remain meaningful. Since this means I have to label/one-hot encode first, I want to check the cardinality of the project features so I can keep the number of final columns in check.

# In[ ]:


project_feats = ['Project ID', 'School ID', 'Teacher ID',
       'Teacher Project Posted Sequence', 'Project Type', 'Project Title',
       'Project Subject Category Tree', 'Project Subject Subcategory Tree', 'Project Grade Level Category',
       'Project Resource Category', 'Project Cost', 'Project Posted Date']
cat_feats = ['Project ID', 'School ID', 'Teacher ID', 'Project Type', 'Project Title',
       'Project Subject Category Tree', 'Project Subject Subcategory Tree', 
       'Project Grade Level Category', 'Project Resource Category']
model_feats = ['Project Cost', 'Teacher Project Posted Sequence']
for feat in donor_projects[cat_feats]:
    print('Feature {} has cardinality: {}'.format(feat, len(donor_projects[feat].unique())))
    if len(donor_projects[feat].unique()) < 100:
        model_feats.append(feat)


# I don't really want to use anything with cardinality over 100, so I'll only be using a few of these

# In[ ]:


# Remove dollar sign from project cost and convert to float
# donor_projects['Project Cost'] = donor_projects['Project Cost'].str[1:].str.replace(',','').astype(np.float32)
model_data = pd.get_dummies(donor_projects[model_feats])
model_data.head()


# In[ ]:


reducer = PCA(n_components=3)  # Limit to 3 so we can visualise
scaler = StandardScaler()
scaled_data = scaler.fit_transform(model_data)
transformed_data = reducer.fit_transform(scaled_data)
del model_data, scaled_data, projects_df, donations_df
gc.collect()


# In[ ]:


points_to_plot = 10000
random_index = np.random.choice(np.arange(len(transformed_data)), points_to_plot)
trace = go.Scatter3d(
    x=transformed_data[random_index, 0],
    y=transformed_data[random_index, 1],
    z=transformed_data[random_index, 2],
    mode='markers',
    marker=dict(
        size=5,
        opacity=0.8
    )
)

layout = go.Layout(
    title='Feature space reduced to 3D',
    margin=dict(
        l=0,
        r=0,
        b=40,
        t=40
    )
)
fig = go.Figure(data=[trace], layout=layout)
py.iplot(fig)


# Now we can visualise the project feature space, lets color some of them by their donor to viusally inspect how similar each donor's projects are:

# In[ ]:


donors_to_plot = np.random.choice(donor_projects['Donor ID'].unique(), 5)

trace = go.Scatter3d(
    x=transformed_data[random_index, 0],
    y=transformed_data[random_index, 1],
    z=transformed_data[random_index, 2],
    mode='markers',
    name='All projects',
    marker=dict(
        size=5,
        opacity=0.05
    )
)
data = [trace]

for donor in donors_to_plot:
    
    donor_mask = donor_projects['Donor ID'] == donor
    
    trace = go.Scatter3d(
        x=transformed_data[donor_mask, 0],
        y=transformed_data[donor_mask, 1],
        z=transformed_data[donor_mask, 2],
        mode='markers',
        name='Donor {}'.format(donor),
        marker=dict(
            size=5,
            opacity=0.8
        )
    )
    data.append(trace)

layout = go.Layout(
    title='Proximity of donor\'s projects in 3D feature space',
    margin=dict(
        l=0,
        r=0,
        b=40,
        t=40
    )
)
fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


# ### 3.2 Examining distances by donor in the project feature space
# 
# So the visual inspection above is fairly inconclusive - it is difficult to categorically say that donors like to donate to similar projects (although it looks like they might do).
# 
# In this step, lets look at the distances between the points in this feature space to quantify whether projects donated to be the same donor are closer than the rest.

# In[ ]:


pwise_distances = pairwise_distances(transformed_data[random_index, :], transformed_data[random_index, :])
diff_projects_mask = pwise_distances.sum(axis=0) > 0
mean_distance = pwise_distances[diff_projects_mask, :].mean()
print('Average pairwise distance between points =\t\t{:.2f}'.format(mean_distance))

donor_distances = []
for donor in donor_projects['Donor ID'].unique()[:100]:  # Takes ages on the server, should vectorise
    donor_mask = donor_projects['Donor ID'] == donor
    d_pwise_distances = pairwise_distances(transformed_data[donor_mask, :], transformed_data[donor_mask, :])
    
    diff_projects_mask = d_pwise_distances.sum(axis=0) > 0
    if sum(diff_projects_mask) == 0:
        print('Not calculating avg. distance for donor {} as all donations to same project')
        continue
        
    d_mean_distance = d_pwise_distances[diff_projects_mask, :].mean()
    donor_distances.append(d_mean_distance)
print('Average pairwise distance between donor\'s points =\t{:.2f}'.format(np.mean(donor_distances)))
print('Donor\'s points are rougly {:.2f}% closer together'.format(100 * (mean_distance - np.mean(donor_distances)) / mean_distance))


# We can therefore see that there is some preference for similar projects by the donor's. Additionally, looking at the distribution of the average distances between each donor's project below, we can see the peak comes significantly lower than the overall average distance between projects.

# In[ ]:


fig, ax = plt.subplots(1, 1, figsize=[10, 5])
sns.distplot(donor_distances, label='Distance between donor\'s projects', ax=ax)
ax.plot([mean_distance, mean_distance], [0, 1], color='k', linestyle='--', label='Average distance between projects')
ax.set_xlabel('Distance between projects in 3D feature space')
ax.legend()
plt.show()


# ### 3.3 Example project recommendation

# So as a first stage simple recommender, we could recommend the closest point in the feature space to the donor's current projects.
# 
# Looking at the features for a random donor's current projects...

# In[ ]:


random_donor = np.random.choice(donor_projects['Donor ID'].unique(), 1)[0]
donor_projects.loc[donor_projects['Donor ID'] == random_donor, project_feats].head(5)


# And then the closest project to their average position...

# In[ ]:


donors_average_coord = transformed_data[donor_projects['Donor ID'] == random_donor, :].mean(axis=0)
closest, _ = pairwise_distances_argmin_min(donors_average_coord.reshape(1, -1), transformed_data)
closest_proj = donor_projects.iloc[closest, :]
closest_proj[project_feats]

