#!/usr/bin/env python
# coding: utf-8

# ![img](https://www.uib.no/sites/w3.uib.no/files/styles/content_main_wide_1x/public/media/corona_0.jpg?itok=nY-uRO-n&timestamp=1582750728)

# Last Updated On

# In[ ]:


from datetime import datetime
print(datetime.now().strftime('%d-%m-%Y %I:%M %p'))


# ## [For Live Updates Open This Notebook in Colab](https://colab.research.google.com/github/prasadpatil99/Web-Scraping/blob/master/Web-Scraping-Covid-19-Cases/LIVE-Covid-19-Updates-Of-India-%26-Other-Countries..ipynb#scrollTo=qym-mhuqYD8u)

# ## Data Gathering
# ### For cases across the world

# In[ ]:


import numpy as np
import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


wd_url = "https://www.worldometers.info/coronavirus/"
req= requests.get(wd_url)
data=req.text
soup=BeautifulSoup(data,'html.parser')

table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')


# In[ ]:


country = []
totalcases = []
newcases = []
totaldeaths = []
newdeaths =[]
totalrecovered = []

for tr in table_rows:
    td = tr.find_all('td')
    country.append(td[1].text)
    totalcases.append(td[2].text.strip())
    newcases.append(td[3].text.strip())
    totaldeaths.append(td[4].text.strip())
    newdeaths.append(td[5].text.strip())
    totalrecovered.append(td[6].text)


# In[ ]:


df1 = pd.DataFrame({'Country':country, 'TotalCases':totalcases, 'NewCases':newcases, 
                    'TotalDeaths':totaldeaths, 'NewDeaths':newdeaths, 'TotalRecovered':totalrecovered})
df = df1.loc[8:]
df.head()


# In[ ]:


df_world = pd.DataFrame(df1.loc[7])
df_world.drop(["Country"],inplace=True)
df_world.head()


# Removing symbols and replacing null values from dataframe

# In[ ]:


def null_values(data):
    data.fillna(0, inplace=True)
    return data
df = null_values(df)


# In[ ]:


def preprocess(data):
    for cols in data:
        data[cols] = data[cols].map(lambda x: str(x).replace(',',''))
        data[cols] = data[cols].map(lambda x: str(x).replace('+',''))
        data[cols] = data[cols].map(lambda x: str(x).replace('\n',''))
preprocess(df_world)
preprocess(df)


# **For cases in India**

# In[ ]:


res = requests.get("https://www.mohfw.gov.in")
soup = BeautifulSoup(res.content,'lxml') 
table = soup.find_all('table')[0]
df_Ind = pd.read_html(str(table))[0]
state = df_Ind["Name of State / UT"].tolist()
cases = df_Ind["Total Confirmed cases*"].tolist()
cured = df_Ind["Cured/Discharged/Migrated*"].tolist()
deaths = df_Ind["Deaths**"].tolist()


# In[ ]:


df_Ind = pd.DataFrame({'States':state, 'Cases':cases, 'Cured':cured, 'Death':deaths})
df_Indtotal = df_Ind.loc[[36]]
df_Ind = df_Ind.loc[:(len(df_Ind)-7)]
df_Ind.head()


# In[ ]:


import pandas as pd 
import plotly.express as px

import cufflinks
from plotly.offline import iplot
cufflinks.go_offline()


# ## Data Visualisation - World

# In[ ]:


df_world.head()


# In[ ]:


df_world.iplot(kind='bar',title="World's Total Cases, New Cases, Total Deaths, New Deaths & Total Recovered")


# In[ ]:


df_newcases = df.copy()
df_newcases["NewCases"] = pd.to_numeric(df_newcases["NewCases"])
df_newcases["NewDeaths"] = pd.to_numeric(df_newcases["NewDeaths"])
df_newcases=df_newcases.sort_values(by = ["NewCases"], ascending = False)
df_newcases = df_newcases[(df_newcases['NewCases']>0) & (df_newcases['NewDeaths']>0)]

fig = px.bar(df_newcases, x='Country', y ='NewCases', color='Country',text='NewCases', height=500, width=1500, 
             title ="Today's New Cases Across Countries")
fig.show()


# In[ ]:


#df["TotalRecovered"] = pd.to_numeric(df["TotalRecovered"])
df=df.sort_values(by = ["TotalRecovered"], ascending = False).head(50)

df.iplot(
    x='Country',
    y=['TotalRecovered'],
    mode='lines',
    size=8,
    title="Top 50 Countries With Recovered Cases")


# In[ ]:


df_newcases.iplot(
    x='Country',
    y=['NewDeaths','NewCases'],
    mode='lines',
    size=8,
    title="Today's New Cases & New Deaths")


# In[ ]:


df_totaldeaths = df.copy()
df_totaldeaths["TotalDeaths"] = pd.to_numeric(df_totaldeaths["TotalDeaths"])
df_totaldeaths = df_totaldeaths[df_totaldeaths['TotalDeaths']>150]
df_totaldeaths=df_totaldeaths.sort_values(["TotalDeaths"], axis=0, ascending=[False])
fig = px.bar(df_totaldeaths, x='Country', y = 'TotalDeaths', color='Country', text='TotalDeaths', height=500, 
             width=1200,title ='Number of Total Deaths Across Countries Greater Than 150')
fig.show()


# In[ ]:


fig = px.pie(df, values='TotalCases',names='Country', labels={'cured':'TotalCases'}, hover_data=['TotalCases'],
            title='Total Number of Cases Countries Suffered')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()


# ## Data Visualisation - India

# In[ ]:


import plotly.io as pio
pio.templates.default = "plotly_dark"

df_Indtotal.head()


# In[ ]:


df_Indtotal.mean().iplot(kind='bar',
                        layout=dict(title="India's Total Cases, Cured Cases & Total Deaths"))


# In[ ]:


df_Indcases = df_Ind.copy()
df_Indcases["Cases"] = pd.to_numeric(df_Indcases["Cases"])
df_Indcases=df_Indcases.sort_values(by = ["Cases"], ascending = False)
fig = px.bar(df_Indcases, x='States', y ='Cases', color='States',text='Cases', height=500, width=950, 
             title ='Number of Total Cases in India')
fig.show()


# In[ ]:


df_Indcured = df_Ind.copy()
df_Indcured["Cured"] = pd.to_numeric(df_Indcured["Cured"])
df_Indcured=df_Indcured.sort_values(by = ["Cured"], ascending = False)
fig = px.bar(df_Indcured, x='States', y ='Cured', color='States',text='Cured', height=500, width=950, 
             title ='Total Cured Cases in Country')
fig.show()


# In[ ]:


df_Indcured = df_Ind.copy()
df_Indcured["Cases"] = pd.to_numeric(df_Indcured["Cases"])
df_Indcured=df_Indcured.sort_values(by = ["Cases"], ascending = False)
df_Indcured.iplot(
    x='States',
    y=['Cured','Cases'],
    mode='lines',
    size=8,
    layout=dict(title='Rate of Total Cured & Total Cases In India'))


# In[ ]:


fig = px.pie(df_Indcured, values='Cases',names='States', labels={'cured':'Cases'}, hover_data=['Cases'],
            title="Total Cases India Suffered as per States")
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()


# ## References
# https://plotly.com/python/<br>
# https://www.mohfw.gov.in <br>
# https://www.worldometers.info/coronavirus
