#!/usr/bin/env python
# coding: utf-8

# <a id="Index"><font size=22>Index</font></a>

# * <a href="#Dataset">Dataset</a>
# * <a href="#RegionSummary">Italy</a><br>
#   * <a href="#RegionSummary">Summary table by Region</a>
#   * <a href="#ItalyDailyNewCases">Daily new cases</a>
#   * <a href="#ItalyCumulativeDeaths">Cumulative deaths</a>
#   * <a href="#ItalyDailyDeaths">Daily deaths</a>
#   * <a href="#ItalyDeathPctTrend">Daily deaths trend</a>
#   * <a href="#ItalyIntCareProgress">Intensive Care Progress</a>
#   * <a href="#ItalyDailyIntCare">Daily Intensive Care</a>
#   * <a href="#ItalyNewCasesProgress">New Cases Progress</a>
# * <a href="#LombardiaCumulativeDeaths">Lombardia</a><br>
#   * <a href="#LombardiaCumulativeDeaths">Cumulative deaths</a>
#   * <a href="#LombardiaDailyDeaths">Daily deaths</a>
#   * <a href="#LombardiaDeathPctTrend">Daily deaths trend</a>
#   * <a href="#LombardiaIntCareProgress">Intensive Care Progress</a>
#   * <a href="#LombardiaDailyIntCare">Daily Intensive Care</a>
#   * <a href="#LombardiaNewCasesProgress">New Cases Progress</a>
# * <a href="#LazioCumulativeDeaths">Lazio</a><br>
#   * <a href="#LazioCumulativeDeaths">Cumulative deaths</a>
#   * <a href="#LazioDailyDeaths">Daily deaths</a>
#   * <a href="#LazioDeathPctTrend">Daily deaths trend</a>
#   * <a href="#LazioIntCareProgress">Intensive Care Progress</a>
#   * <a href="#LazioDailyIntCare">Daily Intensive Care</a>
#   * <a href="#LazioNewCasesProgress">New Cases Progress</a>
# * <a href="#ComparisonHealedDeaths">Comparison Italy Deaths vs Healed</a> 

# <a id="Dataset"><font size=22>Dataset</font></a><br>
# <a href="#Index">Back to Index</a>

# **Last Dataset Update**: 12/06/2020 17:00:00 (ref. https://github.com/pcm-dpc/COVID-19)

# In[ ]:


import numpy as np 
import pandas as pd 
import os

import cufflinks as cf
import plotly.offline
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

def pd_centered(df):
    return df.style.set_table_styles([
        {"selector": "th", "props": [("text-align", "center")]},
        {"selector": "td", "props": [("text-align", "center"), ("width", "100px")]}])


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns

from pandas import read_excel

my_sheet = 'dpc-covid19-ita-regioni'
file_name = '/kaggle/input/covid19initaly-20200612/dpc-covid19-ita-regioni.xlsx' 
df = read_excel(file_name, sheet_name = my_sheet)
del df['lat']
del df['long']
df=df.fillna('-')
#display(pd_centered(df.tail(5)))


# <a id="RegionSummary"><font size=22>Italy summary by region</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


ricoverati_con_sintomi = df.groupby("denominazione_regione")["ricoverati_con_sintomi"].max()
terapia_intensiva = df.groupby("denominazione_regione")["terapia_intensiva"].max()
totale_ospedalizzati = df.groupby("denominazione_regione")["totale_ospedalizzati"].max()
isolamento_domiciliare = df.groupby("denominazione_regione")["isolamento_domiciliare"].max()
#totale_attualmente_positivi = df.groupby("denominazione_regione")["totale_attualmente_positivi"].max()
totale_attualmente_positivi = df.groupby("denominazione_regione")["totale_positivi"].max()
#nuovi_attualmente_positivi = df.groupby("denominazione_regione")["nuovi_attualmente_positivi"].max()
nuovi_attualmente_positivi = df.groupby("denominazione_regione")["nuovi_positivi"].max()
dimessi_guariti = df.groupby("denominazione_regione")["dimessi_guariti"].max()
deceduti = df.groupby("denominazione_regione")["deceduti"].max()
totale_casi = df.groupby("denominazione_regione")["totale_casi"].max()
tamponi = df.groupby("denominazione_regione")["tamponi"].max()


#df2['x'] = italia.groupby("denominazione_regione")["ricoverati_con_sintomi"].max()
italia = pd.concat([ricoverati_con_sintomi, terapia_intensiva, totale_ospedalizzati, isolamento_domiciliare, 
                   totale_attualmente_positivi,nuovi_attualmente_positivi,dimessi_guariti,deceduti,
                   totale_casi, tamponi], axis=1)

#italia.sum(axis=0)
italia['Total'] = italia.sum(axis=1)
italia.loc['Total']= italia.sum()
italia.to_excel('italia.xlsx', sheet_name='data')

core = pd.DataFrame(data=italia)
core = core.sort_values(['totale_casi'], ascending=[False])
#core = core[['totale_casi', 'nuovi_attualmente_positivi', 'terapia_intensiva', 'deceduti', 'dimessi_guariti', 'tamponi', 'Total']]
core = core[['totale_casi', 'nuovi_positivi', 'terapia_intensiva', 'deceduti', 'dimessi_guariti', 'tamponi', 'Total']]
core.to_excel('core.xlsx', sheet_name='data')
display(pd_centered(italia))


# <a id="ItalyNewCases"><font size=22>Italy new cases</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


df['tempo'] = df['data'].map( lambda d: pd.to_datetime(d).timetuple().tm_yday )

de = df.groupby("tempo")["nuovi_positivi"].sum()
de.index = (np.asarray(de.index, dtype='datetime64[D]')-2)#+(np.asarray(de.index, dtype='timedelta64[Y]')-1)

import datetime
de.index=de.index + datetime.timedelta(days=365*50+13)


# In[ ]:


#ax1 = plt.axes()
#ax1.xaxis.label.set_visible(False)
#de.plot(figsize=(10,6), kind='bar', title="ITALY - NEW CASES")
de.iplot(kind="bar", theme="white", title="ITALY - NEW CASES")


# <a id="ItalyDailyNewCases"><font size=22>Daily new cases</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


nc = df.groupby("tempo")["nuovi_positivi"].sum()
#nc = df.groupby("tempo")["nuovi_attualmente_positivi"].sum()
nc = nc.to_frame()
nc['daily'] = nc['nuovi_positivi'].diff()
#nc['daily'] = nc['nuovi_attualmente_positivi'].diff()

nc.index = (np.asarray(nc.index, dtype='datetime64[D]')-2)
nc.index=nc.index + datetime.timedelta(days=365*50+13)

nc_daily = nc['daily'].to_frame()
show=nc.tail(10).sort_index(ascending=False, axis=0)
display(pd_centered(show))


# In[ ]:


nc_daily_graph = nc_daily['daily'] 
#plt.axes().xaxis.label.set_visible(False)
#nc_daily_graph.plot(figsize=(10,6), kind='bar', title="ITALY - DAILY NEW CASES")




nc_daily_graph.iplot(kind="bar", theme="white", title="ITALY - DAILY NEW CASES difference")


# <a id="ItalyCumulativeDeaths"><font size=22>Italy Cumulative Deaths</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


df['tempo'] = df['data'].map( lambda d: pd.to_datetime(d).timetuple().tm_yday )
de = df.groupby("tempo")["deceduti"].sum()

de.index = (np.asarray(de.index, dtype='datetime64[D]')-2)
de.index=de.index + datetime.timedelta(days=365*50+13)


#ax1 = plt.axes()
#ax1.xaxis.label.set_visible(False)
#de.plot(figsize=(10,6), kind='bar', title="ITALY - CUMULATIVE DEATHS")
de.iplot(kind="bar", theme="white", color="blue", title="ITALY - CUMULATIVE DEATHS")


# <a id="ItalyDailyDeaths"><font size=22>Italy daily Deaths</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


de = df.groupby("tempo")["deceduti"].sum()
de = de.to_frame()
de['daily'] = de['deceduti'].diff()
de_daily = de['daily'].to_frame()

de_daily.index = (np.asarray(de_daily.index, dtype='datetime64[D]')-2)
de_daily.index=de_daily.index + datetime.timedelta(days=365*50+13)

de_daily.tail(110).sort_index(ascending=False, axis=0)


# In[ ]:


de_daily.iplot(kind="bar", theme="white", color="red", title="ITALY - DAILY DEATHS")
#de_daily.plot(figsize=(10,6), kind='bar', title="ITALY - DAILY DEATHS")


# <a id="ItalyDeathPctTrend"><font size=22>Italy daily deaths trend</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


de_daily["pct"] = round(de_daily.pct_change(), 3)*100


de_daily["avg"] = round(de_daily["pct"].expanding().mean(), 3)
de_daily_pct = de_daily["pct"]
de_daily_avg = de_daily["avg"]
de_daily.tail(10).sort_index(ascending=False, axis=0)


# In[ ]:


de_daily_avg.iplot(kind="bar", theme="white", color="red", title="ITALY - DAILY DEATHS TREND")


# <a id="ItalyIntCareProgress"><font size=22>Italy intensive care progress</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


ti = df.groupby("tempo")["terapia_intensiva"].sum()
ti.index = (np.asarray(ti.index, dtype='datetime64[D]')-2)
ti.index=ti.index + datetime.timedelta(days=365*50+13)

ti.iplot(kind="bar", theme="white", color="blue", title="ITALY - INTENSIVE CARE PROGRESS")


# <a id="ItalyDailyIntCare"><font size=22>Italy daily Intensive Care</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


ti = ti.to_frame()
ti['daily'] = ti['terapia_intensiva'].diff()
ti_daily = ti['daily'].to_frame()
#ti.tail(10).sort_index(ascending=False, axis=0)


# In[ ]:


#ti_daily.plot(figsize=(10,6), kind='bar', title="ITALY - DAILY INTENSIVE CARE")
ti_daily.iplot(kind="bar", theme="white", color="pink", title="ITALY - DAILY INTENSIVE CARE")


# <a id="ItalyNewCasesProgress"><font size=22>Italy New Cases Progress</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


it_np = df.groupby("tempo")["nuovi_positivi"].sum()
it_np.index = (np.asarray(it_np.index, dtype='datetime64[D]')-2)
it_np.index=it_np.index + datetime.timedelta(days=365*50+13)

it_np.iplot(kind="bar", theme="white", title="ITALY - NEW CASES PROGRESS")


# <a id="LombardiaCumulativeDeaths"><font size=22>Lombardia Cumulative deaths</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


lombardia = df[df['denominazione_regione']=='Lombardia']
lombardia_de = lombardia.groupby("tempo")["deceduti"].sum()
lombardia_de.index = (np.asarray(lombardia_de.index, dtype='datetime64[D]')-2)
lombardia_de.index=lombardia_de.index + datetime.timedelta(days=365*50+13)
lombardia_de.tail(10).sort_index(ascending=False, axis=0).to_frame()


# In[ ]:



lombardia_de.iplot(kind="bar", theme="white", color="red", title="LOMBARDIA - CUMULATIVE DEATHS")


# <a id="LombardiaDailyDeaths"><font size=22>Lombardia daily deaths</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


lombardia_de['daily'] = lombardia['deceduti'].diff()
lombardia_de_daily = lombardia_de['daily'].to_frame()

#lombardia_de_daily.index = (np.asarray(lombardia_de_daily.index, dtype='datetime64[D]')-2)
#lombardia_de_daily.index=lombardia_de_daily.index + datetime.timedelta(days=365*50+13)

lombardia_de_daily.tail(10).sort_index(ascending=False, axis=0)


# In[ ]:


#lombardia_de_daily.plot(figsize=(10,6), kind='bar', title="LOMBARDIA - DAILY DEATHS")

lombardia_de_daily.iplot(kind="bar", theme="white", color="red", title="ITALY - DAILY DEATHS")


# <a id="LombardiaDeathPctTrend"><font size=22>Lombardia daily deaths trend</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


lombardia_de_daily["pct"] = round(lombardia_de_daily.pct_change(), 3)*100
lombardia_de_daily["avg"] = round(lombardia_de_daily["pct"].expanding().mean(), 3)
lombardia_de_daily_pct = lombardia_de_daily["pct"]
lombardia_de_daily_avg = lombardia_de_daily["avg"]
lombardia_de_daily.tail(10).sort_index(ascending=False, axis=0)


# In[ ]:


#plt.axes().xaxis.label.set_visible(False)
#lombardia_de_daily_avg.plot(figsize=(10,6), kind='bar', title="LOMBARDIA - DAILY DEATHS TREND")
lombardia_de_daily_avg.iplot(kind="bar", theme="white", color="red", title="LOMBARDIA - DAILY DEATHS TREND")


# <a id="LombardiaIntCareProgress"><font size=22>Lombardia Intensive Care Progress</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


#plt.axes().xaxis.label.set_visible(False)
lombardiati = lombardia.groupby("tempo")["terapia_intensiva"].sum()

lombardiati.index = (np.asarray(lombardiati.index, dtype='datetime64[D]')-2)
lombardiati.index=lombardiati.index + datetime.timedelta(days=365*50+13)

#lombardiati.plot(figsize=(10,6), kind='bar', title="LOMBARDIA - INTENSIVE CARE PROGRESS")
lombardiati.iplot(kind="bar", theme="white", color="blue", title="LOMBARDIA - INTENSIVE CARE PROGRESS")


# <a id="LombardiaDailyIntCare"><font size=22>Lombardia Daily Intensive Care</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


ti_lo = lombardia.groupby("tempo")["terapia_intensiva"].sum()
ti_lo = ti_lo.to_frame()
ti_lo['daily'] = ti_lo['terapia_intensiva'].diff()
ti_lo_daily = ti_lo['daily'].to_frame()


ti_lo.tail(10).sort_index(ascending=False, axis=0)


# In[ ]:


#ti_lo_daily.plot(figsize=(10,6), kind='bar', title="LOMBARDIA - DAILY INTENSIVE CARE")
ti_lo_daily.index = (np.asarray(ti_lo_daily.index, dtype='datetime64[D]')-2)
ti_lo_daily.index=ti_lo_daily.index + datetime.timedelta(days=365*50+13)
ti_lo_daily.iplot(kind="bar", theme="white", color="blue", title="LOMBARDIA - DAILY INTENSIVE CARE")


# <a id="LombardiaNewCasesProgress"><font size=22>Lombardia New Cases Progress</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


lombardia_np = lombardia.groupby("tempo")["nuovi_positivi"].sum()

lombardia_np.index = (np.asarray(lombardia_np.index, dtype='datetime64[D]')-2)
lombardia_np.index=lombardia_np.index + datetime.timedelta(days=365*50+13)
lombardia_np.iplot(kind="bar", theme="white", title="LOMBARDIA - NEW CASES PROGRESS")


# <a id="LazioCumulativeDeaths"><font size=22>Lazio Cumulative deaths</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


lazio = df[df['denominazione_regione']=='Lazio']
lazio_de = lazio.groupby("tempo")["deceduti"].sum()

lazio_de.index = (np.asarray(lazio_de.index, dtype='datetime64[D]')-2)
lazio_de.index=lazio_de.index + datetime.timedelta(days=365*50+13)

lazio_de.tail(10).sort_index(ascending=False, axis=0).to_frame()


# In[ ]:



lazio_de.iplot(kind="bar", theme="white", color="red", title="LAZIO - CUMULATIVE DEATHS")


# <a id="LazioDailyDeaths"><font size=22>Lazio daily deaths</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


lazio_de['daily'] = lazio['deceduti'].diff()
lazio_de_daily = lazio_de['daily'].to_frame()
#lazio_de_daily=lazio_de_daily.tail(10).sort_index(ascending=False, axis=0)


# In[ ]:


lazio_de_daily.iplot(kind="bar", theme="white", color="red", title="LAZIO - DAILY DEATHS")


# In[ ]:


lazio_de_daily_30 = lazio_de_daily.tail(30)
lazio_de_daily_30["deceduti"].iplot(kind="bar", color='red', theme="white", title="LAZIO - DAILY DEATHS over last 30 days", yTitle='Count')


# <a id="LazioDeathPctTrend"><font size=22>Lazio daily deaths trend</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


lazio_de_daily["pct"] = round(lazio_de_daily.pct_change(), 3)*100
lazio_de_daily["avg"] = round(lazio_de_daily["pct"].expanding().mean(), 3)
lazio_de_daily_pct = lazio_de_daily["pct"]
lazio_de_daily_avg = lazio_de_daily["avg"]
lazio_de_daily=lazio_de_daily.tail(10).sort_index(ascending=False, axis=0)


# In[ ]:


lazio_de_daily_avg.iplot(kind="bar", theme="white", color="red", title="LAZIO - DAILY DEATHS TREND")


# <a id="LazioIntCareProgress"><font size=22>Lazio Intensive Care Progress</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


lazioti = lazio.groupby("tempo")["terapia_intensiva"].sum()
lazioti.index = (np.asarray(lazioti.index, dtype='datetime64[D]')-2)
lazioti.index=lazioti.index + datetime.timedelta(days=365*50+13)
lazioti.iplot(kind="bar", theme="white", color="blue", title="LAZIO - INTENSIVE CARE PROGRESS")


# <a id="LazioDailyIntCare"><font size=22>Lazio Daily Intensive Care</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


ti_la = lazio.groupby("tempo")["terapia_intensiva"].sum()
ti_la = ti_la.to_frame()
ti_la['daily'] = ti_la['terapia_intensiva'].diff()
ti_la_daily = ti_la['daily'].to_frame()
ti_la.index = (np.asarray(ti_la.index, dtype='datetime64[D]')-2)
ti_la.index=ti_la.index + datetime.timedelta(days=365*50+13)
ti_la=ti_la.tail(10).sort_index(ascending=False, axis=0)


# In[ ]:



ti_la_daily.index = (np.asarray(ti_la_daily.index, dtype='datetime64[D]')-2)
ti_la_daily.index=ti_la_daily.index + datetime.timedelta(days=365*50+13)
ti_la_daily.iplot(kind="bar", theme="white", color="blue", title="ITALY - DAILY INTENSIVE CARE")


# <a id="LazioNewCasesProgress"><font size=22>Lazio New Cases Progress</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


lazio_np = lazio.groupby("tempo")["nuovi_positivi"].sum()

lazio_np.index = (np.asarray(lazio_np.index, dtype='datetime64[D]')-2)
lazio_np.index=lazio_np.index + datetime.timedelta(days=365*50+13)
lazio_np.iplot(kind="bar", theme="white", color="orange", title="LAZIO - NEW CASES PROGRESS")


# In[ ]:


lazio_np_30=lazio_np.tail(30)
lazio_np_30.iplot(kind="bar", bins=30, theme="white", title="LAZIO - NEW CASES over last 30 days", yTitle='Cases')


# <a id="ComparisonHealedDeaths"><font size=22>Comparison Italy Deaths vs Healed</font></a><br>
# <a href="#Index">Back to Index</a>

# In[ ]:


he = df.groupby("tempo")["dimessi_guariti"].sum().to_frame()
he['healed'] = he.diff()

de = df.groupby("tempo")["deceduti"].sum().to_frame()
de['deaths'] = de.diff()

he_de = pd.concat([he, de], axis=1)
he_de = he_de.drop('dimessi_guariti', axis=1)
he_de = he_de.drop('deceduti', axis=1)
he_de['diff'] = he_de['healed'] - de['deaths']
he_de=he_de.sort_values(by="tempo", ascending=True)#.head(10)


# In[ ]:


he_de.plot(figsize=(14,6), kind='bar', title="ITALY - HEALED vs DEATHS");
#he_de.iplot(kind='bar', title="ITALY - HEALED vs DEATHS", color=['green','red','blue'])

