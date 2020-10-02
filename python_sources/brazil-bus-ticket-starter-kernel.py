#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_cell_magic('capture', '', '!pip install -U networkx')


# In[ ]:


import pandas as pd
from unidecode import unidecode
import networkx as nx
import matplotlib.pyplot as plt


# In[ ]:


PATH = '/kaggle/input/brazil-interstate-bus-travels/venda_passagem_03_2019/venda_passagem_03_2019.csv'
PATH2 = '/kaggle/input/brazilian-cities/BRAZIL_CITIES.csv'


# In[ ]:


cities_data = (pd.read_csv(PATH2, delimiter=';')
                 .assign(CITY=lambda df: df.CITY.map(unidecode).str.upper()))


# In[ ]:


raw_data = pd.read_csv(PATH, delimiter=';', encoding='iso-8859-1')


# In[ ]:


def separate_location(df):
    location_start = (df.ponto_origem_viagem
                        .str.split("/")
                        .apply(pd.Series)
                        .rename(columns={0: 'city_start', 1: 'state_start'}))
    location_end = (df.ponto_destino_viagem
                      .str.split("/")
                      .apply(pd.Series)
                      .rename(columns={0: 'city_end', 1: 'state_end'}))
    return df.join(location_start).join(location_end)




cols = ['city_start', 'city_end', 'numero_bilhete'] 
data = (raw_data
                .pipe(separate_location)
                .loc[:, cols])


# In[ ]:


s = data.groupby(['city_start', 'city_end']).count().rename(columns={'numero_bilhete': 'travel_count'})


# In[ ]:


city_data = cities_data.set_index(['CITY']).loc[:, ['IBGE_RES_POP', 'LAT', 'LONG']]


# In[ ]:


start = s.droplevel(0).join(city_data)
end = s.droplevel(-1).join(city_data)


# In[ ]:


ndf = (s.reset_index()
        .join(city_data, on='city_start')
        .join(city_data, on='city_end', lsuffix='_end')
      )


# In[ ]:


graph = nx.from_pandas_edgelist(ndf, 'city_start', 'city_end', 'travel_count')


# In[ ]:


edges = graph.edges()
weights = np.array([graph[u][v]['travel_count'] for u,v in edges])
weights = np.sqrt(weights)
weights = 3 * weights / weights.max()


# In[ ]:


plt.figure(figsize=(40, 20), dpi=200)
nx.draw(graph, node_size=3, width=weights, with_labels=True, font_size=7)
plt.show()


# In[ ]:




