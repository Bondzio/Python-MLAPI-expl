#!/usr/bin/env python
# coding: utf-8

# # Make your own Dataset 
# ### Create dataset using beautifulsoup webscraper
# #### Example project for cnvrg.io

# ### Step 1: Import Libraries

# In[ ]:


#Packages
#--Web scraping packages
from bs4 import BeautifulSoup
import requests
#Pandas/numpy for data manipulation
import pandas as pd
import numpy as np


# ### Step 2: Collect URLs to Scrape

# In[ ]:


#load URLs we want to scrape into an array
BASE_URL = [
    'https://tradingeconomics.com/country-list/gdp-annual-growth-rate?continent=europe',
    'https://tradingeconomics.com/country-list/gdp-annual-growth-rate?continent=america',
    'https://tradingeconomics.com/country-list/gdp-annual-growth-rate?continent=asia',
    'https://tradingeconomics.com/country-list/gdp-annual-growth-rate?continent=africa',
    'https://tradingeconomics.com/country-list/gdp-annual-growth-rate?continent=australia'
]


# ### Step 3: Scrape!

# In[ ]:


#loading empty array for board members
items = []
#Loop through our URLs we loaded above
for b in BASE_URL:
    html = requests.get(b).text
    soup = BeautifulSoup(html, "html.parser")
    #identify table we want to scrape
    items_table = soup.find('table', {"class" : "table table-hover"})
    for row in items_table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) != 0:
            p=tuple([b])
            entries_list=[]
            for i in range(0,len(cols)):
                entries_list.append(cols[i].text.strip())
            entries_tuple=tuple(entries_list)
            info=()
            info=p+entries_tuple
            items.append(info)
#            items.append((b, cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip()))


# ### Step 4: Convert to Array

# In[ ]:


#convert output to new array
array = np.asarray(items)
#check length
print("Length of array is",len(array))


# ### Step 5: Convert to dataframe

# In[ ]:


#convert new array to dataframe
df = pd.DataFrame(array)
#Examine last entries
df.tail(5)


# ### Step 6: Label Columns

# In[ ]:


#rename columns, check output
df.columns = ['URL', 'Country', 'Last','Month/Year', 'Previous','Range','Unknown']
df.head()

