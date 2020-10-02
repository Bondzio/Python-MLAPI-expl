#!/usr/bin/env python
# coding: utf-8

# ## 1.Importing libraries 

# In[ ]:


import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 
sns.set_style('dark')
import datetime

import plotly.express as px
import plotly.graph_objects as go
import re
import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
from wordcloud import WordCloud
from PIL import Image

import warnings
warnings.filterwarnings('ignore')


# 
# ## 2.Loading dataset

# In[ ]:


data = pd.read_csv('/kaggle/input/startup-investments-crunchbase/investments_VC.csv',encoding = 'unicode_escape')


# In[ ]:


data.head()


# ## 3. Data engineering 

# ### 3.1 Missing value

# In[ ]:


data.isna().sum().sum()


# Tooooooooo many missing value.Drop out all missing values 

# In[ ]:


data=data.dropna()
# drop 
data=data.reset_index()
# reset index


# ### 3.2 Duplication

# In[ ]:


sum(data.duplicated())


# No duplicated data

# ### 3.3 Selecting columns 
# 
# Because I'll not use all columns I'm going to make a new columns which I'll use for exploratory data analysis  

# In[ ]:


data.columns


# In[ ]:


# selected columns which will be used for EDA

data = pd.DataFrame(data,columns=['category_list',' funding_total_usd ',' market ',
                                  'status','country_code','state_code','city','founded_at','first_funding_at'])


# ### 3.4  Change column name

# In[ ]:


data.rename(columns={' market ':'market',' funding_total_usd ':'funding_total_usd','category_list':'category'},inplace=True)


# ## 4. Data Visualization

# ### 4.1 Market

# In[ ]:


market_Top20=data.market.value_counts()[:20]
market_Top20 =pd.DataFrame(market_Top20,columns=['market'])
market_Top20.rename(columns={'market':'counting'},inplace=True)
market_Top20=market_Top20.reset_index()


# In[ ]:


fig = px.bar(market_Top20, x='index',y='counting',color='counting',
             labels={'pop':'state code counting'}, height=700,title='market field counting')
fig.show();


# > `Software` >>>>>>>>>>>>> `Biotechnology` >> `mobile`>> .....

# In[ ]:


from wordcloud import WordCloud
fig, ax= plt.subplots( figsize=[15, 10])
wordcloud1 = WordCloud( background_color='white',
                        width=1500,
                        height=800).generate(" ".join(data['market']))
ax.imshow(wordcloud1)
ax.axis('off')
ax.set_title('Start-up market keyword',fontsize=40);


# ### 4.2 cateogory

# In[ ]:


category_Top20 =pd.DataFrame(data.category.value_counts()[:20],columns=['category'])
#category_Top20['index'] = category_Top20['index'].iloc[1:-1]
category_Top20.rename(columns={'category':'counting'},inplace=True)
category_Top20.reset_index(inplace=True)


# In[ ]:


def find_punct(text):
    text = re.sub(r'[!"\$%\'()*,\-.\/:;=#@?\[\\\]^_`{|}~]*','', (text))
    return text

category_Top20['index'] = category_Top20['index'].apply(lambda x : find_punct(x))


# In[ ]:


fig = px.bar(category_Top20, x='index',y='counting',color='counting',
             labels={'pop':'category counting'}, height=700,title='category counting')
fig.show()


# In[ ]:


fig, ax= plt.subplots( figsize=[15, 10])
wordcloud1 = WordCloud( background_color='white',
                        width=1500,
                        height=800).generate(" ".join(data['category']))
ax.imshow(wordcloud1)
ax.axis('off')
ax.set_title('Start-up category keywords',fontsize=40);


# ### 4.3 funding total usdollar

# In[ ]:


# remove comma
data['funding_total_usd'] = data['funding_total_usd'].apply(lambda x : find_punct(x))


# In[ ]:


# fill the empty black with NaN
data['funding_total_usd'] = data['funding_total_usd'].replace('    ',np.nan, regex=True)


# In[ ]:


# change the datatype, but only non null value
data['funding_total_usd']=data[~ data['funding_total_usd'].isna()==True]['funding_total_usd'].astype(int)


# In[ ]:


# Build a new dataFrame
funding  = pd.DataFrame(data['funding_total_usd'],columns=['funding_total_usd'])
funding.dropna(inplace=True)

# change the datype
funding=funding.astype(int)


# In[ ]:


# check the statistical insights for setting the range 
print('Average funding amount of startup is: ',int(funding.mean()))
print('Maximum funding amount of startup is: ',funding.max())
print('Minimum funding amount of startup is: ',funding.min())


# In[ ]:


# Range setting for funding level 

funding['funding_level'] = 0
funding.loc[funding['funding_total_usd']<10000,'funding_level'] =1
funding.loc[ (funding['funding_total_usd']>=10000) & (funding['funding_total_usd']<100000),'funding_level' ] =2
funding.loc[ (funding['funding_total_usd']>=100000) & (funding['funding_total_usd']<1000000),'funding_level'] =3
funding.loc[(funding['funding_total_usd']>=1000000) & (funding['funding_total_usd']<10000000) ,'funding_level'] =4
funding.loc[funding['funding_total_usd']>=10000000,'funding_level'] =5


# In[ ]:


funding['funding_level'].value_counts()


# In[ ]:


from plotly import graph_objects as go
fig = go.Figure(go.Funnelarea(
    text = ["Funding level 4","Funding level 5", "Funding level 3", "Fundig level 2", "Funding level 1"],
    values = [7305,5843,4392,1447,125],
    # value count of each funding level
    title = 'funding level ratio'
    ))
fig.show()


# - Funding level 1: US Dollar < **10,000**
# - Funding level 2: **10,000** <= US Dollar <**100,000**
# - Funding level 3: **100,000**<= US Dollar <**1,000,000**
# - Funding level 4: **1,000,000** <= US Dollar < **10,000,000**
# - Funding level 5: US Dollar > **100,000,000** 
# 

# ### 4.4 status 

# In[ ]:


df = pd.DataFrame(data.status.value_counts(),columns=['status'])
df.reset_index(inplace=True)

fig = px.pie(df, values='status', names='index', color_discrete_sequence=px.colors.sequential.RdBu,title='status ratio',)
fig.show()


# ### 4.5 State Code 

# In[ ]:


state_top20 = pd.DataFrame(data.state_code.value_counts()[:20],columns=['state_code'])
state_top20.reset_index(inplace=True)


# In[ ]:


fig = px.bar(state_top20, x='index', y='state_code',color='state_code',
             labels={'pop':'state code counting'}, height=500,title='Top 20 state')
fig.show()


# In[ ]:


fig, ax= plt.subplots( figsize=[15, 10])
wordcloud1 = WordCloud( background_color='white',
                        width=1500,
                        height=800).generate(" ".join(data['state_code']))
ax.imshow(wordcloud1)
ax.axis('off')
ax.set_title('Start-up state keywords',fontsize=40);


# In[ ]:


USA_top20 = pd.DataFrame(data.query('country_code == "USA"')['state_code'].value_counts()[:20],columns=['state_code'])
USA_top20.reset_index(inplace=True)

fig = px.bar(USA_top20, x='index', y='state_code',color='state_code',
             labels={'pop':'state code counting'}, height=500,title='US Top 20 state')
fig.show()


# In[ ]:


fig, ax= plt.subplots( figsize=[15, 10])
wordcloud1 = WordCloud( background_color='white',
                        width=1500,
                        height=800).generate(" ".join(data.query('country_code == "USA"')['state_code']))
ax.imshow(wordcloud1)
ax.axis('off')
ax.set_title('USA Start-up state keywords',fontsize=40);


# In[ ]:


CAN_top9 = pd.DataFrame(data.query('country_code == "CAN"')['state_code'].value_counts()[:20],columns=['state_code'])
CAN_top9.reset_index(inplace=True)

fig = px.bar(CAN_top9, x='index', y='state_code',color='state_code',
             labels={'pop':'state code counting'}, height=500,title='Canada Top 9 state')
fig.show()


# In[ ]:


fig, ax= plt.subplots( figsize=[15, 10])
wordcloud1 = WordCloud( background_color='white',
                        width=1500,
                        height=800).generate(" ".join(data.query('country_code == "CAN"')['state_code']))
ax.imshow(wordcloud1)
ax.axis('off')
ax.set_title('Canada Start-up state keywords',fontsize=40);


# ### Additional : Mapping state 

# In[ ]:


USA = pd.DataFrame(data.query('country_code == "USA"')['state_code'].value_counts(),columns=['state_code'])
USA.reset_index(inplace=True)


# In[ ]:


fig = go.Figure(data=go.Choropleth(
    locations=USA['index'],
    z = USA['state_code'].astype(int), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "start-up counting",
))

fig.update_layout(
    title_text = 'Start up investment USA state counting',
    geo_scope='usa',
)
fig.show()


# ### 4.6 Country

# In[ ]:


df = pd.DataFrame(data.country_code.value_counts(),columns=['country_code'])
df.reset_index(inplace=True)

fig = px.pie(df, values='country_code', names='index', color_discrete_sequence=px.colors.sequential.Sunset,title='Country code ratio',)
fig.show()


# ### 4.7 city
# 
# 

# In[ ]:


city =pd.DataFrame(data.city.value_counts()[:30],columns=['city'])
city.reset_index(inplace=True)


# In[ ]:


fig = px.treemap(city, path=['index'], values='city',title='Top 30 start-up city')
fig.show()


# ### 4.8  Time difference between Foundation and first funding 
# 
# - I want to know how much time did they wait for funding after foundation of their company 
# 
# - Also I want to know how many company couldn't survive before they get a first funding so that I can figure out the important of funding for start up

# In[ ]:


# change the datatype from string to datetime 
data['first_funding_at'] = pd.to_datetime(data['first_funding_at'],errors='coerce')
data['founded_at'] = pd.to_datetime(data['founded_at'],errors='coerce')


# In[ ]:


# drop Null value
data['founded_at'].dropna(inplace=True)
data['first_funding_at'].dropna(inplace=True)


# In[ ]:


# Define the differrence between the date of foundation and first funding
data['difference'] = data['first_funding_at'] - data['founded_at']
# extract only numeric value
data['difference'] = data['difference'].dt.days


# In[ ]:


data.head()


# In[ ]:


# number of neagive days = Start up got investment before the found the company 
print("There are [{}] records where the duration till first investment is larger than Zero.".format(data[data.difference > 0].shape[0]))
print("There are [{}] records where the duration till first investment is equal Zero.".format(data[data.difference == 0].shape[0]))
print("There are [{}] records where the duration till first investment is less than Zero.".format(data[data.difference < 0].shape[0]))


# In[ ]:


fig = go.Figure(go.Funnelarea(
    text = ["Positive Duration ","Negative Duration","Zero"],
    values = [19477,1309,1053],
    title = 'Duration between foundation of company and first funding'
    ))
fig.show()


# In[ ]:


# Range setting for funding level 

positive = data[data['difference']>0]

positive['difference_level'] = 0
positive.loc[positive['difference']<365,'difference_level'] ='under 1year'
positive.loc[ (positive['difference']>=365) & (positive['difference']<1095),'difference_level' ] ='1-3years'
positive.loc[ (positive['difference']>=1095) & (positive['difference']<1825),'difference_level'] ='3-5years'
positive.loc[(positive['difference']>=1825) & (positive['difference']<3650) ,'difference_level'] ='5-10years'
positive.loc[(positive['difference']>=3650) & (positive['difference']<7300) ,'difference_level'] ='10-20years'
positive.loc[positive['difference']>=7300,'difference_level'] ='over 20years'


# In[ ]:


positive['difference_level'].value_counts().iplot(kind='bar',
                                                      yTitle='counting', 
                                                      linecolor='black', 
                                                      opacity=0.7,
                                                      color='blue',
                                                      theme='pearl',
                                                      bargap=0.5,
                                                      gridcolor='white',
                                                      title='Difference level counting')


# ### 4.9 foundation date of start-up

# In[ ]:


foundation = pd.DataFrame(data['founded_at'])


# In[ ]:


foundation['year'] = foundation['founded_at'].dt.year
foundation['month'] = foundation['founded_at'].dt.month


# In[ ]:


foundation['year'].value_counts().iplot(kind='bar',
                                                      yTitle='counting', 
                                                      linecolor='black', 
                                                      opacity=0.7,
                                                      color='purple',
                                                      theme='pearl',
                                                      bargap=0.5,
                                                      gridcolor='white',
                                                      title='Year of foundation')


# In[ ]:


foundation['month'].value_counts().iplot(kind='bar',
                                                      yTitle='counting', 
                                                      linecolor='black', 
                                                      opacity=0.7,
                                                      color='purple',
                                                      theme='pearl',
                                                      bargap=0.5,
                                                      gridcolor='white',
                                                      title='Month of foundation',
                                                      )


# ### 4.10 First funding date

# In[ ]:


first_funding = pd.DataFrame(data['first_funding_at'])

first_funding['year'] = first_funding['first_funding_at'].dt.year
first_funding['month'] = first_funding['first_funding_at'].dt.month


# In[ ]:


first_funding['year'].value_counts().iplot(kind='bar',
                                                      yTitle='counting', 
                                                      linecolor='black', 
                                                      opacity=0.7,
                                                      color='gray',
                                                      theme='pearl',
                                                      bargap=0.5,
                                                      gridcolor='white',
                                                      title='Year of first funding')


# In[ ]:


first_funding['month'].value_counts().iplot(kind='bar',
                                                      yTitle='counting', 
                                                      linecolor='black', 
                                                      opacity=0.7,
                                                      color='gray',
                                                      theme='pearl',
                                                      bargap=0.5,
                                                      gridcolor='white',
                                                      title='Month of first funding')


# If you have any feedback of this kernel, just let me know. I'm totally open for that
# 
# <h3>Thank you all very much <h3>
