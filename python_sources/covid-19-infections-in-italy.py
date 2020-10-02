#!/usr/bin/env python
# coding: utf-8

# # COVID-19 Infections in Italy
# 
# * Using data from https://github.com/pcm-dpc/COVID-19

# In[ ]:


import pandas as pd
import plotly.express as px
data = pd.read_csv('/kaggle/input/coronavirus-in-italy/dati-regioni/dpc-covid19-ita-regioni-20200329.csv') # Update every time
data[['denominazione_regione','totale_attualmente_positivi','deceduti']].sort_values('totale_attualmente_positivi',ascending=False).head(10)


# In[ ]:


fig = px.scatter_geo(data, lat='lat',lon='long',scope='europe',color="totale_attualmente_positivi",
                     hover_name="denominazione_regione", size="totale_attualmente_positivi",
                     projection="natural earth",title='COVID-19 Infections in Italy')
fig.show()


# In[ ]:


print('Last updated 3/29/2020')

