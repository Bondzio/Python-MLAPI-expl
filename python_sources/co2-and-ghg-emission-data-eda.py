#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style("darkgrid")


# In[ ]:


df = pd.read_csv("../input/co2-and-ghg-emission-data/emission data.csv")
df.head()


# In[ ]:


list(df['Country'].unique())


# In[ ]:


print(f'Number of country is:  {len(df["Country"].unique())}')


# In[ ]:


df = df.set_index('Country').T


# In[ ]:


df = df.drop(['World'], axis=1)

df.head()


# In[ ]:


df.columns


# In[ ]:





# In[ ]:


df_country = df.loc[:,'Africa']

#ploting graph

plt.figure(figsize=(20,7))
sns.lineplot(data=df_country, marker="o")
plt.xlabel("Year")
plt.ylabel("CO2 and GHG Emission")
plt.title("CO2 and GHG Emission by Year")
plt.xticks(['1765','1780','1795','1810','1825','1840','1855','1870','1885','1900','1915','1930','1945','1960','1975','1990','2005','2020'],            rotation=45)


# In[ ]:


df_country = df.loc[:,'India']

#ploting graph

plt.figure(figsize=(20,7))
sns.lineplot(data=df_country, marker="o")
plt.xlabel("Year")
plt.ylabel("CO2 and GHG Emission")
plt.title("CO2 and GHG Emission by Year")
plt.xticks(['1765','1780','1795','1810','1825','1840','1855','1870','1885','1900','1915','1930','1945','1960','1975','1990','2005','2020'],            rotation=45)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




