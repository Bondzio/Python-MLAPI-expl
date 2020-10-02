#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib.inline', '')
import seaborn as sns


# In[ ]:


india_daily=pd.read_csv("../input/covid19/Daily_India_covid-19.csv")
india_states_confirmed=pd.read_csv("../input/covid19/Daily_States_Confirmed_india.csv")
india_states_deaths=pd.read_csv("../input/covid19/Daily_States_Deaths_india.csv")
india_states_daily=pd.read_csv("../input/covid19/Daily_States_India.csv")
india_states_recover=pd.read_csv("../input/covid19/Daily_States_Recovered_india.csv")
india_total=pd.read_csv("../input/covid19/Total_India_covid-19.csv")
maha_total=pd.read_csv("../input/covid19/Total_Maharashtra_covid-19.csv")
us_total=pd.read_csv("../input/covid19/Total_US_covid-19.csv")
world_total=pd.read_csv("../input/covid19/Total_World_covid-19.csv")


# In[ ]:


maha_total


# In[ ]:





# In[ ]:


india_daily


# In[ ]:


india_daily.isnull().sum()


# In[ ]:


fig, ax = plt.subplots()
plt.ylabel("no of cases")
plt.xlabel("on the given dates")
plt.title("Daily India Covid-19 Cases(11 june)")
india_daily.plot(x='Date',y='Daily Recovered',ax=ax)
india_daily.plot(x='Date',y='Daily Confirmed',ax=ax)
india_daily.plot(x='Date',y='Daily Deaths',ax=ax)
india_daily.plot(x='Date',y='Total Confirmed',ax=ax)
india_daily.plot(x='Date',y='Total Recovered',ax=ax)
india_daily.plot(x='Date',y='Total Deaths',ax=ax)
india_daily.plot(x='Date',y='Total Active',ax=ax)


# In[ ]:


india_states_confirmed.columns


# In[ ]:


india_states_confirmed.isnull().sum()


# In[ ]:


fig, ax = plt.subplots()
plt.ylabel("no of cases")
plt.xlabel("on the given date")
plt.title("Indian Daily States confirmed cases(11 june)")
india_states_confirmed.plot(x='Date',y='AN',ax=ax)
india_states_confirmed.plot(x='Date',y='AP',ax=ax)
india_states_confirmed.plot(x='Date',y='AR',ax=ax)
india_states_confirmed.plot(x='Date',y='AS',ax=ax)
india_states_confirmed.plot(x='Date',y='BR',ax=ax)
india_states_confirmed.plot(x='Date',y='CH',ax=ax)
india_states_confirmed.plot(x='Date',y='CT',ax=ax)
india_states_confirmed.plot(x='Date',y='DD',ax=ax)
india_states_confirmed.plot(x='Date',y='DL',ax=ax)
india_states_confirmed.plot(x='Date',y='DN',ax=ax)
india_states_confirmed.plot(x='Date',y='GA',ax=ax)
india_states_confirmed.plot(x='Date',y='GJ',ax=ax)
india_states_confirmed.plot(x='Date',y='HP',ax=ax)
india_states_confirmed.plot(x='Date',y='HR',ax=ax)
india_states_confirmed.plot(x='Date',y='JH',ax=ax)
india_states_confirmed.plot(x='Date',y='JK',ax=ax)
india_states_confirmed.plot(x='Date',y='KA',ax=ax)
india_states_confirmed.plot(x='Date',y='KL',ax=ax)
india_states_confirmed.plot(x='Date',y='LA',ax=ax)
india_states_confirmed.plot(x='Date',y='LD',ax=ax)
india_states_confirmed.plot(x='Date',y='MH',ax=ax)
india_states_confirmed.plot(x='Date',y='ML',ax=ax)
india_states_confirmed.plot(x='Date',y='MN',ax=ax)
india_states_confirmed.plot(x='Date',y='MP',ax=ax)
india_states_confirmed.plot(x='Date',y='MZ',ax=ax)
india_states_confirmed.plot(x='Date',y='NL',ax=ax)
india_states_confirmed.plot(x='Date',y='OR',ax=ax)
india_states_confirmed.plot(x='Date',y='PB',ax=ax)
india_states_confirmed.plot(x='Date',y='PY',ax=ax)
india_states_confirmed.plot(x='Date',y='RJ',ax=ax)
india_states_confirmed.plot(x='Date',y='SK',ax=ax)
india_states_confirmed.plot(x='Date',y='TN',ax=ax)
india_states_confirmed.plot(x='Date',y='TG',ax=ax)
india_states_confirmed.plot(x='Date',y='TR',ax=ax)
india_states_confirmed.plot(x='Date',y='UN',ax=ax)
india_states_confirmed.plot(x='Date',y='UP',ax=ax)
india_states_confirmed.plot(x='Date',y='UT',ax=ax)
india_states_confirmed.plot(x='Date',y='WB',ax=ax)
india_states_confirmed.plot(x='Date',y='Total',ax=ax)


# In[ ]:


fig, ax = plt.subplots()
plt.ylabel("no of cases")
plt.xlabel("on the given date")
plt.title("Indian Daily States Deaths cases(11 june)")
india_states_deaths.plot(x='Date',y='AN',ax=ax)
india_states_deaths.plot(x='Date',y='AP',ax=ax)
india_states_deaths.plot(x='Date',y='AR',ax=ax)
india_states_deaths.plot(x='Date',y='AS',ax=ax)
india_states_deaths.plot(x='Date',y='BR',ax=ax)
india_states_deaths.plot(x='Date',y='CH',ax=ax)
india_states_deaths.plot(x='Date',y='CT',ax=ax)
india_states_deaths.plot(x='Date',y='DD',ax=ax)
india_states_deaths.plot(x='Date',y='DL',ax=ax)
india_states_deaths.plot(x='Date',y='DN',ax=ax)
india_states_deaths.plot(x='Date',y='GA',ax=ax)
india_states_deaths.plot(x='Date',y='GJ',ax=ax)
india_states_deaths.plot(x='Date',y='HP',ax=ax)
india_states_deaths.plot(x='Date',y='HR',ax=ax)
india_states_deaths.plot(x='Date',y='JH',ax=ax)
india_states_deaths.plot(x='Date',y='JK',ax=ax)
india_states_deaths.plot(x='Date',y='KA',ax=ax)
india_states_deaths.plot(x='Date',y='KL',ax=ax)
india_states_deaths.plot(x='Date',y='LA',ax=ax)
india_states_deaths.plot(x='Date',y='LD',ax=ax)
india_states_deaths.plot(x='Date',y='MH',ax=ax)
india_states_deaths.plot(x='Date',y='ML',ax=ax)
india_states_deaths.plot(x='Date',y='MN',ax=ax)
india_states_deaths.plot(x='Date',y='MP',ax=ax)
india_states_deaths.plot(x='Date',y='MZ',ax=ax)
india_states_deaths.plot(x='Date',y='NL',ax=ax)
india_states_deaths.plot(x='Date',y='OR',ax=ax)
india_states_deaths.plot(x='Date',y='PB',ax=ax)
india_states_deaths.plot(x='Date',y='PY',ax=ax)
india_states_deaths.plot(x='Date',y='RJ',ax=ax)
india_states_deaths.plot(x='Date',y='SK',ax=ax)
india_states_deaths.plot(x='Date',y='TN',ax=ax)
india_states_deaths.plot(x='Date',y='TG',ax=ax)
india_states_deaths.plot(x='Date',y='TR',ax=ax)
india_states_deaths.plot(x='Date',y='UN',ax=ax)
india_states_deaths.plot(x='Date',y='UP',ax=ax)
india_states_deaths.plot(x='Date',y='UT',ax=ax)
india_states_deaths.plot(x='Date',y='WB',ax=ax)
india_states_deaths.plot(x='Date',y='Total',ax=ax)


# In[ ]:


fig, ax = plt.subplots()
plt.ylabel("no of cases")
plt.xlabel("on the given date")
plt.title("Indian  States Daily cases(11 june)")
india_states_daily.plot(x='Date',y='AN',ax=ax)
india_states_daily.plot(x='Date',y='AP',ax=ax)
india_states_daily.plot(x='Date',y='AR',ax=ax)
india_states_daily.plot(x='Date',y='AS',ax=ax)
india_states_daily.plot(x='Date',y='BR',ax=ax)
india_states_daily.plot(x='Date',y='CH',ax=ax)
india_states_daily.plot(x='Date',y='CT',ax=ax)
india_states_daily.plot(x='Date',y='DD',ax=ax)
india_states_daily.plot(x='Date',y='DL',ax=ax)
india_states_daily.plot(x='Date',y='DN',ax=ax)
india_states_daily.plot(x='Date',y='GA',ax=ax)
india_states_daily.plot(x='Date',y='GJ',ax=ax)
india_states_daily.plot(x='Date',y='HP',ax=ax)
india_states_daily.plot(x='Date',y='HR',ax=ax)
india_states_daily.plot(x='Date',y='JH',ax=ax)
india_states_daily.plot(x='Date',y='JK',ax=ax)
india_states_daily.plot(x='Date',y='KA',ax=ax)
india_states_daily.plot(x='Date',y='KL',ax=ax)
india_states_daily.plot(x='Date',y='LA',ax=ax)
india_states_daily.plot(x='Date',y='LD',ax=ax)
india_states_daily.plot(x='Date',y='MH',ax=ax)
india_states_daily.plot(x='Date',y='ML',ax=ax)
india_states_daily.plot(x='Date',y='MN',ax=ax)
india_states_daily.plot(x='Date',y='MP',ax=ax)
india_states_daily.plot(x='Date',y='MZ',ax=ax)
india_states_daily.plot(x='Date',y='NL',ax=ax)
india_states_daily.plot(x='Date',y='OR',ax=ax)
india_states_daily.plot(x='Date',y='PB',ax=ax)
india_states_daily.plot(x='Date',y='PY',ax=ax)
india_states_daily.plot(x='Date',y='RJ',ax=ax)
india_states_daily.plot(x='Date',y='SK',ax=ax)
india_states_daily.plot(x='Date',y='TN',ax=ax)
india_states_daily.plot(x='Date',y='TG',ax=ax)
india_states_daily.plot(x='Date',y='TR',ax=ax)
india_states_daily.plot(x='Date',y='UN',ax=ax)
india_states_daily.plot(x='Date',y='UP',ax=ax)
india_states_daily.plot(x='Date',y='UT',ax=ax)
india_states_daily.plot(x='Date',y='WB',ax=ax)
india_states_daily.plot(x='Date',y='Total',ax=ax)


# In[ ]:


fig, ax = plt.subplots()
plt.ylabel("no of cases")
plt.xlabel("on the given date")
plt.title("Indian States Recover Cases(11 june)")
india_states_recover.plot(x='Date',y='AN',ax=ax)
india_states_recover.plot(x='Date',y='AP',ax=ax)
india_states_recover.plot(x='Date',y='AR',ax=ax)
india_states_recover.plot(x='Date',y='AS',ax=ax)
india_states_recover.plot(x='Date',y='BR',ax=ax)
india_states_recover.plot(x='Date',y='CH',ax=ax)
india_states_recover.plot(x='Date',y='CT',ax=ax)
india_states_recover.plot(x='Date',y='DD',ax=ax)
india_states_recover.plot(x='Date',y='DL',ax=ax)
india_states_recover.plot(x='Date',y='DN',ax=ax)
india_states_recover.plot(x='Date',y='GA',ax=ax)
india_states_recover.plot(x='Date',y='GJ',ax=ax)
india_states_recover.plot(x='Date',y='HP',ax=ax)
india_states_recover.plot(x='Date',y='HR',ax=ax)
india_states_recover.plot(x='Date',y='JH',ax=ax)
india_states_recover.plot(x='Date',y='JK',ax=ax)
india_states_recover.plot(x='Date',y='KA',ax=ax)
india_states_recover.plot(x='Date',y='KL',ax=ax)
india_states_recover.plot(x='Date',y='LA',ax=ax)
india_states_recover.plot(x='Date',y='LD',ax=ax)
india_states_recover.plot(x='Date',y='MH',ax=ax)
india_states_recover.plot(x='Date',y='ML',ax=ax)
india_states_recover.plot(x='Date',y='MN',ax=ax)
india_states_recover.plot(x='Date',y='MP',ax=ax)
india_states_recover.plot(x='Date',y='MZ',ax=ax)
india_states_recover.plot(x='Date',y='NL',ax=ax)
india_states_recover.plot(x='Date',y='OR',ax=ax)
india_states_recover.plot(x='Date',y='PB',ax=ax)
india_states_recover.plot(x='Date',y='PY',ax=ax)
india_states_recover.plot(x='Date',y='RJ',ax=ax)
india_states_recover.plot(x='Date',y='SK',ax=ax)
india_states_recover.plot(x='Date',y='TN',ax=ax)
india_states_recover.plot(x='Date',y='TG',ax=ax)
india_states_recover.plot(x='Date',y='TR',ax=ax)
india_states_recover.plot(x='Date',y='UN',ax=ax)
india_states_recover.plot(x='Date',y='UP',ax=ax)
india_states_recover.plot(x='Date',y='UT',ax=ax)
india_states_recover.plot(x='Date',y='WB',ax=ax)


# In[ ]:


india_total


# In[ ]:


fig, ax = plt.subplots()
plt.ylabel("no of cases")
plt.xlabel("Statecode")
plt.title("India total covid-19 cases")
india_total.plot(x='Statecode',y='Confirmed',ax=ax)
india_total.plot(x='Statecode',y='Active',ax=ax)
india_total.plot(x='Statecode',y='Recovered',ax=ax)
india_total.plot(x='Statecode',y='Deaths',ax=ax)


# In[ ]:


fig, ax = plt.subplots()
plt.ylabel("no of cases")
plt.xlabel("District")
plt.title("Maharashtra district wise report")
maha_total.plot(x='District',y='Confirmed',ax=ax)
maha_total.plot(x='District',y='Active',ax=ax)
maha_total.plot(x='District',y='Recovered',ax=ax)
maha_total.plot(x='District',y='Deaths',ax=ax)


# In[ ]:


us_total=us_total.replace(np.nan, 0)
us_total


# In[ ]:


fig, ax = plt.subplots()
plt.ylabel("no of cases")
plt.xlabel("USAState")
plt.title("USA Report")
us_total.plot(x='USAState',y='TotalCases',ax=ax)
us_total.plot(x='USAState',y='TotalDeaths',ax=ax)
us_total.plot(x='USAState',y='ActiveCases',ax=ax)
us_total.plot(x='USAState',y='TotalTests',ax=ax)



# In[ ]:




