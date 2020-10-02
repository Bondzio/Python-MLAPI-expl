#!/usr/bin/env python
# coding: utf-8

# This is just a small kernel to show how to use googlemaps package to map location strings to GPS coords. You could use it to merge your external dataset to kiva loans by region.
# 
# Check out my main [kernel](https://www.kaggle.com/gaborfodor/external-data-for-kiva-crowdfunding) and the related [dataset](https://www.kaggle.com/gaborfodor/additional-kiva-snapshot) too!

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
pd.options.mode.chained_assignment = None
pd.options.display.max_columns = 99

import IPython.display as display
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go


# In[ ]:


competition_data_dir = '../input/data-science-for-good-kiva-crowdfunding/'
additional_data_dir = '../input/additional-kiva-snapshot/'


# ### Read the loans

# In[ ]:


loans = pd.read_csv(additional_data_dir + 'loans.csv')
regions = loans.groupby(['country_code', 'country_name', 'town_name']).count()[['loan_id']]
regions = regions.reset_index()
regions.columns = ['country_code', 'country_name', 'town_name', 'cnt']
regions = regions.sort_values(by='cnt', ascending=False)


# In[ ]:


location_names = []
for country, town in regions[['country_name', 'town_name']].values:
    if country not in town:
        location_name = '{}, {}'.format(town, country)
    else:
        location_name = town
    location_names.append(location_name)
regions['location_name'] = location_names
regions.shape
regions.head(3)


# ### Let's check Kaduna, Nigeria

# In[ ]:


display.Image(filename='../input/additional-kiva-snapshot/KadunaNigeria.png', width=1000) 
get_ipython().system('cp ../input/additional-kiva-snapshot/gmaps.png .')


# The [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/start) is actually quite easy to use. You could get it working with 4 lines. 
# 
# ```
# # pip install -U googlemaps
# import googlemaps
# gmaps = googlemaps.Client(key='YourAPIKey')
# gmaps.geocode('Kaduna, Nigeria')
# 
# ```

# In[ ]:


[{'address_components': [{'long_name': 'Kaduna',
    'short_name': 'Kaduna',
    'types': ['locality', 'political']},
   {'long_name': 'Kaduna',
    'short_name': 'KD',
    'types': ['administrative_area_level_1', 'political']},
   {'long_name': 'Nigeria',
    'short_name': 'NG',
    'types': ['country', 'political']}],
  'formatted_address': 'Kaduna, Nigeria',
  'geometry': {'bounds': {'northeast': {'lat': 10.6169963,
     'lng': 7.508812000000001},
    'southwest': {'lat': 10.3971566, 'lng': 7.349789099999999}},
   'location': {'lat': 10.5104642, 'lng': 7.4165053},
   'location_type': 'APPROXIMATE',
   'viewport': {'northeast': {'lat': 10.6169963, 'lng': 7.508812000000001},
    'southwest': {'lat': 10.3971566, 'lng': 7.349789099999999}}},
  'place_id': 'ChIJdRc3NFg1TRARdOG_mpeVAUg',
  'types': ['locality', 'political']}]


# The location names are already parsed and ready to use in this external dataset in **locations.csv**.

# In[ ]:


locations_df = pd.read_csv(additional_data_dir + 'locations.csv')
locations_df.head(3)
locations_df.shape


# Let's remove the duplications.

# In[ ]:


coords = locations_df.groupby('location_name').mean()[['geometry.location.lat',
                                                       'geometry.location.lng']]
coords = coords.reset_index()
coords.columns = ['location_name', 'latitude', 'longitude']
coords.head()


# In[ ]:


loan_coords = loans.merge(regions, on=['country_code', 'country_name', 'town_name'])
loan_coords = loan_coords[['loan_id', 'location_name']].merge(coords, on='location_name')
loan_coords = loan_coords[['loan_id', 'latitude', 'longitude']]
loan_coords.shape
loan_coords.head()


# Actually **loan_coords.csv** is available in the dataset as well.

# In[ ]:


loan_coords = pd.read_csv(additional_data_dir + 'loan_coords.csv')
loan_coords.head(3)
loans_with_coords = loans[['loan_id', 'country_name', 'town_name']]
loans_with_coords = loans_with_coords.merge(loan_coords, how='left', on='loan_id')
matched_pct = 100 * loans_with_coords['latitude'].count() / loans_with_coords.shape[0]
print("{:.1f}% of loans in loans.csv were"
      " successfully merged with loan_coords.csv".format(matched_pct))
print("We have {} loans in loans.csv"
      " with coordinates.".format(loans_with_coords['latitude'].count()))


# In[ ]:


town_counts = loans_with_coords.groupby(['country_name', 'town_name', 'latitude', 'longitude']).count()[['loan_id']].reset_index()
town_counts.columns = ['country_name', 'town_name', 'latitude', 'longitude', 'loan_cnt']
town_counts = town_counts.sort_values(by='loan_cnt', ascending=False)
town_counts.shape
town_counts.head()


# In[ ]:


data = [dict(
    type='scattergeo',
    lon = town_counts['longitude'],
    lat = town_counts['latitude'],
    text = town_counts['town_name'],
    mode = 'markers',
    marker=dict(
        sizemode = 'diameter',
        sizeref = 1,
        size= 5 * (np.log10(town_counts.loan_cnt + 1) - 1),
        color = np.log10(town_counts['loan_cnt'] + 1),
        opacity = 0.7,
        line = dict(width=0),
        colorscale='Reds',
        reversescale=False,
        showscale=True
    ),
)]
layout = dict(
    title = 'Number of Loans by Region (Enhanced)',
    hovermode='closest',
    geo = dict(showframe=False, showland=True, showcoastlines=True, showcountries=True,
               countrywidth=1, projection=dict(type='Mercator'))
)
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='all-town-loans')

