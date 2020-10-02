#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# # Region Level

# In[ ]:


df = pd.read_csv('/kaggle/input/covid19-in-italy/covid19_italy_region.csv')


# In[ ]:


max_date = df.Date.max()
print(max_date)


# In[ ]:


# select most recent data
df_select = df[df.Date==max_date]
df_select


# In[ ]:


n_regions = df_select.shape[0]
print('Number of regions: ', n_regions)


# In[ ]:


lat = 42
lon = 14
m = folium.Map([lat, lon], zoom_start=6)
for i in range(0,n_regions):
   folium.Circle(
      location=[df_select.Latitude.iloc[i], df_select.Longitude.iloc[i]],
      popup=df_select.RegionName.iloc[i]+'; cases: '+str(df_select.TotalPositiveCases.iloc[i]),
      radius=200*np.sqrt(df_select.TotalPositiveCases.iloc[i]),
      color='red',
      fill=True,
      fill_color='red'
   ).add_to(m)

# show map
m


# # Province Level

# In[ ]:


df_prov = pd.read_csv('/kaggle/input/covid19-in-italy/covid19_italy_province.csv')
df_prov = df_prov[df_prov.ProvinceName != 'In fase di definizione/aggiornamento']
df_prov = df_prov[df_prov.ProvinceName != 'In fase di definizione']
df_prov = df_prov[df_prov.ProvinceName != 'fuori Regione/P.A.']
df_prov = df_prov[df_prov.ProvinceName != 'Fuori Regione / Provincia Autonoma']


# In[ ]:


df_prov


# In[ ]:


max_date = df_prov.Date.max()
print(max_date)


# In[ ]:


# select most recent data
df_select_prov = df_prov[df_prov.Date==max_date]
df_select_prov


# In[ ]:


n_provs = df_select_prov.shape[0]
print('Number of provinces: ', n_provs)


# In[ ]:


lat = 42
lon = 14
m = folium.Map([lat, lon], zoom_start=6)
for i in range(0,n_provs):
   folium.Circle(
      location=[df_select_prov.Latitude.iloc[i], df_select_prov.Longitude.iloc[i]],
      popup=df_select_prov.ProvinceName.iloc[i]+'; cases: '+str(df_select_prov.TotalPositiveCases.iloc[i]),
      radius=200.0*np.sqrt(df_select_prov.TotalPositiveCases.iloc[i]),
      color='red',
      fill=True,
      fill_color='red'
   ).add_to(m)

# show map
m


# ## See also https://www.kaggle.com/docxian/corona-italia-region-province for more evaluations.
