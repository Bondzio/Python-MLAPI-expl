#!/usr/bin/env python
# coding: utf-8

# # A quick look at Buenos Aires neighborhoods
# Let's see what we can learn about Buenos Aires neighborhoods with this little dataset.

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-white')


# In[ ]:


df = pd.read_csv('../input/lands-of-buenos-aires-prices/ba_lands_2014-2018.csv')


# Some figures to get started. Pay attention to the _log_ transormation!

# In[ ]:


fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(16,5))

x, y = np.log10(df['M2']), np.log10(df['USD'])

ax1.hist(x, bins=20)
ax1.set_xlabel('log M2')

ax2.hist(y, bins=20)
ax2.set_xlabel('log USD')

ax3.scatter(x, y, s=3)
ax3.set_xlabel('log M2')
ax3.set_ylabel('log USD')

plt.show()


# Look for the most cheap and most expensive neighborhood.

# In[ ]:


df['USD_PER_M2'] = df['USD'].divide(df['M2'])
mean_by_neighborhood = df.groupby('NEIGHBORHOOD').mean()[['USD_PER_M2']]
mean_by_neighborhood.columns = ['NEIGHBORHOOD_MEAN_M2']

mean_by_neighborhood.reset_index(inplace=True)
mean_by_neighborhood.sort_values(by='NEIGHBORHOOD_MEAN_M2', ascending=False, inplace=True)
mean_by_neighborhood.reset_index(drop=True, inplace=True)


# In[ ]:


# Top 10 most expensive neighborhoods
mean_by_neighborhood.head(10)


# In[ ]:


# Top 10 cheapest neighborhoods
mean_by_neighborhood.tail(10)


# Now visualize this information with a choropleth map.

# In[ ]:


import folium


# In[ ]:


df.dropna(inplace=True)


# In[ ]:


map_ba = folium.Map(location=[-34.603722, -58.381592], zoom_start=12)

map_ba.choropleth(geo_data='../input/lands-of-buenos-aires-prices/neighborhoods.geojson', 
             key_on = 'feature.properties.barrio', 
             data = mean_by_neighborhood, 
             columns = ['NEIGHBORHOOD', 'NEIGHBORHOOD_MEAN_M2'],
             fill_color = 'YlGn',
             fill_opacity = 0.7,
             line_opacity = 0.7,
             legend_name = 'Price per square meter in USD'
            )


# In[ ]:


map_ba

