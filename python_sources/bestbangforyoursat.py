#!/usr/bin/env python
# coding: utf-8

# # Best bang for your SAT
# This shows you how to choose a college based on earning prospective 6 years after graduation, given your SAT score!
# Methods:  
# 
# 1. Sort all colleges by their mean earning 6 years after graduation (mn_earn_wne_p6)
# 2. Along with that, records of these colleges' median SAT scores (reading, math and writing). This is considered to be *the necessary SAT scores to get you into the university with a reasonable chance*
# 3. Going through the list from highest mean earning down, for each college find if any (all) of its SAT scores is lower than *what's previously seen*:
#     * if yes, keep this college as it is the best investment at such SAT scores. And update the *what's previously seen* SAT score in bullet point \#3
#     * skip if the college has higher SAT scores.  

# In[ ]:


import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import sqlite3 
import seaborn as sns
import math
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
con = sqlite3.connect('../input/database.sqlite')
data = pd.read_sql('select INSTNM, UNITID, CCBASIC, cast(SATVRMID as int) SATVRMID, cast(SATMTMID as int) SATMTMID, cast(SATWRMID as int) SATWRMID, cast(mn_earn_wne_p6 as int) mn_earn_wne_p6, cast(mn_earn_wne_p7 as int) mn_earn_wne_p7, cast(mn_earn_wne_p8 as int) mn_earn_wne_p8, cast(mn_earn_wne_p9 as int) mn_earn_wne_p9, cast(mn_earn_wne_p10 as int) mn_earn_wne_p10 from Scorecard',con)
dataSAT = data[(data.SATVRMID>0)&(data.SATMTMID>0)&(data.SATWRMID>0)&(data.mn_earn_wne_p6>0)]


# In[ ]:


result_2 = pd.DataFrame()
ordered_dataSAT = dataSAT.sort(columns='mn_earn_wne_p6',ascending=False)
new_SAT = ordered_dataSAT.head(1)[['SATVRMID','SATMTMID','SATWRMID']].squeeze()
#new_SAT is placeholder for the lowest seen SAT
for index, row in ordered_dataSAT.iterrows():
    if (row[['SATVRMID','SATMTMID','SATWRMID']]<=new_SAT).any():
        result_2 = result_2.append(row)
        new_SAT = pd.concat([new_SAT, row[['SATVRMID','SATMTMID','SATWRMID']]], axis=1).min(axis=1)
to_plot = result_2[['INSTNM','mn_earn_wne_p6', 'SATVRMID','SATMTMID','SATWRMID']]
to_plot.columns = ['INSTNM','mn_earn_wne_p6', 0,1,2] #Need numeric symbols for reading, math and writing to annotate
to_plot = to_plot.set_index(['INSTNM','mn_earn_wne_p6']).stack()
to_plot = to_plot.reset_index()
to_plot.columns = ['INSTNM','mn_earn_wne_p6','SAT','value']
to_plot['label'] = to_plot['INSTNM']+','+to_plot['mn_earn_wne_p6'].astype(str)
#attempted to fill the annotation with same color as line hues but failed; 
label = to_plot[to_plot.SAT==2].sort(columns='label')
current_palette = sns.color_palette(n_colors=label.shape[0])
label['color'] = list(current_palette)
current_value = 0
label = label.sort(columns='value')
to_plot = to_plot.merge(label[['label','color']],how='left',on=['label'])
#plotting
pylab.rcParams['figure.figsize'] = 12, 25
plot = sns.pointplot(data = to_plot, x='SAT', y='value', hue='label')
plt.legend().set_visible(False)
#used to create space when annotations are too close
for index, row in label.iterrows():
    if row['value']-current_value<=5:
        label.loc[index,'value'] = current_value + 5
    current_value = label.loc[index]['value']
#bring back the actual x asix labels
labels = [u'Reading',u'Math',u'Writing']
plot.set_xticklabels(labels)
for index, row in label.iterrows():
    plt.text(row['SAT']+0.05,row['value'],row['label'])


# Obviously the criteria **any SAT score lower than lowest seen** creates a very convoluted picture: for example Institution of Native Indian and Alaska Native Culture was chosen despite its earning prospective isn't that great (\$22000) and relatively high reading and writing scores only because it has the lowest math requirement ever seen. Therefore the chart below only captures institutes where **ALL** SAT scores are lower than the lowest seen.

# In[ ]:


result_2 = pd.DataFrame()
ordered_dataSAT = dataSAT.sort(columns='mn_earn_wne_p6',ascending=False)
new_SAT = ordered_dataSAT.head(1)[['SATVRMID','SATMTMID','SATWRMID']].squeeze()
#new_SAT.columns = ['SATVRMID','SATMTMID','SATWRMID']
for index, row in ordered_dataSAT.iterrows():
    if (row[['SATVRMID','SATMTMID','SATWRMID']]<=new_SAT).all():
        #print new_SAT
        #print row[['SATVRMID','SATMTMID','SATWRMID']]
        result_2 = result_2.append(row)
        new_SAT = pd.concat([new_SAT, row[['SATVRMID','SATMTMID','SATWRMID']]], axis=1).min(axis=1)
to_plot = result_2[['INSTNM','mn_earn_wne_p6', 'SATVRMID','SATMTMID','SATWRMID']]
to_plot.columns = ['INSTNM','mn_earn_wne_p6', 0,1,2]
to_plot = to_plot.set_index(['INSTNM','mn_earn_wne_p6']).stack()
to_plot = to_plot.reset_index()
to_plot.columns = ['INSTNM','mn_earn_wne_p6','SAT','value']
to_plot.mn_earn_wne_p6 = to_plot.mn_earn_wne_p6.astype(str)
to_plot['label'] = to_plot['INSTNM']+','+to_plot['mn_earn_wne_p6']
to_plot = to_plot.merge(label[['label','color']],how='left',on=['label'])
pylab.rcParams['figure.figsize'] = 12, 25
plot = sns.pointplot(data = to_plot, x='SAT', y='value', hue='label')
plt.legend().set_visible(False)
label = to_plot[to_plot.SAT==2].sort(columns='label')
#to_plot.groupby('INSTNM').max().reset_index()
current_palette = sns.color_palette(n_colors=label.shape[0])
label['color'] = list(current_palette)
current_value = 0
label = label.sort(columns='value')
for index, row in label.iterrows():
    if row['value']-current_value<=5:
        label.loc[index,'value'] = current_value + 5
    current_value = label.loc[index]['value']
labels = [u'Reading',u'Math',u'Writing']
plot.set_xticklabels(labels)
for index, row in label.iterrows():
    plt.text(row['SAT']+0.05,row['value'],row['label'])


# Doing the same thing for 10 years earning, and MIT, Stanford and Princeton emerged:

# In[ ]:


dataSAT = data[(data.SATVRMID>0)&(data.SATMTMID>0)&(data.SATWRMID>0)&(data.mn_earn_wne_p10>0)]
result_2 = pd.DataFrame()
ordered_dataSAT = dataSAT.sort(columns='mn_earn_wne_p10',ascending=False)
new_SAT = ordered_dataSAT.head(1)[['SATVRMID','SATMTMID','SATWRMID']].squeeze()
#new_SAT.columns = ['SATVRMID','SATMTMID','SATWRMID']
for index, row in ordered_dataSAT.iterrows():
    if (row[['SATVRMID','SATMTMID','SATWRMID']]<=new_SAT).any():
        #print new_SAT
        #print row[['SATVRMID','SATMTMID','SATWRMID']]
        result_2 = result_2.append(row)
        new_SAT = pd.concat([new_SAT, row[['SATVRMID','SATMTMID','SATWRMID']]], axis=1).min(axis=1)
to_plot = result_2[['INSTNM','mn_earn_wne_p10', 'SATVRMID','SATMTMID','SATWRMID']]
to_plot.columns = ['INSTNM','mn_earn_wne_p10', 0,1,2]
to_plot = to_plot.set_index(['INSTNM','mn_earn_wne_p10']).stack()
to_plot = to_plot.reset_index()
to_plot.columns = ['INSTNM','mn_earn_wne_p10','SAT','value']
to_plot.mn_earn_wne_p10 = to_plot.mn_earn_wne_p10.astype(str)
to_plot['label'] = to_plot['INSTNM']+','+to_plot['mn_earn_wne_p10']
#to_plot = to_plot.merge(label[['label','color']],how='left',on=['label'])
pylab.rcParams['figure.figsize'] = 12, 25
plot = sns.pointplot(data = to_plot, x='SAT', y='value', hue='label')
plt.legend().set_visible(False)
label = to_plot[to_plot.SAT==2].sort(columns='label')
#to_plot.groupby('INSTNM').max().reset_index()
current_palette = sns.color_palette(n_colors=label.shape[0])
current_value = 0
label = label.sort(columns='value')
for index, row in label.iterrows():
    if row['value']-current_value<=5:
        label.loc[index,'value'] = current_value + 5
    current_value = label.loc[index]['value']
labels = [u'Reading',u'Math',u'Writing']
plot.set_xticklabels(labels)
for index, row in label.iterrows():
    plt.text(row['SAT']+0.05,row['value'],row['label'])


# In[ ]:


dataSAT = data[(data.SATVRMID>0)&(data.SATMTMID>0)&(data.SATWRMID>0)&(data.mn_earn_wne_p10>0)]
result_2 = pd.DataFrame()
ordered_dataSAT = dataSAT.sort(columns='mn_earn_wne_p10',ascending=False)
new_SAT = ordered_dataSAT.head(1)[['SATVRMID','SATMTMID','SATWRMID']].squeeze()
#new_SAT.columns = ['SATVRMID','SATMTMID','SATWRMID']
for index, row in ordered_dataSAT.iterrows():
    if (row[['SATVRMID','SATMTMID','SATWRMID']]<=new_SAT).all():
        #print new_SAT
        #print row[['SATVRMID','SATMTMID','SATWRMID']]
        result_2 = result_2.append(row)
        new_SAT = pd.concat([new_SAT, row[['SATVRMID','SATMTMID','SATWRMID']]], axis=1).min(axis=1)
to_plot = result_2[['INSTNM','mn_earn_wne_p10', 'SATVRMID','SATMTMID','SATWRMID']]
to_plot.columns = ['INSTNM','mn_earn_wne_p10', 0,1,2]
to_plot = to_plot.set_index(['INSTNM','mn_earn_wne_p10']).stack()
to_plot = to_plot.reset_index()
to_plot.columns = ['INSTNM','mn_earn_wne_p10','SAT','value']
to_plot.mn_earn_wne_p10 = to_plot.mn_earn_wne_p10.astype(str)
to_plot['label'] = to_plot['INSTNM']+','+to_plot['mn_earn_wne_p10']
#to_plot = to_plot.merge(label[['label','color']],how='left',on=['label'])
pylab.rcParams['figure.figsize'] = 12, 25
plot = sns.pointplot(data = to_plot, x='SAT', y='value', hue='label')
plt.legend().set_visible(False)
label = to_plot[to_plot.SAT==2].sort(columns='label')
#to_plot.groupby('INSTNM').max().reset_index()
current_palette = sns.color_palette(n_colors=label.shape[0])
current_value = 0
label = label.sort(columns='value')
for index, row in label.iterrows():
    if row['value']-current_value<=5:
        label.loc[index,'value'] = current_value + 5
    current_value = label.loc[index]['value']
labels = [u'Reading',u'Math',u'Writing']
plot.set_xticklabels(labels)
for index, row in label.iterrows():
    plt.text(row['SAT']+0.05,row['value'],row['label'])

