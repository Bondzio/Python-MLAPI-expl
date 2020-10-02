#!/usr/bin/env python
# coding: utf-8

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
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from pathlib import Path
import plotly.offline as py
import plotly.express as px
import cufflinks as cf


# In[ ]:


py.init_notebook_mode(connected=False)
cf.set_config_file(offline=True)
sns.set()
pd.plotting.register_matplotlib_converters
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


file1 = '/kaggle/input/covid19-in-italy/covid19_italy_province.csv'
file2 = '/kaggle/input/covid19-in-italy/covid19_italy_region.csv'


# In[ ]:


province = pd.read_csv(file1)
region = pd.read_csv(file2)


# In[ ]:


province.head()


# In[ ]:


region.head()


# In[ ]:


#is null?
pv = province.isnull().sum()
pv[pv>0]


# In[ ]:


it_prov = province.dropna()


# In[ ]:


it_prov.isnull().any()


# In[ ]:


#information 
it_prov.info()


# In[ ]:


#we take only the interest feature
data_province = it_prov[['Date', 'ProvinceName', 'Latitude', 'Longitude', 'TotalPositiveCases']].copy()


# In[ ]:


data_province['Date'] = pd.to_datetime(data_province['Date'])
data_province['Date'] = data_province['Date'].dt.strftime('%m/%d/%Y')
data_province.head() #ok


# In[ ]:


region['Date'] = pd.to_datetime(region['Date'], infer_datetime_format=True)
region['Date'] = region['Date'].dt.strftime('%m/%d/%Y')


# In[ ]:


#now for region
region.isnull().sum()[region.isnull().sum()>0]


# In[ ]:


# information
region.info()


# In[ ]:


#we remove the feature not necessary
data_region = region.drop(['SNo', 'Country', 'RegionCode'], axis=1)


# In[ ]:


data_region.head()


# # Some Statistics and Visualization

# ## Province

# In[ ]:


start_date = data_province.Date.min()
end_date = data_province.Date.max()


# In[ ]:


daily_info_province = data_province[data_province.Date == end_date].sort_values(by='TotalPositiveCases',                                                                                ascending=False)
daily_info_province.style.background_gradient(cmap='Pastel1_r')


# In[ ]:


print('========Province Information on COVID-19 ======================')
print('========= Report at date {} ==================\n'.format(end_date))
print('Number of province are touched: {}'.format(len(daily_info_province.ProvinceName.unique())))
print('Number of people are positive case: {}'.format(daily_info_province.TotalPositiveCases.sum()))
print('Province most affected: {}'.format((daily_info_province.iloc[0, 1], daily_info_province.iloc[0, 4])))
print('Province less affected: {}'.format((daily_info_province.iloc[105, 1], daily_info_province.iloc[105, 4])))
print('================================================================')


# In[ ]:


#plotting
daily_province = daily_info_province.set_index('ProvinceName')
daily_province['TotalPositiveCases'].iplot(kind='bar', title='Italy affected by COVID-19',                                           yTitle='Total Positive cases', colors='blue', lon='Longitude', 
                                          lat='Latitude')


# In[ ]:


case = data_province.groupby('Date')['TotalPositiveCases'].agg('sum')


# In[ ]:


case.iplot(kind='bar', title = 'Total Positive cases  evolution in Italy', yTitle='Total Positive cases')


# In[ ]:


overTime_case = data_province.groupby(['Date', 'ProvinceName'])['TotalPositiveCases'].agg('sum')


# In[ ]:


fig = px.bar(daily_info_province, 
             x="ProvinceName", 
             y="TotalPositiveCases",
             color='TotalPositiveCases',
             hover_name="ProvinceName",
             animation_frame= 'Date',
             title='Global COVID-19 Infections over time')
fig.update(layout_coloraxis_showscale=False)
fig.show()


# ## latitude & longitude density 

# In[ ]:


#latitude & longitude
sns.jointplot(x='Longitude', y='Latitude', data=data_province, kind='kde', annot_kws=dict(stat="r") )
plt.title('Covid19 province density')


# ## spread of Covid19 over space and time

# In[ ]:


center_point = dict(lon=9, lat=46)
figx = px.density_mapbox(data_province, lat='Latitude', lon='Longitude', z="TotalPositiveCases",
                        center = center_point, hover_name='ProvinceName', zoom = 5,
                         range_color= [10, 20] , radius=10,
                        mapbox_style= 'open-street-map', title='Novel Covid19 in Italy',
                        animation_frame='Date')
figx.update(layout_coloraxis_showscale=False)
figx.show()


# In[ ]:


size = data_province.TotalPositiveCases.pow(0.4)
figy = px.scatter(data_province, x='Latitude', y='Longitude',
                  color="TotalPositiveCases", 
                        hover_name='ProvinceName', size=size,
                         title='Novel Covid19 move across Italy',
                        animation_frame='Date')
figy.update(layout_coloraxis_showscale=False)
figy.show()


# ## Why covid19 like to move along a latitude not longitude? there is causing by the displacement of population or another?
# 
# we need to see that

# **Latitude vs Longitude**

# In[ ]:


figs = px.scatter_3d(data_province, x='Longitude', y='Latitude', z='TotalPositiveCases',
                 hover_name='ProvinceName', 
                    size= size, opacity=0.7,
                     animation_frame='Date', color='TotalPositiveCases')
figs.update(layout_coloraxis_showscale=False)
figs.show()


# **Something is not normal. please, look for the behaviour between Lodi and bergamo**

# ## Region

# In[ ]:


# feature statistics
need_feature = list(set(data_region.columns) - set(['Latitude', 'Longitude','Date', 'RegionName']))
dneed = list(set(data_region.columns) - set(['Latitude', 'Longitude', 'RegionName'])) 
data_region[dneed].describe()


# **Correlation**

# In[ ]:


data_region[need_feature].corr()


# source: https://gist.github.com/fabianp/9396204419c7b638d38f

# In[ ]:


from scipy import stats, linalg

def partial_corr(C):
    """
    Returns the sample linear partial correlation coefficients between pairs of variables in C, controlling 
    for the remaining variables in C.
    Parameters
    ----------
    C : array-like, shape (n, p)
        Array with the different variables. Each column of C is taken as a variable
    Returns
    -------
    P : array-like, shape (p, p)
        P[i, j] contains the partial correlation of C[:, i] and C[:, j] controlling
        for the remaining variables in C.
    """

    C = np.asarray(C)
    p = C.shape[1]
    P_corr = np.zeros((p, p), dtype=np.float)
    for i in range(p):
        P_corr[i, i] = 1
        for j in range(i+1, p):
            idx = np.ones(p, dtype=np.bool)
            idx[i] = False
            idx[j] = False
            beta_i = linalg.lstsq(C[:, idx], C[:, j])[0]
            beta_j = linalg.lstsq(C[:, idx], C[:, i])[0]

            res_j = C[:, j] - C[:, idx].dot( beta_i)
            res_i = C[:, i] - C[:, idx].dot(beta_j)

            corr = stats.pearsonr(res_i, res_j)[0]
            P_corr[i, j] = corr
            P_corr[j, i] = corr

    return P_corr


# **Partial Correlation**

# In[ ]:


pcoray = data_region[need_feature].values 
corrpartial = pd.DataFrame(partial_corr(pcoray), columns=need_feature, index=need_feature)
corrpartial.head(15)


# In[ ]:


# I take only TotalPositiveCases to see the correlation with all other feature
data_region[need_feature].corr().loc[:,'TotalPositiveCases']


# TotalPositiveCases are most correlated with all other feature. So, we can use only this feature to know the behavior of disease. 

# In[ ]:


daily_info_region = data_region[data_region.Date.isin([end_date])].sort_values(by='TotalPositiveCases',                                                                                ascending=False)
daily_region = daily_info_region.set_index('RegionName')


# In[ ]:


daily_region['TotalPositiveCases'].iplot(kind='bar', title='Italy affected by COVID-19',                                           yTitle='Total Positive cases', colors='blue', lon='Longitude', 
                                          lat='Latitude')


# In[ ]:


#latitude & longitude
sns.jointplot(x='Longitude', y='Latitude', data=data_region, kind='kde', annot_kws=dict(stat="r") )
plt.title('Covid19 region density ')


# In[ ]:


center_point = dict(lon=9, lat=46)
figi = px.density_mapbox(data_region, lat='Latitude', lon='Longitude', z="TotalPositiveCases",
                        center = center_point, hover_name='RegionName', zoom = 5,
                         range_color= [10, 20] , radius=10,
                        mapbox_style= 'open-street-map', title='Novel Covid19 region in Italy',
                        animation_frame='Date')
figi.update(layout_coloraxis_showscale=False)
figi.show()


# In[ ]:


siz = data_region.TotalPositiveCases.pow(0.4)
fige = px.scatter(data_region, x='Latitude', y='Longitude',
                  color="TotalPositiveCases", 
                        hover_name='RegionName', size=siz,
                         title='Novel Covid19 move across Italy',
                        animation_frame='Date')
fige.update(layout_coloraxis_showscale=False)
fige.show()


# please, see the line between piemonte region to Basilicata. 
# 
# i have the impression that each region transmits the virus to another region starting with the lombardia region. then follows other regions like Emilla, Veneto and Piemeto. And that piemeto then transmits the virus to liguria until basilicata forming a curvature. 

# In[ ]:


figo = px.scatter_3d(data_region, x='Longitude', y='Latitude', z='TotalPositiveCases',
                 hover_name='RegionName', 
                    size= siz, opacity=0.7,
                     animation_frame='Date', color='TotalPositiveCases')
figo.update(layout_coloraxis_showscale=False)
figo.show()


# # Which region or province are similar?

# **Which region are similar for Total positive cases?**

# In[ ]:


X = data_region[data_region.Date.isin([end_date])] 
cols = list(set(X.columns) - set(['Date']))
X_sim = X[cols]
Xsim = X_sim.set_index('RegionName')


# In[ ]:


print('============ Today: {}; which Region are Similar? ================='.format(end_date))
Xsim.style.background_gradient('viridis')


# In[ ]:


import plotly.figure_factory as reg
ff = reg.create_dendrogram(Xsim, orientation='left', labels=Xsim.index)
ff.update_layout(width=800, height=800)
ff.show()


# # Correlation and Partial correlation between feature over time

# source: https://raphaelvallat.com/correlation.html
# 
# source: https://en.wikipedia.org/wiki/Partial_correlation
# 
# source: https://stats.stackexchange.com/questions/288273/partial-correlation-in-panda-dataframe-python/298754

# **Correlation**

# In[ ]:


xp = data_region[need_feature].corr()
mask_ut=np.triu(np.ones(xp.shape)).astype(np.bool)
sns.heatmap(xp, mask=mask_ut, cmap= 'viridis')
plt.title('Correlation of all features')


# The correlation tell us that all feature are more correlated but we verify very well if there is true using partial correlation

# **Partial correlation**
# 
# In probability theory and statistics, partial correlation measures the degree of association between two random variables, with the effect of a set of controlling random variables removed. If we are interested in finding to what extent there is a numerical relationship between two variables of interest, using their correlation coefficient will give misleading results if there is another, confounding, variable that is numerically related to both variables of interest. This misleading information can be avoided by controlling for the confounding variable, which is done by computing the partial correlation coefficient. This is precisely the motivation for including other right-side variables in a multiple regression; but while multiple regression gives unbiased results for the effect size, it does not give a numerical value of a measure of the strength of the relationship between the two variables of interest.
# 
# For example, if we have economic data on the consumption, income, and wealth of various individuals and we wish to see if there is a relationship between consumption and income, failing to control for wealth when computing a correlation coefficient between consumption and income would give a misleading result, since income might be numerically related to wealth which in turn might be numerically related to consumption; a measured correlation between consumption and income might actually be contaminated by these other correlations. The use of a partial correlation avoids this problem.
# 
# Extract from: https://en.wikipedia.org/wiki/Partial_correlation

# In[ ]:


# Feature selection with high partial correlated features 
# Select upper triangle of correlation matrix
upper = corrpartial.where(np.triu(np.ones(corrpartial.shape),k=1).astype(np.bool))
# Find index of feature columns with partial correlation greater than 0.65
high_columns = [column for column in upper.columns if any(abs(upper[column]) > 0.65)]
high_cp = corrpartial[high_columns]    #.drop(index=0, columns=to_drop)
to_drop = list(set(upper.columns) - set(high_columns)) 

print("====================   Feature with High Partial Correlation   ==============================")
high_cp=  high_cp.drop(index=to_drop)
high_cp.style.background_gradient('viridis')


# **We are plotting only the feature that are most partial correlated** 

# In[ ]:


need_feature


# In[ ]:


plane = data_region[high_columns].copy()
plane.head(2)


# In[ ]:


sns.pairplot(plane)


# # Latitude: space-time spread of COVID-19 Italy

# In[ ]:


#groupby 
la_lon = data_region.groupby(['Latitude','Longitude','Date','RegionName'])[need_feature].agg('sum')
laon = la_lon.reset_index()
laon.head()


# In[ ]:


ch = laon.RegionName.unique()
ch


# In[ ]:



space_time = px.line(laon,x='Latitude', y='TotalPositiveCases',animation_frame='Date', hover_name='RegionName',
                    range_y=[0, 35000])

space_time.update(layout_coloraxis_showscale=False) 
space_time.show()


# This is a spread of COVID-19 space-time along a Latitude. Lombardia is the Source of the spreading of COVID-19. It must be isolated from other cities. 
# 
# This curve are nonlinear spreading

# # Spread to various region over time

# In[ ]:


# we have 21 regions, I divide it to 3 groups where each group have 7 regions to plot it
vorac1 = []
vorac2 = []
vorac3 = []
k = 0
for c in ch:
    k += 1
    voir = laon[laon.RegionName == c].copy()
    
    if k <= 7:
        vorac1.append(voir)
    
    elif not(k <= 7) and k <= 14:
        vorac2.append(voir)
        
    else:
        vorac3.append(voir)
        
    voir = pd.DataFrame()

#voir1= laon[laon.RegionName=='Sicilia']
#voir2 = laon[laon.RegionName=='Calabria']
#voir3 = laon[laon.RegionName=='Sardegna']

lazio = pd.concat(vorac1)
roma = pd.concat(vorac2)
inter = pd.concat(vorac3)


# In[ ]:


print('========== checkpoint ===================')
print('lazio: {}\nroma: {}\ninter: {}'.format(lazio.RegionName.nunique() , roma.RegionName.nunique() , 
                                              inter.RegionName.nunique() ))
print('========== ok ===========================')


# In[ ]:


print('========== checkpoint ===================')
print('lazio: {}\nroma: {}\ninter: {}'.format(lazio.RegionName.unique() , roma.RegionName.unique() , 
                                              inter.RegionName.unique() ))
print('========== ok ===========================')


# In[ ]:


def multiple_plot(data=None, figsize=(20,10), sp = (0.4, 0.2)):
    """ plot many figure
        
        figsize the size of figure
        
        sp the spacing of the figure
        
    """
    a = data['RegionName'].unique()
    
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(hspace= sp[0], wspace=sp[0])
    
    for i, ct in enumerate(a):
        ax = fig.add_subplot(3,3,i+1)
        
        data[data['RegionName'] == ct].plot(x='Date', y='TotalPositiveCases', ax=ax)
        ax.set_xlabel('Date')
        ax.set_ylabel('TotalPositiveCases')
        ax.set_title('nCovid19 evolution in Region = ' + ct)
        
    plt.show() 


# In[ ]:


multiple_plot(data=lazio, figsize=(20,15), sp = (0.4, 0.1))


# In[ ]:


multiple_plot(data = roma, figsize=(20,15), sp = (0.4, 0.1))


# In[ ]:


multiple_plot(data=inter, figsize=(20,15), sp = (0.4, 0.1))


# # Predicting the spread of covid19 ahead time to take preventive mesures

# In[ ]:


def extraction_data(data=None, feature=['RegionName', 'TotalPositiveCases'], region=None, date='Date'):
    """
        - data: the array-like dataframe pandas
        - feature: the feature that we need to use to do prediction one is object and second is numeric
        - region: the region where it is interested to forecast
        - date: the date for fprecast
        
        Returns
            - the raw data for all country. full_data
            - the raw  data for specific region. full_region
    """
    
    
    if len(feature) == 2:
        pass
        
    elif len(feature) == 1:
        pass
    else:
        print('feature must have two entries')
        return -1
    
    if type(date) != str:
        print('date variable must be a string type. Thank!')
        return -1
    
    #if type(region) != str:
     #   print('region variable must be a string type. Thank!')
      #  return -1
    
    #if type(data) == type(pd.DataFrame()):
     #   print('data must be a pandas dataframe type')
      #  return -1
    
    
    if region:
        
        if type(feature[0]) != str or type(feature[1]) != str:
            print('feature must have two entries the same string type. Thank!')
            return -1
    
        country = feature[0] # pandas series correspond to columns country must be a string type 
        umeric = feature[1] #  pandas series correspond to columns country must be a numeric type
    
        extract_data = data[[date, country, umeric]].copy()
        extract_region = extract_data[extract_data[country] == region].copy()
        full_region = extract_region[[date, umeric]].copy()
        
        return full_region # for region
    
    else:
        umeric = feature[0]
        full_data = data[[date, umeric]].copy()
        return full_data # when we  do not use a region
    
    
def preventive_measures(data=None, foryou = None, csp = 0.05 ):
    '''
        foryou: a string name of country/region concerns by a preventive measures
        data: pandas dataframe
        cdp: is the changepoint_prior_scale for prophet
    
    '''
    from fbprophet import Prophet
    from fbprophet.diagnostics import cross_validation
    from fbprophet.diagnostics import performance_metrics
    from fbprophet.plot import plot_cross_validation_metric
    
    if data.shape[1] != 2:
        print('We need a rigth dataframe for making a preventive measure. Give another!')
        return -1
    
    print('================ Preventive Measures ===================')
    print('================ For {} ============================'.format(foryou))
    print('================ The end of nCOVID-19 ==================\n')
    
    cols = data.columns
    dat = data.rename(columns={cols[0]:'ds', cols[1]:'y'})
    
    print('data after renamed')
    print(dat.head(3),'\n')
        
    m = Prophet(interval_width=0.95,changepoint_prior_scale=csp)
    m.fit(dat)
    
    # future days
    futureDays = m.make_future_dataframe(periods=12)
    print('future days')
    print(futureDays.tail(),'\n')
    
    forecast = m.predict(futureDays)
    
    print('forecast data')
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(),'\n')
    
    #we plot graph
    graph = m.plot(forecast)
    plt.title( 'ncovid 19 forecasting for ' + foryou)
    
    graph1 = m.plot_components(forecast)
    plt.title('components forecast for ' + foryou)
    
    if dat.shape[0] > 20:
        #for cross validation we are taking the range of our data 
        df_cv = cross_validation(m, initial='12 days', period='2 days', horizon = '10 days')
        print('cross validation')
        print(df_cv.head(3), '\n')
    
        df_p = performance_metrics(df_cv)
        print('performance metrics')
        print(df_p.head(), '\n')
        
        ufig = plot_cross_validation_metric(df_cv, metric='mape')
    else:
        print('We cannot make a diagnostic for {} because there have small data.'.format(foryou))


# In[ ]:


silic = extraction_data(data=lazio, region='Sicilia')


# In[ ]:


preventive_measures(silic, foryou='Sicilia', csp=1.05)


# In[ ]:


zio = extraction_data(data=roma, region='Lazio')


# In[ ]:


preventive_measures(data=zio, foryou='Lazio', csp=1.05)


# In[ ]:


lombard = extraction_data(data=inter, region='Lombardia')


# In[ ]:


preventive_measures(data=lombard, foryou='Lombardia', csp=1.05)


# # Italy preventive measures

# In[ ]:


covid = data_region.groupby('Date')[need_feature].agg('sum')
covid = covid.reset_index()
covid.head()


# In[ ]:


italy = extraction_data(data=covid, feature=['TotalPositiveCases'] )


# In[ ]:


preventive_measures(data=italy, foryou='Italy', csp=1.05)


# Next find the period in space and time after determinate a velocity of the spreading of covid-19. soon.

# ## UpNext!
# 
# 

# I recommand this notebook https://www.kaggle.com/paultimothymooney/does-latitude-impact-the-spread-of-covid-19 

# In[ ]:




