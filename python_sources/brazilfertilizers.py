#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# In[ ]:


df = pd.read_csv('/kaggle/input/fertilizers-by-product-fao/FertilizersProduct.csv', encoding='ISO-8859-1')
df


# In[ ]:


# Drop irrelevant columns
df.drop(['Area Code','Item Code', 'Element Code', 'Year Code', 'Flag'],inplace=True,axis=1)


# Get only Brazil info

# In[ ]:


df_br = df.loc[df.Area == 'Brazil']


# In[ ]:


agr_usage = df_br.loc[df_br.Element == 'Agricultural Use']
agr_usage.sort_values(by=['Value'], ascending=False)


# # Analysing agricultural use of fertilizers:

# In[ ]:


fig = px.area(agr_usage, x="Year", y="Value", color="Item", line_group="Item", title='Agricultural usage of fertilizers in Brazil')
fig.show()


# Urea is the most used fertilizer in Brazil

# Agricultural usage of fertilizers by country in 2017

# In[ ]:


usage_global = df.loc[(df.Element == 'Agricultural Use')  & (df.Year == 2017)]
countries = df.Area.unique()
cdf = []
adf = []
for country in countries:
    df_aux = usage_global.loc[usage_global.Area == country]
    amount = df_aux.Value.sum()
    cdf.append(country)
    adf.append(amount)
df_fert = pd.DataFrame({'Country': cdf, 'Amount': adf})
df_fert = df_fert.sort_values(by=['Amount'], ascending=False)


# In[ ]:


fig = px.bar(df_fert, x=df_fert.Country[:10], y=df_fert.Amount[:10], title='Countries with higher fertilizer use in 2017', color=df_fert.Amount[:10],
             labels={'x': 'Country', 'y': 'Amount (tonnes)', 'color': 'Amount (t)'})
fig.show()


# # Production and Export of fertilizers in Brazil

# In[ ]:


fert_prod = df_br.loc[df_br.Element == 'Production']
fert_prod.sort_values(by=['Value'], ascending=False)


# In[ ]:


fig = px.area(fert_prod, x="Year", y="Value", color="Item", line_group="Item", title='Production of fertilizers in Brazil')
fig.show()


# Urea is the most produced fertilizer in Brazil

# In[ ]:


urea_export = df_br.loc[(df_br.Item == 'Urea') & (df_br.Element == 'Export Value')]
urea_export


# In[ ]:


fig = px.line(urea_export, x="Year", y="Value", title='Exportation of Urea in Brazil (x1000 US$)')
fig.show()


# Total exportation of Urea 2002-2017 in US$:

# In[ ]:


import math

millnames = ['',' Thousand',' Million',' Billion',' Trillion']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


# In[ ]:


total = urea_export['Value'].sum()
print (f'Brazil exported US$ {millify(total*1000)} of Urea')

