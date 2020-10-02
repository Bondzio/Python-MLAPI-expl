#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        pass
        #print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ## COVID-19 - Keeping an Eye on Reopening of Countries and States
# 
# 
# This notebook is intended to serve as a watchdog of the various partial economic reopenings occurring around the world. With the arrival rate of new cases dropping in almost every country, many countries are relaxing social distancing practices and allowing the reopening of local businesses. This is an exciting and nervous time - no one wants another hot reignition of the spread of the virus.
# 
# In addition to monitoring growth rates in the re-opened countries and states, a new section of the notebook now calculates the reproduction rate $R_t$, which is a key indicator of the safety of reopening. 
# 
# This notebook is based on my prior effort which attempted to identify inflection points in the grow curves:
# https://www.kaggle.com/wjholst/covid-19-growth-patterns-in-critical-countries
# 
# 
# 
# 
# ## Background
# 
# I think it is important for everyone to understand the nature of the growth patterns of pandemics. There is an excellent Youtube video from [3Blue1Brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw) that offers a great explanation.
# 
# ### Understanding Growth Video Link
# 
# ![image.png](attachment:image.png)
# 
# https://www.youtube.com/watch?v=Kas0tIxDvrg&t=35s

# In[ ]:


#import IPython
#IPython.display.IFrame(<iframe width="650" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="2019-nCoV" src="/gisanddata.maps.arcgis.com/apps/Embed/index.html?webmap=14aa9e5660cf42b5b4b546dec6ceec7c&extent=77.3846,11.535,163.5174,52.8632&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light"></iframe>)


# In[ ]:


from IPython.display import HTML

HTML('<div style="position:relative;height:0;padding-bottom:56.25%"><iframe src="https://www.youtube.com/embed/jmHbS8z57yI?ecver=2" width="640" height="360" frameborder="0" style="position:absolute;width:100%;height:100%;left:0" allowfullscreen></iframe></div>')


# # Purpose of This Document
# 
# This document will maintain a dynamic list of countries and states as they reopen local businesses. It will track the daily and logistic growth patterns to identify any flair-ups of the virus.
# 
# In addition to the visual tracking of new cases, active cases, and growth rates, this notebook now incorporates the calculation of the effective reproduction number R. This is a key variable to track in determining when the situation is really safe to reopen public venues. We will track changes in R over time. As R becomes < 1, it is much safer to resume normal activities, because the virus will not spread. 
# 
# The addition of the R modeling is inspired by the work from Kevin Systrom, **Estimating COVID-19's $R_t$ in Real-Time** at https://github.com/k-sys/covid-19/blob/master/Realtime%20R0.ipynb
# 
# 
# ## Starting Observations
# 
# As of April 22, 2020, there are about 6 European countries that have some form of reopening in place.
# * Denmark - reopened daycare and primary schools on April 14. April 20 saw reopening of hairdressers, tattooists, and psychologists.
# * Austria - April 14 non-essintial shops with floor space < 400 square meters. May 1, this extended to shopping centers.
# * Norway - April 20 - kindergartens. Primary and some high schools on April 27, along with universities, beauty salons. Domestic travel is allowed but discouraged.
# * Germany - April 20, shops < 800 square meters, along with car showrooms, bookstores, and bicycle shops. Schools on May 4th.
# * Switzerland - April 27 hairdressers, hardware stores, beauty salons and flower shops.  Also non-essential medical care. 
# * Sweden - Never closed down so it is included as a reference point.
# * Georgia - First US state to reopen. It includes hair and nail salons, barber shops, massage businesses and gyms.
# * New Zealand - Will partially reopen 4/27. They had one of the most agressive lock-downs of anywhere and have very low case and death rates. 
# * Several US states, Colorado, Tennessee, South Carolina, Alaska, Oklahoma, Montana, Minnesota, Alabama. These are part of an early phase I reopening.
# * Many more European countries opening on 5/4.
# 
# In the next two weeks, several US states are scheduled to reopen. They will be added as the reopening occurs.
# 
# ## Observation Log
# 
# * 2020-04-26 - European reopening countries are all ok, although Germany and Denmark's R value has moved above 1. Sweden still shows increasing cases; they probably have not reached an inflection point.
# * 2020-04-27 - Alaska, Sweden, and Montana still have errors in R calculations. Germany and Denmark have both dropped below 1. South Carolina has risen above 1 since the reopen, so we should watch it. Sweden's new case rate has turned, so the R calculations may work.
# * 2020-04-29 - Minnesota still has positive > R values. Their growth curve has not peaked, so this is a state to watch. South Carolina has dropped below 1. The R value seems to be a weekly cyclical pattern.
# * 2020-05-01 - Minnesota shows no improvement - R values hover around 2. Sweden and Germany both have a weekly cyclical pattern, hovering around R = 1. 
# * 2020-05-05 - Minnesota has now dropped to around 1.
# * 2020-05-08 - Germany, Portugual, and Maine have all shown strong uptick in R values. They should be watched.
# * 2020-05-10 - The 3 regions above have dropped back. South Dakota shows an increase in new cases and R, probably due to a new testing site near the meat packing plant. In general, the R calculation still has some bias due to testing increases. There is a revision in Kevin Systrom's model which softens the testing increase that I will look at using.
# * 2020-05-11 - Germany, Portugal, and Maine are all back under 1. South Dakota is trending down, so the issue there was testing increase. There is no evidence of another meat packing plant outbreak.
# * 2020-05-12 - Arkansas, one on the newly added states, has showing upward movement in R for more than a week. Keep an eye on that state.
# * 2020-05-15 - On https://rt.live  only 2 states, Wyoming and Minnesota, show R values > 1. Austria and Arizona have shown a steady increase in R, so they should be watched.  
# * 2020-05-18 - Minnesota is the only state which is still above 1, but it may be trending down. Another interesting observation is that the high density interval (HDI) for the collective no-lockdown states is very narrow, which implies that those states now are truely below an R value of 1.
# * 2020-05-22 - Arkansas and Maine both show steady uptrends in R. This many be due to increased testing. We should watch them over the next week.
# * 2020-05-24 - Arkansas, Maine, and Georgia still show increasing R. They should still be monitored.
# * 2020-06-08 - Sweden and several US states all showing increasing R values.
# 
# ## Change History
# 
# * 2020-03-18 - Addressed a problem with some of the curve fitting not converging. Because some of the countries, like the US, had a long period of days with no increases of cases, the tracking start date.
# * 2020-03-18 - Added US "hot" states, NY, CA, and WA. Also added Germany, which has shown rapid recent growth.
# * 2020-03-19 - Added Colorado, per friend request. Also added France and 2 high density countries, Monaco and Singapore
# * 2020-03-20 - Removed Monaco, not enough cases
# * 2020-03-21 - Added Switzerland, New Jersey, Louisiana, and 12 'hot' European countries as a group
# * 2020-03-22 - Added United Kingdom and UK to hot European group
# * 2020-03-23 - Changed South Korea extract, due to a data change in source; moved Iran to the logistic curve section;
# * 2020-03-24 - Changed dataset source due to issues with corona-virus-report/covid_19_clean_complete.csv; United Kingdom is called UK on this dataset
# * 2020-03-27 - Added more US states: Massachusetts, Florida, Michigan, Illinois. Add new cases tracking graph. Removed Iran from logistic graph. 
# * 2020-03-30 - Added Sweden to country tracking because they are not enforcing any social distancing rules. Also added India because of population size.
# * 2020-03-31 - Moved Italy, Spain, Hot European, and New York to the logistic plot.
# * 2020-04-02 - Added Washington to logistic plot. Corrected error with negative growth rates.
# * 2020-04-05 - Added Germany, California, Washington to logistic plot. Corrected error with negative growth rates.
# * 2020-04-06 - Added Louisiana, Massachusetts, Florida, and the rest of the world without China to logistic plots.
# * 2020-04-08 - Added United States to logistic plots.
# * 2020-04-22 - Converted this to a reopening tracker
# * 2020-04-22 - Added Rt tracking
# * 2020-04-26 - Added Georgia and New Zealand
# * 2020-04-27 - Added more US states
# * 2020-05-05 - Added more European countries
# * 2020-05-12 - Added more states; added separate date for shelter ends
# * 2020-05-21 - Added composite for US and hot European countries
# * 2020-06-09 - Added Brazil due to alarming increases in case counts
# 
# 
# ## About Coronavirus
# 
# * Coronaviruses are **zoonotic** viruses (means transmitted between animals and people).  
# * Symptoms include from fever, cough, respiratory symptoms, and breathing difficulties. 
# * In severe cases, it can cause pneumonia, severe acute respiratory syndrome (SARS), kidney failure and even death.
# * Coronaviruses are also asymptomatic, means a person can be a carrier for the infection but experiences no symptoms
# 
# ## Novel coronavirus (nCoV)
# * A **novel coronavirus (nCoV)** is a new strain that has not been previously identified in humans.
# 
# ## COVID-19 (Corona Virus Disease 2019)
# * Caused by a **SARS-COV-2** corona virus.  
# * First identified in **Wuhan, Hubei, China**. Earliest reported symptoms reported in **November 2019**. 
# * First cases were linked to contact with the Huanan Seafood Wholesale Market, which sold live animals. 
# * On 30 January the WHO declared the outbreak to be a Public Health Emergency of International Concern 

# # Acknowledgements
# 
# This effort was inspired by an excellent Youtube video from [3Blue1Brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw)
# 
# * Video - https://www.youtube.com/watch?v=Kas0tIxDvrg&t=35s 
# * Starting kernel - https://www.kaggle.com/imdevskp/covid-19-analysis-viz-prediction-comparisons
# * https://github.com/CSSEGISandData/COVID-19
# * https://arxiv.org/ftp/arxiv/papers/2003/2003.05681.pdf
# * https://github.com/k-sys/covid-19/blob/master/Realtime%20R0.ipynb
# 
# 

# # Libraries

# ### Install

# In[ ]:


## install calmap
#! pip install calmap


# ### Import Libraries

# In[ ]:


# essential libraries
import json
import random
from urllib.request import urlopen

# storing and anaysis
import numpy as np
import pandas as pd

# visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
#import calmap
import folium
import plotly.io as pio
pio.templates.default = "plotly_dark"
from plotly.subplots import make_subplots

# color pallette
cnf = '#393e46' # confirmed - grey
dth = '#ff2e63' # death - red
rec = '#21bf73' # recovered - cyan
act = '#fe9801' # active case - yellow

# converter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()   

# hide warnings
import warnings
warnings.filterwarnings('ignore')

# html embedding
from IPython.display import Javascript
from IPython.core.display import display
from IPython.core.display import HTML


# # Dataset

# In[ ]:


# importing datasets


full_table = pd.read_csv('/kaggle/input/novel-corona-virus-2019-dataset/covid_19_data.csv',parse_dates = ['ObservationDate'])
#full_table = pd.read_csv('../input/corona-virus-report/covid_19_clean_complete.csv', parse_dates=['Date'])
#train = pd.read_csv('/kaggle/input/covid19-global-forecasting-week-1/train.csv')


# ## Most Recent Update

# In[ ]:


print ('Last update of this dataset was ' + str(full_table.loc[len(full_table)-1]['Last Update']))
#print ('Last update of this dataset was ' + str(full_table.loc[len(full_table)-1]['Date']))


# In[ ]:


full_table.columns = ['SNo', 'Date', 'Province/State', 'Country/Region','Last Update', 'Confirmed', 'Deaths', 'Recovered']


# # Preprocessing

# In[ ]:


### Cleaning Data

# cases 
cases = ['Confirmed', 'Deaths', 'Recovered', 'Active']

# Active Case = confirmed - deaths - recovered
full_table['Active'] = full_table['Confirmed'] - full_table['Deaths'] - full_table['Recovered']

# replacing Mainland china with just China
full_table['Country/Region'] = full_table['Country/Region'].replace('Mainland China', 'China')

# filling missing values 
full_table[['Province/State']] = full_table[['Province/State']].fillna('')
full_table[cases] = full_table[cases].fillna(0)
# cases in the ships
ship = full_table[full_table['Province/State'].str.contains('Grand Princess')|full_table['Country/Region'].str.contains('Cruise Ship')]

# china and the row
china = full_table[full_table['Country/Region']=='China']
us = full_table[full_table['Country/Region']=='US']
skorea  = full_table[full_table['Country/Region']=='South Korea']
hot_europe = full_table[full_table['Country/Region'].isin(
    ['Italy,Spain','Germany','France','UK','Switzerland','Netherlands','Belgium','Austria','Norway','Sweden','Denmark','Portugal', 'Great Britain']) ]
italy = full_table[full_table['Country/Region']=='Italy']
iran = full_table[full_table['Country/Region']=='Iran']
spain = full_table[full_table['Country/Region']=='Spain']
france = full_table[full_table['Country/Region']=='France']
uk = full_table[full_table['Country/Region']=='UK']
switzerland = full_table[full_table['Country/Region']=='Switzerland']
singapore = full_table[full_table['Country/Region']=='Singapore']
sweden = full_table[full_table['Country/Region']=='Sweden']
india = full_table[full_table['Country/Region']=='India']
japan = full_table[full_table['Country/Region']=='Japan']
nz = full_table[full_table['Country/Region']=='New Zealand']
portugal = full_table[full_table['Country/Region']=='Portugal']
belgium = full_table[full_table['Country/Region']=='Belgium']
netherlands = full_table[full_table['Country/Region']=='Netherlands']
greece = full_table[full_table['Country/Region']=='Greece']
brazil = full_table[full_table['Country/Region']=='Brazil']
row = full_table[full_table['Country/Region']!='China']
#rest of China
roc = china[china['Province/State'] != 'Hubei']
germany = full_table[full_table['Country/Region']=='Germany']
ca = us[us['Province/State'] == 'California']
ny = us[us['Province/State'] == 'New York']
wa = us[us['Province/State'] == 'Washington']
co = us[us['Province/State'] == 'Colorado']
nj = us[us['Province/State'] == 'New Jersey']
la = us[us['Province/State'] == 'Louisiana']
ma = us[us['Province/State'] == 'Massachusetts']
fl = us[us['Province/State'] == 'Florida']
mi = us[us['Province/State'] == 'Michigan']
il = us[us['Province/State'] == 'Illinois']
ga = us[us['Province/State'] == 'Georgia']
ak = us[us['Province/State'] == 'Alaska']
mn = us[us['Province/State'] == 'Minnesota']
mt = us[us['Province/State'] == 'Montana']
ok = us[us['Province/State'] == 'Oklahoma']
sc = us[us['Province/State'] == 'South Carolina']
tn = us[us['Province/State'] == 'Tennessee']
ms = us[us['Province/State'] == 'Mississippi']
Id = us[us['Province/State'] == 'Idaho']
ut = us[us['Province/State'] == 'Utah']
wy = us[us['Province/State'] == 'Wyoming']
sd = us[us['Province/State'] == 'South Dakota']
nd = us[us['Province/State'] == 'North Dakota']
ia = us[us['Province/State'] == 'Iowa']
tx = us[us['Province/State'] == 'Texas']
al = us[us['Province/State'] == 'Alabama']
me = us[us['Province/State'] == 'Maine']
az = us[us['Province/State'] == 'Arizona']
ar = us[us['Province/State'] == 'Arkansas']
hi = us[us['Province/State'] == 'Hawaii']
In = us[us['Province/State'] == 'Indiana']
ks = us[us['Province/State'] == 'Kansas']
ne = us[us['Province/State'] == 'Nebraska']
nv = us[us['Province/State'] == 'Nevada']
nc = us[us['Province/State'] == 'North Carolina']
pa = us[us['Province/State'] == 'Pennsylvania']
ri = us[us['Province/State'] == 'Rhode Island'] 

    
nsh = full_table[full_table['Province/State'].isin(['North Dakota','South Dakota','Iowa','Nebraska','Arkansas',])]

# new countries

denmark = full_table[full_table['Country/Region']=='Denmark']
austria = full_table[full_table['Country/Region']=='Austria']
norway = full_table[full_table['Country/Region']=='Norway']

# latest
full_latest = full_table[full_table['Date'] == max(full_table['Date'])].reset_index()
china_latest = full_latest[full_latest['Country/Region']=='China']
row_latest = full_latest[full_latest['Country/Region']!='China']

# latest condensed
full_latest_grouped = full_latest.groupby('Country/Region')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
china_latest_grouped = china_latest.groupby('Province/State')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
row_latest_grouped = row_latest.groupby('Country/Region')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
def country_info (country, dt, reopen = None):
    
    by_date = country.groupby (['Date'])[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum()
    by_date = by_date.reset_index()
    by_date = by_date[by_date.Date>=dt]
    #print (len(by_date))

    #print ('Rates for country/region : ' + pd.unique(country['Country/Region']))

    #print (by_date)
    
    
    # Add need fields
    
    by_date ['prior_confirmed'] = 0
    by_date ['prior_deaths'] = 0
    by_date ['prior_recovered'] = 0
    by_date ['daily_confirmed'] = 0
    by_date ['daily_deaths'] = 0
    by_date ['daily_recovered'] = 0
    p_confirmed = 0
    p_deaths = 0
    p_recovered = 0
   
    for i, row in by_date.iterrows():
        #print (by_date.loc[i])
        by_date.loc[i,'prior_confirmed'] = p_confirmed 
        by_date.loc[i,'prior_deaths'] = p_deaths 
        by_date.loc[i,'prior_recovered'] = p_recovered
        p_confirmed = by_date.loc[i,'Confirmed']
        p_deaths = by_date.loc[i,'Deaths']
        p_recovered = by_date.loc[i,'Recovered']
        
        
    
    by_date ['delta_confirmed'] = by_date.Confirmed - by_date.prior_confirmed
    by_date ['delta_deaths'] = by_date.Deaths - by_date.prior_deaths
    by_date ['delta_recovered'] = by_date.Recovered - by_date.prior_recovered
    
    return by_date

us_by_date = country_info(us,'2020-03-04',)
china_by_date = country_info(china,'2020-01-01',)
hot_europe_by_date = country_info(hot_europe,'2020-02-20',) 
italy_by_date = country_info(italy,'2020-02-20',)
skorea_by_date = country_info(skorea,'2020-02-17')
iran_by_date = country_info(iran,'2020-02-23')
spain_by_date = country_info(spain,'2020-02-23')
row['Country/Region'] = 'Rest of World'
row_by_date = country_info(row,'2020-02-17')
roc_by_date = country_info (roc, '2020-01-01')
germany_by_date = country_info (germany, '2020-02-23')
uk_by_date = country_info (uk, '2020-02-23')
france_by_date = country_info (france, '2020-02-23')
switzerland_by_date = country_info(switzerland,'2020-02-23')
singapore_by_date = country_info(singapore,'2020-01-23')
sweden_by_date = country_info(sweden,'2020-02-25')
norway_by_date = country_info(norway,'2020-02-23')
austria_by_date = country_info(austria,'2020-02-23')
denmark_by_date = country_info(denmark,'2020-02-23')
india_by_date = country_info(india,'2020-02-23')
japan_by_date = country_info(japan,'2020-01-23')
nz_by_date = country_info(nz,'2020-03-03')
portugal_by_date = country_info(portugal,'2020-02-23')
belgium_by_date = country_info(belgium,'2020-02-23')
netherlands_by_date = country_info(netherlands,'2020-02-23')
greece_by_date = country_info(greece,'2020-02-23')
brazil_by_date = country_info(brazil,'2020-03-01')

ca['Country/Region'] = 'California'
ny['Country/Region'] = 'New York'
wa['Country/Region'] = 'Washington'
ca_by_state = country_info(ca,'2020-03-09')
ny_by_state = country_info(ny,'2020-03-09')
wa_by_state = country_info(wa,'2020-03-09')
co_by_state = country_info(co,'2020-03-09')
nj_by_state = country_info(nj,'2020-03-09')
la_by_state = country_info(la,'2020-03-09')
ma_by_state = country_info(ma,'2020-03-09')
fl_by_state = country_info(fl,'2020-03-09')
mi_by_state = country_info(mi,'2020-03-09')
il_by_state = country_info(il,'2020-03-09')
ga_by_state = country_info(ga,'2020-03-09')
ms_by_state = country_info(ms,'2020-03-09')
ak_by_state = country_info(ak,'2020-03-16')
mn_by_state = country_info(mn,'2020-03-09')
mt_by_state = country_info(mt,'2020-03-11')
ok_by_state = country_info(ok,'2020-03-09')
sc_by_state = country_info(sc,'2020-03-09')
tn_by_state = country_info(tn,'2020-03-09')
Id_by_state = country_info(Id,'2020-03-12')
ut_by_state = country_info(ut,'2020-03-12')
wy_by_state = country_info(wy,'2020-03-12')
sd_by_state = country_info(sd,'2020-03-12')
nd_by_state = country_info(nd,'2020-03-12')
ia_by_state = country_info(ia,'2020-03-12')
tx_by_state = country_info(tx,'2020-03-12')
al_by_state = country_info(al,'2020-03-12')
me_by_state = country_info(me,'2020-03-12')
az_by_state = country_info(az,'2020-03-12') 
ar_by_state = country_info(ar,'2020-03-12')
hi_by_state = country_info(hi,'2020-03-12')
In_by_state = country_info(In,'2020-03-12')
ks_by_state = country_info(ks,'2020-03-12')
ne_by_state = country_info(ne,'2020-03-12')
nv_by_state = country_info(nv,'2020-03-12')
nc_by_state = country_info(nc,'2020-03-12')
pa_by_state = country_info(pa,'2020-03-12')
ri_by_state = country_info(ri,'2020-03-12')

nsh_by_state = country_info(nsh,'2020-03-09')


# In[ ]:


dict1 = {'United States':us_by_date,
        'California':ca_by_state,
        'Washington':wa_by_state,
        'New York':ny_by_state,
        'Colorado':co_by_state,
        'New Jersey': nj_by_state,
        'Louisiana': la_by_state,
        'Massachusetts': ma_by_state,
        'Florida': fl_by_state,
        'Michigan': mi_by_state,
        'Illinois': il_by_state,
        'Georgia': ga_by_state,
        'China':china_by_date,
        'Rest of world -w/o China':row_by_date,
        'Hot European Countries':hot_europe_by_date,
        'Italy':italy_by_date,   
        'Iran':iran_by_date,
        'South Korea':skorea_by_date,
        'Spain':spain_by_date,
        'France':france_by_date,
        'Germany':germany_by_date,      
        'United Kingdom':uk_by_date,
        'Switzerland':switzerland_by_date,
        'Sweden':sweden_by_date,
        'Singapore':singapore_by_date,
        'India':india_by_date,
        'Japan':japan_by_date,

        'Rest of China w/o Hubei': roc_by_date,
        }

dict_reopen = {
        'Sweden':[sweden_by_date,'2020-03-12',], 
        'Denmark':[denmark_by_date,'2020-04-14',], 
        'Austria':[austria_by_date,'2020-04-14',], 
        'Germany':[germany_by_date, '2020-04-20',], 
        'Norway': [norway_by_date,'2020-04-20',], 
        'Switzerland':[switzerland_by_date,'2020-04-27',], 
        'New Zealand':[nz_by_date,'2020-04-27',],
        'Portugal':[portugal_by_date,'2020-05-04',],
        'Belgium':[belgium_by_date,'2020-05-04',],
        'Italy':[italy_by_date,'2020-05-04',],
        'Spain':[spain_by_date,'2020-05-04',],
        'Greece':[greece_by_date,'2020-05-04',],
        'Brazil':[brazil_by_date,'2020-05-15',],
        'Netherlands':[netherlands_by_date,'2020-05-11',],
        'France':[france_by_date,'2020-05-11',],
        'Hot European':[hot_europe_by_date,'2020-04-27',],
        'US - All States':[us_by_date,'2020-05-08',],
        'US - South Carolina':[sc_by_state,'2020-04-20',],
        'US - Georgia':[ga_by_state,'2020-04-24',], 
        'US - Alaska':[ak_by_state,'2020-04-24',], 
        'US - Minnesota':[mn_by_state,'2020-04-27',],
        'US - Montana':[mt_by_state,'2020-04-27',], 
        'US - Tennessee':[tn_by_state,'2020-04-27',], 
        'US - Mississippi':[ms_by_state,'2020-04-27',], 
        'US - Colorado':[co_by_state,'2020-05-01',],
        'US - Oklahoma':[ok_by_state,'2020-05-01',], 
        'US - Idaho':[Id_by_state,'2020-05-01',], 
        'US - Utah':[ut_by_state,'2020-05-01',], 
        'US - Wyoming':[wy_by_state,'2020-05-01',],
        'US - South Dakota':[sd_by_state,'2020-05-01',],
        #'US - North Dakota':[nd_by_state,'2020-05-01',],  
        'US - Iowa':[ia_by_state,'2020-05-01',], 
        'US - Texas':[tx_by_state,'2020-05-01',], 
        'US - Maine':[me_by_state,'2020-05-01',],
        'US - Arizona':[az_by_state,'2020-05-08',], 
        'US - Arkansas':[ar_by_state,'2020-05-06',], 
        'US - Hawaii':[hi_by_state,'2020-05-06',], 
        'US - Indiana':[In_by_state,'2020-05-03',], 
        'US - Kansas':[ks_by_state,'2020-05-03',], 
        'US - Nebraska':[ne_by_state,'2020-05-03',], 
        'US - Nevada':[nv_by_state,'2020-05-09',], 
        'US - North Carolina':[nc_by_state,'2020-05-08',], 
        'US - Pennsylvania':[pa_by_state,'2020-05-08',],     
        'US - Rhode Island':[ri_by_state,'2020-05-07',], 
        'US - No Stay Home': [nsh_by_state,'2020-03-15',], 



        }

dict_reopenx = {
        'Sweden':[sweden_by_date,'2020-02-23',], 
        #'Denmark':[denmark_by_date,'2020-04-14',], 
        #'Austria':[austria_by_date,'2020-04-14',], 
        #'Germany':[germany_by_date, '2020-04-20',], 
        #'Norway': [norway_by_date,'2020-04-20',], 
        #'Switzerland':[switzerland_by_date,'2020-04-27',], 
        'New Zealand':[nz_by_date,'2020-04-27',],
        #'US - South Carolina':[sc_by_state,'2020-04-20',],
        #'US - Georgia':[ga_by_state,'2020-04-24',], 
        'US - Alaska':[ak_by_state,'2020-04-24',], 
        #'US - Minnesota':[mn_by_state,'2020-04-27',],
        #'US - Montana':[mt_by_state,'2020-04-27',], 
        #'US - Tennessee':[tn_by_state,'2020-04-27',], 
        #'US - Mississippi':[ms_by_state,'2020-04-27',], 
        #'US - Colorado':[co_by_state,'2020-05-01',],
        #'US - Oklahoma':[ok_by_state,'2020-05-01',],     
        #'US - No Stay Home': [nsh_by_state,'2020-04-01',], 
        #'Minnesota':minnesota_by_state,

        }

skip_R_calc = ['Sweden','New Zealand','Belgium','Spain','France','US - Alasxxka', 'US - Mississippi','US - Montana','US - Hawaii',]

dict_sigmoid = {
        'China':china_by_date,
        'South Korea': skorea_by_date,
        'Rest of China w/o Hubei': roc_by_date,
        'Rest of world -w/o China':row_by_date,
        'Iran':iran_by_date,
        'Hot European Countries':hot_europe_by_date,
        'Italy':italy_by_date,
        'Switzerland':switzerland_by_date,
        'Spain':spain_by_date,
        'Germany':germany_by_date,
        'France':france_by_date,
        'United States':us_by_date,
        'New York':ny_by_state,
        'Washington':wa_by_state,
        'California':ca_by_state,
        'Colorado':co_by_state,
        'Louisiana': la_by_state,
        'Massachusetts': ma_by_state,
        'Florida': fl_by_state,

}

dict_test = {
        'Sweden':[sweden_by_date,'2020-02-23'],
        'Denmark': [denmark_by_date,'2020-04-14'],
        #'Minnesota':minnesota_by_state,
}


# ## Examining the Growth Curves
# 
# These distributions start off exponentially, but eventually become a logistic curve. We can plot them both ways, and then fit a non-linear regression to the curve to determine the rate.
# 
# First we look at mortality curves. The trend to what for is an increasing mortality curve. This means that medical treatments are not controlling the virus well. This is true in Italy, which has an older population and seemed to be slow to respond in social distancing efforts. Compare Italy to South Korea, which had an agressive testing and treatment program, we see that Italy has a severe virus growth situation.
# 
# ### What these curves show
# 
# There are several groups of curves shown. They show:
# 
# * Death and recovery rates for each region - these are on a log scale and show rates of death and recovery per confirmed cases 
# * Growth rate over time - this shows the daily growth rate for each region 
# * Exponential growth for each region - there are separate plots for confirmed cases, deaths, and recovered
# * Logistic growth curves - these are for only the countries that have reached an inflection point
# * Gaussian (Normal) curves - these are an approximation of the derivative of the logistic curve, which is the number of daily new cases over time 
# 
# The growth and normal curves also have the coefficents and errors for each coeffients. The second coefficient is the growth rate.
# 
# You may observe several countries/regions where the daily arrival rates are to the right of the predicted curve. This is a good signal that the growth rate might be reaching an inflection point. Once this point is reached, the infection point, the growth rate will slow down, and the curve will be S-shaped, a sigmoid curve. This is a very good signal!
# 
# The infection point generally indicates that 50 percent of the cummulative cases have been reached.

# In[ ]:


#import plotly.graph_objects as go
def plots_by_country (country, country_name, start_dt):

    temp = country

    # adding two more columns
    temp['No. of Deaths to 100 Confirmed Cases'] = round(temp['Deaths']/temp['Confirmed'], 3)*100
    temp['No. of Recovered to 100 Confirmed Cases'] = round(temp['Recovered']/temp['Confirmed'], 3)*100
    # temp['No. of Recovered to 1 Death Case'] = round(temp['Recovered']/temp['Deaths'], 3)
    #print (temp)

    
    #print (temp.iloc[13]['Date'])
    last_date = temp.iloc[len(temp)-1]['Date']
    death_rate = temp[temp.Date ==last_date]['No. of Deaths to 100 Confirmed Cases']
    recovered_rate = temp[temp.Date ==last_date]['No. of Recovered to 100 Confirmed Cases']
    temp = temp.melt(id_vars='Date', value_vars=['No. of Deaths to 100 Confirmed Cases', 'No. of Recovered to 100 Confirmed Cases'], 
                     var_name='Ratio', value_name='Value')

    #str(full_table.loc[len(full_table)-1]['Date'])
    #fig = go.Figure()
    fig = px.line(temp, x="Date", y="Value", color='Ratio', log_y=True, width=1000, height=700,
                  title=country_name + ' Recovery and Mortality Rate Over Time', color_discrete_sequence=[dth, rec])
    fig.add_annotation(
            x=start_dt,
            y=0,
            text="Reopen")
    
    fig.show()
    return death_rate, recovered_rate
        
rates = []
for (key, [value,start_dt]) in dict_reopen.items():
    print (start_dt)
    death_rate, recovered_rate  = plots_by_country (value,key, start_dt)

    


# ## New Daily Cases
# 
# This graph shows only the new cases on a daily basis. As long as this curve is still rising, we haven't reached an inflection point.

# In[ ]:


def get_smoothed (value):
    return value.rolling(7,
        win_type='gaussian',
        min_periods=1,
        center=True).mean(std=2).round()


# In[ ]:


def plots_of_daily (country, country_name, start_dt, attribute):

    temp = country
    #print (temp.columns)
    temp.columns = ['Date', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'prior_confirmed',
       'prior_deaths', 'prior_recovered', 'daily_confirmed', 'daily_deaths',
       'daily_recovered', 'New Daily Confirmed', 'delta_deaths', 'delta_recovered',
       'No. of Deaths to 100 Confirmed Cases',
       'No. of Recovered to 100 Confirmed Cases']
    #print (temp.iloc[13]['Date'])
    last_date = temp.iloc[len(temp)-1]['Date']

    smoothed_daily = temp[attribute].rolling(7,
        win_type='gaussian',
        min_periods=1,
        center=True).mean(std=2).round()

    #str(full_table.loc[len(full_table)-1]['Date'])
    

    fig = px.line(temp, x="Date", y=attribute, log_y=False, width=800, height=800, 
                  title=country_name + ' ' + attribute ,color_discrete_sequence=[dth, rec])
    fig.add_scatter(x=temp.Date, y=smoothed_daily, mode='lines')
    fig.add_annotation(
            x= start_dt,
            y=5,
            text="Reopen date")
    


    fig.update_layout(showlegend=False)
    fig.show()

        
rates = []
for (key, [value,start_dt]) in dict_reopen.items():
    
    plots_of_daily (value,key,start_dt, 'New Daily Confirmed',)
    plots_of_daily (value,key,start_dt, "Active",)


# ## Smoothing the Curve
# 
# We observe that the curves for some countries are very choppy. This may because of differing reporting mechanisms for each country or state. So it is necessary to smooth this out. A 7 day Gaussian smoothing algorithm in the graphs above removes most of that choppy behavior.
# 
# 

# Next, let's review some of the grow curves.
# 
# 

# In[ ]:


import pylab
import datetime
from scipy.optimize import curve_fit

def sigmoid(x, x0, k, ymax):
     y = ymax / (1 + np.exp(-k*(x-x0)))
     return y

def exp (x,a,b):
    y = a* np.exp(x*b)
    return y

def gaussian(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

def growth_rate_over_time (f, country, attribute, title):
    ydata = country[attribute]
    

    xdata = list(range(len(ydata)))

    rates = []
    for i, x in enumerate(xdata):
        if i > 2:
#            print (xdata[:x+1])
#            print (ydata[:x+1])

            popt, pcov = curve_fit(f, xdata[:x+1], ydata[:x+1],)
            if popt[1] < 0:
                rates.append (0.0)
            else:    
                rates.append (popt[1])
    rates = np.array(rates) 
    pylab.style.use('dark_background')
    pylab.figure(figsize=(12,8))
    xdata = np.array(xdata)
    #pylab.grid(True, linestyle='-', color='0.75')
    pylab.plot(xdata[3:]+1, 100*rates, 'o', linestyle='solid', label=attribute)
    #if fit_good:
    #    pylab.plot(x,y, label='fit')
    #pylab.ylim(0, ymax*1.05)
    #pylab.legend(loc='best')
    pylab.xlabel('Days Since Start')
    pylab.ylabel('Growth rate percentage ' + attribute)
    pylab.title(title + attribute, size = 15)
    pylab.show()
    
        
    

def plot_curve_fit (f, country, attribute, title, start_dt, normalize = False, curve = 'Exp',):
    #country = country[10:]
    first_dt = min(country.Date)
    fmt = '%Y-%m-%d'
    #d1 = datetime.datetime.strptime(first_dt,fmt)
    d2 = datetime.datetime.strptime(start_dt,fmt)
    d = d2-first_dt
    print (d.days)
    fit_good = True
    ydata = country[attribute]
    #ydata = np.array(ydata)
    xdata = range(len(ydata))
    mu = np.mean(ydata)
    sigma = np.std(ydata)
    ymax = np.max(ydata)    
    if normalize:
        ydata_norm = ydata/ymax
    else:
        ydata_norm = ydata
    #f = sigmoid
    try:
        if curve == 'Gauss': # pass the mean and stddev
            popt, pcov = curve_fit(f, xdata, ydata_norm, p0 = [1, mu, sigma])
        elif curve == 'Sigmoid':
            popt, pcov = curve_fit(f, xdata, ydata_norm, bounds = ([0,0,0],np.inf),maxfer=1000)
        else:    
            popt, pcov = curve_fit(f, xdata, ydata_norm,)
    except RuntimeError:
        print ('Exception - RuntimeError - could not fit curve')
        fit_good = False
    else:

        fit_good = True
        
    if fit_good:
        if curve == 'Exp':
            if popt[1] < 0.9: # only print if we have a growth rate
                
                print (key + ' -- Coefficients for y = a * e^(x*b)  are ' + str(popt))
                print ('Growth rate is now ' + str(round(popt[1],2)))
                print ('...This doubles in ' + str (round(0.72/popt[1] , 1) ) +' days')
            else:
                fit_good = False
        elif curve == 'Gauss':
            print (key + ' -- Coefficients are ' + str(popt))
        else:   # sigmoid 
            print (key + ' -- Coefficients for y = 1/(1 + e^(-k*(x-x0)))  are ' + str(popt))
            
        if fit_good:
            print ('Mean error for each coefficient: ' + str(np.sqrt(np.diag(pcov))/popt))
    else:
        print (key + ' -- Could not resolve coefficients ---')
    x = np.linspace(-1, len(ydata), 100)
    if fit_good:
        y = f(x, *popt)
        if normalize:
            y = y * ymax
        plt.style.use('dark_background')
        pylab.figure(figsize=(15,12)) 
        #pylab.grid(True, linestyle='-', color='0.75')
        pylab.plot(xdata, ydata, 'o', label=attribute)
        #if fit_good:
        pylab.plot(x,y, label='fit')
        pylab.axvline(x=d.days)
        pylab.ylim(0, ymax*1.05)
        pylab.legend(loc='best')
        pylab.xlabel('Days Since Start')
        pylab.ylabel('Number of ' + attribute)
        pylab.title(title + attribute, size = 15)
        pylab.show()


# ### Growth Rates of Confirmed Cases and Deaths 
# 
# There are three graphs in this section which show exponential growth rate of confirmed, deaths, and recovered. The head shows the current growth rate.
# 
# You can use the rule of 72 to find the doubling rate. As of March 20th, the confirmed growth rate for the United States is around 0.35. That means that the number of confirmed cases will double in just 2 days. *( 72/35 = 2.06 )*

# In[ ]:


round (72/35,2)


# In[ ]:


if False:
  for (key, [value,start_dt]) in dict_reopen.items():

    if key in ["China",'Rest of China w/o Hubei']:
        pass
    else:
        print (start_dt)
        plot_curve_fit (exp, value, 'Confirmed', key + ' - Growth Curve for ',start_dt,False,'Exp')
        plot_curve_fit (exp, value, 'Deaths', key + ' - Growth Curve for ',start_dt,False,'Exp')
        plot_curve_fit (exp, value, 'Recovered', key + ' - Growth Curve for ',start_dt,False,'Exp')


# 
# ## Logistic Growth Curves
# 
# Here are logistic growth curves of the reopened regions. The line indicates when the reopening occurred.

# In[ ]:


for (key, [value,start_dt]) in dict_reopen.items():
    plot_curve_fit (sigmoid, value, 'Confirmed', key + ' - Logistic Growth Curve for ',start_dt,True,'Logistic')
    plot_curve_fit (sigmoid, value, 'Deaths', key + ' - Logistic Growth Curve for ',start_dt,True,'Logistic',)
    #plot_curve_fit (sigmoid, value, 'Recovered', key + ' - Logistic Growth Curve for ',True,'Logistic',start_dt)


# # Exploration of $R_t$ - Effective Reproduction Rate
# 
# This is a key indicator in letting us know when it is 'safe' to resume somewhat normal activities. As long as the number is above 1, it means the growth rate of the virus is still growing. 
# 
# Keven Systrom uses a Bayes' rule approach to predict the value for R. The value for $R_t$ is a function of the value of yesterday's value $R_{t-1}$. His work is based on a method in a paper by [Bettencourt & Ribeiro 2008](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0002185) to estimate R.
# 
# At this point, I will skip the probability theory behind this estimate and get to the actual algorithm.
# 
# 
# ## A Simple Poisson Arrival Model
# 
# We need a likelihood function which identifies how likely we are to see $k$ new cases, given a value of $R_t$.
# 
# Statisticians and operation research people usually model 'arrivals' (in our case, new cases) over some time period of time with [Poisson Distribution](https://en.wikipedia.org/wiki/Poisson_distribution). 
# 
# Given an average arrival rate of $\lambda$ new cases per day, the probability of seeing $k$ new cases is distributed according to the Poisson distribution:
# 
# $$P(k|\lambda) = \frac{\lambda^k e^{-\lambda}}{k!}$$

# We also need to find the highest density intervals.

# In[ ]:



def highest_density_interval_slow(pmf, p=.9):
    # If we pass a DataFrame, just call this recursively on the columns
    if(isinstance(pmf, pd.DataFrame)):
        return pd.DataFrame([highest_density_interval(pmf[col], p=p) for col in pmf],
                            index=pmf.columns)
    
    cumsum = np.cumsum(pmf.values)
    best = None
    for i, value in enumerate(cumsum):
        for j, high_value in enumerate(cumsum[i+1:]):
            if (high_value-value > p) and (not best or j<best[1]-best[0]):
                best = (i, i+j+1)
                break
            
    low = pmf.index[best[0]]
    high = pmf.index[best[1]]
    return pd.Series([low, high], index=[f'Low_{p*100:.0f}', f'High_{p*100:.0f}'])

#hdi = highest_density_interval(posteriors)
#hdi.tail()


# In[ ]:





# In[ ]:


def highest_density_interval(pmf, p=.9, debug=False):
   
    # If we pass a DataFrame, just call this recursively on the columns
    if(isinstance(pmf, pd.DataFrame)):
        return pd.DataFrame([highest_density_interval(pmf[col], p=p) for col in pmf],
                            index=pmf.columns)
    cumsum = np.cumsum(pmf.values)
    
    # N x N matrix of total probability mass for each low, high
    total_p = cumsum - cumsum[:, None]
    
    # Return all indices with total_p > p
    lows, highs = (total_p > p).nonzero()
    
    # Find the smallest range (highest density)
    best = (highs - lows).argmin()
    
    low = pmf.index[lows[best]]
    high = pmf.index[highs[best]]
    
    return pd.Series([low, high],
                     index=[f'Low_{p*100:.0f}',
                            f'High_{p*100:.0f}'])


# In[ ]:


from scipy import stats as sps
from scipy.interpolate import interp1d
# Column vector of k
k = np.arange(0, 70)[:, None]

# Different values of Lambda
lambdas = [10, 20, 30, 40]

# Evaluated the Probability Mass Function (remember: poisson is discrete)
y = sps.poisson.pmf(k, lambdas)


# In[ ]:


fig, ax = plt.subplots(figsize=(10,5))
plt.style.use('ggplot')
ax.set(title='Poisson Distribution of Cases\n $p(k|\lambda)$')

plt.plot(k, y,
         marker='o',
         markersize=3,
         lw=0)

plt.legend(title="$\lambda$", labels=lambdas);


# The above shows the distributions for each value of lambda. The y axis shows the probability that a new case will arrive over time, given each lambda value.

# ## Function for Calculating the Posteriors
# 
# This taken verbatim from Keven Systrom's great notebook. His algorithm is as follows:
# 
# To calculate the posteriors we follow these steps:
# 1. Calculate $\lambda$ - the expected arrival rate for every day's poisson process
# 2. Calculate each day's likelihood distribution over all possible values of $R_t$
# 3. Calculate the process matrix based on the value of $\sigma$ we discussed above
# 4. Calculate our initial prior because our first day does not have a previous day from which to take the posterior
#   - Based on [info from the cdc](https://wwwnc.cdc.gov/eid/article/26/7/20-0282_article) we will choose a Gamma with mean 7.
# 5. Loop from day 1 to the end, doing the following:
#   - Calculate the prior by applying the Gaussian to yesterday's prior.
#   - Apply Bayes' rule by multiplying this prior and the likelihood we calculated in step 2.
#   - Divide by the probability of the data (also Bayes' rule)

# In[ ]:


R_T_MAX = 12
r_t_range = np.linspace(0, R_T_MAX, R_T_MAX*100+1)
GAMMA = 1/7
def get_posteriors(sr, sigma=0.15):

    # (1) Calculate Lambda
    lam = sr[:-1].values * np.exp(GAMMA * (r_t_range[:, None] - 1))

    
    # (2) Calculate each day's likelihood
    likelihoods = pd.DataFrame(
        data = sps.poisson.pmf(sr[1:].values, lam),
        index = r_t_range,
        columns = sr.index[1:])
    
    # (3) Create the Gaussian Matrix
    process_matrix = sps.norm(loc=r_t_range,
                              scale=sigma
                             ).pdf(r_t_range[:, None]) 

    # (3a) Normalize all rows to sum to 1
    process_matrix /= process_matrix.sum(axis=0)
    
    # (4) Calculate the initial prior
    #prior0 = sps.gamma(a=4).pdf(r_t_range)
    prior0 = np.ones_like(r_t_range)/len(r_t_range)
    prior0 /= prior0.sum()

    # Create a DataFrame that will hold our posteriors for each day
    # Insert our prior as the first posterior.
    posteriors = pd.DataFrame(
        index=r_t_range,
        columns=sr.index,
        data={sr.index[0]: prior0}
    )
    
    # We said we'd keep track of the sum of the log of the probability
    # of the data for maximum likelihood calculation.
    log_likelihood = 0.0

    # (5) Iteratively apply Bayes' rule
    for previous_day, current_day in zip(sr.index[:-1], sr.index[1:]):

        #(5a) Calculate the new prior
        current_prior = process_matrix @ posteriors[previous_day]
        
        #(5b) Calculate the numerator of Bayes' Rule: P(k|R_t)P(R_t)
        numerator = likelihoods[current_day] * current_prior
        
        #(5c) Calcluate the denominator of Bayes' Rule P(k)
        denominator = np.sum(numerator)
        
        # Execute full Bayes' Rule
        if denominator == 0:
            posteriors[current_day] = 0
        else:    
            posteriors[current_day] = numerator/denominator
        
        # Add to the running sum of log likelihoods
        log_likelihood += np.log(denominator)
    
    return posteriors, log_likelihood


# In[ ]:





# In[ ]:


# Note that we're fixing sigma to a value just for the example

smoothed = get_smoothed(germany_by_date['New Daily Confirmed'])
dates = germany_by_date[['Date']]


posteriors, log_likelihood = get_posteriors(smoothed, sigma=.25)
posteriors.columns = [dates.Date]


# In[ ]:


state_name = 'Germany'

if True:
    plt.style.use('classic')

    ax = posteriors.plot(title=f'{state_name} - Daily Posterior for $R_t$',
           legend=False, 
           lw=1,
           c='k',
           alpha=.3,
           xlim=(0.4,6))

    ax.set_xlabel('$R_t$');


# This graph shows that early days have a much higher R value and flatter curve. As time goes on, the distributions become more peaked and closer to 1.
# 
# We also need to calculate a most likely value and low-high density probabilities.
# 
# 

# In[ ]:


# Note that this takes a while to execute - it's not the most efficient algorithm
hdis = highest_density_interval(posteriors, p=.9)

most_likely = posteriors.idxmax().rename('ML')

# Look into why you shift -1
result = pd.concat([most_likely, hdis], axis=1)

result.tail(10)


# Let's plot these values over time so we can see the evolving $R_t$ values.

# In[ ]:


#dict_reopen.get(state_name)[1]


# In[ ]:


from matplotlib.dates import date2num, num2date
from matplotlib import dates as mdates
from matplotlib import ticker
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

def plot_rt(result, ax, state_name):
    
    ax.set_title(f"{state_name}")
    
    # Colors
    ABOVE = [1,0,0]
    MIDDLE = [1,1,1]
    BELOW = [0,0,1]
    cmap = ListedColormap(np.r_[
        np.linspace(BELOW,MIDDLE,25),
        np.linspace(MIDDLE,ABOVE,25)
    ])
    color_mapped = lambda y: np.clip(y, .5, 1.5)-.5
    
    index = result['ML'].index.get_level_values('Date')
    values = result['ML'].values
    
    # Plot dots and line
    ax.plot(index, values, c='k', zorder=1, alpha=.25)
    ax.scatter(index,
               values,
               s=40,
               lw=.5,
               c=cmap(color_mapped(values)),
               edgecolors='k', zorder=2)
    
    # Aesthetically, extrapolate credible interval by 1 day either side
    lowfn = interp1d(date2num(index),
                     result['Low_90'].values,
                     bounds_error=False,
                     fill_value='extrapolate')
    
    highfn = interp1d(date2num(index),
                      result['High_90'].values,
                      bounds_error=False,
                      fill_value='extrapolate')
    
    extended = pd.date_range(start=pd.Timestamp('2020-03-01'),
                             end=index[-1]+pd.Timedelta(days=1))
    
    ax.fill_between(extended,
                    lowfn(date2num(extended)),
                    highfn(date2num(extended)),
                    color='k',
                    alpha=.1,
                    lw=0,
                    zorder=3)

    ax.axhline(1.0, c='k', lw=1, label='$R_t=1.0$', alpha=.25);
    
    # Formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}"))
    ax.yaxis.tick_right()
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.margins(0)
    ax.grid(which='major', axis='y', c='k', alpha=.1, zorder=-2)
    ax.margins(0)
    ax.set_ylim(0.0, 4.0)
    ax.set_xlim(pd.Timestamp('2020-03-15'), result.index.get_level_values('Date')[-1]+pd.Timedelta(days=1))
    ax.set_title(f'Real-time $R_t$ for {state_name}')
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.axvline(pd.to_datetime(dict_reopen.get(state_name)[1]))
    fig.set_facecolor('w')

    
fig, ax = plt.subplots(figsize=(600/72,400/72))

plot_rt(result, ax, state_name)


# It is interesting that Germany dropped to below 1 in late March, but then bounces back above several times. Since April 20, the R rate has been rising and now is around 1.3. This is something to be watched. The increase may be due to either a resurgance of the virus or increased testing.

# ## Choosing the optimal $\sigma$
# 
# In the previous section we described choosing an optimal $\sigma$, but we just assumed a value. But now that we can evaluate each state with any sigma, we have the tools for choosing the optimal $\sigma$.
# 
# Above we said we'd choose the value of $\sigma$ that maximizes the likelihood of the data $P(k)$. Since we don't want to overfit on any one state, we choose the sigma that maximizes $P(k)$ over every state. To do this, we add up all the log likelihoods per state for each value of sigma then choose the maximum.
# 

# In[ ]:


from IPython.display import clear_output
sigmas = np.linspace(1/20, 1, 20)

results = {}
for (key, [value,start_dt]) in dict_reopen.items():
    smoothed = get_smoothed(value['New Daily Confirmed'])
    dates = value[['Date']]
    state_name = key
    if state_name in skip_R_calc:
        pass
    else:
        print(state_name)
        result = {}

        # Holds all posteriors with every given value of sigma
        result['posteriors'] = []

        # Holds the log likelihood across all k for each value of sigma
        result['log_likelihoods'] = []

        for sigma in sigmas:
            posteriors, log_likelihood = get_posteriors(smoothed, sigma=sigma)
            posteriors.fillna(0)
            posteriors.columns = [dates.Date]
            result['posteriors'].append(posteriors)
            result['log_likelihoods'].append(log_likelihood)

        # Store all results keyed off of state name
        results[state_name] = result
        clear_output(wait=True)

print('Done.')


# In[ ]:


log_likelihood


# In[ ]:


#results['New Zealand']


# 

# In[ ]:


# Each index of this array holds the total of the log likelihoods for
# the corresponding index of the sigmas array.
total_log_likelihoods = np.zeros_like(sigmas)

# Loop through each state's results and add the log likelihoods to the running total.
for state_name, result in results.items():
    total_log_likelihoods += result['log_likelihoods']

# Select the index with the largest log likelihood total
max_likelihood_index = total_log_likelihoods.argmax()

# Select the value that has the highest log likelihood
sigma = sigmas[max_likelihood_index]

# Plot it
fig, ax = plt.subplots()
ax.set_title(f"Maximum Likelihood value for $\sigma$ = {sigma:.2f}");
ax.plot(sigmas, total_log_likelihoods)
ax.axvline(sigma, color='k', linestyle=":");


# In[ ]:


spain_by_date.tail(10)


# In[ ]:


final_results = None

for state_name, result in results.items():
    print(state_name)
    #print(result)
    posteriors = result['posteriors'][max_likelihood_index]
    #print (len(state_name))
    hdis_90 = highest_density_interval(posteriors, p=.9)
    hdis_50 = highest_density_interval(posteriors, p=.5)
    most_likely = posteriors.idxmax().rename('ML')
    
    result = pd.concat([most_likely, hdis_90, hdis_50], axis=1)
    result['State'] = state_name
    #print (result.columns)
    if final_results is None:
        final_results = result
    else:
        final_results = pd.concat([final_results, result])
    clear_output(wait=True)

print('Done.')


# In[ ]:


cols = ['ML', 'Low_90', 'High_90', 'Low_50', 'High_50',]


# # Plotting Continuous $R_t$ Values for Reopened Countries and States
# 
# We now plot the calculated **R** values for our select re-opened areas. 

# In[ ]:


ncols = 2
nrows = int(np.ceil(len(results) / ncols))

fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, nrows*3))

for i, (state_name, result) in enumerate(final_results.groupby('State')):
#for i, (state_name, result) in enumerate(final_results):  
    #print (result)
    plot_rt(result[1:][cols], axes.flat[i], state_name)

    fig.tight_layout()
    fig.set_facecolor('w')


# https://www.kaggle.com/imdevskp/mers-outbreak-analysis  
# https://www.kaggle.com/imdevskp/sars-2003-outbreak-analysis  
# https://www.kaggle.com/imdevskp/western-africa-ebola-outbreak-analysis
# 
