#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In this notebook, I would like to share an analysis on aircraft delays. I also performed a regression to better understand the impact of each features. Feel free to tell me what you think in the comments.
# #  Preview of the data
# #  Comparative exploration between January and February
# ## Airline company
# ## Seasonality
# ## Let's make the journeys
# 
# 
# 
# # Studies of planned flights duration and prediction model
# ## Relationship between planned travel time and seasonality
# ## Predictions and interpretation (Coming soon)
# Variation: "The most likely flight time."
# 
# 
# 
# 
# **Acknowledgement:** Many thank to Fabien Daniel for his advices and encouragements.

# # 0 Preview of the dataset

# In[ ]:


d=pd.read_csv('../input/flights.csv')
d.head()


# In[ ]:


miss = []
for col in d.columns:
    i=d[col].isnull().sum()
    miss_v_p = i*100/d.shape[0]
    miss.append(miss_v_p)
    print ('{} -----> {}%'.format(col, 100-i*100/d.shape[0]))

dico = {'columns': d.columns, 'filling rate': 100-np.array(miss), 'taux nan': miss}
#print(miss, dico['taux de remplissage'])
tr=pd.DataFrame(dico)
r = range(tr.shape[0])
barWidth=0.85
plt.figure(figsize=(20,8))
plt.bar(r, tr['filling rate'], color='#a3acff', edgecolor='white', width=barWidth)
plt.bar(r, tr['taux nan'], bottom=tr['filling rate'], color ='#b5ffb9', edgecolor= 'white', width=barWidth)
plt.title('fill rate representation')
plt.xticks(r, tr['columns'], rotation='vertical')
plt.xlabel('columns')
plt.ylabel('filling rate')
plt.margins(0.01)


# In[ ]:


def conv_min(i):
    """to convert 'HH MM' to minutes"""
    if np.isnan(i):
        return(i)
    i=int(i)
    s=str(i)
    sign=1
    if s[0]=='-':
        sign=-1
        s=s[1:]
    if len(s)<3:
        return i
    else:
        return sign*(int(s[:-2])*60+int(s[-2:]))
    
    
d['CRS_DEP_MIN']=d['DEPARTURE_TIME'].apply(conv_min)
d['CRS_ARR_MIN']= d['ARRIVAL_TIME'].apply(conv_min)


# In[ ]:


d.drop(columns=['WHEELS_OFF', 'WHEELS_ON', 'TAXI_IN', 'TAXI_OUT', 'DIVERTED', 
                'CANCELLED', 'CANCELLATION_REASON', 'AIR_SYSTEM_DELAY','SECURITY_DELAY', 
                'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY','WEATHER_DELAY'], inplace=True)#'TAIL_NUMBER', 

d.head()


# # 'ARRIVAL_DELAY' our target

# In[ ]:


d_delay = d[d['ARRIVAL_DELAY']>0]
print("the percentage of planes late in 2015 is %.2f"%(d_delay.shape[0]*100/d.shape[0]))
d_ok = d[d['ARRIVAL_DELAY']==0]
print("the percentage of planes right on time in 2015 is %.2f"%(d_ok.shape[0]*100/d.shape[0]))
d_advance = d[d['ARRIVAL_DELAY']<0]
print("the percentage of planes in advance in 2015 is %.2f"%(d_advance.shape[0]*100/d.shape[0]))


# In[ ]:


plt.boxplot(d.loc[:, ['ARRIVAL_DELAY']].dropna().T, showfliers=False)
plt.ylabel('minutes of delays')
plt.title('Distribution of delays')


# # 1 Comparative exploration between January and February
# ## 1.1 Airline company

# In[ ]:


jan = d[d['MONTH']==1]
feb = d[d['MONTH']==2]


# In[ ]:


lab = jan['AIRLINE'].unique()

l=[]
plt.figure(figsize=(20,8))
plt.subplot(121)
for carrier in lab:
    cl=(jan[jan['AIRLINE']==carrier]['ARRIVAL_DELAY'])
    l.append(cl.dropna().sort_values())
ax1 = plt.boxplot(l, patch_artist=True, showfliers=False) 
#print(l[0], type(d['UNIQUE_CARRIER'].unique()))
ax1 = plt.xticks(range(1, jan['AIRLINE'].nunique()+1), lab)
ax1 = plt.title('Distribution of delays by company in JANUARY')

l=[]
plt.subplot(122)
for carrier in lab:
    cl=(feb[feb['AIRLINE']==carrier]['ARRIVAL_DELAY'])
    l.append(cl.dropna().sort_values())
ax2 = plt.boxplot(l, patch_artist=True, showfliers=False) 
#print(l[0], type(d['UNIQUE_CARRIER'].unique()))
ax2 = plt.xticks(range(1, feb['AIRLINE'].nunique()+1), lab)
ax2 = plt.title('Distribution of delays by company in FEBRUARY')


# The distribution of delays by company seems similar between January and February. This 'AIRLINE' feature seems interesting for our predictions<br>
# The qualitity of the company surely plays a role. However, as we can see below these compagny can be specialized for certain types of journey (long, short,
# surely the geographical area...).

# In[ ]:



plt.style.use('default')
sns.pairplot(jan.loc[:,['ARRIVAL_DELAY', 'DISTANCE', 'SCHEDULED_TIME', 'AIRLINE']], hue='AIRLINE', plot_kws={'s':14})
plt.title('JANUARY flights')


# 

# In[ ]:


t_time = d[d['ARRIVAL_TIME']<90]
t_time[t_time['ARRIVAL_TIME']>60]
#d['TAIL_NUMBER'].unique()


# # 1.2 Saisonality
# #### It is easy to see weekly seasonality with the number of flights...

# In[ ]:



plt.figure(figsize=(17,5))

plt.subplot(121)
dgrp = jan.loc[:,['DAY', 'FLIGHT_NUMBER', 'ARRIVAL_DELAY']].groupby('DAY').count()
ax1 = plt.plot(dgrp.index, dgrp['FLIGHT_NUMBER'])
ax1 = plt.title('number of flights by day of JANUARY')

plt.subplot(122)
dgrp = feb.loc[:,['DAY', 'FLIGHT_NUMBER', 'ARRIVAL_DELAY']].groupby('DAY').count()
ax2 = plt.plot(dgrp.index, dgrp['FLIGHT_NUMBER'])
ax2 = plt.title('number of flights by day of FEBRUARY')


# **Rq**: Above, we can also note irregularities related to vacation days.<br><br>
# #### ... But when we talk about delays, the seasonality is much less obvious:

# In[ ]:



plt.figure(figsize=(17,5))

plt.subplot(121)
mean_delay = jan.loc[:,['DAY', 'DAY_OF_WEEK', 'FLIGHT_NUMBER', 'ARRIVAL_DELAY']].groupby('DAY').mean()
ax1 = plt.bar(mean_delay.index, mean_delay['ARRIVAL_DELAY'])
ax1 = plt.title('Average delays according to the day of JANUARY 2015')

plt.subplot(122)
mean_delay = feb.loc[:,['DAY', 'DAY_OF_WEEK', 'FLIGHT_NUMBER', 'ARRIVAL_DELAY']].groupby('DAY').mean()
ax2 = plt.bar(mean_delay.index, mean_delay['ARRIVAL_DELAY'])
ax2 = plt.title('Average delays according to the day of FEBRUARY 2015')


# In[ ]:


plt.figure(figsize=(17,5))

plt.subplot(121)
week_delay = jan.loc[:,['DAY', 'DAY_OF_WEEK', 'FLIGHT_NUMBER', 'ARRIVAL_DELAY']].groupby('DAY_OF_WEEK').mean()
ax1 = plt.bar(week_delay.index, week_delay['ARRIVAL_DELAY'])
ax1 = plt.title('Average of the delays according to the day of the week in JANUARY')

plt.subplot(122)
week_delay = feb.loc[:,['DAY', 'DAY_OF_WEEK', 'FLIGHT_NUMBER', 'ARRIVAL_DELAY']].groupby('DAY_OF_WEEK').mean()
ax2 = plt.bar(week_delay.index, week_delay['ARRIVAL_DELAY'])
ax2 = plt.title('Average of the delays according to the day of the week in FEBRUARY')


# Eventually, we could note a daily seasonality by averaging the delays for each minute of the day:

# In[ ]:


plt.figure(figsize=(17,5))

plt.subplot(121)
h_delay = jan.loc[:,['CRS_DEP_MIN', 'DAY_OF_WEEK', 'FLIGHT_NUMBER', 'ARRIVAL_DELAY']].groupby('CRS_DEP_MIN').mean()
#display(h_delay.head())
ax1=plt.plot(h_delay.index, h_delay['ARRIVAL_DELAY'], '.')
ax1=plt.title("Average delays based on departure time in JANUARY")
ax1=plt.xlabel('day converted to minutes (1day = 1440min)')
ax1=plt.ylabel('average delays')

plt.subplot(122)
h_delay = feb.loc[:,['CRS_DEP_MIN', 'DAY_OF_WEEK', 'FLIGHT_NUMBER', 'ARRIVAL_DELAY']].groupby('CRS_DEP_MIN').mean()
#display(h_delay.head())
ax2=plt.plot(h_delay.index, h_delay['ARRIVAL_DELAY'], '.')
ax2=plt.title("Average delays based on departure time in FEBRUARY")
ax2=plt.xlabel('day converted to minutes (1day = 1440min)')
ax2=plt.ylabel('average delays')


# The average delay increases in the afternoon and reaches a high point in the early evening for departures and towards 23h for arrivals. Departure time and arrival time will be useful for our predictions
# #### Same representation but without averaging delays:

# In[ ]:


plt.figure(figsize=(17,5))

plt.subplot(121)
ax1 = sns.regplot(jan.loc[:, 'CRS_DEP_MIN'], jan.loc[:,'ARRIVAL_DELAY'], scatter_kws={"color":"darkred","alpha":0.05,"s":1} )
ax1 = plt.title("delays according to 'departure time' in JANUARY")

plt.subplot(122)
ax2 = sns.regplot(feb.loc[:, 'CRS_DEP_MIN'], feb.loc[:,'ARRIVAL_DELAY'], scatter_kws={"color":"darkred","alpha":0.05,"s":1} )
ax2 = plt.title("delays according to 'departure time' in FEBRUARY")


# Above, we understand that the dispersion of averages at the beginning of the day is due to the fact that there are fewer flights at this time.

# In[ ]:


jan.head()


# # 1.3 Let's make the journeys
# The problem is that we have many different airports. We will therefore schematize the flight paths in this part.

# In[ ]:


airp = pd.read_csv('../input/airports.csv')
airp.head()


# In[ ]:


airp_state = airp.loc[:, ['IATA_CODE', 'STATE', 'CITY']]
ori_airp = airp_state.rename(columns={'IATA_CODE':'ORIGIN_AIRPORT','STATE': 'ORIGIN_STATE_ABR', 'CITY':'ORIGIN_CITY_NAME'})#rename for Origine
dest_airp = airp_state.rename(columns={'IATA_CODE':'DESTINATION_AIRPORT','STATE': 'DEST_STATE_ABR', 'CITY': 'DEST_CITY_NAME'})#rename for Destination
display(dest_airp.head(2))
temp = d.merge(ori_airp, on='ORIGIN_AIRPORT')
d = temp.merge(dest_airp, on='DESTINATION_AIRPORT')
d.head(3)


# In[ ]:


#d.info()#I check the new column 'ORIGIN_STATE_ABR' contains string.


# ### One Hot Encoder trips may take too much computing time
# We will group states according to time zones.
# In addition this will also allow us to automatically determine the time zones later.

# In[ ]:


states = airp['STATE'].unique()
states


# In[ ]:


geo_states = {'East_N' : ['OH', 'NY', 'PA', 'IN', 'ME', 'MI', 'VI', 'MA', 'VA', 'NJ', 'PR', 'MD', 'NE', 'CT', 'RI', 'AL', 'VT', 'WV', 'NH', 'DE'],
             'East_S': ['FL', 'GA', 'SC', 'NC'],
             'Cent_N':['ND', 'MN', 'WI', 'SD', 'IA', 'IL', 'TN', 'KY'],
             'Cent_S':['TX','OK', 'LA', 'AR', 'MS', 'KS', 'MO'],
             'Mont_N' : ['ID', 'WY', 'MT'],
             'Mont_S': ['AZ', 'NM', 'UT', 'CO'],
             'Pac_N' : ['OR', 'WA'],
             'Pac_S' : ['NV', 'CA'],
             'Alask': ['AK'],
             'Haw':['HI'],
             'Territory':['GU','AS']}


# In[ ]:


"""Classification aid"""
rest = list(states)
for key, item in geo_states.items():
    print (key, item)
    for k in item:
        #print(k)
        try:
            rest.remove(k)
        except:
            print(k ,'not in liste')
print('rest: ',len(rest), rest) 


# In[ ]:


def compare_word(word):
    """Check if 'word' can be referenced to one of our clusters. Each category is a key of our dico 'states'"""
    if word == ' 'or word == 'nan':
        pass
    for key, val in geo_states.items():
        if word in val:
            return key 
    pass


def simple_geo (data, trajet=['ORIGIN_STATE_ABR','DEST_STATE_ABR']):
    """defines a new columns in 'data' with geographical simplification. This allows a cluster according to the location and trajet."""
    i=0
    name=['ORI_GEO', 'DEST_GEO']
    for lab in trajet:
        list_column=[]
        data[name[i]]=data[lab].apply(compare_word)
        print('Column {} has been initialized'.format(name[i]))
        i+=1
    
def simple_traj(d, trajet=['ORIGIN_STATE_ABR','DEST_STATE_ABR'], drop_loc=False):
    simple_geo(d, trajet=trajet )
    d['path']=d['ORI_GEO']+'-->'+d['DEST_GEO']
    print("'path' initialized")
    if drop_loc:
        d.drop(columns=['ORI_GEO', 'DEST_GEO'], inplace=True)
        print("We remove 'ORI_GEO' and 'DEST_GEO'")


# In[ ]:


simple_traj(d, drop_loc=True)


# In[ ]:


"""Let's redefine our tables for January and February to get the update 'path'."""
jan = d[d['MONTH']==1]
feb = d[d['MONTH']==2]


# In[ ]:


plt.figure(figsize=(13,17))
plt.subplots_adjust(wspace = 0.3)

plt.subplot(121)
d_traj_jan = jan.loc[:,['ARRIVAL_DELAY','path']].groupby(['path']).mean()
ax1 = plt.barh(d_traj_jan.index, d_traj_jan['ARRIVAL_DELAY'])
ax1 = plt.title('Average delays by path in JANUARY ')
ax1 = plt.grid(True)

plt.subplot(122)
d_traj_feb = feb.loc[:,['ARRIVAL_DELAY','path']].groupby(['path']).mean()
ax2 = plt.barh(d_traj_jan.index, d_traj_feb['ARRIVAL_DELAY'])
ax2 = plt.title('Average delays by path in FEBRUARY ')
ax2 = plt.grid(True)


# There seem to be similarities in the average delays between these two months.<br>
# The 'path' could therefore have an impact on delays. <br>
# Of course, this impact could be only a consequence of features already seen (as the distance and the airline). (We 'll have the answer only at the end of the notebook)

# # Conclusion : 
# We compared the delays for two consecutive months. These results are influenced by the seasons (the winters).

# # 2 Studies of planned flights duration and prediction model
# 
# ## 2.1 Relationship between planned travel time and seasonality
# 
# 
# 
# Before performing predictions, **let's develop the link between delay and programmed flight time**. This is an **essential** point of the notebook :<br>
# Let define **'time_f'** the real time of the flight.
# 

# In[ ]:


d['time_f']=d['SCHEDULED_TIME']+d['ARRIVAL_DELAY']


# Let take 2 differents path to compare:

# In[ ]:


d_GA_CA = d[(d['ORIGIN_CITY_NAME']=='Atlanta')&(d['DEST_CITY_NAME']=='Los Angeles')]
#d_MA_TX = d[(d['ORIGIN_STATE_ABR']=='MA')&(d['DEST_STATE_ABR']=='TX')]
d_NY_TX = d[(d['ORIGIN_CITY_NAME']=='New York')&(d['DEST_CITY_NAME']=='Dallas')]


# In[ ]:


def graph_crs_time(d, lab='DAY_OF_WEEK', bar=False):
    group = d.groupby([lab, 'SCHEDULED_TIME']).count()
    dico = {'nb':group.iloc[:,1], lab :group.index.get_level_values(0), 'time_f':group.index.get_level_values(1)}
    r = pd.DataFrame(dico)
    plt.style.use('default')
    plt.xlim((r['time_f'].quantile(0.007),r['time_f'].quantile(0.993)))
    if bar:
        """
        sns.kdeplot(data=r['time_f'], data2=r['nb'], , hue=r[lab], 
                        palette=sns.color_palette("hls", r[lab].nunique()))
        """
        sns.barplot(x=r['time_f'], y=r['nb'], hue=r[lab], 
                        palette=sns.color_palette("hls", r[lab].nunique()))
                        
    else:
        sns.scatterplot(x=r['time_f'], y=r['nb'], hue=r[lab], 
                        legend='full', 
                        palette=sns.color_palette("hls", r[lab].nunique()),
                        alpha = 0.8
                         )
    plt.title('Number of flights for each scheduled duration from {} to {}'.format(d['ORIGIN_CITY_NAME'].iloc[0], d['DEST_CITY_NAME'].iloc[0] ))
    plt.show()
    
    
def graph_time_f(d, lab='DAY_OF_WEEK', bar=False):
    group = d.groupby([lab, 'time_f']).count()
    dico = {'nb':group.iloc[:,1], lab :group.index.get_level_values(0), 'time_f':group.index.get_level_values(1)}
    r = pd.DataFrame(dico)
    plt.style.use('default')
    plt.xlim((r['time_f'].quantile(0.007),r['time_f'].quantile(0.993)))
    if bar:
        sns.barplot(x=r['time_f'], y=r['nb'], hue=r[lab], 
                        palette=sns.color_palette("hls", r[lab].nunique()))
    else:
    
        sns.scatterplot(x=r['time_f'], y=r['nb'], hue=r[lab], 
                        legend='full', 
                        palette=sns.color_palette("hls", r[lab].nunique()),
                        alpha = 0.8
                         )
    plt.title('Number of flights for each duration observed from {} to {}'.format(d['ORIGIN_CITY_NAME'].iloc[0], d['DEST_CITY_NAME'].iloc[0] ))
    plt.show()    


# ### 2.1.1 Monthly seasonality:

# In[ ]:


graph_time_f(d_NY_TX, lab='MONTH')
graph_crs_time(d_NY_TX, lab='MONTH')


# In[ ]:


#graph_time_f(d_Bos_Nash, lab='MONTH', bar=True)
#graph_crs_time(d_Bos_Nash, lab='MONTH')
graph_time_f(d_GA_CA, lab='MONTH')
graph_crs_time(d_GA_CA, lab='MONTH')


# In winter, the scheduled flight time is longer than in the summer.

# ### 2.1.2 Weekly seasonality : 

# In[ ]:


graph_crs_time(d_NY_TX, lab='DAY_OF_WEEK')


# Above, Travel time planning does not seem to be affected by the day of the week.<br>
# (In fact, we will see below that it is well influenced on average by the day of the week)

# In[ ]:


plt.figure(figsize=(17,5))

d01=d_NY_TX[d_NY_TX['MONTH']==1]
d02=d_NY_TX[d_NY_TX['MONTH']==2]

mean_time = d01.loc[:,['DAY', 'DAY_OF_WEEK', 'SCHEDULED_TIME', 'ARRIVAL_DELAY', 'time_f']].groupby('DAY').mean()
plt.subplot(121)
plt.bar(mean_time.index, mean_time['time_f'])
plt.ylim(min(mean_time['time_f']), max(mean_time['time_f']))
plt.title('average flight duration (New York->Dallas) according the day of January 2015')

plt.subplot(122)
#mean_time = d01.loc[:,['DAY_OF_MONTH', 'ARR_DELAY', 'CRS_ELAPSED_TIME','time_f']].groupby('DAY_OF_MONTH').mean()
p1 = plt.bar(mean_time.index, mean_time['SCHEDULED_TIME'])
p2 = plt.bar(mean_time.index, mean_time['ARRIVAL_DELAY'], bottom=mean_time['SCHEDULED_TIME'], width=0.3)
plt.ylim(min(mean_time['time_f']), max(mean_time['time_f']))
plt.xlabel('january day')
plt.ylabel('duration in minutes')
plt.legend([p1[0], p2[0]], ['Average scheduled time', 'Average delay'])
plt.title('average flight duration(New York->Dallas) according the day of January 2015')


# Here we can see that the scheduled elapsed time has a weekly seasonal component. We also see the impact of holidays :

# In[ ]:



d01=d_GA_CA[d_GA_CA['MONTH']==1]
d02=d_GA_CA[d_GA_CA['MONTH']==2]


plt.figure(figsize=(17,4))
plt.subplot(121)
mean_time = d01.loc[:,['DAY', 'ARRIVAL_DELAY', 'SCHEDULED_TIME','time_f']].groupby('DAY').mean()
p1 = plt.bar(mean_time.index, mean_time['SCHEDULED_TIME'])
p2 = plt.bar(mean_time.index, mean_time['ARRIVAL_DELAY'], bottom=mean_time['SCHEDULED_TIME'], width=0.3)
plt.ylim(min(mean_time['time_f']), max(mean_time['time_f']))
plt.xlabel('January day')
plt.ylabel('duration in minutes')
plt.legend([p1[0], p2[0]], ['Average scheduled time', 'Average delay'])
plt.title('average flight duration(Atl->LA) according the day of January 2015')

plt.subplot(122)
mean_time = d02.loc[:,['DAY', 'ARRIVAL_DELAY', 'SCHEDULED_TIME','time_f']].groupby('DAY').mean()
p1 = plt.bar(mean_time.index, mean_time['SCHEDULED_TIME'])
p2 = plt.bar(mean_time.index, mean_time['ARRIVAL_DELAY'], bottom=mean_time['SCHEDULED_TIME'], width=0.3)
plt.ylim(min(mean_time['time_f']), max(mean_time['time_f']))
plt.xlabel('February day')
plt.ylabel('duration in minutes')
plt.legend([p1[0], p2[0]], ['Average scheduled time', 'Average delay'])
plt.title('average flight duration (Atl->LA) according the day of February 2015')


# In addition to the seasonally scheduled travel times, we notice an increase in travel time in mid-February. It appends at the begining of hollidays...

# 

# To be continued...

# # Let include holidays
# 
# 
# 

# In[ ]:


from datetime import timedelta
holidays = ['2015-01-01', '2015-01-19', '2015-02-16', '2015-05-25', 
            '2015-07-04', '2015-09-07', '2015-10-12', '2015-11-11', '2015-11-11', '2015-12-25', '2016-01-01']
holid=[]
for date in holidays:
    holid.append(pd.Timestamp(date))
holid


# In[ ]:


def date_dep(i, data, y=2015):
    #i=d.index
    return pd.Timestamp(data.loc[i,'YEAR'], data.loc[i,'MONTH'], data.loc[i,'DAY'])

#ind=pd.Series(d.index)
#d['FL_DATE']=list(ind.apply(lambda x : date_dep(x,data=d)))#take too much time to compute


# In[ ]:



d['FL_DATE']=d['YEAR'].map(str)+'-'+d['MONTH'].map(str)+'-'+d['DAY'].map(str)
d['FL_DATE'] = d['FL_DATE'].apply(pd.Timestamp)


# In[ ]:


def holi_feature(data):
    """
    Add a new feature to the dataframe 'data':
    'abs_H': the number of days separating the current date from the closest holiday
    """
    #data['DATE_DEP']=pd.Series(data.index).apply(lambda x : date_dep(x,data=data))
    dep_day=pd.Series(data['FL_DATE'].unique())
    day_y=dep_day.apply(pd.Timestamp)
    #print(type(day_y), pd.Series(day_y))
    
    d_abs = day_y.apply(lambda x: (min([abs(x-h) for h in holid])).days)
    dico_holi = {'FL_DATE' : dep_day, 'abs_H' : d_abs}
    d_holidays=pd.DataFrame(dico_holi)
    #display(d_holidays)                      
    data = pd.merge(data, d_holidays, on='FL_DATE')
    return data


# In[ ]:


d = holi_feature(d)


# # Let check our new features in the dataframe:

# In[ ]:


d.iloc[:5,-13:]


# To be continued...

# # 2.2 Predictions and Interpretations
# 
# We have seen above that the seasonal influence on delays could be offset by the planned duration of flight time. <br>
# The model below ** facilitates interpretation **. <br> <br>
# 
# ## Method:
# 
# Let's try to predict the duration of the trip and then subtract the expected transport time to obtain the prediction of the delay. <br>
# 
# ## note :
# We could perform the regression directly on ARRIVAL_DELAY. Here, **we are not looking for the best performing model**, but the one that offers **the most readability** for the comprehension.

# In[ ]:


#from sklearn.linear_model import ElasticNetCV, Ridge, ElasticNet
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn import preprocessing
from scipy import sparse
from sklearn.linear_model import SGDRegressor, Lasso
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn import metrics
from datetime import timedelta


# In[ ]:


d.dropna(subset=['ARRIVAL_DELAY'], axis=0, inplace=True)


# In[ ]:



d=d.sample(1000000)


# Let's treat the number of days separating holidays as categorical:

# In[ ]:


d['abs_H']=d['abs_H'].apply(str)


# Other categorical featrues : 

# In[ ]:


week = {1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'}
month = {1:'jan',2:'feb',3:'mars',4:'apr', 5:'may',6:'jun', 7:'jul',8:'aug',9:'sept',10:'oct',11:'nov', 12:'dec'}

d['DAY_W']=d['DAY_OF_WEEK'].apply(lambda x: week[x])
d['M']=d['MONTH'].apply(lambda x: month[x])


# In[ ]:


categ_feat = pd.get_dummies(d.loc[:,['ORIGIN_CITY_NAME', 'DEST_CITY_NAME', 'DAY_W', 'AIRLINE', 'M', 'abs_H', 'path']] , sparse=False,
                            prefix=['ORIGIN', 'DEST', 'DAY', 'CARRIER', 'M', 'd_H', 'dir'])


# In[ ]:


COL_CAT=categ_feat.columns
d_categ = sparse.csr_matrix(categ_feat)
COL_CAT.shape


# In[ ]:


d_y = d.loc[:,['time_f', 'ARRIVAL_DELAY']]
d_num = d.loc[:,['DISTANCE', 'CRS_DEP_MIN', 'CRS_ARR_MIN', 'SCHEDULED_TIME']]
COL_NUM=d_num.columns
N_NUM = COL_NUM.shape[0]
d_num_s = sparse.csr_matrix(d_num)
d_work = sparse.hstack((d_num_s, d_categ))


# **note :** We can choose whether to use 'SCHEDULED_TIME' in our regression or not. It depends on the interpretation we want give to that regression wich predict "the most likely flight time."
# (Here I use it.)

# In[ ]:


xtr, xte, ytr, yte = train_test_split(d_work,
                                     d_y,
                                     test_size=0.2, random_state=0)


# In[ ]:


X_train_num = xtr[:,:N_NUM].toarray()#here we can decide to include or not (NUM_COL or NUM_COL-1)
scale = preprocessing.StandardScaler().fit(X_train_num)
X_train_std = scale.transform(X_train_num)


# In[ ]:


X_train_categ = xtr[:,N_NUM:]
print(type(X_train_std), type(X_train_categ))
X_train = sparse.hstack((sparse.csr_matrix(X_train_std), X_train_categ))


# In[ ]:


X_test_num = xte[:,:N_NUM].toarray()
X_test_std = scale.transform(X_test_num[:,:N_NUM])#here we can decide to include or not (NUM_COL or NUM_COL-1)
X_test_categ = xte[:,N_NUM:]
X_test = sparse.hstack((sparse.csr_matrix(X_test_std), X_test_categ))


# In[ ]:


n_alpha = 5#200
alpha = np.logspace(-5,-2,n_alpha)
param_grid = {'alpha' : alpha, "l1_ratio" : [0.8, 0.6, 0.7, 0.9]}

#d.loc[:,['DISTANCE', 'CRS_DEP_MIN', 'CRS_ARR_MIN', 'SCHEDULED_TIME']]


# In[ ]:


"""determine the hypers parametres"""
#reg = GridSearchCV(SGDRegressor(), param_grid=param_grid, cv=5, scoring='neg_mean_absolute_error')
#reg.fit(X_train, ytr['time_f'])
#reg.best_params_

reg = SGDRegressor(alpha=0.01, l1_ratio=0.7)
#reg= Lasso(alpha=0.01)
reg.fit(X_train, ytr['time_f'])


# In[ ]:


print(X_test.shape)
y_pred=reg.predict(X_test)

print('Predictions on the duration of flights: /n RMSE ={}, MSE={}, R2= {}, RSE={} \n mean absolute error : {}'.format(np.sqrt(mean_squared_error(y_pred, yte['time_f'])), 
                                                mean_squared_error(y_pred, yte['time_f']),
      r2_score(y_pred, yte['time_f']),
      (1-r2_score(y_pred, yte['time_f'])), mean_absolute_error(y_pred, yte['time_f'])))


# In[ ]:


tests = pd.DataFrame({'prediction': y_pred, 'time_noted' :list(yte['time_f'])})
sns.jointplot(x='prediction',y='time_noted', data=tests, kind='reg', scatter_kws = {'alpha':0.2,'s':0.8 })


# ## After subtraction of the announced flight time we obtain the prediction of the delays:

# In[ ]:


xte_crs_time = X_test_num[:,3]#xte.todense()[:,3]
#xte_crs_time = xte[:,3]
y_pred_delay = y_pred-xte_crs_time.flatten()


# In[ ]:


print('Pour les retards : /n RMSE ={}, MSE={}, R2= {}, RSE={} \n mean absolute error : {}'.format(
    np.sqrt(mean_squared_error(y_pred_delay, list(yte['ARRIVAL_DELAY']))), 
                                                mean_squared_error(y_pred_delay, list(yte['ARRIVAL_DELAY'])),
      r2_score(y_pred_delay, list(yte['ARRIVAL_DELAY'])),
      (1-r2_score(y_pred_delay, list(yte['ARRIVAL_DELAY']))), mean_absolute_error(y_pred_delay, list(yte['ARRIVAL_DELAY']))))


# In[ ]:


print(reg.coef_.shape[0], X_test.shape)
plt.plot(range(reg.coef_.shape[0]),reg.coef_)
plt.title('value of the beta coefficients')


# In[ ]:


#print(list(COL_NUM)[:-1])
COL_COEF = list(COL_NUM)+list(COL_CAT)
COL_CAT[610:690]
d_coef = pd.DataFrame(reg.coef_, index=COL_COEF, columns=['coef'])
d_coef.sort_values(by='coef', ascending=False)


# In[ ]:


tests = pd.DataFrame({'Delay prediction': y_pred_delay, 'delay_noted' :list(yte['ARRIVAL_DELAY'])})
sns.jointplot(x='Delay prediction',y='delay_noted', data=tests, kind='reg', scatter_kws = {'alpha':0.2,'s':0.8 })


# To be continued...

# In[ ]:





# In[ ]:




