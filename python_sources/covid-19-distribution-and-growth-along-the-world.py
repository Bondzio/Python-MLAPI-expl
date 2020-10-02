#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
import seaborn as sns


# # Importing data
# this data base includes archived_data and csse_covid_19_data folder. As we can see in folder description, the csse_covid_19_data has been updated daily until now. So we use this folder data.

# In[ ]:


confirmed_cases = pd.read_csv('/kaggle/input/covid19-01222020-to-02272020/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')

deaths_cases = pd.read_csv('/kaggle/input/covid19-01222020-to-02272020/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')

recovered_cases = pd.read_csv('/kaggle/input/covid19-01222020-to-02272020/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')


# # exploring data
# from the last step the confirmed_cases and deaths_cases and recovered_cases are Pandas dataframes with similar structure. It can be seen in the below format:
# 

# In[ ]:


confirmed_cases.head()


# we can also get some information about these dataframes with following method. Up to now the number of countries which seen coronavirus is 105 and we can see timeseries data (confirmed/deaths/recovered cases) with lenght 37 in each country. The following method print some info about confirmed cases.

# In[ ]:


confirmed_cases.info()


# In the next step, group cases by Country/Region column.

# In[ ]:


confirmed_by_country = confirmed_cases.groupby('Country/Region')
deaths_by_country = deaths_cases.groupby('Country/Region')
recovered_by_country = recovered_cases.groupby('Country/Region')


# The following code find the total number of (confirmed/deaths/recovered) cases in each group(country)
# I also renamed some indexes of dataframes because of making them compatible with another csv file containing Three_Letter_Country_Code which I need to use them for rendering world map.

# In[ ]:



aggr_confirmed_country = confirmed_by_country.apply(lambda df:df.iloc[:,4:].sum()).iloc[:,-1]
aggr_deaths_country = deaths_by_country.apply(lambda df:df.iloc[:,4:].sum()).iloc[:,-1]
aggr_recovered_country = recovered_by_country.apply(lambda df:df.iloc[:,4:].sum()).iloc[:,-1]

aggr_confirmed_country = aggr_confirmed_country.rename(index = 
                                 {'Mainland China':'China','North Macedonia':'Macedonia',
                                  'South Korea':'Korea, Republic of','UK':'United Kingdom',
                                  'Macau':'Maca','US':'United States of America'})

aggr_deaths_country = aggr_deaths_country.rename(index = 
                                 {'Mainland China':'China','North Macedonia':'Macedonia',
                                  'South Korea':'Korea, Republic of','UK':'United Kingdom',
                                  'Macau':'Maca','US':'United States of America'})

aggr_recovered_country = aggr_recovered_country.rename(index = 
                                 {'Mainland China':'China','North Macedonia':'Macedonia',
                                  'South Korea':'Korea, Republic of','UK':'United Kingdom',
                                  'Macau':'Maca','US':'United States of America'})


# country_info is contain some information about countries which I want for render world map.
# 

# In[ ]:


from io import StringIO
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
url = 'https://pkgstore.datahub.io/JohnSnowLabs/country-and-continent-codes-list/country-and-continent-codes-list-csv_csv/data/b7876b7f496677669644f3d1069d3121/country-and-continent-codes-list-csv_csv.csv'
s=requests.get(url, headers= headers).text
country_info = pd.read_csv(StringIO(s))

def get_tree_letter_code(s):
    country = country_info[country_info['Country_Name'].str.contains(s)]
    if country.empty:
        return ''
    else:
        return country['Three_Letter_Country_Code'].values[0]


# Now all the data is provided to make a dataframe consist of countries, number of confirmed/deaths/recovered cases and Three_Letter_Country_Code

# In[ ]:



aggr_country_df = pd.DataFrame()
aggr_country_df['country'] = aggr_confirmed_country.index
aggr_country_df['confirmed'] = aggr_confirmed_country.values
aggr_country_df['deaths'] = aggr_deaths_country.values
aggr_country_df['recovered'] = aggr_recovered_country.values
aggr_country_df['Three_Letter_Country_Code'] = aggr_country_df['country'].apply(get_tree_letter_code)
aggr_country_df.head()


# The following method is defined to get the zindex(the attribute based on this each country assinged a color) and color scale and title and color title and draw world map plot.

# In[ ]:


def draw_world_map(zindex,cscale,title,color_title):
    fig = go.Figure(data=go.Choropleth(
        locations = aggr_country_df['Three_Letter_Country_Code'],
        z = zindex,
        text = aggr_country_df['country'],
        colorscale = cscale,
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = color_title,
    ))

    fig.update_layout(
        title_text=title,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    fig.show()


# In the next call draw_world_map for confirmed cases, as we can see in the below plot because the number of confirmed cases in china is about 1.5M people and too far with other countries, this plot is not informative.

# In[ ]:


draw_world_map(aggr_country_df['confirmed'],'Reds','Confirmed covid19','number of confirmed')


# so I add a log-confirmed column to this dataframe to eliminate the large numbers.
# also we want to see the number of deaths/recovered ratio based on the confirmed case, so I add deaths-ratio and recovered-ratio column to this dataframe.

# In[ ]:



aggr_country_df['log-confirmed'] = np.log(aggr_country_df['confirmed']+ 1e-7 )
aggr_country_df['deaths-ratio'] = aggr_country_df['deaths']/aggr_country_df['confirmed']
aggr_country_df['recovered-ratio'] = aggr_country_df['recovered']/aggr_country_df['confirmed']
aggr_country_df.head()


# Now we can call the draw_world_map with log-confirmed data and we can see the distribution of confirmed cases along the world map.

# In[ ]:


draw_world_map(aggr_country_df['log-confirmed'],'Blues','logarithmic distribution of confirmed cases','log of num of confirmed')


# The below figure illustrate deaths ratio based on confirmed cases in each country.

# In[ ]:


draw_world_map(aggr_country_df['deaths-ratio'],'Reds','distribution of deaths-ratio cases','ratio')


# The below figure illustrate recovered ratio based on confirmed cases in each country.

# In[ ]:


draw_world_map(aggr_country_df['recovered-ratio'],'Greens',' distribution of recovered-ratio cases','ration')


# Up to now, I illustrate the aggregate data based on each country.
# Now I want to illustrate and analyis the changes through the time.

# In[ ]:



time_series_confirmed = confirmed_by_country.apply(lambda df:df.iloc[:,4:].sum())
time_series_deaths = deaths_by_country.apply(lambda df:df.iloc[:,4:].sum())
time_series_recovered = recovered_by_country.apply(lambda df:df.iloc[:,4:].sum())

time_series_deaths_ratio = time_series_deaths.divide((time_series_confirmed + 1e-10))
time_series_recovered_ratio = time_series_recovered.divide((time_series_confirmed + 1e-10))


# The following method get country name and illustrate the changes of (confirmed/deaths/recovered) case through the time

# In[ ]:



def draw_growth_plot(country):
    
    test_df = pd.DataFrame()
    t1 = np.trim_zeros(time_series_confirmed.loc[country].values)
    t2 = time_series_deaths.loc[country].values[-t1.shape[0]:]
    t3 = time_series_recovered.loc[country].values[-t1.shape[0]:]

    test_df['day'] = range(len(t1))
    test_df['conf'] = t1
    test_df['death'] =t2
    test_df['rec'] = t3

    test_df = pd.melt(test_df, id_vars=['day'],value_vars=['conf', 'death','rec'])
    test_df
    fig, ax1 = plt.subplots(figsize=(10, 10))
    sns.barplot(x='day', y='value', hue='variable', data=test_df,ax = ax1)


# For exmaple from the deaths ratio world map we can see Iran has a larger ratio than other countries.
# Also I depict Mainland China and South Korea for other examples.

# In[ ]:


draw_growth_plot('Iran')


# In[ ]:


draw_growth_plot('Mainland China')


# In[ ]:



draw_growth_plot('South Korea')


# In[ ]:


draw_growth_plot('US')


# In the below code I want to illustrate heat map of correlations among confirmed growth of all the participant countries.

# In[ ]:


cmap = sns.diverging_palette(220, 10, as_cmap=True)
fig, ax = plt.subplots(figsize=(10,10)) 
sns.heatmap(time_series_confirmed.transpose().corr(),cmap = cmap,linewidths=.5,vmax=1,ax=ax)


# In the below code I want to illustrate heat map of correlations among deaths growth of all the participant countries.

# In[ ]:


cmap = sns.diverging_palette(220, 10, as_cmap=True)
fig, ax = plt.subplots(figsize=(10,10)) 
sns.heatmap(time_series_deaths_ratio.transpose().corr(),cmap = cmap,linewidths=.5,ax=ax)


# In the below code I want to illustrate heat map of correlations among deaths growth of all the participant countries.

# In[ ]:


cmap = sns.diverging_palette(220, 10, as_cmap=True)
fig, ax = plt.subplots(figsize=(10,10)) 
sns.heatmap(time_series_recovered_ratio.transpose().corr(),cmap = cmap,linewidths=.5,ax=ax)


# The below method get a timeseries and a lower_bound_treshold and title, to add all counties growth in one plot which satisfy the bound limitation.

# In[ ]:


# time_series_confirmed 

def draw_comparison_growth(arr,lower_bound_treshold,title):
    temp = arr.transpose()
    temp = temp.set_index([pd.Index([i for i in range(len(temp.index))])])
    plt.figure(figsize=(10,10))
    aggr_count = temp.iloc[-1,:]
    for cnt in temp.columns:
        if cnt == 'Mainland China' or cnt =='Others' or aggr_count[cnt] < lower_bound_treshold :
            pass
        else:
            plt.plot(temp[cnt])
    plt.legend()
    plt.title(title)
    
draw_comparison_growth(time_series_confirmed,50,'Growth of confirmed cases which at least has 400 confirmed case')


# In[ ]:


draw_comparison_growth(time_series_deaths,5,'Growth of death cases which at least has 5 death case') 


# In[ ]:


# time_series_recovered
draw_comparison_growth(time_series_recovered,5,'Growth of recovered cases which at least has 5 recovered case') 

